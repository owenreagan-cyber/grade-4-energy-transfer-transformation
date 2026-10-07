"""Dry-run hook and MCP governance tests. No hook file is activated."""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.evidence import compute_evidence_seal, evaluate, evidence_from_dict  # noqa: E402
from chapter_qa.gates import gate_by_id, load_gates  # noqa: E402
from chapter_qa.identity import BuildIdentity  # noqa: E402
from hooks.final_release_gate import decide_stop, main as stop_main  # noqa: E402
from hooks.invalidate_evidence import invalidate_edit  # noqa: E402
from hooks.mcp_policy import (  # noqa: E402
    builder_expected_is_authority,
    failure_cannot_pass,
    judge_may_fetch_missing_evidence,
    local_verification_required,
    may_satisfy_independent_gate,
    role_may_call,
    same_design_state_may_certify,
)
from hooks.protect_git import decide_git, main as git_main  # noqa: E402
from hooks.redact import redact  # noqa: E402
from hooks.validate_evidence import validate_record  # noqa: E402

BUMPED = {
    "SOURCE_AUTHORITY",
    "CURRICULUM_CORRECTNESS",
    "NOTES_SLIDES_SYNC",
    "ASSESSMENT_ALIGNMENT",
    "PLAYBOOK_ALIGNMENT",
    "RENDER_COMPLETENESS",
    "RENDERED_VISUAL_QA",
    "PDF_QUALITY",
    "RELEASE_EXACT_SET",
    "RELEASE_PARITY",
    "STATUS_AUTHORITY",
}

HASH = "a" * 64


def build():
    return BuildIdentity(
        buildId="build-1",
        candidatePath="qa/work/candidate",
        candidateFreezeId="freeze-1",
        candidateHash=HASH,
        sourceFreezeId="src-1",
        sourceHash=HASH,
        inputHashes={"reader": HASH},
    )


def record_for(gate, identity, **overrides):
    data = {
        "schemaVersion": "1.0",
        "evidenceId": "ev-%s" % gate.gateId,
        "gateId": gate.gateId,
        "gateVersion": gate.gateVersion,
        "buildId": identity.buildId,
        "candidatePath": identity.candidatePath,
        "candidateHash": identity.candidateHash,
        "auditorRole": gate.expectedEvidenceRole,
        "status": "FAIL",
        "performed": True,
        "mandatory": gate.mandatory,
        "releaseBlocking": gate.releaseBlocking,
        "startedAt": "2026-10-06T20:00:00Z",
        "completedAt": "2026-10-06T20:05:00Z",
        "expectedInputs": ["reader"],
        "observedInputs": ["reader"],
        "inputHashes": dict(identity.inputHashes),
        "toolVersions": {
            "python": "3.14.7",
            "producer": __import__("chapter_qa.registry", fromlist=["expected_producer"]).expected_producer(gate.gateId)["id"],
            "producerVersion": "1.0",
        },
        "thingBeingCertified": "candidate-packet",
        "independentEvidenceSource": "authoritative-reader",
        "findings": [],
        "evidencePaths": ["qa/gold-standard/evidence.schema.json"],
        "sourceFreezeId": identity.sourceFreezeId,
        "sourceHash": identity.sourceHash,
        "candidateFreezeId": identity.candidateFreezeId,
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
    data.update(overrides)
    data["seal"] = compute_evidence_seal(data)
    return data


@contextmanager
def evidence_dir():
    root = ROOT / "qa" / "work"
    root.mkdir(parents=True, exist_ok=True)
    folder = tempfile.mkdtemp(prefix="hooktest-", dir=root)
    try:
        yield folder
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def isolated_git():
    """A clean git repo so certification tests do not see this checkout's edits."""
    folder = Path(tempfile.mkdtemp(prefix="hook-git-"))
    subprocess.check_call(["git", "init"], cwd=folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (folder / "README").write_text("clean\n", encoding="utf-8")
    subprocess.check_call(["git", "add", "README"], cwd=folder, stdout=subprocess.DEVNULL)
    subprocess.check_call(
        ["git", "-c", "user.email=hook@example", "-c", "user.name=hook", "commit", "-m", "init"],
        cwd=folder,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return str(folder)


def write_packet(payload, directory, lifecycle=None):
    folder = Path(directory)
    for old in folder.glob("*.json"):
        old.unlink()
    for index, row in enumerate(payload["evidence"]):
        (folder / ("%02d.json" % index)).write_text(json.dumps(row), encoding="utf-8")
    body = {key: value for key, value in payload.items() if key != "evidence"}
    body["evidenceDirectory"] = str(folder)
    body.setdefault("editedPaths", [])
    body.setdefault("workspace_roots", [isolated_git()])
    if lifecycle is not None:
        path = folder / "lifecycle.json"
        path.write_text(json.dumps(lifecycle), encoding="utf-8")
        body["lifecyclePath"] = str(path)
    return body


def passing_payload(identity=None):
    identity = identity or build()
    gates = load_gates()
    rows = [record_for(gate, identity) for gate in gates if gate.applicability == "always"]
    from chapter_qa.identity import hash_file
    bound = "qa/gold-standard/evidence.schema.json"
    return {
        "requestedAction": "chapter_ready",
        "evidenceDirectory": None,
        "build": {
            "buildId": identity.buildId,
            "candidatePath": identity.candidatePath,
            "candidateFreezeId": identity.candidateFreezeId,
            "candidateHash": identity.candidateHash,
            "sourceFreezeId": identity.sourceFreezeId,
            "sourceHash": identity.sourceHash,
            "inputHashes": dict(identity.inputHashes),
            "candidateFiles": {bound: hash_file(str(ROOT / bound))},
        },
        "evidence": rows,
    }


class GateVersionAuditTests(unittest.TestCase):
    def test_bumped_gates_are_1_1_and_the_rest_stay_1_0(self):
        gates = load_gates()
        self.assertEqual(len(gates), 27)
        rebump = {"RENDER_COMPLETENESS", "RENDERED_VISUAL_QA", "PDF_QUALITY"}
        for gate in gates:
            if gate.gateId in rebump:
                self.assertEqual(gate.gateVersion, "1.2", gate.gateId)
            elif gate.gateId in BUMPED:
                self.assertEqual(gate.gateVersion, "1.1", gate.gateId)
            else:
                self.assertEqual(gate.gateVersion, "1.0", gate.gateId)

    def test_render_visual_and_pdf_reject_1_1_evidence(self):
        identity = build()
        for gate_id in ("RENDER_COMPLETENESS", "RENDERED_VISUAL_QA", "PDF_QUALITY"):
            gate = gate_by_id(load_gates(), gate_id)
            stale = evidence_from_dict(record_for(gate, identity, gateVersion="1.1", status="PASS"))
            result = evaluate(stale, gate, identity)
            self.assertEqual(result.status, "FAIL", gate_id)
            self.assertIn("GATE_VERSION_MISMATCH", result.codes)

    def test_old_version_evidence_is_rejected(self):
        gate = gate_by_id(load_gates(), "SOURCE_AUTHORITY")
        identity = build()
        stale = evidence_from_dict(record_for(gate, identity, gateVersion="1.0", status="PASS"))
        result = evaluate(stale, gate, identity)
        self.assertEqual(result.status, "FAIL")
        self.assertIn("GATE_VERSION_MISMATCH", result.codes)


class GitProtectionTests(unittest.TestCase):
    def test_read_only_git_is_allowed(self):
        for command in ("git status", "git diff", "git diff --check", "git log", "git rev-parse HEAD"):
            result = decide_git(command)
            self.assertEqual(result["decision"], "ALLOW", command)

    def test_unrelated_command_is_allowed(self):
        self.assertEqual(decide_git("python -m unittest tests/chapter_qa/test_hooks.py")["decision"], "ALLOW")
        self.assertEqual(decide_git("echo git reset --hard")["decision"], "ALLOW")

    def test_destructive_git_is_denied(self):
        for command in (
            "git reset --hard",
            "git clean -fd",
            "git stash",
            "git stash pop",
            "git restore .",
            "git checkout -- .",
        ):
            result = decide_git(command)
            self.assertEqual(result["decision"], "DENY", command)

    def test_authorization_does_not_permit_reset(self):
        result = decide_git("git reset --hard", {
            "workflowAuthorizesCommit": True,
            "ownerAuthorizesPush": True,
            "ownerAuthorizedFreeze": True,
        })
        self.assertEqual(result["decision"], "DENY")

    def test_push_and_commit_require_real_booleans(self):
        self.assertEqual(decide_git("git push")["decision"], "DENY")
        self.assertEqual(decide_git("git commit -m msg")["decision"], "DENY")
        self.assertEqual(decide_git("git push", {"ownerAuthorizesPush": "true"})["decision"], "DENY")
        self.assertEqual(decide_git("git push", {"ownerAuthorizesPush": True})["decision"], "ALLOW")
        self.assertEqual(decide_git("git commit -m msg", {"workflowAuthorizesCommit": True})["decision"], "ALLOW")

    def test_chained_destructive_command_is_denied(self):
        result = decide_git("git status && git clean -fd")
        self.assertEqual(result["decision"], "DENY")
        result = decide_git("git status; git reset --hard")
        self.assertEqual(result["decision"], "DENY")

    def test_quoted_and_wrapped_destructive_commands_are_denied(self):
        self.assertEqual(decide_git('git\t"reset"\t--hard')["decision"], "DENY")
        self.assertEqual(decide_git("bash -lc \"git clean -fd\"")["decision"], "DENY")
        self.assertEqual(decide_git("eval git reset --hard")["decision"], "DENY")
        self.assertEqual(decide_git("FOO=bar git reset --hard")["decision"], "DENY")
        self.assertEqual(decide_git("git status\ngit reset --hard")["decision"], "DENY")
        self.assertEqual(decide_git("git log -S 'git reset'")["decision"], "ALLOW")
        self.assertEqual(decide_git("git -c diff.external='git reset --hard' diff")["decision"], "DENY")
        self.assertEqual(decide_git("GIT_EXTERNAL_DIFF='git reset --hard' git diff")["decision"], "DENY")
        self.assertEqual(decide_git("echo $(git reset --hard)")["decision"], "DENY")
        self.assertEqual(decide_git("echo '$(git reset --hard)'")["decision"], "ALLOW")
        self.assertEqual(decide_git("python -c \"print('git reset --hard')\"")["decision"], "ALLOW")
        self.assertEqual(decide_git("git stash list")["decision"], "ALLOW")
        self.assertEqual(decide_git("git.exe reset --hard")["decision"], "DENY")
        self.assertEqual(decide_git("git \\\nstatus")["decision"], "ALLOW")
        self.assertEqual(decide_git("perl -e 'system(\"git\".\" reset --hard\")'")["decision"], "DENY")
        self.assertEqual(decide_git("printf 'git reset --hard' | sh")["decision"], "DENY")
        self.assertEqual(decide_git("echo Z2l0 | base64 -D | sh")["decision"], "DENY")
        self.assertEqual(decide_git("git -c include.path=/tmp/extra.config diff")["decision"], "DENY")
        self.assertEqual(decide_git("export GIT_EXTERNAL_DIFF=echo; git diff")["decision"], "DENY")
        self.assertEqual(decide_git("echo <(git reset --hard)")["decision"], "DENY")
        self.assertEqual(decide_git("echo ok # $(git reset --hard)")["decision"], "ALLOW")
        self.assertEqual(decide_git("python -c \"print('base64')\"")["decision"], "ALLOW")
        self.assertEqual(decide_git("GIT_DIR=/tmp/evil git diff")["decision"], "DENY")
        self.assertEqual(decide_git("git --git-dir=/tmp/evil diff")["decision"], "DENY")
        self.assertEqual(decide_git("typeset -x GIT_EXTERNAL_DIFF=echo; git diff")["decision"], "DENY")
        self.assertEqual(decide_git("echo 'export git'")["decision"], "ALLOW")
        self.assertEqual(decide_stop({"message": "the build is certified"})["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "why is this build certified"})["decision"], "DENY")
        transcript = Path(tempfile.mkdtemp(prefix="hook-transcript-")) / "turn.jsonl"
        transcript.write_text(json.dumps({"role": "assistant", "text": "chapter ready"}) + "\n", encoding="utf-8")
        from_transcript = decide_stop({
            "hook_event_name": "stop",
            "status": "completed",
            "transcript_path": str(transcript),
        })
        self.assertEqual(from_transcript["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "I froze the chapter"})["decision"], "DENY")
        self.assertEqual(
            decide_git("python -c \"import os; os.system('git reset --hard')\"")["decision"],
            "DENY",
        )

    def test_malformed_command_is_denied(self):
        self.assertEqual(decide_git('git "reset')["decision"], "DENY")
        self.assertEqual(decide_git("")["decision"], "DENY")
        self.assertEqual(decide_git(None)["decision"], "DENY")

    def test_git_hook_does_not_execute(self):
        def boom(*_args, **_kwargs):
            raise AssertionError("git was executed")

        original = subprocess.run
        subprocess.run = boom
        try:
            result = decide_git("git reset --hard")
        finally:
            subprocess.run = original
        self.assertEqual(result["decision"], "DENY")

    def test_cli_dry_run_exit_codes(self):
        previous = sys.stdin
        try:
            sys.stdin = io.StringIO(json.dumps({"command": "git status"}))
            self.assertEqual(git_main([]), 0)
            sys.stdin = io.StringIO(json.dumps({"command": "git reset --hard"}))
            self.assertEqual(git_main([]), 2)
            sys.stdin = io.StringIO("{")
            self.assertEqual(git_main([]), 2)
            self.assertEqual(git_main(["--apply"]), 2)
        finally:
            sys.stdin = previous


class InvalidationTests(unittest.TestCase):
    def test_notes_edit_invalidates_downstream_gates_only(self):
        result = invalidate_edit({
            "path": "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx",
        })
        affected = result["affected"]
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(affected["NOTES_STRUCTURE"], "CANDIDATE_CHANGED")
        self.assertEqual(affected["NOTES_SLIDES_SYNC"], "DEPENDENCY_CHANGED")
        self.assertEqual(affected["RENDERED_VISUAL_QA"], "DEPENDENCY_CHANGED")
        self.assertEqual(affected["RELEASE_PARITY"], "DEPENDENCY_CHANGED")
        for unrelated in ("SOURCE_AUTHORITY", "SLIDES_STRUCTURE", "SCHEDULE_POLICY", "PLAYBOOK_ALIGNMENT"):
            self.assertNotIn(unrelated, affected)

    def test_slides_quiz_and_playbook_are_scoped(self):
        slides = invalidate_edit({"path": "production/slides/02-ch2-moving-objects-have-energy-slides.pptx"})
        self.assertIn("SLIDES_STRUCTURE", slides["affected"])
        self.assertNotIn("NOTES_STRUCTURE", slides["affected"])
        quiz = invalidate_edit({"path": "production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx"})
        self.assertEqual(quiz["affected"]["ASSESSMENT_ALIGNMENT"], "CANDIDATE_CHANGED")
        self.assertNotIn("NOTES_STRUCTURE", quiz["affected"])
        playbook = invalidate_edit({"path": "production/teacher-playbook/unit1-teacher-playbook.docx"})
        self.assertEqual(playbook["affected"]["PLAYBOOK_ALIGNMENT"], "CANDIDATE_CHANGED")
        self.assertNotIn("NOTES_STRUCTURE", playbook["affected"])

    def test_detector_and_gate_version_are_scoped(self):
        pdf = invalidate_edit({"path": "tools/qa_pdf_quality.py"})
        self.assertEqual(pdf["affected"]["PDF_QUALITY"], "AUDITOR_VERSION_CHANGED")
        self.assertIn("FRESH_EXPORT", pdf["affected"])
        self.assertNotIn("SOURCE_AUTHORITY", pdf["affected"])
        versions = invalidate_edit({
            "path": "qa/gold-standard/gates.json",
            "previousGateVersions": {"SOURCE_AUTHORITY": "1.0", "SCHEDULE_POLICY": "1.0"},
            "currentGateVersions": {"SOURCE_AUTHORITY": "1.1", "SCHEDULE_POLICY": "1.0"},
        })
        self.assertEqual(versions["affected"]["SOURCE_AUTHORITY"], "GATE_VERSION_CHANGED")
        self.assertIn("CURRICULUM_CORRECTNESS", versions["affected"])
        self.assertNotEqual(versions["affected"].get("SCHEDULE_POLICY"), "GATE_VERSION_CHANGED")

    def test_unchanged_gate_version_does_not_invalidate(self):
        result = invalidate_edit({
            "path": "qa/gold-standard/gates.json",
            "previousGateVersions": {"SCHEDULE_POLICY": "1.0"},
            "currentGateVersions": {"SCHEDULE_POLICY": "1.0"},
        })
        self.assertEqual(result["affected"], {})

    def test_unrelated_doc_does_not_invalidate(self):
        result = invalidate_edit({"path": "docs/planning/NINE_WEEK_SCOPE_SEQUENCE.md"})
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["affected"], {})
        self.assertEqual(invalidate_edit({"path": "qa/reports/footnote-review.md"})["affected"], {})
        escaped = invalidate_edit({"path": "docs/../production/premium-notes/a.docx"})
        self.assertIn("NOTES_STRUCTURE", escaped["affected"])
        release_notes = invalidate_edit({"path": "production/releases/02-release-notes.docx"})
        self.assertIn("RELEASE_EXACT_SET", release_notes["affected"])
        self.assertNotIn("NOTES_STRUCTURE", release_notes["affected"])
        quiz_slides = invalidate_edit({"path": "production/slides/02-ch2-quiz-slides.pptx"})
        self.assertIn("SLIDES_STRUCTURE", quiz_slides["affected"])
        self.assertNotIn("ASSESSMENT_ALIGNMENT", quiz_slides["affected"])

    def test_expected_inventory_invalidates_release_set(self):
        result = invalidate_edit({"path": "qa/gold-standard/expected-inventory.json"})
        self.assertEqual(result["affected"]["INVENTORY"], "EXPECTED_INVENTORY_CHANGED")
        self.assertIn("RELEASE_EXACT_SET", result["affected"])


class StopHookTests(unittest.TestCase):
    def test_ordinary_responses_are_allowed(self):
        for payload in (
            {"requestedAction": "show_failures"},
            {"requestedAction": "build_draft"},
            {"message": "show me what failed"},
            {"message": "build draft"},
            {"message": "this draft is not chapter ready"},
            {"message": "why did chapter ready fail?"},
            {"message": "the chapter ready gate failed"},
            {"message": "cannot call this chapter ready"},
        ):
            result = decide_stop(payload)
            self.assertEqual(result["decision"], "ALLOW", payload)

    def test_release_claim_without_evidence_is_denied(self):
        result = decide_stop({"message": "chapter ready"})
        self.assertEqual(result["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "chapter is frozen"})["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "INTERNAL RELEASE CERTIFICATION: PASS"})["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "not only is this chapter ready, ship it"})["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "chapter  ready"})["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "why is the chapter ready?"})["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "discuss ready for freeze criteria tomorrow"})["decision"], "DENY")
        self.assertEqual(decide_stop({"message": "chapter\u200b ready"})["decision"], "DENY")
        result = decide_stop({"requestedAction": "freeze_chapter"})
        self.assertEqual(result["decision"], "DENY")

    def test_missing_stale_wrong_build_and_forged_pass_are_denied(self):
        identity = build()
        payload = passing_payload(identity)
        with evidence_dir() as directory:
            missing = dict(payload)
            missing.pop("evidenceDirectory", None)
            self.assertEqual(decide_stop(missing)["decision"], "DENY")
            absent = dict(payload)
            absent["evidenceDirectory"] = str(ROOT / "qa" / "work" / "missing-hook-evidence")
            self.assertEqual(decide_stop(absent)["decision"], "DENY")
            stale = json.loads(json.dumps(payload))
            stale["evidence"][0]["execution"]["stale"] = True
            self.assertEqual(decide_stop(write_packet(stale, directory))["decision"], "DENY")
            wrong = json.loads(json.dumps(payload))
            wrong["build"]["buildId"] = "other-build"
            self.assertEqual(decide_stop(write_packet(wrong, directory))["decision"], "DENY")
            forged = json.loads(json.dumps(payload))
            forged["evidence"] = [forged["evidence"][0]]
            forged["evidence"][0]["status"] = "PASS"
            forged["evidence"][0]["performed"] = False
            forged["judgment"] = {"status": "PASS"}
            self.assertEqual(decide_stop(write_packet(forged, directory))["decision"], "DENY")
            mismatched = json.loads(json.dumps(payload))
            mismatched["evidence"][0]["gateVersion"] = "1.0"
            self.assertEqual(decide_stop(write_packet(mismatched, directory))["decision"], "DENY")
            unknown = json.loads(json.dumps(payload))
            unknown["evidence"][0]["gateId"] = "NOT_A_GATE"
            self.assertEqual(decide_stop(write_packet(unknown, directory))["decision"], "DENY")
            inline = dict(payload)
            inline["evidenceDirectory"] = directory
            self.assertEqual(decide_stop(inline)["decision"], "DENY")

    def test_judge_pass_allows_internal_certification_only(self):
        identity = build()
        payload = passing_payload(identity)
        with evidence_dir() as directory:
            ready = decide_stop(write_packet(payload, directory))
            self.assertEqual(ready["decision"], "ALLOW", ready["reason"])
            recorded = {
                "state": "APPROVED_FOR_FREEZE",
                "externalAuditAccepted": True,
                "buildId": identity.buildId,
            }
            freeze = write_packet(payload, directory, recorded)
            freeze["requestedAction"] = "freeze_chapter"
            freeze["lifecycleState"] = "APPROVED_FOR_FREEZE"
            self.assertEqual(decide_stop(freeze)["decision"], "DENY")
            freeze["ownerAuthorizedFreeze"] = True
            self.assertEqual(decide_stop(freeze)["decision"], "ALLOW")
            unsigned = write_packet(payload, directory, {
                "state": "APPROVED_FOR_FREEZE",
                "externalAuditAccepted": False,
                "buildId": identity.buildId,
            })
            unsigned["requestedAction"] = "freeze_chapter"
            unsigned["lifecycleState"] = "APPROVED_FOR_FREEZE"
            unsigned["ownerAuthorizedFreeze"] = True
            self.assertEqual(decide_stop(unsigned)["decision"], "DENY")
            early = write_packet(payload, directory, {
                "state": "BUILT_UNCERTIFIED",
                "externalAuditAccepted": True,
                "buildId": identity.buildId,
            })
            early["requestedAction"] = "freeze_chapter"
            early["lifecycleState"] = "BUILT_UNCERTIFIED"
            early["ownerAuthorizedFreeze"] = True
            self.assertEqual(decide_stop(early)["decision"], "DENY")
            contradicted = write_packet(payload, directory)
            contradicted["requestedAction"] = "build_draft"
            contradicted["message"] = "chapter ready"
            self.assertEqual(decide_stop(contradicted)["decision"], "DENY")
            dirty = isolated_git()
            notes = Path(dirty) / "production" / "premium-notes" / "02-ch2-guided-notes.docx"
            notes.parent.mkdir(parents=True)
            notes.write_text("changed\n", encoding="utf-8")
            hidden = write_packet(payload, directory)
            hidden["workspace_roots"] = [dirty]
            hidden["editedPaths"] = []
            self.assertEqual(decide_stop(hidden)["decision"], "DENY")
            lied = write_packet(payload, directory)
            lied["workspace_roots"] = [dirty]
            lied["editedPaths"] = []
            lied["affected"] = {}
            self.assertEqual(decide_stop(lied)["decision"], "DENY")
            closed = write_packet(payload, directory)
            closed["failClosed"] = True
            self.assertEqual(decide_stop(closed)["decision"], "DENY")

    def test_failure_modes_deny_certification_and_allow_drafts(self):
        self.assertEqual(decide_stop({"requestedAction": "chapter_ready", "dependencyMissing": True})["decision"], "DENY")
        self.assertEqual(decide_stop({"requestedAction": "build_draft", "dependencyMissing": True})["decision"], "ALLOW")
        self.assertEqual(decide_stop({"requestedAction": "chapter_ready", "timedOut": True})["decision"], "DENY")
        self.assertEqual(decide_stop({"requestedAction": "build_draft", "timedOut": True})["decision"], "ALLOW")
        self.assertEqual(decide_stop(["nope"])["decision"], "DENY")
        self.assertEqual(decide_stop({"requestedAction": "launch"})["decision"], "DENY")

        def crash(*_args, **_kwargs):
            raise RuntimeError("judge crashed")

        identity = build()
        payload = passing_payload(identity)
        with evidence_dir() as directory:
            crashed = write_packet(payload, directory)
            crashed["judgment"] = {"status": "PASS", "blockingReasons": "not-a-list"}
            self.assertEqual(decide_stop(crashed, judge_fn=crash)["decision"], "DENY")

    def test_claimed_fail_status_does_not_hide_a_real_pass(self):
        identity = build()
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        result = validate_record(record_for(gate, identity, status="PASS"), load_gates(), identity)
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(evaluate(evidence_from_dict(record_for(gate, identity)), gate, identity).status, "PASS")

    def test_stop_cli_denies_a_bare_claim(self):
        previous = sys.stdin
        previous_out = sys.stdout
        try:
            sys.stdin = io.StringIO(json.dumps({"message": "chapter ready"}))
            sys.stdout = io.StringIO()
            code = stop_main([])
            written = sys.stdout.getvalue()
        finally:
            sys.stdin = previous
            sys.stdout = previous_out
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(written)["decision"], "DENY")


class AdversaryHookTests(unittest.TestCase):
    def test_hka_cases(self):
        identity = build()
        base = passing_payload(identity)
        with evidence_dir() as directory:
            hka01 = dict(base)
            hka01.pop("evidenceDirectory", None)
            hka02 = json.loads(json.dumps(base))
            hka02["evidence"][0]["execution"]["stale"] = True
            hka03 = json.loads(json.dumps(base))
            hka03["build"]["buildId"] = "wrong-build"
            hka04 = json.loads(json.dumps(base))
            hka04["evidence"][0]["status"] = "PASS"
            hka04["evidence"][0]["performed"] = False
            hka04["judgment"] = {"status": "PASS"}
            hka05 = json.loads(json.dumps(base))
            hka05["evidence"][0]["gateVersion"] = "9.9"
            hka06 = json.loads(json.dumps(base))
            hka06["evidence"] = []
            hka06["judgment"] = {"status": "PASS"}
            denied = {
                "HKA01": decide_stop(hka01),
                "HKA02": decide_stop(write_packet(hka02, directory)),
                "HKA03": decide_stop(write_packet(hka03, directory)),
                "HKA04": decide_stop(write_packet(hka04, directory)),
                "HKA05": decide_stop(write_packet(hka05, directory)),
                "HKA06": decide_stop(write_packet(hka06, directory)),
                "HKA07": decide_git('git \t "reset" \t --hard'),
                "HKA08": decide_git("git status && git reset --hard"),
                "HKA09": decide_stop({"message": "chapter ready"}),
            }
            for name, result in denied.items():
                self.assertEqual(result["decision"], "DENY", name)
            hka10 = decide_stop({"message": "build draft notes for tomorrow"})
            self.assertEqual(hka10["decision"], "ALLOW")
            self.assertEqual(decide_git("git status")["decision"], "ALLOW")


class McpPolicyTests(unittest.TestCase):
    def test_role_separation_and_independence(self):
        self.assertTrue(role_may_call("SOURCE_SCHOLAR", "READ_ONLY_SOURCE"))
        self.assertTrue(role_may_call("VISUAL_ART_DIRECTOR", "DESIGN_WRITE"))
        self.assertFalse(role_may_call("VISUAL_QA_AUDITOR", "DESIGN_WRITE"))
        self.assertFalse(role_may_call("QA_ADVERSARY", "REPOSITORY_WRITE"))
        self.assertFalse(role_may_call("RELEASE_JUDGE", "DESIGN_WRITE"))
        self.assertFalse(role_may_call("RELEASE_JUDGE", "READ_ONLY_SOURCE"))
        self.assertFalse(may_satisfy_independent_gate("VISUAL_QA_AUDITOR", "DESIGN_WRITE"))
        self.assertFalse(may_satisfy_independent_gate("SOURCE_SCHOLAR", "READ_ONLY_SOURCE"))
        self.assertTrue(local_verification_required("DESIGN_WRITE"))
        self.assertTrue(failure_cannot_pass("DESIGN_WRITE"))
        self.assertFalse(builder_expected_is_authority("CURRICULUM_AUDITOR"))
        self.assertFalse(judge_may_fetch_missing_evidence("RELEASE_JUDGE"))
        self.assertFalse(same_design_state_may_certify("VISUAL_ART_DIRECTOR", "VISUAL_QA_AUDITOR"))
        from hooks.mcp_policy import authorize_mcp
        self.assertFalse(authorize_mcp("QA_ADVERSARY", "figma", "READ_ONLY_REVIEW"))
        self.assertFalse(authorize_mcp("RELEASE_JUDGE", "github"))
        self.assertFalse(authorize_mcp("SOURCE_SCHOLAR", "github"))
        self.assertFalse(authorize_mcp("QA_ADVERSARY", "github"))

    def test_redaction_keeps_environment_names(self):
        cleaned = redact("token=github_pat_examplevalue FIGMA_TOKEN sk-abcdef123456")
        self.assertNotIn("github_pat_examplevalue", cleaned)
        self.assertNotIn("sk-abcdef123456", cleaned)
        self.assertIn("[REDACTED]", cleaned)
        self.assertIn("FIGMA_TOKEN", redact("auth=FIGMA_TOKEN"))
        self.assertNotIn("abcdefghijklmnop", redact("Authorization: Bearer abcdefghijklmnop"))
        self.assertNotIn("secret value", redact('token="super secret value"'))
        self.assertNotIn("SUPER_SECRET_VALUE", redact("password=SUPER_SECRET_VALUE"))
        self.assertIn("${FIGMA_TOKEN}", redact("token=${FIGMA_TOKEN}"))
        self.assertNotIn("secret value", redact('Bearer "super secret value"'))
        self.assertNotIn("gho_AbCdEfGh1234567890abcdef", redact("gho_AbCdEfGh1234567890abcdef"))

    def test_example_config_is_inactive_and_has_no_secret(self):
        example = json.loads((ROOT / "docs" / "gold-standard" / "mcp.example.json").read_text(encoding="utf-8"))
        self.assertTrue(example["exampleOnly"])
        self.assertFalse(example["active"])
        text = json.dumps(example)
        self.assertNotIn("github_pat_", text)
        self.assertNotIn("sk-", text)
        hooks = json.loads((ROOT / ".cursor" / "hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(hooks["version"], 1)
        commands = {name: row[0]["command"] for name, row in hooks["hooks"].items()}
        self.assertIn("tools/hooks/protect_git.py", commands["beforeShellExecution"])
        self.assertIn("tools/hooks/invalidate_evidence.py", commands["afterFileEdit"])
        self.assertIn("tools/hooks/final_release_gate.py", commands["stop"])
        self.assertIn("tools/hooks/mcp_policy.py", commands["beforeMCPExecution"])
        self.assertTrue(hooks["hooks"]["stop"][0]["failClosed"])
        self.assertFalse((ROOT / ".cursor" / "mcp.json").exists())

    def test_governance_doc_states_the_independence_rule(self):
        text = (ROOT / "docs" / "gold-standard" / "MCP_GOVERNANCE.md").read_text(encoding="utf-8")
        for needle in (
            "READ_ONLY_SOURCE",
            "DESIGN_WRITE",
            "REPOSITORY_WRITE",
            "EXTERNAL_ACTION",
            "DEFER",
            "NOT CONFIGURED",
            "local",
        ):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
