"""One-shot export helper: DOCX/PPTX -> PDF (soffice headless) -> PNG previews (pdftoppm).

Usage: .venv/bin/python tools/export_pdf_previews.py SRC.(docx|pptx) PREVIEW_DIR PREFIX [DPI] [--pad2]
 - PDF is written next to the source (same stem).
 - Previews: PREFIX-N.png (or PREFIX-NN.png with --pad2). Old previews with this PREFIX are removed first.
Runs one soffice process at a time and exits. Uses an isolated profile (never touches the desktop).
"""
import glob, os, shutil, subprocess, sys, tempfile

def export(src, prev_dir, prefix, dpi=110, pad2=False):
    src = os.path.abspath(src)
    out_dir = os.path.dirname(src)
    prof = tempfile.mkdtemp(prefix="lo_prof_")
    try:
        subprocess.run(["soffice", "--headless", "--norestore", "-env:UserInstallation=file://" + prof,
                        "--convert-to", "pdf", "--outdir", out_dir, src],
                       check=True, capture_output=True, text=True, timeout=300)
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    pdf = os.path.splitext(src)[0] + ".pdf"
    os.makedirs(prev_dir, exist_ok=True)
    for old in glob.glob(os.path.join(prev_dir, prefix + "-*.png")):
        os.remove(old)
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), pdf, os.path.join(prev_dir, prefix)], check=True)
    # normalise pdftoppm numbering (it zero-pads to the page-count width)
    files = sorted(glob.glob(os.path.join(prev_dir, prefix + "-*.png")),
                   key=lambda f: int(os.path.splitext(f)[0].rsplit("-", 1)[1]))
    for f in files:
        n = int(os.path.splitext(f)[0].rsplit("-", 1)[1])
        new = os.path.join(prev_dir, "%s-%s.png" % (prefix, ("%02d" % n) if pad2 else str(n)))
        if new != f:
            os.replace(f, new)
    return pdf, len(files)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    pdf, n = export(a[0], a[1], a[2], int(a[3]) if len(a) > 3 else 110, pad2="--pad2" in sys.argv)
    print("pdf:", pdf, "previews:", n)
