"""Phase 1.1 regression tests for the iPad QA capture modes + screenshot cache.

These test the pure planning/cache logic only (no simulator, no xcodebuild).
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from ipad_qa_driver import (  # noqa: E402
    MODE_CHANGED_ONLY,
    MODE_FULL,
    MODE_PREVIEW,
    cache_key,
    parse_pages,
    plan_screenshot_names,
    resolve_plan,
)

HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64


def _artifacts():
    return [
        {
            "artifactId": "ch3-guided-notes",
            "artifactType": "GUIDED_NOTES",
            "artifactSHA256": HASH_A,
            "currentSHA256": HASH_A,
            "expectedPages": 3,
            "orientation": "portrait",
            "viewMode": "fit-page",
            "chapter": 3,
        },
        {
            "artifactId": "ch3-quiz",
            "artifactType": "QUIZ",
            "artifactSHA256": HASH_B,
            "currentSHA256": HASH_B,
            "expectedPages": 1,
            "orientation": "portrait",
            "viewMode": "fit-page",
            "chapter": 3,
        },
        {
            "artifactId": "ch3-slides",
            "artifactType": "SLIDE_PDF",
            "artifactSHA256": HASH_C,
            "currentSHA256": HASH_C,
            "expectedPages": 41,
            "orientation": "landscape",
            "viewMode": "fit-page",
            "chapter": 3,
        },
    ]


DEVICE = {"slug": "ipad-a16-sim", "os": "26.5", "model": "iPad (A16)"}


class PreviewModeTests(unittest.TestCase):
    def test_selects_only_requested_artifact(self):
        plan = resolve_plan(MODE_PREVIEW, _artifacts(), {}, DEVICE, artifact_sel="ch3-quiz")
        self.assertEqual(plan["evidenceClass"], "preview")
        self.assertEqual([i["artifactId"] for i in plan["capture"]], ["ch3-quiz"])
        self.assertEqual(plan["cached"], [])

    def test_default_first_page(self):
        plan = resolve_plan(MODE_PREVIEW, _artifacts(), {}, DEVICE, artifact_sel="ch3-guided-notes")
        self.assertEqual(plan["capture"][0]["pages"], [1])

    def test_pages_restricted(self):
        plan = resolve_plan(MODE_PREVIEW, _artifacts(), {}, DEVICE,
                            artifact_sel="ch3-guided-notes", pages_spec="2,3")
        self.assertEqual(plan["capture"][0]["pages"], [2, 3])

    def test_does_not_capture_unrelated_artifacts(self):
        plan = resolve_plan(MODE_PREVIEW, _artifacts(), {}, DEVICE, artifact_sel="ch3-quiz")
        captured_ids = {i["artifactId"] for i in plan["capture"]}
        self.assertNotIn("ch3-guided-notes", captured_ids)
        self.assertNotIn("ch3-slides", captured_ids)

    def test_slides_shorthand_selects_slide_deck(self):
        plan = resolve_plan(MODE_PREVIEW, _artifacts(), {}, DEVICE, slides_spec="12,28,30")
        self.assertEqual([i["artifactId"] for i in plan["capture"]], ["ch3-slides"])
        self.assertEqual(plan["capture"][0]["pages"], [12, 28, 30])

    def test_unknown_artifact_errors(self):
        plan = resolve_plan(MODE_PREVIEW, _artifacts(), {}, DEVICE, artifact_sel="nope")
        self.assertTrue(plan["errors"])
        self.assertEqual(plan["capture"], [])


class FullModeTests(unittest.TestCase):
    def test_captures_every_artifact_every_page(self):
        plan = resolve_plan(MODE_FULL, _artifacts(), {}, DEVICE)
        self.assertEqual(plan["evidenceClass"], "certification")
        self.assertEqual([i["artifactId"] for i in plan["capture"]],
                         ["ch3-guided-notes", "ch3-quiz", "ch3-slides"])
        self.assertTrue(all(i["pages"] is None for i in plan["capture"]))
        self.assertEqual(plan["cached"], [])


class ChangedOnlyModeTests(unittest.TestCase):
    def _entry(self, artifact, device=DEVICE):
        key = cache_key(artifact["artifactId"], artifact["currentSHA256"],
                        device["slug"], device["os"], artifact["orientation"],
                        artifact["viewMode"], artifact["expectedPages"])
        return key, {"artifactId": artifact["artifactId"], "pageCount": artifact["expectedPages"]}

    def test_unchanged_artifact_uses_cache(self):
        arts = _artifacts()
        key, entry = self._entry(arts[1])  # ch3-quiz cached
        plan = resolve_plan(MODE_CHANGED_ONLY, arts, {key: entry}, DEVICE)
        self.assertEqual(plan["evidenceClass"], "changed-only")
        cached_ids = [c["artifactId"] for c in plan["cached"]]
        captured_ids = [i["artifactId"] for i in plan["capture"]]
        self.assertIn("ch3-quiz", cached_ids)
        self.assertNotIn("ch3-quiz", captured_ids)
        # the other two are not cached -> captured
        self.assertEqual(set(captured_ids), {"ch3-guided-notes", "ch3-slides"})

    def test_changed_artifact_recaptures(self):
        arts = _artifacts()
        # cache holds the OLD hash for ch3-quiz
        old = dict(arts[1], currentSHA256=HASH_A)
        key, entry = self._entry(old)
        # but the artifact's current hash is HASH_B (changed) -> key differs
        plan = resolve_plan(MODE_CHANGED_ONLY, arts, {key: entry}, DEVICE)
        self.assertIn("ch3-quiz", [i["artifactId"] for i in plan["capture"]])
        self.assertNotIn("ch3-quiz", [c["artifactId"] for c in plan["cached"]])

    def test_changed_viewer_settings_invalidate_cache(self):
        arts = _artifacts()
        # cached under portrait, but the artifact is now landscape
        portrait = dict(arts[1])
        key, entry = self._entry(portrait)  # orientation=portrait
        arts[1]["orientation"] = "landscape"
        plan = resolve_plan(MODE_CHANGED_ONLY, arts, {key: entry}, DEVICE)
        self.assertIn("ch3-quiz", [i["artifactId"] for i in plan["capture"]])

    def test_changed_os_invalidates_cache(self):
        arts = _artifacts()
        key, entry = self._entry(arts[1])  # os 26.5
        other_device = {"slug": "ipad-a16-sim", "os": "27.0", "model": "iPad (A16)"}
        plan = resolve_plan(MODE_CHANGED_ONLY, arts, {key: entry}, other_device)
        self.assertIn("ch3-quiz", [i["artifactId"] for i in plan["capture"]])


class CacheKeyTests(unittest.TestCase):
    def test_wrong_hash_invalidates(self):
        a = cache_key("x", HASH_A, "s", "26.5", "portrait", "fit-page", 3)
        b = cache_key("x", HASH_B, "s", "26.5", "portrait", "fit-page", 3)
        self.assertNotEqual(a, b)

    def test_wrong_device_invalidates(self):
        a = cache_key("x", HASH_A, "ipad-a16-sim", "26.5", "portrait", "fit-page", 3)
        b = cache_key("x", HASH_A, "ipad-a16-sim", "27.0", "portrait", "fit-page", 3)
        c = cache_key("x", HASH_A, "other-device", "26.5", "portrait", "fit-page", 3)
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)

    def test_stable_for_same_inputs(self):
        a = cache_key("x", HASH_A, "s", "26.5", "portrait", "fit-page", 3)
        b = cache_key("x", HASH_A, "s", "26.5", "portrait", "fit-page", 3)
        self.assertEqual(a, b)


class ParsePagesTests(unittest.TestCase):
    def test_list(self):
        self.assertEqual(parse_pages("1,2"), [1, 2])

    def test_range(self):
        self.assertEqual(parse_pages("1-3"), [1, 2, 3])

    def test_mixed(self):
        self.assertEqual(parse_pages("1-3,5"), [1, 2, 3, 5])

    def test_single(self):
        self.assertEqual(parse_pages("2"), [2])

    def test_none(self):
        self.assertIsNone(parse_pages(None))
        self.assertIsNone(parse_pages(""))


class ScreenshotNamingTests(unittest.TestCase):
    def test_duplicate_screenshot_names_fail(self):
        arts = _artifacts()
        by_id = {a["artifactId"]: a for a in arts}
        plan = [{"artifactId": "ch3-quiz", "pages": [1, 1], "currentSHA256": HASH_B}]
        _, dups = plan_screenshot_names(plan, by_id, DEVICE["slug"])
        self.assertTrue(dups, "duplicate page list must produce duplicate screenshot names")

    def test_unique_plan_has_no_duplicates(self):
        arts = _artifacts()
        by_id = {a["artifactId"]: a for a in arts}
        plan = [{"artifactId": "ch3-guided-notes", "pages": None, "currentSHA256": HASH_A}]
        names, dups = plan_screenshot_names(plan, by_id, DEVICE["slug"])
        self.assertEqual(len(names), 3)
        self.assertEqual(dups, [])


if __name__ == "__main__":
    unittest.main()
