"""Premium guided notes — Chapter 4: Energy Transfer (4 pages)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "04-ch4-energy-transfer-guided-notes.docx"))

doc = new_doc()

# ---------------- PAGE 1 ----------------
title_block(doc, "Energy Transfer", "Chapter 4 Guided Notes · Grade 4 Energy Transfer & Transformation")
big_question(doc, "What evidence shows that energy is transferred from place to place?")

heading(doc, "Key Words")
fill(doc, "energy transfer — Energy transfer means energy moves", "________________",
     "place to place or object to object.", size=13)
fill(doc, "evidence — Evidence is an observable", "________________", "in the target.", size=13)

heading(doc, "Model It")
body(doc, "Energy leaves a source, moves, and changes a target. The change is the evidence of transfer.", size=12, italic=True, color=GRAY, after=30)
model_boxes(doc, ["SOURCE", "ENERGY MOVES", "TARGET CHANGES"], box_w=2300, arr_w=620, size=13)

heading(doc, "Source → Path → Receiver")
body(doc, "Sound, light, heat, and electric current can all transfer energy.", size=13, bold=True, after=20)
data_table(doc, ["SOURCE (where energy starts)", "PATH (how it travels)", "RECEIVER (what changes)"],
           [("sound (tapped cup)", "", ""),
            ("light (flashlight)", "", ""),
            ("heat (warm water)", "", ""),
            ("electric current (battery)", "", "")],
           col_widths=[2400, 2400, 2400], row_h=560)

# ---------------- PAGE 2 ----------------
title_block(doc, "Sound + Light Transfer", "Chapter 4 Guided Notes · Page 2", new_page=True)

heading(doc, "Sound Transfers Energy")
body(doc, "A tap makes the cup vibrate. The paper target moves even though nothing touched it.", size=12, color=GRAY, after=20)
data_table(doc, ["Source", "What changed? (evidence)"],
           [("tapped cup (sound)", "")],
           col_widths=[3400, 3400], row_h=660)

heading(doc, "Light Transfers Energy")
body(doc, "A flashlight lights a card across the room. A barrier in the path stops the change.", size=12, color=GRAY, after=20)
data_table(doc, ["Source", "What changed? (evidence)"],
           [("flashlight (light)", "")],
           col_widths=[3400, 3400], row_h=660)

heading(doc, "Draw / Label")
body(doc, "Draw the flashlight, the path of light, and the lit card. Label the SOURCE, PATH, and RECEIVER.", size=12, color=GRAY, after=20)
draw_box(doc, FULL_W, 2300, "draw and label the light path")

# ---------------- PAGE 3 ----------------
title_block(doc, "Heat + Electric Current Transfer", "Chapter 4 Guided Notes · Page 3", new_page=True)

heading(doc, "Heat Transfers Energy")
body(doc, "Warm water is placed next to a cooler cup. The temperatures change over time.", size=12, color=GRAY, after=20)
data_table(doc, ["Before", "Later", "What changed? (evidence)"],
           [("", "", "")],
           col_widths=[2400, 2400, 2400], row_h=640)

heading(doc, "Electric Current Transfers Energy")
key_idea(doc, "Electric current can transfer energy from place to place.")
body(doc, "A battery connects through wires to a bulb, buzzer, or motor. The device changes.", size=12, color=GRAY, after=20)
data_table(doc, ["Source", "Device", "What changed? (evidence)"],
           [("battery", "", "")],
           col_widths=[2400, 2400, 2400], row_h=640)

heading(doc, "Draw / Label")
body(doc, "Draw a battery, wires, and a bulb. Label where the energy moves.", size=12, color=GRAY, after=20)
draw_box(doc, FULL_W, 2300, "draw and label the circuit")

# ---------------- PAGE 4 ----------------
title_block(doc, "Transfer vs Transformation", "Chapter 4 Guided Notes · Page 4", new_page=True)

heading(doc, "Two Different Ideas")
body(doc, "TRANSFER = energy MOVES.      TRANSFORMATION = energy CHANGES FORM.", size=13, bold=True, after=20)
body(doc, "A system can show transfer, transformation, or BOTH.", size=12, italic=True, color=GRAY, after=20)
data_table(doc, ["TRANSFER (energy moves)", "TRANSFORMATION (changes form)", "BOTH (moves AND changes)"],
           [("", "", ""),
            ("", "", ""),
            ("", "", "")],
           col_widths=[2400, 2400, 2400], row_h=720)

heading(doc, "Check Your Thinking")
body(doc, "A flashlight: the battery sends energy through wires to the bulb, and the bulb gives off light. Is that transfer, transformation, or BOTH? Explain.", size=13, bold=True, after=30)
wline(doc, 3, gap=30, after=18)

connect(doc, "Chapter 1 → 4: energy causes change; now we can trace HOW energy moves to cause that change.")

doc.save(OUT)
print("saved", OUT)
