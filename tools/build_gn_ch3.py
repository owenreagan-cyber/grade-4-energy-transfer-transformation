"""Premium guided notes — Chapter 3: Energy and Speed Are Related (3 pages)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "03-ch3-energy-speed-guided-notes.docx"))

doc = new_doc()

# ---------------- PAGE 1 ----------------
title_block(doc, "Energy and Speed Are Related", "Chapter 3 Guided Notes · Grade 4 Energy Transfer & Transformation")
big_question(doc, "How are energy and speed related?")

heading(doc, "Key Words")
fill(doc, "speed — Speed is a measurement of the", "________________", "an object travels over an amount of time.")

heading(doc, "Key Idea")
key_idea(doc, "For the SAME object, faster motion means MORE energy of motion than slower motion.")

heading(doc, "Model It")
body(doc, "We compare the SAME object moving faster and slower. A greater change is evidence of more energy of motion.", size=12, italic=True, color=GRAY, after=30)
model_boxes(doc, ["SAME OBJECT · FASTER", "GREATER CHANGE", "MORE ENERGY OF MOTION"], box_w=2060, arr_w=520, size=12)

heading(doc, "Draw / Label")
body(doc, "Draw the same ball at a LOW ramp and a HIGH ramp. Show which rolls away faster.", size=12, color=GRAY, after=20)
labeled_pair(doc, "LOW RAMP (slower)", "HIGH RAMP (faster)", height_dxa=1600)
fill(doc, "Which one caused a greater change? How do you know?", "________________", size=12)

# ---------------- PAGE 2 ----------------
title_block(doc, "Measured vs Inferred", "Chapter 3 Guided Notes · Page 2", new_page=True)

heading(doc, "Measured vs Inferred")
body(doc, "We do NOT directly measure speed or energy. We measure the change and infer the relationship.", size=12, color=GRAY, after=20)
data_table(doc, ["MEASURED (I used a tool)", "INFERRED (I reasoned it)"],
           [("ramp height", "relative speed (faster / slower)"),
            ("cup displacement (cm)", "relative energy of motion (more / less)"),
            ("", "")],
           col_widths=[3600, 3600], row_h=720)

heading(doc, "Fair Test")
body(doc, "A fair test changes ONE thing at a time and keeps everything else the same.", size=12, color=GRAY, after=20)
fill(doc, "In Ramp It Up!, the ONE thing we changed was", "________________", size=13)
fill(doc, "What we kept the same (the ball, the cup, the surface):", "________________", size=13)

heading(doc, "Ramp It Up! Evidence")
data_table(doc, ["Ramp height (books)", "Cup displacement (cm)"],
           [("1 book", ""), ("2 books", ""), ("3 books", "")],
           col_widths=[3600, 3600], row_h=700)

# ---------------- PAGE 3 ----------------
title_block(doc, "Claim + Evidence", "Chapter 3 Guided Notes · Page 3", new_page=True)

heading(doc, "Make a Claim")
body(doc, "Claim: For the SAME object, when it moves faster it has ______ energy of motion, because it caused a ______ change.", size=13, bold=True, after=30)
fill(doc, "Evidence from Ramp It Up!: the", "________________", "ramp made the cup move the farthest.", size=13)
fill(doc, "In my own words — the relationship: the same object moving faster has",
     "________________", "energy of motion.", size=13)

heading(doc, "Graph It")
draw_box(doc, FULL_W, 2600, "draw or sketch a bar graph of ramp height vs cup displacement")

heading(doc, "Check Your Thinking")
body(doc, "Why do we compare the SAME object instead of a heavy ball and a light ball?", size=13, bold=True, after=30)
wline(doc, 2, gap=30, after=18)

connect(doc, "Chapter 1 → 2 → 3: energy causes change; moving objects have energy; faster (same object) = more energy of motion.")

doc.save(OUT)
print("saved", OUT)
