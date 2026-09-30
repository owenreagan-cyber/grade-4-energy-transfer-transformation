#!/usr/bin/env python3
"""
Phase 13S — student-facing font-floor fixer.

Bumps any run whose size is below `floor_pt` up to `floor_pt`, preserving
bold/italic/color. Skips runs whose text looks like a slide/page-number,
provenance footer, or other non-student metadata (optional).

Usage:
  python tools/fix_font_floor.py --files <list> --floor 12 [--dry-run]
"""
import argparse
import glob
import os
import sys

from docx import Document
from docx.shared import Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Words that indicate a metadata/provenance footer we should NOT touch
SKIP_HINTS = ("provenance:", "source:", "adapted", "custom", "extension",
              "©", "v1.", "version")


def should_skip(text):
    t = text.strip().lower()
    if not t:
        return True
    # pure page numbers / tiny labels
    if len(t) <= 3 and t.isdigit():
        return False  # still bump; they're not student-facing but harmless
    if any(h in t for h in SKIP_HINTS):
        return True
    return False


def bump_docx(path, floor, dry_run):
    doc = Document(path)
    changed = 0
    skipped = 0

    def fix_runs(paras):
        nonlocal changed, skipped
        for p in paras:
            for r in p.runs:
                if r.font.size is not None and r.font.size.pt < floor:
                    txt = r.text
                    if should_skip(txt):
                        skipped += 1
                        continue
                    if not dry_run:
                        r.font.size = Pt(floor)
                    changed += 1

    fix_runs(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                fix_runs(cell.paragraphs)

    if not dry_run:
        doc.save(path)
    return changed, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--floor", type=float, default=12.0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    paths = []
    for pat in args.files:
        full = pat if os.path.isabs(pat) else os.path.join(ROOT, pat)
        paths += glob.glob(full, recursive=True)

    total_c = total_s = 0
    for p in sorted(set(paths)):
        c, s = bump_docx(p, args.floor, args.dry_run)
        rel = os.path.relpath(p, ROOT)
        mode = "DRY-RUN" if args.dry_run else "FIXED"
        print(f"[{mode}] {rel}: bumped={c} skipped={s}")
        total_c += c
        total_s += s
    print(f"\nTotal: {total_c} runs bumped, {total_s} skipped")


if __name__ == "__main__":
    main()
