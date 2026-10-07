"""Throwaway Chapter Factory rehearsal. Writes only under qa/work.

Collect-all: every producer runs. A failure does not skip the rest.
The canonical chapter trees are not modified.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.adversary import (  # noqa: E402
    ROLES,
    SOURCE,
    _anchors,
    _box,
    _claim,
    _page,
    _pair,
    _render_item,
    make_identity,
)
from chapter_qa.cross_artifact import emit_cross_evidence  # noqa: E402
from chapter_qa.emit import seal  # noqa: E402
from chapter_qa.evidence import evidence_from_dict  # noqa: E402
from chapter_qa.gates import default_release_gates, load_gates  # noqa: E402
from chapter_qa.pdf_fixture import write_pdf  # noqa: E402
from chapter_qa.release_judge import judge  # noqa: E402
from chapter_qa.render_completeness import emit_render_evidence  # noqa: E402
from chapter_qa.schedule_policy import emit_schedule_evidence  # noqa: E402
from chapter_qa.source_audit import emit_source_evidence  # noqa: E402
from chapter_qa.visual_qa import emit_visual_evidence  # noqa: E402
from qa_ooxml import emit_ooxml_gate  # noqa: E402
from qa_pdf_quality import emit_pdf_evidence  # noqa: E402
from qa_status_authority import emit_status_evidence  # noqa: E402

POLICY = "collect-all"


def _touch(folder: Path, name: str) -> str:
    path = folder / "_stubs" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def _clean_spec():
    return {
        "chapter": 2,
        "identityChapter": 2,
        "title": "Moving Objects Have Energy",
        "bigQuestion": "How can an object have energy?",
        "sourceRanges": ["Reader pp. 7-12"],
        "concepts": ["motion", "energy of motion"],
        "exclusions": ["speed-energy relationship"],
        "vocabulary": ["motion", "energy of motion"],
        "anchors": [
            {"code": "BQ", "order": 1, "status": "REQUIRED"},
            {"code": "V1", "order": 2, "status": "REQUIRED"},
            {"code": "N1", "order": 3, "status": "REQUIRED"},
        ],
        "schedule": [{"day": "Wednesday", "token": "REQUIRED"}],
        "inventory": ["notes", "slides", "quiz"],
    }


def _notes():
    row = {
        "pageCount": 3,
        "anchors": ["BQ", "V1", "N1"],
        "vocabulary": ["motion"],
        "blankCount": 4,
        "answerKey": "notes-key",
        "writingSpace": True,
        "forbidden": [],
        "text": ["Moving objects have energy."],
        "secondSystem": False,
        "candidateHash": "a" * 64,
    }
    return dict(row), dict(row)


def _slides():
    row = {
        "slideCount": 4,
        "anchors": ["BQ", "V1", "N1"],
        "vocabulary": ["motion"],
        "speakerNotes": ["N1"],
        "planStatus": True,
        "uncodedAnswer": False,
        "candidateHash": "a" * 64,
    }
    return dict(row), dict(row)


def _leak():
    return [
        {"kind": "slide", "anchor": "N1", "reveals": [], "writes": []},
        {"kind": "student", "anchor": "N1", "reveals": [], "writes": ["wheel"], "prefilled": False},
        {"kind": "slide", "anchor": "N1-key", "reveals": ["wheel"], "writes": ["wheel"]},
    ]


def _fresh():
    return [{
        "label": "notes",
        "sourceHash": "s" * 64,
        "outputHash": "o" * 64,
        "freshHash": "o" * 64,
        "pageCount": 3,
        "expectedPageCount": 3,
        "dimensions": "612x792",
        "expectedDimensions": "612x792",
        "normalizedText": "moving objects have energy",
        "freshText": "moving objects have energy",
    }]


def _mandatory(folder, identity, defects):
    from chapter_qa.mandatory_producers import (
        emit_adversarial_qa,
        emit_answer_leakage,
        emit_chapter_spec,
        emit_fresh_export,
        emit_inventory,
        emit_notes_structure,
        emit_prior_frozen,
        emit_retired_content,
        emit_slides_structure,
    )
    spec = _clean_spec()
    if "spec" in defects:
        spec = dict(spec)
        spec["bigQuestion"] = ""
    notes_e, notes_o = _notes()
    if "notes" in defects:
        notes_o = dict(notes_o)
        notes_o["anchors"] = ["BQ", "BQ", "N1"]
    slides_e, slides_o = _slides()
    if "slides" in defects:
        slides_o = dict(slides_o)
        slides_o["anchors"] = ["BQ"]
        slides_o["slideCount"] = 1
    leak = _leak()
    if "leak" in defects:
        leak = [{"kind": "slide", "anchor": "S0", "reveals": ["wheel"], "writes": []}]
    fresh = _fresh()
    if "fresh" in defects:
        fresh = [dict(fresh[0], outputHash="stale")]
    retired_files = [{"name": "notes.pdf", "text": "Moving objects have energy.", "perceptualHash": "live"}]
    baselines = [{"token": "interactive science notebook", "perceptualHash": "retired-page"}]
    if "retired" in defects:
        retired_files = [{"name": "renamed.pdf", "text": "interactive science notebook", "perceptualHash": "retired-page"}]
    inventory = ["notes", "slides", "quiz"]
    observed_inventory = list(inventory)
    if "inventory" in defects:
        observed_inventory = ["notes", "slides"]
    adversarial = {
        "projectBad": 90, "projectBadGreen": 0, "heldOutBad": 12, "heldOutGreen": 0,
        "clean": 15, "cleanRed": 0, "canonicalRepoTouched": 0, "completed": True,
    }
    if "adversarial" in defects:
        adversarial = dict(adversarial, projectBadGreen=1)
    frozen = {
        "1": {"guard": "6/6", "guardExpected": "6/6", "unreviewed": 0, "stale": 0, "parity": "14/14", "parityExpected": "14/14", "churn": 0},
        "2": {"guard": "PASS", "guardExpected": "PASS", "unreviewed": 0, "stale": 0, "parity": "PASS", "parityExpected": "PASS", "churn": 0},
    }
    if "frozen" in defects:
        frozen = dict(frozen)
        frozen["1"] = dict(frozen["1"], churn=1)
    if "suite" in defects:
        adversarial = _live_adversarial()
        frozen = _live_frozen()
    return {
        "CHAPTER_SPEC": emit_chapter_spec(spec, identity, _touch(folder, "spec-ev.json")),
        "NOTES_STRUCTURE": emit_notes_structure(notes_e, notes_o, identity, _touch(folder, "notes-ev.json")),
        "SLIDES_STRUCTURE": emit_slides_structure(slides_e, slides_o, identity, _touch(folder, "slides-ev.json")),
        "ANSWER_LEAKAGE": emit_answer_leakage(leak, identity, _touch(folder, "leak-ev.json")),
        "FRESH_EXPORT": emit_fresh_export(fresh, identity, _touch(folder, "fresh-ev.json")),
        "RETIRED_CONTENT": emit_retired_content(retired_files, baselines, identity, _touch(folder, "retired-ev.json")),
        "INVENTORY": emit_inventory(inventory, observed_inventory, identity, _touch(folder, "inventory-ev.json")),
        "ADVERSARIAL_QA": emit_adversarial_qa(adversarial, identity, _touch(folder, "adversary-ev.json")),
        "PRIOR_FROZEN_NONREGRESSION": emit_prior_frozen(frozen, identity, _touch(folder, "frozen-ev.json")),
    }


def _live_adversarial():
    from run_adversarial_qa import execute
    _rows, summary = execute(seed=20261006, held_out=True)
    summary = dict(summary)
    summary["completed"] = True
    summary["canonicalRepoTouched"] = summary.get("canonicalTouched", 1)
    return summary


def _live_frozen():
    def run(script, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "tools" / script), *args],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
    guard = run("qa_ch1_note_architecture.py")
    parity1 = run("qa_release_parity.py", "--chapter", "1")
    certify = run("certify_chapter.py", "--chapter", "2")
    golden = run("qa_ch2_golden.py", "--mode", "post-freeze")
    parity2 = run("qa_release_parity.py", "--chapter", "2")
    status = subprocess.run(
        ["git", "status", "--short", "--", "curriculum/chapter-01", "curriculum/chapter-02", "production"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    churn = 0 if status.returncode == 0 and not status.stdout.strip() else 1
    passes = sum(1 for line in parity1.stdout.splitlines() if line.startswith("[PASS]"))
    return {
        "1": {
            "guard": "6/6" if "6/6" in guard.stdout and "unreviewed: 0" in guard.stdout else "FAIL",
            "guardExpected": "6/6",
            "unreviewed": 0 if "unreviewed: 0" in guard.stdout else 1,
            "stale": 0 if "stale allowlist: 0" in guard.stdout else 1,
            "parity": "14/14" if passes == 14 and "OVERALL: PASS" in parity1.stdout else "FAIL",
            "parityExpected": "14/14",
            "churn": churn,
        },
        "2": {
            "guard": "PASS" if certify.returncode == 0 and "OVERALL: PASS" in golden.stdout else "FAIL",
            "guardExpected": "PASS",
            "unreviewed": 0,
            "stale": 0,
            "parity": "PASS" if "OVERALL: PASS" in parity2.stdout else "FAIL",
            "parityExpected": "PASS",
            "churn": churn,
        },
    }


def _filler(gate, identity, evidence_path: str):
    data = {
        "evidenceId": "rehearsal-%s" % gate.gateId.lower(),
        "gateId": gate.gateId,
        "auditorRole": gate.expectedEvidenceRole,
        "performed": True,
        "expectedInputs": ["rehearsal"],
        "observedInputs": ["rehearsal"],
        "thingBeingCertified": "candidate-packet",
        "independentEvidenceSource": "authoritative-reader",
        "findings": [],
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": True,
            "detectorException": False,
            "requiredInputsPresent": True,
            "missingRender": False,
            "missingEvidence": False,
            "stale": False,
            "gateSpecificFailure": False,
            "unavailableEvidence": False,
        },
        "inventory": [{"name": "pages", "expected": 3, "observed": 3}],
    }
    return seal(data, identity, gate)


def produce(mode: str) -> dict:
    defects = {
        "clean": set(),
        "defect": {"render"},
        "multi": {"curriculum", "render", "status"},
    }[mode]
    identity = make_identity("rehearsal-%s" % mode)
    folder = ROOT / "qa" / "work" / "rehearsal" / mode
    if folder.exists():
        import shutil
        shutil.rmtree(folder)
    folder.mkdir(parents=True, exist_ok=True)
    statuses = {}
    stored = {}

    def keep(gate_id, sealed):
        record, result = sealed
        statuses[gate_id] = result.status
        stored[gate_id] = record

    text = SOURCE if "curriculum" not in defects else SOURCE + " and the energy disappears"
    keep("SOURCE_AUTHORITY", emit_source_evidence(
        [_claim(SOURCE)], identity, "SOURCE_AUTHORITY", _touch(folder, "source.json"),
        auditor_role=ROLES["SOURCE_AUTHORITY"],
    ))
    keep("CURRICULUM_CORRECTNESS", emit_source_evidence(
        [_claim(text)], identity, "CURRICULUM_CORRECTNESS", _touch(folder, "curriculum.json"),
        auditor_role=ROLES["CURRICULUM_CORRECTNESS"],
    ))
    keep("NOTES_SLIDES_SYNC", emit_cross_evidence(
        *_pair(_anchors(), _anchors()), identity, "NOTES_SLIDES_SYNC", _touch(folder, "sync.json"),
        auditor_role=ROLES["NOTES_SLIDES_SYNC"],
    ))
    keep("ASSESSMENT_ALIGNMENT", emit_cross_evidence(
        *_pair(_anchors(), _anchors(), "quiz", "quiz_key"), identity, "ASSESSMENT_ALIGNMENT",
        _touch(folder, "assessment.json"), auditor_role=ROLES["ASSESSMENT_ALIGNMENT"],
    ))
    keep("SCHEDULE_POLICY", emit_schedule_evidence(
        [{"day": "Monday", "token": "REQUIRED", "firstExposure": True, "negated": False}],
        identity, _touch(folder, "schedule.json"), auditor_role=ROLES["SCHEDULE_POLICY"],
    ))
    items = [_render_item(1, "e" * 64, ROOT), _render_item(2, "f" * 64, ROOT)]
    observed = items[:1] if "render" in defects else items
    keep("RENDER_COMPLETENESS", emit_render_evidence(
        items, observed, identity, _touch(folder, "render.json"),
        auditor_role=ROLES["RENDER_COMPLETENESS"],
    ))
    keep("RENDERED_VISUAL_QA", emit_visual_evidence(
        [_page([_box()])], identity, _touch(folder, "visual.json"),
        expected_count=1, auditor_role=ROLES["RENDERED_VISUAL_QA"],
    ))
    pdf = folder / "candidate.pdf"
    write_pdf(pdf, [(612, 792, b"BT /F1 24 Tf 72 100 Td (Hello) Tj ET")])
    keep("PDF_QUALITY", emit_pdf_evidence(
        str(pdf), identity, _touch(folder, "pdf.json"),
        {"pageCount": 1, "pageSizePts": (612, 792), "label": mode},
        auditor_role=ROLES["PDF_QUALITY"],
    ))
    docx = folder / "candidate.docx"
    _write_docx(docx)
    ooxml = emit_ooxml_gate(str(docx), identity, _touch(folder, "ooxml.json"))
    statuses["OOXML_FORENSICS"] = ooxml[1].status
    surfaces = [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "manifest", "text": "FROZEN"}]
    if "status" in defects:
        surfaces.append({"kind": "HUMAN_FACING_STATUS", "surfaceId": "callout", "text": "Phase 7.3 remediation candidate"})
    keep("STATUS_AUTHORITY", emit_status_evidence(
        "FROZEN", surfaces, identity, _touch(folder, "status.json"),
        auditor_role=ROLES["STATUS_AUTHORITY"],
    ))
    playbook_left = _anchors()
    playbook_right = _anchors()
    for side in (playbook_left, playbook_right):
        for row in side.values():
            row["required_status"] = "required"
    keep("PLAYBOOK_ALIGNMENT", emit_cross_evidence(
        *_pair(playbook_left, playbook_right, "playbook", "chapter_spec"), identity, "PLAYBOOK_ALIGNMENT",
        _touch(folder, "playbook.json"), auditor_role="CROSS_ARTIFACT_AUDITOR",
    ))
    release = folder / "release"
    release.mkdir(parents=True, exist_ok=True)
    (release / "packet.txt").write_text("chapter-2 rehearsal\n", encoding="utf-8")
    import hashlib
    digest = hashlib.sha256((release / "packet.txt").read_bytes()).hexdigest()
    manifest = {"files": {"packet.txt": digest}, "status": "BUILT_UNCERTIFIED", "expectStatus": "BUILT_UNCERTIFIED"}
    from chapter_qa.release_set import emit_release_evidence
    keep("RELEASE_EXACT_SET", emit_release_evidence(
        ["packet.txt"], release, manifest, identity, _touch(folder, "release.json"),
        original_hashes={"packet.txt": digest},
    ))
    keep("RELEASE_PARITY", emit_release_evidence(
        ["packet.txt"], release, manifest, identity, _touch(folder, "parity.json"),
        gate_id="RELEASE_PARITY", original_hashes={"packet.txt": digest},
    ))
    gate_defects = set(defects)
    if mode == "clean":
        gate_defects.add("suite")
    for gate_id, sealed in _mandatory(folder, identity, gate_defects).items():
        keep(gate_id, sealed)
    checked = [gate for gate in default_release_gates() if gate.gateId in stored]
    records = [evidence_from_dict(stored[gate.gateId]) for gate in checked]
    for gate_id, record in stored.items():
        if gate_id == "OOXML_FORENSICS":
            continue
        (folder / ("%s.json" % gate_id)).write_text(json.dumps(record), encoding="utf-8")
    judgment = judge(default_release_gates(load_gates()), records, identity)
    missing = [gate.gateId for gate in default_release_gates() if gate.gateId not in stored]
    hook = _stop(folder, identity, "chapter ready")
    return {
        "mode": mode,
        "policy": POLICY,
        "defects": sorted(defects),
        "producerStatus": statuses,
        "judge": judgment.status,
        "hook": hook["decision"],
        "hookReason": hook["reason"],
        "hookSeconds": hook.get("seconds"),
        "failedGates": sorted(gate for gate, status in statuses.items() if status != "PASS" and gate != "OOXML_FORENSICS"),
        "missingProducers": missing,
    }


def _write_docx(path: Path) -> None:
    import zipfile
    document = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Hello</w:t></w:r></w:p></w:body></w:document>"""
    content_types = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>"""
    rels = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>"""
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("[Content_Types].xml", content_types)
        package.writestr("_rels/.rels", rels)
        package.writestr("word/document.xml", document)


def _clean_workspace() -> str:
    folder = ROOT / "qa" / "work" / "rehearsal-git"
    if not (folder / ".git").exists():
        folder.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(["git", "init"], cwd=folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        (folder / "README").write_text("clean rehearsal workspace\n", encoding="utf-8")
        subprocess.check_call(["git", "add", "README"], cwd=folder, stdout=subprocess.DEVNULL)
        subprocess.check_call(
            ["git", "-c", "user.email=hook@example", "-c", "user.name=hook", "commit", "-m", "init"],
            cwd=folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    return str(folder)


def _stop(folder: Path, identity, message: str, extra=None) -> dict:
    payload = {
        "hook_event_name": "stop",
        "status": "completed",
        "loop_count": 0,
        "message": message,
        "requestedAction": "chapter_ready" if "ready" in message else None,
        "workspace_roots": [_clean_workspace()],
        "evidenceDirectory": str(folder),
        "build": {
            "buildId": identity.buildId,
            "candidatePath": identity.candidatePath,
            "candidateFreezeId": identity.candidateFreezeId,
            "candidateHash": identity.candidateHash,
            "sourceFreezeId": identity.sourceFreezeId,
            "sourceHash": identity.sourceHash,
            "inputHashes": dict(identity.inputHashes),
        },
        "editedPaths": [],
    }
    if extra:
        payload.update(extra)
    return _hook("tools/hooks/final_release_gate.py", payload)


def _hook(script: str, payload: dict) -> dict:
    started = time.perf_counter()
    completed = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(ROOT / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )
    elapsed = time.perf_counter() - started
    try:
        body = json.loads(completed.stdout)
    except json.JSONDecodeError:
        body = {"decision": "DENY", "reason": "malformed hook output", "stdout": completed.stdout}
    body["exitCode"] = completed.returncode
    body["seconds"] = round(elapsed, 4)
    return body


def protocol() -> dict:
    samples = {
        "allow": ["git status", "git diff", "git diff --check", "git log", "git rev-parse HEAD"],
        "deny": [
            "git reset --hard",
            "git clean -fd",
            "git stash",
            "git restore .",
            "git checkout -- .",
            "git commit -m x",
            "git push",
            "git status && git reset --hard",
            "bash -lc \"git clean -fd\"",
            "eval git reset --hard",
            "python -c \"import os; os.system('git reset --hard')\"",
            "node -e \"require('child_process').execSync('git reset --hard')\"",
            "GIT_DIR=/tmp/evil git diff",
            "git --git-dir=/tmp/evil diff",
            "git --config-env=diff.external=MYVAR diff",
        ],
    }
    results = {"allow": [], "deny": []}
    timings = []
    for command in samples["allow"] + samples["deny"]:
        body = _hook("tools/hooks/protect_git.py", {"command": command, "cwd": str(ROOT)})
        timings.append(body["seconds"])
        bucket = "allow" if command in samples["allow"] else "deny"
        results[bucket].append({"command": command, "decision": body["decision"], "exit": body["exitCode"]})
    edit = _hook("tools/hooks/invalidate_evidence.py", {
        "hook_event_name": "afterFileEdit",
        "file_path": str(ROOT / "docs/planning/NINE_WEEK_SCOPE_SEQUENCE.md"),
        "editedPaths": ["production/premium-notes/hidden.docx"],
        "workspace_roots": [str(ROOT)],
    })
    mcp_denied = _hook("tools/hooks/mcp_policy.py", {
        "mcp_server_name": "figma",
        "tool_name": "use_figma",
        "role": "RELEASE_JUDGE",
    })
    mcp_art = _hook("tools/hooks/mcp_policy.py", {
        "mcp_server_name": "figma",
        "tool_name": "use_figma",
        "role": "VISUAL_ART_DIRECTOR",
    })
    ordinary = _hook("tools/hooks/final_release_gate.py", {"message": "build draft", "hook_event_name": "stop"})
    return {
        "git": results,
        "gitWrong": [row for row in results["allow"] if row["decision"] != "ALLOW"] + [row for row in results["deny"] if row["decision"] != "DENY"],
        "unrelatedEdit": {"decision": edit["decision"], "affected": edit.get("affected"), "pathSource": edit.get("pathSource")},
        "mcpJudge": mcp_denied["decision"],
        "mcpArt": mcp_art["decision"],
        "ordinary": ordinary["decision"],
        "shellMedianSeconds": sorted(timings)[len(timings) // 2],
        "shellWorstSeconds": max(timings),
        "afterEditSeconds": edit["seconds"],
        "beforeMcpSeconds": mcp_denied["seconds"],
        "stopOrdinarySeconds": ordinary["seconds"],
    }


def postcert() -> dict:
    """Clean certification, then a real notes edit hidden behind editedPaths=[]."""
    import tempfile
    clean = produce("clean")
    folder = Path(tempfile.mkdtemp(prefix="rehearse-git-"))
    subprocess.check_call(["git", "init"], cwd=folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    readme = folder / "README"
    readme.write_text("clean\n", encoding="utf-8")
    subprocess.check_call(["git", "add", "README"], cwd=folder, stdout=subprocess.DEVNULL)
    subprocess.check_call(
        ["git", "-c", "user.email=hook@example", "-c", "user.name=hook", "commit", "-m", "init"],
        cwd=folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    notes = folder / "production" / "premium-notes" / "02-ch2-guided-notes.docx"
    notes.parent.mkdir(parents=True)
    notes.write_text("edited after certification\n", encoding="utf-8")
    identity = make_identity("rehearsal-clean")
    hidden = _stop(
        ROOT / "qa" / "work" / "rehearsal" / "clean",
        identity,
        "chapter ready",
        {"workspace_roots": [str(folder)], "editedPaths": []},
    )
    return {"cleanHook": clean["hook"], "afterHiddenEdit": hidden["decision"], "reason": hidden["reason"]}


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "protocol":
        print(json.dumps(protocol(), indent=2))
        return 0
    if mode == "postcert":
        print(json.dumps(postcert(), indent=2))
        return 0
    if mode == "missing":
        folder = ROOT / "qa" / "work" / "rehearsal" / "clean"
        target = folder / "CHAPTER_SPEC.json"
        if target.exists():
            target.unlink()
        identity = make_identity("rehearsal-clean")
        hook = _stop(folder, identity, "chapter ready")
        print(json.dumps({"removed": "CHAPTER_SPEC", "hook": hook["decision"], "reason": hook["reason"]}))
        return 0 if hook["decision"] == "DENY" else 1
    if mode == "failures":
        identity = make_identity("rehearsal-failures")
        folder = ROOT / "qa" / "work" / "rehearsal" / "failures"
        folder.mkdir(parents=True, exist_ok=True)
        names = {
            "spec": "CHAPTER_SPEC", "notes": "NOTES_STRUCTURE", "slides": "SLIDES_STRUCTURE",
            "leak": "ANSWER_LEAKAGE", "fresh": "FRESH_EXPORT", "retired": "RETIRED_CONTENT",
            "inventory": "INVENTORY", "adversarial": "ADVERSARIAL_QA", "frozen": "PRIOR_FROZEN_NONREGRESSION",
        }
        report = {}
        for key, gate_id in names.items():
            sealed = _mandatory(folder, identity, {key})[gate_id]
            report[gate_id] = sealed[1].status
        print(json.dumps(report, indent=2))
        return 0 if all(status == "FAIL" for status in report.values()) else 1
    modes = ["clean", "defect", "multi"] if mode == "all" else [mode]
    summary = [produce(item) for item in modes]
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
