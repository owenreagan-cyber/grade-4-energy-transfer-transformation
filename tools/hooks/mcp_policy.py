"""MCP role policy. No server is contacted.

A design tool's own state cannot satisfy an independent gate.
Release Judge cannot call a write-capable server or fetch missing evidence.
Tool failure cannot become PASS.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from hooks.decisions import allow, deny

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


def _server_key(name: str) -> str:
    text = (name or "").strip().lower()
    if "figma" in text:
        return "figma"
    if "canva" in text:
        return "canva"
    if "github" in text:
        return "github"
    return text


def _writes(tool_name: str) -> bool:
    text = (tool_name or "").lower()
    return any(token in text for token in ("use_figma", "create", "update", "delete", "generate", "upload", "write"))


def decide_mcp(payload) -> dict:
    """beforeMCPExecution decision. Unknown servers and roles fail closed."""
    if not isinstance(payload, dict):
        return deny("malformed hook input")
    server = _server_key(str(payload.get("mcp_server_name") or payload.get("server") or ""))
    tool = str(payload.get("tool_name") or "")
    role = str(payload.get("role") or payload.get("auditorRole") or "UNSPECIFIED")
    if not server or not authorize_mcp(role, server):
        return deny("%s cannot call %s" % (role, server or "unknown server"))
    if _writes(tool) and not role_may_call(role, SERVERS[server]):
        return deny("%s cannot write through %s" % (role, server))
    if role == "RELEASE_JUDGE":
        return deny("release judge cannot call an MCP")
    return allow("%s may call %s" % (role, tool or server))


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="MCP execution policy. Does not call a server.")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.apply:
        sys.stdout.write(json.dumps(deny("hook activation does not grant MCP writes")))
        return 2
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        result = decide_mcp(payload)
    except Exception:
        result = deny("MCP policy failed closed")
    sys.stdout.write(json.dumps(result))
    return 2 if result["decision"] == "DENY" else 0


if __name__ == "__main__":
    raise SystemExit(main())
