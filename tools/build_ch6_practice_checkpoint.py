"""Build Chapter 6 practice worksheet and concept checkpoint DOCX."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from ch4_common import *

WS = os.path.join(os.path.dirname(__file__), '..', 'production', 'worksheets')
CP = os.path.join(os.path.dirname(__file__), '..', 'production', 'quizzes')


def build_practice():
    d = Document()
    setup_portrait(d)
    title(d, "Energy Transformations — Practice",
          "Chapter 6 · Energy Transformations + Engineering Design · Week 7")
    name_date(d)

    section(d, "A. TRANSFER / TRANSFORMATION / BOTH")
    prompt(d, "Read each system. Circle TRANSFER, TRANSFORMATION, or BOTH.")
    rows = [
        ("Warm water warms a cool spoon.", "TRANSFER", "TRANSFORMATION", "BOTH"),
        ("A flashlight changes stored energy to light.", "TRANSFER", "TRANSFORMATION", "BOTH"),
        ("A toy car hits a cup: the cup moves and we hear a sound.", "TRANSFER", "TRANSFORMATION", "BOTH"),
        ("A buzzer changes electrical energy to sound.", "TRANSFER", "TRANSFORMATION", "BOTH"),
        ("Falling dominoes knock over the next domino, and we hear a click.", "TRANSFER", "TRANSFORMATION", "BOTH"),
    ]
    for i, (q, a, b, c) in enumerate(rows, 1):
        add_par(d, f"{i}. {q}", size=11, space_before=2, space_after=0)
        add_par(d, f"     {a}      {b}      {c}", size=11, bold=True, space_after=6)

    section(d, "B. INPUT → CHANGE → OUTPUT")
    prompt(d, "Fill in the missing part of each energy chain.")
    add_par(d, "1. Wind-up toy:  INPUT = stored energy → CHANGE = _____ → OUTPUT = the toy moves.", size=11, space_after=2)
    answer_lines(d, 1)
    add_par(d, "2. Flashlight:  INPUT = stored energy → CHANGE = _____ → OUTPUT = light we see.", size=11, space_after=2)
    answer_lines(d, 1)
    add_par(d, "3. Solar panel:  INPUT = _____ → CHANGE = light to electrical → OUTPUT = electricity.", size=11, space_after=2)
    answer_lines(d, 1)

    section(d, "C. FIX THE ENERGY CHAIN")
    prompt(d, "Each chain has a mistake. Rewrite it correctly.")
    add_par(d, "1. \u201cINPUT: sound  →  OUTPUT: stored energy\u201d  (the order is wrong)", size=11, italic=True, space_after=2)
    answer_lines(d, 1)
    add_par(d, "2. \u201cThe energy DISAPPEARED when the toy stopped.\u201d", size=11, italic=True, space_after=2)
    answer_lines(d, 2)

    section(d, "D. DESIGN THINKING — criteria vs constraints")
    prompt(d, "Label each statement CRITERIA (what it must do) or CONSTRAINT (a limit).")
    add_par(d, "1. It must make a clear sound signal.  → ____________________", size=11, space_after=2)
    add_par(d, "2. You may use only the provided materials.  → ____________________", size=11, space_after=2)
    add_par(d, "3. It must work three times in a row.  → ____________________", size=11, space_after=2)
    add_par(d, "4. No wall electricity is allowed.  → ____________________", size=11, space_after=6)

    section(d, "E. SHORT EXPLANATION")
    prompt(d, "How can changing energy from one form to another solve a problem? "
              "Use one device as an example (toaster, flashlight, wind-up timer, or solar panel).")
    answer_lines(d, 3)

    d.save(os.path.join(WS, "06-ch6-energy-transformations-practice.docx"))
    print("built practice")


def build_checkpoint():
    d = Document()
    setup_portrait(d)
    title(d, "Chapter 6 Concept Checkpoint — Energy Transformations",
          "Grade 4 · Energy Transfer and Transformation · Week 7")
    name_date(d)
    add_par(d, "Circle or write the best answer.", size=11, italic=True, color=GRAY, space_after=8)

    def q(num, text):
        add_par(d, f"{num}. {text}", size=12, space_before=4, space_after=2)

    section(d, "PART 1 — Core Ideas")
    q(1, "Energy transformation means energy ___.")
    add_par(d, "a) disappears   b) changes form   c) stops moving   d) becomes nothing", size=11, space_after=6)
    q(2, "Energy transfer means energy ___.")
    add_par(d, "a) changes form   b) moves from one object or place to another   "
              "c) disappears   d) turns into light", size=11, space_after=6)
    q(3, "A flashlight changes stored energy to light. This is a ___.")
    add_par(d, "a) transformation   b) transfer only   c) nothing   d) loss of energy", size=11, space_after=6)
    q(4, "Falling dominoes knock over the next domino AND make a click. This is ___.")
    add_par(d, "a) transfer only   b) transformation only   c) BOTH transfer and transformation   d) neither", size=11, space_after=6)

    section(d, "PART 2 — Energy Chain")
    q(5, "Fill in the chain for a wind-up toy:")
    add_par(d, "INPUT = stored energy  →  CHANGE = _____  →  OUTPUT = the toy moves", size=11, space_after=6)

    section(d, "PART 3 — Engineering Design")
    q(6, "The desired features a good solution must have are called ___.")
    add_par(d, "a) constraints   b) criteria   c) tests   d) materials", size=11, space_after=6)
    q(7, "The limits on a design (materials, cost, time, safety) are called ___.")
    add_par(d, "a) criteria   b) problems   c) constraints   d) signals", size=11, space_after=6)
    q(8, "After a test, engineers use the results to ___.")
    add_par(d, "a) stop forever   b) refine the design   c) hide the problem   d) start over without thinking", size=11, space_after=6)

    section(d, "PART 4 — Evidence")
    q(9, "A student's device worked in Test 1 but not in Test 2. What should the team do?")
    add_par(d, "a) give up   b) look at the evidence and change ONE thing   "
              "c) pretend it worked   d) throw it away", size=11, space_after=6)
    q(10, "Finish this sentence using the words \u201cevidence\u201d and \u201csupports\u201d (NOT \u201cproves\u201d):")
    add_par(d, "Our observation that the bell rang louder is ___ that ___ the change helped.", size=11, space_after=6)

    d.save(os.path.join(CP, "06-ch6-concept-checkpoint.docx"))
    print("built checkpoint")


if __name__ == "__main__":
    build_practice()
    build_checkpoint()
    print("done")
