#!/usr/bin/env python3
"""Defect register schema + helpers (reusable across chapters).

A defect record binds a slide to its stable identity, category, severity,
evidence, expected/actual behavior, proposed repair, and retest result.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

CATEGORIES = [
    "TEXT_CLIP_OVERFLOW",
    "FONT_READABILITY",
    "IMAGE_QUALITY",
    "ASPECT_RATIO",
    "OVERLAP",
    "LABEL_BADGE",
    "HIERARCHY_ALIGNMENT",
    "COMPOSITION",
    "SCIENCE_ERROR",
    "ANSWER_LEAK",
    "CURRICULUM_PARITY",
    "VIDEO_MISSING",
    "VIDEO_PLAYBACK",
    "VIDEO_CONTENT",
    "SLIDE_COUNT",
    "SEQUENCE",
]

SEVERITIES = ["BLOCKING", "HIGH", "MEDIUM", "LOW", "INFO"]

REPAIR_STATUS = ["OPEN", "IN_PROGRESS", "FIXED", "WONT_FIX", "NOT_A_DEFECT"]

STATUS = ["NOT_VERIFIED", "PASS", "FAIL"]


def new_defect(slide: int, slide_id: str, category: str, severity: str,
               evidence: list[str], expected: str, actual: str,
               proposed_repair: str) -> dict:
    if category not in CATEGORIES:
        raise ValueError(f"unknown category {category!r}")
    if severity not in SEVERITIES:
        raise ValueError(f"unknown severity {severity!r}")
    return {
        "slide": slide,
        "slideId": slide_id,
        "category": category,
        "severity": severity,
        "evidence": evidence,
        "expected": expected,
        "actual": actual,
        "proposedRepair": proposed_repair,
        "repairStatus": "OPEN",
        "retestResult": None,
    }


class DefectRegister:
    def __init__(self, path: str):
        self.path = Path(path)
        self.data = {
            "schemaVersion": 1,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "defects": [],
        }

    def add(self, defect: dict) -> None:
        self.data["defects"].append(defect)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    @staticmethod
    def load(path: str) -> "DefectRegister":
        r = DefectRegister(path)
        r.data = json.loads(Path(path).read_text(encoding="utf-8"))
        return r

    def mark_retest(self, slide: int, slide_id: str, result: str) -> None:
        for d in self.data["defects"]:
            if d["slide"] == slide and d["slideId"] == slide_id:
                d["retestResult"] = result
                d["repairStatus"] = "FIXED" if result == "PASS" else d["repairStatus"]
