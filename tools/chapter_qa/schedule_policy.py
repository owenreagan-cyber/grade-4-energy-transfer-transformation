"""Friday and token policy. First exposure of required content cannot be Friday."""

from __future__ import annotations

import datetime

from chapter_qa.emit import seal

ALLOWED_TOKENS = {"REQUIRED", "OPTIONAL", "FLEX"}


def _is_friday(value: str) -> bool:
    text = (value or "").strip()
    if text.lower() == "friday":
        return True
    if "T" in text:
        text = text.split("T", 1)[0]
    try:
        return datetime.date.fromisoformat(text).weekday() == 4
    except ValueError:
        return False


def assess_schedule(rows: list[dict]) -> list[dict]:
    findings = []
    for row in rows:
        token = (row.get("token") or "").strip().upper()
        if token and token not in ALLOWED_TOKENS:
            findings.append({"severity": "HIGH", "code": "unknown_token", "message": "unknown token %s" % token})
        first = row.get("firstExposure") is True
        negated = row.get("negated") is True
        day = row.get("day") or ""
        if first and negated:
            findings.append({"severity": "BLOCKING", "code": "friday_first_exposure", "message": "negation cannot hide a first exposure"})
        if negated and not first:
            continue
        if first and _is_friday(day):
            findings.append({
                "severity": "BLOCKING",
                "code": "friday_first_exposure",
                "message": "required first exposure is on Friday via %s" % (row.get("representation") or day),
            })
    return findings


def emit_schedule_evidence(rows, identity, evidence_path, *, auditor_role="CURRICULUM_AUDITOR"):
    findings = assess_schedule(rows)
    labels = ["row-%s" % index for index in range(len(rows))]
    data = {
        "evidenceId": "schedule-policy",
        "gateId": "SCHEDULE_POLICY",
        "auditorRole": auditor_role,
        "performed": bool(rows),
        "expectedInputs": labels,
        "observedInputs": [] if findings or not rows else labels,
        "thingBeingCertified": "candidate-schedule:%s" % identity.candidateHash,
        "independentEvidenceSource": "calendar-policy:%s" % identity.sourceHash,
        "findings": findings,
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": bool(rows),
            "detectorException": False,
            "requiredInputsPresent": bool(rows),
            "missingRender": False,
            "missingEvidence": not bool(rows),
            "stale": False,
            "gateSpecificFailure": bool(findings),
            "unavailableEvidence": False,
        },
        "inventory": [{"name": "scheduleRows", "expected": len(rows), "observed": len(rows)}],
    }
    if not rows:
        data["expectedInputs"] = []
        data["observedInputs"] = []
        data["inventory"] = [{"name": "scheduleRows", "expected": 0, "observed": 0}]
    return seal(data, identity, producer=True)
