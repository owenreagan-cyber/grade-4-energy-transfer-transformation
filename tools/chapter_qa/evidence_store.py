"""Fail-on-abort evidence store.

A producer failure, abort, exception, timeout, parser failure, or partial run can
NEVER leave an earlier PASS active. This module provides the orchestration layer
that:

- invalidates the prior active record for (buildId, gateId, scope) BEFORE running;
- runs the producer and converts any abort into a current FAIL record;
- writes evidence atomically (temp + rename), never half-written;
- deduplicates to exactly one active record per (buildId, gateId, scope);
- records a run manifest so a partial run is explicit.

This layer is not a gate evaluator; it delegates to the registered producer and
the central evaluator (``seal``).
"""

from __future__ import annotations

import json
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path

from chapter_qa.identity import REPO_ROOT

ACTIVE_SUFFIX = ".json"
ARCHIVE_DIR = "archive"
RUN_MANIFEST = "run-manifest.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def evidence_root(build_id: str, root: Path | None = None) -> Path:
    return (root or REPO_ROOT) / "qa" / "work" / build_id / "evidence"


def active_key(gate_id: str, scope: str | None = None) -> str:
    key = gate_id.lower()
    if scope:
        key += "-" + str(scope).lower().replace("/", "-")
    return key


def active_path(build_id: str, gate_id: str, scope: str | None = None, root: Path | None = None) -> Path:
    return evidence_root(build_id, root) / (active_key(gate_id, scope) + ACTIVE_SUFFIX)


def _archive_path(build_id: str, gate_id: str, scope: str | None, root: Path | None = None) -> Path:
    folder = evidence_root(build_id, root) / ARCHIVE_DIR
    stamp = utc_now().replace(":", "").replace("-", "").replace("T", "-")
    return folder / ("%s-%s.json" % (stamp, active_key(gate_id, scope)))


def invalidate_prior(build_id: str, gate_id: str, scope: str | None = None, root: Path | None = None) -> list[str]:
    """Move the current active record (if any) into the archive and return archived names.

    This guarantees an aborted rerun cannot leave the previous PASS in the active
    location.
    """
    current = active_path(build_id, gate_id, scope, root)
    if not current.is_file():
        return []
    archive = _archive_path(build_id, gate_id, scope, root)
    archive.parent.mkdir(parents=True, exist_ok=True)
    os.replace(str(current), str(archive))
    return [archive.name]


def write_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def fail_record(build_id: str, gate_id: str, scope: str | None, identity, exc: BaseException) -> dict:
    """A minimal current FAIL record for an aborted producer run."""
    return {
        "schemaVersion": "1.0",
        "evidenceId": "%s-abort" % active_key(gate_id, scope),
        "gateId": gate_id,
        "buildId": build_id,
        "candidatePath": getattr(identity, "candidatePath", ""),
        "candidateHash": getattr(identity, "candidateHash", ""),
        "status": "FAIL",
        "performed": False,
        "aborted": True,
        "failureReason": "%s: %s" % (type(exc).__name__, str(exc)[:400]),
        "traceback": traceback.format_exc(limit=8),
        "abortedAt": utc_now(),
    }


def record_manifest(manifest: dict, build_id: str, root: Path | None = None) -> None:
    path = evidence_root(build_id, root) / RUN_MANIFEST
    write_atomic(path, manifest)


def active_records(build_id: str, root: Path | None = None) -> dict[str, Path]:
    """Map active_key -> path for the current active evidence records."""
    folder = evidence_root(build_id, root)
    if not folder.is_dir():
        return {}
    return {
        p.name[: -len(ACTIVE_SUFFIX)]: p
        for p in folder.glob("*" + ACTIVE_SUFFIX)
        if p.is_file() and p.name != RUN_MANIFEST
    }


def run_gate(build_id: str, gate_id: str, producer, identity, *, scope: str | None = None,
             root: Path | None = None, manifest: dict | None = None) -> dict:
    """Run one producer with fail-on-abort semantics.

    Invalidates prior active evidence, runs the producer, and writes exactly one
    current active record (PASS/FAIL/NOT_VERIFIED from seal, or an abort-FAIL
    record on exception). Returns the stored record dict.

    `producer` is a zero-argument-or-preadded callable that returns ``(stored, result)``
    from ``seal()``. On any exception it is replaced with an abort-FAIL record.
    """
    invalidate_prior(build_id, gate_id, scope, root)
    path = active_path(build_id, gate_id, scope, root)
    try:
        stored, result = producer()
        if not isinstance(stored, dict):
            stored = fail_record(build_id, gate_id, scope, identity, ValueError("producer returned no record"))
    except Exception as exc:  # noqa: BLE001 — fail-on-abort is the point
        stored = fail_record(build_id, gate_id, scope, identity, exc)
    write_atomic(path, stored)
    if manifest is not None:
        manifest.setdefault("gates", []).append({
            "gateId": gate_id,
            "scope": scope,
            "status": stored.get("status", "FAIL"),
            "aborted": bool(stored.get("aborted")),
            "evidencePath": str(path.relative_to(root or REPO_ROOT)),
            "finishedAt": utc_now(),
        })
    return stored


def dedup_active(build_id: str, gate_id: str, scope: str | None = None, root: Path | None = None) -> list[str]:
    """Archive any extra active records for the same key beyond the first, returning names.

    Deterministic active naming means there is at most one file per key by
    construction; this is a defensive sweep for stray duplicates.
    """
    key = active_key(gate_id, scope)
    matches = sorted(p for p in (evidence_root(build_id, root).glob(key + ACTIVE_SUFFIX)) if p.is_file())
    archived = []
    for extra in matches[1:]:
        archive = _archive_path(build_id, gate_id, scope, root)
        archive = archive.with_name(archive.name.replace(".json", "-dup.json"))
        archive.parent.mkdir(parents=True, exist_ok=True)
        os.replace(str(extra), str(archive))
        archived.append(archive.name)
    return archived
