"""Cross-artifact comparison.

Agreement between notes and slides is not source authority and cannot
satisfy SOURCE_AUTHORITY or CURRICULUM_CORRECTNESS.
"""

from __future__ import annotations

import re

from chapter_qa.emit import seal
from chapter_qa.severity import resolve_severity

ARTIFACT_CLASSES = (
    "guided_notes",
    "notes_key",
    "slides",
    "speaker_notes",
    "practice",
    "practice_key",
    "quiz",
    "quiz_key",
    "lab",
    "recovery",
    "playbook",
    "chapter_spec",
)

DIMENSIONS = (
    "instructional_text",
    "anchor_code",
    "vocabulary",
    "blanks",
    "answers",
    "sequence",
    "labels",
    "punctuation",
    "page_ownership",
    "required_status",
    "scoring",
    "source_references",
)

ALLOWED_GATES = ("NOTES_SLIDES_SYNC", "PLAYBOOK_ALIGNMENT", "ASSESSMENT_ALIGNMENT")
HIGH_DIMENSIONS = {"answers", "vocabulary", "scoring", "blanks"}
GATE_PAIRS = {
    "NOTES_SLIDES_SYNC": frozenset({"guided_notes", "slides"}),
    "PLAYBOOK_ALIGNMENT": frozenset({"playbook", "chapter_spec"}),
    "ASSESSMENT_ALIGNMENT": frozenset({
        frozenset({"practice", "practice_key"}),
        frozenset({"quiz", "quiz_key"}),
        frozenset({"lab", "notes_key"}),
    }),
}
GATE_DIMENSIONS = {
    "NOTES_SLIDES_SYNC": ("instructional_text", "vocabulary", "anchor_code"),
    "PLAYBOOK_ALIGNMENT": ("instructional_text", "required_status"),
    "ASSESSMENT_ALIGNMENT": ("answers", "scoring", "blanks"),
}


def _words(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def compare(left: dict, right: dict, dimensions=None) -> list[dict]:
    dimensions = tuple(dimensions or DIMENSIONS)
    diffs = []
    anchors = sorted(set(left.get("anchors") or {}) | set(right.get("anchors") or {}))
    for anchor in anchors:
        left_row = (left.get("anchors") or {}).get(anchor) or {}
        right_row = (right.get("anchors") or {}).get(anchor) or {}
        for dimension in dimensions:
            left_has = dimension in left_row
            right_has = dimension in right_row
            a = left_row.get(dimension)
            b = right_row.get(dimension)
            if not left_has or not right_has or a != b:
                kind = "missing" if not left_has or not right_has else "content"
                if dimension not in HIGH_DIMENSIONS and a is not None and b is not None and _words(str(a)) == _words(str(b)):
                    kind = "punctuation"
                diffs.append({
                "anchor": anchor,
                "dimension": dimension,
                "kind": kind,
                "left": a,
                "right": b,
            })
    return diffs


def _severity_for(diff: dict) -> dict:
    if diff["dimension"] in HIGH_DIMENSIONS or diff["kind"] == "missing":
        return resolve_severity("answer_mismatch")
    if diff["kind"] == "punctuation":
        return resolve_severity("minor_spacing")
    return {"severity": "MEDIUM", "failsGate": True}


def emit_cross_evidence(left, right, identity, gate_id, evidence_path: str, *, dimensions=None, auditor_role=None):
    if gate_id not in ALLOWED_GATES:
        raise ValueError("cross-artifact evidence cannot satisfy %s" % gate_id)
    for side in (left, right):
        if side.get("artifactClass") not in ARTIFACT_CLASSES:
            raise ValueError("unknown artifact class %s" % side.get("artifactClass"))
    pair = frozenset({left.get("artifactClass"), right.get("artifactClass")})
    allowed = GATE_PAIRS[gate_id]
    pair_ok = pair in allowed if gate_id == "ASSESSMENT_ALIGNMENT" else pair == allowed
    diffs = compare(left, right, dimensions or GATE_DIMENSIONS[gate_id])
    findings = []
    fails = not pair_ok
    if not pair_ok:
        findings.append({
            "severity": "HIGH",
            "code": "artifact_class",
            "message": "this gate does not compare %s" % ", ".join(sorted(pair)),
        })
    for diff in diffs:
        decision = _severity_for(diff)
        findings.append({
            "severity": decision["severity"],
            "code": diff["dimension"],
            "message": "%s differs at %s (%s)" % (diff["dimension"], diff["anchor"], diff["kind"]),
        })
        fails = fails or decision["failsGate"]
    anchors = sorted(set(left.get("anchors") or {}) | set(right.get("anchors") or {}))
    data = {
        "evidenceId": "cross-%s" % gate_id.lower(),
        "gateId": gate_id,
        "auditorRole": auditor_role,
        "performed": bool(anchors),
        "expectedInputs": ["%s:%s" % (left.get("artifactClass"), left.get("label")),
                           "%s:%s" % (right.get("artifactClass"), right.get("label"))],
        "observedInputs": ["%s:%s" % (left.get("artifactClass"), left.get("label")),
                           "%s:%s" % (right.get("artifactClass"), right.get("label"))] if anchors else [],
        "thingBeingCertified": "candidate-%s:%s" % (right.get("artifactClass"), identity.candidateHash),
        "independentEvidenceSource": "compared-%s:%s" % (left.get("artifactClass"), left.get("contentHash") or "none"),
        "findings": findings,
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": bool(anchors),
            "detectorException": False,
            "requiredInputsPresent": bool(anchors),
            "missingRender": False,
            "missingEvidence": not bool(anchors),
            "stale": False,
            "gateSpecificFailure": fails,
            "unavailableEvidence": False,
        },
        "inventory": [{
            "name": "anchors",
            "expected": len(anchors) if anchors else 0,
            "observed": len(anchors) if anchors else 0,
        }],
    }
    if not anchors:
        data["expectedInputs"] = []
        data["observedInputs"] = []
    return seal(data, identity)
