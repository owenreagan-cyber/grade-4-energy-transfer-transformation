"""Premium guided notes — Chapter 7: Thomas Edison + Unit Synthesis (3 pages)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "07-ch7-edison-unit-synthesis-guided-notes.docx"))

doc = new_doc()

# ---------------- PAGE 1 ----------------
title_block(doc, "Solving Problems and Designing Solutions: Thomas A. Edison",
            "Chapter 7 Guided Notes · Grade 4 Energy Transfer & Transformation")
big_question(doc, "How did Thomas Edison use his knowledge of energy transfer and transformation to solve problems?")

heading(doc, "Key Idea")
key_idea(doc, "Engineering is iterative: PROBLEM → DESIGN → TEST → EVIDENCE → IMPROVE. Failure is information.")

heading(doc, "Edison's Light-Bulb Work")
body(doc, "Source-supported facts. Read each, then write what you learned.", size=12, color=GRAY, after=20)
data_table(doc, ["Fact", "What I learned"],
           [("Edison did NOT invent the first light bulb — he IMPROVED earlier designs.", ""),
            ("His team tested more than 6,000 materials for the filament.", ""),
            ("In 1879 he used a bamboo + carbon filament that lasted longer.", ""),
            ("Lewis Latimer improved the bulb too (wire-to-filament + stronger filament).", "")],
           col_widths=[4200, 3000], row_h=720)

# ---------------- PAGE 2 ----------------
title_block(doc, "The Engineering Cycle", "Chapter 7 Guided Notes · Page 2", new_page=True)

heading(doc, "Model It")
model_stack(doc, ["PROBLEM", "DESIGN", "TEST", "EVIDENCE", "IMPROVE"], size=13)

heading(doc, "Fill the Cycle")
body(doc, "Trace the cycle with Edison's light-bulb work AND with your own device.", size=12, color=GRAY, after=20)
data_table(doc, ["Step", "Edison's example", "My device"],
           [("Problem", "light bulbs did not last or were not practical", ""),
            ("Design", "", ""),
            ("Test", "", ""),
            ("Evidence", "", ""),
            ("Improve", "", "")],
           col_widths=[1400, 3000, 3000], row_h=640)

# ---------------- PAGE 3 ----------------
title_block(doc, "Unit Concept Map", "Chapter 7 Guided Notes · Page 3", new_page=True)

heading(doc, "Connect the Whole Unit")
body(doc, "Energy is the ability to cause change. Draw arrows to connect each idea to ENERGY.", size=12, color=GRAY, after=20)
ct = doc.add_table(rows=3, cols=3)
no_table_borders(ct)
branch_w = 2100
labels = {4: "ENERGY",
          0: "change", 2: "motion", 6: "speed",
          8: "transfer", 3: "collisions", 5: "transformation",
          1: "stored energy", 7: "engineering"}
for i in range(3):
    for j in range(3):
        c = ct.cell(i, j)
        set_cell_width(c, branch_w)
        set_cell_margins(c, top=30, left=30, bottom=30, right=30)
        set_cell_border(c, top=dict(sz=8, val='single', color=NAVY_HEX),
                        left=dict(sz=8, val='single', color=NAVY_HEX),
                        bottom=dict(sz=8, val='single', color=NAVY_HEX),
                        right=dict(sz=8, val='single', color=NAVY_HEX))
        cp = c.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        lab = labels.get(i * 3 + j, "")
        if lab == "ENERGY":
            shade_cell(c, NAVY_HEX)
            set_run(cp.add_run(lab), size=13, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        else:
            set_run(cp.add_run(lab), size=12, bold=True, color=NAVY)
set_row_height(ct.rows[0], 1100, rule='exact')
set_row_height(ct.rows[1], 1100, rule='exact')
set_row_height(ct.rows[2], 1100, rule='exact')
sp = doc.add_paragraph(); spPr = sp._p.get_or_add_pPr()
se = OxmlElement('w:spacing'); se.set(qn('w:after'), '30'); spPr.append(se)

heading(doc, "Check Your Thinking")
body(doc, "Write one sentence that connects energy, change, and engineering using the whole unit.", size=13, bold=True, after=30)
wline(doc, 3, gap=30, after=18)

connect(doc, "Unit synthesis: energy causes change → motion & speed → transfer & collisions → transformation → engineering.")

doc.save(OUT)
print("saved", OUT)
