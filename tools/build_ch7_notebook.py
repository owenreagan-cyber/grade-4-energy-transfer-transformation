"""Build Chapter 7 interactive notebook (2-3 inserts) as DOCX."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ch4_common import *
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = "production/student-notebook/chapter-07/07-ch7-interactive-notebook.docx"

doc = Document()
setup_portrait(doc)

title(doc, "Interactive Science Notebook", "Chapter 7 — Solving Problems and Designing Solutions: Thomas A. Edison")
add_par(doc, "Unit close • Week 9 • 3 inserts", size=11, italic=True, color=GRAY, space_after=8)
name_date(doc)

# ---------------- INSERT 1 ----------------
section(doc, "INSERT 1 — ENGINEERING IS A CYCLE")
prompt(doc, "Cut out and glue this cycle into your notebook. Then add your own examples.")
cyc = doc.add_table(rows=5, cols=1)
for i, step in enumerate(["PROBLEM", "DESIGN", "TEST", "EVIDENCE", "IMPROVE"]):
    cell = cyc.rows[i].cells[0]
    set_cell_text(cell, step, size=14, bold=True, color=RGBColor(0xFF,0xFF,0xFF), align=WD_ALIGN_PARAGRAPH.CENTER)
    shade_cell(cell, "2E6E8E")
add_par(doc, "", space_after=2)
prompt(doc, "One example from Edison's work:")
answer_lines(doc, 2)
prompt(doc, "One example from my own tabletop device:")
answer_lines(doc, 2)

# ---------------- INSERT 2 ----------------
page_break(doc)
section(doc, "INSERT 2 — ENERGY UNIT CONCEPT MAP")
prompt(doc, "Center: ENERGY.  Branches: causes change · motion · speed · transfer · collisions · transformation · engineering.")
prompt(doc, "Add ONE example or piece of evidence under each branch.")
table = doc.add_table(rows=8, cols=2)
style_table(table, header_shade="1F3A5F")
hdr = table.rows[0].cells
set_cell_text(hdr[0], "Branch", size=12, bold=True, color=RGBColor(0xFF,0xFF,0xFF))
set_cell_text(hdr[1], "My example / evidence", size=12, bold=True, color=RGBColor(0xFF,0xFF,0xFF))
branches = ["causes change", "motion", "speed", "transfer", "collisions", "transformation", "engineering"]
for i, b in enumerate(branches):
    row = table.rows[i+1].cells
    set_cell_text(row[0], b, size=11, bold=True)
    set_cell_text(row[1], "", size=11)
    row[1].width = Inches(4.4)
    # add writing space
    row[1]._tc.get_or_add_tcPr()

# ---------------- INSERT 3 ----------------
page_break(doc)
section(doc, "INSERT 3 — UNIT REFLECTION")
prompt(doc, "Finish these sentences with your own ideas.")
prompts = [
    "Something I can explain now:",
    "A lab that gave strong evidence:",
    "One engineering change that improved a design:",
    "One question I still have:",
]
for p in prompts:
    add_par(doc, p, size=12, bold=True, space_before=6, space_after=0)
    answer_lines(doc, 2)

add_par(doc, "", space_after=4)
add_par(doc, "Provenance: CUSTOM (engineering cycle + unit concept map + reflection scaffolds). "
             "Content: SOURCE-aligned (Reader Ch.7 pp.37-42; TG pp.94-98).",
        size=9, italic=True, color=GRAY)

doc.save(OUT)
print("wrote", OUT)
