"""Producer provenance: traceable, tracked, clean source verified against git.

A release-certifying producer must exist in git, be tracked, be clean, and match
its recorded source hash. The Judge recomputes these from disk; it never trusts
evidence-file metadata alone.

Provenance is stamped into ``toolVersions`` (covered by the evidence seal) and
verified by the Judge by recomputing the current producer source from disk.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

from chapter_qa.identity import REPO_ROOT

# Producer id "module:function" -> repo-relative source path.
# Both "chapter_qa.x" and "qa_x" live under tools/.


def producer_source_path(producer_id: str) -> str:
    module = (producer_id or "").split(":", 1)[0]
    if not module:
        return ""
    return "tools/" + module.replace(".", "/") + ".py"


def sha256_file(path: Path) -> str:
    if not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(args: list[str], root: Path = REPO_ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(root), capture_output=True, text=True, check=False,
    )


def git_head(root: Path = REPO_ROOT) -> str:
    completed = _git(["rev-parse", "HEAD"], root)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def git_blob(relpath: str, root: Path = REPO_ROOT) -> str:
    completed = _git(["rev-parse", "HEAD:" + relpath], root)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def is_tracked(relpath: str, root: Path = REPO_ROOT) -> bool:
    return _git(["ls-files", "--error-unmatch", "--", relpath], root).returncode == 0


def is_clean(relpath: str, root: Path = REPO_ROOT) -> bool:
    completed = _git(["status", "--porcelain", "--", relpath], root)
    return completed.stdout.strip() == ""


def producer_provenance(gate_id: str, producer_id: str, root: Path = REPO_ROOT) -> dict:
    """Compute current provenance for a producer from disk/git."""
    rel = producer_source_path(producer_id)
    if not rel:
        return {
            "producerSourcePath": "",
            "producerSourceHash": "",
            "gitBlobId": "",
            "repositoryCommit": git_head(root),
            "trackedSource": False,
            "sourceClean": False,
        }
    tracked = is_tracked(rel, root)
    clean = is_clean(rel, root) if tracked else False
    content_hash = sha256_file(root / rel)
    return {
        "producerSourcePath": rel,
        "producerSourceHash": content_hash,
        "gitBlobId": git_blob(rel, root) if tracked else "",
        "repositoryCommit": git_head(root),
        "trackedSource": tracked,
        "sourceClean": clean,
    }


def provenance_toolversions(provenance: dict) -> dict:
    """Flatten provenance into string-valued toolVersions entries."""
    return {
        "producerSourcePath": provenance.get("producerSourcePath", ""),
        "producerSourceHash": provenance.get("producerSourceHash", ""),
        "gitBlobId": provenance.get("gitBlobId", ""),
        "repositoryCommit": provenance.get("repositoryCommit", ""),
        "trackedSource": "true" if provenance.get("trackedSource") else "false",
        "sourceClean": "true" if provenance.get("sourceClean") else "false",
    }


def verify_provenance(gate_id: str, recorded: dict, root: Path = REPO_ROOT) -> list[str]:
    """Recompute producer provenance from disk and compare to the recorded values.

    Returns mismatch codes. Empty means the recorded provenance matches the
    current tracked producer source. ``sourceClean`` and ``gitBlobId`` are
    recorded for traceability; the tamper-evident property is enforced by the
    source-hash comparison (editing a producer after sealing changes its hash).
    Hard "clean working tree" enforcement at execution belongs to the F-6 commit
    gate, not the Judge.
    """
    from chapter_qa.registry import expected_producer

    spec = expected_producer(gate_id)
    if spec is None:
        return []
    current = producer_provenance(gate_id, spec["id"], root)
    recorded = recorded or {}
    codes = []
    if current["trackedSource"] is not True:
        codes.append("PRODUCER_UNTRACKED")
    if recorded.get("producerSourcePath") != current["producerSourcePath"]:
        codes.append("PRODUCER_PATH_MISMATCH")
    if recorded.get("producerSourceHash") != current["producerSourceHash"]:
        codes.append("PRODUCER_SOURCE_CHANGED")
    return codes
