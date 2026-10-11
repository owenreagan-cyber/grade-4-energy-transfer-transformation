"""Seal Chapter 3 source and curriculum evidence. Does not assign PASS."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.identity import BuildIdentity
from chapter_qa.source_audit import emit_source_evidence

BUILD_ID = "ch3-factory-2026-10-06"
SPEC = ROOT / "docs/chapter-03/CH3_CHAPTER_SPEC.json"


def identity_from_work():
    data = json.loads((ROOT / "qa/work" / BUILD_ID / "identity.json").read_text(encoding="utf-8"))
    return BuildIdentity(
        buildId=data["buildId"],
        candidatePath=data["candidatePath"],
        candidateFreezeId=data["candidateFreezeId"],
        candidateHash=data["candidateHash"],
        sourceFreezeId=data["sourceFreezeId"],
        sourceHash=data["sourceHash"],
        inputHashes=dict(data["inputHashes"]),
    )


def main():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    identity = identity_from_work()
    folder = ROOT / "qa/work" / BUILD_ID / "evidence"
    jobs = (
        ("SOURCE_AUTHORITY", "SOURCE_SCHOLAR", spec["sourceClaims"] + spec["exclusionClaims"]),
        ("CURRICULUM_CORRECTNESS", "CURRICULUM_AUDITOR", spec["sourceClaims"] + spec["approvedClaims"] + spec["exclusionClaims"]),
    )
    results = []
    for gate_id, role, claims in jobs:
        rel = "qa/work/%s/evidence/%s.json" % (BUILD_ID, gate_id)
        path = ROOT / rel
        path.write_text("{}\n", encoding="utf-8")
        stored, result = emit_source_evidence(claims, identity, gate_id, rel, auditor_role=role)
        path.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
        results.append({
            "gateId": gate_id,
            "status": result.status,
            "reasons": list(result.reasons),
            "findings": stored["findings"],
        })
    print(json.dumps(results, indent=2))
    return 0 if all(item["status"] == "PASS" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
