"""Shared hook decisions.

ALLOW, DENY, and WARN are the only outcomes. A certification path that
cannot decide denies. These helpers do not evaluate evidence.
"""

from __future__ import annotations

ALLOW = "ALLOW"
DENY = "DENY"
WARN = "WARN"


def decide(kind: str, reason: str, **extra) -> dict:
    if kind not in (ALLOW, DENY, WARN):
        kind = DENY
        reason = "unknown decision forced closed"
    permission = {ALLOW: "allow", DENY: "deny", WARN: "allow"}[kind]
    payload = {
        "decision": kind,
        "permission": permission,
        "reason": reason,
        "agent_message": reason,
    }
    payload.update(extra)
    return payload


def allow(reason: str, **extra) -> dict:
    return decide(ALLOW, reason, **extra)


def deny(reason: str, **extra) -> dict:
    return decide(DENY, reason, **extra)


def warn(reason: str, **extra) -> dict:
    return decide(WARN, reason, **extra)
