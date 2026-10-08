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

# Release-status claims a human-facing surface may make. A claim that outranks
# the authoritative lifecycle state is stale and must not stay green.
_RELEASE_CLAIM = re.compile(r"\b(CERTIFIED|APPROVED|RELEASED|FROZEN)\b", re.I)
_NEGATION = re.compile(r"\b(not|never|no|n't)\b", re.I)

_CLAIM_LEVEL = {
    "CERTIFIED": 3,
    "APPROVED": 4,
    "RELEASED": 5,
    "FROZEN": 5,
}
_LIFECYCLE_LEVEL = {
    "BUILD_IN_PROGRESS": 0,
    "BUILT_UNCERTIFIED": 1,
    "INTERNAL_AUDIT_PENDING": 2,
    "INTERNAL_AUDIT_FAILED": 1,
    "INTERNALLY_CERTIFIED": 3,
    "EXTERNAL_AUDIT_PENDING": 3,
    "EXTERNAL_AUDIT_REJECTED": 1,
    "APPROVED_FOR_FREEZE": 4,
    "FROZEN": 5,
}


def _max_release_claim(text: str) -> int:
    """Highest positive (non-negated) release claim present in the surface text."""
    level = 0
    for match in _RELEASE_CLAIM.finditer(text):
        before = text[:match.start()]
        if _NEGATION.search(before[-20:]):
            continue
        level = max(level, _CLAIM_LEVEL[match.group(1).upper()])
    return level


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
        if kind in ("HUMAN_FACING_STATUS", "BUILD_LABEL"):
            if authoritative == "FROZEN" and CANDIDATE_LANGUAGE.search(text):
                decision = resolve_severity("stale_human_status", {"before_freeze": False})
                findings.append({
                    "severity": decision["severity"],
                    "code": "stale_human_status",
                    "message": "current surface %s still describes a candidate: %s" % (surface.get("surfaceId"), text.strip()[:180]),
                    "failsGate": decision["failsGate"],
                })
            # A release claim (RELEASED/CERTIFIED/APPROVED/FROZEN) must not
            # outrank the authoritative lifecycle. Human-facing surfaces cannot
            # outrank lifecycle authority.
            auth_level = _LIFECYCLE_LEVEL.get(authoritative, 0)
            claim_level = _max_release_claim(text)
            if claim_level > auth_level:
                decision = resolve_severity("stale_status_claim")
                findings.append({
                    "severity": decision["severity"],
                    "code": "stale_status_claim",
                    "message": "current surface %s claims a release status the lifecycle does not support: %s" % (surface.get("surfaceId"), text.strip()[:180]),
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
    return seal(data, identity, producer=True)


def read_surfaces_from_files(surface_files: list[dict], root=None) -> list[dict]:
    """Open actual status-surface files and derive their text from disk.

    Each entry is ``{"surfaceId": str, "kind": SURFACE_CLASS, "path": relpath}``.
    The producer reads the file bytes; it never trusts caller-supplied text.
    """
    from chapter_qa.observation import read_any_text
    from chapter_qa.identity import REPO_ROOT as _ROOT

    base = root or _ROOT
    surfaces = []
    for entry in surface_files or []:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        if not path:
            continue
        text = read_any_text(str(path), base)
        surfaces.append({
            "surfaceId": entry.get("surfaceId") or str(path),
            "kind": entry.get("kind") or "HUMAN_FACING_STATUS",
            "text": text,
            "path": str(path),
        })
    return surfaces


def emit_status_evidence_from_files(authoritative, surface_files, identity, evidence_path, *, auditor_role="CROSS_ARTIFACT_AUDITOR"):
    """File-observing STATUS_AUTHORITY: open actual status surfaces from a registry."""
    surfaces = read_surfaces_from_files(surface_files)
    findings = find_conflicts(authoritative, surfaces)
    fails = any(item["failsGate"] for item in findings)
    labels = [surface["surfaceId"] for surface in surfaces]
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
    return seal(data, identity, producer=True)
