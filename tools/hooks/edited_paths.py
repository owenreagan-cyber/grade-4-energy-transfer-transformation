"""Edited paths from the Cursor event and from git.

A caller-supplied editedPaths list is not the source of truth. An empty
list does not hide a file that the event or git can see.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

_EVENT_KEYS = ("file_path", "filePath", "path")
_EVENT_LISTS = ("paths", "file_paths", "filePaths", "edited_files", "editedFiles")


def _run_git(root: Path, args: list[str]) -> tuple[list[str], str | None]:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [], "git unavailable: %s" % type(exc).__name__
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "git failed").strip().splitlines()
        return [], detail[0] if detail else "git failed"
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()], None


def git_changed_paths(root: Path) -> tuple[list[str], str | None]:
    """Tracked edits versus HEAD, plus untracked files git does not ignore."""
    if not root.is_dir():
        return [], "workspace root is not a directory"
    probe, error = _run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if error or probe != ["true"]:
        return [], error or "not a git worktree"
    changed, error = _run_git(root, ["diff", "--name-only", "HEAD"])
    if error:
        return [], error
    staged, staged_error = _run_git(root, ["diff", "--cached", "--name-only"])
    if staged_error:
        return [], staged_error
    untracked, untracked_error = _run_git(root, ["ls-files", "--others", "--exclude-standard"])
    if untracked_error:
        return [], untracked_error
    return _unique([*changed, *staged, *untracked]), None


def _unique(items: list[str]) -> list[str]:
    seen = []
    for item in items:
        text = str(item).replace("\\", "/").strip()
        if text and text not in seen:
            seen.append(text)
    return seen


def _relativize(path: str, roots: list[Path]) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        return path.replace("\\", "/").lstrip("./")
    resolved = candidate.resolve()
    for root in roots:
        try:
            return str(resolved.relative_to(root.resolve())).replace("\\", "/")
        except ValueError:
            continue
    text = str(resolved).replace("\\", "/")
    for marker in ("production/", "curriculum/", "qa/gold-standard/", "tools/", "docs/"):
        at = text.find("/" + marker)
        if at >= 0:
            return text[at + 1:]
    return text


def event_paths(payload: dict, roots: list[Path]) -> list[str]:
    """Paths Cursor put on the event. editedPaths is intentionally ignored."""
    found = []
    for key in _EVENT_KEYS:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            found.append(_relativize(value, roots))
    for key in _EVENT_LISTS:
        value = payload.get(key)
        if isinstance(value, list):
            found.extend(_relativize(item, roots) for item in value if isinstance(item, str))
    edits = payload.get("edits")
    if isinstance(edits, list):
        for edit in edits:
            if isinstance(edit, dict) and isinstance(edit.get("file_path"), str):
                found.append(_relativize(edit["file_path"], roots))
    return _unique(found)


def workspace_roots(payload: dict, default: Path) -> list[Path]:
    raw = payload.get("workspace_roots")
    if isinstance(raw, list) and raw:
        return [Path(item) for item in raw if isinstance(item, str) and item.strip()]
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        return [Path(cwd)]
    return [default]


def resolve_edited_paths(payload: dict, default_root: Path) -> dict:
    """Merge the event file list with git. Never let an empty claim hide either."""
    if not isinstance(payload, dict):
        return {"paths": [], "error": "malformed payload", "source": "none", "callerHidEdits": False}
    roots = workspace_roots(payload, default_root)
    git_paths: list[str] = []
    error = None
    for root in roots:
        names, git_error = git_changed_paths(root)
        if git_error:
            error = git_error
        git_paths.extend(names)
    observed = _unique([*event_paths(payload, roots), *git_paths])
    claimed = payload.get("editedPaths")
    hidden = isinstance(claimed, list) and len(claimed) == 0 and len(observed) > 0
    source = "event+git" if event_paths(payload, roots) and git_paths else (
        "event" if event_paths(payload, roots) else "git" if git_paths else "clean"
    )
    return {
        "paths": observed,
        "error": error,
        "source": source,
        "callerHidEdits": hidden,
    }
