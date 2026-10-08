#!/usr/bin/env python3
"""iPad Artifact QA driver (Phase 1.1).

Adds performance modes over the Phase 1 harness while keeping full certification
capability intact:

    --mode preview       fast single-artifact/page capture (NOT certification evidence)
    --mode changed-only  reuse unchanged artifacts from a run-independent cache
    --mode full          every artifact / page / slide (certification standard, no caching)

QA infrastructure only. Never writes over production/curriculum artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QA_APP = REPO / "qa" / "ipad-artifact-qa"
XCODEPROJ = QA_APP / "ScienceArtifactQA.xcodeproj"
TEMP = REPO / "qa" / "temp" / "ipad-artifact-qa"
RUN_CONFIG_PATH = TEMP / "current-run.json"
CH3_RENDER = TEMP / "ch3"
FIXTURES = TEMP / "fixtures"
CACHE_PATH = TEMP / "cache.json"
CACHE_SHOTS = TEMP / "cache-shots"

DEVICE_NAME = "iPad (A16)"
DEVICE_SLUG = "ipad-a16-sim"

DEFAULT_MANIFEST = "qa/ipad-artifact-qa/manifests/ch3-current.json"

MODE_PREVIEW = "preview"
MODE_CHANGED_ONLY = "changed-only"
MODE_FULL = "full"
MODES = (MODE_PREVIEW, MODE_CHANGED_ONLY, MODE_FULL)

# Evidence classes are deliberately distinct from modes: preview and
# changed-only captures may never be packaged as blind-review evidence.
EVIDENCE_CLASS = {
    MODE_PREVIEW: "preview",
    MODE_CHANGED_ONLY: "changed-only",
    MODE_FULL: "certification",
}

CACHE_SCHEMA_VERSION = 1

# Chapter 3 masters -> fresh PDF names (all TEMP_FRESH_RENDER).
CH3_MASTERS = [
    ("production/premium-notes/03-ch3-energy-speed-guided-notes.docx", "03-ch3-energy-speed-guided-notes.pdf"),
    ("production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx", "03-ch3-energy-speed-guided-notes-key.pdf"),
    ("production/worksheets/03-ch3-ramp-it-up-student.docx", "03-ch3-ramp-it-up-student.pdf"),
    ("production/worksheets/03-ch3-energy-speed-practice.docx", "03-ch3-energy-speed-practice.pdf"),
    ("production/quizzes/03-ch3-energy-speed-quiz.docx", "03-ch3-energy-speed-quiz.pdf"),
    ("production/worksheets/03-ch3-absent-student-recovery.docx", "03-ch3-absent-student-recovery.pdf"),
    ("production/slides/03-ch3-energy-speed-slides.pptx", "03-ch3-energy-speed-slides.pdf"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- #
# pure mode / cache logic (unit-tested; no simulator IO)
# --------------------------------------------------------------------------- #
def evidence_class_for(mode: str) -> str:
    return EVIDENCE_CLASS.get(mode, EVIDENCE_CLASS[MODE_FULL])


def parse_pages(spec) -> list[int] | None:
    """Parse a comma/range page spec into a sorted unique list.

    ``None`` / ``""`` -> None; ``"1,2"`` -> [1, 2]; ``"1-3,5"`` -> [1, 2, 3, 5].
    """
    if spec is None:
        return None
    text = str(spec).strip()
    if not text:
        return None
    out: list[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo_s, hi_s = part.split("-", 1)
            lo, hi = int(lo_s.strip()), int(hi_s.strip())
            if hi < lo:
                raise ValueError(f"invalid descending range: {part!r}")
            out.extend(range(lo, hi + 1))
        else:
            out.append(int(part))
    return sorted(set(out))


def cache_key(artifact_id: str, artifact_sha: str, device_slug: str, os_version: str,
              orientation: str, view_mode: str, page_count: int) -> str:
    """Run-independent cache key: artifact hash + device profile + viewer settings."""
    payload = json.dumps(
        {
            "artifactId": artifact_id,
            "artifactSHA256": artifact_sha,
            "deviceSlug": device_slug,
            "osVersion": os_version,
            "orientation": orientation,
            "viewMode": view_mode,
            "pageCount": page_count,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _select_artifacts(artifacts, artifact_sel, slides_spec):
    artifacts = [a for a in artifacts if a.get("captureRequired", True)]
    if artifact_sel:
        matches = [a for a in artifacts if a["artifactId"] == artifact_sel]
        if len(matches) != 1:
            ids = ", ".join(a["artifactId"] for a in artifacts)
            raise ValueError(
                f"unknown artifact {artifact_sel!r} (available: {ids})"
            )
        return matches
    if slides_spec:
        matches = [a for a in artifacts if a["artifactType"] == "SLIDE_PDF"]
        if len(matches) != 1:
            raise ValueError("--slides requires exactly one SLIDE_PDF artifact in the manifest")
        return matches
    raise ValueError("preview mode requires --artifact or --slides")


def _pages_for_preview(artifact, pages_spec, slides_spec) -> list[int]:
    spec = pages_spec if pages_spec is not None else slides_spec
    pages = parse_pages(spec)
    if pages is None:
        pages = [1]  # default first page
    for p in pages:
        if p < 1 or p > artifact["expectedPages"]:
            raise ValueError(
                f"page {p} out of range for {artifact['artifactId']} (1..{artifact['expectedPages']})"
            )
    return pages


def resolve_plan(mode: str, artifacts, cache_entries, device, artifact_sel=None,
                 pages_spec=None, slides_spec=None) -> dict:
    """Return the capture plan for a mode. Pure; no simulator IO.

    ``artifacts`` must carry a ``currentSHA256`` (recomputed file hash) for
    changed-only comparison. Returns::

        {"capture": [{"artifactId", "pages", "currentSHA256"}, ...],
         "cached":  [{"artifactId", "cacheKey", "currentSHA256"}, ...],
         "evidenceClass": "...",
         "errors": [...]}
    """
    capture: list[dict] = []
    cached: list[dict] = []
    errors: list[str] = []
    evidence = evidence_class_for(mode)
    device_slug = device.get("slug", DEVICE_SLUG)
    os_version = device.get("os", "")

    capture_artifacts = [a for a in artifacts if a.get("captureRequired", True)]

    if mode == MODE_FULL:
        for a in capture_artifacts:
            capture.append({
                "artifactId": a["artifactId"],
                "pages": None,
                "currentSHA256": a.get("currentSHA256", a["artifactSHA256"]),
            })
    elif mode == MODE_PREVIEW:
        try:
            selected = _select_artifacts(capture_artifacts, artifact_sel, slides_spec)
            for a in selected:
                pages = _pages_for_preview(a, pages_spec, slides_spec)
                capture.append({
                    "artifactId": a["artifactId"],
                    "pages": pages,
                    "currentSHA256": a.get("currentSHA256", a["artifactSHA256"]),
                })
        except ValueError as e:
            errors.append(str(e))
    elif mode == MODE_CHANGED_ONLY:
        for a in capture_artifacts:
            current = a.get("currentSHA256", a["artifactSHA256"])
            key = cache_key(
                a["artifactId"], current,
                device_slug, os_version,
                a["orientation"], a["viewMode"], a["expectedPages"],
            )
            if key in cache_entries:
                cached.append({"artifactId": a["artifactId"], "cacheKey": key, "currentSHA256": current})
            else:
                capture.append({"artifactId": a["artifactId"], "pages": None, "currentSHA256": current})
    else:
        errors.append(f"unknown mode {mode!r}")

    return {"capture": capture, "cached": cached, "evidenceClass": evidence, "errors": errors}


def screenshot_name(artifact_id: str, artifact_type: str, device_slug: str,
                    orientation: str, view_mode: str, page: int) -> str:
    """Mirror the Swift screenshot filename for duplicate detection in Python tests."""
    prefix = "s" if artifact_type == "SLIDE_PDF" else "p"
    vm = view_mode.replace("_", "-")
    return f"{artifact_id}__{device_slug}__{orientation}__{vm}__{prefix}{page:03d}.png"


def plan_screenshot_names(plan_items, artifacts_by_id, device_slug):
    """Compute screenshot filenames for a plan and report any duplicates."""
    names: list[str] = []
    seen: set[str] = set()
    dups: list[str] = []
    for item in plan_items:
        a = artifacts_by_id[item["artifactId"]]
        pages = item["pages"] or list(range(1, a["expectedPages"] + 1))
        for p in pages:
            n = screenshot_name(a["artifactId"], a["artifactType"], device_slug,
                                a["orientation"], a["viewMode"], p)
            if n in seen:
                dups.append(n)
            seen.add(n)
            names.append(n)
    return names, dups


# --------------------------------------------------------------------------- #
# cache IO (thin wrappers around the pure logic above)
# --------------------------------------------------------------------------- #
def load_cache(path: Path = CACHE_PATH) -> dict:
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    return {"version": CACHE_SCHEMA_VERSION, "entries": {}}


def save_cache(cache: dict, path: Path = CACHE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def recompute_hashes(artifacts, repo: Path):
    """Attach ``currentSHA256`` (live file hash) to each artifact."""
    out = []
    for a in artifacts:
        b = dict(a)
        src = repo / a["sourcePath"]
        b["currentSHA256"] = sha256(src) if src.is_file() else a.get("artifactSHA256")
        out.append(b)
    return out


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_fresh():
    CH3_RENDER.mkdir(parents=True, exist_ok=True)
    for src, _ in CH3_MASTERS:
        src_path = REPO / src
        if not src_path.is_file():
            raise SystemExit(f"missing master: {src}")
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(CH3_RENDER), str(src_path)],
            check=True, capture_output=True,
        )
    summary = []
    for _, pdf_name in CH3_MASTERS:
        pdf = CH3_RENDER / pdf_name
        pages = _pdf_pages(pdf)
        summary.append({"file": pdf_name, "pages": pages, "sha256": sha256(pdf), "status": "TEMP_FRESH_RENDER"})
    print(json.dumps(summary, indent=2))


def _pdf_pages(pdf: Path) -> int:
    out = run(["pdfinfo", str(pdf)]).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    return 0


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
def make_fixtures():
    FIXTURES.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(REPO / "tools"))
    from chapter_qa.pdf_fixture import write_pdf  # local import

    p1 = b"0.5 0.5 0.9 g 50 50 512 692 re f\n0 0 0 g\nBT /F1 24 Tf 72 720 Td (Fixture Page 1) Tj ET"
    p2 = b"0.5 0.5 0.9 g 50 50 512 692 re f\n0 0 0 g\nBT /F1 24 Tf 72 720 Td (Fixture Page 2) Tj ET"
    write_pdf(FIXTURES / "fixture-2page.pdf", [(612, 792, p1), (612, 792, p2)])
    (FIXTURES / "malformed.pdf").write_bytes(b"%PDF-1.4\nthis is not a real pdf\x00\xff\xfe garbage")
    print("fixtures written:", sorted(p.name for p in FIXTURES.iterdir()))


# --------------------------------------------------------------------------- #
# simulator
# --------------------------------------------------------------------------- #
def _simulators():
    out = run(["xcrun", "simctl", "list", "devices", "available", "-j"]).stdout
    return json.loads(out)


def _os_version(runtime_id: str) -> str:
    tag = runtime_id.split(".")[-1]  # e.g. iOS-27-0
    parts = tag.split("-")
    return ".".join(parts[1:]) if len(parts) > 1 else tag


def pick_device():
    data = _simulators()
    candidates = []
    for runtime_id, devices in data.get("devices", {}).items():
        if "iOS" not in runtime_id:
            continue
        for dev in devices:
            if dev.get("name", "").startswith(DEVICE_NAME) and dev.get("isAvailable", False):
                candidates.append((_os_version(runtime_id), runtime_id, dev["udid"], dev["udid"] in _booted_udids()))
    if not candidates:
        raise SystemExit(f"no available simulator named {DEVICE_NAME!r}")
    candidates.sort(key=lambda c: (c[3], c[0]))
    osv, runtime_id, udid, _booted = candidates[0]
    return {"model": DEVICE_NAME, "slug": DEVICE_SLUG, "os": osv, "udid": udid, "runtime": runtime_id}


def _booted_udids() -> set[str]:
    out = run(["xcrun", "simctl", "list", "devices", "booted", "-j"]).stdout
    return {d["udid"] for devs in json.loads(out).get("devices", {}).values() for d in devs}


# --------------------------------------------------------------------------- #
# prepare (run-config)
# --------------------------------------------------------------------------- #
def prepare(mode: str, manifest_path: str, artifact_sel, pages_spec, slides_spec):
    run_id = "ipad-qa-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    output_dir = TEMP / run_id
    device = pick_device()
    manifest_abs = (REPO / manifest_path).resolve()
    manifest = json.loads(manifest_abs.read_text(encoding="utf-8"))
    artifacts = recompute_hashes(manifest["artifacts"], REPO)
    cache = load_cache()
    plan = resolve_plan(mode, artifacts, cache["entries"], device,
                        artifact_sel, pages_spec, slides_spec)

    config = {
        "runId": run_id,
        "buildId": manifest.get("buildId", "unknown"),
        "manifestPath": str(manifest_abs),
        "outputDirPath": str(output_dir),
        "deviceModel": device["model"],
        "deviceSlug": device["slug"],
        "osVersion": device["os"],
        "simulatorUdid": device["udid"],
        "runtimeId": device["runtime"],
        "mode": mode,
        "evidenceClass": plan["evidenceClass"],
        "capturePlan": plan["capture"],
        "cachedArtifacts": plan["cached"],
        "planErrors": plan["errors"],
    }
    RUN_CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(json.dumps(config, indent=2))


# --------------------------------------------------------------------------- #
# test
# --------------------------------------------------------------------------- #
def run_tests():
    config = json.loads(RUN_CONFIG_PATH.read_text(encoding="utf-8"))
    udid = config["simulatorUdid"]
    output_dir = TEMP / config["runId"]
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "screenshots").mkdir(parents=True, exist_ok=True)
    booted = run(["xcrun", "simctl", "list", "devices", "booted", "-j"]).stdout
    if udid not in booted:
        run(["xcrun", "simctl", "boot", udid])
        run(["xcrun", "simctl", "bootstatus", udid, "-b"])
    result_bundle = TEMP / "result.xcresult"
    if result_bundle.exists():
        shutil.rmtree(result_bundle)
    cmd = ["xcodebuild"]
    # Full certification keeps a deterministic clean build; dev modes use the
    # incremental build for faster iteration (certification rigor is unchanged).
    if config.get("mode") == MODE_FULL:
        cmd.append("clean")
    cmd += [
        "test",
        "-project", str(XCODEPROJ),
        "-scheme", "ScienceArtifactQA",
        "-destination", f"platform=iOS Simulator,id={udid}",
        "-resultBundlePath", str(result_bundle),
    ]
    print(" ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(QA_APP), text=True)
    return proc.returncode


# --------------------------------------------------------------------------- #
# post-process
# --------------------------------------------------------------------------- #
def _reemit_cached(entry: dict, config: dict, output_dir: Path) -> list[dict]:
    """Materialize a cached artifact's screenshots into this run and re-emit records."""
    shots_dir = output_dir / "screenshots"
    shots_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for r in entry.get("records", []):
        src_name = Path(r["screenshotPath"]).name
        cache_src = CACHE_SHOTS / entry.get("cacheKey", "") / src_name
        dst = shots_dir / src_name
        if cache_src.is_file():
            shutil.copyfile(cache_src, dst)
        new = dict(r)
        new["runId"] = config["runId"]
        new["buildId"] = config["buildId"]
        new["screenshotPath"] = str(dst)
        out.append(new)
    return out


def update_cache_from_capture(config: dict, artifacts_by_id: dict, records_by_artifact: dict):
    """Cache complete (all-pages) captures from non-preview modes. Never caches
    partial preview captures, so preview evidence can never masquerade as a full
    artifact capture."""
    cache = load_cache()
    device = {"slug": config["deviceSlug"], "os": config["osVersion"], "model": config["deviceModel"]}
    for item in config.get("capturePlan", []):
        if config.get("mode") == MODE_PREVIEW:
            continue
        if item.get("pages") is not None:
            continue  # partial capture — do not cache
        aid = item["artifactId"]
        art = artifacts_by_id.get(aid)
        if not art:
            continue
        recs = records_by_artifact.get(aid, [])
        if len(recs) != art["expectedPages"]:
            continue  # incomplete — do not cache
        key = cache_key(aid, item.get("currentSHA256", art["artifactSHA256"]),
                        device["slug"], device["os"], art["orientation"],
                        art["viewMode"], art["expectedPages"])
        shot_dir = CACHE_SHOTS / key
        shot_dir.mkdir(parents=True, exist_ok=True)
        new_records, paths, hashes = [], [], []
        for r in sorted(recs, key=lambda r: r["pdfPage"]):
            src = Path(r["screenshotPath"])
            dst = shot_dir / src.name
            if src.is_file():
                shutil.copyfile(src, dst)
            nr = dict(r)
            nr["screenshotPath"] = str(dst)
            new_records.append(nr)
            paths.append(str(dst))
            hashes.append(r.get("screenshotSHA256", ""))
        cache["entries"][key] = {
            "artifactId": aid,
            "artifactSHA256": art["artifactSHA256"],
            "device": device["model"],
            "deviceSlug": device["slug"],
            "osVersion": device["os"],
            "orientation": art["orientation"],
            "viewMode": art["viewMode"],
            "zoomScale": recs[0].get("zoomScale") if recs else None,
            "pageCount": art["expectedPages"],
            "screenshotPaths": paths,
            "screenshotHashes": hashes,
            "timestamp": utc(),
            "evidenceClass": config.get("evidenceClass"),
            "cacheKey": key,
            "records": new_records,
        }
    save_cache(cache)


def seed_cache_from_run(manifest_json_path: str):
    """Import a prior run's ``manifest.json`` records into the run-independent cache.

    Lets a previously completed full run seed the cache so ``changed-only`` can
    reuse its screenshots without re-capturing unchanged artifacts.
    """
    data = json.loads(Path(manifest_json_path).read_text(encoding="utf-8"))
    records = data.get("records", [])
    cache = load_cache()
    by_artifact: dict[str, list[dict]] = {}
    for r in records:
        by_artifact.setdefault(r["artifactId"], []).append(r)
    for aid, recs in by_artifact.items():
        recs_sorted = sorted(recs, key=lambda r: r["pdfPage"])
        page_count = len(recs_sorted)
        first = recs_sorted[0]
        key = cache_key(
            aid, first["artifactSHA256"],
            data.get("deviceSlug", DEVICE_SLUG), data.get("osVersion", ""),
            first["orientation"], first["viewMode"], page_count,
        )
        shot_dir = CACHE_SHOTS / key
        shot_dir.mkdir(parents=True, exist_ok=True)
        new_records, paths, hashes = [], [], []
        for r in recs_sorted:
            src = Path(r["screenshotPath"])
            dst = shot_dir / src.name
            if src.is_file():
                shutil.copyfile(src, dst)
            nr = dict(r)
            nr["screenshotPath"] = str(dst)
            new_records.append(nr)
            paths.append(str(dst))
            hashes.append(r.get("screenshotSHA256", ""))
        cache["entries"][key] = {
            "artifactId": aid,
            "artifactSHA256": first["artifactSHA256"],
            "device": data.get("deviceModel", DEVICE_NAME),
            "deviceSlug": data.get("deviceSlug", DEVICE_SLUG),
            "osVersion": data.get("osVersion", ""),
            "orientation": first["orientation"],
            "viewMode": first["viewMode"],
            "zoomScale": first.get("zoomScale"),
            "pageCount": page_count,
            "screenshotPaths": paths,
            "screenshotHashes": hashes,
            "timestamp": utc(),
            "evidenceClass": data.get("evidenceClass", EVIDENCE_CLASS[MODE_FULL]),
            "cacheKey": key,
            "records": new_records,
        }
    save_cache(cache)
    print(json.dumps({"seededArtifacts": len(by_artifact), "totalEntries": len(cache["entries"])}, indent=2))


def postprocess():
    config = json.loads(RUN_CONFIG_PATH.read_text(encoding="utf-8"))
    run_id = config["runId"]
    output_dir = TEMP / run_id
    capture = output_dir / "capture.jsonl"
    lines = [json.loads(l) for l in capture.read_text(encoding="utf-8").splitlines() if l.strip()] \
        if capture.is_file() else []

    manifest_abs = Path(config["manifestPath"])
    manifest = json.loads(manifest_abs.read_text(encoding="utf-8"))
    artifacts_by_id = {a["artifactId"]: a for a in manifest["artifacts"]}

    mode = config.get("mode", MODE_FULL)
    evidence_class = config.get("evidenceClass", EVIDENCE_CLASS[MODE_FULL])

    # Merge cached artifacts (reused from the run-independent cache).
    cache = load_cache()
    cached_records: list[dict] = []
    for c in config.get("cachedArtifacts", []):
        entry = cache["entries"].get(c["cacheKey"])
        if entry:
            cached_records.extend(_reemit_cached(entry, config, output_dir))

    all_records = lines + cached_records

    # Per-artifact expected counts from the plan (capture items + cached items).
    expected = {}
    involved = []
    for item in config.get("capturePlan", []):
        art = artifacts_by_id[item["artifactId"]]
        expected[item["artifactId"]] = (
            len(item["pages"]) if item["pages"] is not None else art["expectedPages"]
        )
        involved.append(item["artifactId"])
    for c in config.get("cachedArtifacts", []):
        entry = cache["entries"].get(c["cacheKey"])
        expected[c["artifactId"]] = entry["pageCount"] if entry else 0
        if c["artifactId"] not in involved:
            involved.append(c["artifactId"])

    counts = {}
    for rec in all_records:
        counts[rec["artifactId"]] = counts.get(rec["artifactId"], 0) + 1

    problems = []
    failed = []
    for aid in involved:
        got = counts.get(aid, 0)
        if got != expected[aid]:
            problems.append(f"{aid}: expected {expected[aid]}, captured {got}")
            failed.append(aid)

    paths = [rec["screenshotPath"] for rec in all_records]
    dups = sorted({p for p in paths if paths.count(p) > 1})

    # Optional harness stats recorded by the Swift walk.
    stats = {}
    stats_file = output_dir / "harness-stats.json"
    if stats_file.is_file():
        try:
            stats = json.loads(stats_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            stats = {}

    final = {
        "runId": run_id,
        "buildId": config["buildId"],
        "mode": mode,
        "evidenceClass": evidence_class,
        "deviceModel": config["deviceModel"],
        "deviceSlug": config["deviceSlug"],
        "osVersion": config["osVersion"],
        "capturedAt": utc(),
        "artifactCount": len(involved),
        "totalScreenshots": len(all_records),
        "totalExpected": sum(expected.values()),
        "launchCount": stats.get("launchCount"),
        "artifactLoads": stats.get("artifactLoads"),
        "captureCount": stats.get("captureCount"),
        "perArtifact": {
            aid: {"expected": expected[aid], "captured": counts.get(aid, 0)}
            for aid in involved
        },
        "problems": problems,
        "duplicateFilenames": dups,
        "records": all_records,
    }
    (output_dir / "manifest.json").write_text(json.dumps(final, indent=2), encoding="utf-8")

    # Differential capture summary (new in Phase 1.1).
    summary = {
        "runId": run_id,
        "mode": mode,
        "evidenceClass": evidence_class,
        "cached": [c["artifactId"] for c in config.get("cachedArtifacts", [])],
        "captured": [i["artifactId"] for i in config.get("capturePlan", [])],
        "failed": failed,
        "launchCount": stats.get("launchCount"),
        "artifactLoads": stats.get("artifactLoads"),
        "captureCount": stats.get("captureCount"),
    }
    (output_dir / "capture-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Blind review: certification-only. Preview / changed-only captures are a
    # different evidence class and are never packaged for blind review.
    blind_note = "blind-review generated" if evidence_class == "certification" else \
        f"blind-review skipped (evidence class '{evidence_class}' is not certification)"
    if evidence_class == "certification":
        blind = output_dir / "blind-review"
        blind.mkdir(exist_ok=True)
        index = []
        for a in manifest["artifacts"]:
            for rec in all_records:
                if rec["artifactId"] != a["artifactId"]:
                    continue
                src = Path(rec["screenshotPath"])
                dst = blind / src.name
                shutil.copyfile(src, dst)
                index.append({
                    "file": src.name,
                    "artifactId": a["artifactId"],
                    "artifactType": a["artifactType"],
                    "purpose": _purpose(a["artifactType"]),
                    "studentOrTeacher": a["studentOrTeacher"],
                    "pageOrSlide": rec["pdfPage"],
                    "chapter": a["chapter"],
                })
        index.sort(key=lambda r: (r["artifactId"], r["pageOrSlide"]))
        (blind / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
        (blind / "README.txt").write_text(_blind_readme(len(index)), encoding="utf-8")

    # Refresh the cache with any newly captured complete artifacts.
    records_by_artifact = {}
    for rec in lines:
        records_by_artifact.setdefault(rec["artifactId"], []).append(rec)
    update_cache_from_capture(config, artifacts_by_id, records_by_artifact)

    print(json.dumps({
        "runId": run_id,
        "mode": mode,
        "evidenceClass": evidence_class,
        "totalScreenshots": len(all_records),
        "totalExpected": sum(expected.values()),
        "cached": summary["cached"],
        "captured": summary["captured"],
        "failed": failed,
        "problems": problems,
        "duplicateFilenames": dups,
        "launchCount": stats.get("launchCount"),
        "artifactLoads": stats.get("artifactLoads"),
        "captureCount": stats.get("captureCount"),
        "blindReview": blind_note,
    }, indent=2))
    return 1 if (problems or dups or failed) else 0


def _purpose(artifact_type: str) -> str:
    return {
        "GUIDED_NOTES": "Guided notes — student fill-in reference",
        "GUIDED_NOTES_KEY": "Guided notes answer key",
        "WORKSHEET": "Worksheet",
        "LAB": "Lab (Ramp It Up 2.0) student sheet",
        "PRACTICE": "Practice",
        "QUIZ": "Quiz",
        "QUIZ_KEY": "Quiz answer key",
        "RECOVERY": "Absent-student recovery / makeup",
        "FLEX": "Friday FLEX",
        "SLIDE_PDF": "Instructional slide (landscape)",
    }.get(artifact_type, artifact_type)


def _blind_readme(n: int) -> str:
    return (
        f"Blind review bundle — {n} images\n\n"
        "Contents: iPad (A16) simulator screenshots of the native PDFKit view only,\n"
        "plus artifact name/purpose and page/slide number.\n\n"
        "Excluded by construction: sensor results, PASS/FAIL reports, builder code,\n"
        "prior findings, known Codex issues, and generator geometry expectations.\n"
    )


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def _add_mode_args(p: argparse.ArgumentParser, suppress: bool = False):
    default = argparse.SUPPRESS if suppress else None
    p.add_argument("--mode", choices=list(MODES), default=default,
                   help="capture mode (default: full)")
    p.add_argument("--artifact", default=default,
                   help="artifact id to capture (preview mode)")
    p.add_argument("--pages", default=default,
                   help="comma page list for the selected artifact (preview mode)")
    p.add_argument("--slides", default=default,
                   help="comma slide list (preview mode; shorthand for the SLIDE_PDF artifact)")
    p.add_argument("--manifest", default=argparse.SUPPRESS if suppress else DEFAULT_MANIFEST,
                   help="manifest path")


def main():
    ap = argparse.ArgumentParser(description="iPad Artifact QA driver (Phase 1.1)")
    _add_mode_args(ap)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("render")
    sub.add_parser("fixtures")
    p_prepare = sub.add_parser("prepare")
    _add_mode_args(p_prepare, suppress=True)
    sub.add_parser("test")
    sub.add_parser("postprocess")
    p_seed = sub.add_parser("seed-cache")
    p_seed.add_argument("--from", dest="from_manifest", required=True,
                        help="prior run manifest.json to import into the cache")
    args = ap.parse_args()

    mode = args.mode or MODE_FULL

    if args.cmd == "render":
        render_fresh()
    elif args.cmd == "fixtures":
        make_fixtures()
    elif args.cmd == "seed-cache":
        seed_cache_from_run(args.from_manifest)
    elif args.cmd == "prepare":
        prepare(mode, args.manifest, args.artifact, args.pages, args.slides)
    elif args.cmd == "test":
        sys.exit(run_tests())
    elif args.cmd == "postprocess":
        sys.exit(postprocess())
    else:
        # End-to-end mode run: prepare -> test -> postprocess.
        prepare(mode, args.manifest, args.artifact, args.pages, args.slides)
        config = json.loads(RUN_CONFIG_PATH.read_text(encoding="utf-8"))
        if config.get("mode") == MODE_CHANGED_ONLY and not config.get("capturePlan"):
            print("changed-only: every artifact is cached — skipping capture (no simulator work)")
        else:
            rc = run_tests()
            if rc != 0:
                sys.exit(rc)
        sys.exit(postprocess())


if __name__ == "__main__":
    main()
