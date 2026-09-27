"""Premium guided notes — Chapter 2: Moving Objects Have Energy (2 pages)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "02-ch2-moving-objects-have-energy-guided-notes.docx"))

doc = new_doc()

# ---------------- PAGE 1 ----------------
title_block(doc, "Moving Objects Have Energy", "Chapter 2 Guided Notes · Grade 4 Energy Transfer & Transformation")
big_question(doc, "How are energy, change, and movement of objects related?")

heading(doc, "Notice")
body(doc, "In our marble demo, write what happened when the moving marble reached the target.", size=12, color=GRAY, after=20)
wline(doc, 2, gap=30, after=18)

heading(doc, "Key Words")
fill(doc, "motion — Motion is the process of an object changing", trail=".")
fill(doc, "energy of motion — Energy of motion is the energy an object has", "________________", "it is moving.")

heading(doc, "Model It")
body(doc, "A moving object can cause another object to change. The change is our evidence.", size=12, italic=True, color=GRAY, after=30)
model_boxes(doc, ["MOVING OBJECT", "CAUSES CHANGE", "EVIDENCE OF ENERGY"], box_w=2060, arr_w=560, size=12)

heading(doc, "Draw / Label")
body(doc, "Draw the marble before and after it hits the target. Use arrows to show the direction of motion.", size=12, color=GRAY, after=20)
labeled_pair(doc, "BEFORE", "AFTER", height_dxa=2000, left_hint="marble rolls toward target", right_hint="target moves after contact")
fill(doc, "What changed?", "________________________________________________", size=12)

# ---------------- PAGE 2 ----------------
title_block(doc, "Evidence + Lab Connection", "Chapter 2 Guided Notes · Page 2", new_page=True)

heading(doc, "Observation vs Inference")
body(doc, "Observation = what I saw.      Inference = what I think it means.", size=12, color=GRAY, after=20)
data_table(doc, ["Observation (what I saw)", "Inference (what I think)"],
           [("The target marble moved.", "The moving marble had energy."),
            ("", "")],
           col_widths=[3600, 3600], row_h=660)

heading(doc, "Example / Non-Example")
data_table(doc, ["Shows energy of motion (example)", "Does NOT (non-example)"],
           [("", ""), ("", "")],
           col_widths=[3600, 3600], row_h=660)

heading(doc, "Lab Connection — Moving Marbles")
body(doc, "Record one thing you observed and the evidence it gives.", size=12, color=GRAY, after=20)
data_table(doc, ["What I observed", "Evidence that the moving object had energy"],
           [("", "")],
           col_widths=[3600, 3600], row_h=700)

heading(doc, "Check Your Thinking")
body(doc, "How do we know a moving object has energy, even though we cannot see the energy?", size=13, bold=True, after=30)
wline(doc, 2, gap=30, after=18)

connect(doc, "Chapter 1 → 2: energy can cause change; a moving object is one thing that has energy.")

doc.save(OUT)
print("saved", OUT)
