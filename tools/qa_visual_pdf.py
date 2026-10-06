"""Reusable deterministic visual QA for rendered PDFs (Phase 6.1). Classifies each page PASS / WARN / FAIL.

Per page (poppler + Pillow only; no GUI):
  FAIL  blank page (no words AND <0.15% ink) · text out of bounds / in the unsafe edge band · overlapping words ·
        wrong page size for the artifact kind · pixel ink in the outer 0.2in band on print pages (clipping) ·
        any word box shorter than MIN_FAIL_PT
  WARN  word box shorter than MIN_WARN_PT (small text) · body ends in the last 0.45in (tight bottom) ·
        sparse page (body fills <30% of page height) on a non-final page · grayscale contrast: >2% pure-mid pixels
        is NOT checked (see tools/qa_visual_system.py for token contrast)
  PASS  otherwise
Kinds: letter (8.5x11 print) · slide (16:9) · key (letter, teacher-only).

Usage: .venv/bin/python tools/qa_visual_pdf.py --report qa/reports/X.md PDF[:kind[:LO-HI]] ...
"""
import argparse, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_render_geometry as G
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MIN_FAIL_PT = 6.0     # word-box height (~5pt font)
MIN_WARN_PT = 8.4     # word-box height (~7pt font)
SIZES = {"letter": (612, 792), "key": (612, 792), "slide": (960, 540), "landscape": (792, 612)}


def classify(pdf, kind):
    pages = G.pages(pdf)
    rep = G.check(pdf, edge_pt=(5.0 if kind == "slide" else 14.0))   # slides: chrome (slide no.) may sit near the edge
    out = []
    tmp = tempfile.mkdtemp(prefix="vqa_")
    subprocess.run(["pdftoppm", "-gray", "-r", "40", pdf, os.path.join(tmp, "p")], check=True)
    imgs = sorted(f for f in os.listdir(tmp) if f.endswith(".pgm") or f.endswith(".png"))
    for i, (W, H, words) in enumerate(pages, 1):
        fails, warns = [], []
        ew, eh = SIZES[kind]
        if abs(W - ew) > 3 or abs(H - eh) > 3:
            fails.append("page size %.0fx%.0f (expect %dx%d)" % (W, H, ew, eh))
        r = rep[i]
        if r["oob"]:
            fails.append("out-of-bounds words: %s" % r["oob"][:4])
        if r["overlap"]:
            fails.append("overlapping words: %s" % r["overlap"][:4])
        im = Image.open(os.path.join(tmp, imgs[i - 1])).convert("L")
        px = im.load(); w, h = im.size
        ink = sum(1 for y in range(h) for x in range(w) if px[x, y] < 200) / float(w * h)
        if not words and ink < 0.0015:
            fails.append("blank page")
        if words and kind != "slide" and not [wd for wd in words if wd[3] < H - 40]:
            fails.append("blank page (footer only)")
        if kind != "slide":
            band = int(0.2 * 40)
            edge = sum(1 for y in range(h) for x in range(w)
                       if (x < band or y < band or x >= w - band or y >= h - band) and px[x, y] < 160)
            if edge > 6:
                fails.append("ink in outer 0.2in band (%d px) — clipping risk" % edge)
        heights = [wd[3] - wd[1] for wd in words if wd[4].strip()]
        small = [x for x in heights if x < MIN_FAIL_PT]
        warn_small = [x for x in heights if MIN_FAIL_PT <= x < MIN_WARN_PT]
        if small:
            fails.append("%d word(s) with box height < %.1fpt (min %.1f)" % (len(small), MIN_FAIL_PT, min(small)))
        elif warn_small and kind != "slide":
            warns.append("%d word(s) with box height %.1f–%.1fpt (small print)" % (len(warn_small), MIN_FAIL_PT, MIN_WARN_PT))
        if words and kind != "slide":
            body = [wd for wd in words if wd[3] < H - 40]
            if body:
                bottom = max(wd[3] for wd in body)
                if bottom > H - 0.45 * 72 - 18:
                    warns.append("tight bottom (body ends %.2fin from bottom incl. footer allowance)" % ((H - bottom) / 72))
                if bottom < 0.30 * H and i < len(pages):
                    warns.append("sparse page (body fills %d%%)" % int(100 * bottom / H))
        out.append((i, "FAIL" if fails else ("WARN" if warns else "PASS"), fails, warns))
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--report"); ap.add_argument("items", nargs="+")
    a = ap.parse_args()
    lines, worst, summary = [], "PASS", []
    for it in a.items:
        parts = it.split(":")
        path, kind = parts[0], (parts[1] if len(parts) > 1 and parts[1] else "letter")
        res = classify(os.path.join(REPO, path), kind)
        label = path
        if len(parts) > 2 and parts[2]:          # page range, e.g. 1-21 (artifact scope)
            lo, hi = [int(x) for x in parts[2].split("-")]
            res = [r for r in res if lo <= r[0] <= hi]
            label = "%s [pp. %d-%d]" % (path, lo, hi)
        path = label
        cnt = {"PASS": 0, "WARN": 0, "FAIL": 0}
        for pg, st, fails, warns in res:
            cnt[st] += 1
            for msg in fails:
                lines.append((path, pg, "FAIL", msg))
            for msg in warns:
                lines.append((path, pg, "WARN", msg))
        art = "FAIL" if cnt["FAIL"] else ("WARN" if cnt["WARN"] else "PASS")
        if art == "FAIL" or (art == "WARN" and worst == "PASS"):
            worst = art if worst != "FAIL" else worst
        summary.append((path, kind, len(res), cnt, art))
        print("%-4s %-78s pages=%-3d P/W/F=%d/%d/%d" % (art, path, len(res), cnt["PASS"], cnt["WARN"], cnt["FAIL"]))
    for p, pg, st, msg in lines:
        print("  %s %s p%d: %s" % (st, p, pg, msg))
    print("OVERALL:", worst)
    if a.report:
        with open(os.path.join(REPO, a.report), "w") as f:
            f.write("# Visual QA (deterministic rendered checks)\n\nTool: `tools/qa_visual_pdf.py` · overall: **%s**\n\n" % worst)
            f.write("| Artifact | Kind | Pages | PASS | WARN | FAIL | Result |\n|---|---|---|---|---|---|---|\n")
            for p, k, n, c, art in summary:
                f.write("| `%s` | %s | %d | %d | %d | %d | **%s** |\n" % (p, k, n, c["PASS"], c["WARN"], c["FAIL"], art))
            f.write("\n## WARN / FAIL detail\n\n")
            if not lines:
                f.write("None.\n")
            f.write("| File | Page/slide | Class | Issue |\n|---|---|---|---|\n")
            for p, pg, st, msg in lines:
                f.write("| `%s` | %d | %s | %s |\n" % (p, pg, st, msg.replace("|", "/")))
    sys.exit(1 if worst == "FAIL" else 0)


if __name__ == "__main__":
    main()
