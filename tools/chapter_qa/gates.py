"""Gate-definition contract. Chapter expectations are not hard-coded here."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from chapter_qa.roles import ROLES

ROOT = Path(__file__).resolve().parents[2]
GATES_PATH = ROOT / "qa" / "gold-standard" / "gates.json"

REQUIRED_GATE_FIELDS = (
    "gateId",
    "gateVersion",
    "mandatory",
    "releaseBlocking",
    "requiresIndependentEvidence",
    "allowedNotVerified",
    "expectedEvidenceRole",
    "dependencies",
    "applicability",
)


@dataclass(frozen=True)
class GateDefinition:
    gateId: str
    gateVersion: str
    mandatory: bool
    releaseBlocking: bool
    requiresIndependentEvidence: bool
    allowedNotVerified: bool
    expectedEvidenceRole: str
    dependencies: tuple
    applicability: str

    def to_dict(self) -> dict:
        return {
            "gateId": self.gateId,
            "gateVersion": self.gateVersion,
            "mandatory": self.mandatory,
            "releaseBlocking": self.releaseBlocking,
            "requiresIndependentEvidence": self.requiresIndependentEvidence,
            "allowedNotVerified": self.allowedNotVerified,
            "expectedEvidenceRole": self.expectedEvidenceRole,
            "dependencies": list(self.dependencies),
            "applicability": self.applicability,
        }


def validate_gate_dict(data: dict, known_ids: set[str] | None = None) -> list[str]:
    errors = []
    for key in REQUIRED_GATE_FIELDS:
        if key not in data:
            errors.append("missing %s" % key)
    if errors:
        return errors
    if data["expectedEvidenceRole"] not in ROLES:
        errors.append("expectedEvidenceRole")
    if data["applicability"] not in ("always", "when_configured"):
        errors.append("applicability")
    for flag in ("mandatory", "releaseBlocking", "requiresIndependentEvidence", "allowedNotVerified"):
        if not isinstance(data[flag], bool):
            errors.append(flag)
    if not isinstance(data["dependencies"], list):
        errors.append("dependencies")
    elif known_ids is not None:
        for dep in data["dependencies"]:
            if dep not in known_ids:
                errors.append("unknown dependency %s" % dep)
            if dep == data["gateId"]:
                errors.append("self dependency")
    return errors


def load_gates(path: Path | None = None) -> tuple[GateDefinition, ...]:
    payload = json.loads((path or GATES_PATH).read_text(encoding="utf-8"))
    rows = payload["gates"]
    ids = {row["gateId"] for row in rows}
    if len(ids) != len(rows):
        raise ValueError("duplicate gateId")
    gates = []
    for row in rows:
        errors = validate_gate_dict(row, ids)
        if errors:
            raise ValueError("%s: %s" % (row.get("gateId"), ", ".join(errors)))
        gates.append(
            GateDefinition(
                gateId=row["gateId"],
                gateVersion=row["gateVersion"],
                mandatory=row["mandatory"],
                releaseBlocking=row["releaseBlocking"],
                requiresIndependentEvidence=row["requiresIndependentEvidence"],
                allowedNotVerified=row["allowedNotVerified"],
                expectedEvidenceRole=row["expectedEvidenceRole"],
                dependencies=tuple(row["dependencies"]),
                applicability=row["applicability"],
            )
        )
    return tuple(gates)


def default_release_gates(gates: tuple[GateDefinition, ...] | None = None) -> tuple[GateDefinition, ...]:
    """Gates that apply to every chapter. when_configured gates stay out until a chapter enables them."""
    chosen = gates if gates is not None else load_gates()
    return tuple(gate for gate in chosen if gate.applicability == "always")


def gate_by_id(gates, gate_id: str) -> GateDefinition:
    for gate in gates:
        if gate.gateId == gate_id:
            return gate
    raise KeyError(gate_id)
