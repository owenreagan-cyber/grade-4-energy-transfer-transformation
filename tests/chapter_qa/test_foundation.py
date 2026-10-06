"""Platform tests for the Chapter Factory certification foundation."""

from __future__ import annotations

import ast
import builtins
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.completeness import assess_completeness  # noqa: E402
from chapter_qa.evidence import (  # noqa: E402
    GATE_STATUSES,
    REQUIRED_FIELDS,
    evaluate,
    evidence_from_dict,
    is_self_evidence,
    validate_evidence_dict,
)
from chapter_qa.gates import REQUIRED_GATE_FIELDS, default_release_gates, load_gates  # noqa: E402
from chapter_qa.identity import BuildIdentity, association_hash  # noqa: E402
from chapter_qa.invalidation import (  # noqa: E402
    INVALIDATION_REASONS,
    expected_inventory_changed,
    propagate,
    tool_versions_changed,
)
from chapter_qa.lifecycle import (  # noqa: E402
    STATES,
    compare_frozen_bytes,
    frozen_classroom_change_permitted,
    legal_transition,
    transition_to_frozen_allowed,
)
from chapter_qa.release_judge import (  # noqa: E402
    CERTIFICATION_FAIL,
    CERTIFICATION_PASS,
    judge,
)
from chapter_qa.roles import (  # noqa: E402
    AGENT_ROLE_MAP,
    CAPABILITIES,
    may_issue_release_certification,
)

HASH_A = "a" * 64
HASH_B = "b" * 64


def build(build_id="build-A", candidate_hash=HASH_A, notes_hash=HASH_A):
    return BuildIdentity(
        buildId=build_id,
        candidatePath="candidate/chapter-x",
        candidateFreezeId="cand-1" if build_id == "build-A" else "cand-2",
        candidateHash=candidate_hash,
        sourceFreezeId="src-1",
        sourceHash=HASH_A,
        inputHashes={"notes": notes_hash, "reader": HASH_A},
    )


def execution(**overrides):
    facts = {
        "succeeded": True,
        "detectorException": False,
        "requiredInputsPresent": True,
        "missingRender": False,
        "missingEvidence": False,
        "stale": False,
        "gateSpecificFailure": False,
        "unavailableEvidence": False,
    }
    facts.update(overrides)
    return facts


def evidence_dict(**overrides):
    overrides = dict(overrides)
    facts = execution(**overrides.pop("execution", {}))
    identity = build()
    data = {
        "schemaVersion": "1.0",
        "evidenceId": "ev-1",
        "gateId": "CURRICULUM_CORRECTNESS",
        "gateVersion": "1.0",
        "buildId": identity.buildId,
        "candidatePath": identity.candidatePath,
        "candidateHash": identity.candidateHash,
        "auditorRole": "CURRICULUM_AUDITOR",
        "status": "PASS",
        "performed": True,
        "mandatory": True,
        "releaseBlocking": True,
        "startedAt": "2026-10-06T20:00:00Z",
        "completedAt": "2026-10-06T20:05:00Z",
        "expectedInputs": ["reader", "candidate-notes"],
        "observedInputs": ["reader", "candidate-notes"],
        "inputHashes": dict(identity.inputHashes),
        "toolVersions": {"python": "3.14.7"},
        "thingBeingCertified": "candidate-notes:cand-1",
        "independentEvidenceSource": "authoritative-reader:src-1",
        "findings": [],
        "evidencePaths": ["qa/gold-standard/evidence.schema.json"],
        "sourceFreezeId": identity.sourceFreezeId,
        "sourceHash": identity.sourceHash,
        "candidateFreezeId": identity.candidateFreezeId,
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": facts,
        "inventory": [{"name": "notesPages", "expected": 3, "observed": 3}],
    }
    data.update(overrides)
    return data


def evidence(**overrides):
    return evidence_from_dict(evidence_dict(**overrides))


def gate(**overrides):
    from chapter_qa.gates import GateDefinition

    data = {
        "gateId": "CURRICULUM_CORRECTNESS",
        "gateVersion": "1.0",
        "mandatory": True,
        "releaseBlocking": True,
        "requiresIndependentEvidence": True,
        "allowedNotVerified": False,
        "expectedEvidenceRole": "CURRICULUM_AUDITOR",
        "dependencies": (),
        "applicability": "always",
    }
    data.update(overrides)
    data["dependencies"] = tuple(data["dependencies"])
    return GateDefinition(**data)


class EvaluationTests(unittest.TestCase):
    def test_not_performed_is_not_pass(self):
        result = evaluate(evidence(performed=False, status="PASS"), gate(), build())
        self.assertNotEqual(result.status, "PASS")
        self.assertEqual(result.status, "FAIL")
        self.assertIn("NOT_PERFORMED", result.codes)

    def test_missing_required_input_cannot_pass(self):
        result = evaluate(
            evidence(execution={"requiredInputsPresent": False}, status="PASS"),
            gate(allowedNotVerified=True),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("MISSING_INPUT", result.codes)
        self.assertNotEqual(result.status, "NOT_VERIFIED")

    def test_no_evidence_is_not_pass(self):
        result = evaluate(
            evidence(execution={"missingEvidence": True}, status="PASS"),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("MISSING_EVIDENCE", result.codes)
        empty_paths = evaluate(evidence(evidencePaths=[], status="PASS"), gate(), build())
        self.assertEqual(empty_paths.status, "FAIL")

    def test_detector_exception_cannot_pass(self):
        result = evaluate(
            evidence(
                execution={"detectorException": True, "succeeded": False, "unavailableEvidence": True},
                notVerifiedReason="detector unavailable",
                status="NOT_VERIFIED",
            ),
            gate(allowedNotVerified=True),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("DETECTOR_EXCEPTION", result.codes)

    def test_missing_render_is_fail(self):
        result = evaluate(
            evidence(execution={"missingRender": True}, notVerifiedReason="no render", status="NOT_VERIFIED"),
            gate(allowedNotVerified=True),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("MISSING_RENDER", result.codes)

    def test_expected_n_observed_zero_fails(self):
        result = evaluate(
            evidence(inventory=[{"name": "slides", "expected": 5, "observed": 0}]),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "FAIL")

    def test_expected_n_observed_n_minus_one_fails(self):
        result = evaluate(
            evidence(inventory=[{"name": "slides", "expected": 5, "observed": 4}]),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("COUNT_MISMATCH", result.codes)

    def test_expected_n_observed_n_may_proceed(self):
        codes = assess_completeness(
            ["reader", "candidate-notes"],
            ["reader", "candidate-notes"],
            [{"name": "slides", "expected": 5, "observed": 5}],
        )
        self.assertEqual(codes, [])
        result = evaluate(
            evidence(inventory=[{"name": "slides", "expected": 5, "observed": 5}]),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "PASS")

    def test_no_input_is_not_clean_input(self):
        result = evaluate(evidence(expectedInputs=[], observedInputs=[]), gate(), build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("ZERO_INPUT", result.codes)
        silent_zero = evaluate(
            evidence(inventory=[{"name": "slides", "expected": 0, "observed": 0}]),
            gate(),
            build(),
        )
        self.assertEqual(silent_zero.status, "FAIL")
        self.assertIn("ZERO_INPUT", silent_zero.codes)

    def test_zero_findings_are_not_pass_unless_execution_and_completeness_are_valid(self):
        not_run = evaluate(evidence(findings=[], performed=False), gate(), build())
        self.assertNotEqual(not_run.status, "PASS")
        short = evaluate(
            evidence(findings=[], inventory=[{"name": "keys", "expected": 3, "observed": 2}]),
            gate(),
            build(),
        )
        self.assertNotEqual(short.status, "PASS")
        clean = evaluate(evidence(findings=[]), gate(), build())
        self.assertEqual(clean.status, "PASS")

    def test_low_finding_does_not_invent_a_warning_status(self):
        result = evaluate(
            evidence(findings=[{"severity": "LOW", "code": "NOTE", "message": "spacing note"}]),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "PASS")
        self.assertNotIn("PASS_WITH_WARNINGS", GATE_STATUSES)

    def test_blocking_finding_cannot_pass(self):
        result = evaluate(
            evidence(findings=[{"severity": "BLOCKING", "code": "LEAK", "message": "answer on student page"}]),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("BLOCKING_FINDING", result.codes)

    def test_build_a_evidence_cannot_certify_build_b(self):
        result = evaluate(evidence(), gate(), build("build-B", candidate_hash=HASH_B, notes_hash=HASH_B))
        self.assertNotEqual(result.status, "PASS")
        self.assertIn("BUILD_MISMATCH", result.codes)
        self.assertNotEqual(association_hash(build()), association_hash(build("build-B", HASH_B, HASH_B)))

    def test_candidate_identity_mismatch_cannot_certify(self):
        result = evaluate(evidence(), gate(), build(candidate_hash=HASH_B))
        self.assertEqual(result.status, "FAIL")
        self.assertIn("HASH_MISMATCH", result.codes)

    def test_stale_evidence_cannot_pass(self):
        result = evaluate(evidence(invalidationReasons=["CANDIDATE_CHANGED"]), gate(), build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("STALE", result.codes)
        self.assertFalse(result.accepted)
        flagged = evaluate(evidence(execution={"stale": True}), gate(), build())
        self.assertEqual(flagged.status, "FAIL")
        self.assertFalse(flagged.accepted)

    def test_self_evidence_rejected_when_independence_required(self):
        self.assertTrue(is_self_evidence("ledger", "ledger"))
        self.assertTrue(is_self_evidence("source-model:chapter", "source-model:other"))
        self.assertTrue(is_self_evidence("working-tree-golden", "working-tree-golden"))
        self.assertTrue(is_self_evidence("newly-generated-freeze", "newly-generated-freeze"))
        self.assertTrue(is_self_evidence("source-model hash:aaa", "source-model hash:bbb"))
        self.assertTrue(is_self_evidence("working-tree-golden", "mutable-golden"))
        self.assertTrue(is_self_evidence("working-tree-golden hash:abc", "mutable-golden hash:abc"))
        self.assertTrue(is_self_evidence("source model A", "source model B"))
        self.assertFalse(is_self_evidence("candidate-notes:cand-1", "authoritative-reader:src-1"))
        result = evaluate(
            evidence(
                thingBeingCertified="ledger",
                independentEvidenceSource="ledger",
            ),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("SELF_EVIDENCE", result.codes)
        self.assertFalse(result.accepted)

    def test_builder_only_independent_evidence_rejected(self):
        result = evaluate(
            evidence(auditorRole="BUILDER"),
            gate(expectedEvidenceRole="BUILDER"),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("BUILDER_ONLY", result.codes)
        self.assertFalse(result.accepted)

    def test_claimed_pass_cannot_upgrade_a_failed_record(self):
        raw = evidence_dict(status="PASS", performed=False)
        self.assertEqual(raw["status"], "PASS")
        result = evaluate(evidence_from_dict(raw), gate(), build())
        self.assertEqual(result.status, "FAIL")

    def test_illegal_status_words_are_rejected(self):
        for word in ("OK", "READY", "CLEAN", "PASS_WITH_WARNINGS", "MOSTLY_PASS", "PARTIAL"):
            raw = evidence_dict(status=word)
            self.assertTrue(validate_evidence_dict(raw), word)

    def test_not_verified_only_when_the_gate_permits_unavailable_evidence(self):
        legal = evaluate(
            evidence(
                performed=False,
                status="NOT_VERIFIED",
                notVerifiedReason="post-freeze golden is not configured",
                execution={"unavailableEvidence": True},
                evidencePaths=[],
            ),
            gate(allowedNotVerified=True),
            build(),
        )
        self.assertEqual(legal.status, "NOT_VERIFIED")
        illegal = evaluate(
            evidence(
                performed=False,
                status="NOT_VERIFIED",
                notVerifiedReason="skipped",
                execution={"unavailableEvidence": True},
            ),
            gate(allowedNotVerified=False),
            build(),
        )
        self.assertEqual(illegal.status, "FAIL")

    def test_alias_labels_are_self_evidence(self):
        result = evaluate(
            evidence(
                thingBeingCertified="working-tree-golden",
                independentEvidenceSource="mutable-golden",
            ),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("SELF_EVIDENCE", result.codes)
        tagged = evaluate(
            evidence(
                thingBeingCertified="source-model hash:aaa",
                independentEvidenceSource="source-model hash:bbb",
            ),
            gate(),
            build(),
        )
        self.assertEqual(tagged.status, "FAIL")
        self.assertIn("SELF_EVIDENCE", tagged.codes)

    def test_empty_hashes_cannot_match(self):
        row = replace(evidence(), candidateHash="", sourceHash="", inputHashes={})
        requested = replace(build(), candidateHash="", sourceHash="", inputHashes={})
        result = evaluate(row, gate(), requested)
        self.assertEqual(result.status, "FAIL")
        self.assertIn("HASH_MISMATCH", result.codes)
        raw = evidence_dict(candidateHash="", sourceHash="", inputHashes={})
        self.assertTrue(validate_evidence_dict(raw))

    def test_missing_evidence_file_cannot_pass(self):
        result = evaluate(
            evidence(evidencePaths=["qa/evidence/does-not-exist-phase-a.json"]),
            gate(),
            build(),
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("MISSING_EVIDENCE", result.codes)

    def test_whitespace_inputs_are_not_a_clean_set(self):
        result = evaluate(evidence(expectedInputs=[" "], observedInputs=[" "]), gate(), build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("ZERO_INPUT", result.codes)


class ReleaseJudgeTests(unittest.TestCase):
    def test_missing_mandatory_gate_fails(self):
        result = judge([gate()], [], build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("MISSING_GATE: CURRICULUM_CORRECTNESS", result.blockingReasons)
        self.assertEqual(result.certification, CERTIFICATION_FAIL)

    def test_prose_cannot_hide_a_missing_mandatory_gate(self):
        result = judge([gate()], [], build())
        self.assertEqual(result.status, "FAIL")
        self.assertFalse(hasattr(result, "narrative"))

    def test_mandatory_fail_fails_the_judge(self):
        row = evidence(
            mandatory=False,
            inventory=[{"name": "notesPages", "expected": 3, "observed": 2}],
        )
        result = judge([gate(mandatory=True)], [row], build())
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any(item.startswith("GATE_FAIL:") for item in result.blockingReasons))

    def test_mandatory_not_verified_fails_the_judge(self):
        row = evidence(
            performed=False,
            status="NOT_VERIFIED",
            notVerifiedReason="archive offline",
            execution={"unavailableEvidence": True},
            evidencePaths=[],
        )
        result = judge([gate(allowedNotVerified=True, mandatory=True)], [row], build())
        self.assertEqual(row and evaluate(row, gate(allowedNotVerified=True), build()).status, "NOT_VERIFIED")
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any(item.startswith("NOT_VERIFIED:") for item in result.blockingReasons))

    def test_release_blocking_optional_fail_fails_the_judge(self):
        required = evidence(evidenceId="ev-required")
        optional = evidence(
            evidenceId="ev-optional",
            gateId="PLAYBOOK_ALIGNMENT",
            auditorRole="CROSS_ARTIFACT_AUDITOR",
            mandatory=False,
            releaseBlocking=False,
            execution={"gateSpecificFailure": True},
            failureReason="playbook drift",
            status="FAIL",
        )
        gates = [
            gate(),
            gate(
                gateId="PLAYBOOK_ALIGNMENT",
                mandatory=False,
                releaseBlocking=True,
                expectedEvidenceRole="CROSS_ARTIFACT_AUDITOR",
            ),
        ]
        result = judge(gates, [required, optional], build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("GATE_FAIL: PLAYBOOK_ALIGNMENT", result.blockingReasons)

    def test_explicit_nonblocking_optional_fail_may_continue(self):
        required = evidence(evidenceId="ev-required")
        optional = evidence(
            evidenceId="ev-optional",
            gateId="PLAYBOOK_ALIGNMENT",
            auditorRole="CROSS_ARTIFACT_AUDITOR",
            mandatory=False,
            releaseBlocking=False,
            execution={"gateSpecificFailure": True},
            failureReason="optional drift",
            status="FAIL",
            findings=[{"severity": "HIGH", "code": "DRIFT", "message": "heading drift"}],
        )
        gates = [
            gate(),
            gate(
                gateId="PLAYBOOK_ALIGNMENT",
                mandatory=False,
                releaseBlocking=False,
                expectedEvidenceRole="CROSS_ARTIFACT_AUDITOR",
            ),
        ]
        result = judge(gates, [required, optional], build())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failedGateCount, 1)
        self.assertEqual(result.certification, CERTIFICATION_PASS)

    def test_blocking_finding_fails_release_even_on_an_optional_gate(self):
        required = evidence(evidenceId="ev-required")
        optional = evidence(
            evidenceId="ev-optional",
            gateId="PLAYBOOK_ALIGNMENT",
            auditorRole="CROSS_ARTIFACT_AUDITOR",
            mandatory=False,
            releaseBlocking=False,
            status="FAIL",
            findings=[{"severity": "BLOCKING", "code": "LEAK", "message": "answer leaked"}],
        )
        gates = [
            gate(),
            gate(
                gateId="PLAYBOOK_ALIGNMENT",
                mandatory=False,
                releaseBlocking=False,
                expectedEvidenceRole="CROSS_ARTIFACT_AUDITOR",
            ),
        ]
        result = judge(gates, [required, optional], build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("BLOCKING_FINDING: PLAYBOOK_ALIGNMENT", result.blockingReasons)
        self.assertIn("ev-optional", result.acceptedEvidenceIds)

    def test_all_mandatory_independent_current_build_evidence_passes(self):
        row = evidence()
        result = judge([gate()], [row], build())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.passedGateCount, 1)
        self.assertEqual(result.failedGateCount, 0)
        self.assertEqual(result.missingGateCount, 0)
        self.assertEqual(result.notVerifiedGateCount, 0)
        self.assertEqual(result.blockingReasons, ())
        self.assertEqual(result.certification, CERTIFICATION_PASS)
        self.assertIn("ev-1", result.acceptedEvidenceIds)

    def test_build_a_evidence_does_not_certify_build_b(self):
        result = judge([gate()], [evidence()], build("build-B", HASH_B, HASH_B))
        self.assertEqual(result.status, "FAIL")
        self.assertIn("ev-1", result.rejectedEvidenceIds)
        self.assertNotIn("ev-1", result.acceptedEvidenceIds)

    def test_self_evidence_and_builder_evidence_do_not_satisfy_the_judge(self):
        self_row = evidence(thingBeingCertified="ledger", independentEvidenceSource="ledger")
        builder_row = evidence(evidenceId="ev-builder", auditorRole="BUILDER")
        self_result = judge([gate()], [self_row], build())
        builder_result = judge([gate(expectedEvidenceRole="BUILDER")], [builder_row], build())
        self.assertEqual(self_result.status, "FAIL")
        self.assertIn("ev-1", self_result.rejectedEvidenceIds)
        self.assertEqual(builder_result.status, "FAIL")
        self.assertIn("ev-builder", builder_result.rejectedEvidenceIds)

    def test_empty_gate_list_cannot_pass(self):
        result = judge([], [], build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("NO_GATES", result.blockingReasons)

    def test_unmarked_stale_evidence_fails_when_the_change_map_is_passed(self):
        from chapter_qa.invalidation import propagate
        from chapter_qa.gates import load_gates

        affected = propagate("notes", "CANDIDATE_CHANGED", load_gates())
        row = evidence(
            gateId="NOTES_STRUCTURE",
            auditorRole="CROSS_ARTIFACT_AUDITOR",
            invalidationReasons=[],
        )
        result = judge(
            [gate(gateId="NOTES_STRUCTURE", expectedEvidenceRole="CROSS_ARTIFACT_AUDITOR")],
            [row],
            build(),
            affected=affected,
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("ev-1", result.rejectedEvidenceIds)
        self.assertNotIn("ev-1", result.acceptedEvidenceIds)

    def test_blocking_on_same_build_rejected_evidence_still_fails(self):
        required = evidence(evidenceId="ev-required")
        stale_blocking = evidence(
            evidenceId="ev-stale",
            gateId="PLAYBOOK_ALIGNMENT",
            auditorRole="CROSS_ARTIFACT_AUDITOR",
            mandatory=False,
            releaseBlocking=False,
            invalidationReasons=["CANDIDATE_CHANGED"],
            findings=[{"severity": "BLOCKING", "code": "LEAK", "message": "answer leaked"}],
        )
        gates = [
            gate(),
            gate(
                gateId="PLAYBOOK_ALIGNMENT",
                mandatory=False,
                releaseBlocking=False,
                expectedEvidenceRole="CROSS_ARTIFACT_AUDITOR",
            ),
        ]
        result = judge(gates, [required, stale_blocking], build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("BLOCKING_FINDING: PLAYBOOK_ALIGNMENT", result.blockingReasons)

    def test_blocking_on_another_build_does_not_fail_this_build(self):
        required = evidence(evidenceId="ev-required")
        raw = evidence_dict(
            evidenceId="ev-other",
            buildId="build-B",
            candidateHash=HASH_B,
            candidateFreezeId="cand-2",
            inputHashes={"notes": HASH_B, "reader": HASH_A},
            findings=[{"severity": "BLOCKING", "code": "LEAK", "message": "other build"}],
        )
        result = judge([gate()], [required, evidence_from_dict(raw)], build())
        self.assertEqual(result.status, "PASS")
        self.assertIn("ev-other", result.rejectedEvidenceIds)

    def test_release_judge_is_read_only(self):
        source = (ROOT / "tools" / "chapter_qa" / "release_judge.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        called = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
                if name in {"open", "write_text", "write_bytes", "unlink", "remove", "system", "popen"}:
                    called.append(name)
        self.assertEqual(called, [])
        self.assertNotIn("subprocess", source)
        self.assertFalse(CAPABILITIES["RELEASE_JUDGE"]["editCanonical"])
        self.assertTrue(may_issue_release_certification("RELEASE_JUDGE"))
        self.assertFalse(may_issue_release_certification("BUILDER"))
        self.assertFalse(may_issue_release_certification("QA_ADVERSARY"))

        def _blocked_open(*_args, **_kwargs):
            raise AssertionError("release judge called open")

        original = builtins.open
        builtins.open = _blocked_open
        try:
            result = judge([gate()], [evidence()], build())
        finally:
            builtins.open = original
        self.assertEqual(result.status, "PASS")


class ContractTests(unittest.TestCase):
    def test_schema_required_fields_match_the_evaluator(self):
        schema = json.loads((ROOT / "qa" / "gold-standard" / "evidence.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["required"], list(REQUIRED_FIELDS))
        gate_schema = json.loads((ROOT / "qa" / "gold-standard" / "gate.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(gate_schema["required"], list(REQUIRED_GATE_FIELDS))
        listed = schema["properties"]["invalidationReasons"]["items"]["enum"]
        self.assertEqual(listed, list(INVALIDATION_REASONS))

    def test_gate_matrix_is_generic(self):
        raw = (ROOT / "qa" / "gold-standard" / "gates.json").read_text(encoding="utf-8")
        self.assertNotIn("chapter-02", raw)
        self.assertNotIn("37", raw)
        gates = load_gates()
        ids = [item.gateId for item in gates]
        self.assertEqual(len(ids), 22)
        self.assertIn("POST_FREEZE_GOLDEN", ids)
        self.assertNotIn("POST_FREEZE_GOLDEN", [item.gateId for item in default_release_gates(gates)])
        post = next(item for item in gates if item.gateId == "POST_FREEZE_GOLDEN")
        self.assertFalse(post.mandatory)
        self.assertFalse(post.releaseBlocking)
        self.assertTrue(post.allowedNotVerified)
        self.assertEqual(post.applicability, "when_configured")
        for item in gates:
            if item.applicability == "always":
                self.assertTrue(item.mandatory)
                self.assertTrue(item.releaseBlocking)

    def test_notes_change_does_not_invalidate_unrelated_gates(self):
        gates = load_gates()
        affected = propagate("notes", "CANDIDATE_CHANGED", gates)
        self.assertEqual(affected["NOTES_STRUCTURE"], "CANDIDATE_CHANGED")
        for downstream in (
            "NOTES_SLIDES_SYNC",
            "RENDER_COMPLETENESS",
            "RENDERED_VISUAL_QA",
            "RELEASE_PARITY",
        ):
            self.assertEqual(affected[downstream], "DEPENDENCY_CHANGED")
        for unrelated in ("SOURCE_AUTHORITY", "SLIDES_STRUCTURE", "SCHEDULE_POLICY", "PLAYBOOK_ALIGNMENT"):
            self.assertNotIn(unrelated, affected)

    def test_slides_change_does_not_invalidate_notes_structure(self):
        affected = propagate("slides", "CANDIDATE_CHANGED", load_gates())
        self.assertIn("SLIDES_STRUCTURE", affected)
        self.assertIn("NOTES_SLIDES_SYNC", affected)
        self.assertNotIn("NOTES_STRUCTURE", affected)
        self.assertNotIn("SOURCE_AUTHORITY", affected)

    def test_tool_and_inventory_drift(self):
        self.assertTrue(tool_versions_changed({"python": "3.14.7"}, {"python": "3.14.8"}))
        self.assertFalse(tool_versions_changed({"python": "3.14.7"}, {"python": "3.14.7"}))
        self.assertTrue(expected_inventory_changed({"slides": 5}, {"slides": 4}))
        self.assertFalse(expected_inventory_changed({"slides": 5}, {"slides": 5}))

    def test_lifecycle_cannot_jump_to_frozen(self):
        self.assertFalse(legal_transition("BUILT_UNCERTIFIED", "FROZEN"))
        self.assertTrue(legal_transition("APPROVED_FOR_FREEZE", "FROZEN"))
        self.assertTrue(transition_to_frozen_allowed("APPROVED_FOR_FREEZE"))
        for state in STATES:
            if state != "APPROVED_FOR_FREEZE":
                self.assertFalse(legal_transition(state, "FROZEN"), state)
        self.assertTrue(legal_transition("BUILD_IN_PROGRESS", "BUILT_UNCERTIFIED"))
        self.assertFalse(legal_transition("FROZEN", "BUILD_IN_PROGRESS"))
        self.assertFalse(legal_transition("PASS", "FROZEN"))

    def test_frozen_byte_compare_reports_a_changed_hash(self):
        same = {"notes": HASH_A}
        self.assertEqual(compare_frozen_bytes(same, dict(same)), [])
        self.assertEqual(compare_frozen_bytes(same, {"notes": HASH_B}), ["notes"])
        self.assertEqual(compare_frozen_bytes({}, {}), ["EMPTY_IDENTITY"])
        self.assertEqual(compare_frozen_bytes(same, {"notes": ""}), ["notes"])

    def test_frozen_chapters_require_owner_authorization(self):
        self.assertFalse(frozen_classroom_change_permitted(1, False))
        self.assertFalse(frozen_classroom_change_permitted(2, False))
        self.assertTrue(frozen_classroom_change_permitted(1, True))
        self.assertTrue(frozen_classroom_change_permitted(2, True))
        self.assertFalse(frozen_classroom_change_permitted(2, "yes"))

    def test_existing_agents_are_not_duplicated_into_the_release_judge(self):
        self.assertIn("VISUAL_QA_AUDITOR", AGENT_ROLE_MAP["visual-art-director"]["notRoles"])
        self.assertIn("RELEASE_JUDGE", AGENT_ROLE_MAP["qa-certification-reviewer"]["notRoles"])
        self.assertEqual(AGENT_ROLE_MAP["release-judge"]["finalCertificationRole"], "RELEASE_JUDGE")
        self.assertIsNone(AGENT_ROLE_MAP["curriculum-source-reviewer"]["finalCertificationRole"])
        self.assertEqual(GATE_STATUSES, ("PASS", "FAIL", "NOT_VERIFIED"))


if __name__ == "__main__":
    unittest.main()
