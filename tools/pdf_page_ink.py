"""Print per-page body ink extent (inches) of a PDF using pdftotext -bbox (poppler only)."""
import sys, subprocess, re
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import qa_render_geometry as G
for pdf in sys.argv[1:]:
    print(pdf)
    for i, (W, H, words) in enumerate(G.pages(pdf), 1):
        body = [w for w in words if w[3] < H - 40]   # drop footer band
        first = body[0][4] if body else ''
        print("  p%d words=%d body_bottom=%.2fin first=%r last=%r" % (i, len(words), (max(w[3] for w in body)/72) if body else 0, first, body[-1][4] if body else ''))
