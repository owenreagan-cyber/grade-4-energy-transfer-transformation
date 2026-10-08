#!/usr/bin/env python3
"""Build the canonical Chapter 3 v1.3 release package.

The builder consumes tracked masters, exports every PDF with an isolated
LibreOffice profile, records source and builder provenance, writes the one
canonical release manifest, derives the iPad inventory from that manifest, and
promotes only a candidate that passes the Chapter 3 release-authority preflight.

Usage: .venv/bin/python tools/build_ch3_release.py
"""

from __future__ import annotations

import hashlib
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
REL = REPO / "production/releases/chapter-03"
IPAD_MANIFEST = REPO / "qa/ipad-artifact-qa/manifests/ch3-current.json"
BUILDER_REL = "tools/build_ch3_release.py"
QA_REL = "tools/qa_ch3_release_authority.py"
VERSION = "1.3"
STATUS = "BUILT_UNCERTIFIED"
BUILD_ID = "ch3-rebuild-v13-2026-10-07"
CANDIDATE_SPEC = "docs/chapter-03/CH3_CHAPTER_SPEC.json"
RETIRED_DIR = "production/archive/retired/chapter-03-pre-v1.3/"


def artifact(
    artifact_id: str,
    name: str,
    artifact_type: str,
    audience: str,
    master: str,
    *,
    output_kind: str = "pdf",
    upstream_builder: str | None = None,
    sources: list[str] | None = None,
    title: str | None = None,
    capture_required: bool = True,
    capture_reason: str = "Native-view certification surface.",
) -> dict:
    return {
        "artifactId": artifact_id,
        "name": name,
        "artifactType": artifact_type,
        "audience": audience,
        "master": master,
        "sources": sources or [master],
        "outputKind": output_kind,
        "upstreamBuilder": upstream_builder,
        "title": title,
        "captureRequired": capture_required,
        "captureReason": capture_reason,
    }


CURRENT = [
    artifact(
        "ch3-guided-notes",
        "03-ch3-energy-speed-guided-notes.pdf",
        "GUIDED_NOTES",
        "student",
        "production/premium-notes/03-ch3-energy-speed-guided-notes.docx",
        upstream_builder="tools/build_ch3_guided_notes.py",
    ),
    artifact(
        "ch3-guided-notes-key",
        "03-ch3-energy-speed-guided-notes-key.pdf",
        "GUIDED_NOTES_KEY",
        "teacher",
        "production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx",
        upstream_builder="tools/build_ch3_guided_notes.py",
    ),
    artifact(
        "ch3-slides-deck",
        "03-ch3-energy-speed-slides.pptx",
        "SLIDE_DECK",
        "teacher",
        "production/slides/03-ch3-energy-speed-slides.pptx",
        output_kind="copy",
        upstream_builder="tools/build_ch3_slides.py",
        capture_required=False,
        capture_reason="The editable PPTX is current, but its builder-produced slide PDF is the native-view certification surface.",
    ),
    artifact(
        "ch3-slides",
        "03-ch3-energy-speed-slides.pdf",
        "SLIDE_PDF",
        "teacher",
        "production/slides/03-ch3-energy-speed-slides.pptx",
        upstream_builder="tools/build_ch3_slides.py",
    ),
    artifact(
        "ch3-ramp-it-up",
        "03-ch3-ramp-it-up-student.pdf",
        "LAB",
        "student",
        "production/worksheets/03-ch3-ramp-it-up-student.docx",
        upstream_builder="tools/build_ch3_handouts.py",
    ),
    artifact(
        "ch3-practice",
        "03-ch3-energy-speed-practice.pdf",
        "PRACTICE",
        "student",
        "production/worksheets/03-ch3-energy-speed-practice.docx",
        upstream_builder="tools/build_ch3_handouts.py",
    ),
    artifact(
        "ch3-quiz",
        "03-ch3-energy-speed-quiz.pdf",
        "QUIZ",
        "student",
        "production/quizzes/03-ch3-energy-speed-quiz.docx",
        upstream_builder="tools/build_ch3_handouts.py",
    ),
    artifact(
        "ch3-recovery",
        "03-ch3-absent-student-recovery.pdf",
        "RECOVERY",
        "student",
        "production/worksheets/03-ch3-absent-student-recovery.docx",
        upstream_builder="tools/build_ch3_handouts.py",
    ),
    artifact(
        "ch3-drop-it",
        "03-ch3-drop-it-student.pdf",
        "FLEX_LAB",
        "student",
        "production/worksheets/03-ch3-drop-it-student.docx",
    ),
    artifact(
        "ch3-friday-flex",
        "03-ch3-friday-flex.pdf",
        "FRIDAY_FLEX",
        "student",
        "curriculum/chapter-03/student/03-ch3-friday-flex.md",
        output_kind="markdown",
        title="Chapter 3 Friday FLEX",
    ),
    artifact(
        "ch3-teacher-key",
        "03-ch3-energy-speed-teacher-key.pdf",
        "TEACHER_KEY",
        "teacher",
        "production/answer-keys/03-ch3-ramp-it-up-key.md",
        output_kind="markdown",
        sources=[
            "production/answer-keys/03-ch3-ramp-it-up-key.md",
            "production/answer-keys/03-ch3-drop-it-key.md",
            "production/answer-keys/03-ch3-energy-speed-practice-key.md",
            "production/answer-keys/03-ch3-energy-speed-quiz-key.md",
        ],
        title="Chapter 3 Teacher Key",
    ),
]


CSS = """<style>
@page{size:8.5in 11in;margin:0.65in}
body{font-family:'Helvetica Neue',Arial,sans-serif;font-size:11pt;line-height:1.34;color:#1a1d26}
h1{color:#1B4FC2;font-size:19pt;border-bottom:2px solid #5E8A18;padding-bottom:5px}
h2{color:#1B4FC2;font-size:14pt;margin-top:18px}
h3{color:#2B2F36;font-size:12pt;margin-top:14px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:8.5pt}
th,td{border:1px solid #777;padding:3px 5px;vertical-align:top;text-align:left}
th{background:#1B4FC2;color:#fff}
code{background:#eee;padding:0 2px}
blockquote{color:#444;border-left:4px solid #5E8A18;margin:6px 0;padding-left:10px}
</style>"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_ooxml_hash(path: Path) -> str | None:
    if path.suffix.lower() not in {".docx", ".pptx", ".xlsx"}:
        return None
    digest = hashlib.sha256()
    with zipfile.ZipFile(path) as archive:
        for name in sorted(n for n in archive.namelist() if not n.endswith("/")):
            payload = archive.read(name)
            digest.update(name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(len(payload).to_bytes(8, "big"))
            digest.update(payload)
    return digest.hexdigest()


def tracked(relpath: str) -> bool:
    return subprocess.run(
        ["git", "ls-files", "--error-unmatch", relpath],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def require_inputs() -> None:
    required = {BUILDER_REL, QA_REL, CANDIDATE_SPEC}
    for spec in CURRENT:
        required.update(spec["sources"])
        if spec.get("upstreamBuilder"):
            required.add(spec["upstreamBuilder"])
    missing = [rel for rel in sorted(required) if not (REPO / rel).is_file()]
    if missing:
        raise SystemExit("missing required tracked input(s): " + ", ".join(missing))
    untracked = [rel for rel in sorted(required) if not tracked(rel)]
    if untracked:
        raise SystemExit("release provenance requires tracked input(s): " + ", ".join(untracked))


def isolated_export(source: Path, output: Path) -> None:
    work = Path(tempfile.mkdtemp(prefix="ch3rel_export_"))
    profile = Path(tempfile.mkdtemp(prefix="lo_ch3rel_"))
    try:
        completed = subprocess.run(
            [
                "soffice",
                "--headless",
                "--norestore",
                "-env:UserInstallation=file://" + str(profile),
                "--convert-to",
                "pdf",
                "--outdir",
                str(work),
                str(source),
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if completed.returncode != 0:
            raise RuntimeError("LibreOffice export failed for %s: %s" % (source, completed.stderr[-500:]))
        produced = list(work.glob("*.pdf"))
        if len(produced) != 1:
            raise RuntimeError("expected one PDF for %s; got %s" % (source, [p.name for p in produced]))
        shutil.move(str(produced[0]), output)
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(profile, ignore_errors=True)


def _sanitize_markdown(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.lstrip("- ").startswith("**Artifact:**"):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"(?m)^(\s*)- \[[xX ]\] ", r"\1- ", text)
    text = re.sub(r"`(?:docs|curriculum|production|tools|qa|assets)/[^`]+`", "the matching Chapter 3 resource", text)
    return text


def markdown_bundle_to_pdf(spec: dict, output: Path) -> None:
    import markdown

    parts = ["<h1>%s</h1>" % spec["title"]]
    for index, rel in enumerate(spec["sources"]):
        text = _sanitize_markdown((REPO / rel).read_text(encoding="utf-8"))
        body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
        if spec["artifactType"] == "FRIDAY_FLEX":
            counter = [0]

            def section_break(match):
                counter[0] += 1
                heading = match.group(1)
                if counter[0] == 1 or heading.startswith("Rule check"):
                    return match.group(0)
                return '<h2 style="page-break-before:always">%s</h2>' % heading

            body = re.sub(r"<h2>(.*?)</h2>", section_break, body)
        parts.append(body)
        if index < len(spec["sources"]) - 1:
            parts.append('<div style="page-break-after:always"></div>')
    html = "<!doctype html><html><head><meta charset='utf-8'>%s</head><body>%s</body></html>" % (
        CSS,
        "".join(parts),
    )
    work = Path(tempfile.mkdtemp(prefix="ch3rel_md_"))
    try:
        html_path = work / "chapter3.html"
        html_path.write_text(html, encoding="utf-8")
        isolated_export(html_path, output)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def pdf_page_count(path: Path) -> int:
    completed = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True)
    match = re.search(r"^Pages:\s+(\d+)", completed.stdout, re.M)
    if not match:
        raise RuntimeError("could not read page count from " + str(path))
    return int(match.group(1))


def slide_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return len([name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)])


def _source_provenance(relpaths: list[str]) -> tuple[list[str], list[str | None]]:
    hashes = [sha256(REPO / rel) for rel in relpaths]
    canonical = [canonical_ooxml_hash(REPO / rel) for rel in relpaths]
    return hashes, canonical


def build_into(destination: Path) -> dict:
    destination.mkdir(parents=True, exist_ok=True)
    builder_hash = sha256(REPO / BUILDER_REL)
    files = []
    for spec in CURRENT:
        output = destination / spec["name"]
        master = REPO / spec["master"]
        if spec["outputKind"] == "copy":
            shutil.copy2(master, output)
        elif spec["outputKind"] == "pdf":
            isolated_export(master, output)
        elif spec["outputKind"] == "markdown":
            markdown_bundle_to_pdf(spec, output)
        else:
            raise RuntimeError("unknown output kind " + spec["outputKind"])
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError("builder did not create " + spec["name"])

        source_hashes, source_canonical = _source_provenance(spec["sources"])
        upstream = spec.get("upstreamBuilder")
        count = pdf_page_count(output) if output.suffix.lower() == ".pdf" else slide_count(output)
        entry = {
            "name": spec["name"],
            "classification": "CURRENT",
            "kind": "copy" if spec["outputKind"] == "copy" else "derived",
            "source": spec["master"],
            "master": spec["master"],
            "sources": spec["sources"],
            "sourceSHA256": source_hashes,
            "source_sha256": source_hashes,
            "sourceCanonicalOOXMLHashes": source_canonical,
            "builder": BUILDER_REL,
            "builderSourceHash": builder_hash,
            "upstreamBuilder": upstream,
            "upstreamBuilderSourceHash": sha256(REPO / upstream) if upstream else None,
            "output": "production/releases/chapter-03/" + spec["name"],
            "artifactType": spec["artifactType"],
            "studentOrTeacher": spec["audience"],
            "pagesOrSlides": count,
            "rawSHA256": sha256(output),
            "sha256": sha256(output),
            "canonicalOOXMLHash": canonical_ooxml_hash(output),
            "freshnessMethod": "isolated-libreoffice" if spec["outputKind"] == "pdf" else spec["outputKind"],
            "status": "CURRENT",
            "captureRequired": spec["captureRequired"],
            "captureReason": spec["captureReason"],
        }
        files.append(entry)

    manifest = {
        "schema": "chapter-release-manifest-2.0",
        "chapter": 3,
        "chapterTitle": "Energy and Speed Are Related",
        "version": VERSION,
        "status": STATUS,
        "buildId": BUILD_ID,
        "candidateSpec": CANDIDATE_SPEC,
        "candidateHash": sha256(REPO / CANDIDATE_SPEC),
        "builder": BUILDER_REL,
        "builderSourceHash": builder_hash,
        "files": files,
        "nonCurrent": [
            {
                "name": "03-ch3-interactive-science-notebook.pdf",
                "classification": "RETIRED",
                "location": RETIRED_DIR + "03-ch3-interactive-science-notebook.pdf",
                "status": "NOT_ACTIVE",
            },
            {
                "name": "03-ch3-energy-speed-slides-28.pptx",
                "classification": "HISTORICAL",
                "location": RETIRED_DIR + "03-ch3-energy-speed-slides-28.pptx",
                "status": "NOT_ACTIVE",
            },
        ],
        "developmentOnly": [
            {
                "path": "production/premium-notes/03-ch3-energy-speed-guided-notes.pdf",
                "classification": "DEVELOPMENT_ONLY",
                "note": "Working preview beside the editable master; the builder-produced release PDF is CURRENT.",
            },
            {
                "path": "production/premium-notes/03-ch3-energy-speed-guided-notes-key.pdf",
                "classification": "DEVELOPMENT_ONLY",
                "note": "Working preview beside the editable master; the builder-produced release PDF is CURRENT.",
            },
            {
                "path": "production/slides/03-ch3-energy-speed-slides.pdf",
                "classification": "DEVELOPMENT_ONLY",
                "note": "Working preview beside the editable deck; the builder-produced release slide PDF is CURRENT.",
            },
        ],
        "retired_to": RETIRED_DIR,
    }
    (destination / "RELEASE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (destination / "README.md").write_text(
        "# Chapter 3 v1.3 release package\n\n"
        "Status: **BUILT_UNCERTIFIED**. This directory is generated by "
        "`tools/build_ch3_release.py`; do not edit release files by hand.\n\n"
        "`RELEASE_MANIFEST.json` is the single machine-readable authority. "
        "Guided Notes are primary. The interactive notebook is retired, the "
        "28-slide deck is historical, and neither appears here.\n",
        encoding="utf-8",
    )
    return manifest


def ipad_manifest_from_release(manifest: dict, release_manifest_path: Path) -> dict:
    artifacts = []
    for entry in manifest["files"]:
        landscape = entry["artifactType"] in {"SLIDE_DECK", "SLIDE_PDF"}
        artifact_entry = {
            "artifactId": next(spec["artifactId"] for spec in CURRENT if spec["name"] == entry["name"]),
            "artifactType": entry["artifactType"],
            "sourcePath": entry["output"],
            "masterPath": entry["master"],
            "artifactSHA256": entry["rawSHA256"],
            "expectedPages": entry["pagesOrSlides"],
            "orientation": "landscape" if landscape else "portrait",
            "viewMode": "fit-page",
            "studentOrTeacher": entry["studentOrTeacher"],
            "chapter": 3,
            "captureRequired": entry["captureRequired"],
            "captureReason": entry["captureReason"],
        }
        artifacts.append(artifact_entry)
    return {
        "schema": "ipad-artifact-manifest-1.1",
        "chapter": 3,
        "buildId": manifest["buildId"],
        "candidateHash": manifest["candidateHash"],
        "derivedFrom": "production/releases/chapter-03/RELEASE_MANIFEST.json",
        "releaseManifestSHA256": sha256(release_manifest_path),
        "renderStatus": "BUILDER_PRODUCED_CURRENT_RELEASE",
        "renderNote": "Derived by tools/build_ch3_release.py from the canonical current release inventory.",
        "artifacts": artifacts,
    }


def promote(stage: Path) -> None:
    REL.mkdir(parents=True, exist_ok=True)
    keep = {path.name for path in stage.iterdir()}
    for path in REL.iterdir():
        if path.name not in keep:
            if path.is_file() or path.is_symlink():
                path.unlink()
            else:
                raise RuntimeError("unexpected directory in active release: " + str(path))
    for path in stage.iterdir():
        shutil.copy2(path, REL / path.name)


def refresh_final_delivery_hashes() -> int:
    """Refresh only existing Chapter 3 rows in the shared delivery hash index."""
    csv_path = REPO / "production/final-delivery/RELEASE_HASH_MANIFEST.csv"
    if not csv_path.is_file():
        return 0
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return 0
    changed = 0
    for row in rows[1:]:
        if len(row) < 6 or not row[0].startswith("03-ch3"):
            continue
        target = REPO / row[3]
        if not target.is_file():
            continue
        row[4] = sha256(target)
        row[5] = str(target.stat().st_size)
        changed += 1
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)
    return changed


def main() -> None:
    require_inputs()
    stage = Path(tempfile.mkdtemp(prefix="ch3release_"))
    ipad_candidate = Path(tempfile.mktemp(prefix="ch3-ipad-manifest-", suffix=".json"))
    try:
        manifest = build_into(stage)
        ipad = ipad_manifest_from_release(manifest, stage / "RELEASE_MANIFEST.json")
        ipad_candidate.write_text(json.dumps(ipad, indent=2) + "\n", encoding="utf-8")
        preflight = subprocess.run(
            [
                sys.executable,
                str(REPO / QA_REL),
                "--release-dir",
                str(stage),
                "--ipad-manifest",
                str(ipad_candidate),
                "--no-canaries",
            ],
            cwd=REPO,
        )
        if preflight.returncode != 0:
            raise SystemExit("candidate release failed preflight; active release was not updated")
        promote(stage)
        IPAD_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ipad_candidate, IPAD_MANIFEST)
        refreshed = refresh_final_delivery_hashes()
        print("Chapter 3 release built:", len(manifest["files"]), "current artifacts")
        print("Final-delivery Chapter 3 hash rows refreshed:", refreshed)
        print("Release directory:", REL)
        print("iPad manifest:", IPAD_MANIFEST)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        ipad_candidate.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
