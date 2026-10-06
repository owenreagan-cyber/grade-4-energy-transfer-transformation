"""Compare Chapter 2 instructional text to the reviewed golden baseline.

PRE-FREEZE (default): live extraction must equal qa/baselines/ch2_golden_text.json.
POST-FREEZE: the expected text is the file stored in the freeze commit, not the
working-tree copy. Editing the baseline in the same tree does not bless a change.

Usage:
  .venv/bin/python tools/qa_ch2_golden.py
  .venv/bin/python tools/qa_ch2_golden.py --mode post-freeze
  .venv/bin/python tools/qa_ch2_golden.py --root PATH
"""
import argparse, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapter_text import diff_lines
from ch2_golden_collect import collect

HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.abspath(os.path.join(HERE, ".."))
GOLDEN = "qa/baselines/ch2_golden_text.json"
FREEZE = "qa/baselines/ch2_freeze_baseline.json"


def _load(path):
    return json.load(open(path, encoding="utf-8"))


def expected_golden(mode, root):
    freeze_path = os.path.join(root, FREEZE)
    if mode == "post-freeze":
        if not os.path.exists(freeze_path):
            return None, "post-freeze baseline file is missing"
        freeze = _load(freeze_path)
        sha = freeze.get("freeze_commit") or "PENDING"
        if sha in ("", "PENDING", None):
            return None, "post-freeze mode is not armed; freeze commit is not recorded"
        try:
            blob = subprocess.check_output(
                ["git", "show", "%s:%s" % (sha, GOLDEN)], cwd=CANON, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            return None, "freeze commit does not contain %s (%s)" % (GOLDEN, exc.output.decode()[:180])
        return json.loads(blob.decode("utf-8")), None
    path = os.path.join(root, GOLDEN)
    if not os.path.exists(path):
        return None, "missing " + GOLDEN
    return _load(path), None


def _report(label, expected, actual, fails):
    added, removed, changed = diff_lines(expected, actual)
    if not added and not removed and not changed:
        return
    fails.append(label)
    if removed:
        print("  removed:", removed[0][:160])
    if added:
        print("  added:", added[0][:160])
    if changed:
        print("  expected:", " | ".join(changed[0]["expected"])[:160])
        print("  actual:", " | ".join(changed[0]["actual"])[:160])


def compare(expected, actual):
    fails = []
    for key, spec in expected["artifacts"].items():
        if key == "teacher_keys":
            live = actual["artifacts"]["teacher_keys"]
            for i, item in enumerate(spec):
                _report("teacher key %s" % item["path"], item["lines"], live[i]["lines"], fails)
            continue
        if key == "slides":
            live_slides = actual["artifacts"]["slides"]["slides"]
            exp_slides = spec["slides"]
            if len(live_slides) != len(exp_slides):
                fails.append("slides count %d != %d" % (len(live_slides), len(exp_slides)))
            for exp, live in zip(exp_slides, live_slides):
                _report("slide %d face" % exp["slide"], exp["lines"], live["lines"], fails)
                _report("slide %d speaker" % exp["slide"], exp["speaker"].split("\n"), live["speaker"].split("\n"), fails)
            continue
        _report(key, spec["lines"], actual["artifacts"][key]["lines"], fails)
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--mode", choices=("pre-freeze", "post-freeze"), default="pre-freeze")
    a = ap.parse_args()
    root = os.path.abspath(a.root or CANON)
    expected, err = expected_golden(a.mode, root if a.mode == "pre-freeze" else CANON)
    print("=" * 72)
    print("CH2 GOLDEN TEXT  mode=%s" % a.mode)
    print("=" * 72)
    if err:
        print("[FAIL] GOLDEN", err)
        sys.exit(1)
    fails = compare(expected, collect(root))
    if fails:
        for f in fails:
            print("[FAIL] GOLDEN", f)
        print("OVERALL: FAIL (%d)" % len(fails))
        sys.exit(1)
    print("[PASS] golden instructional text matches the %s baseline" % a.mode)
    print("OVERALL: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
