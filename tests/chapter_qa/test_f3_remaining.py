"""F-3 remaining-producer independence self-tests (file-observing entrypoints).

STATUS_AUTHORITY, SCHEDULE_POLICY, ADVERSARIAL_QA, PRIOR_FROZEN_NONREGRESSION
now open actual files/run actual tools and derive their own observation.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.identity import BuildIdentity  # noqa: E402
from chapter_qa.mandatory_producers import (  # noqa: E402
    emit_adversarial_qa_from_file,
    emit_prior_frozen_from_tools,
)
from chapter_qa.schedule_policy import emit_schedule_evidence_from_file  # noqa: E402
from qa_status_authority import emit_status_evidence_from_files  # noqa: E402

HASH = "a" * 64
WORK = ROOT / "qa" / "work" / "_f3b"


def identity():
    return BuildIdentity(
        buildId="f3b", candidatePath="c", candidateFreezeId="f", candidateHash=HASH,
        sourceFreezeId="s", sourceHash=HASH, inputHashes={"r": HASH},
    )


def _write(name: str, text: str) -> str:
    path = WORK / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def _evidence() -> str:
    p = WORK / "evidence.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}\n", encoding="utf-8")
    return p.relative_to(ROOT).as_posix()


class StatusAuthorityFileTests(unittest.TestCase):
    def test_frozen_surface_matches_authoritative(self):
        path = _write("status-frozen.md", "FROZEN")
        files = [{"surfaceId": "m", "kind": "AUTHORITATIVE_STATUS", "path": path}]
        status = emit_status_evidence_from_files("FROZEN", files, identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")

    def test_premature_frozen_conflict_fails(self):
        path = _write("status-released.md", "RELEASED")
        files = [{"surfaceId": "m", "kind": "AUTHORITATIVE_STATUS", "path": path}]
        status = emit_status_evidence_from_files("BUILD_IN_PROGRESS", files, identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")


class SchedulePolicyFileTests(unittest.TestCase):
    def _table(self, friday_token):
        return (
            "| Session | Date | Status |\n|---|---|---|\n"
            "| 1 | 2026-10-19 | REQUIRED |\n"
            "| 5 | 2026-10-23 | %s |\n" % friday_token
        )

    def test_friday_flex_passes(self):
        path = _write("pace-flex.md", self._table("FLEX"))
        self.assertEqual(emit_schedule_evidence_from_file(path, identity(), _evidence())[1].status, "PASS")

    def test_friday_required_first_exposure_fails(self):
        path = _write("pace-req.md", self._table("REQUIRED"))
        self.assertEqual(emit_schedule_evidence_from_file(path, identity(), _evidence())[1].status, "FAIL")


class AdversarialQaFileTests(unittest.TestCase):
    def _report(self, bad_green, clean_red=0):
        return {
            "runId": "r1", "buildId": "b", "completed": True,
            "summary": {"projectBad": 10, "projectBadGreen": bad_green,
                        "heldOutBad": 5, "heldOutGreen": 0, "clean": 5,
                        "cleanRed": clean_red, "canonicalTouched": 0},
            "results": [{"expectedStatus": "FAIL", "caught": True}] * 10,
        }

    def test_clean_report_passes(self):
        path = _write("adv-clean.json", json.dumps(self._report(0)))
        self.assertEqual(emit_adversarial_qa_from_file(path, identity(), _evidence())[1].status, "PASS")

    def test_escaped_mutation_fails(self):
        path = _write("adv-bad.json", json.dumps(self._report(1)))
        self.assertEqual(emit_adversarial_qa_from_file(path, identity(), _evidence())[1].status, "FAIL")

    def test_aborted_report_fails(self):
        report = self._report(0)
        report["aborted"] = True
        report["completed"] = False
        path = _write("adv-abort.json", json.dumps(report))
        self.assertEqual(emit_adversarial_qa_from_file(path, identity(), _evidence())[1].status, "FAIL")


class PriorFrozenToolsTests(unittest.TestCase):
    def test_frozen_nonregression_runs(self):
        # The real Ch1/Ch2 frozen files are unchanged, so this must PASS.
        status = emit_prior_frozen_from_tools(identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")


if __name__ == "__main__":
    unittest.main()
