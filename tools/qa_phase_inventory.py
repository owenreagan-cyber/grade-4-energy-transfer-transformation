"""Phase artifact-inventory completeness QA (reusable; Phase 6.1 governance).

Every changed path (git status, untracked expanded) that is IN SCOPE for the phase must be covered by a backticked
path/glob in the phase inventory. Brace groups `{a,b}` are expanded; `*` is a glob; directory prefixes cover children.

Usage: .venv/bin/python tools/qa_phase_inventory.py INVENTORY.md [--exclude REGEX ...] [--report out.md]
Exit 0 = every in-scope changed path accounted for.
"""
import glob, argparse, fnmatch, itertools, os, re, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
# Default exclusions for the Phase 6.1 (Chapter 1) run: other chapters / concurrent phases.
DEFAULT_EXCLUDES = [
    r"(^|/)(0[2-9])-ch[2-9]", r"chapter-0[2-9]", r"CH[2-9]_", r"PHASE_7_", r"ch[2-9]-(notes|slides)", r"_ch[2-9]_", r"build_ch[2-9]",
    r"qa_ch[2-9]",
]


def expand_braces(s):
    m = re.search(r"\{([^{}]*)\}", s)
    if not m:
        return [s]
    out = []
    for opt in m.group(1).split(","):
        out += expand_braces(s[:m.start()] + opt + s[m.end():])
    return out


def inventory_patterns(md):
    toks = re.findall(r"`([^`\n]+)`", open(md, encoding="utf-8").read())
    pats = set()
    for t in toks:
        if "/" not in t and not t.endswith((".py", ".md")):
            continue
        t = re.sub(r"\s+\(.*$", "", t).strip()
        for e in expand_braces(t.strip()):
            for part in re.split(r",\s+", e):
                if part.strip():
                    pats.add(part.strip())
    return pats


def changed_paths():
    out = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=REPO, capture_output=True, text=True).stdout
    paths = []
    for line in out.splitlines():
        p = line[3:].strip().strip('"')
        if " -> " in p:
            p = p.split(" -> ")[1]
        paths.append(p)
    return paths


def covered(path, pats):
    for pat in pats:
        if path == pat or fnmatch.fnmatch(path, pat) or path.startswith(pat.rstrip("*").rstrip("/") + "/") and not pat.endswith(".md"):
            return True
        # "dir/*" style and bare-dir mentions
        if fnmatch.fnmatch(path, pat + "*") and pat.endswith(("-", "_")):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inventory"); ap.add_argument("--exclude", action="append", default=None); ap.add_argument("--report")
    a = ap.parse_args()
    ex = [re.compile(x) for x in (a.exclude if a.exclude is not None else DEFAULT_EXCLUDES)]
    pats = inventory_patterns(os.path.join(REPO, a.inventory))
    inscope, excluded, missing = [], [], []
    for p in changed_paths():
        if any(r.search(p) for r in ex):
            excluded.append(p); continue
        inscope.append(p)
        if not covered(p, pats):
            missing.append(p)
    # existence check: every concrete path / glob the inventory names must resolve to something on disk or in git history
    ghosts = []
    for pat in sorted(pats):
        if "…" in pat or "<" in pat or pat.startswith(("http", "~")) or "/" not in pat:
            continue
        if not (glob.glob(os.path.join(REPO, pat)) or os.path.exists(os.path.join(REPO, pat.rstrip("*/")))):
            ghosts.append(pat)
    for gp in ghosts:
        print("  GHOST (named in inventory, not on disk)", gp)
    missing += ["GHOST:" + g for g in ghosts]
    print("changed paths: %d · in scope: %d · excluded (other chapters/phases): %d · NOT in inventory: %d" %
          (len(inscope) + len(excluded), len(inscope), len(excluded), len(missing)))
    for m in missing:
        print("  MISSING", m)
    if a.report:
        with open(os.path.join(REPO, a.report), "w") as f:
            f.write("# Artifact-inventory completeness\n\nInventory: `%s` · in-scope changed paths: %d · excluded: %d · missing: **%d** → **%s**\n\n" %
                    (a.inventory, len(inscope), len(excluded), len(missing), "PASS" if not missing else "FAIL"))
            for m in missing:
                f.write("- MISSING `%s`\n" % m)
            f.write("\nExcluded by regex (other chapters / concurrent phases):\n")
            for e in excluded:
                f.write("- `%s`\n" % e)
    sys.exit(0 if not missing else 1)


if __name__ == "__main__":
    main()
