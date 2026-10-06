"""Compare current Chapter 2 PDFs with a fresh export of the canonical source.

A notes PDF swapped for the key, a blank key, or a stale slides PDF fails.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapter_text import norm_line

PAIRS = [
    ("guided notes", "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx",
     "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.pdf"),
    ("guided notes key", "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes-key.docx",
     "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes-key.pdf"),
    ("slides", "production/slides/02-ch2-moving-objects-have-energy-slides.pptx",
     "production/slides/02-ch2-moving-objects-have-energy-slides.pdf"),
    ("quiz", "production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx",
     "production/quizzes/02-ch2-moving-objects-have-energy-quiz.pdf"),
    ("practice", "production/worksheets/02-ch2-moving-objects-have-energy-practice.docx",
     "production/worksheets/02-ch2-moving-objects-have-energy-practice.pdf"),
    ("moving marbles", "production/worksheets/02-ch2-moving-marbles-student.docx",
     "production/worksheets/02-ch2-moving-marbles-student.pdf"),
    ("friday flex", "production/worksheets/02-ch2-friday-flex.docx",
     "production/releases/chapter-02/02-ch2-friday-flex.pdf"),
    ("recovery", "production/worksheets/02-ch2-absent-student-recovery.docx",
     "production/worksheets/02-ch2-absent-student-recovery.pdf"),
    ("playbook", "production/teacher-playbook/unit1-teacher-playbook.docx",
     "production/teacher-playbook/unit1-teacher-playbook.pdf"),
]


def _pages(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    n = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
    return n, (size.group(1), size.group(2)) if size else ("", "")


def _text(path):
    n, _size = _pages(path)
    pages = []
    for i in range(1, n + 1):
        raw = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", path, "-"],
                             capture_output=True, text=True).stdout
        pages.append(norm_line(raw))
    return pages


def _export(src, dest_pdf):
    work = tempfile.mkdtemp(prefix="ch2fresh_")
    prof = tempfile.mkdtemp(prefix="lo_fresh_")
    try:
        subprocess.run(["soffice", "--headless", "--norestore", "-env:UserInstallation=file://" + prof,
                        "--convert-to", "pdf", "--outdir", work, src],
                       check=True, capture_output=True, text=True, timeout=180)
        produced = [f for f in os.listdir(work) if f.endswith(".pdf")]
        if len(produced) != 1:
            raise RuntimeError("expected one pdf, got %s" % produced)
        shutil.copy2(os.path.join(work, produced[0]), dest_pdf)
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(prof, ignore_errors=True)


def check_pair(root, name, src_rel, pdf_rel):
    src = os.path.join(root, src_rel)
    pdf = os.path.join(root, pdf_rel)
    if not os.path.exists(src) or not os.path.exists(pdf):
        return ["FRESH missing %s" % name]
    fresh = tempfile.mktemp(suffix=".pdf")
    try:
        _export(src, fresh)
        live_pages, live_size = _pages(pdf)
        new_pages, new_size = _pages(fresh)
        fails = []
        if live_pages != new_pages:
            fails.append("FRESH %s page count %s != fresh %s" % (name, live_pages, new_pages))
        if live_size != new_size:
            fails.append("FRESH %s page size %s != %s" % (name, live_size, new_size))
        live = _text(pdf)
        new = _text(fresh)
        for i, (a, b) in enumerate(zip(live, new), 1):
            if a != b:
                fails.append("FRESH %s page %d text does not match a fresh export" % (name, i))
                break
        return fails
    finally:
        if os.path.exists(fresh):
            os.remove(fresh)


def check(root, only=None):
    fails = []
    for name, src, pdf in PAIRS:
        if only and name != only:
            continue
        fails.extend(check_pair(root, name, src, pdf))
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    root = os.path.abspath(a.root or os.path.join(os.path.dirname(__file__), ".."))
    fails = check(root, a.only)
    if fails:
        for f in fails:
            print("[FAIL]", f)
        sys.exit(1)
    print("[PASS] fresh exports match current PDFs")
    sys.exit(0)


if __name__ == "__main__":
    main()
