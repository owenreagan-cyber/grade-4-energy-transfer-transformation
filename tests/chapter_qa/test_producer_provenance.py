"""F-4 producer-provenance tests.

Provenance is verified against a throwaway git repo so tests do not depend on
this checkout's own producer files being clean. The Judge recomputes producer
source from disk and rejects untracked, dirty, or changed producer source.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.producer_provenance import (  # noqa: E402
    is_tracked,
    producer_provenance,
    producer_source_path,
    provenance_toolversions,
    verify_provenance,
)

HASH = "a" * 64


class ProducerProvenanceUnitTests(unittest.TestCase):
    def test_source_path_mapping(self):
        self.assertEqual(
            producer_source_path("chapter_qa.source_audit:emit_source_evidence"),
            "tools/chapter_qa/source_audit.py",
        )
        self.assertEqual(
            producer_source_path("qa_pdf_quality:emit_pdf_evidence"),
            "tools/qa_pdf_quality.py",
        )

    def test_registered_producers_are_tracked(self):
        from chapter_qa.registry import PRODUCERS
        for gate_id, spec in PRODUCERS.items():
            rel = producer_source_path(spec["id"])
            self.assertTrue(is_tracked(rel), "%s producer %s is not tracked" % (gate_id, rel))

    def test_verify_provenance_passes_for_clean_tracked_producer(self):
        from chapter_qa.registry import PRODUCERS
        for gate_id in ("SOURCE_AUTHORITY", "PDF_QUALITY", "RELEASE_EXACT_SET"):
            spec = PRODUCERS[gate_id]
            prov = provenance_toolversions(producer_provenance(gate_id, spec["id"]))
            self.assertEqual(verify_provenance(gate_id, prov), [], gate_id)


class ProvenanceAttackTests(unittest.TestCase):
    """Throwaway-repo attacks against producer provenance."""

    def _repo(self):
        folder = Path(tempfile.mkdtemp(prefix="prov-git-"))
        subprocess.check_call(["git", "init", "-q"], cwd=folder)
        subprocess.check_call(["git", "config", "user.email", "p@example"], cwd=folder)
        subprocess.check_call(["git", "config", "user.name", "p"], cwd=folder)
        return folder

    def test_edit_producer_after_seal_is_detected(self):
        repo = self._repo()
        (repo / "tools").mkdir()
        producer_file = repo / "tools" / "myproducer.py"
        producer_file.write_text("def emit(x):\n    return x\n", encoding="utf-8")
        subprocess.check_call(["git", "add", "tools/myproducer.py"], cwd=repo)
        subprocess.check_call(["git", "commit", "-q", "-m", "add producer"], cwd=repo)

        with mock.patch("chapter_qa.registry.expected_producer", return_value={"id": "myproducer:emit", "version": "1.0"}):
            sealed = provenance_toolversions(producer_provenance("G", "myproducer:emit", repo))
            self.assertEqual(verify_provenance("G", sealed, repo), [])
            # Edit after seal -> recorded hash no longer matches disk.
            producer_file.write_text("def emit(x):\n    return x + 1\n", encoding="utf-8")
            self.assertIn("PRODUCER_SOURCE_CHANGED", verify_provenance("G", sealed, repo))

    def test_untracked_producer_is_rejected(self):
        repo = self._repo()
        (repo / "tools").mkdir()
        (repo / "tools" / "untracked.py").write_text("x = 1\n", encoding="utf-8")
        prov = provenance_toolversions(producer_provenance("U_GATE", "untracked:emit", repo))
        self.assertEqual(prov["trackedSource"], "false")
        with mock.patch("chapter_qa.registry.expected_producer", return_value={"id": "untracked:emit", "version": "1.0"}):
            self.assertIn("PRODUCER_UNTRACKED", verify_provenance("U_GATE", prov, repo))


class JudgeProvenanceTests(unittest.TestCase):
    """The Judge rejects a real-gate record whose producer source hash is forged."""

    def test_forged_producer_source_hash_rejects(self):
        from chapter_qa.evidence import compute_evidence_seal, evidence_from_dict
        from chapter_qa.gates import GateDefinition
        from chapter_qa.identity import BuildIdentity
        from chapter_qa.release_judge import judge
        import chapter_qa.registry as registry

        identity = BuildIdentity(
            buildId="b", candidatePath="c", candidateFreezeId="f", candidateHash=HASH,
            sourceFreezeId="s", sourceHash=HASH, inputHashes={"r": HASH},
        )
        gate = GateDefinition("SOURCE_AUTHORITY", "1.0", True, True, True, False, "SOURCE_SCHOLAR", (), "always")
        spec = registry.PRODUCERS["SOURCE_AUTHORITY"]
        prov = provenance_toolversions(producer_provenance("SOURCE_AUTHORITY", spec["id"]))
        data = {
            "schemaVersion": "1.0", "evidenceId": "ev", "gateId": "SOURCE_AUTHORITY", "gateVersion": "1.0",
            "buildId": "b", "candidatePath": "c", "candidateHash": HASH, "auditorRole": "SOURCE_SCHOLAR",
            "status": "PASS", "performed": True, "mandatory": True, "releaseBlocking": True,
            "startedAt": "2026-10-06T20:00:00Z", "completedAt": "2026-10-06T20:05:00Z",
            "expectedInputs": ["x"], "observedInputs": ["x"], "inputHashes": {"r": HASH},
            "toolVersions": {"python": "3.14.7", "producer": spec["id"], "producerVersion": spec["version"]},
            "thingBeingCertified": "c", "independentEvidenceSource": "s", "findings": [],
            "evidencePaths": ["qa/gold-standard/evidence.schema.json"],
            "sourceFreezeId": "s", "sourceHash": HASH, "candidateFreezeId": "f",
            "failureReason": None, "notVerifiedReason": None, "invalidationReasons": [],
            "execution": {"succeeded": True, "detectorException": False, "requiredInputsPresent": True,
                          "missingRender": False, "missingEvidence": False, "stale": False,
                          "gateSpecificFailure": False, "unavailableEvidence": False},
            "inventory": [{"name": "p", "expected": 1, "observed": 1}],
        }
        data["toolVersions"].update(prov)
        data["seal"] = compute_evidence_seal(data)
        self.assertEqual(judge([gate], [evidence_from_dict(data)], identity).status, "PASS")

        # Forge the recorded source hash and re-seal (attacker has the producer).
        forged = dict(data, toolVersions=dict(data["toolVersions"], producerSourceHash="0" * 64))
        forged["seal"] = compute_evidence_seal(forged)
        result = judge([gate], [evidence_from_dict(forged)], identity)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("PRODUCER_SOURCE_CHANGED" in r for r in result.blockingReasons))


if __name__ == "__main__":
    unittest.main()
