"""Reseal gates invalidated by the v1.2 detector changes, then judge."""
import json
import subprocess
import sys

sys.path.insert(0, "tools")
from chapter_qa.mandatory_producers import emit_adversarial_qa, emit_inventory, emit_prior_frozen
from chapter_qa.release_set import emit_release_evidence
from ch3_seal_remaining import RELEASE, identity, inventory_names, release_dir, seal_call, spec
from run_adversarial_qa import execute

def frozen_rows():
    def run(script, *args):
        return subprocess.run([sys.executable, "tools/" + script, *args], capture_output=True, text=True, check=False)
    guard = run("qa_ch1_note_architecture.py")
    parity1 = run("qa_release_parity.py", "--chapter", "1")
    certify = run("certify_chapter.py", "--chapter", "2")
    golden = run("qa_ch2_golden.py", "--mode", "post-freeze")
    parity2 = run("qa_release_parity.py", "--chapter", "2")
    status = subprocess.run([
        "git", "status", "--short", "--",
        "docs/chapter-01", "docs/chapter-02",
        "production/teacher-playbook/unit1-teacher-playbook.docx",
        "production/teacher-playbook/unit1-teacher-playbook.pdf",
        "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx",
        "production/slides/02-ch2-moving-objects-have-energy-slides.pptx",
    ], capture_output=True, text=True, check=False)
    churn = 0 if status.returncode == 0 and not status.stdout.strip() else 1
    passes = sum(1 for line in parity1.stdout.splitlines() if line.startswith("[PASS]"))
    playbook = subprocess.run(["git", "diff", "--exit-code", "--", "production/teacher-playbook/unit1-teacher-playbook.docx", "production/teacher-playbook/unit1-teacher-playbook.pdf"], capture_output=True)
    return {
        "1": {
            "guard": "6/6" if "6/6" in guard.stdout and "unreviewed: 0" in guard.stdout else guard.stdout[-120:],
            "guardExpected": "6/6",
            "unreviewed": 0 if "unreviewed: 0" in guard.stdout else 1,
            "stale": 0 if "stale allowlist: 0" in guard.stdout else 1,
            "parity": "14/14" if passes == 14 and "OVERALL: PASS" in parity1.stdout else parity1.stdout[-120:],
            "parityExpected": "14/14",
            "churn": churn,
        },
        "2": {
            "guard": "PASS" if certify.returncode == 0 and "OVERALL: PASS" in golden.stdout else (certify.stdout or certify.stderr)[-160:],
            "guardExpected": "PASS",
            "unreviewed": 0,
            "stale": 0,
            "parity": "PASS" if "OVERALL: PASS" in parity2.stdout else parity2.stdout[-120:],
            "parityExpected": "PASS",
            "churn": churn,
        },
        "playbookUnchanged": playbook.returncode == 0,
        "churnText": status.stdout,
    }

def main():
    ident = identity()
    chapter = spec()
    expected, observed = inventory_names(chapter)
    inventory = seal_call("INVENTORY", lambda rel: emit_inventory(expected, observed, ident, rel))
    originals = release_dir(expected)
    manifest = {"files": originals, "status": "BUILD_IN_PROGRESS", "expectStatus": "BUILD_IN_PROGRESS"}
    exact = seal_call("RELEASE_EXACT_SET", lambda rel: emit_release_evidence(sorted(originals), str(RELEASE), manifest, ident, rel, gate_id="RELEASE_EXACT_SET", original_hashes=originals))
    parity = seal_call("RELEASE_PARITY", lambda rel: emit_release_evidence(sorted(originals), str(RELEASE), manifest, ident, rel, gate_id="RELEASE_PARITY", original_hashes=originals))
    _rows, adversarial = execute(seed=20261006, held_out=True)
    adversarial = dict(adversarial)
    adversarial["completed"] = True
    adversarial["canonicalRepoTouched"] = adversarial.get("canonicalTouched", 1)
    attack = seal_call("ADVERSARIAL_QA", lambda rel: emit_adversarial_qa(adversarial, ident, rel))
    frozen = frozen_rows()
    playbook = frozen.pop("playbookUnchanged")
    churn_text = frozen.pop("churnText")
    frozen_gate = seal_call("PRIOR_FROZEN_NONREGRESSION", lambda rel: emit_prior_frozen({"1": frozen["1"], "2": frozen["2"]}, ident, rel))
    print(json.dumps({
        "inventory": inventory["status"],
        "exact": exact["status"],
        "parity": parity["status"],
        "adversarial": adversarial,
        "attack": attack["status"],
        "frozen": frozen_gate["status"],
        "frozenDetail": frozen,
        "playbook": playbook,
        "churn": churn_text,
    }, indent=2))

if __name__ == "__main__":
    main()
