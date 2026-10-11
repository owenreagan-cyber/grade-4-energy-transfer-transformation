#!/usr/bin/env python3
"""One-shot, font-faithful PPTX -> PDF -> PNG render (Phase 5C).

Root cause this fixes (Phase 5C, CH1_VISUAL_QA_ROOT_CAUSE_ANALYSIS.md RC-6): a *fresh* isolated LibreOffice
profile launched from an agent shell does not enumerate macOS system fonts, so Avenir Next / Georgia silently
became Linux Libertine / Frank Ruhl. Every render that reused a desktop-session instance hid this. We therefore
stage the deck's font files into the isolated profile's user/fonts directory (LibreOffice registers them at
start-up) — the system fonts themselves are never modified.

Usage: .venv/bin/python tools/render_slides_isolated.py DECK.pptx OUT_DIR [--dpi 110] [--sheet contact-sheet.png]
Writes OUT_DIR/<stem>.pdf, OUT_DIR/previews/slide-NN.png and (optionally) a contact sheet. Exits non-zero on any
failed step (soffice exit code, missing/old PDF, page count mismatch). One soffice process; it exits on return.
"""
import argparse, glob, os, shutil, subprocess, sys, tempfile, time

FONT_FILES = [
    "/System/Library/Fonts/Avenir Next.ttc",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf",
    "/System/Library/Fonts/LucidaGrande.ttc",   # macOS fallback for U+2192 "→" (absent from Avenir/Georgia)
]


def render(pptx, out_dir, dpi=110, sheet=None, expect_pages=None):
    from pptx import Presentation
    pptx = os.path.abspath(pptx)
    os.makedirs(out_dir, exist_ok=True)
    n_slides = expect_pages or len(Presentation(pptx).slides)
    prof = tempfile.mkdtemp(prefix="lo_prof_5c_")
    try:
        fdir = os.path.join(prof, "user", "fonts")
        os.makedirs(fdir)
        for f in FONT_FILES:
            if not os.path.exists(f):
                raise SystemExit("missing font file: %s" % f)
            shutil.copy(f, fdir)
        t0 = time.time()
        r = subprocess.run(["soffice", "--headless", "--norestore", "-env:UserInstallation=file://" + prof,
                            "--convert-to", "pdf", "--outdir", out_dir, pptx],
                           capture_output=True, text=True, timeout=600)
        if r.returncode != 0:
            raise SystemExit("soffice exit %d: %s" % (r.returncode, r.stderr[-400:]))
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    pdf = os.path.join(out_dir, os.path.splitext(os.path.basename(pptx))[0] + ".pdf")
    if not os.path.exists(pdf) or os.path.getmtime(pdf) < t0 - 1:
        raise SystemExit("PDF missing or stale: %s" % pdf)
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    pages = int([l for l in info.splitlines() if l.startswith("Pages:")][0].split()[1])
    if pages != n_slides:
        raise SystemExit("page count %d != slides %d" % (pages, n_slides))
    prev = os.path.join(out_dir, "previews")
    os.makedirs(prev, exist_ok=True)
    for old in glob.glob(os.path.join(prev, "slide-*.png")):
        os.remove(old)
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), pdf, os.path.join(prev, "p")], check=True)
    for f in glob.glob(os.path.join(prev, "p-*.png")):
        n = int(os.path.splitext(f)[0].rsplit("-", 1)[1])
        os.rename(f, os.path.join(prev, "slide-%02d.png" % n))
    if sheet:
        contact_sheet(prev, sheet)
    return pdf, prev, pages


def contact_sheet(prev, out, cols=5, tw=440):
    from PIL import Image, ImageDraw
    files = sorted(glob.glob(os.path.join(prev, "slide-*.png")))
    th = int(tw * 7.5 / 13.333)
    rows = (len(files) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 34) + 12), (40, 40, 40))
    d = ImageDraw.Draw(sh)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB").resize((tw, th))
        x = 12 + (i % cols) * (tw + 12); y = 12 + (i // cols) * (th + 34)
        sh.paste(im, (x, y)); d.text((x, y + th + 6), os.path.basename(f), fill=(230, 230, 230))
    sh.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx"); ap.add_argument("out_dir"); ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--sheet")
    a = ap.parse_args()
    pdf, prev, pages = render(a.pptx, a.out_dir, a.dpi, a.sheet)
    print("pdf:", pdf, "pages:", pages, "previews:", prev)
