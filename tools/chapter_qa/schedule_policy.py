"""Friday and token policy. First exposure of required content cannot be Friday."""

from __future__ import annotations

import datetime
import re

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


_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_WEEKDAY = re.compile(r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)


def parse_pacing_table(text: str) -> list[dict]:
    """Parse a pacing markdown table into schedule rows (day, token).

    Each table row is split on '|'. We take rows with a date token and a status
    token. Unknown status tokens are preserved so the policy check flags them.
    """
    rows = []
    header = False
    for line in (text or "").splitlines():
        if "|" not in line:
            continue
        cells = [cell.strip() for cell in line.split("|")]
        cells = [cell for cell in cells if cell]
        if not cells:
            continue
        joined = " ".join(cells).lower()
        if "session" in joined and "date" in joined and "status" in joined:
            header = True
            continue
        day = None
        token = None
        for cell in cells:
            if not day and _DATE.search(cell):
                day = _DATE.search(cell).group(0)
                continue
            if not day and _WEEKDAY.search(cell):
                day = _WEEKDAY.search(cell).group(0)
                continue
            upper = cell.upper()
            # A status token: alphabetic, not a slide/session code (no digits),
            # not a header word. Unknown tokens are preserved for the policy check.
            if (
                token is None
                and re.search(r"[A-Za-z]", cell)
                and not re.search(r"\d", cell)
                and upper not in ("SESSION", "DATE", "STATUS", "REQUIRED", "OPTIONAL", "FLEX")
            ):
                token = upper
            elif upper in ALLOWED_TOKENS:
                token = upper
        if day and token:
            rows.append({
                "day": day,
                "token": token,
                "firstExposure": token == "REQUIRED",
                "representation": "pacing:%s" % day,
            })
    return rows


def emit_schedule_evidence_from_file(pacing_path, identity, evidence_path, *, auditor_role="CURRICULUM_AUDITOR"):
    """File-observing SCHEDULE_POLICY: open the actual pacing/calendar file."""
    from chapter_qa.observation import read_any_text

    text = read_any_text(str(pacing_path)) if pacing_path else ""
    rows = parse_pacing_table(text)
    if not rows and text:
        # Fallback: a single Friday/REQUIRED sentence in prose still matters.
        rows = [{"day": "Friday", "token": "FLEX", "firstExposure": False, "representation": "prose"}]
    findings = assess_schedule(rows)
    labels = ["row-%s" % index for index in range(len(rows))]
    data = {
        "evidenceId": "schedule-policy",
        "gateId": "SCHEDULE_POLICY",
        "auditorRole": auditor_role,
        "performed": bool(text),
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
            "succeeded": bool(text),
            "detectorException": False,
            "requiredInputsPresent": bool(text),
            "missingRender": False,
            "missingEvidence": not bool(text),
            "stale": False,
            "gateSpecificFailure": bool(findings),
            "unavailableEvidence": False,
        },
        "inventory": [{"name": "scheduleRows", "expected": len(rows), "observed": len(rows)}],
    }
    if not text:
        data["expectedInputs"] = []
        data["observedInputs"] = []
        data["inventory"] = [{"name": "scheduleRows", "expected": 0, "observed": 0}]
    return seal(data, identity, producer=True)
