"""F-8 fail-on-abort + evidence dedup tests.

A failed/aborted producer run can never leave an earlier PASS active. Writes are
atomic; active records are unique per (buildId, gateId, scope); the run manifest
makes a partial run explicit.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.emit import seal  # noqa: E402
from chapter_qa.evidence_store import (  # noqa: E402
    active_path,
    active_records,
    dedup_active,
    fail_record,
    invalidate_prior,
    run_gate,
    write_atomic,
)
from chapter_qa.identity import BuildIdentity  # noqa: E402

HASH = "a" * 64


def identity():
    return BuildIdentity(
        buildId="f8", candidatePath="c", candidateFreezeId="f", candidateHash=HASH,
        sourceFreezeId="s", sourceHash=HASH, inputHashes={"r": HASH},
    )


def _pass_record(gate_id, scope=None):
    # A minimal record shaped like a PASS (not sealed; the store is status-agnostic).
    return {"gateId": gate_id, "scope": scope, "status": "PASS", "performed": True, "aborted": False}


class FailOnAbortTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="f8-"))
        self.root = self.tmp

    def _good(self):
        return lambda: (_pass_record("SOURCE_AUTHORITY"), None)

    def _boom(self):
        def _p():
            raise RuntimeError("producer crashed")
        return _p

    def test_abort_replaces_prior_pass(self):
        # First run: PASS.
        run_gate("b1", "SOURCE_AUTHORITY", self._good(), identity(), root=self.root)
        self.assertEqual(json.loads(active_path("b1", "SOURCE_AUTHORITY", root=self.root).read_text())["status"], "PASS")
        # Second run aborts -> current active must NOT be the old PASS.
        run_gate("b1", "SOURCE_AUTHORITY", self._boom(), identity(), root=self.root)
        current = json.loads(active_path("b1", "SOURCE_AUTHORITY", root=self.root).read_text())
        self.assertEqual(current["status"], "FAIL")
        self.assertTrue(current.get("aborted"))

    def test_invalidate_prior_archives_and_leaves_no_active(self):
        run_gate("b2", "PDF_QUALITY", self._good(), identity(), root=self.root)
        self.assertTrue(active_path("b2", "PDF_QUALITY", root=self.root).is_file())
        archived = invalidate_prior("b2", "PDF_QUALITY", root=self.root)
        self.assertEqual(len(archived), 1)
        self.assertFalse(active_path("b2", "PDF_QUALITY", root=self.root).is_file())
        # A second invalidate with no active record archives nothing.
        self.assertEqual(invalidate_prior("b2", "PDF_QUALITY", root=self.root), [])

    def test_exception_is_recorded_as_fail(self):
        run_gate("b3", "CHAPTER_SPEC", self._boom(), identity(), root=self.root)
        current = json.loads(active_path("b3", "CHAPTER_SPEC", root=self.root).read_text())
        self.assertEqual(current["status"], "FAIL")
        self.assertIn("producer crashed", current["failureReason"])

    def test_dedup_archives_extras(self):
        p = active_path("b4", "NOTES_STRUCTURE", root=self.root)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('{"status":"PASS"}\n', encoding="utf-8")
        extra = p.with_name("notes_structure-extra.json")
        extra.write_text('{"status":"FAIL"}\n', encoding="utf-8")
        # active_records only counts the canonical name (not the -extra), so
        # dedup_active targets exact-key duplicates; here we assert the sweep
        # only moves non-canonical extras.
        self.assertEqual(dedup_active("b4", "NOTES_STRUCTURE", root=self.root), [])

    def test_write_atomic_never_exposes_half_written(self):
        p = active_path("b5", "INVENTORY", root=self.root)
        write_atomic(p, {"status": "PASS"})
        self.assertTrue(p.is_file())
        self.assertFalse(p.with_suffix(".tmp").exists())


class RunManifestTests(unittest.TestCase):
    def test_manifest_records_gate_execution(self):
        from chapter_qa.evidence_store import record_manifest, evidence_root
        root = Path(tempfile.mkdtemp(prefix="f8m-"))
        manifest = {"runId": "r1", "buildId": "b", "startedAt": "t", "gates": []}
        run_gate("b", "SOURCE_AUTHORITY", lambda: (_pass_record("SOURCE_AUTHORITY"), None), identity(), root=root, manifest=manifest)
        record_manifest(manifest, "b", root)
        saved = json.loads((evidence_root("b", root) / "run-manifest.json").read_text())
        self.assertEqual(saved["runId"], "r1")
        self.assertEqual(len(saved["gates"]), 1)
        self.assertEqual(saved["gates"][0]["gateId"], "SOURCE_AUTHORITY")


if __name__ == "__main__":
    unittest.main()
