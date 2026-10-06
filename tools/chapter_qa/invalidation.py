"""Evidence invalidation and downstream propagation.

A change marks the gates that read the changed artifact, then their dependents.
Unrelated gates stay valid.
"""

from __future__ import annotations

INVALIDATION_REASONS = (
    "SOURCE_CHANGED",
    "CANDIDATE_CHANGED",
    "FREEZE_CHANGED",
    "EXPECTED_INVENTORY_CHANGED",
    "AUDITOR_VERSION_CHANGED",
    "GATE_VERSION_CHANGED",
    "TOOL_VERSION_CHANGED",
    "DEPENDENCY_CHANGED",
)

# Artifact class -> gates that directly read it. Not a chapter inventory.
DIRECT_GATES = {
    "authoritative-source": ("SOURCE_AUTHORITY",),
    "notes": ("NOTES_STRUCTURE",),
    "slides": ("SLIDES_STRUCTURE",),
    "assessment": ("ASSESSMENT_ALIGNMENT",),
    "schedule": ("SCHEDULE_POLICY",),
    "playbook": ("PLAYBOOK_ALIGNMENT",),
    "release": ("FRESH_EXPORT", "RELEASE_EXACT_SET", "RELEASE_PARITY"),
    "inventory": ("INVENTORY",),
    "freeze": ("PRIOR_FROZEN_NONREGRESSION", "POST_FREEZE_GOLDEN"),
}


def dependents(gate_id: str, gates) -> set[str]:
    """Transitive gates that list gate_id, or a downstream gate, as a dependency."""
    found = set()
    stack = [gate_id]
    by_dep = {}
    for gate in gates:
        for dep in gate.dependencies:
            by_dep.setdefault(dep, set()).add(gate.gateId)
    while stack:
        current = stack.pop()
        for child in by_dep.get(current, ()):
            if child not in found:
                found.add(child)
                stack.append(child)
    return found


def propagate(artifact: str, reason: str, gates) -> dict[str, str]:
    """Map gateId -> invalidation reason.

    The direct gates receive `reason`. Dependents receive DEPENDENCY_CHANGED.
    Gates that do not read the artifact, and are not downstream of one that does,
    are omitted.
    """
    if reason not in INVALIDATION_REASONS:
        raise ValueError("unknown invalidation reason %s" % reason)
    if artifact not in DIRECT_GATES:
        raise KeyError(artifact)
    affected = {}
    for gate_id in DIRECT_GATES[artifact]:
        affected[gate_id] = reason
        for child in dependents(gate_id, gates):
            affected.setdefault(child, "DEPENDENCY_CHANGED")
    return affected


def tool_versions_changed(recorded: dict, current: dict) -> bool:
    return dict(recorded) != dict(current)


def expected_inventory_changed(recorded: dict, current: dict) -> bool:
    return dict(recorded) != dict(current)


def reasons_for_evidence(evidence, affected: dict[str, str]) -> list[str]:
    reason = affected.get(evidence.gateId)
    if reason is None:
        return []
    return [reason]
