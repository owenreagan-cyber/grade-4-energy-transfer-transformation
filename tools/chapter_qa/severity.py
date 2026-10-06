"""Finding severity. Context can raise a default when instructional content is lost."""

from __future__ import annotations

import json
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parents[2] / "qa" / "gold-standard" / "severity_policy.json"


def load_severity_policy(path: Path | None = None) -> dict:
    return json.loads((path or POLICY_PATH).read_text(encoding="utf-8"))["findings"]


def resolve_severity(code: str, context: dict | None = None, policy: dict | None = None) -> dict:
    """Return severity and whether the central evaluator should fail the gate.

    The auditor records this fact. It does not assign PASS.
    """
    rules = policy if policy is not None else load_severity_policy()
    if code not in rules:
        return {"severity": "BLOCKING", "failsGate": True}
    rule = dict(rules[code])
    context = context or {}
    if context.get("lost_instructional_content") and rule.get("lostInstructionalContent"):
        rule["severity"] = rule["lostInstructionalContent"]
        rule["failsGate"] = True
    if context.get("before_freeze") is False and code == "stale_human_status":
        rule = dict(rule)
        rule["failsGate"] = True
    return {"severity": rule["severity"], "failsGate": bool(rule.get("failsGate"))}
