import json
import sys
sys.path.insert(0, "tools")
from ch3_seal_remaining import identity, playbook_records, seal_call, spec
ident = identity()
left, right = playbook_records(spec())
result = seal_call("PLAYBOOK_ALIGNMENT", lambda rel: __import__("chapter_qa.cross_artifact", fromlist=["emit_cross_evidence"]).emit_cross_evidence(left, right, ident, "PLAYBOOK_ALIGNMENT", rel, auditor_role="CROSS_ARTIFACT_AUDITOR"))
print(json.dumps(result, indent=2))
