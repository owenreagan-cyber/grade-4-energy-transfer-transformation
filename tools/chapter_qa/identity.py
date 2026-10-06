"""Build and freeze identity. Evidence from build A cannot certify build B."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


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

    def canonical_payload(self) -> dict:
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
        identity.canonical_payload(),
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
