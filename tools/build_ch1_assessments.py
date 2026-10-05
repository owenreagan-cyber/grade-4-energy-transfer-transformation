"""Phase 6.1 — Chapter 1 student assessments & resources (rebuilt on the Unit 1 Visual System).

Builds (DOCX; PDF + previews via tools/export_pdf_previews.py):
  production/worksheets/01-ch1-energy-causes-change-practice.docx        (ungraded practice, 2 pp)
  production/quizzes/01-ch1-energy-causes-change-quiz.docx               (scored, 9 items / 16 pts)
  production/worksheets/01-ch1-energy-detectives-student.docx            (OPTIONAL, ungraded)

Corrections vs v1.0 (F2 F3 F9 F6): Reader-supported stored-energy examples only; quiz item/point
mismatches fixed; standard score + percent line; Name + Homeroom header (no Date); real ruled writing
lines (table rows) with >= 2 lines on every explain prompt; Detectives is optional and carries NO points.

Run: .venv/bin/python tools/build_ch1_assessments.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_ch1_guided_notes as g
from build_ch1_guided_notes import (Inches, Pt, WD_ALIGN_PARAGRAPH, WD_ALIGN_VERTICAL, FULL_W, USABLE_IN,
    PRIMARY_HEX, ACCENT_HEX, INK_HEX, SURFACE_HEX, RULE_HEX, CH1_PRIMARY, CH1_ACCENT, CH1_NEUTRAL, INK, INK_SOFT, WHITE)

ROOT = g.ROOT
BODY, PROMPT, CAP = 14.0, 14.5, 12.0

# ---------------------------------------------------------------- shared pieces
def header(doc, title, tag, group=False, key_note=None):
    g._para(doc, "UNIT 1 \u00b7 ENERGY TRANSFER & TRANSFORMATION", size=g.ATTR_SZ, bold=True, color=INK_SOFT, after=2, caps=True)
    g._para(doc, title, size=22, bold=True, color=CH1_PRIMARY, after=2)
    g._para(doc, tag, size=CAP, bold=True, color=CH1_NEUTRAL, after=4)
    p = doc.add_paragraph(); g._spacing(p, 0, 6, line_pt=26)
    g._run(p, "Name: ", size=CAP, bold=True); g._run(p, "_" * 24, size=CAP, underline=True)
    if group:
        g._run(p, "   Group: ", size=CAP, bold=True); g._run(p, "_" * 10, size=CAP, underline=True)
    g._run(p, "   Homeroom:  ", size=CAP, bold=True)
    for i, lbl in enumerate(("4A", "4B", "4C", "4D")):
        g._run(p, ("  " if i else "") + "\u25CB " + lbl, size=CAP)

def score_box(doc, total):
    """Standard score line (raw + percent) \u2014 all scored work."""
    t = doc.add_table(rows=1, cols=1); g._no_borders(t)
    c = t.cell(0, 0); c.width = FULL_W
    g._margins(c, top=70, left=120, bottom=70, right=120); g._shade(c, SURFACE_HEX)
    g._border(c, left=dict(sz=18, color=ACCENT_HEX))
    p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    g._run(p, "SCORE:  ", size=CAP, bold=True, color=CH1_NEUTRAL)
    g._run(p, "_____", size=PROMPT, underline=True)
    g._run(p, " / %d      " % total, size=PROMPT, bold=True)
    g._run(p, "_______", size=PROMPT, underline=True)
    g._run(p, " %", size=PROMPT, bold=True)

def lines(doc, n):
    g._writing_line(doc, size=BODY, gap_pt=28, n=n)

def spacer(doc, pt=6):
    g._para(doc, "", after=pt)

def grid(doc, headers, widths, rows, row_h=640, head_fill=PRIMARY_HEX, cell_fn=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers)); g._no_borders(t)
    for r in t.rows:
        for i, w in enumerate(widths):
            r.cells[i].width = Inches(w)
    for i, h in enumerate(headers):
        c = t.cell(0, i); g._margins(c, top=40, left=80, bottom=40, right=80); g._shade(c, head_fill); g._vcenter(c)
        g._run(c.paragraphs[0], h, size=CAP, bold=True, color=WHITE, caps=True)
    g._row_height(t.rows[0], 440, rule='atLeast')
    for ri, row in enumerate(rows, 1):
        for ci, val in enumerate(row):
            c = t.cell(ri, ci); g._margins(c, top=40, left=80, bottom=40, right=80); g._vcenter(c)
            g._border(c, bottom=dict(sz=8, color=INK_HEX))
            if cell_fn:
                cell_fn(c, ri - 1, ci, val)
            elif val:
                g._run(c.paragraphs[0], val, size=BODY, bold=(ci == 0), color=CH1_PRIMARY if ci == 0 else INK)
        g._row_height(t.rows[ri], row_h, rule='atLeast')
    return t

def circle_choice(c, options, size=BODY):
    p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, o in enumerate(options):
        g._run(p, ("     " if i else "") + o, size=size, bold=True, color=CH1_PRIMARY)

def pbb(doc):
    """Page break via page_break_before on a 1pt paragraph (never leaves a blank page)."""
    p = doc.add_paragraph(); p.paragraph_format.page_break_before = True
    g._spacing(p, 0, 0, line_pt=1)
    r = p.add_run(""); r.font.size = Pt(1)
    return p

def finish(doc, path, footer):
    g._footer(doc, footer)
    g._seal(doc)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    return path

# ---------------------------------------------------------------- PRACTICE (ungraded, 2 pp)
def build_practice():
    doc = g.new_doc()
    header(doc, "Practice \u2014 Energy Causes Change", "Chapter 1 \u00b7 Grade 4 \u00b7 PRACTICE \u2014 NOT GRADED")
    g._section_head(doc, "A", "What changed?")
    g._caption(doc, "Write the change you could observe and one form of energy.", after=4)
    grid(doc, ["Scenario", "What changed?", "Form of energy"], [3.0, 2.6, 1.8], [
        ["A light switch is flipped.", "", ""], ["A toy car is pushed.", "", ""], ["A bell is rung.", "", ""],
        ["An ice cube sits on a warm hand.", "", ""]], row_h=660)
    spacer(doc, 3)
    g._section_head(doc, "B", "Evidence or not enough evidence?")
    g._caption(doc, "Circle one. Then finish the sentence: \u201cBecause \u2026\u201d", after=4)
    def b_cell(c, r, ci, val):
        if ci == 1:
            circle_choice(c, ["EVIDENCE", "NOT ENOUGH"], size=11)
        elif val:
            g._run(c.paragraphs[0], val, size=BODY, color=INK)
    grid(doc, ["Observation", "Circle one", "Because \u2026"], [3.3, 1.9, 2.2], [
        ["The fan blades started spinning when we plugged it in.", "x", ""],
        ["The battery looks shiny.", "x", ""],
        ["The room got brighter when the light came on.", "x", ""],
        ["I think the motor is strong.", "x", ""]], row_h=680, cell_fn=b_cell)
    pbb(doc)
    g._section_head(doc, "C", "Stored energy")
    g._caption(doc, "Circle YES or NO. Then tell what change could happen later \u2014 or say if it is happening now.", after=4)
    def c_cell(c, r, ci, val):
        if ci == 1:
            circle_choice(c, ["YES", "NO"], size=BODY)
        elif val:
            g._run(c.paragraphs[0], val, size=BODY, bold=(ci == 0), color=CH1_PRIMARY if ci == 0 else INK)
    grid(doc, ["Example", "Stored energy?", "Change later \u2014 or happening now?"], [2.7, 1.5, 3.2], [
        ["a battery in a flashlight that is switched off", "x", ""], ["an apple held above the ground", "x", ""],
        ["a stretched rubber band", "x", ""], ["a toy car rolling across the floor", "x", ""]], row_h=860, cell_fn=c_cell)
    spacer(doc, 8)
    g._section_head(doc, "D", "Explain")
    g._para(doc, "Energy is the ability to cause change. Describe one change you have observed. Tell why that change is evidence of energy.",
            size=PROMPT, bold=True, color=INK, after=4)
    lines(doc, 4)
    return finish(doc, os.path.join(ROOT, "production", "worksheets", "01-ch1-energy-causes-change-practice.docx"),
                  "Unit 1 \u00b7 Chapter 1 \u00b7 Practice \u00b7 Energy Causes Change \u00b7 Not graded")

# ---------------------------------------------------------------- QUIZ (scored, 9 items / 16 pts)
QUIZ_POINTS = [1, 1, 2, 1, 2, 2, 1, 3, 3]
assert sum(QUIZ_POINTS) == 16

def q_head(doc, n, pts, text=None):
    p = doc.add_paragraph(); g._spacing(p, 6, 3, line_pt=20)
    g._run(p, "%d.  " % n, size=PROMPT, bold=True, color=CH1_ACCENT)
    if text:
        g._run(p, text, size=PROMPT, bold=True, color=INK)
    g._run(p, "   (%d pt%s)" % (pts, "" if pts == 1 else "s"), size=10, italic=True, color=INK_SOFT)
    return p

def mc(doc, opts):
    for L, o in zip("abcd", opts):
        p = doc.add_paragraph(); g._spacing(p, 0, 2, line_pt=20)
        p.paragraph_format.left_indent = Inches(0.35)
        g._run(p, "%s)  " % L, size=BODY, bold=True, color=CH1_PRIMARY); g._run(p, o, size=BODY)

def stem(doc, text):
    p = g._para(doc, text, size=BODY, after=3); p.paragraph_format.left_indent = Inches(0.35)

def build_quiz():
    doc = g.new_doc()
    header(doc, "Chapter 1 Quiz \u2014 Energy Causes Change", "Chapter 1 \u00b7 Grade 4 \u00b7 SCORED \u2014 9 questions \u00b7 16 points")
    p = doc.add_paragraph(); g._spacing(p, 0, 6, line_pt=20)
    g._run(p, "Notes today:   \u25CB OPEN NOTE     \u25CB CLOSED NOTE", size=CAP, bold=True, color=CH1_NEUTRAL)
    g._run(p, "      (teacher circles one)", size=10, italic=True, color=INK_SOFT)
    score_box(doc, 16)
    q_head(doc, 1, 1, "Energy is the ability to \u2026")
    mc(doc, ["be invisible", "disappear", "cause change", "make sound"])
    q_head(doc, 2, 1, "When you see a change, that change is \u2026 that energy is present.")
    mc(doc, ["not important", "evidence", "impossible", "a guess"])
    q_head(doc, 3, 2, "A student pushes a toy car and it rolls across the floor.")
    g._para(doc, "What changed?", size=BODY, bold=True, after=2).paragraph_format.left_indent = Inches(0.35)
    lines(doc, 2)
    g._para(doc, "What form of energy do you observe?", size=BODY, bold=True, after=2).paragraph_format.left_indent = Inches(0.35)
    lines(doc, 1)
    q_head(doc, 4, 1, "Which list names forms of energy?")
    mc(doc, ["red, blue, green", "up, down, left, right", "fast, slow", "motion, sound, light, heat, electrical energy"])
    pbb(doc)
    q_head(doc, 5, 2, "Fill in the blanks to show the model we use.")
    stem(doc, "Word bank:   evidence      change")
    p = doc.add_paragraph(); g._spacing(p, 4, 6, line_pt=30); p.paragraph_format.left_indent = Inches(0.35)
    g._run(p, "ENERGY  \u2192  ", size=PROMPT, bold=True, color=CH1_PRIMARY); g._run(p, "_" * 12, size=PROMPT, underline=True)
    g._run(p, "  \u2192  ", size=PROMPT, bold=True, color=CH1_PRIMARY); g._run(p, "_" * 12, size=PROMPT, underline=True)
    q_head(doc, 6, 2, "A battery is sitting still in a flashlight that is switched off. Does the battery have energy? Explain.")
    lines(doc, 3)
    q_head(doc, 7, 1, "A book is held up high above the floor. It is not moving. The book \u2026")
    mc(doc, ["has stored energy", "has no energy", "is moving", "is lighter"])
    q_head(doc, 8, 3, "A student flips a switch and the light bulb turns on. Is this evidence of energy? Explain. Use the word \u201cchange.\u201d")
    lines(doc, 3)
    q_head(doc, 9, 3, "Circle YES or NO: is it evidence that energy caused a change?")
    def nine(c, r, ci, val):
        if ci == 1:
            circle_choice(c, ["YES", "NO"], size=BODY)
        elif val:
            g._run(c.paragraphs[0], val, size=BODY, color=INK)
    t = grid(doc, ["Statement", "Circle one"], [5.4, 2.0], [["a)  The flag waved when the wind blew.", "x"],
             ["b)  The desk is brown.", "x"], ["c)  The music got louder.", "x"]], row_h=560, cell_fn=nine)
    return finish(doc, os.path.join(ROOT, "production", "quizzes", "01-ch1-energy-causes-change-quiz.docx"),
                  "Unit 1 \u00b7 Chapter 1 \u00b7 Quiz \u00b7 Energy Causes Change \u00b7 16 points")

# ---------------------------------------------------------------- ENERGY DETECTIVES (optional, ungraded)
def build_detectives():
    doc = g.new_doc()
    header(doc, "Energy Detectives \u2014 Scavenger Hunt", "Chapter 1 \u00b7 OPTIONAL \u00b7 NOT GRADED \u00b7 Friday FLEX or review day", group=True)
    g._band(doc, "BIG QUESTION   Where can we observe evidence of energy causing change?", PRIMARY_HEX, size=13)
    spacer(doc, 4)
    g._section_head(doc, "A", "Class example \u2014 the pencil sharpener")
    for lbl in ("Before:", "After:", "What changed?", "What evidence did you observe?"):
        g._para(doc, lbl, size=BODY, bold=True, after=1)
        lines(doc, 2)
    g._para(doc, "What form of energy might be involved?", size=BODY, bold=True, after=1)
    lines(doc, 1)
    pbb(doc)
    g._section_head(doc, "B", "Energy scavenger hunt")
    g._caption(doc, "Find three changes in our classroom. Do not copy the class example. Your evidence is the change you observe.", after=4)
    grid(doc, ["Object", "Before", "After", "Energy form"], [2.0, 1.8, 1.8, 1.8],
         [["", "", "", ""], ["", "", "", ""], ["", "", "", ""]], row_h=640)
    spacer(doc, 2)
    g._section_head(doc, "C", "Stored energy \u2014 flashlight demo")
    for lbl, n in (("Prediction \u2014 What do you think will happen?", 2), ("Observation \u2014 What happened?", 2),
                   ("Evidence \u2014 What change did you observe?", 2),
                   ("Explanation \u2014 What does this tell you about stored energy?", 3)):
        g._para(doc, lbl, size=BODY, bold=True, after=1)
        lines(doc, n)
        if lbl[0] != "E" or not lbl.startswith("Explanation"): spacer(doc, 2)
    return finish(doc, os.path.join(ROOT, "production", "worksheets", "01-ch1-energy-detectives-student.docx"),
                  "Unit 1 \u00b7 Chapter 1 \u00b7 Energy Detectives \u00b7 Optional \u00b7 Not graded")

if __name__ == "__main__":
    for f in (build_practice, build_quiz, build_detectives):
        print("saved", f())
