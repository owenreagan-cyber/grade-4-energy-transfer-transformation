"""Producers for the nine previously unbound mandatory gates, and staging authorization."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.adversary import make_identity  # noqa: E402
from chapter_qa.mandatory_producers import (  # noqa: E402
    emit_adversarial_qa,
    emit_answer_leakage,
    emit_chapter_spec,
    emit_fresh_export,
    emit_inventory,
    emit_notes_structure,
    emit_prior_frozen,
    emit_retired_content,
    emit_slides_structure,
)
from chapter_qa.registry import PRODUCERS  # noqa: E402
from hooks.protect_git import decide_git  # noqa: E402


def _path(name):
    folder = Path(tempfile.mkdtemp(prefix="producer-"))
    path = folder / name
    path.write_text("{}\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix() if str(path).startswith(str(ROOT)) else str(path)


class ProducerTests(unittest.TestCase):
    def setUp(self):
        self.identity = make_identity("producer-test")
        self.evidence = "qa/gold-standard/evidence.schema.json"

    def test_registry_covers_the_nine_gates(self):
        for gate_id in (
            "CHAPTER_SPEC", "NOTES_STRUCTURE", "SLIDES_STRUCTURE", "ANSWER_LEAKAGE",
            "FRESH_EXPORT", "RETIRED_CONTENT", "INVENTORY", "ADVERSARIAL_QA",
            "PRIOR_FROZEN_NONREGRESSION",
        ):
            self.assertIn(gate_id, PRODUCERS)

    def test_each_new_gate_fails_its_defect_and_passes_when_complete(self):
        spec = {
            "chapter": 2, "identityChapter": 2, "title": "Moving Objects Have Energy",
            "bigQuestion": "How can an object have energy?", "sourceRanges": ["Reader pp. 7-12"],
            "concepts": ["motion"], "exclusions": ["speed-energy"], "vocabulary": ["motion"],
            "anchors": [{"code": "BQ", "order": 1, "status": "REQUIRED"}, {"code": "N1", "order": 2, "status": "REQUIRED"}],
            "schedule": [{"day": "Wednesday"}], "inventory": ["notes"],
        }
        self.assertEqual(emit_chapter_spec(spec, self.identity, self.evidence)[1].status, "PASS")
        broken = dict(spec)
        broken["bigQuestion"] = ""
        self.assertEqual(emit_chapter_spec(broken, self.identity, self.evidence)[1].status, "FAIL")
        self.assertEqual(emit_chapter_spec({}, self.identity, self.evidence)[1].status, "FAIL")

        notes = {
            "pageCount": 3, "anchors": ["BQ", "N1"], "vocabulary": ["motion"], "blankCount": 2,
            "answerKey": "key", "writingSpace": True, "forbidden": ["inertia"], "text": ["motion"],
            "secondSystem": False, "candidateHash": "a" * 64,
        }
        self.assertEqual(emit_notes_structure(notes, notes, self.identity, self.evidence)[1].status, "PASS")
        dup = dict(notes)
        dup["anchors"] = ["BQ", "BQ"]
        self.assertEqual(emit_notes_structure(notes, dup, self.identity, self.evidence)[1].status, "FAIL")

        slides = {
            "slideCount": 3, "anchors": ["BQ", "N1"], "vocabulary": ["motion"], "speakerNotes": ["N1"],
            "planStatus": True, "uncodedAnswer": False, "candidateHash": "a" * 64,
        }
        self.assertEqual(emit_slides_structure(slides, slides, self.identity, self.evidence)[1].status, "PASS")
        short = dict(slides)
        short["anchors"] = ["BQ"]
        short["slideCount"] = 1
        self.assertEqual(emit_slides_structure(slides, short, self.identity, self.evidence)[1].status, "FAIL")

        clean = [
            {"kind": "slide", "anchor": "N1", "reveals": [], "writes": []},
            {"kind": "student", "anchor": "N1", "reveals": [], "writes": ["wheel"], "prefilled": False},
            {"kind": "slide", "anchor": "key", "reveals": ["wheel"], "writes": ["wheel"]},
        ]
        self.assertEqual(emit_answer_leakage(clean, self.identity, self.evidence)[1].status, "PASS")
        for bad in (
            [{"kind": "slide", "anchor": "early", "reveals": ["wheel"], "writes": []}],
            [{"kind": "student", "anchor": "N1", "reveals": [], "writes": ["wheel"], "prefilled": True}],
            [{"kind": "speaker", "anchor": "N1", "reveals": ["wheel"], "writes": []}],
            [{"kind": "uncoded", "anchor": "X", "reveals": ["wheel"], "writes": []}],
        ):
            self.assertEqual(emit_answer_leakage(bad, self.identity, self.evidence)[1].status, "FAIL", bad)

        pair = {
            "label": "notes", "sourceHash": "s", "outputHash": "o", "freshHash": "o",
            "pageCount": 1, "expectedPageCount": 1, "dimensions": "612x792", "expectedDimensions": "612x792",
            "normalizedText": "same", "freshText": "same",
        }
        self.assertEqual(emit_fresh_export([pair], self.identity, self.evidence)[1].status, "PASS")
        self.assertEqual(emit_fresh_export([dict(pair, outputHash="old")], self.identity, self.evidence)[1].status, "FAIL")
        self.assertEqual(emit_fresh_export([], self.identity, self.evidence)[1].status, "FAIL")

        files = [{"name": "live.pdf", "text": "energy", "perceptualHash": "live"}]
        base = [{"token": "interactive science notebook", "perceptualHash": "retired"}]
        self.assertEqual(emit_retired_content(files, base, self.identity, self.evidence)[1].status, "PASS")
        renamed = [{"name": "notes.pdf", "text": "see the interactive science notebook", "perceptualHash": "retired"}]
        self.assertEqual(emit_retired_content(renamed, base, self.identity, self.evidence)[1].status, "FAIL")

        self.assertEqual(emit_inventory(["notes", "slides"], ["notes", "slides"], self.identity, self.evidence)[1].status, "PASS")
        self.assertEqual(emit_inventory(["notes", "slides"], ["notes"], self.identity, self.evidence)[1].status, "FAIL")
        self.assertEqual(emit_inventory([], ["notes"], self.identity, self.evidence)[1].status, "FAIL")

        good = {
            "projectBad": 90, "projectBadGreen": 0, "heldOutBad": 12, "heldOutGreen": 0,
            "clean": 15, "cleanRed": 0, "canonicalRepoTouched": 0, "completed": True,
        }
        self.assertEqual(emit_adversarial_qa(good, self.identity, self.evidence)[1].status, "PASS")
        escaped = dict(good, projectBadGreen=1)
        self.assertEqual(emit_adversarial_qa(escaped, self.identity, self.evidence)[1].status, "FAIL")

        frozen = {
            "1": {"guard": "6/6", "guardExpected": "6/6", "unreviewed": 0, "stale": 0, "parity": "14/14", "parityExpected": "14/14", "churn": 0},
            "2": {"guard": "PASS", "guardExpected": "PASS", "unreviewed": 0, "stale": 0, "parity": "PASS", "parityExpected": "PASS", "churn": 0},
        }
        self.assertEqual(emit_prior_frozen(frozen, self.identity, self.evidence)[1].status, "PASS")
        changed = {"1": dict(frozen["1"], churn=1)}
        self.assertEqual(emit_prior_frozen(changed, self.identity, self.evidence)[1].status, "FAIL")


class StagingTests(unittest.TestCase):
    def test_explicit_authorized_add_is_allowed_and_broad_add_is_denied(self):
        auth = {"workflowAuthorizesStaging": True, "allowedPaths": ["docs/gold-standard/CURSOR_HOOK_PLAN.md"]}
        self.assertEqual(decide_git("git add docs/gold-standard/CURSOR_HOOK_PLAN.md", auth)["decision"], "ALLOW")
        self.assertEqual(decide_git("git add tools/hooks/protect_git.py", auth)["decision"], "DENY")
        self.assertEqual(decide_git("git add .", auth)["decision"], "DENY")
        self.assertEqual(decide_git("git add -A", auth)["decision"], "DENY")
        self.assertEqual(decide_git("git add --all", auth)["decision"], "DENY")
        self.assertEqual(decide_git("git add docs/../tools/hooks/protect_git.py", auth)["decision"], "DENY")
        self.assertEqual(decide_git("git add ../docs/gold-standard/CURSOR_HOOK_PLAN.md", auth)["decision"], "DENY")
        self.assertEqual(decide_git("git commit -a -m msg", {"workflowAuthorizesCommit": True})["decision"], "DENY")
        self.assertEqual(decide_git("git commit --amend -m msg", {"workflowAuthorizesCommit": True})["decision"], "DENY")
        self.assertEqual(decide_git("git add docs/gold-standard/CURSOR_HOOK_PLAN.md", {})["decision"], "DENY")

    def test_commit_and_push_stay_separately_authorized(self):
        self.assertEqual(decide_git("git commit -m msg", {"workflowAuthorizesCommit": False})["decision"], "DENY")
        self.assertEqual(decide_git("git commit -m msg", {"workflowAuthorizesCommit": True})["decision"], "ALLOW")
        self.assertEqual(decide_git("git push", {"workflowAuthorizesCommit": True})["decision"], "DENY")
        self.assertEqual(decide_git("git reset --hard", {"workflowAuthorizesCommit": True, "workflowAuthorizesStaging": True})["decision"], "DENY")


if __name__ == "__main__":
    unittest.main()
