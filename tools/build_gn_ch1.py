"""Premium guided notes — Chapter 1: Energy Causes Change (3 pages)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "01-ch1-energy-causes-change-guided-notes.docx"))

doc = new_doc()

# ---------------- PAGE 1 ----------------
title_block(doc, "Energy Causes Change", "Chapter 1 Guided Notes · Grade 4 Energy Transfer & Transformation")
big_question(doc, "Where can we observe evidence of energy causing change?")

heading(doc, "Key Words")
fill(doc, "energy — Energy is the ability to cause", trail=".")
fill(doc, "change — Change means something becomes", trail=".")
fill(doc, "evidence — Evidence is something we observe that helps us", "________________", "what happened.")

heading(doc, "Model It")
body(doc, "Energy causes a change. The change is our evidence.", size=12, italic=True, color=GRAY, after=30)
model_boxes(doc, ["ENERGY", "CHANGE", "EVIDENCE"])
body(doc, "In my own words:", size=13, bold=True, after=20)
wline(doc, 1, gap=30, after=18)

heading(doc, "Draw / Label")
body(doc, "Pick one change from class. Draw what it looked like before and after, then write what changed.", size=12, color=GRAY, after=20)
labeled_pair(doc, "BEFORE", "AFTER", height_dxa=1900)
fill(doc, "What changed?", "________________________________________________", size=12)

# ---------------- PAGE 2 ----------------
title_block(doc, "Forms of Energy + Stored Energy", "Chapter 1 Guided Notes · Page 2", new_page=True)

heading(doc, "Forms of Energy")
body(doc, "Energy has different forms. Write or draw one example that shows a change for each.", size=12, color=GRAY, after=20)
two_col_table(doc, ["Form", "One example that shows a change"],
              [("motion", ""), ("sound", ""), ("light", ""), ("heat", ""), ("electrical energy", "")],
              row_h=600)

heading(doc, "Stored Energy")
key_idea(doc, "Stored energy can cause a change later.")
body(doc, "For each example, write the change that could happen later.", size=12, color=GRAY, after=20)
two_col_table(doc, ["Example", "What change could happen later?"],
              [("battery (in a flashlight)", ""),
               ("stretched rubber band", ""),
               ("raised object", "")],
              row_h=720)

heading(doc, "Draw One Stored-Energy Example")
draw_box(doc, FULL_W, 1750, "draw your stored-energy example here")

# ---------------- PAGE 3 ----------------
title_block(doc, "Energy Detectives — Evidence", "Chapter 1 Guided Notes · Page 3", new_page=True)

heading(doc, "Observation vs Explanation")
body(doc, "Observation = what I see.      Explanation = what it means.", size=13, after=20)
fill(doc, "Example: The light turned on. That is an", "________________", "because I saw the change.", size=13)
fill(doc, "Example: Energy caused the change. That is an", "________________", "because it tells what it means.", size=13)

heading(doc, "Evidence Table")
body(doc, "Record one change you found as an Energy Detective.", size=12, color=GRAY, after=20)
two_col_table(doc, ["Prompt", "Your answer"],
              [("Before", ""), ("After", ""), ("What changed?", ""), ("What is the evidence?", "")],
              row_h=680)

heading(doc, "Check Your Thinking")
body(doc, "How do scientists know energy is involved if energy itself cannot be seen directly?", size=13, bold=True, after=30)
wline(doc, 2, gap=30, after=18)

heading(doc, "Remember")
model_boxes(doc, ["ENERGY", "CHANGE", "EVIDENCE"], size=12)
connect(doc, "Chapter 1 connection: every change we observe is a clue that energy was involved.")

doc.save(OUT)
print("saved", OUT)
