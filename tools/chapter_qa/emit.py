"""Turn auditor observations into a Phase A evidence record.

The status written on the record is the central evaluator's status.
A caller-supplied PASS is discarded before evaluation.
"""

from __future__ import annotations

from datetime import datetime, timezone

from chapter_qa.evidence import evaluate, evidence_from_dict
from chapter_qa.gates import gate_by_id, load_gates
from chapter_qa.roles import ROLES

SCHEMA_VERSION = "1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def seal(data: dict, identity, gate=None, *, producer: bool = False) -> tuple[dict, object]:
    """Evaluate one observation. The returned status comes from evaluate()."""
    payload = dict(data)
    if gate is None:
        gate = gate_by_id(load_gates(), payload["gateId"])
    payload["schemaVersion"] = SCHEMA_VERSION
    payload["gateId"] = gate.gateId
    payload["gateVersion"] = gate.gateVersion
    payload["mandatory"] = gate.mandatory
    payload["releaseBlocking"] = gate.releaseBlocking
    payload["auditorRole"] = payload.get("auditorRole") if payload.get("auditorRole") in ROLES else "BUILDER"
    payload["status"] = "FAIL"
    payload["buildId"] = identity.buildId
    payload["candidatePath"] = identity.candidatePath
    payload["candidateHash"] = identity.candidateHash
    payload["candidateFreezeId"] = identity.candidateFreezeId
    payload["sourceFreezeId"] = identity.sourceFreezeId
    payload["sourceHash"] = identity.sourceHash
    payload["inputHashes"] = dict(identity.inputHashes)
    payload.setdefault("startedAt", utc_now())
    payload.setdefault("completedAt", utc_now())
    payload.setdefault("toolVersions", {})
    if producer:
        from chapter_qa.registry import expected_producer, stamp

        if expected_producer(gate.gateId if gate is not None else payload["gateId"]):
            stamp(payload, gate.gateId if gate is not None else payload["gateId"])
    payload.setdefault("invalidationReasons", [])
    payload.setdefault("notVerifiedReason", None)
    payload.setdefault("failureReason", None)
    record = evidence_from_dict(payload)
    result = evaluate(record, gate, identity)
    stored = record.to_dict()
    stored["status"] = result.status
    if result.status == "FAIL":
        stored["failureReason"] = "; ".join(result.reasons) or payload.get("failureReason")
    elif result.status == "NOT_VERIFIED":
        stored["failureReason"] = None
    else:
        stored["failureReason"] = None
    return stored, result
