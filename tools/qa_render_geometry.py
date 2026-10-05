"""Deterministic rendered-geometry checks on a PDF (reusable; Phase 6.1 visual QA).

For every page:
  * out-of-bounds words (outside the page or inside the unsafe edge band)
  * overlapping words (two different words whose boxes intersect > OVERLAP_FRAC of the smaller one)
  * near-empty pages (no words)
Uses `pdftotext -bbox` (poppler) only; no GUI, no network.
"""
import re, subprocess

OVERLAP_FRAC = 0.30
WORD_RE = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
PAGE_RE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)

def pages(pdf):
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True).stdout
    res = []
    for m in PAGE_RE.finditer(out):
        w, h = float(m.group(1)), float(m.group(2))
        words = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in WORD_RE.findall(m.group(3))]
        res.append((w, h, words))
    return res

def check(pdf, edge_pt=14.0, ignore=lambda t: False):
    """Return dict page-> {'oob': [...], 'overlap': [...], 'words': n}."""
    report = {}
    for pi, (W, H, words) in enumerate(pages(pdf), 1):
        oob = [t for (x0, y0, x1, y1, t) in words if x0 < edge_pt or y0 < edge_pt or x1 > W - edge_pt or y1 > H - edge_pt]
        ov = []
        n = len(words)
        for i in range(n):
            a = words[i]
            if ignore(a[4]):
                continue
            for j in range(i + 1, n):
                b = words[j]
                if b[0] >= a[2] or a[0] >= b[2] or b[1] >= a[3] or a[1] >= b[3]:
                    continue
                ix = min(a[2], b[2]) - max(a[0], b[0])
                iy = min(a[3], b[3]) - max(a[1], b[1])
                if ix <= 0 or iy <= 0:
                    continue
                area = ix * iy
                small = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
                if small > 0 and area / small > OVERLAP_FRAC:
                    ov.append("%s|%s" % (a[4], b[4]))
        report[pi] = {"oob": oob, "overlap": ov, "words": n}
    return report

def summarize(report):
    oob = {p: r["oob"] for p, r in report.items() if r["oob"]}
    ov = {p: r["overlap"] for p, r in report.items() if r["overlap"]}
    empty = [p for p, r in report.items() if r["words"] == 0]
    return oob, ov, empty

if __name__ == "__main__":
    import sys
    rep = check(sys.argv[1])
    oob, ov, empty = summarize(rep)
    print("pages", len(rep), "oob", oob, "overlap", ov, "empty", empty)
