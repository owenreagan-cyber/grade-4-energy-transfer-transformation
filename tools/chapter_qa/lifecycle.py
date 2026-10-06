"""Release lifecycle. State is not a gate status."""

from __future__ import annotations

STATES = (
    "BUILD_IN_PROGRESS",
    "BUILT_UNCERTIFIED",
    "INTERNAL_AUDIT_PENDING",
    "INTERNAL_AUDIT_FAILED",
    "INTERNALLY_CERTIFIED",
    "EXTERNAL_AUDIT_PENDING",
    "EXTERNAL_AUDIT_REJECTED",
    "APPROVED_FOR_FREEZE",
    "FROZEN",
)

# Legal edges only. FROZEN has no outbound edge in this factory.
_EDGES = {
    "BUILD_IN_PROGRESS": frozenset({"BUILT_UNCERTIFIED"}),
    "BUILT_UNCERTIFIED": frozenset({"INTERNAL_AUDIT_PENDING", "BUILD_IN_PROGRESS"}),
    "INTERNAL_AUDIT_PENDING": frozenset({"INTERNALLY_CERTIFIED", "INTERNAL_AUDIT_FAILED"}),
    "INTERNAL_AUDIT_FAILED": frozenset({"BUILD_IN_PROGRESS"}),
    "INTERNALLY_CERTIFIED": frozenset({"EXTERNAL_AUDIT_PENDING"}),
    "EXTERNAL_AUDIT_PENDING": frozenset({"APPROVED_FOR_FREEZE", "EXTERNAL_AUDIT_REJECTED"}),
    "EXTERNAL_AUDIT_REJECTED": frozenset({"BUILD_IN_PROGRESS"}),
    "APPROVED_FOR_FREEZE": frozenset({"FROZEN"}),
    "FROZEN": frozenset(),
}

FROZEN_CHAPTERS = {
    1: {
        "version": "1.1",
        "status": "FROZEN",
        "constant": "UNIT1_CH1_GOLD_STANDARD_VERSION",
    },
    2: {
        "version": "1.0",
        "status": "FROZEN",
        "constant": "UNIT1_CH2_GOLD_STANDARD_VERSION",
        "freezeCommit": "a491193ddf74598910247385a2f55a4458b8b55c",
        "postFreezeArmCommit": "785e3e699b688adcf536e25f87bf896c2b38eae3",
    },
}


def legal_transition(source: str, target: str) -> bool:
    if source not in _EDGES or target not in STATES:
        return False
    if source == target:
        return False
    return target in _EDGES[source]


def transition_to_frozen_allowed(source: str) -> bool:
    return legal_transition(source, "FROZEN")


def compare_frozen_bytes(expected: dict, observed: dict) -> list[str]:
    """Return keys whose freeze hashes differ.

    An empty expected or observed map is a mismatch. Matching empty strings
    are not a clean comparison.
    """
    if not expected or not observed:
        return ["EMPTY_IDENTITY"]
    mismatched = []
    for key in sorted(set(expected) | set(observed)):
        left = str(expected.get(key) or "").strip()
        right = str(observed.get(key) or "").strip()
        if not left or not right or left != right:
            mismatched.append(key)
    return mismatched


def frozen_classroom_change_permitted(chapter: int, owner_authorized: bool) -> bool:
    """True only when the owner explicitly authorizes reopening a frozen chapter."""
    if chapter not in FROZEN_CHAPTERS:
        raise KeyError("chapter %s is not in the frozen registry" % chapter)
    return owner_authorized is True
