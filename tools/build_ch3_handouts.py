"""Chapter 3 practice, quiz, Ramp It Up sheet, recovery, and teacher records.

Reads the chapter spec. Does not edit frozen Chapter 1 or Chapter 2 files.
Run: .venv/bin/python tools/build_ch3_handouts.py
"""
import json
import os

from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPEC = json.load(open(os.path.join(ROOT, "docs/chapter-03/CH3_CHAPTER_SPEC.json"), encoding="utf-8"))
PRIMARY = RGBColor(0x1B, 0x4F, 0xC2)
INK = RGBColor(0x1A, 0x1D, 0x26)
FONT = "Calibri"


def doc():
    document = Document()
    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    style = document.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(14)
    style.font.color.rgb = INK
    return document


def add(document, text, size=14, bold=False, color=INK, space=6):
    p = document.add_paragraph()
    p.paragraph_format.space_after = Pt(space)
    run = p.add_run(text)
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = color
    return p


def save(document, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    document.save(path)
    print(path)


def practice():
    document = doc()
    add(document, "Chapter 3  ·  Energy and Speed Are Related", 18, True, PRIMARY)
    add(document, "Practice  ·  not graded  ·  OPTIONAL", 12, True)
    add(document, "Name ______________________________    Date ______________")
    add(document, "Use one ball in every part. Do not write a speed number.")
    add(document, "1. A student rolls the same ball down a low ramp and a steeper ramp. The cup moves farther from the steeper ramp. What is the evidence?", bold=True)
    add(document, "________________________________________________________________")
    add(document, "________________________________________________________________")
    add(document, "2. Why is it one ball, not a heavy ball and a light ball?", bold=True)
    add(document, "________________________________________________________________")
    add(document, "________________________________________________________________")
    add(document, "3. Name one thing that was measured in centimeters, and one thing that was inferred.", bold=True)
    add(document, "Measured: ______________________________________________________")
    add(document, "Inferred: ______________________________________________________")
    save(document, os.path.join(ROOT, "production/worksheets/03-ch3-energy-speed-practice.docx"))
    key = """# Chapter 3 Practice Key

Not graded. OPTIONAL.

1. The farther cup move is the evidence. Accept: a bigger change, or the cup moved farther. Do not accept a speed number.
2. This chapter compares the same object at two speeds. A heavier ball and a lighter ball would change the mass too.
3. Measured: ramp height in centimeters, or how far the cup moved in centimeters. Inferred: which setup had the faster ball, or which had more energy of motion.

Reader pp. 13–16. Teacher Guide Lessons 4 and 5.
"""
    path = os.path.join(ROOT, "production/answer-keys/03-ch3-energy-speed-practice-key.md")
    open(path, "w", encoding="utf-8").write(key)
    print(path)


def quiz():
    document = doc()
    add(document, "Chapter 3  ·  Energy and Speed Are Related", 18, True, PRIMARY)
    add(document, "Quiz  ·  8 items  ·  12 points  ·  FLEX", 12, True)
    add(document, "Name ______________________________    Date ______________")
    add(document, "Score: ______ / 12 = ______ %", 16, True)
    items = [
        "1. (1 point) Speed is a measurement of the ________ an object travels over an amount of time.",
        "2. (1 point) Which comparison fits this chapter?  A. one ball at two speeds   B. a heavy ball and a light ball",
        "3. (2 points) What shows that the faster ball had more energy of motion?",
        "4. (2 points) In Ramp It Up, what did you measure, and what did you infer?",
        "5. (1 point) What was the one thing you changed?",
        "6. (1 point) A correct graph uses which labels?  A. ramp height (cm) and average cup movement (cm)   B. speed and energy",
        "7. (2 points) The same ball rolls from a steeper ramp. What change do you look for?",
        "8. (2 points) How are energy and speed related?",
    ]
    for item in items:
        add(document, item, bold=True, space=2)
        add(document, "________________________________________________________________", space=10)
    save(document, os.path.join(ROOT, "production/quizzes/03-ch3-energy-speed-quiz.docx"))
    key = """# Chapter 3 Quiz Key

8 items · 12 points. Score: ______ / 12 = ______ %.
FLEX. Friday 2026-10-23 or makeup within 2 school days. Not a first lesson.

1. (1) distance. Reader p. 13.
2. (1) A. one ball at two speeds.
3. (2) A greater change. Accept a farther cup move, a higher bounce, or a louder sound. No speed number.
4. (2) Measured centimeters (ramp height and/or cup movement). Inferred the speed relationship.
5. (1) ramp height. The ball stayed the same.
6. (1) A. ramp height (cm) and average cup movement (cm).
7. (2) A greater change, such as the cup or bucket moving farther.
8. (2) For the same object, greater speed is related to greater energy of motion. A greater change is the evidence.

Do not accept kinetic, potential, mechanical, or a speed in meters per second.
"""
    path = os.path.join(ROOT, "production/answer-keys/03-ch3-energy-speed-quiz-key.md")
    open(path, "w", encoding="utf-8").write(key)
    print(path)
    blueprint = """# Chapter 3 Quiz Blueprint

8 items · 12 points · raw score and percentage.
Status: FLEX. It assesses ideas taught Monday 2026-10-19 through Thursday 2026-10-22.

| Item | Points | Anchor | Demand |
|---|---|---|---|
| 1 | 1 | V1 | vocabulary in context |
| 2 | 1 | N1 | same object |
| 3 | 2 | N1 | evidence |
| 4 | 2 | N2 | measured and inferred |
| 5 | 1 | N2 | fair test |
| 6 | 1 | GRAPH | axis labels |
| 7 | 2 | N3 | steeper ramp |
| 8 | 2 | BQ_NOW | Big Question |

No mass comparison as a correct answer. No required speed or energy calculation.
"""
    path = os.path.join(ROOT, "production/quizzes/03-ch3-energy-speed-quiz-blueprint.md")
    open(path, "w", encoding="utf-8").write(blueprint)
    print(path)


def lab():
    document = doc()
    add(document, "Ramp It Up 2.0", 18, True, PRIMARY)
    add(document, "Chapter 3  ·  REQUIRED  ·  Tuesday and Wednesday", 12, True)
    add(document, "Name ______________________________    Date ______________")
    add(document, "One ball. Measure the vertical ramp height in centimeters. Measure how far the cup moves in centimeters.")
    add(document, "Roll once to calibrate. Do not record that roll. Then record three trials at each height. That is nine measured trials.")
    add(document, "Ramp height is not a speed. Do not write a speed number.")
    table = document.add_table(rows=4, cols=5)
    headers = ["Books", "Ramp height (cm)", "Trial 1 (cm)", "Trial 2 (cm)", "Trial 3 (cm)"]
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = header
    for index, books in enumerate(("1", "2", "3"), start=1):
        table.rows[index].cells[0].text = books
    add(document, "")
    add(document, "Average cup movement (cm):   1 book ________    2 books ________    3 books ________", bold=True)
    add(document, "Graph: ramp height (cm) on one axis. Average cup movement (cm) on the other. Do not label an axis as speed.")
    add(document, "Challenge: move the cup as close as you can to 30 cm without going past.")
    add(document, "My closest result: ________ cm. Did it go past 30 cm?  yes / no")
    save(document, os.path.join(ROOT, "production/worksheets/03-ch3-ramp-it-up-student.docx"))
    key = """# Ramp It Up 2.0 Key

REQUIRED lab. There is no single correct centimeter table. Students record their own trials.

Look for:
- one ball
- vertical ramp height in centimeters for 1, 2, and 3 books
- one unrecorded calibration roll
- three recorded trials at each height (nine recorded trials)
- averages
- a graph of ramp height (cm) against average cup movement (cm)
- no speed number and no meters per second
- the 30 cm challenge judged by closeness without going past

A steeper ramp should usually move the cup farther. If it does not, help the student check the fair test before changing the science claim.
"""
    path = os.path.join(ROOT, "production/answer-keys/03-ch3-ramp-it-up-key.md")
    open(path, "w", encoding="utf-8").write(key)
    print(path)
    spec = """# Ramp It Up 2.0 — Teacher Spec

Status: REQUIRED. Provenance: ADAPTED from AP 4.1.
Dates: Tuesday 2026-10-20 and Wednesday 2026-10-21.
Materials: cardboard ramp, 3 books, 1 ball, 1 cup, centimeter ruler.

%s

Do not build a second ramp lab. Drop It is Friday FLEX, not this lab.
""" % SPEC["anchors"][4]["protocolStatement"]
    path = os.path.join(ROOT, "production/labs/03-ch3-ramp-it-up-teacher-spec.md")
    open(path, "w", encoding="utf-8").write(spec)
    print(path)


def recovery():
    document = doc()
    add(document, "Chapter 3  ·  Absent-Student Recovery", 18, True, PRIMARY)
    add(document, "FLEX  ·  not a first lesson", 12, True)
    add(document, "Name ______________________________    Date ______________")
    add(document, "Finish Guided Notes: BQ, V1, N1, N2, N3, N4, CHECK, and BQ now.")
    add(document, "Use the Reader catch, the ramp and bucket, and the bounce. Do not invent centimeter numbers you did not measure.")
    add(document, "If you missed the lab, explain the relationship from the Reader. Your teacher may show you the class graph. Do not copy fake personal data.")
    add(document, "Drop It is not required makeup.")
    add(document, "If you missed the quiz, makeup is within 2 school days.")
    add(document, "My explanation:", bold=True)
    add(document, "________________________________________________________________")
    add(document, "________________________________________________________________")
    add(document, "________________________________________________________________")
    save(document, os.path.join(ROOT, "production/worksheets/03-ch3-absent-student-recovery.docx"))


def pacing_and_playbook():
    lines = ["# Chapter 3 — Authoritative Pacing Plan", "", "Generated from `docs/chapter-03/CH3_CHAPTER_SPEC.json`. Do not keep a second timing system.", "", "30-minute block. Required sessions stay at or under 24 minutes.", ""]
    lines.append("| Session | Date | Status | Reader | Required min | Slides |")
    lines.append("|---|---|---|---|---|---|")
    for session in SPEC["sessions"]:
        lines.append("| %s | %s | %s | %s | %s | %s |" % (
            session["id"], session["date"], session["status"], session["readerPages"] or "—",
            session["requiredMinutes"], ", ".join(session["slideIds"]),
        ))
    lines.append("")
    lines.append(SPEC["calendarResolution"]["statement"])
    lines.append("")
    lines.append(SPEC["anchors"][4]["protocolStatement"])
    path = os.path.join(ROOT, "docs/chapter-03/CH3_PACING_PLAN.md")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(path)
    play = ["# Chapter 3 Playbook Region", "", "The frozen unit playbook is not edited. This file is the Chapter 3 teacher region.", ""]
    for anchor in SPEC["anchors"]:
        text = " ".join(anchor.get("lines") or []) or anchor.get("protocolStatement") or ""
        play.append("## %s" % anchor["code"])
        play.append("status: %s" % anchor["status"])
        play.append("text: %s" % text)
        play.append("")
    path = os.path.join(ROOT, "docs/chapter-03/CH3_PLAYBOOK_REGION.md")
    open(path, "w", encoding="utf-8").write("\n".join(play))
    print(path)


def main():
    practice()
    quiz()
    lab()
    recovery()
    pacing_and_playbook()


if __name__ == "__main__":
    main()
