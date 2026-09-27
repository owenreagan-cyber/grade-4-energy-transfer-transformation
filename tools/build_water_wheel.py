"""Flagship Lab 2 — Water Wheel (student + teacher). Rebuilt per Phase 13B spec.

ONE independent variable (pour height) · constants held (wheel, axle, blades, water volume,
pour opening, thread/load) · ONE primary response (paperclips lifted) · no pre-written
student observations · Grade-4 vocabulary · Thursday hands-on / Friday analysis.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "labs", "unit-02"))
os.makedirs(OUT_DIR, exist_ok=True)
SUB = "Flagship Lab 2 · Grade 4 Using Natural Resources for Energy"

def save(doc, fn):
    doc.save(os.path.join(OUT_DIR, fn))
    print("saved", fn)

def build_student():
    doc = new_doc()
    title_block(doc, "Water Wheel", SUB + " · Student Sheet")
    big_question(doc, "How does falling water transfer energy to lift a load?")

    heading(doc, "What We Know")
    body(doc, "Falling water has energy of motion. That energy can be transferred to a wheel and used to lift a load.", size=12, color=GRAY, after=20)

    heading(doc, "Fair Test")
    key_idea(doc, "We change ONE thing. We keep everything else the same.")
    two_col_table(doc, ["The ONE thing we change", "The ONE thing we measure"],
                  [("pour height (how high the water is poured from)", "how many paperclips the wheel lifts")],
                  row_h=800)

    heading(doc, "Keep the Same")
    body(doc, "Check the parts that must stay the same in every trial.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Part", "Same every time? (check ✓)"],
                  [("wheel design", ""), ("axle", ""), ("blade setup", ""),
                   ("water volume", ""), ("pour opening", ""), ("thread / load system", "")],
                  row_h=420)

    heading(doc, "Prediction")
    body(doc, "Fill in your prediction.", size=12, color=GRAY, after=20)
    fill(doc, "If I pour water from a", "________________", "height, then the wheel will lift", "paperclips.", trail="")
    # fix the above in a follow-up line
    wline(doc, 1, gap=30, after=18)

    heading(doc, "Draw the Wheel")
    body(doc, "Draw your group's wheel. Label the blades, the axle, and the thread.", size=12, color=GRAY, after=20)
    draw_box(doc, FULL_W, 1700, "draw your water wheel here")

    check_thinking(doc, "Why is it important to change only ONE thing in this test?", lines=2)
    save(doc, "water-wheel-flagship-lab-student.docx")
    return doc

def build_student2():
    # Rebuild student sheet as a single clean 3-page packet (avoid the stray fill line above).
    doc = new_doc()
    title_block(doc, "Water Wheel", SUB + " · Student Sheet")
    big_question(doc, "How does falling water transfer energy to lift a load?")

    heading(doc, "What We Know")
    body(doc, "Falling water has energy of motion. That energy can be transferred to a wheel and used to lift a load.", size=12, color=GRAY, after=20)

    heading(doc, "Fair Test")
    key_idea(doc, "We change ONE thing. We keep everything else the same.")
    two_col_table(doc, ["The ONE thing we change", "The ONE thing we measure"],
                  [("pour height (how high the water is poured from)", "how many paperclips the wheel lifts")],
                  row_h=800)

    heading(doc, "Keep the Same")
    body(doc, "These parts must stay the same in every trial:", size=12, color=GRAY, after=12)
    body(doc, "☐ wheel design      ☐ axle      ☐ blade setup", size=13, after=8)
    body(doc, "☐ water volume      ☐ pour opening      ☐ thread / load system", size=13, after=20)

    heading(doc, "Prediction")
    body(doc, "If I pour water from a HIGHER height, I predict the wheel will lift ______ paperclips.", size=13, bold=True, after=20)
    wline(doc, 1, gap=30, after=18)

    heading(doc, "Draw the Wheel")
    body(doc, "Draw your group's wheel. Label the blades, the axle, and the thread.", size=12, color=GRAY, after=20)
    draw_box(doc, FULL_W, 1400, "draw your water wheel here")

    # PAGE 2
    title_block(doc, "Test and Record", "Water Wheel · Page 2", new_page=True)
    heading(doc, "Data Table")
    body(doc, "Test three pour heights. Keep everything else the same. Record what happens.", size=12, color=GRAY, after=20)
    data_table(doc, ["Trial", "Pour height (cm)", "Paperclips lifted (count)", "What I noticed"],
               [("Low", "", "", ""), ("Medium", "", "", ""), ("High", "", "", "")],
               col_widths=[1200, 2200, 2500, 4180], row_h=1100)

    heading(doc, "Energy Pathway")
    body(doc, "Number the pathway in order from 1 to 4.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Step", "Order"],
                  [("falling water", ""), ("spinning wheel", ""), ("water at the top", ""), ("lifted load", "")],
                  row_h=460)

    # PAGE 3
    title_block(doc, "Claim and Redesign", "Water Wheel · Page 3", new_page=True)
    heading(doc, "Make a Claim")
    body(doc, "Finish the claim using your data.", size=12, color=GRAY, after=20)
    fill(doc, "When I poured water from a higher height, the wheel lifted", "________________", "paperclips.")
    body(doc, "This is evidence that falling water from a higher height has more energy of motion to transfer.", size=12, color=GRAY, after=20)

    heading(doc, "Redesign")
    body(doc, "If you could change ONE part of the wheel to lift more paperclips, what would you change? Why?", size=12, color=GRAY, after=20)
    wline(doc, 3, gap=30, after=18)

    check_thinking(doc, "A real hydroelectric dam uses spinning turbines connected to generators. How is your water wheel like a dam's turbine?", lines=2)
    connect(doc, "Water wheel connection: falling water → spinning wheel → lifted load. Real dams: falling water → spinning turbine → generator → electricity.")
    save(doc, "water-wheel-flagship-lab-student.docx")
    return doc

def build_teacher():
    doc = new_doc()
    title_block(doc, "Water Wheel — Teacher Guide", SUB + " · Teacher")
    body(doc, "Thursday: hands-on testing. Friday: analysis, redesign, reflection.", size=13, bold=True, color=NAVY, after=30)

    heading(doc, "Big Question")
    body(doc, "How does falling water transfer energy to lift a load?", size=13, after=20)

    heading(doc, "Connection to Real Systems")
    body(doc, "Real hydroelectric systems use spinning turbines connected to generators. In this lab, the spinning wheel (turbine) lifts a load instead of turning a generator — the energy pathway is the same.", size=12, color=GRAY, after=20)
    model_boxes(doc, ["FALLING WATER", "SPINNING WHEEL", "LIFTED LOAD"], size=12)

    heading(doc, "Variables")
    two_col_table(doc, ["Type", "Detail"],
                  [("Independent (change)", "pour height (ONE variable)"),
                   ("Response (measure)", "paperclips lifted (count)"),
                   ("Constants (keep same)", "wheel design · axle · blade setup · water volume · pour opening · thread/load system")],
                  row_h=760)

    heading(doc, "Materials (per group of 4)")
    body(doc, "paper plate or plastic lid wheel · 8–10 blade cups/popsicle-stick blades · straw or dowel axle · ~50 cm thread · paperclips (load) · small cup with a pour opening · 500 mL water source · basin/tray to catch water · ruler (height) · towel", size=12, color=GRAY, after=20)

    heading(doc, "Setup & Safety")
    body(doc, "• Build the wheel first (blades on a plate/lid, axle through the center).", size=12, after=6)
    body(doc, "• Hang thread from the axle; attach paperclips as the load.", size=12, after=6)
    body(doc, "• Pour water from a cup with a fixed opening onto the blades over a basin.", size=12, after=6)
    body(doc, "• Change ONLY pour height (e.g., 15 cm, 30 cm, 45 cm). Same water volume (500 mL) and same pour opening each trial.", size=12, after=6)
    body(doc, "• Safety: keep water over the basin; wipe spills immediately; no horseplay near water.", size=12, after=20)

    heading(doc, "Timing (30-min class)")
    two_col_table(doc, ["Segment", "Minutes"],
                  [("Build wheel + review fair test", "10"),
                   ("Test 3 pour heights (rotate jobs)", "15"),
                   ("Record + quick cleanup", "5")],
                  row_h=460)

    heading(doc, "Expected Outcome")
    body(doc, "Higher pour height → falling water has more energy of motion → wheel spins faster/longer → lifts more paperclips (or lifts the fixed load in less time). Do NOT pre-print these results on the student sheet; students infer them.", size=12, color=GRAY, after=20)

    heading(doc, "What to Listen For")
    body(doc, "• Students keep the wheel/water/pour the same and change only height.", size=12, after=6)
    body(doc, "• Students use 'energy of motion' and 'transfer' (not 'mechanical energy').", size=12, after=6)
    body(doc, "• Students connect falling water → spinning wheel → lifted load to dams.", size=12, after=20)

    heading(doc, "Absent-Student Recovery")
    body(doc, "Send the student sheet + a partner's data table. Have the absent student complete the claim, pathway, and redesign using the provided data.", size=12, color=GRAY, after=20)

    heading(doc, "Assessment")
    body(doc, "Formative: fair-test check, data table, claim, redesign, check-your-thinking response.", size=12, color=GRAY, after=20)
    save(doc, "water-wheel-flagship-lab-teacher.docx")
    return doc

if __name__ == "__main__":
    build_student2()
    build_teacher()
    print("DONE")
