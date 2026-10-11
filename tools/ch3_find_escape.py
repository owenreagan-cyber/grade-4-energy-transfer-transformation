import sys
sys.path.insert(0, "tools")
from run_adversarial_qa import execute
rows, summary = execute(seed=20261006, held_out=True)
print(summary)
for row in rows:
    if row["expectedStatus"] == "FAIL" and not row["caught"]:
        print("ESCAPED", row["caseId"], row.get("mutationMethod"), row.get("status"), row.get("targetGate"))
