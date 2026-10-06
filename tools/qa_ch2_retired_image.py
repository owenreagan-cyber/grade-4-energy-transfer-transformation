"""Detect a rasterized retired notebook page inside the Chapter 2 release.

Text markers still apply. This pass renders pages and compares a perceptual
hash with the archived notebook, so a picture of that page fails too.
"""
import argparse, os, subprocess, sys, tempfile
from PIL import Image

ARCHIVE = "production/archive/retired/chapter-02-pre-7.1/02-ch2-interactive-science-notebook.pdf"


def _ahash(path):
    im = Image.open(path).convert("L").resize((8, 8))
    pixels = list(im.get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.getdata())
    avg = sum(pixels) / len(pixels)
    bits = 0
    for i, p in enumerate(pixels):
        if p >= avg:
            bits |= 1 << i
    return bits


def _dist(a, b):
    return bin(a ^ b).count("1")


def _render(pdf, page, dest):
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "40", "-png", pdf, dest],
                   check=True, capture_output=True)
    hits = sorted(p for p in os.listdir(os.path.dirname(dest) or ".") if p.startswith(os.path.basename(dest)))
    if not hits:
        return ""
    return os.path.join(os.path.dirname(dest), hits[0])


def _pages(pdf):
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    import re
    return int(re.search(r"Pages:\s+(\d+)", info).group(1))


def archive_hashes(root):
    pdf = os.path.join(root, ARCHIVE)
    hashes = []
    if not os.path.exists(pdf):
        return hashes
    work = tempfile.mkdtemp(prefix="ch2img_")
    try:
        for i in range(1, _pages(pdf) + 1):
            base = os.path.join(work, "a%d" % i)
            png = _render(pdf, i, base)
            if os.path.exists(png):
                hashes.append(_ahash(png))
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    return hashes


def check(root, release_dir=None):
    rel = release_dir or os.path.join(root, "production/releases/chapter-02")
    known = archive_hashes(root)
    if not known or not os.path.isdir(rel):
        return ["RETIRED image baseline missing"] if not known else []
    fails = []
    work = tempfile.mkdtemp(prefix="ch2relimg_")
    try:
        for name in sorted(os.listdir(rel)):
            if not name.endswith(".pdf"):
                continue
            pdf = os.path.join(rel, name)
            for i in range(1, _pages(pdf) + 1):
                base = os.path.join(work, "%s-%d" % (name, i))
                png = _render(pdf, i, base)
                if not os.path.exists(png):
                    continue
                digest = _ahash(png)
                close = min(_dist(digest, h) for h in known)
                if close <= 6:
                    fails.append("RETIRED raster page %s p%d distance %d" % (name, i, close))
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--release-dir", default=None)
    a = ap.parse_args()
    root = os.path.abspath(a.root or os.path.join(os.path.dirname(__file__), ".."))
    fails = check(root, a.release_dir)
    if fails:
        for f in fails:
            print("[FAIL]", f)
        sys.exit(1)
    print("[PASS] no rasterized retired notebook page in the release")
    sys.exit(0)


if __name__ == "__main__":
    main()
