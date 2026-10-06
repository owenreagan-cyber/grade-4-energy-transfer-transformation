"""Phase C adversarial, provenance, and clean-room tests."""

from __future__ import annotations

import shutil
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.adversary import canonical_fingerprint, held_out_cases, promote_release, run_case  # noqa: E402
from chapter_qa.adversary_catalog import cases  # noqa: E402
from chapter_qa.clean_room import same_output_is_not_independent  # noqa: E402
from chapter_qa.heldout import prose  # noqa: E402
from run_adversarial_qa import execute, summarize  # noqa: E402


class PhaseCTests(unittest.TestCase):
    def tearDown(self):
        work = ROOT / "qa" / "work" / "_phase_c"
        if work.exists():
            shutil.rmtree(work)

    def test_held_out_prose_is_not_a_detector_literal(self):
        sentence = prose(20261006, "HELD-T-20261006")
        for path in (
            ROOT / "tools" / "chapter_qa" / "source_audit.py",
            ROOT / "tools" / "chapter_qa" / "visual_qa.py",
            ROOT / "tools" / "qa_status_authority.py",
        ):
            self.assertNotIn(sentence, path.read_text(encoding="utf-8"))

    def test_same_generator_output_is_not_independent(self):
        self.assertTrue(same_output_is_not_independent(b"same", b"same"))
        self.assertFalse(same_output_is_not_independent(b"same", b"other"))

    def test_catalog_covers_required_ids(self):
        ids = {row["caseId"] for row in cases()}
        for required in (
            "T01", "S01", "L01", "ST03", "SC04", "A01", "R01", "P01", "O01",
            "REL06", "RET01", "B01", "H01", "D01", "E05", "RJ01", "C-JUDGE",
        ):
            self.assertIn(required, ids)

    def test_full_suite_has_no_bad_green_or_clean_red(self):
        before = canonical_fingerprint()
        results, summary = execute(seed=20261006, held_out=True, keep=False)
        self.assertEqual(summary["projectBadGreen"], 0, [row["caseId"] for row in results if row["expectedStatus"] == "FAIL" and not row["caught"] and not str(row["caseId"]).startswith("HELD-")])
        self.assertEqual(summary["heldOutGreen"], 0)
        self.assertEqual(summary["cleanRed"], 0, [row["caseId"] for row in results if row["expectedStatus"] == "PASS" and not row["caught"]])
        self.assertEqual(summary["canonicalTouched"], 0)
        self.assertGreater(summary["projectBadCaught"], 0)
        self.assertGreater(summary["heldOutCaught"], 0)
        self.assertEqual(canonical_fingerprint(), before)
        self.assertEqual(len(held_out_cases(20261006)), 12)

    def test_one_case_records_the_result_contract(self):
        case = next(row for row in cases() if row["caseId"] == "P01")
        result = run_case(case, 7)
        for key in (
            "caseId", "family", "seed", "buildId", "originalHash", "mutatedHash",
            "mutationTarget", "expectedGate", "expectedStatus", "actualGateStatuses",
            "releaseJudgeStatus", "caught", "evidencePaths", "workspacePath", "canonicalRepoTouched",
        ):
            self.assertIn(key, result)
        self.assertFalse(result["canonicalRepoTouched"])
        self.assertTrue(result["caught"])
        self.assertNotEqual(result["actualGateStatuses"]["PDF_QUALITY"], "PASS")

    def test_failed_judgment_does_not_promote(self):
        source = ROOT / "qa" / "work" / "_phase_c" / "promo-src"
        dest = ROOT / "qa" / "work" / "_phase_c" / "promo-dest"
        source.mkdir(parents=True)
        (source / "packet.pdf").write_bytes(b"body")
        blocked = promote_release(type("J", (), {"status": "FAIL"})(), source, dest, ROOT)
        self.assertFalse(blocked["promoted"])
        self.assertFalse(dest.exists())
        with self.assertRaises(ValueError):
            promote_release(type("J", (), {"status": "PASS"})(), source, ROOT / "production" / "releases" / "chapter-02", ROOT)


if __name__ == "__main__":
    unittest.main()
