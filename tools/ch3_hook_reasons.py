import json
import sys
sys.path.insert(0, "tools")
from chapter_qa.evidence import evidence_from_dict
from chapter_qa.gates import load_gates
from chapter_qa.identity import BuildIdentity
from chapter_qa.release_judge import judge
from hooks.edited_paths import resolve_edited_paths
from hooks.final_release_gate import _REPO
from hooks.invalidate_evidence import invalidate_edit

resolved = resolve_edited_paths({}, _REPO)
invalidation = invalidate_edit({"paths": resolved["paths"]})
affected = invalidation.get("affected") or {}
print("AFFECTED")
print(json.dumps(affected, indent=2))
root_ident = json.loads(open("qa/work/ch3-factory-2026-10-06/identity.json").read())
ident = BuildIdentity(**root_ident)
records = [evidence_from_dict(json.loads(p.read_text())) for p in sorted(__import__("pathlib").Path("qa/work/ch3-factory-2026-10-06/evidence").glob("*.json"))]
result = judge(load_gates(), records, ident, affected)
print("JUDGE_WITH_TREE")
print(json.dumps({"status": result.status, "blocking": result.blockingReasons}, indent=2))
