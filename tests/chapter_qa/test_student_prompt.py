"""STUDENT_PROMPT_CLARITY classification tests: vague prompts fail, scoped pass."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.student_prompt import assess_prompts, extract_prompts  # noqa: E402


def _status(prompts):
    findings = assess_prompts(prompts)
    return "FAIL" if findings else "PASS"


class StudentPromptClarityTests(unittest.TestCase):
    def test_vague_prompts_fail(self):
        for text, classification in (
            ("Use evidence.", "CLAIM_EVIDENCE"),
            ("Infer the relationship.", "EXPLAIN"),
            ("What does this show?", "EXPLAIN"),
            ("Explain why.", "EXPLAIN"),
            ("What is that change?", "OBSERVE"),
        ):
            status = _status([{"artifact": "practice", "anchor": "q1", "text": text, "classification": classification}])
            self.assertEqual(status, "FAIL", text)

    def test_read_data_without_scope_fails(self):
        status = _status([{"artifact": "lab", "anchor": "q1", "text": "Which was greater?", "classification": "READ_DATA"}])
        self.assertEqual(status, "FAIL")

    def test_claim_without_evidence_fails(self):
        status = _status([{"artifact": "lab", "anchor": "q1", "text": "What is your claim?", "classification": "CLAIM_EVIDENCE"}])
        self.assertEqual(status, "FAIL")

    def test_scoped_prompts_pass(self):
        prompts = [
            {"artifact": "lab", "anchor": "compare", "text": "Compare your 1-book and 3-book averages. Which moved the cup farther?", "classification": "COMPARE"},
            {"artifact": "lab", "anchor": "evidence", "text": "Write two actual average cup-movement values from your table that support your claim.", "classification": "CLAIM_EVIDENCE"},
            {"artifact": "lab", "anchor": "extend", "text": "If you tested a ramp height between two tested heights, what cup movement would you predict from your graph?", "classification": "EXTEND"},
        ]
        self.assertEqual(_status(prompts), "PASS")

    def test_more_than_one_extension_fails(self):
        prompts = [
            {"artifact": "lab", "anchor": "e1", "text": "What would you predict for a new height?", "classification": "EXTEND"},
            {"artifact": "lab", "anchor": "e2", "text": "What else could you test?", "classification": "EXTEND"},
        ]
        self.assertEqual(_status(prompts), "FAIL")

    def test_missing_classification_fails(self):
        self.assertEqual(_status([{"artifact": "lab", "anchor": "q1", "text": "Read the graph."}]), "FAIL")

    def test_empty_prompts_fail(self):
        self.assertTrue(assess_prompts(None))
        self.assertEqual(_status([]), "FAIL")

    def test_extract_prompts_opens_files(self):
        work = ROOT / "qa" / "work" / "_prompt_extract"
        work.mkdir(parents=True, exist_ok=True)
        f = work / "lab.md"
        f.write_text("Compare your 1-book and 3-book averages. Which moved the cup farther?\nInfer the relationship.\n", encoding="utf-8")
        prompts = extract_prompts([{"artifact": "lab", "path": f.relative_to(ROOT).as_posix()}])
        texts = [p["text"] for p in prompts]
        self.assertTrue(any("Compare your 1-book" in t for t in texts))
        self.assertTrue(any("Infer the relationship" in t for t in texts))


if __name__ == "__main__":
    unittest.main()
