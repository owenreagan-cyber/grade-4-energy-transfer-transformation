"""Run adversarial mutations on throwaway workspaces.

The canonical classroom tree is not modified. The runner is not a detector.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chapter_qa.adversary import canonical_fingerprint, held_out_cases, run_case
from chapter_qa.adversary_catalog import cases, matrix_markdown, write_case_files
from chapter_qa.evidence import REPO_ROOT


def select(all_cases, family=None, case_id=None):
    chosen = all_cases
    if family:
        chosen = [row for row in chosen if row["family"] == family]
    if case_id:
        chosen = [row for row in chosen if row["caseId"] == case_id]
    return chosen


def summarize(results):
    bad = [row for row in results if row["expectedStatus"] == "FAIL"]
    clean = [row for row in results if row["expectedStatus"] == "PASS"]
    held = [row for row in results if str(row["caseId"]).startswith("HELD-")]
    project_bad = [row for row in bad if not str(row["caseId"]).startswith("HELD-")]
    return {
        "projectBad": len(project_bad),
        "projectBadCaught": sum(1 for row in project_bad if row["caught"]),
        "projectBadGreen": sum(1 for row in project_bad if not row["caught"]),
        "heldOutBad": len(held),
        "heldOutCaught": sum(1 for row in held if row["caught"]),
        "heldOutGreen": sum(1 for row in held if not row["caught"]),
        "clean": len(clean),
        "cleanPass": sum(1 for row in clean if row["caught"]),
        "cleanRed": sum(1 for row in clean if not row["caught"]),
        "canonicalTouched": sum(1 for row in results if row["canonicalRepoTouched"]),
    }


def execute(seed=20261006, family=None, case_id=None, held_out=True, keep=False):
    chosen = select(cases(), family, case_id)
    if held_out and not case_id:
        chosen = chosen + held_out_cases(seed)
    before = canonical_fingerprint()
    results = []
    try:
        for row in chosen:
            results.append(run_case(row, seed, canonical_before=before))
    finally:
        work = REPO_ROOT / "qa" / "work" / "_phase_c"
        if work.exists() and not keep:
            shutil.rmtree(work)
    return results, summarize(results)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", type=int, default=0)
    parser.add_argument("--case", default=None)
    parser.add_argument("--family", default=None)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--held-out", action="store_true")
    parser.add_argument("--seed", type=int, default=20261006)
    parser.add_argument("--keep-workdir", action="store_true")
    parser.add_argument("--json-report", default=None)
    parser.add_argument("--write-matrix", default=None)
    parser.add_argument("--emit-cases", action="store_true")
    args = parser.parse_args()
    if args.emit_cases:
        write_case_files(REPO_ROOT / "qa" / "gold-standard" / "adversarial_cases")
        print("cases written")
        return
    results, summary = execute(
        seed=args.seed, family=args.family, case_id=args.case,
        held_out=args.held_out or args.all or not args.case, keep=args.keep_workdir,
    )
    print(json.dumps(summary, indent=2))
    if summary["projectBadGreen"] or summary["heldOutGreen"] or summary["cleanRed"] or summary["canonicalTouched"]:
        sys.exit(1)
    if args.json_report:
        Path = __import__("pathlib").Path
        Path(args.json_report).write_text(json.dumps({"summary": summary, "results": results}, indent=2), encoding="utf-8")
    if args.write_matrix:
        text = matrix_markdown([row for row in results if not str(row["caseId"]).startswith("HELD-")])
        __import__("pathlib").Path(args.write_matrix).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
