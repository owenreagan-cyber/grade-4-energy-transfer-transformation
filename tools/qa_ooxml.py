"""DOCX and PPTX package forensics.

Structural evidence does not satisfy rendered visual QA.
"""

from __future__ import annotations

import json
import os
import sys
import zipfile
from xml.etree import ElementTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chapter_qa.severity import resolve_severity

NS = {
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
}


def _finding(code, message, context=None):
    decision = resolve_severity(code, context)
    return {"severity": decision["severity"], "code": code, "message": message, "failsGate": decision["failsGate"]}


def inspect_package(path, *, notes_required=False, allow_hidden=False):
    findings = []
    summary = {"parts": [], "slides": [], "notes": [], "hiddenSlides": [], "externalLinks": [], "metadata": {}}
    try:
        package = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        findings.append(_finding("corrupt_xml", "package is not a valid ZIP"))
        return {
            "findings": findings,
            "failsGate": True,
            "satisfiesPdfQuality": False,
            "satisfiesVisualQa": False,
            "summary": summary,
            "commandFailed": True,
        }
    names = set(package.namelist())
    summary["parts"] = sorted(names)
    if "[Content_Types].xml" not in names:
        findings.append(_finding("broken_relationship", "missing [Content_Types].xml"))
    else:
        try:
            root = ElementTree.fromstring(package.read("[Content_Types].xml"))
        except ElementTree.ParseError:
            findings.append(_finding("corrupt_xml", "[Content_Types].xml is not XML"))
            root = None
        if root is not None:
            for node in root.findall("ct:Override", NS):
                part = (node.attrib.get("PartName") or "").lstrip("/")
                if part and part not in names:
                    findings.append(_finding("broken_relationship", "content type points at missing %s" % part))
    required = []
    if any(name.startswith("word/") for name in names):
        required.append("word/document.xml")
    if any(name.startswith("ppt/") for name in names):
        required.append("ppt/presentation.xml")
    for part in required:
        if part not in names:
            findings.append(_finding("broken_relationship", "missing required part %s" % part))
    for name in names:
        if not name.endswith(".rels"):
            continue
        try:
            root = ElementTree.fromstring(package.read(name))
        except ElementTree.ParseError:
            findings.append(_finding("corrupt_xml", "%s is not XML" % name))
            continue
        base = name.rsplit("/_rels/", 1)[0] if "/_rels/" in name else ""
        if base == "_rels":
            base = ""
        for rel in root.findall("rel:Relationship", NS):
            target = rel.attrib.get("Target") or ""
            mode = rel.attrib.get("TargetMode")
            if mode == "External" or target.startswith("http://") or target.startswith("https://"):
                summary["externalLinks"].append(target)
                findings.append(_finding("unexpected_external_link", "external target %s" % target))
                continue
            if target.startswith("../"):
                resolved = os.path.normpath(os.path.join(base, target)).replace("\\", "/")
            else:
                folder = base
                resolved = "/".join(part for part in (folder, target) if part)
            if resolved not in names:
                findings.append(_finding("broken_relationship", "%s target %s is missing" % (name, target)))
    for name in sorted(names):
        if "/slides/slide" in name and name.endswith(".xml"):
            summary["slides"].append(name)
            try:
                root = ElementTree.fromstring(package.read(name))
            except ElementTree.ParseError:
                findings.append(_finding("corrupt_xml", "%s is not XML" % name))
                continue
            hidden = False
            for key, value in root.attrib.items():
                local = key.rsplit("}", 1)[-1]
                if local == "show" and value == "0":
                    hidden = True
                if local == "hidden" and value == "1":
                    hidden = True
            if hidden:
                summary["hiddenSlides"].append(name)
                if not allow_hidden:
                    findings.append(_finding("hidden_slide", "%s is hidden" % name))
        if name.startswith("ppt/notesSlides/") and name.endswith(".xml"):
            summary["notes"].append(name)
        if name.endswith(".xml") and name not in ("[Content_Types].xml",):
            try:
                ElementTree.fromstring(package.read(name))
            except ElementTree.ParseError:
                findings.append(_finding("corrupt_xml", "%s is not XML" % name))
    if notes_required and summary["slides"] and len(summary["notes"]) != len(summary["slides"]):
        findings.append(_finding(
            "speaker_note_mismatch",
            "notes %s != slides %s" % (len(summary["notes"]), len(summary["slides"])),
        ))
    if "docProps/core.xml" in names:
        try:
            core = ElementTree.fromstring(package.read("docProps/core.xml"))
            summary["metadata"] = {node.tag.rsplit("}", 1)[-1]: (node.text or "") for node in list(core)}
        except ElementTree.ParseError:
            findings.append(_finding("corrupt_xml", "core.xml is not XML"))
    package.close()
    return {
        "findings": findings,
        "failsGate": any(item["failsGate"] for item in findings),
        "satisfiesPdfQuality": False,
        "satisfiesVisualQa": False,
        "summary": summary,
        "commandFailed": False,
    }


def write_ooxml_observation(path, evidence_path, *, notes_required=False, allow_hidden=False):
    """Record structural findings. This does not satisfy PDF_QUALITY or visual QA."""
    assessed = inspect_package(path, notes_required=notes_required, allow_hidden=allow_hidden)
    assessed["satisfiesPdfQuality"] = False
    assessed["satisfiesVisualQa"] = False
    with open(evidence_path, "w", encoding="utf-8") as handle:
        json.dump({"findings": assessed["findings"], "summary": {
            "slides": assessed["summary"]["slides"],
            "notes": assessed["summary"]["notes"],
            "hiddenSlides": assessed["summary"]["hiddenSlides"],
            "externalLinks": assessed["summary"]["externalLinks"],
        }, "failsGate": assessed["failsGate"]}, handle)
    return assessed
