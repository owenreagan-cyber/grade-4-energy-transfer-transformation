"""Build (or verify) the frozen-chapter registry of protected byte hashes.

The registry maps repo-relative path -> SHA-256 for every frozen classroom
artifact of Unit 1 Chapter 1, Unit 1 Chapter 2, and the combined frozen
playbook. Its own integrity is anchored by a pinned hash in the enforcement
hook (``.git/hooks/pre-commit``), not by this file.

Usage:
  .venv/bin/python tools/chapter_qa/build_frozen_registry.py --write   (regenerate)
  .venv/bin/python tools/chapter_qa/build_frozen_registry.py --check   (verify unchanged)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "qa" / "gold-standard" / "frozen_registry.json"

# Unit 1 Chapter 1 classroom artifacts (all byte outputs, not u2).
CH1_GLOBS = (
    "production/premium-notes/01-ch1-*",
    "production/slides/01-ch1-*",
    "production/quizzes/01-ch1-*",
    "production/worksheets/01-ch1-*",
    "production/answer-keys/01-ch1-*",
    "production/labs/01-ch1-*",
)
# Unit 1 Chapter 2 classroom artifacts.
CH2_GLOBS = (
    "production/premium-notes/02-ch2-*",
    "production/slides/02-ch2-*",
    "production/quizzes/02-ch2-*",
    "production/worksheets/02-ch2-*",
    "production/answer-keys/02-ch2-*",
    "production/labs/02-ch2-*",
)
PLAYBOOK_GLOBS = (
    "production/teacher-playbook/unit1-teacher-playbook.docx",
    "production/teacher-playbook/unit1-teacher-playbook.pdf",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _glob_paths(globs) -> list[str]:
    found = set()
    for pattern in globs:
        for p in ROOT.glob(pattern):
            if p.is_file():
                found.add(p.relative_to(ROOT).as_posix())
    return sorted(found)


def build_registry() -> dict:
    files = {}
    for rel in _glob_paths(CH1_GLOBS + CH2_GLOBS + PLAYBOOK_GLOBS):
        files[rel] = _sha256(ROOT / rel)
    return {
        "schemaVersion": "1.0",
        "description": "Frozen Unit 1 Chapter 1 and Chapter 2 classroom bytes plus the combined playbook. Path -> SHA-256.",
        "chapters": {
            "1": {"version": "1.1", "freezeCommit": "279a9de"},
            "2": {"version": "1.0", "freezeCommit": "a491193ddf74598910247385a2f55a4458b8b55c"},
        },
        "playbook": "production/teacher-playbook/unit1-teacher-playbook.docx",
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.write:
        registry = build_registry()
        REGISTRY.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote %s (%d files)" % (REGISTRY, len(registry["files"])))
        return 0

    if args.check:
        current = build_registry()["files"]
        try:
            stored = json.loads(REGISTRY.read_text(encoding="utf-8"))["files"]
        except (OSError, ValueError, KeyError):
            print("registry missing or unreadable")
            return 1
        mism = sorted(set(stored) ^ set(current)) + [p for p in stored if p in current and stored[p] != current[p]]
        if mism:
            for item in mism:
                print("MISMATCH: %s" % item)
            return 1
        print("frozen registry unchanged (%d files)" % len(stored))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
