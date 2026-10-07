"""Redact secret-shaped text before it is written to an inventory or report.

Environment-variable names are kept. Values assigned to token-like keys
are replaced. This module does not read or write MCP configuration.
"""

from __future__ import annotations

import re

_ASSIGNED = re.compile(
    r"(?i)\b(api[\s_-]*key|token|secret|password|authorization|access[\s_-]*key)\b(\s*[:=]\s*)(\"[^\"]*\"|'[^']*'|[^\n]+)"
)
_GITHUB = re.compile(r"github_pat_[A-Za-z0-9_]+|gh[opurs]_[A-Za-z0-9_]+")
_SK = re.compile(r"\bsk-[A-Za-z0-9_\-]{8,}\b")
_BEARER = re.compile(r"(?i)\bBearer\s+(\"[^\"]*\"|'[^']*'|\S+)")
_AWS = re.compile(r"\bAKIA[A-Z0-9]{16}\b")
_SLACK = re.compile(r"\bxox[baprs]-[A-Za-z0-9-]+\b")
_JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+\b")


def redact(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("redact expects text")

    def _assigned(match: re.Match) -> str:
        value = match.group(3)
        bare = value.strip("\"'")
        if bare.startswith("${") and bare.endswith("}"):
            return match.group(0)
        return match.group(1) + match.group(2) + "[REDACTED]"

    cleaned = _BEARER.sub("Bearer [REDACTED]", text)
    cleaned = _ASSIGNED.sub(_assigned, cleaned)
    cleaned = _GITHUB.sub("[REDACTED]", cleaned)
    cleaned = _SK.sub("[REDACTED]", cleaned)
    cleaned = _AWS.sub("[REDACTED]", cleaned)
    cleaned = _SLACK.sub("[REDACTED]", cleaned)
    cleaned = _JWT.sub("[REDACTED]", cleaned)
    return cleaned
