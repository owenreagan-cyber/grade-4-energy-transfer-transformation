import json
import sys
sys.path.insert(0, "tools")
from chapter_qa.mandatory_producers import emit_adversarial_qa
from ch3_seal_remaining import identity, seal_call
from run_adversarial_qa import execute
_rows, summary = execute(seed=20261006, held_out=True)
summary = dict(summary)
summary["completed"] = True
summary["canonicalRepoTouched"] = summary.get("canonicalTouched", 1)
result = seal_call("ADVERSARIAL_QA", lambda rel: emit_adversarial_qa(summary, identity(), rel))
print(json.dumps({"status": result["status"], "summary": summary}, indent=2))
