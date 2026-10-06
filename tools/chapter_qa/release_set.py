"""Release set and retired-content checks. Hashes are content, not a copied manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path

from chapter_qa.emit import seal


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def assess_release(expected: list[str], observed_dir: Path, manifest: dict, *, retired_tokens: list[str] | None = None,
                   original_hashes: dict | None = None) -> dict:
    findings = []
    names = sorted(p.name for p in observed_dir.iterdir()) if observed_dir.is_dir() else []
    expected_set = set(expected)
    observed_set = set(names)
    for name in sorted(expected_set - observed_set):
        findings.append({"severity": "BLOCKING", "code": "missing_release_artifact", "message": "missing %s" % name})
    for name in sorted(observed_set - expected_set):
        findings.append({"severity": "BLOCKING", "code": "unexpected_release_artifact", "message": "unexpected %s" % name})
    if not original_hashes:
        findings.append({"severity": "BLOCKING", "code": "hash_launder", "message": "no established content hash was supplied"})
    tokens = [token.lower() for token in (retired_tokens or [])]
    for name in names:
        lowered = name.lower()
        if any(token in lowered for token in tokens):
            findings.append({"severity": "BLOCKING", "code": "retired_content", "message": "retired token in %s" % name})
        path = observed_dir / name
        digest = _hash_file(path)
        recorded = (manifest.get("files") or {}).get(name)
        if recorded is None:
            findings.append({"severity": "BLOCKING", "code": "manifest_mismatch", "message": "manifest missing hash for %s" % name})
        elif recorded != digest:
            findings.append({"severity": "BLOCKING", "code": "hash_mismatch", "message": "hash mismatch for %s" % name})
        if original_hashes is not None and original_hashes.get(name) not in (None, digest):
            findings.append({"severity": "BLOCKING", "code": "hash_launder", "message": "bytes for %s differ from the established hash" % name})
        if tokens and path.suffix == ".pdf" and any(token.encode() in path.read_bytes().lower() for token in tokens):
            if not any(item["message"].endswith(name) for item in findings):
                findings.append({"severity": "BLOCKING", "code": "retired_content", "message": "retired token embedded in %s" % name})
    status = (manifest.get("status") or "").strip()
    if manifest.get("expectStatus") and status != manifest.get("expectStatus"):
        findings.append({"severity": "BLOCKING", "code": "status_conflict", "message": "manifest status %s" % status})
    return {"findings": findings, "fails": bool(findings), "names": names}


def emit_release_evidence(expected, observed_dir, manifest, identity, evidence_path, *,
                          gate_id="RELEASE_EXACT_SET", auditor_role="PROVENANCE_AUDITOR", retired_tokens=None,
                          original_hashes=None):
    assessed = assess_release(
        expected, Path(observed_dir), manifest, retired_tokens=retired_tokens, original_hashes=original_hashes,
    )
    data = {
        "evidenceId": "release-%s" % gate_id.lower(),
        "gateId": gate_id,
        "auditorRole": auditor_role,
        "performed": True,
        "expectedInputs": list(expected),
        "observedInputs": [] if assessed["fails"] else list(expected),
        "thingBeingCertified": "candidate-release:%s" % identity.candidateHash,
        "independentEvidenceSource": "content-hashes:%s" % identity.sourceHash,
        "findings": assessed["findings"],
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": True,
            "detectorException": False,
            "requiredInputsPresent": bool(expected),
            "missingRender": False,
            "missingEvidence": not bool(expected),
            "stale": False,
            "gateSpecificFailure": assessed["fails"],
            "unavailableEvidence": False,
        },
        "inventory": [{"name": "releaseFiles", "expected": len(expected), "observed": 0 if assessed["fails"] else len(assessed["names"])}],
    }
    if not expected:
        data["expectedInputs"] = []
        data["observedInputs"] = []
    return seal(data, identity)
