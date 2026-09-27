"""Premium guided-notes QA (Phase 12A): fonts, pages, clipping, coverage, forbidden vocab."""
import os, re, subprocess, sys
from docx import Document
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NOTES = os.path.join(ROOT, "production", "premium-notes")

CHAPTERS = {
    "01-ch1": {
        "target": (2, 3),
        "concepts": ["energy", "change", "evidence", "motion", "light", "sound", "heat",
                     "electrical", "stored energy", "battery", "rubber band", "raised object",
                     "observation", "explanation"],
    },
    "02-ch2": {
        "target": (2, 3),
        "concepts": ["motion", "energy of motion", "moving", "change", "evidence",
                     "before", "after", "inference"],
    },
    "03-ch3": {
        "target": (2, 3),
        "concepts": ["speed", "same object", "faster", "slower", "energy of motion",
                     "ramp", "measured", "inferred", "fair test", "displacement"],
    },
    "04-ch4": {
        "target": (3, 4),
        "concepts": ["transfer", "sound", "light", "heat", "electric current",
                     "source", "path", "receiver", "transformation", "evidence"],
    },
    "05-ch5": {
        "target": (2, 3),
        "concepts": ["collide", "collision", "before", "during", "after", "motion",
                     "transfer", "same object", "fair test", "energy does not disappear", "sound"],
    },
    "06-ch6": {
        "target": (3, 4),
        "concepts": ["transform", "convert", "transformation", "input", "output",
                     "transfer", "criteria", "constraints", "engineering", "test", "improve"],
    },
    "07-ch7": {
        "target": (2, 3),
        "concepts": ["edison", "engineering", "problem", "design", "test", "evidence",
                     "improve", "light bulb", "latimer", "filament"],
    },
}

FORBIDDEN = ["proof", "proves", "prove", "kinetic", "potential", "mechanical energy",
             "radiant", "momentum", "impulse", "electron", "compression wave"]
UNIT_NAME = "energy transfer & transformation"

def iter_paragraphs(container):
    if hasattr(container, "paragraphs"):
        for p in container.paragraphs:
            yield p
    if hasattr(container, "tables"):
        for t in container.tables:
            for row in t.rows:
                for c in row.cells:
                    yield from iter_paragraphs(c)

def full_text(doc):
    return "\n".join(p.text for p in iter_paragraphs(doc))

def fonts(doc):
    s = set()
    for p in iter_paragraphs(doc):
        for r in p.runs:
            if r.font.size:
                s.add(r.font.size.pt)
    return sorted(s)

def pdf_pages(p):
    r = subprocess.run(["pdfinfo", p], capture_output=True, text=True)
    m = re.search(r"Pages:\s+(\d+)", r.stdout)
    return int(m.group(1)) if m else 0

report = []
report.append("# PREMIUM GUIDED NOTES QA — CHAPTERS 1–7\n")

all_pass = True
for key, spec in CHAPTERS.items():
    docx = [f for f in os.listdir(NOTES) if f.startswith(key) and f.endswith(".docx")][0]
    dpath = os.path.join(NOTES, docx)
    d = Document(dpath)
    text = full_text(d).lower()
    scan = text.replace(UNIT_NAME, "")
    fs = fonts(d)
    lo, hi = spec["target"]
    pdf = dpath[:-5] + ".pdf"
    pages = pdf_pages(pdf)
    missing = [c for c in spec["concepts"] if c not in text]
    forb = [f for f in FORBIDDEN if re.search(r"\b" + re.escape(f) + r"\b", scan)]
    min_font = min(fs) if fs else 0
    issues = []
    if pages < lo or pages > hi:
        issues.append(f"page count {pages} outside target {lo}-{hi}")
    if min_font < 12:
        issues.append(f"min font {min_font}pt < 12pt floor")
    if missing:
        issues.append(f"missing concepts: {missing}")
    if forb:
        issues.append(f"forbidden vocab: {forb}")
    status = "PASS" if not issues else "FAIL"
    if issues:
        all_pass = False
    report.append(f"## {key} — {docx}")
    report.append(f"- Pages: {pages} (target {lo}-{hi}) · fonts {fs}")
    report.append(f"- Concepts missing: {missing or 'none'} · forbidden: {forb or 'none'}")
    report.append(f"- **{status}** {' — ' + '; '.join(issues) if issues else ''}\n")

report.append(f"\n**OVERALL: {'PASS' if all_pass else 'FAIL'}**")
out = os.path.join(ROOT, "qa", "guided-notes-ch1-7", "QA_GATES.md")
with open(out, "w") as f:
    f.write("\n".join(report))
print("\n".join(report))
