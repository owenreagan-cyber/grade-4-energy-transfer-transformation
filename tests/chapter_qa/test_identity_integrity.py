"""F-1/F-2/F-5 regression tests: build identity covers classroom bytes and
evidence is tamper-evident. A mutation that is later committed still fails,
because staleness is a function of current bytes, not git cleanliness.
"""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.evidence import (  # noqa: E402
    compute_evidence_seal,
    evidence_from_dict,
    evaluate,
    seal_valid,
)
from chapter_qa.gates import GateDefinition  # noqa: E402
from chapter_qa.identity import BuildIdentity, recompute_mismatches  # noqa: E402
from chapter_qa.release_judge import judge  # noqa: E402

HASH = "a" * 64


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build(candidate_files=None, **overrides):
    kwargs = dict(
        buildId="build-A",
        candidatePath="candidate/chapter-x",
        candidateFreezeId="cand-1",
        candidateHash=HASH,
        sourceFreezeId="src-1",
        sourceHash=HASH,
        inputHashes={"notes": HASH, "reader": HASH},
    )
    kwargs.update(overrides)
    return BuildIdentity(**kwargs, candidateFiles=candidate_files or {})


def gate(**overrides):
    data = dict(
        gateId="CURRICULUM_CORRECTNESS",
        gateVersion="1.0",
        mandatory=True,
        releaseBlocking=True,
        requiresIndependentEvidence=True,
        allowedNotVerified=False,
        expectedEvidenceRole="CURRICULUM_AUDITOR",
        dependencies=(),
        applicability="always",
    )
    data.update(overrides)
    data["dependencies"] = tuple(data["dependencies"])
    return GateDefinition(**data)


def evidence_dict():
    return {
        "schemaVersion": "1.0",
        "evidenceId": "ev-1",
        "gateId": "CURRICULUM_CORRECTNESS",
        "gateVersion": "1.0",
        "buildId": "build-A",
        "candidatePath": "candidate/chapter-x",
        "candidateHash": HASH,
        "auditorRole": "CURRICULUM_AUDITOR",
        "status": "PASS",
        "performed": True,
        "mandatory": True,
        "releaseBlocking": True,
        "startedAt": "2026-10-06T20:00:00Z",
        "completedAt": "2026-10-06T20:05:00Z",
        "expectedInputs": ["reader", "candidate-notes"],
        "observedInputs": ["reader", "candidate-notes"],
        "inputHashes": {"notes": HASH, "reader": HASH},
        "toolVersions": {
            "python": "3.14.7",
            "producer": "chapter_qa.source_audit:emit_source_evidence",
            "producerVersion": "1.0",
        },
        "thingBeingCertified": "candidate-notes:cand-1",
        "independentEvidenceSource": "authoritative-reader:src-1",
        "findings": [],
        "evidencePaths": ["qa/gold-standard/evidence.schema.json"],
        "sourceFreezeId": "src-1",
        "sourceHash": HASH,
        "candidateFreezeId": "cand-1",
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
        "inventory": [{"name": "notesPages", "expected": 3, "observed": 3}],
    }


def sealed_evidence(**overrides):
    data = evidence_dict()
    data.update(overrides)
    data["seal"] = compute_evidence_seal(data)
    return data


class CandidateBytesTests(unittest.TestCase):
    def test_recompute_reports_missing_and_changed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.docx").write_bytes(b"one")
            (root / "b.pdf").write_bytes(b"two")
            ident = build(candidate_files={"a.docx": _sha(b"one"), "b.pdf": _sha(b"two")})
            self.assertEqual(recompute_mismatches(ident, root), [])
            (root / "a.docx").write_bytes(b"changed")
            mism = recompute_mismatches(ident, root)
            self.assertTrue(any("a.docx" in item for item in mism))
            (root / "b.pdf").unlink()
            mism = recompute_mismatches(ident, root)
            self.assertTrue(any("b.pdf" in item and "missing" in item for item in mism))

    def test_mutated_classroom_bytes_fail_the_judge(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "notes.docx").write_bytes(b"v1")
            ident = build(candidate_files={"notes.docx": _sha(b"v1")})
            row = evidence_from_dict(sealed_evidence())
            self.assertEqual(judge([gate()], [row], ident, root=root).status, "PASS")
            # Mutate after sealing. This is equivalent to a committed mutation:
            # the bytes differ regardless of git state.
            (root / "notes.docx").write_bytes(b"v2")
            result = judge([gate()], [row], ident, root=root)
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(any("CANDIDATE_BYTES_MISMATCH" in r for r in result.blockingReasons))

    def test_empty_candidate_files_means_no_bytes_are_bound(self):
        ident = build(candidate_files={})
        self.assertEqual(recompute_mismatches(ident), [])


class EvidenceSealTests(unittest.TestCase):
    def test_hand_edited_findings_break_the_seal(self):
        data = sealed_evidence(findings=[{"severity": "BLOCKING", "code": "leak", "message": "x"}])
        record = evidence_from_dict(data)
        self.assertEqual(evaluate(record, gate(), build()).status, "FAIL")
        # Hand edit the stored JSON to hide the finding without re-sealing.
        tampered = dict(data, findings=[], status="PASS")
        with self.assertRaises(ValueError):
            evidence_from_dict(tampered)

    def test_edited_input_hash_breaks_the_seal(self):
        data = sealed_evidence()
        tampered = dict(data, inputHashes={"notes": "b" * 64, "reader": HASH})
        with self.assertRaises(ValueError):
            evidence_from_dict(tampered)

    def test_edited_status_breaks_the_seal(self):
        data = sealed_evidence()
        tampered = dict(data, status="FAIL")
        with self.assertRaises(ValueError):
            evidence_from_dict(tampered)

    def test_seal_valid_detects_in_memory_tamper(self):
        record = evidence_from_dict(sealed_evidence())
        self.assertTrue(seal_valid(record))
        tampered = replace(record, auditorRole="BUILDER")
        self.assertFalse(seal_valid(tampered))

    def test_copy_from_another_build_is_rejected(self):
        row = evidence_from_dict(sealed_evidence(buildId="build-B"))
        result = judge([gate()], [row], build())
        self.assertEqual(result.status, "FAIL")
        self.assertIn("ev-1", result.rejectedEvidenceIds)

    def test_judge_rejects_a_seal_mismatch(self):
        # Construct a record whose seal field is wrong (simulates a hand edit
        # that bypassed the loader). The Judge must still refuse it.
        record = evidence_from_dict(sealed_evidence())
        forged = replace(record, seal="0" * 64)
        result = judge([gate()], [forged], build())
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("SEAL_MISMATCH" in r for r in result.blockingReasons))


if __name__ == "__main__":
    unittest.main()
