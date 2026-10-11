"""Run the Release Judge and the certification stop hook for this build."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from chapter_qa.evidence import evidence_from_dict
from chapter_qa.gates import load_gates
from chapter_qa.identity import BuildIdentity
from chapter_qa.release_judge import judge
from hooks.final_release_gate import decide_stop

root = Path("qa/work/ch3-factory-2026-10-06")
ident = BuildIdentity(**json.loads((root / "identity.json").read_text(encoding="utf-8")))
records = []
for path in sorted((root / "evidence").glob("*.json")):
    records.append(evidence_from_dict(json.loads(path.read_text(encoding="utf-8"))))
gates = load_gates()
plain = judge(gates, records, ident)
print("JUDGE_WITHOUT_INVALIDATION")
print(json.dumps(plain.to_dict(), indent=2))
payload = {
    "requestedAction": "internally_certified",
    "message": "CHAPTER 3 INTERNAL CERTIFICATION: PASS",
    "evidenceDirectory": str((root / "evidence").resolve()),
    "build": ident.canonical_payload(),
}
hook = decide_stop(payload)
print("HOOK")
print(json.dumps(hook, indent=2))
summary = json.loads((root / "seal-summary.json").read_text(encoding="utf-8"))
print("ADVERSARIAL")
print(json.dumps(summary.get("adversarial"), indent=2))
print("SYNC_MISSING", summary.get("syncMissing"))
print("PLAYBOOK_UNCHANGED", summary.get("playbookUnchanged"))
print("LIFECYCLE", summary.get("lifecycle"))
print("FONTS", json.dumps(summary.get("fonts"), indent=2))
