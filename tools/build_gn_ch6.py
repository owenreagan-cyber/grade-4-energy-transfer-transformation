"""Premium guided notes — Chapter 6: Energy Transformations (4 pages)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "06-ch6-energy-transformations-guided-notes.docx"))

doc = new_doc()

# ---------------- PAGE 1 ----------------
title_block(doc, "Energy Transformations", "Chapter 6 Guided Notes · Grade 4 Energy Transfer & Transformation")
big_question(doc, "How do energy transformations help people?")

heading(doc, "Key Words")
fill(doc, "transform / convert — To transform energy is to change it", "________________",
     "one form to another.", size=13)
fill(doc, "energy transformation — Energy transformation is when energy", "________________",
     "form.", size=13)

heading(doc, "Key Idea")
key_idea(doc, "Transformation = energy CHANGES FORM.  Transfer = energy MOVES.  BOTH can happen together.")

heading(doc, "Model It")
body(doc, "A device takes energy in, changes its form, and gives a useful output.", size=12, italic=True, color=GRAY, after=30)
model_boxes(doc, ["INPUT", "TRANSFORMATION", "OUTPUT"], box_w=2400, arr_w=620, size=13)

heading(doc, "Quick Check")
body(doc, "Name one device that transforms energy, and tell what form it changes into.", size=13, bold=True, after=20)
wline(doc, 1, gap=30, after=18)

# ---------------- PAGE 2 ----------------
title_block(doc, "Trace the Energy", "Chapter 6 Guided Notes · Page 2", new_page=True)

heading(doc, "Device Systems")
body(doc, "For each device, write the input, the change in form, and the output.", size=12, color=GRAY, after=20)
data_table(doc, ["Device", "INPUT", "TRANSFORMATION", "OUTPUT / CHANGE"],
           [("flashlight", "battery (stored)", "electrical → light", ""),
            ("buzzer", "", "", ""),
            ("motor", "", "", ""),
            ("wind-up toy", "", "", "")],
           col_widths=[1900, 1900, 1900, 1900], row_h=640)

heading(doc, "Transfer vs Transformation vs BOTH")
body(doc, "Sort each system. Some are BOTH.", size=12, color=GRAY, after=20)
data_table(doc, ["System", "TRANSFER", "TRANSFORMATION", "BOTH"],
           [("falling dominoes", "", "", ""),
            ("battery → flashlight → light", "", "", ""),
            ("warm water → cooler spoon", "", "", "")],
           col_widths=[2600, 1500, 1500, 1500], row_h=560)

# ---------------- PAGE 3 ----------------
title_block(doc, "Engineering Design", "Chapter 6 Guided Notes · Page 3", new_page=True)

heading(doc, "Problem, Criteria, Constraints")
fill(doc, "Problem — something we need to", "________________", size=13)
fill(doc, "Criteria — the things a good design", "________________", size=13)
fill(doc, "Constraints — the things that", "________________", "what we can use.", size=13)

heading(doc, "Engineering Cycle")
body(doc, "Engineers design, build, test, and improve. Test results — even failures — are useful evidence.", size=12, italic=True, color=GRAY, after=30)
model_stack(doc, ["PROBLEM", "DESIGN", "TEST", "EVIDENCE", "IMPROVE"], size=13)

heading(doc, "My Blueprint")
body(doc, "Sketch your Tabletop Alert / Signal Device. Label the energy pathway.", size=12, color=GRAY, after=20)
draw_box(doc, FULL_W, 2100, "draw and label your device blueprint")

# ---------------- PAGE 4 ----------------
title_block(doc, "Test → Change → Retest", "Chapter 6 Guided Notes · Page 4", new_page=True)

heading(doc, "Test 1 vs Test 2")
data_table(doc, ["Test 1 — what happened?", "What I changed (and WHY)", "Test 2 — what happened?"],
           [("", "", ""),
            ("", "", "")],
           col_widths=[2400, 2400, 2400], row_h=760)

heading(doc, "Draw Your Improved Design")
draw_box(doc, FULL_W, 2000, "draw the change you made to your device")

heading(doc, "Check Your Thinking")
body(doc, "Your first design did not work well. Explain why that is useful evidence, not a failure.", size=13, bold=True, after=30)
wline(doc, 2, gap=30, after=18)

connect(doc, "Chapter 1 → 6: energy causes change; devices transform energy to solve problems people have.")

doc.save(OUT)
print("saved", OUT)
