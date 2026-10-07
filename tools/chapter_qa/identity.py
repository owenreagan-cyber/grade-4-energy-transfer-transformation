"""Build and freeze identity. Evidence from build A cannot certify build B.

Build identity binds the candidate to the actual classroom bytes. The Judge
recomputes those hashes from disk; caller-supplied current hashes are not
trusted. A committed mutation still fails because the bytes differ.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class BuildIdentity:
    buildId: str
    candidatePath: str
    candidateFreezeId: str
    candidateHash: str
    sourceFreezeId: str
    sourceHash: str
    inputHashes: dict
    # repo-relative path -> sha256 for every certification-relevant classroom
    # and release file. The exact set comes from the candidate inventory; it is
    # never hard-coded here. Empty means the build did not bind its bytes.
    candidateFiles: dict = field(default_factory=dict)

    def canonical_payload(self) -> dict:
        return {
            "buildId": self.buildId,
            "candidatePath": self.candidatePath,
            "candidateFreezeId": self.candidateFreezeId,
            "candidateHash": self.candidateHash,
            "sourceFreezeId": self.sourceFreezeId,
            "sourceHash": self.sourceHash,
            "inputHashes": dict(sorted(self.inputHashes.items())),
            "candidateFiles": dict(sorted(self.candidateFiles.items())),
        }

    def association_payload(self) -> dict:
        """Shared fields an evidence record can reconstruct. candidateFiles is a
        build-level binding verified from disk, not a per-record field."""
        return {
            "buildId": self.buildId,
            "candidatePath": self.candidatePath,
            "candidateFreezeId": self.candidateFreezeId,
            "candidateHash": self.candidateHash,
            "sourceFreezeId": self.sourceFreezeId,
            "sourceHash": self.sourceHash,
            "inputHashes": dict(sorted(self.inputHashes.items())),
        }


def association_hash(identity: BuildIdentity) -> str:
    raw = json.dumps(
        identity.association_payload(),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_hex(raw)


def identity_from_evidence(evidence) -> BuildIdentity:
    return BuildIdentity(
        buildId=evidence.buildId,
        candidatePath=evidence.candidatePath,
        candidateFreezeId=evidence.candidateFreezeId or "",
        candidateHash=evidence.candidateHash or "",
        sourceFreezeId=evidence.sourceFreezeId or "",
        sourceHash=evidence.sourceHash or "",
        inputHashes=dict(evidence.inputHashes),
    )


def recompute_mismatches(identity: BuildIdentity, root: Path | None = None) -> list[str]:
    """Recompute classroom-file hashes from disk and report every mismatch.

    Returns a list of human-readable mismatch descriptions. An empty list means
    every bound file's current bytes match the recorded build identity. Missing
    files are mismatches. This is the F-1/F-2 mechanism: staleness is a function
    of current bytes, not of git cleanliness.
    """
    base = root or REPO_ROOT
    mismatches = []
    if not identity.candidateFiles:
        return mismatches
    for rel, recorded in sorted(identity.candidateFiles.items()):
        text = str(rel or "").strip()
        if not text or text.startswith("/") or ".." in Path(text).parts:
            mismatches.append("%s: unsafe path" % text)
            continue
        target = base / text
        if not target.is_file():
            mismatches.append("%s: missing" % text)
            continue
        current = hash_file(str(target))
        if not recorded or current != recorded:
            mismatches.append("%s: hash mismatch (recorded %s, current %s)" % (text, recorded[:12], current[:12]))
    return mismatches


def _blank(value) -> bool:
    return not str(value or "").strip()


def _hashes_present(mapping) -> bool:
    if not mapping:
        return False
    return all(not _blank(key) and not _blank(value) for key, value in mapping.items())


def identity_mismatch_codes(evidence, requested: BuildIdentity) -> list[str]:
    """Return mismatch codes. Empty means the evidence belongs to the requested build."""
    codes = []
    if evidence.buildId != requested.buildId:
        codes.append("BUILD_MISMATCH")
    if evidence.candidatePath != requested.candidatePath:
        codes.append("IDENTITY_MISMATCH")
    if (evidence.candidateFreezeId or "") != requested.candidateFreezeId:
        codes.append("IDENTITY_MISMATCH")
    if (
        _blank(evidence.candidateHash)
        or _blank(requested.candidateHash)
        or evidence.candidateHash != requested.candidateHash
    ):
        codes.append("HASH_MISMATCH")
    if (evidence.sourceFreezeId or "") != requested.sourceFreezeId:
        codes.append("IDENTITY_MISMATCH")
    if (
        _blank(evidence.sourceHash)
        or _blank(requested.sourceHash)
        or evidence.sourceHash != requested.sourceHash
        or not _hashes_present(evidence.inputHashes)
        or not _hashes_present(requested.inputHashes)
        or dict(evidence.inputHashes) != dict(requested.inputHashes)
    ):
        codes.append("HASH_MISMATCH")
    ev_identity = identity_from_evidence(evidence)
    if association_hash(ev_identity) != association_hash(requested):
        if "BUILD_MISMATCH" not in codes and "IDENTITY_MISMATCH" not in codes and "HASH_MISMATCH" not in codes:
            codes.append("IDENTITY_MISMATCH")
    return codes
