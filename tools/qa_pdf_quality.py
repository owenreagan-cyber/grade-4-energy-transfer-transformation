"""PDF structural and image-quality evidence.

Opening a PDF is not a quality pass. Thresholds live in qa/gold-standard/dpi_policy.json.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chapter_qa.emit import seal
from chapter_qa.severity import resolve_severity

POLICY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "qa", "gold-standard", "dpi_policy.json")


def load_dpi_policy(path=None):
    with open(path or POLICY_PATH, encoding="utf-8") as handle:
        return json.load(handle)["classes"]


def effective_dpi(pixel_width, pixel_height, placed_width_in, placed_height_in):
    if placed_width_in <= 0 or placed_height_in <= 0:
        raise ValueError("placed size must be positive")
    return (pixel_width / placed_width_in, pixel_height / placed_height_in)


def classify_dpi(dpi_x, dpi_y, image_class, *, essential=False, policy=None):
    rules = (policy or load_dpi_policy())[image_class]
    worst = min(dpi_x, dpi_y)
    if worst >= rules["passDpi"]:
        band = "pass"
    elif worst >= rules["failDpi"]:
        band = "warn"
    else:
        band = "fail"
    finding = None
    fails_gate = essential and worst < rules["passDpi"]
    if image_class == "print-instructional" and worst < rules["failDpi"]:
        fails_gate = True
    if band == "warn":
        code = "low_effective_dpi_essential" if fails_gate else "low_effective_dpi"
        decision = resolve_severity(code)
        finding = {
            "severity": decision["severity"],
            "code": code,
            "message": "effective DPI %.1f is below the pass threshold" % worst,
            "failsGate": fails_gate or decision["failsGate"],
        }
    elif band == "fail":
        code = "low_effective_dpi_essential" if essential or fails_gate else "low_effective_dpi"
        decision = resolve_severity(code)
        finding = {
            "severity": decision["severity"],
            "code": code,
            "message": "effective DPI %.1f is below the fail threshold" % worst,
            "failsGate": True if fails_gate else decision["failsGate"],
        }
    return {"band": band, "worst": worst, "threshold": rules, "finding": finding, "essential": essential}


def _run(command):
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        return {"missing_tool": command[0], "error": str(exc), "code": 127, "stdout": "", "stderr": ""}
    return {"code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "missing_tool": None}


def _pdfinfo(text):
    info = {}
    pages = []
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    if "Pages" in info:
        info["pageCount"] = int(info["Pages"])
    size = info.get("Page size", "")
    match = re.search(r"([0-9.]+) x ([0-9.]+) pts", size)
    if match:
        pages.append((float(match.group(1)), float(match.group(2))))
    info["pageSizes"] = pages
    return info


def _pdffonts(text):
    fonts = []
    lines = text.splitlines()
    if not lines:
        return fonts
    header = lines[0]
    emb_at = header.find("emb")
    if emb_at < 0:
        return fonts
    for line in lines[2:]:
        if not line.strip() or len(line) <= emb_at:
            continue
        token = line[emb_at:emb_at + 3].strip().lower()
        fonts.append({"name": line.split()[0], "embedded": token.startswith("yes"), "raw": line})
    return fonts


def _pdfimages(text):
    images = []
    lines = text.splitlines()
    header = None
    for line in lines:
        if "x-ppi" in line and "width" in line:
            header = line
            continue
        if header and re.match(r"\s*\d+", line):
            parts = line.split()
            if len(parts) < 5:
                continue
            image = {"page": int(parts[0]), "type": parts[2], "width": int(parts[3]), "height": int(parts[4]), "raw": line}
            if "x-ppi" in header:
                columns = header.split()
                values = line.split()
                if "x-ppi" in columns and len(values) > columns.index("x-ppi"):
                    try:
                        image["xPpi"] = float(values[columns.index("x-ppi")])
                        image["yPpi"] = float(values[columns.index("y-ppi")])
                    except ValueError:
                        pass
            images.append(image)
    return images


def _extract_text(path):
    """Text presence comes from pdftotext. Content streams may be compressed."""
    extracted = _run(["pdftotext", path, "-"])
    if extracted.get("missing_tool") or extracted.get("code") not in (0,):
        return extracted, ""
    return extracted, extracted.get("stdout") or ""


def collect_pdf_tools(path):
    qpdf = _run(["qpdf", "--check", path])
    info = _run(["pdfinfo", path])
    fonts = _run(["pdffonts", path])
    images = _run(["pdfimages", "-list", path])
    extracted, text = _extract_text(path)
    chars = len(re.sub(r"\s+", "", text))
    return {
        "qpdf": qpdf,
        "pdfinfo": _pdfinfo(info["stdout"]) if info["code"] == 0 else {"error": info["stderr"], "pageCount": None, "pageSizes": []},
        "fonts": _pdffonts(fonts["stdout"]) if fonts["code"] == 0 else [],
        "images": _pdfimages(images["stdout"]) if images["code"] == 0 else [],
        "toolFailure": any(item.get("missing_tool") for item in (qpdf, info, fonts, images, extracted)),
        "qpdfCode": qpdf["code"],
        "hasText": chars > 0,
        "textChars": chars,
    }


def assess_pdf(path, expectations, tool_output=None, policy=None):
    output = tool_output if tool_output is not None else collect_pdf_tools(path)
    findings = []
    fails = False

    def add(code, message, context=None):
        nonlocal fails
        decision = resolve_severity(code, context)
        findings.append({"severity": decision["severity"], "code": code, "message": message, "failsGate": decision["failsGate"]})
        fails = fails or decision["failsGate"]

    if output.get("toolFailure"):
        add("corrupt_pdf", "a required PDF tool is missing")
        return {"findings": findings, "failsGate": True, "output": output, "commandFailed": True}
    if output.get("qpdfCode") not in (0, 3):
        add("corrupt_pdf", "qpdf rejected the file")
    expected_pages = expectations.get("pageCount")
    actual_pages = output["pdfinfo"].get("pageCount")
    if expected_pages is not None and actual_pages != expected_pages:
        add("missing_release_artifact", "page count %s != expected %s" % (actual_pages, expected_pages))
    expected_size = expectations.get("pageSizePts")
    sizes = output["pdfinfo"].get("pageSizes") or []
    if len(set(sizes)) > 1:
        add("corrupt_pdf", "page sizes are inconsistent")
    if expected_size and sizes:
        width, height = sizes[0]
        if abs(width - expected_size[0]) > 1 or abs(height - expected_size[1]) > 1:
            add("missing_release_artifact", "page size %s x %s is not %s" % (width, height, expected_size))
    for font in output.get("fonts") or []:
        if not font.get("embedded"):
            add("font_not_embedded", "font %s is not embedded" % font.get("name"))
    page_area = None
    if sizes:
        page_area = (sizes[0][0] / 72.0) * (sizes[0][1] / 72.0)
    for image in output.get("images") or []:
        if image.get("type") == "smask":
            continue
        if "xPpi" in image and "yPpi" in image and image["xPpi"] and image["yPpi"]:
            image_class = expectations.get("imageClass", "print-instructional")
            essential = expectations.get("essentialImage", False)
            if page_area:
                placed = (image["width"] / image["xPpi"]) * (image["height"] / image["yPpi"])
                if placed / page_area >= 0.9:
                    image_class = "decorative"
                    essential = False
            classified = classify_dpi(
                image["xPpi"], image["yPpi"], image_class,
                essential=essential, policy=policy,
            )
            if classified["finding"]:
                findings.append(classified["finding"])
                fails = fails or classified["finding"]["failsGate"]
    if expectations.get("textRequired") and output.get("hasText") is False:
        add("missing_release_artifact", "required text is absent")
        add("image_only_page", "page has no text")
    placements = expectations.get("placements") or []
    for placement in placements:
        dpi_x, dpi_y = effective_dpi(
            placement["pixelWidth"], placement["pixelHeight"],
            placement["placedWidthIn"], placement["placedHeightIn"],
        )
        classified = classify_dpi(
            dpi_x, dpi_y, placement.get("imageClass", "print-instructional"),
            essential=placement.get("essential", False), policy=policy,
        )
        record = {
            "pixelWidth": placement["pixelWidth"],
            "pixelHeight": placement["pixelHeight"],
            "placedWidthIn": placement["placedWidthIn"],
            "placedHeightIn": placement["placedHeightIn"],
            "effectiveDpiX": dpi_x,
            "effectiveDpiY": dpi_y,
            "band": classified["band"],
        }
        if classified["finding"]:
            finding = dict(classified["finding"])
            finding["placement"] = record
            findings.append(finding)
            fails = fails or finding["failsGate"]
    return {"findings": findings, "failsGate": fails, "output": output, "commandFailed": False}


def emit_pdf_evidence(path, identity, evidence_path, expectations, *, auditor_role=None, invalidation_reasons=None):
    if not str(path).lower().endswith(".pdf"):
        assessed = {
            "findings": [{"severity": "BLOCKING", "code": "corrupt_pdf", "message": "PDF quality requires a .pdf file", "failsGate": True}],
            "failsGate": True,
            "output": {"pdfinfo": {"pageCount": 0}, "qpdfCode": 2},
            "commandFailed": True,
        }
    else:
        assessed = assess_pdf(path, expectations, tool_output=None)
    page_count = (assessed["output"].get("pdfinfo") or {}).get("pageCount") or 0
    expected_pages = expectations.get("pageCount") or 0
    data = {
        "evidenceId": "pdf-quality",
        "gateId": "PDF_QUALITY",
        "auditorRole": auditor_role,
        "performed": True,
        "expectedInputs": ["pdf:%s" % expectations.get("label", "candidate")],
        "observedInputs": [] if assessed["commandFailed"] or assessed["failsGate"] else ["pdf:%s" % expectations.get("label", "candidate")],
        "thingBeingCertified": "candidate-pdf:%s" % identity.candidateHash,
        "independentEvidenceSource": "qpdf-pdfinfo:%s" % identity.candidateHash,
        "findings": [{"severity": item["severity"], "code": item["code"], "message": item["message"]} for item in assessed["findings"]],
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": list(invalidation_reasons or []),
        "execution": {
            "succeeded": not assessed["commandFailed"] and assessed["output"].get("qpdfCode") in (0, 3, None),
            "detectorException": assessed["commandFailed"],
            "requiredInputsPresent": not assessed["commandFailed"],
            "missingRender": False,
            "missingEvidence": assessed["commandFailed"],
            "stale": bool(invalidation_reasons),
            "gateSpecificFailure": assessed["failsGate"],
            "unavailableEvidence": False,
        },
        "inventory": [{
            "name": "pdfPages",
            "expected": expected_pages,
            "observed": page_count if not assessed["commandFailed"] else 0,
        }],
    }
    if expected_pages <= 0:
        data["expectedInputs"] = []
        data["observedInputs"] = []
    return seal(data, identity, producer=True)
