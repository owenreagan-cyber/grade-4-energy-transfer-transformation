"""F-3 producer-independence self-tests.

Each rewired producer must PASS a good fixture and FAIL a bad fixture through
its normal file-observing entrypoint. Bad fixtures mutate the actual artifact
bytes (not the caller's config), proving the producer reads the file.
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
    emit_chapter_spec,
    emit_inventory,
    emit_notes_structure,
    emit_retired_content,
    emit_slides_structure,
)
from chapter_qa.student_prompt import emit_student_prompt_evidence  # noqa: E402

HASH = "a" * 64
WORK = ROOT / "qa" / "work" / "_f3"


def identity():
    return BuildIdentity(
        buildId="f3-test",
        candidatePath="candidate/chapter-x",
        candidateFreezeId="cand-1",
        candidateHash=HASH,
        sourceFreezeId="src-1",
        sourceHash=HASH,
        inputHashes={"notes": HASH, "reader": HASH},
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


class ChapterSpecFileTests(unittest.TestCase):
    def _spec(self):
        return {
            "chapter": 3, "identityChapter": 3, "title": "Energy and Speed Are Related",
            "bigQuestion": "How are energy and speed related?",
            "sourceRanges": ["Reader pp. 13-16"], "concepts": ["same object"],
            "exclusions": ["kinetic"], "vocabulary": [{"term": "speed"}],
            "anchors": [{"code": "BQ", "order": 1, "status": "REQUIRED"}],
            "schedule": [{"day": "Monday"}], "inventory": ["notes"],
        }

    def test_good_spec_passes(self):
        path = _write("spec-good.json", json.dumps(self._spec()))
        status = emit_chapter_spec(path, identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")

    def test_removed_big_question_fails(self):
        spec = self._spec()
        spec["bigQuestion"] = ""
        path = _write("spec-bad.json", json.dumps(spec))
        status = emit_chapter_spec(path, identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")

    def test_missing_file_fails(self):
        status = emit_chapter_spec("qa/work/_f3/does-not-exist.json", identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")


class NotesStructureFileTests(unittest.TestCase):
    def _expected(self):
        return {"anchors": ["BQ", "N1"], "blankCount": 2, "forbidden": ["inertia"],
                "answerKey": None, "vocabulary": ["speed"], "writingSpace": True}

    def test_good_notes_pass(self):
        path = _write("notes-good.md", "BQ How are energy and speed related?\nN1 Compare the same ball.\nspeed ____ ____")
        status = emit_notes_structure(path, self._expected(), identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")

    def test_removed_anchor_fails(self):
        path = _write("notes-no-anchor.md", "How are energy and speed related?\nCompare the same ball.\nspeed ____ ____")
        status = emit_notes_structure(path, self._expected(), identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")

    def test_forbidden_term_fails(self):
        path = _write("notes-forbidden.md", "BQ q\nN1 q\ninertia ____ ____")
        status = emit_notes_structure(path, self._expected(), identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")


class SlidesStructureFileTests(unittest.TestCase):
    def _expected(self):
        return {"slideCount": 2, "anchors": ["BQ", "N1"], "speakerNotes": ["N1"]}

    def test_good_slides_pass(self):
        path = _write("slides-good.md", "SLIDE 1\nBQ q\nSLIDE 2\nN1 q\nNOTES 1\nN1")
        status = emit_slides_structure(path, self._expected(), identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")

    def test_deleted_slide_fails(self):
        path = _write("slides-one.md", "SLIDE 1\nBQ q\nNOTES 1\nN1")
        status = emit_slides_structure(path, self._expected(), identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")

    def test_removed_anchor_fails(self):
        path = _write("slides-no-n1.md", "SLIDE 1\nBQ q\nSLIDE 2\nNOTES 1\n")
        status = emit_slides_structure(path, self._expected(), identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")


class InventoryFileTests(unittest.TestCase):
    def test_scan_matches(self):
        _write("set/a.txt", "a")
        _write("set/b.txt", "b")
        status = emit_inventory(["a.txt", "b.txt"], "qa/work/_f3/set", identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")

    def test_missing_file_fails(self):
        _write("set2/a.txt", "a")
        status = emit_inventory(["a.txt", "b.txt"], "qa/work/_f3/set2", identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")


class RetiredContentFileTests(unittest.TestCase):
    def _baselines(self):
        return [{"token": "interactive science notebook", "perceptualHash": None}]

    def test_clean_dir_passes(self):
        _write("ret/ok.txt", "energy and speed")
        status = emit_retired_content("qa/work/_f3/ret", self._baselines(), identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")

    def test_retired_token_fails(self):
        _write("ret2/bad.txt", "see the interactive science notebook")
        status = emit_retired_content("qa/work/_f3/ret2", self._baselines(), identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")


class StudentPromptFileTests(unittest.TestCase):
    def test_scoped_prompts_pass(self):
        path = _write("lab.md", "Compare your 1-book and 3-book averages. Which moved the cup farther?\nWrite two actual average cup-movement values from your table that support your claim.")
        files = [{"artifact": "lab", "path": path}]
        status = emit_student_prompt_evidence(files, identity(), _evidence())[1].status
        self.assertEqual(status, "PASS")

    def test_vague_prompt_fails(self):
        path = _write("lab2.md", "Infer the relationship.")
        files = [{"artifact": "lab", "path": path}]
        status = emit_student_prompt_evidence(files, identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")

    def test_missing_files_fails(self):
        status = emit_student_prompt_evidence([], identity(), _evidence())[1].status
        self.assertEqual(status, "FAIL")


if __name__ == "__main__":
    unittest.main()
