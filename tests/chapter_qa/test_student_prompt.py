"""STUDENT_PROMPT_CLARITY gate fixtures: vague prompts fail, scoped prompts pass."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.identity import BuildIdentity  # noqa: E402
from chapter_qa.student_prompt import assess_prompts, emit_student_prompt_evidence  # noqa: E402

HASH = "a" * 64


def identity():
    return BuildIdentity(
        buildId="build-A",
        candidatePath="candidate/chapter-x",
        candidateFreezeId="cand-1",
        candidateHash=HASH,
        sourceFreezeId="src-1",
        sourceHash=HASH,
        inputHashes={"notes": HASH, "reader": HASH},
    )


def _status(prompts):
    from chapter_qa.student_prompt import emit_student_prompt_evidence
    path = ROOT / "qa" / "work" / "_prompt_evidence.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}\n", encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    stored, result = emit_student_prompt_evidence(prompts, identity(), rel)
    return result.status, stored


class StudentPromptClarityTests(unittest.TestCase):
    def test_vague_prompts_fail(self):
        for text, classification in (
            ("Use evidence.", "CLAIM_EVIDENCE"),
            ("Infer the relationship.", "EXPLAIN"),
            ("What does this show?", "EXPLAIN"),
            ("Explain why.", "EXPLAIN"),
            ("What is that change?", "OBSERVE"),
        ):
            status, _stored = _status([{"artifact": "practice", "anchor": "q1", "text": text, "classification": classification}])
            self.assertEqual(status, "FAIL", text)

    def test_read_data_without_scope_fails(self):
        status, _ = _status([{"artifact": "lab", "anchor": "q1", "text": "Which was greater?", "classification": "READ_DATA"}])
        self.assertEqual(status, "FAIL")

    def test_claim_without_evidence_fails(self):
        status, _ = _status([{"artifact": "lab", "anchor": "q1", "text": "What is your claim?", "classification": "CLAIM_EVIDENCE"}])
        self.assertEqual(status, "FAIL")

    def test_scoped_prompts_pass(self):
        prompts = [
            {"artifact": "lab", "anchor": "compare", "text": "Compare your 1-book and 3-book averages. Which moved the cup farther?", "classification": "COMPARE"},
            {"artifact": "lab", "anchor": "evidence", "text": "Write two actual average cup-movement values from your table that support your claim.", "classification": "CLAIM_EVIDENCE"},
            {"artifact": "lab", "anchor": "extend", "text": "If you tested a ramp height between two tested heights, what cup movement would you predict from your graph?", "classification": "EXTEND"},
        ]
        status, _ = _status(prompts)
        self.assertEqual(status, "PASS")

    def test_more_than_one_extension_fails(self):
        prompts = [
            {"artifact": "lab", "anchor": "e1", "text": "What would you predict for a new height?", "classification": "EXTEND"},
            {"artifact": "lab", "anchor": "e2", "text": "What else could you test?", "classification": "EXTEND"},
        ]
        status, _ = _status(prompts)
        self.assertEqual(status, "FAIL")

    def test_missing_classification_fails(self):
        status, _ = _status([{"artifact": "lab", "anchor": "q1", "text": "Read the graph."}])
        self.assertEqual(status, "FAIL")

    def test_empty_prompts_fail(self):
        self.assertTrue(assess_prompts(None))
        self.assertEqual(_status([])[0], "FAIL")


if __name__ == "__main__":
    unittest.main()
