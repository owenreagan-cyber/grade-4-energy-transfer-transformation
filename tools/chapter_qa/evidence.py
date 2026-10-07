"""Evidence contract and the single gate-status evaluator.

Claimed status cannot upgrade a result. PASS is computed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from chapter_qa.completeness import InventoryCount, assess_completeness
from chapter_qa.identity import BuildIdentity, identity_mismatch_codes
from chapter_qa.roles import ROLES, is_builder

SCHEMA_VERSION = "1.0"
REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_STATUSES = ("PASS", "FAIL", "NOT_VERIFIED")
FINDING_SEVERITIES = ("BLOCKING", "HIGH", "MEDIUM", "LOW", "INFO")
ISO_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

# Each tuple is one self-validation family. Different spellings are not distinct evidence.
SELF_EVIDENCE_FAMILIES = (
    ("source-model", "source model"),
    ("ledger",),
    ("working-tree-golden", "working tree golden", "mutable-golden", "mutable golden"),
    ("newly-generated-freeze", "newly generated freeze"),
)

REQUIRED_FIELDS = (
    "schemaVersion",
    "evidenceId",
    "gateId",
    "gateVersion",
    "buildId",
    "candidatePath",
    "candidateHash",
    "auditorRole",
    "status",
    "performed",
    "mandatory",
    "releaseBlocking",
    "startedAt",
    "completedAt",
    "expectedInputs",
    "observedInputs",
    "inputHashes",
    "toolVersions",
    "thingBeingCertified",
    "independentEvidenceSource",
    "findings",
    "evidencePaths",
    "sourceFreezeId",
    "sourceHash",
    "candidateFreezeId",
    "failureReason",
    "notVerifiedReason",
    "invalidationReasons",
    "execution",
    "inventory",
)

EXECUTION_FIELDS = (
    "succeeded",
    "detectorException",
    "requiredInputsPresent",
    "missingRender",
    "missingEvidence",
    "stale",
    "gateSpecificFailure",
    "unavailableEvidence",
)

# Identity and staleness failures are rejections: the record cannot be accepted.
REJECTION_CODES = frozenset({
    "SCHEMA",
    "BUILD_MISMATCH",
    "IDENTITY_MISMATCH",
    "HASH_MISMATCH",
    "STALE",
    "SELF_EVIDENCE",
    "BUILDER_ONLY",
    "ROLE_MISMATCH",
    "GATE_VERSION_MISMATCH",
})


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str

    def to_dict(self) -> dict:
        return {"severity": self.severity, "code": self.code, "message": self.message}


@dataclass(frozen=True)
class ExecutionFacts:
    succeeded: bool
    detectorException: bool
    requiredInputsPresent: bool
    missingRender: bool
    missingEvidence: bool
    stale: bool
    gateSpecificFailure: bool
    unavailableEvidence: bool

    def to_dict(self) -> dict:
        return {
            "succeeded": self.succeeded,
            "detectorException": self.detectorException,
            "requiredInputsPresent": self.requiredInputsPresent,
            "missingRender": self.missingRender,
            "missingEvidence": self.missingEvidence,
            "stale": self.stale,
            "gateSpecificFailure": self.gateSpecificFailure,
            "unavailableEvidence": self.unavailableEvidence,
        }


@dataclass(frozen=True)
class EvidenceRecord:
    schemaVersion: str
    evidenceId: str
    gateId: str
    gateVersion: str
    buildId: str
    candidatePath: str
    candidateHash: str
    auditorRole: str
    status: str
    performed: bool
    mandatory: bool
    releaseBlocking: bool
    startedAt: str
    completedAt: str
    expectedInputs: tuple
    observedInputs: tuple
    inputHashes: dict
    toolVersions: dict
    thingBeingCertified: str
    independentEvidenceSource: str
    findings: tuple
    evidencePaths: tuple
    sourceFreezeId: str
    sourceHash: str
    candidateFreezeId: str
    failureReason: str | None
    notVerifiedReason: str | None
    invalidationReasons: tuple
    execution: ExecutionFacts
    inventory: tuple

    def to_dict(self) -> dict:
        return {
            "schemaVersion": self.schemaVersion,
            "evidenceId": self.evidenceId,
            "gateId": self.gateId,
            "gateVersion": self.gateVersion,
            "buildId": self.buildId,
            "candidatePath": self.candidatePath,
            "candidateHash": self.candidateHash,
            "auditorRole": self.auditorRole,
            "status": self.status,
            "performed": self.performed,
            "mandatory": self.mandatory,
            "releaseBlocking": self.releaseBlocking,
            "startedAt": self.startedAt,
            "completedAt": self.completedAt,
            "expectedInputs": list(self.expectedInputs),
            "observedInputs": list(self.observedInputs),
            "inputHashes": dict(self.inputHashes),
            "toolVersions": dict(self.toolVersions),
            "thingBeingCertified": self.thingBeingCertified,
            "independentEvidenceSource": self.independentEvidenceSource,
            "findings": [f.to_dict() for f in self.findings],
            "evidencePaths": list(self.evidencePaths),
            "sourceFreezeId": self.sourceFreezeId,
            "sourceHash": self.sourceHash,
            "candidateFreezeId": self.candidateFreezeId,
            "failureReason": self.failureReason,
            "notVerifiedReason": self.notVerifiedReason,
            "invalidationReasons": list(self.invalidationReasons),
            "execution": self.execution.to_dict(),
            "inventory": [item.to_dict() for item in self.inventory],
        }


@dataclass(frozen=True)
class Evaluation:
    status: str
    reasons: tuple
    codes: frozenset

    @property
    def accepted(self) -> bool:
        return not (self.codes & REJECTION_CODES)


def _is_bool(value) -> bool:
    return isinstance(value, bool)


def _normalize_label(text: str) -> str:
    return " ".join(text.lower().replace("_", " ").replace("-", " ").split())


def _evidence_family(text: str) -> str | None:
    normalized = _normalize_label(text)
    for family in SELF_EVIDENCE_FAMILIES:
        for token in family:
            if _normalize_label(token) in normalized:
                return family[0]
    return None


def is_self_evidence(thing: str, independent: str) -> bool:
    """True when the cited source is not materially distinct from the thing certified.

    Labels in the same family are the same evidence, including a source model
    compared with another source model and a working-tree golden compared with
    a mutable golden. A hash written into the label does not make them distinct.
    """
    left = (thing or "").strip()
    right = (independent or "").strip()
    if not left or not right or _normalize_label(left) == _normalize_label(right):
        return True
    left_family = _evidence_family(left)
    right_family = _evidence_family(right)
    if left_family and left_family == right_family:
        return True
    return False


def missing_evidence_paths(paths, root: Path | None = None) -> bool:
    """True when a performed gate did not cite a real file inside the repo."""
    if not paths:
        return True
    base = root or REPO_ROOT
    for rel in paths:
        text = str(rel).strip()
        path = Path(text)
        if not text or path.is_absolute() or ".." in path.parts:
            return True
        if not (base / path).is_file():
            return True
    return False


def validate_evidence_dict(data: dict) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return ["evidence must be an object"]
    unknown = set(data) - set(REQUIRED_FIELDS)
    if unknown:
        errors.append("unknown %s" % ",".join(sorted(unknown)))
    for key in REQUIRED_FIELDS:
        if key not in data:
            errors.append("missing %s" % key)
    if errors:
        return errors
    if data["schemaVersion"] != SCHEMA_VERSION:
        errors.append("schemaVersion")
    if not isinstance(data["evidenceId"], str) or not data["evidenceId"].strip():
        errors.append("evidenceId")
    if data["status"] not in GATE_STATUSES:
        errors.append("status")
    if not _is_bool(data["performed"]):
        errors.append("performed")
    if not _is_bool(data["mandatory"]) or not _is_bool(data["releaseBlocking"]):
        errors.append("gate flags")
    if data["auditorRole"] not in ROLES:
        errors.append("auditorRole")
    if not ISO_TIME.match(data["startedAt"] or "") or not ISO_TIME.match(data["completedAt"] or ""):
        errors.append("timestamps")
    if not isinstance(data["expectedInputs"], list) or not isinstance(data["observedInputs"], list):
        errors.append("inputs")
    if not isinstance(data["inputHashes"], dict) or not isinstance(data["toolVersions"], dict):
        errors.append("hashes")
    else:
        hashes_blank = (
            not isinstance(data.get("candidateHash"), str)
            or not data["candidateHash"].strip()
            or not isinstance(data.get("sourceHash"), str)
            or not data["sourceHash"].strip()
            or not data["inputHashes"]
        )
        if hashes_blank:
            errors.append("empty hash")
        for key, value in data["inputHashes"].items():
            if not str(key).strip() or not isinstance(value, str) or not value.strip():
                errors.append("empty hash")
                break
    execution_keys = data.get("execution")
    if isinstance(execution_keys, dict) and set(execution_keys) - set(EXECUTION_FIELDS):
        errors.append("unknown execution")
    if not isinstance(data["invalidationReasons"], list):
        errors.append("invalidationReasons")
    if not isinstance(data["evidencePaths"], list):
        errors.append("evidencePaths")
    if not isinstance(data["findings"], list):
        errors.append("findings")
    else:
        for finding in data["findings"]:
            if not isinstance(finding, dict) or finding.get("severity") not in FINDING_SEVERITIES:
                errors.append("finding severity")
                break
            if not finding.get("code") or not finding.get("message"):
                errors.append("finding")
                break
    execution = data["execution"]
    if not isinstance(execution, dict):
        errors.append("execution")
    else:
        for key in EXECUTION_FIELDS:
            if key not in execution or not _is_bool(execution[key]):
                errors.append("execution.%s" % key)
                break
    if not isinstance(data["inventory"], list):
        errors.append("inventory")
    else:
        for item in data["inventory"]:
            if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item.get("name", "").strip():
                errors.append("inventory item")
                break
            for count_key in ("expected", "observed"):
                value = item.get(count_key)
                if value is not None and (isinstance(value, bool) or not isinstance(value, int)):
                    errors.append("inventory count")
                    break
            if "explicitEmptyAllowed" in item and not isinstance(item["explicitEmptyAllowed"], bool):
                errors.append("explicitEmptyAllowed")
                break
    if data["failureReason"] is not None and not isinstance(data["failureReason"], str):
        errors.append("failureReason")
    if data["notVerifiedReason"] is not None and not isinstance(data["notVerifiedReason"], str):
        errors.append("notVerifiedReason")
    for key in ("thingBeingCertified", "independentEvidenceSource", "buildId", "candidatePath",
                "candidateHash", "sourceHash", "sourceFreezeId", "candidateFreezeId", "gateId", "gateVersion"):
        if not isinstance(data[key], str):
            errors.append(key)
    return errors


def evidence_from_dict(data: dict) -> EvidenceRecord:
    errors = validate_evidence_dict(data)
    if errors:
        raise ValueError("invalid evidence: %s" % ", ".join(errors))
    execution = data["execution"]
    inventory = tuple(
        InventoryCount(
            name=item["name"],
            expected=item.get("expected"),
            observed=item.get("observed"),
            explicitEmptyAllowed=bool(item.get("explicitEmptyAllowed", False)),
        )
        for item in data["inventory"]
    )
    findings = tuple(
        Finding(severity=item["severity"], code=item["code"], message=item["message"])
        for item in data["findings"]
    )
    return EvidenceRecord(
        schemaVersion=data["schemaVersion"],
        evidenceId=data["evidenceId"],
        gateId=data["gateId"],
        gateVersion=data["gateVersion"],
        buildId=data["buildId"],
        candidatePath=data["candidatePath"],
        candidateHash=data["candidateHash"],
        auditorRole=data["auditorRole"],
        status=data["status"],
        performed=data["performed"],
        mandatory=data["mandatory"],
        releaseBlocking=data["releaseBlocking"],
        startedAt=data["startedAt"],
        completedAt=data["completedAt"],
        expectedInputs=tuple(data["expectedInputs"]),
        observedInputs=tuple(data["observedInputs"]),
        inputHashes=dict(data["inputHashes"]),
        toolVersions=dict(data["toolVersions"]),
        thingBeingCertified=data["thingBeingCertified"],
        independentEvidenceSource=data["independentEvidenceSource"],
        findings=findings,
        evidencePaths=tuple(data["evidencePaths"]),
        sourceFreezeId=data["sourceFreezeId"],
        sourceHash=data["sourceHash"],
        candidateFreezeId=data["candidateFreezeId"],
        failureReason=data["failureReason"],
        notVerifiedReason=data["notVerifiedReason"],
        invalidationReasons=tuple(data["invalidationReasons"]),
        execution=ExecutionFacts(
            succeeded=execution["succeeded"],
            detectorException=execution["detectorException"],
            requiredInputsPresent=execution["requiredInputsPresent"],
            missingRender=execution["missingRender"],
            missingEvidence=execution["missingEvidence"],
            stale=execution["stale"],
            gateSpecificFailure=execution["gateSpecificFailure"],
            unavailableEvidence=execution["unavailableEvidence"],
        ),
        inventory=inventory,
    )


def _add(codes: list, reasons: list, code: str, reason: str) -> None:
    if code not in codes:
        codes.append(code)
    reasons.append(reason)


def evaluate(evidence: EvidenceRecord, gate, requested: BuildIdentity) -> Evaluation:
    """Authoritative gate status for one evidence record.

    The record's claimed `status` is ignored. PASS is returned only when every
    contract condition holds.
    """
    codes: list[str] = []
    reasons: list[str] = []
    execution = evidence.execution

    if evidence.schemaVersion != SCHEMA_VERSION:
        _add(codes, reasons, "SCHEMA", "schemaVersion is not %s" % SCHEMA_VERSION)
    if evidence.gateVersion != gate.gateVersion or evidence.gateId != gate.gateId:
        _add(codes, reasons, "GATE_VERSION_MISMATCH", "gate id or version does not match the definition")
    if evidence.auditorRole != gate.expectedEvidenceRole:
        _add(codes, reasons, "ROLE_MISMATCH", "auditor role does not match expectedEvidenceRole")
    if gate.mandatory:
        from chapter_qa.registry import expected_producer

        spec = expected_producer(evidence.gateId)
        recorded = evidence.toolVersions.get("producer")
        recorded_version = evidence.toolVersions.get("producerVersion")
        if spec is None or recorded != spec["id"] or recorded_version != spec["version"]:
            _add(codes, reasons, "PRODUCER_UNREGISTERED", "mandatory evidence has no registered producer")
    # Independence applies to a performed result. An explicit unavailable
    # record has no evidence source to compare.
    if evidence.performed:
        if gate.requiresIndependentEvidence and is_builder(evidence.auditorRole):
            _add(codes, reasons, "BUILDER_ONLY", "builder evidence cannot satisfy an independent gate")
        if gate.requiresIndependentEvidence and is_self_evidence(
            evidence.thingBeingCertified, evidence.independentEvidenceSource
        ):
            _add(codes, reasons, "SELF_EVIDENCE", "independent evidence source is not distinct")

    for code in identity_mismatch_codes(evidence, requested):
        _add(codes, reasons, code, code)

    if execution.stale or evidence.invalidationReasons:
        _add(codes, reasons, "STALE", "evidence is stale")

    hard = False
    if evidence.performed and execution.unavailableEvidence:
        _add(codes, reasons, "CONTRADICTION", "performed evidence cannot also be unavailable")
        hard = True
    if execution.detectorException:
        _add(codes, reasons, "DETECTOR_EXCEPTION", "detector exception")
        hard = True
    if not execution.requiredInputsPresent:
        _add(codes, reasons, "MISSING_INPUT", "missing required input")
        hard = True
    if execution.missingRender:
        _add(codes, reasons, "MISSING_RENDER", "missing render")
        hard = True
    if execution.missingEvidence:
        _add(codes, reasons, "MISSING_EVIDENCE", "missing evidence")
        hard = True
    if evidence.performed and missing_evidence_paths(evidence.evidencePaths):
        _add(codes, reasons, "MISSING_EVIDENCE", "cited evidence path is missing")
        hard = True
    if evidence.performed and not execution.succeeded:
        _add(codes, reasons, "EXECUTION_FAILED", "execution failed")
        hard = True
    if execution.gateSpecificFailure:
        _add(codes, reasons, "GATE_SPECIFIC_FAILURE", "gate-specific failure")
        hard = True
    if any(item.severity == "BLOCKING" for item in evidence.findings):
        _add(codes, reasons, "BLOCKING_FINDING", "BLOCKING finding")
        hard = True

    if evidence.performed:
        for code in assess_completeness(
            evidence.expectedInputs, evidence.observedInputs, evidence.inventory
        ):
            _add(codes, reasons, code, code)
            hard = True
    elif not evidence.performed:
        _add(codes, reasons, "NOT_PERFORMED", "gate was not performed")

    unavailable = (
        gate.allowedNotVerified
        and bool(evidence.notVerifiedReason)
        and execution.unavailableEvidence
        and not evidence.performed
        and not hard
        and not (set(codes) & REJECTION_CODES)
    )
    if unavailable:
        return Evaluation("NOT_VERIFIED", tuple(reasons), frozenset(codes))

    if codes:
        return Evaluation("FAIL", tuple(reasons), frozenset(codes))

    # Zero findings is acceptable only because execution and completeness already passed.
    return Evaluation("PASS", tuple(), frozenset())
