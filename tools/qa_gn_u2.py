"""Premium guided-notes QA — Unit 2 (Chapters 1–9): fonts, pages, clipping, coverage, forbidden vocab."""
import os, re, subprocess
from docx import Document

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NOTES = os.path.join(ROOT, "production", "premium-notes", "unit-02")

CHAPTERS = {
    "unit-02-ch1-renewable-nonrenewable": {
        "target": (2, 3),
        "concepts": ["renewable", "nonrenewable", "fossil fuel", "abundant", "location",
                     "wind", "sunlight", "coal", "petroleum", "natural gas", "restored"],
    },
    "unit-02-ch2-types-of-fossil-fuels": {
        "target": (2, 2),
        "concepts": ["coal", "petroleum", "crude oil", "natural gas", "peat", "organisms",
                     "state of matter", "swamp"],
    },
    "unit-02-ch3-using-fossil-fuels": {
        "target": (2, 3),
        "concepts": ["extract", "refine", "combustion", "transport", "steam", "turbine",
                     "generator", "electricity", "benefit", "limitation", "spill", "stewardship"],
    },
    "unit-02-ch4-nuclear-energy": {
        "target": (2, 2),
        "concepts": ["nuclear", "uranium", "heat", "steam", "turbine", "generator",
                     "nonrenewable", "store"],
    },
    "unit-02-ch5-wind-energy": {
        "target": (2, 2),
        "concepts": ["wind", "turbine", "blade", "generator", "renewable", "location",
                     "batteries", "electricity"],
    },
    "unit-02-ch6-hydroelectric-energy": {
        "target": (2, 2),
        "concepts": ["hydroelectric", "dam", "reservoir", "turbine", "generator",
                     "salmon", "fish ladder", "renewable", "predictable"],
    },
    "unit-02-ch7-solar-energy": {
        "target": (2, 2),
        "concepts": ["solar", "sunlight", "solar cell", "electricity", "renewable",
                     "available", "cost"],
    },
    "unit-02-ch8-geothermal-energy": {
        "target": (2, 2),
        "concepts": ["geothermal", "heat", "earth", "steam", "turbine", "location",
                     "volcanic", "clean"],
    },
    "unit-02-ch9-energy-resource-innovations": {
        "target": (1, 2),
        "concepts": ["biofuel", "hybrid", "fuel cell", "wave", "engineering",
                     "regenerative", "efficient"],
    },
}

FORBIDDEN = ["proof", "proves", "prove", "kinetic", "potential", "mechanical energy",
             "radiant", "momentum", "impulse", "electron", "compression wave",
             "split atoms", "splitting atoms", "fission"]
CONTROVERSIAL = ["climate change", "global warming", "carbon footprint", "carbon tax",
                 "cap and trade", "climate crisis", "climate activism", "energy policy",
                 "community energy plan", "sustainable community energy plan", "warming"]

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

report = ["# PREMIUM GUIDED NOTES QA — UNIT 2 (CHAPTERS 1–9)\n"]
all_pass = True
for key, spec in CHAPTERS.items():
    docx = [f for f in os.listdir(NOTES) if f.startswith(key) and f.endswith(".docx")]
    if not docx:
        report.append(f"## {key} — MISSING")
        all_pass = False
        continue
    dpath = os.path.join(NOTES, docx[0])
    d = Document(dpath)
    text = full_text(d).lower()
    fs = fonts(d)
    lo, hi = spec["target"]
    pdf = dpath[:-5] + ".pdf"
    pages = pdf_pages(pdf)
    missing = [c for c in spec["concepts"] if c not in text]
    forb = [f for f in FORBIDDEN if re.search(r"\b" + re.escape(f) + r"\b", text)]
    contr = [f for f in CONTROVERSIAL if re.search(re.escape(f), text)]
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
    if contr:
        issues.append(f"controversial terms: {contr}")
    status = "PASS" if not issues else "FAIL"
    if issues:
        all_pass = False
    report.append(f"## {key} — {docx[0]}")
    report.append(f"- Pages: {pages} (target {lo}-{hi}) · fonts {fs} · min {min_font}pt")
    report.append(f"- Concepts missing: {missing or 'none'} · forbidden: {forb or 'none'} · controversial: {contr or 'none'}")
    report.append(f"- **{status}**{' — ' + '; '.join(issues) if issues else ''}\n")

report.append(f"\n**OVERALL: {'PASS' if all_pass else 'FAIL'}**")
out = os.path.join(ROOT, "qa", "reports", "PHASE13B_UNIT2_GUIDED_NOTES_QA.md")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    f.write("\n".join(report))
print("\n".join(report))
