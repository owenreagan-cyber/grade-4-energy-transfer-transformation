"""Seal Chapter 3 CHAPTER_SPEC evidence. Does not assign PASS."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.identity import BuildIdentity, hash_file
from chapter_qa.mandatory_producers import emit_chapter_spec
from chapter_qa.workspace import workspace_for

SPEC = ROOT / "docs/chapter-03/CH3_CHAPTER_SPEC.json"
BUILD_ID = "ch3-factory-2026-10-06"


def main():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    reader = ROOT / "assets/authoritative/student-reader/chapters/Chapter_3_Energy_and_Speed_Are_Related.pdf"
    guide = ROOT / "assets/authoritative/teacher-guide/Science 4 - Energy Transfer - TG .pdf"
    calendar = ROOT / "docs/playbook/UNIT1_PACING_CALENDAR.md"
    prompt = ROOT / "docs/gold-standard/CHAPTER_03_PRODUCTION_PROMPT.md"
    identity = BuildIdentity(
        buildId=BUILD_ID,
        candidatePath="docs/chapter-03/CH3_CHAPTER_SPEC.json",
        candidateFreezeId="UNFROZEN",
        candidateHash=hash_file(str(SPEC)),
        sourceFreezeId="ckSci-ch3-reader-tg",
        sourceHash=hash_file(str(reader)),
        inputHashes={
            "calendar": hash_file(str(calendar)),
            "chapterSpec": hash_file(str(SPEC)),
            "productionPrompt": hash_file(str(prompt)),
            "readerChapter": hash_file(str(reader)),
            "teacherGuide": hash_file(str(guide)),
        },
    )
    work = workspace_for(BUILD_ID, ROOT / "qa" / "work")
    evidence_rel = "qa/work/%s/evidence/CHAPTER_SPEC.json" % BUILD_ID
    evidence_path = ROOT / evidence_rel
    evidence_path.write_text("{}\n", encoding="utf-8")
    stored, result = emit_chapter_spec(spec, identity, evidence_rel)
    evidence_path.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
    (work / "identity.json").write_text(
        json.dumps(identity.canonical_payload(), indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "gateId": stored["gateId"],
        "status": result.status,
        "reasons": list(result.reasons),
        "findings": stored["findings"],
        "evidence": evidence_rel,
        "candidateHash": identity.candidateHash,
    }, indent=2))
    return 0 if result.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
