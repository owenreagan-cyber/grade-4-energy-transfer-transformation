"""Premium guided notes — Chapter 5: Collisions Transfer Energy (2 pages)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "05-ch5-collisions-transfer-energy-guided-notes.docx"))

doc = new_doc()

# ---------------- PAGE 1 ----------------
title_block(doc, "Collisions Transfer Energy", "Chapter 5 Guided Notes · Grade 4 Energy Transfer & Transformation")
big_question(doc, "How is energy involved in collisions?")

heading(doc, "Key Words")
fill(doc, "collide — To collide is when two objects", "________________", "with impact (make contact).")
fill(doc, "collision — A collision happens when two objects", "________________", "with impact.")

heading(doc, "Model It")
body(doc, "In a collision, a moving object's energy of motion can transfer to the other object. Energy does NOT disappear.", size=12, italic=True, color=GRAY, after=30)
model_stack(doc, ["COLLISION", "MOTION CAN CHANGE", "ENERGY CAN TRANSFER", "ENERGY DOES NOT DISAPPEAR"], size=13)

heading(doc, "Draw / Label — Before · During · After")
body(doc, "Draw the two cars BEFORE, DURING, and AFTER they collide. Use arrows to show motion.", size=12, color=GRAY, after=20)
t = doc.add_table(rows=1, cols=3)
no_table_borders(t)
for idx, lab in enumerate(["BEFORE", "DURING", "AFTER"]):
    c = t.cell(0, idx)
    set_cell_width(c, 2300)
    set_cell_margins(c, top=20, left=40, bottom=20, right=40)
    set_cell_border(c, top=dict(sz=8, val='single', color=NAVY_HEX),
                    left=dict(sz=8, val='single', color=NAVY_HEX),
                    bottom=dict(sz=8, val='single', color=NAVY_HEX),
                    right=dict(sz=8, val='single', color=NAVY_HEX))
    cp = c.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(cp.add_run(lab), size=13, bold=True, color=CORAL, caps=True)
set_row_height(t.rows[0], 2600, rule='exact')

# ---------------- PAGE 2 ----------------
title_block(doc, "Evidence + Fair Test", "Chapter 5 Guided Notes · Page 2", new_page=True)

heading(doc, "What Changes in a Collision?")
body(doc, "List the changes a collision can cause, with an example from our Crash Lab.", size=12, color=GRAY, after=20)
data_table(doc, ["Change", "Example from our Crash Lab"],
           [("motion (speed or direction)", ""),
            ("shape", ""),
            ("sound", "")],
           col_widths=[3600, 3600], row_h=620)

heading(doc, "Fair Test")
body(doc, "A fair test changes ONE thing at a time. Compare the SAME object at different speeds.", size=12, color=GRAY, after=20)
fill(doc, "Part A — the ONE thing we changed was", "________________", "(the SAME car).", size=13)

heading(doc, "Crash Lab Evidence")
data_table(doc, ["SAME car, ramp height", "Target displacement (cm)"],
           [("low (slower)", ""), ("high (faster)", "")],
           col_widths=[3600, 3600], row_h=640)
body(doc, "The faster the SAME car moved, the ______ the target moved. That change is evidence of MORE energy of motion.", size=13, bold=True, after=30)

heading(doc, "Check Your Thinking")
body(doc, "After a crash, the cars stop. Did the energy disappear? Explain using motion and sound.", size=13, bold=True, after=30)
wline(doc, 1, gap=30, after=18)

connect(doc, "Chapter 1 → 5: energy causes change; a collision transfers energy and makes sound.")

doc.save(OUT)
print("saved", OUT)
