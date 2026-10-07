"""Dry-run git protection.

Decides whether a shell command may run. It never executes git.
Destructive git is denied. Commit and push are denied unless the
payload carries the matching boolean authorization. Read-only git
and unrelated commands are allowed.

This module is not registered in `.cursor/hooks.json`.
"""

from __future__ import annotations

import json
import re
import shlex
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from hooks.decisions import allow, deny

SAFE_FRONT = frozenset({"echo", "printf"})

READ_ONLY = frozenset({
    "status",
    "diff",
    "log",
    "rev-parse",
    "show",
    "blame",
    "describe",
    "rev-list",
    "ls-files",
    "ls-tree",
    "cat-file",
    "grep",
    "shortlog",
    "name-rev",
    "merge-base",
})

ALWAYS_DENY = frozenset({
    "reset",
    "clean",
    "stash",
    "restore",
    "checkout",
    "switch",
    "rebase",
    "merge",
    "pull",
    "am",
    "cherry-pick",
    "revert",
    "filter-branch",
    "filter-repo",
})

WRAPPERS = frozenset({"sudo", "command", "exec", "env", "nice", "time", "nohup"})
SHELLS = frozenset({"bash", "sh", "zsh", "dash"})
INTERPRETERS = frozenset({"python", "python3", "python3.14", "perl", "ruby", "node"})
GIT_GLOBALS = frozenset({
    "-p",
    "--paginate",
    "--no-pager",
    "--bare",
    "--literal-pathspecs",
    "--glob-pathspecs",
    "--noglob-pathspecs",
    "--icase-pathspecs",
})
GIT_GLOBALS_WITH_VALUE = frozenset({
    "-C",
    "-c",
    "--git-dir",
    "--work-tree",
    "--namespace",
    "--super-prefix",
    "--exec-path",
})

_GIT_CALL = re.compile(
    r"""(?ix)
    \bgit\b
    (?:\s+(?:-[A-Za-z]|--[A-Za-z0-9-]+)(?:[= ]\S+)?){0,8}
    \s+
    (?P<verb>reset|clean|stash|restore|checkout|switch|rebase|merge|pull|push|commit|filter-branch|filter-repo|am|cherry-pick|revert)
    \b
    """
)


def _split_commands(text: str) -> list[str]:
    """Split a shell command on &&, ||, ;, |, &, and newlines. Quotes are kept."""
    parts: list[str] = []
    buf: list[str] = []
    quote = None
    i = 0
    while i < len(text):
        char = text[i]
        if quote:
            buf.append(char)
            if char == quote:
                quote = None
            i += 1
            continue
        if char in "'\"":
            quote = char
            buf.append(char)
            i += 1
            continue
        if text.startswith("&&", i) or text.startswith("||", i):
            parts.append("".join(buf))
            buf = []
            i += 2
            continue
        if char in ";|&\n":
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(char)
        i += 1
    if quote:
        raise ValueError("unbalanced quotes")
    parts.append("".join(buf))
    return [part.strip() for part in parts if part.strip()]


_DANGEROUS_ENV = (
    "GIT_EXTERNAL_DIFF",
    "GIT_PAGER",
    "GIT_EDITOR",
    "GIT_SEQUENCE_EDITOR",
    "GIT_SSH",
    "GIT_SSH_COMMAND",
    "GIT_EXEC_PATH",
)
_DANGEROUS_CONFIG = (
    "alias.",
    "diff.external",
    "difftool.",
    "mergetool.",
    "protocol.",
    "core.pager",
    "core.editor",
    "core.sshcommand",
    "sequence.editor",
    "credential.helper",
    "gpg.program",
)
_OBFUSCATED = re.compile(
    r"""(?ix)(b64decode|base64\.(?:b64|decod)|\\[0-7]{3}|\\x[0-9a-fA-F]{2}|fromhex|['\"]git['\"]\s*\+|git['\"]\s*\+)"""
)
_EXEC_API = re.compile(r"(?i)\b(system|popen|exec\w*|subprocess|spawn|child_process|eval|Function)\b")


def _env_is_dangerous(name: str) -> bool:
    upper = name.upper()
    return upper in _DANGEROUS_ENV or upper.startswith("GIT_")


def _config_is_dangerous(value: str) -> bool:
    key = value.split("=", 1)[0].strip().lower()
    return any(key == item or key.startswith(item) for item in _DANGEROUS_CONFIG)


def _is_git_name(name: str) -> bool:
    base = name.lower()
    return base == "git" or (base.startswith("git.") and base != "github")


def _peel(argv: list[str]) -> tuple[list[str], list[str]]:
    env_names: list[str] = []
    while argv:
        name = Path(argv[0]).name
        if name in WRAPPERS:
            argv = argv[1:]
            while argv and argv[0].startswith("-"):
                flag = argv.pop(0)
                if flag in ("-u", "-i", "-C") and argv:
                    argv.pop(0)
            continue
        if "=" in argv[0] and not argv[0].startswith("-"):
            env_names.append(argv[0].split("=", 1)[0])
            argv = argv[1:]
            continue
        break
    return argv, env_names


def _shell_script(argv: list[str]) -> str | None:
    index = 1
    while index < len(argv):
        token = argv[index]
        if token == "-c":
            return argv[index + 1] if index + 1 < len(argv) else ""
        if token.startswith("-") and not token.startswith("--") and "c" in token[1:]:
            return argv[index + 1] if index + 1 < len(argv) else ""
        if token == "--":
            return None
        index += 1
    return None


def _git_invocation(argv: list[str], authorization: dict) -> dict | None:
    """Return a decision for a git argv, or None when argv is not git."""
    if not argv or not _is_git_name(Path(argv[0]).name):
        return None
    index = 1
    while index < len(argv):
        token = argv[index]
        if token == "--":
            return deny("git option separator hides the subcommand")
        if token in GIT_GLOBALS:
            index += 1
            continue
        if token == "-c" or (token.startswith("-c") and not token.startswith("--")):
            return deny("git config overrides are not authorized")
        if token in GIT_GLOBALS_WITH_VALUE:
            index += 2
            continue
        if token in ("--git-dir", "--work-tree", "--config-env") or token.startswith("--git-dir=") or token.startswith("--work-tree=") or token.startswith("--config-env="):
            return deny("git repository override is not authorized")
        if token.startswith("-"):
            index += 1
            continue
        if token == "stash":
            sub = argv[index + 1] if index + 1 < len(argv) else ""
            if sub in ("list", "show"):
                return None
            return deny("destructive git command stash is not authorized")
        return _classify_verb(token, authorization)
    return deny("git invocation has no subcommand")


def _verbs_in_script(script: str) -> list[str]:
    folded = script.replace('"', " ").replace("'", " ").replace("`", " ")
    return [match.group("verb").lower() for match in _GIT_CALL.finditer(folded)]


def _classify_verb(verb: str | None, authorization: dict) -> dict | None:
    if verb is None:
        return None
    if verb == "":
        return deny("git invocation has no subcommand")
    if verb in ALWAYS_DENY:
        return deny("destructive git command %s is not authorized" % verb)
    if verb == "push":
        if authorization.get("ownerAuthorizesPush") is True:
            return None
        return deny("git push requires owner authorization")
    if verb == "commit":
        if authorization.get("workflowAuthorizesCommit") is True:
            return None
        return deny("git commit requires workflow authorization")
    if verb in READ_ONLY:
        return None
    return deny("git command %s is not in the read-only allow list" % verb)


def _active_substitutions(segment: str) -> list[str]:
    """Return command substitutions that the shell would execute."""
    found = []
    buf: list[str] = []
    quote = None
    i = 0
    while i < len(segment):
        char = segment[i]
        if quote == "'":
            if char == "'":
                quote = None
            i += 1
            continue
        if quote == '"':
            if char == '"':
                quote = None
                i += 1
                continue
        elif char in "'\"":
            quote = char
            i += 1
            continue
        if segment.startswith("$(", i):
            depth = 1
            i += 2
            start = i
            while i < len(segment) and depth:
                if segment[i] == "(":
                    depth += 1
                elif segment[i] == ")":
                    depth -= 1
                i += 1
            found.append(segment[start:i - 1] if depth == 0 else segment[start:])
            continue
        if char == "`":
            i += 1
            start = i
            while i < len(segment) and segment[i] != "`":
                i += 1
            found.append(segment[start:i])
            i += 1
            continue
        buf.append(char)
        i += 1
    return found


def _read_script(token: str) -> str | None:
    if not token or token.startswith("-") or token.startswith("/") or ".." in Path(token).parts:
        return None
    path = Path(token)
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def _script_token(argv: list[str]) -> str | None:
    for token in argv[1:]:
        if not token.startswith("-"):
            return token
    return None


def _code_without_strings(script: str) -> str:
    return re.sub(
        r"'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\"|'(?:\\.|[^'])*'|\"(?:\\.|[^\"])*\"",
        " ",
        script,
    )


def _inline_decision(script: str, authorization: dict, depth: int) -> dict | None:
    if _OBFUSCATED.search(script):
        return deny("obfuscated command is not authorized")
    for inner in _active_substitutions(script):
        if _OBFUSCATED.search(inner):
            return deny("obfuscated command is not authorized")
        found = _walk(inner, authorization, depth + 1)
        if found is not None:
            return found
    if _EXEC_API.search(_code_without_strings(script)):
        return deny("interpreter execution api is not authorized")
    return None


def _file_decision(name: str, token: str, authorization: dict, depth: int) -> dict | None:
    body = _read_script(token)
    if body is None:
        return deny("script body is unavailable")
    if name in SHELLS or name in {"source", "."}:
        return _walk(body, authorization, depth + 1)
    return _inline_decision(body, authorization, depth)


def _strip_comments(text: str) -> str:
    out: list[str] = []
    quote = None
    index = 0
    while index < len(text):
        char = text[index]
        if quote:
            out.append(char)
            if char == quote:
                quote = None
            index += 1
            continue
        if char in "'\"":
            quote = char
            out.append(char)
            index += 1
            continue
        if char == "#":
            while index < len(text) and text[index] != "\n":
                index += 1
            continue
        out.append(char)
        index += 1
    return "".join(out)


def _has_process_sub(segment: str) -> bool:
    quote = None
    index = 0
    while index < len(segment):
        char = segment[index]
        if quote == "'":
            if char == "'":
                quote = None
            index += 1
            continue
        if char in "'\"":
            quote = char
            index += 1
            continue
        if segment.startswith("<(", index) or segment.startswith(">(", index) or segment.startswith("=(", index):
            return True
        index += 1
    return False


def _walk(command: str, authorization: dict, depth: int) -> dict | None:
    if depth > 4:
        return deny("shell nesting is too deep to classify")
    try:
        segments = _split_commands(command)
    except ValueError:
        return deny("malformed shell command")
    env_changed = False
    for segment in segments:
        try:
            argv, env_names = _peel(shlex.split(segment, posix=True))
        except ValueError:
            return deny("malformed shell command")
        if any(_env_is_dangerous(name) for name in env_names):
            return deny("git environment can execute a program")
        if not argv:
            continue
        if Path(argv[0]).name in {"export", "declare", "typeset", "alias"}:
            env_changed = True
            continue
        if env_changed and (_is_git_name(Path(argv[0]).name) or "git" in segment.lower()):
            return deny("environment changes before git are not authorized")
        if _has_process_sub(segment):
            return deny("process substitution is not authorized")
        name = Path(argv[0]).name
        for inner in _active_substitutions(segment):
            if _OBFUSCATED.search(inner):
                return deny("obfuscated command is not authorized")
            found = _walk(inner, authorization, depth + 1)
            if found is not None:
                return found
        if name in SHELLS:
            script = _shell_script(argv)
            if script is not None:
                if _active_substitutions(script) or _has_process_sub(script):
                    return deny("command substitution in a shell script is not authorized")
                found = _inline_decision(script, authorization, depth)
                if found is not None:
                    return found
                found = _walk(script, authorization, depth + 1)
                if found is not None:
                    return found
                continue
            token = _script_token(argv)
            if token is None:
                continue
            return _file_decision(name, token, authorization, depth)
        inline = None
        if name in INTERPRETERS and ("-c" in argv or "-e" in argv):
            flag = "-c" if "-c" in argv else "-e"
            code_at = argv.index(flag)
            inline = argv[code_at + 1] if code_at + 1 < len(argv) else ""
            found = _inline_decision(inline, authorization, depth)
            if found is not None:
                return found
            continue
        if name in INTERPRETERS and "-m" not in argv:
            token = _script_token(argv)
            if token is not None:
                return _file_decision(name, token, authorization, depth)
        if name in {"eval", "source", "."}:
            token = _script_token(argv)
            if token and not token.startswith("-") and Path(token).suffix in {".sh", ".bash", ".zsh"}:
                return _file_decision(name, token, authorization, depth)
            found = _walk(" ".join(shlex.quote(token) for token in argv[1:]), authorization, depth + 1)
            if found is not None:
                return found
            continue
        if name not in SAFE_FRONT and not _is_git_name(name):
            for verb in _verbs_in_script(segment):
                found = _classify_verb(verb, authorization)
                if found is not None:
                    return found
        found = _git_invocation(argv, authorization)
        if found is not None:
            return found
    return None


def decide_git(command, authorization=None) -> dict:
    """Return ALLOW or DENY for one shell command. Never runs the command."""
    if not isinstance(command, str) or not command.strip():
        return deny("malformed hook input")
    command = _strip_comments(command.replace("\\\r\n", " ").replace("\\\n", " "))
    authorization = authorization if isinstance(authorization, dict) else {}
    found = _walk(command, authorization, 0)
    if found is not None:
        return found
    return allow("command is read-only git or unrelated to git")


def decide_payload(payload) -> dict:
    if not isinstance(payload, dict):
        return deny("malformed hook input")
    command = payload.get("command")
    authorization = payload.get("authorization") if isinstance(payload.get("authorization"), dict) else {}
    return decide_git(command, authorization)


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Dry-run git protection. Does not execute git.")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.apply:
        sys.stdout.write(json.dumps(deny("hook activation is refused; dry-run only")))
        return 2
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        result = decide_payload(payload)
    except Exception:
        result = deny("git protection failed closed")
    sys.stdout.write(json.dumps(result))
    return 2 if result["decision"] == "DENY" else 0


if __name__ == "__main__":
    raise SystemExit(main())
