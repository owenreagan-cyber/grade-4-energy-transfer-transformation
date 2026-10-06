"""Status and version authority.

Historical narrative may mention an old candidate state. A current
human-facing surface may not contradict the authoritative status.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chapter_qa.emit import seal
from chapter_qa.lifecycle import STATES
from chapter_qa.severity import resolve_severity

SURFACE_CLASSES = (
    "AUTHORITATIVE_STATUS",
    "BUILD_LABEL",
    "HISTORICAL_NARRATIVE",
    "HUMAN_FACING_STATUS",
)

def _collapsed(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


CANDIDATE_LANGUAGE = re.compile(
    r"remediation candidate|phase 7\.3 candidate|is not frozen",
    re.I,
)


def find_conflicts(authoritative: str, surfaces: list[dict]) -> list[dict]:
    if authoritative not in STATES and authoritative not in ("",):
        raise ValueError("unknown authoritative status %s" % authoritative)
    findings = []
    for surface in surfaces:
        kind = surface.get("kind")
        if kind not in SURFACE_CLASSES:
            raise ValueError("unknown surface class %s" % kind)
        text = _collapsed(surface.get("text") or "")
        if kind == "HISTORICAL_NARRATIVE":
            continue
        if kind == "BUILD_LABEL" and not CANDIDATE_LANGUAGE.search(text):
            continue
        if kind == "AUTHORITATIVE_STATUS" and text and text != authoritative:
            decision = resolve_severity("missing_release_artifact")
            findings.append({
                "severity": decision["severity"],
                "code": "status_conflict",
                "message": "authoritative surface %s says %s" % (surface.get("surfaceId"), text),
                "failsGate": True,
            })
        if kind in ("HUMAN_FACING_STATUS", "BUILD_LABEL") and authoritative == "FROZEN" and CANDIDATE_LANGUAGE.search(text):
            decision = resolve_severity("stale_human_status", {"before_freeze": False})
            findings.append({
                "severity": decision["severity"],
                "code": "stale_human_status",
                "message": "current surface %s still describes a candidate: %s" % (surface.get("surfaceId"), text.strip()[:180]),
                "failsGate": decision["failsGate"],
            })
    return findings


def emit_status_evidence(authoritative, surfaces, identity, evidence_path, *, auditor_role=None):
    findings = find_conflicts(authoritative, surfaces)
    fails = any(item["failsGate"] for item in findings)
    labels = [surface.get("surfaceId") or surface["kind"] for surface in surfaces]
    data = {
        "evidenceId": "status-authority",
        "gateId": "STATUS_AUTHORITY",
        "auditorRole": auditor_role,
        "performed": bool(surfaces),
        "expectedInputs": labels,
        "observedInputs": labels if surfaces else [],
        "thingBeingCertified": "candidate-status:%s" % identity.candidateHash,
        "independentEvidenceSource": "authoritative-lifecycle:%s" % authoritative,
        "findings": [{"severity": item["severity"], "code": item["code"], "message": item["message"]} for item in findings],
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": bool(surfaces),
            "detectorException": False,
            "requiredInputsPresent": bool(surfaces),
            "missingRender": False,
            "missingEvidence": not bool(surfaces),
            "stale": False,
            "gateSpecificFailure": fails,
            "unavailableEvidence": False,
        },
        "inventory": [{
            "name": "statusSurfaces",
            "expected": len(surfaces),
            "observed": len(surfaces),
        }],
    }
    if not surfaces:
        data["expectedInputs"] = []
        data["observedInputs"] = []
        data["inventory"] = [{"name": "statusSurfaces", "expected": 0, "observed": 0}]
    return seal(data, identity)
