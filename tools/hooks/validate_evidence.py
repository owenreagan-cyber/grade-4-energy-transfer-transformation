"""Dry-run evidence check.

Re-evaluates records through the Phase A evaluator. A status field of
PASS on the input is ignored.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from chapter_qa.evidence import evaluate, evidence_from_dict
from chapter_qa.gates import gate_by_id
from chapter_qa.identity import BuildIdentity

from hooks.decisions import allow, deny


def identity_from_payload(data) -> BuildIdentity:
    if not isinstance(data, dict):
        raise ValueError("build identity missing")
    required = (
        "buildId",
        "candidatePath",
        "candidateFreezeId",
        "candidateHash",
        "sourceFreezeId",
        "sourceHash",
    )
    for key in required:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError("build identity field %s missing" % key)
    hashes = data.get("inputHashes")
    if not isinstance(hashes, dict) or not hashes:
        raise ValueError("build identity inputHashes missing")
    candidate_files = data.get("candidateFiles")
    if candidate_files is None:
        candidate_files = {}
    if not isinstance(candidate_files, dict):
        raise ValueError("build identity candidateFiles must be a map")
    return BuildIdentity(
        buildId=data["buildId"],
        candidatePath=data["candidatePath"],
        candidateFreezeId=data["candidateFreezeId"],
        candidateHash=data["candidateHash"],
        sourceFreezeId=data["sourceFreezeId"],
        sourceHash=data["sourceHash"],
        inputHashes=dict(hashes),
        candidateFiles=dict(candidate_files),
    )


def validate_record(data, gates, identity: BuildIdentity) -> dict:
    """Return ALLOW only when evaluate() accepts the record."""
    if not isinstance(data, dict):
        return deny("malformed evidence")
    try:
        record = evidence_from_dict(data)
        gate = gate_by_id(gates, record.gateId)
        result = evaluate(record, gate, identity)
        from hooks.final_release_gate import _design_source
        if _design_source(record.independentEvidenceSource):
            return deny("design server state is not independent evidence")
    except Exception as exc:
        return deny("evidence rejected: %s" % type(exc).__name__)
    if result.status != "PASS":
        return deny(
            "evidence is not PASS",
            status=result.status,
            codes=sorted(result.codes),
        )
    return allow("evidence passed evaluation", status=result.status, codes=[])


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Dry-run evidence validation.")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.apply:
        sys.stdout.write(json.dumps(deny("hook activation is refused; dry-run only")))
        return 2
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            result = deny("malformed hook input")
        else:
            from chapter_qa.gates import load_gates

            result = validate_record(
                payload.get("evidence"),
                load_gates(),
                identity_from_payload(payload.get("build")),
            )
    except Exception:
        result = deny("evidence validation failed closed")
    sys.stdout.write(json.dumps(result))
    return 2 if result["decision"] == "DENY" else 0


if __name__ == "__main__":
    raise SystemExit(main())
