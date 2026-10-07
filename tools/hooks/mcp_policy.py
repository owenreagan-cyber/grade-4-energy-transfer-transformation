"""MCP role policy. No server is contacted.

A design tool's own state cannot satisfy an independent gate.
Release Judge cannot call a write-capable server or fetch missing evidence.
Tool failure cannot become PASS.
"""

from __future__ import annotations

CLASSES = (
    "READ_ONLY_SOURCE",
    "READ_ONLY_REVIEW",
    "DESIGN_WRITE",
    "REPOSITORY_WRITE",
    "EXTERNAL_ACTION",
)

# Agent or auditor role -> MCP classes it may call once a server is configured.
ALLOWED = {
    "SOURCE_SCHOLAR": frozenset({"READ_ONLY_SOURCE", "READ_ONLY_REVIEW"}),
    "CURRICULUM_AUDITOR": frozenset({"READ_ONLY_SOURCE"}),
    "VISUAL_ART_DIRECTOR": frozenset({"DESIGN_WRITE"}),
    "VISUAL_QA_AUDITOR": frozenset({"READ_ONLY_REVIEW"}),
    "QA_ADVERSARY": frozenset({"READ_ONLY_REVIEW"}),
    "RELEASE_JUDGE": frozenset(),
    "BUILDER": frozenset(),
    "CROSS_ARTIFACT_AUDITOR": frozenset(),
    "PDF_OOXML_FORENSICS": frozenset(),
    "PROVENANCE_AUDITOR": frozenset({"READ_ONLY_REVIEW"}),
}

WRITE_CLASSES = frozenset({"DESIGN_WRITE", "REPOSITORY_WRITE", "EXTERNAL_ACTION"})

# Server name is the authority. A caller-supplied class cannot relabel it.
# GitHub is deferred. It is intentionally absent, so no role can call it yet.
SERVERS = {
    "figma": "DESIGN_WRITE",
    "canva": "DESIGN_WRITE",
}


def authorize_mcp(role: str, server_name: str, claimed_class: str | None = None) -> bool:
    """Allow a call only when the registered class permits it.

    A claimed class that disagrees with the registry is a mismatch and is denied.
    """
    actual = SERVERS.get(str(server_name or "").strip().lower())
    if actual is None:
        return False
    if claimed_class is not None and claimed_class != actual:
        return False
    return role_may_call(role, actual)


def role_may_call(role: str, server_class: str) -> bool:
    if server_class not in CLASSES:
        return False
    return server_class in ALLOWED.get(role, frozenset())


def may_satisfy_independent_gate(role: str, server_class: str) -> bool:
    """MCP output is an input at most. It is never the independent gate result."""
    del role, server_class
    return False


def local_verification_required(server_class: str) -> bool:
    return server_class in CLASSES


def failure_cannot_pass(server_class: str) -> bool:
    """True when a missing or failed MCP call is forbidden from becoming PASS."""
    return server_class in CLASSES


def builder_expected_is_authority(role: str) -> bool:
    """Curriculum audit does not treat a builder's expected answer as the source."""
    if role == "CURRICULUM_AUDITOR":
        return False
    return False


def judge_may_fetch_missing_evidence(role: str) -> bool:
    if role == "RELEASE_JUDGE":
        return False
    return False


def same_design_state_may_certify(producer_role: str, auditor_role: str) -> bool:
    """Visual QA cannot certify from the design file that produced the asset."""
    if producer_role == "VISUAL_ART_DIRECTOR" and auditor_role == "VISUAL_QA_AUDITOR":
        return False
    return False
