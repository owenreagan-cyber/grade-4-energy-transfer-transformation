"""Evidence workspace. Visual QA output stays out of production directories."""

from __future__ import annotations

from pathlib import Path

WORK_DIRS = ("evidence", "renders", "crops", "logs", "reports")
PROTECTED_PREFIXES = ("production", "curriculum", "assets/authoritative")


def workspace_for(build_id: str, base: Path) -> Path:
    if not build_id or build_id.strip() != build_id:
        raise ValueError("build id is required")
    if any(part in build_id for part in ("/", "\\", "..")):
        raise ValueError("build id cannot contain a path")
    root = Path(base) / build_id
    for name in WORK_DIRS:
        (root / name).mkdir(parents=True, exist_ok=True)
    return root


def assert_output_allowed(path: Path, repo_root: Path) -> None:
    """Refuse to write render or evidence output over classroom artifacts."""
    resolved = Path(path).resolve()
    repo = Path(repo_root).resolve()
    try:
        relative = resolved.relative_to(repo).as_posix()
    except ValueError:
        return
    for prefix in PROTECTED_PREFIXES:
        if relative == prefix or relative.startswith(prefix + "/"):
            raise ValueError("refusing to write under %s" % prefix)


def safe_cleanup(path: Path, repo_root: Path) -> None:
    """Delete a directory only when it is inside qa/work and is not qa/work itself."""
    resolved = Path(path).resolve()
    work = (Path(repo_root).resolve() / "qa" / "work").resolve()
    if resolved == work or work not in resolved.parents:
        raise ValueError("cleanup is limited to a subdirectory of qa/work")
    import shutil
    shutil.rmtree(resolved)
