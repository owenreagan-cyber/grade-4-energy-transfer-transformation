"""Release Judge. Evidence in, PASS or FAIL out.

This module does not edit, build, regenerate, repair, or freeze anything.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from chapter_qa.evidence import evaluate, seal_valid
from chapter_qa.identity import BuildIdentity, REPO_ROOT, recompute_mismatches
from chapter_qa.invalidation import reasons_for_evidence

_OTHER_BUILD = frozenset({"BUILD_MISMATCH", "IDENTITY_MISMATCH", "HASH_MISMATCH"})

JUDGE_STATUSES = ("PASS", "FAIL")
CERTIFICATION_PASS = "INTERNAL RELEASE CERTIFICATION: PASS"
CERTIFICATION_FAIL = "INTERNAL RELEASE CERTIFICATION: FAIL"


@dataclass(frozen=True)
class ReleaseJudgment:
    buildId: str
    status: str
    requiredGateCount: int
    passedGateCount: int
    failedGateCount: int
    notVerifiedGateCount: int
    missingGateCount: int
    blockingReasons: tuple
    acceptedEvidenceIds: tuple
    rejectedEvidenceIds: tuple

    def to_dict(self) -> dict:
        return {
            "buildId": self.buildId,
            "status": self.status,
            "requiredGateCount": self.requiredGateCount,
            "passedGateCount": self.passedGateCount,
            "failedGateCount": self.failedGateCount,
            "notVerifiedGateCount": self.notVerifiedGateCount,
            "missingGateCount": self.missingGateCount,
            "blockingReasons": list(self.blockingReasons),
            "acceptedEvidenceIds": list(self.acceptedEvidenceIds),
            "rejectedEvidenceIds": list(self.rejectedEvidenceIds),
        }

    @property
    def certification(self) -> str:
        if self.status == "PASS":
            return CERTIFICATION_PASS
        return CERTIFICATION_FAIL


def judge(gates, evidence_records, requested: BuildIdentity, affected=None, *, root: Path | None = None) -> ReleaseJudgment:
    """Decide release certification for one build.

    Gate definitions are authoritative for mandatory and releaseBlocking.
    Flags stored on an evidence record cannot hide a mandatory gate.

    `affected` is the map from `invalidation.propagate`. When a gate is in
    that map, its evidence is stale even if the record was not stamped.

    The Judge recomputes current classroom-file hashes from disk (`root`) and
    re-verifies every evidence seal. Caller-supplied current values are not
    trusted; a committed mutation still fails because the bytes differ.
    """
    affected = affected or {}
    accepted_ids = []
    rejected_ids = []
    blocking = []
    if not gates:
        blocking.append("NO_GATES")

    base = root or REPO_ROOT
    for mismatch in recompute_mismatches(requested, base):
        blocking.append("CANDIDATE_BYTES_MISMATCH: %s" % mismatch)

    accepted_by_gate = {gate.gateId: [] for gate in gates}
    evaluations = {}

    for evidence in evidence_records:
        gate = next((item for item in gates if item.gateId == evidence.gateId), None)
        if gate is None:
            rejected_ids.append(evidence.evidenceId)
            continue
        if not seal_valid(evidence):
            rejected_ids.append(evidence.evidenceId)
            blocking.append("SEAL_MISMATCH: %s" % evidence.gateId)
            continue
        extra = reasons_for_evidence(evidence, affected)
        if extra:
            stamped = tuple(dict.fromkeys((*evidence.invalidationReasons, *extra)))
            evidence = replace(evidence, invalidationReasons=stamped)
        result = evaluate(evidence, gate, requested)
        evaluations[evidence.evidenceId] = result
        if not result.accepted:
            rejected_ids.append(evidence.evidenceId)
            same_build = not (result.codes & _OTHER_BUILD)
            if same_build and any(item.severity == "BLOCKING" for item in evidence.findings):
                blocking.append("BLOCKING_FINDING: %s" % evidence.gateId)
            continue
        accepted_ids.append(evidence.evidenceId)
        accepted_by_gate[evidence.gateId].append(evidence)

    passed = failed = not_verified = missing = 0
    required = 0

    for gate in gates:
        rows = accepted_by_gate[gate.gateId]
        if gate.mandatory or gate.releaseBlocking:
            required += 1
        if not rows:
            missing += 1
            if gate.mandatory or gate.releaseBlocking:
                blocking.append("MISSING_GATE: %s" % gate.gateId)
            continue

        statuses = [evaluations[row.evidenceId].status for row in rows]
        if any(
            finding.severity == "BLOCKING"
            for row in rows
            for finding in row.findings
        ):
            status = "FAIL"
            blocking.append("BLOCKING_FINDING: %s" % gate.gateId)
        elif "PASS" in statuses and "FAIL" not in statuses:
            status = "PASS"
        elif "FAIL" in statuses:
            status = "FAIL"
        else:
            status = "NOT_VERIFIED"

        if status == "PASS":
            passed += 1
            if gate.requiresIndependentEvidence and all(row.auditorRole == "BUILDER" for row in rows):
                blocking.append("BUILDER_ONLY: %s" % gate.gateId)
        elif status == "FAIL":
            failed += 1
            if gate.mandatory or gate.releaseBlocking:
                blocking.append("GATE_FAIL: %s" % gate.gateId)
        else:
            not_verified += 1
            if gate.mandatory or gate.releaseBlocking:
                blocking.append("NOT_VERIFIED: %s" % gate.gateId)

    status = "PASS" if not blocking else "FAIL"
    if status not in JUDGE_STATUSES:
        status = "FAIL"
        blocking.append("JUDGE_STATUS")
    return ReleaseJudgment(
        buildId=requested.buildId,
        status=status,
        requiredGateCount=required,
        passedGateCount=passed,
        failedGateCount=failed,
        notVerifiedGateCount=not_verified,
        missingGateCount=missing,
        blockingReasons=tuple(blocking),
        acceptedEvidenceIds=tuple(accepted_ids),
        rejectedEvidenceIds=tuple(rejected_ids),
    )
