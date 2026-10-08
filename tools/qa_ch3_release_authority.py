#!/usr/bin/env python3
"""Deterministic Chapter 3 release-authority and provenance gate.

Checks the canonical release exact set, source/output/builder parity, isolated
fresh exports, lifecycle status, and the three-way release/chapter/iPad
authority invariant. ``--canaries`` is the default and proves every governed
defect family can make the gate fail in the same run.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
DEFAULT_RELEASE = REPO / "production/releases/chapter-03"
DEFAULT_IPAD = REPO / "qa/ipad-artifact-qa/manifests/ch3-current.json"
CHAPTER_MANIFEST = REPO / "curriculum/chapter-03/CHAPTER_MANIFEST.md"
PRODUCTION_MANIFEST = REPO / "production/PRODUCTION_MANIFEST.md"
EXPECTED_STATUS = "BUILT_UNCERTIFIED"
EXPECTED_BUILDER = "tools/build_ch3_release.py"
EXPECTED_BUILD_ID = "ch3-rebuild-v13-2026-10-07"
EXPECTED_CANDIDATE_HASH = "d76dafca35132352b750416ab068a3945928f9c7365d610fc7bb60dc86d9f2ed"
RETIRED_NAME = "03-ch3-interactive-science-notebook.pdf"
HISTORICAL_NAME = "03-ch3-energy-speed-slides-28.pptx"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tracked(relpath: str) -> bool:
    return subprocess.run(
        ["git", "ls-files", "--error-unmatch", relpath],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_release_names(manifest: dict) -> set[str]:
    return {entry.get("name", "") for entry in manifest.get("files", []) if entry.get("classification") == "CURRENT"}


def exact_set_findings(manifest: dict, observed_names: set[str]) -> list[str]:
    expected = expected_release_names(manifest) | {"README.md", "RELEASE_MANIFEST.json"}
    findings = []
    missing = sorted(expected - observed_names)
    extra = sorted(observed_names - expected)
    if missing:
        findings.append("missing release files: " + ", ".join(missing))
    if extra:
        findings.append("unexpected release files: " + ", ".join(extra))
    names = [entry.get("name") for entry in manifest.get("files", [])]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        findings.append("duplicate CURRENT entries: " + ", ".join(duplicates))
    return findings


def parity_findings(manifest: dict, release_dir: Path) -> list[str]:
    sys.path.insert(0, str(REPO / "tools"))
    import build_ch3_release as builder

    findings = []
    if manifest.get("builder") != EXPECTED_BUILDER:
        findings.append("release manifest builder is not the tracked Chapter 3 release builder")
    builder_path = REPO / EXPECTED_BUILDER
    if not builder_path.is_file() or not tracked(EXPECTED_BUILDER):
        findings.append("tracked release builder is unavailable")
    elif manifest.get("builderSourceHash") != sha256(builder_path):
        findings.append("release-level builder source hash mismatch")
    if manifest.get("buildId") != EXPECTED_BUILD_ID:
        findings.append("build ID mismatch")
    if manifest.get("candidateHash") != EXPECTED_CANDIDATE_HASH:
        findings.append("candidate hash mismatch")

    for entry in manifest.get("files", []):
        name = entry.get("name", "<unnamed>")
        if entry.get("classification") != "CURRENT" or entry.get("status") != "CURRENT":
            findings.append("%s is not classified CURRENT" % name)
        output = release_dir / name
        if not output.is_file():
            findings.append("%s output missing" % name)
            continue
        live_hash = sha256(output)
        if entry.get("rawSHA256") != live_hash or entry.get("sha256") != live_hash:
            findings.append("%s output hash mismatch" % name)
        if entry.get("output") != "production/releases/chapter-03/" + name:
            findings.append("%s output path mismatch" % name)
        if entry.get("builder") != EXPECTED_BUILDER:
            findings.append("%s lacks tracked builder provenance" % name)
        if builder_path.is_file() and entry.get("builderSourceHash") != sha256(builder_path):
            findings.append("%s builder source hash mismatch" % name)

        sources = entry.get("sources") or []
        recorded = entry.get("sourceSHA256") or []
        recorded_legacy = entry.get("source_sha256") or []
        if not sources or len(sources) != len(recorded):
            findings.append("%s source provenance is incomplete" % name)
            continue
        live_source_hashes = []
        live_canonical = []
        for rel in sources:
            source = REPO / rel
            if not source.is_file():
                findings.append("%s source missing: %s" % (name, rel))
                live_source_hashes.append("MISSING")
                live_canonical.append(None)
                continue
            if not tracked(rel):
                findings.append("%s source is untracked: %s" % (name, rel))
            live_source_hashes.append(sha256(source))
            live_canonical.append(builder.canonical_ooxml_hash(source))
        if live_source_hashes != recorded or live_source_hashes != recorded_legacy:
            findings.append("%s source hash drift" % name)
        if live_canonical != entry.get("sourceCanonicalOOXMLHashes"):
            findings.append("%s canonical source OOXML hash drift" % name)
        if entry.get("kind") == "copy" and live_source_hashes and live_hash != live_source_hashes[0]:
            findings.append("%s copied output differs from its master" % name)
        if entry.get("canonicalOOXMLHash") != builder.canonical_ooxml_hash(output):
            findings.append("%s canonical output OOXML hash mismatch" % name)

        upstream = entry.get("upstreamBuilder")
        upstream_hash = entry.get("upstreamBuilderSourceHash")
        if upstream:
            upstream_path = REPO / upstream
            if not upstream_path.is_file() or not tracked(upstream):
                findings.append("%s upstream builder is unavailable or untracked" % name)
            elif upstream_hash != sha256(upstream_path):
                findings.append("%s upstream builder hash mismatch" % name)
        if output.suffix.lower() == ".pdf":
            count = pdf_metadata(output)[0]
        elif output.suffix.lower() == ".pptx":
            count = builder.slide_count(output)
        else:
            count = 0
        if entry.get("pagesOrSlides") != count:
            findings.append("%s page/slide count mismatch" % name)
    return findings


def status_findings(manifest: dict, chapter_text: str, production_text: str, readme_text: str) -> list[str]:
    findings = []
    if manifest.get("status") != EXPECTED_STATUS:
        findings.append("release lifecycle is not BUILT_UNCERTIFIED")
    if "**Lifecycle:** `BUILT_UNCERTIFIED`" not in chapter_text:
        findings.append("chapter manifest lifecycle does not match release authority")
    if "Chapter 3 lifecycle:** v1.3 is `BUILT_UNCERTIFIED`" not in production_text:
        findings.append("production manifest lifecycle does not match release authority")
    if "Status: **BUILT_UNCERTIFIED**" not in readme_text:
        findings.append("release README lifecycle does not match release authority")
    forbidden = [r"STATUS\s*=\s*FROZEN", r"Chapter 3 v1\.3\s+is\s+(?:CERTIFIED|FROZEN)"]
    for pattern in forbidden:
        if re.search(pattern, chapter_text, re.I) or re.search(pattern, readme_text, re.I):
            findings.append("premature current certification/freeze claim")
            break
    return findings


def authority_findings(
    manifest: dict,
    ipad: dict,
    chapter_text: str,
    production_text: str,
) -> list[str]:
    findings = []
    current = expected_release_names(manifest)
    entries = manifest.get("files", [])
    if len(current) != 11 or len(entries) != 11:
        findings.append("canonical current inventory must contain exactly 11 unique artifacts")
    if "production/releases/chapter-03/RELEASE_MANIFEST.json" not in chapter_text:
        findings.append("CHAPTER_MANIFEST does not point to the canonical release manifest")
    if "41-slide" not in chapter_text or "**RETIRED:** `03-ch3-interactive-science-notebook.pdf`" not in chapter_text:
        findings.append("CHAPTER_MANIFEST current/historical classifications are incomplete")
    if "28-slide deck is historical" not in production_text:
        findings.append("PRODUCTION_MANIFEST does not classify the 28-slide deck as historical")
    if manifest.get("builder") != EXPECTED_BUILDER or "manual remediation" in json.dumps(manifest).lower():
        findings.append("release manifest still depends on manual remediation")

    for entry in entries:
        name = str(entry.get("name") or "")
        if name in {RETIRED_NAME, HISTORICAL_NAME} or "interactive-science-notebook" in name or "slides-28" in name:
            findings.append("retired or historical artifact appears CURRENT: " + name)
        required = ("master", "builder", "builderSourceHash", "output", "artifactType", "studentOrTeacher", "pagesOrSlides", "rawSHA256", "status")
        if any(not entry.get(field) for field in required):
            findings.append("CURRENT artifact lacks required provenance: " + name)

    noncurrent = {entry.get("name"): entry.get("classification") for entry in manifest.get("nonCurrent", [])}
    if noncurrent.get(RETIRED_NAME) != "RETIRED":
        findings.append("interactive notebook is not classified RETIRED")
    if noncurrent.get(HISTORICAL_NAME) != "HISTORICAL":
        findings.append("28-slide deck is not classified HISTORICAL")
    development = {entry.get("path"): entry.get("classification") for entry in manifest.get("developmentOnly", [])}
    for path in (
        "production/premium-notes/03-ch3-energy-speed-guided-notes.pdf",
        "production/premium-notes/03-ch3-energy-speed-guided-notes-key.pdf",
        "production/slides/03-ch3-energy-speed-slides.pdf",
    ):
        if development.get(path) != "DEVELOPMENT_ONLY":
            findings.append("non-release preview lacks DEVELOPMENT_ONLY classification: " + path)

    ipad_entries = ipad.get("artifacts", [])
    ipad_names = [Path(str(item.get("sourcePath") or "")).name for item in ipad_entries]
    if set(ipad_names) != current or len(ipad_names) != len(current):
        findings.append("iPad manifest does not account for every CURRENT release artifact exactly once")
    if ipad.get("derivedFrom") != "production/releases/chapter-03/RELEASE_MANIFEST.json":
        findings.append("iPad manifest is not derived from canonical release authority")
    if ipad.get("renderStatus") != "BUILDER_PRODUCED_CURRENT_RELEASE":
        findings.append("iPad manifest still uses temporary-render authority")
    if ipad.get("buildId") != manifest.get("buildId") or ipad.get("candidateHash") != manifest.get("candidateHash"):
        findings.append("iPad manifest build identity disagrees with release authority")
    for item in ipad_entries:
        name = Path(str(item.get("sourcePath") or "")).name
        if name in {RETIRED_NAME, HISTORICAL_NAME}:
            findings.append("iPad manifest references a non-current artifact")
        if "captureRequired" not in item or not item.get("captureReason"):
            findings.append("iPad capture policy is silent for " + name)
        if name.endswith(".pdf") and item.get("captureRequired") is not True:
            findings.append("current PDF excluded from capture: " + name)
        if name.endswith(".pptx") and item.get("captureRequired") is not False:
            findings.append("editable PPTX must defer to its slide PDF capture surface")
    return findings


def pdf_metadata(path: Path) -> tuple[int, tuple[float, float]]:
    completed = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True)
    if completed.returncode != 0:
        return 0, (0.0, 0.0)
    pages = re.search(r"^Pages:\s+(\d+)", completed.stdout, re.M)
    size = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+)", completed.stdout, re.M)
    return (
        int(pages.group(1)) if pages else 0,
        (round(float(size.group(1)), 2), round(float(size.group(2)), 2)) if size else (0.0, 0.0),
    )


def normalized_page_text(path: Path) -> list[str]:
    count = pdf_metadata(path)[0]
    pages = []
    for page in range(1, count + 1):
        completed = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(path), "-"],
            capture_output=True,
            text=True,
        )
        pages.append(re.sub(r"\s+", " ", completed.stdout).strip())
    return pages


def rendered_page_hashes(path: Path) -> list[str]:
    work = Path(tempfile.mkdtemp(prefix="ch3_pdf_render_"))
    try:
        prefix = work / "page"
        completed = subprocess.run(
            ["pdftoppm", "-r", "144", "-png", str(path), str(prefix)],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if completed.returncode != 0:
            return []
        return [sha256(page) for page in sorted(work.glob("page-*.png"))]
    finally:
        shutil.rmtree(work, ignore_errors=True)


def compare_pdf_to_fresh(source: Path, production: Path) -> list[str]:
    sys.path.insert(0, str(REPO / "tools"))
    import build_ch3_release as builder

    work = Path(tempfile.mkdtemp(prefix="ch3_fresh_compare_"))
    fresh = work / "fresh.pdf"
    findings = []
    try:
        builder.isolated_export(source, fresh)
        production_meta = pdf_metadata(production)
        fresh_meta = pdf_metadata(fresh)
        if production_meta != fresh_meta:
            findings.append("page count/size differs from isolated fresh export")
        if normalized_page_text(production) != normalized_page_text(fresh):
            findings.append("page text differs from isolated fresh export")
        production_renders = rendered_page_hashes(production)
        fresh_renders = rendered_page_hashes(fresh)
        if not production_renders or production_renders != fresh_renders:
            findings.append("page renders differ from isolated fresh export")
        return findings
    finally:
        shutil.rmtree(work, ignore_errors=True)


def fresh_export_findings(manifest: dict, release_dir: Path) -> list[str]:
    findings = []
    for entry in manifest.get("files", []):
        source = REPO / str(entry.get("master") or "")
        output = release_dir / str(entry.get("name") or "")
        if output.suffix.lower() != ".pdf" or source.suffix.lower() not in {".docx", ".pptx"}:
            continue
        if not source.is_file() or not output.is_file():
            findings.append("%s missing source/output for fresh export" % entry.get("name"))
            continue
        for detail in compare_pdf_to_fresh(source, output):
            findings.append("%s: %s" % (entry.get("name"), detail))
    return findings


def run_canaries(
    manifest: dict,
    ipad: dict,
    chapter_text: str,
    production_text: str,
    release_dir: Path,
    observed_names: set[str],
) -> tuple[list[tuple[str, str]], int]:
    results = []

    def record(name: str, caught: bool):
        results.append((name, "CAUGHT" if caught else "ESCAPED"))

    bad_chapter = chapter_text.replace("production/releases/chapter-03/RELEASE_MANIFEST.json", "missing-authority.json")
    record("chapter-manifest disagreement", bool(authority_findings(manifest, ipad, bad_chapter, production_text)))

    bad_ipad = copy.deepcopy(ipad)
    bad_ipad["artifacts"].append({
        "artifactId": "retired-notebook",
        "artifactType": "GUIDED_NOTES",
        "sourcePath": "production/archive/retired/chapter-03-pre-v1.3/" + RETIRED_NAME,
        "captureRequired": True,
        "captureReason": "canary",
    })
    record("iPad references non-current artifact", bool(authority_findings(manifest, bad_ipad, chapter_text, production_text)))

    omitted_ipad = copy.deepcopy(ipad)
    omitted_ipad["artifacts"] = omitted_ipad["artifacts"][:-1]
    record("current artifact omitted from capture policy", bool(authority_findings(manifest, omitted_ipad, chapter_text, production_text)))

    retired_current = copy.deepcopy(manifest)
    retired_current["files"][0]["name"] = RETIRED_NAME
    record("retired artifact marked current", bool(authority_findings(retired_current, ipad, chapter_text, production_text)))

    historical_current = copy.deepcopy(manifest)
    historical_current["files"][0]["name"] = HISTORICAL_NAME
    record("historical deck marked current", bool(authority_findings(historical_current, ipad, chapter_text, production_text)))

    manual = copy.deepcopy(manifest)
    manual["builder"] = "manual remediation"
    record("manual-remediation release", bool(authority_findings(manual, ipad, chapter_text, production_text)))

    no_provenance = copy.deepcopy(manifest)
    no_provenance["files"][0].pop("builderSourceHash", None)
    record("missing tracked-builder provenance", bool(authority_findings(no_provenance, ipad, chapter_text, production_text)))

    record("release exact-set extra file", bool(exact_set_findings(manifest, observed_names | {RETIRED_NAME})))

    drift = copy.deepcopy(manifest)
    drift["files"][0]["rawSHA256"] = "0" * 64
    record("release parity hash drift", bool(parity_findings(drift, release_dir)))

    bad_status = copy.deepcopy(manifest)
    bad_status["status"] = "FROZEN"
    readme = (release_dir / "README.md").read_text(encoding="utf-8")
    record("premature status", bool(status_findings(bad_status, chapter_text, production_text, readme)))

    sys.path.insert(0, str(REPO / "tools"))
    import build_ch3_release as builder

    work = Path(tempfile.mkdtemp(prefix="ch3_stale_canary_"))
    try:
        html = work / "stale.html"
        html.write_text("<html><body><h1>STALE CANARY</h1></body></html>", encoding="utf-8")
        stale_pdf = work / "stale.pdf"
        builder.isolated_export(html, stale_pdf)
        source = REPO / "production/worksheets/03-ch3-energy-speed-practice.docx"
        record("stale PDF fresh-export mismatch", bool(compare_pdf_to_fresh(source, stale_pdf)))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    escaped = sum(1 for _, status in results if status == "ESCAPED")
    return results, escaped


def print_gate(name: str, findings: list[str]) -> None:
    status = "PASS" if not findings else "FAIL"
    print("[%s] %s" % (status, name))
    for finding in findings:
        print("  -", finding)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-dir", default=str(DEFAULT_RELEASE))
    parser.add_argument("--ipad-manifest", default=str(DEFAULT_IPAD))
    parser.add_argument("--no-canaries", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Inventory/capture plan only; skip fresh re-export and canaries.")
    args = parser.parse_args()

    release_dir = Path(args.release_dir).resolve()
    ipad_path = Path(args.ipad_manifest).resolve()
    release_manifest_path = release_dir / "RELEASE_MANIFEST.json"
    if not release_manifest_path.is_file() or not ipad_path.is_file():
        print("[FAIL] CH3_RELEASE_AUTHORITY")
        print("  - missing release or iPad manifest")
        raise SystemExit(1)

    manifest = load_json(release_manifest_path)
    ipad = load_json(ipad_path)
    chapter_text = CHAPTER_MANIFEST.read_text(encoding="utf-8")
    production_text = PRODUCTION_MANIFEST.read_text(encoding="utf-8")
    readme_text = (release_dir / "README.md").read_text(encoding="utf-8") if (release_dir / "README.md").is_file() else ""
    observed_names = {path.name for path in release_dir.iterdir()}

    exact = exact_set_findings(manifest, observed_names)
    parity = parity_findings(manifest, release_dir)
    status = status_findings(manifest, chapter_text, production_text, readme_text)
    authority = authority_findings(manifest, ipad, chapter_text, production_text)
    fresh = [] if args.dry_run else fresh_export_findings(manifest, release_dir)

    print_gate("RELEASE_EXACT_SET", exact)
    print_gate("RELEASE_PARITY", parity)
    print_gate("FRESH_EXPORT", fresh)
    print_gate("STATUS_AUTHORITY", status)
    print_gate("CH3_RELEASE_AUTHORITY", authority)

    capture = [item for item in ipad.get("artifacts", []) if item.get("captureRequired") is True]
    excluded = [item for item in ipad.get("artifacts", []) if item.get("captureRequired") is False]
    expected_screens = sum(int(item.get("expectedPages") or 0) for item in capture)
    print("[INVENTORY] current artifacts=%d capture-required=%d excluded=%d expected-screenshots=%d" % (
        len(manifest.get("files", [])), len(capture), len(excluded), expected_screens,
    ))
    for item in excluded:
        print("  - excluded %s: %s" % (item.get("artifactId"), item.get("captureReason")))

    escaped = 0
    if not args.no_canaries and not args.dry_run:
        results, escaped = run_canaries(manifest, ipad, chapter_text, production_text, release_dir, observed_names)
        for name, result in results:
            print("[%s] CANARY %s" % (result, name))
        print("[CANARIES] total=%d escaped=%d" % (len(results), escaped))

    failed = bool(exact or parity or fresh or status or authority or escaped)
    print("OVERALL:", "FAIL" if failed else "PASS")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
