#!/usr/bin/env python3
"""
Phase 13S/13T visual-QA render harness.

Renders every active release artifact to PNG for visual inspection and produces:
  - per-file slide/page renders  -> qa/temp/<phase>/render/<safe_name>/<nnn>.png
  - contact sheets               -> qa/temp/<phase>/contact/<safe_name>.png
  - typography extraction        -> qa/temp/<phase>/typography.json
  - manifest index               -> qa/temp/<phase>/manifest.json

Pipeline:
  PPTX  -> LibreOffice headless -> PDF -> pdftoppm -> PNG
  PDF   -> pdftoppm -> PNG
  DOCX  -> LibreOffice headless -> PDF -> pdftoppm -> PNG

Usage: python tools/render_visual_qa.py --phase phase13s [--dpi 110] [--only <glob>]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)


def which(tool):
    return shutil.which(tool)


def safe(name):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def render_pdf_to_png(pdf, out_prefix, dpi):
    ensure_dir(os.path.dirname(out_prefix))
    r = sh(f'pdftoppm -png -r {dpi} "{pdf}" "{out_prefix}"')
    if r.returncode != 0:
        print(f"  !! pdftoppm failed for {pdf}: {r.stderr[:300]}")
        return []
    return sorted(f for f in os.listdir(os.path.dirname(out_prefix))
                  if f.startswith(os.path.basename(out_prefix)) and f.endswith(".png"))


def convert_to_pdf(src, outdir):
    ensure_dir(outdir)
    r = sh(f'soffice --headless --convert-to pdf --outdir "{outdir}" "{src}"')
    if r.returncode != 0:
        print(f"  !! soffice failed for {src}: {r.stderr[:300]}")
        return None
    base = os.path.splitext(os.path.basename(src))[0] + ".pdf"
    p = os.path.join(outdir, base)
    return p if os.path.exists(p) else None


def contact_sheet(pngs, out_path, cols=4, thumb_w=640):
    from PIL import Image
    if not pngs:
        return
    imgs = []
    for p in pngs:
        try:
            im = Image.open(p)
            w, h = im.size
            nw = thumb_w
            nh = max(1, int(h * thumb_w / w))
            imgs.append(im.resize((nw, nh)))
        except Exception as e:
            print(f"  !! cannot open {p}: {e}")
    if not imgs:
        return
    pad = 12
    label_h = 20
    rows = (len(imgs) + cols - 1) // cols
    cell_w = thumb_w + pad
    cell_h = max(im.height for im in imgs) + label_h + pad
    sheet = Image.new("RGB", (cols * cell_w + pad, rows * cell_h + pad), "white")
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        x = pad + c * cell_w
        y = pad + r * cell_h
        sheet.paste(im, (x, y + label_h))
        d.text((x, y), os.path.basename(pngs[i]), fill="black")
    sheet.save(out_path)
    print(f"  contact sheet -> {out_path} ({len(imgs)} images)")


def discover_artifacts():
    """Return dict of lists of active artifacts."""
    decks = sorted(glob_slides())
    pdfs = sorted(glob_pdfs())
    docxs = sorted(glob_docxs())
    return {"ppt": decks, "pdf": pdfs, "docx": docxs}


def glob_slides():
    import glob
    return glob.glob(os.path.join(ROOT, "production", "slides", "*.pptx"))


def glob_pdfs():
    import glob
    dirs = [
        "production/releases",
        "production/premium-notes",
        "production/activities",
        "production/labs",
        "production/quizzes",
        "production/review",
        "production/lab-setup-guides",
        "production/rubrics",
    ]
    out = []
    for d in dirs:
        out += glob.glob(os.path.join(ROOT, d, "**", "*.pdf"), recursive=True)
    return out


def glob_docxs():
    import glob
    dirs = [
        "production/premium-notes",
        "production/worksheets",
        "production/labs",
        "production/activities",
        "production/quizzes",
        "production/student-notebook",
        "production/review",
        "production/lab-setup-guides",
        "production/rubrics",
    ]
    out = []
    for d in dirs:
        out += glob.glob(os.path.join(ROOT, d, "**", "*.docx"), recursive=True)
    return out


def sha256_short(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def extract_pptx_typography(path):
    """Extract min/max font sizes per slide for typography audit."""
    from pptx import Presentation
    from pptx.util import Pt
    prs = Presentation(path)
    slides = []
    for idx, slide in enumerate(prs.slides, 1):
        sizes = []
        texts = []
        for shp in slide.shapes:
            if shp.has_text_frame:
                for para in shp.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.size is not None:
                            sizes.append(run.font.size.pt)
                        if run.text.strip():
                            texts.append(run.text.strip())
                    if para.text.strip() and not any(r.text for r in para.runs):
                        texts.append(para.text.strip())
        slides.append({
            "slide": idx,
            "min_pt": round(min(sizes), 1) if sizes else None,
            "max_pt": round(max(sizes), 1) if sizes else None,
            "n_text_chars": sum(len(t) for t in texts),
        })
    return slides


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="phase13s")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--only", default=None, help="substring filter for filenames")
    ap.add_argument("--skip-pdf", action="store_true")
    ap.add_argument("--skip-docx", action="store_true")
    ap.add_argument("--skip-ppt", action="store_true")
    args = ap.parse_args()

    for tool in ("soffice", "pdftoppm"):
        if not which(tool):
            print(f"FATAL: {tool} not on PATH"); sys.exit(1)

    base = os.path.join(ROOT, "qa", "temp", args.phase)
    render_dir = os.path.join(base, "render")
    contact_dir = os.path.join(base, "contact")
    pdf_tmp = os.path.join(base, "pdf_tmp")
    ensure_dir(render_dir)
    ensure_dir(contact_dir)
    ensure_dir(pdf_tmp)

    arts = discover_artifacts()
    manifest = {"phase": args.phase, "dpi": args.dpi, "artifacts": []}

    def matches(path):
        return (args.only is None) or (args.only.lower() in os.path.basename(path).lower())

    tasks = []
    if not args.skip_ppt:
        tasks += [("ppt", p) for p in arts["ppt"] if matches(p)]
    if not args.skip_pdf:
        tasks += [("pdf", p) for p in arts["pdf"] if matches(p)]
    if not args.skip_docx:
        tasks += [("docx", p) for p in arts["docx"] if matches(p)]

    print(f"Rendering {len(tasks)} artifacts ({sum(1 for t,_ in tasks if t=='ppt')} decks, "
          f"{sum(1 for t,_ in tasks if t=='pdf')} pdfs, {sum(1 for t,_ in tasks if t=='docx')} docx) @ {args.dpi} dpi")

    for kind, path in tasks:
        name = os.path.basename(path)
        stem = safe(os.path.splitext(name)[0])
        print(f"[{kind}] {name}")
        rec = {"kind": kind, "file": name, "rel": os.path.relpath(path, ROOT),
               "sha256": sha256_short(path)}

        if kind == "ppt":
            pdf = convert_to_pdf(path, pdf_tmp)
            if not pdf:
                rec["status"] = "CONVERT_FAIL"; manifest["artifacts"].append(rec); continue
            pngs = render_pdf_to_png(pdf, os.path.join(render_dir, stem, "slide"), args.dpi)
            rec["pages"] = len(pngs)
            rec["typography"] = extract_pptx_typography(path)
            rec["status"] = "OK"
            contact_sheet([os.path.join(render_dir, stem, p) for p in pngs],
                          os.path.join(contact_dir, stem + "_contact.png"))
        else:
            pdf = None
            if kind == "pdf":
                pdf = path
            else:  # docx -> pdf
                pdf = convert_to_pdf(path, pdf_tmp)
            if not pdf:
                rec["status"] = "CONVERT_FAIL"; manifest["artifacts"].append(rec); continue
            pngs = render_pdf_to_png(pdf, os.path.join(render_dir, stem, "page"), args.dpi)
            rec["pages"] = len(pngs)
            rec["status"] = "OK"
            contact_sheet([os.path.join(render_dir, stem, p) for p in pngs],
                          os.path.join(contact_dir, stem + "_contact.png"))

        manifest["artifacts"].append(rec)

    with open(os.path.join(base, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    ok = sum(1 for a in manifest["artifacts"] if a["status"] == "OK")
    fail = len(manifest["artifacts"]) - ok
    print(f"\nDone. OK={ok} FAIL={fail}  manifest={os.path.join(base,'manifest.json')}")


if __name__ == "__main__":
    main()
