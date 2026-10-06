"""Source and curriculum evidence.

SOURCE_DERIVED cites Reader/TG text. APPROVED_DERIVED cites an approved
decision that is not the Reader. UNRESOLVED has neither. Agreement of a
candidate with itself is not source authority.
"""

from __future__ import annotations

import re

from chapter_qa.emit import seal
from chapter_qa.severity import resolve_severity

DERIVATIONS = ("SOURCE_DERIVED", "APPROVED_DERIVED", "UNRESOLVED")
SOURCE_GATES = ("SOURCE_AUTHORITY", "CURRICULUM_CORRECTNESS")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def derivation(claim: dict) -> str:
    source_id = (claim.get("sourceId") or "").strip()
    candidate_id = (claim.get("candidateId") or "").strip()
    if source_id and candidate_id and source_id == candidate_id:
        return "UNRESOLVED"
    source_text = _norm(claim.get("sourceText") or "")
    candidate_text = _norm(claim.get("candidateText") or "")
    approved = _norm(claim.get("approvedText") or "")
    if source_text and candidate_text and candidate_text == source_text:
        return "SOURCE_DERIVED"
    if approved and candidate_text and candidate_text == approved:
        return "APPROVED_DERIVED"
    return "UNRESOLVED"


def _finding(code: str, message: str, context: dict | None = None) -> tuple[dict, bool]:
    decision = resolve_severity(code, context)
    return (
        {"severity": decision["severity"], "code": code, "message": message},
        decision["failsGate"],
    )


def audit_claims(claims: list[dict], gate_id: str) -> dict:
    if gate_id not in SOURCE_GATES:
        raise ValueError("%s is not a source or curriculum gate" % gate_id)
    findings = []
    fails = False
    rows = []
    if not claims:
        finding, fail = _finding("missing_release_artifact", "no source claims were supplied")
        findings.append(finding)
        fails = fails or fail
    for claim in claims:
        kind = derivation(claim)
        rows.append({
            "claimId": claim.get("claimId"),
            "kind": claim.get("kind"),
            "derivation": kind,
            "sourceLocation": claim.get("sourceLocation"),
            "sourceId": claim.get("sourceId"),
        })
        same_bytes = (claim.get("sourceId") or "") and claim.get("sourceId") == claim.get("candidateId")
        if same_bytes:
            finding, fail = _finding(
                "generated_agreement",
                "claim %s cites the candidate as its own source" % claim.get("claimId"),
            )
            findings.append(finding)
            fails = fails or fail
            continue
        if claim.get("kind") == "exclusion":
            banned = _norm(claim.get("sourceText") or "")
            if banned and banned in _norm(claim.get("candidateText") or ""):
                finding, fail = _finding(
                    "unsupported_addition",
                    "excluded text appears in claim %s" % claim.get("claimId"),
                    {"lost_instructional_content": True},
                )
                findings.append(finding)
                fails = fails or fail
            continue
    positive = [
        claim for claim in claims
        if claim.get("kind") != "exclusion" and derivation(claim) in ("SOURCE_DERIVED", "APPROVED_DERIVED")
    ]
    sourced = [claim for claim in positive if derivation(claim) == "SOURCE_DERIVED"]
    if gate_id == "SOURCE_AUTHORITY" and not sourced:
        finding, fail = _finding("unsupported_addition", "no claim is derived from Reader/TG text")
        findings.append(finding)
        fails = fails or fail
    if gate_id == "CURRICULUM_CORRECTNESS" and not positive:
        finding, fail = _finding("unsupported_addition", "no claim is derived from a source or an approved decision")
        findings.append(finding)
        fails = fails or fail
    for claim in claims:
        if claim.get("kind") == "exclusion":
            continue
        kind = derivation(claim)
        if gate_id == "SOURCE_AUTHORITY" and kind != "SOURCE_DERIVED":
            finding, fail = _finding(
                "unsupported_addition",
                "claim %s is %s and cannot establish source authority" % (claim.get("claimId"), kind),
            )
            findings.append(finding)
            fails = fails or fail
        elif gate_id == "CURRICULUM_CORRECTNESS" and kind == "UNRESOLVED":
            finding, fail = _finding(
                "unsupported_addition",
                "claim %s is unresolved against Reader/TG and approved decisions" % claim.get("claimId"),
            )
            findings.append(finding)
            fails = fails or fail
        if kind == "SOURCE_DERIVED" and not (claim.get("sourceLocation") or "").strip():
            finding, fail = _finding(
                "unsupported_addition",
                "claim %s has no source location" % claim.get("claimId"),
            )
            findings.append(finding)
            fails = fails or fail
    return {"rows": rows, "findings": findings, "failsGate": fails}


def emit_source_evidence(claims, identity, gate_id, evidence_path: str, *, auditor_role=None) -> tuple[dict, object]:
    """Build a source or curriculum evidence record and let evaluate() set status."""
    observed = audit_claims(claims, gate_id)
    inputs = [row["claimId"] for row in observed["rows"] if row.get("claimId")]
    if not inputs:
        inputs = []
    data = {
        "evidenceId": "src-%s" % gate_id.lower(),
        "gateId": gate_id,
        "auditorRole": auditor_role,
        "performed": True,
        "expectedInputs": inputs or ["source-claims"],
        "observedInputs": inputs,
        "thingBeingCertified": "candidate-curriculum:%s" % identity.candidateHash,
        "independentEvidenceSource": "authoritative-reader-tg:%s" % identity.sourceHash,
        "findings": observed["findings"],
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": True,
            "detectorException": False,
            "requiredInputsPresent": bool(claims),
            "missingRender": False,
            "missingEvidence": not bool(claims),
            "stale": False,
            "gateSpecificFailure": observed["failsGate"],
            "unavailableEvidence": False,
        },
        "inventory": [{
            "name": "sourceClaims",
            "expected": len(claims),
            "observed": len(observed["rows"]),
        }],
    }
    if not claims:
        data["expectedInputs"] = []
        data["observedInputs"] = []
        data["inventory"] = [{"name": "sourceClaims", "expected": 0, "observed": 0}]
    return seal(data, identity)
