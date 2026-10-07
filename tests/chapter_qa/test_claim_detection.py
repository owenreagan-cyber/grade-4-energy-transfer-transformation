"""F-10 claim-detection controls: concept terms are sensitive in chapter/build
context, negations and failure/error phrasing stay ordinary.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from hooks.final_release_gate import classify_action  # noqa: E402

DENY_ACTIONS = {
    "chapter_ready",
    "internally_certified",
    "release_ready",
    "ready_for_external_audit",
    "approved_for_freeze",
    "freeze_chapter",
}


class ClaimDetectionTests(unittest.TestCase):
    def assert_sensitive(self, message):
        action = classify_action({"message": message})
        self.assertIn(action, DENY_ACTIONS, message)

    def assert_ordinary(self, message):
        self.assertEqual(classify_action({"message": message}), "ordinary", message)

    def test_positive_claims_are_sensitive(self):
        for message in (
            "chapter ready",
            "the chapter is ready",
            "chapter 3 is ready to ship",
            "good to ship",
            "signed-off",
            "sign off on this",
            "certified internally",
            "the chapter is approved",
            "freeze chapter 3",
            "ready for external audit",
            "release-ready",
            "build complete",
            "propagate the release",
            "chapter is now final",
        ):
            self.assert_sensitive(message)

    def test_negations_and_failures_stay_ordinary(self):
        for message in (
            "why did certification fail?",
            "show me the release errors",
            "this is not ready",
            "the chapter release errors are listed",
            "why is the chapter ready fail?",
            "do not freeze the chapter",
            "the build is not approved",
        ):
            self.assert_ordinary(message)

    def test_no_context_is_ordinary(self):
        for message in (
            "ready",
            "approved",
            "freeze",
            "final answer",
            "complete this step",
            "gold medal",
            "release errors",
        ):
            self.assert_ordinary(message)

    def test_hyphen_and_punctuation_normalization(self):
        self.assert_sensitive("release-ready")
        self.assert_sensitive("release_ready")
        self.assert_sensitive("signed-off")
        self.assert_sensitive("ready-for-external-audit")
        self.assert_sensitive("chapter is READY!")


if __name__ == "__main__":
    unittest.main()
