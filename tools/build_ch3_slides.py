"""Chapter 3 slides. Mirrors the chapter spec. Measurement / Data theme.

Run: .venv/bin/python tools/build_ch3_slides.py
"""
import json
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPEC = json.load(open(os.path.join(ROOT, "docs/chapter-03/CH3_CHAPTER_SPEC.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "production/slides/03-ch3-energy-speed-slides.pptx")

PRIMARY = RGBColor(0x1B, 0x4F, 0xC2)
ACCENT = RGBColor(0x5E, 0x8A, 0x18)
CHARCOAL = RGBColor(0x2B, 0x2F, 0x36)
MIST = RGBColor(0xE9, 0xEB, 0xEF)
INK = RGBColor(0x1A, 0x1D, 0x26)
SOFT = RGBColor(0x4A, 0x52, 0x68)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Avenir Next"

# Student-visible display labels for anchor chips. Internal codes (BQ_NOW, RECOVER)
# are never rendered raw; the visible chip uses a clean label.
DISPLAY_LABELS = {
    "BQ": "BQ",
    "V1": "V1",
    "N1": "N1",
    "N2": "N2",
    "N3": "N3",
    "N4": "N4",
    "DEMO": "DEMO",
    "LAB": "LAB",
    "GRAPH": "GRAPH",
    "CHECK": "CHECK",
    "BQ_NOW": "BQ NOW",
    "DROP": "DROP IT",
    "RECOVER": "RECOVER",
}

# Student-visible lines. Reveal slides are the first place an answer word appears.
BODY = {
    "S01": ["Energy and Speed Are Related", "How are energy and speed related?"],
    "S02": ["How are energy and speed related?", "Turn and talk. We will collect evidence before we answer."],
    "S03": ["My first thinking", "Write one idea. There is no missing word yet."],
    "S04": ["One ball.", "A gentle catch, then a hard catch.", "Which catch did more to your hand?"],
    "S05": ["speed", "a measurement of the ________ an object travels over an amount of time.", "Reader p. 13"],
    "S06": ["Write the missing word on V1.", "speed — a measurement of the ________ an object travels over an amount of time."],
    "S07": ["speed — a measurement of the distance an object travels over an amount of time."],
    "S08": ["One ball at two speeds.", "You decide from what you observe.", "BALL  →  OBSERVE  →  EVIDENCE"],
    "S09": ["Write both missing words.", "Compare the ________ ball at two speeds.", "A bigger ________ is how we know the faster ball had more energy of motion."],
    "S10": ["Compare the same ball at two speeds.", "A bigger change is how we know the faster ball had more energy of motion."],
    "S11": ["Preview. One ball.", "Low setup, then a steeper setup.", "Which cup move was bigger?", "Do not measure. Do not write a speed number."],
    "S12": ["Tomorrow we measure the ramp height and how far the target moves.", "We use centimeters.", "We do not write a speed number."],
    "S13": ["Exit. One sentence about one ball.", "Not graded."],
    "S14": ["How are energy and speed related?", "What have we already observed?"],
    "S15": ["A fair test changes one thing.", "Keep one ball."],
    "S16": ["Write the missing words.", "We measure ramp ________ in centimeters.", "We measure how far the ________ moves in centimeters.", "We do not measure a speed number.", "The one thing we change is ramp ________.", "We keep the ________ ball."],
    "S17": ["We measure ramp height in centimeters.", "We measure how far the cup moves in centimeters.", "We do not measure a speed number.", "The one thing we change is ramp height.", "We keep the same ball."],
    "S18": ["Calibration trial.", "Roll the ball once.", "Do not record that roll."],
    "S19": ["Measure the vertical ramp for 1 book, 2 books, and 3 books.", "Write the centimeters."],
    "S20": ["Three recorded trials at each setup.", "Nine recorded trials.", "Write how far the cup moves, in centimeters."],
    "S21": ["Stop recording.", "Averages and the graph come next."],
    "S22": ["How are energy and speed related?"],
    "S23": ["Average the three cup measurements at each setup."],
    "S24": ["Graph axes", "Ramp height (cm)", "Average cup movement (cm)", "Do not label an axis as speed."],
    "S25": ["Plot your three averages.", "Use your own measurements."],
    "S26": ["Challenge", "Move the cup as close as you can to 30 cm without going past."],
    "S27": ["You may change the ramp.", "Keep one ball.", "Do not write a speed number."],
    "S28": ["Which setup moved the cup farther?", "A farther cup move is a bigger change."],
    "S29": ["Reader pages 15 and 16.", "How are energy and speed related?"],
    "S30": ["A steeper ramp. One ball.", "The Reader tells us what happens when the same ball rolls down a steeper ramp.", "Watch how far the cup or bucket moves."],
    "S31": ["Write the missing words.", "Objects pick up more ________ on steeper ramps.", "From the steeper ramp, that ball made a ________ change."],
    "S32": ["Objects pick up more speed on steeper ramps.", "From the steeper ramp, that ball made a greater change."],
    "S33": ["A soft bounce. A hard bounce.", "Which bounce went farther up?"],
    "S34": ["Write the missing word.", "The faster ball bounced ________ than the slower ball."],
    "S35": ["The faster ball bounced higher than the slower ball.", "A louder sound is also a bigger change."],
    "S36": ["Check your thinking.", "How are energy and speed related?", "Name the ball you kept and one change that was bigger."],
    "S37": ["Sample: That ball had more energy of motion when it caused a greater change.", "I did not measure a speed number."],
    "S38": ["Now I think", "How are energy and speed related?", "Write your answer."],
    "S39": ["Exit. Not graded.", "Look for one ball and a bigger change."],
    "S40": ["FLEX  ·  Drop It", "Same ball. Two drop heights. Compare the craters.", "This does not teach a new idea."],
    "S41": ["FLEX", "Finish the notes, practice, or take the quiz.", "The quiz is not a first lesson."],
}

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
# python-pptx preserves the template's legacy screen4x3 type token even after
# setting 16:9 dimensions. Keep the package metadata truthful for projection
# QA and downstream consumers.
prs._element.sldSz.set("type", "screen16x9")
BLANK = prs.slide_layouts[6]


def rect(slide, x, y, w, h, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.adjustments[0] = 0.08
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def write(shape, text, size, color, bold=False, align=PP_ALIGN.LEFT):
    frame = shape.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    frame.margin_left = Inches(0.12)
    frame.margin_right = Inches(0.12)
    p = frame.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = FONT


def textbox(slide, x, y, w, h, lines, size, color, bold=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    for index, line in enumerate(lines):
        p = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(10)
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = FONT
    return box


def build():
    sessions = {row["id"]: row for row in SPEC["sessions"]}
    titles = {row["code"]: row["title"] for row in SPEC["anchors"]}
    if list(BODY) != [row["id"] for row in SPEC["slides"]]:
        raise SystemExit("slide body map does not match the spec")
    for row in SPEC["slides"]:
        slide = prs.slides.add_slide(BLANK)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = PRIMARY if row["id"] == "S01" else WHITE
        bg.line.fill.background()
        bg.shadow.inherit = False
        lines = BODY[row["id"]]
        session = sessions[row["session"]]
        if row["id"] == "S01":
            tab = rect(slide, 0.6, 0.58, 4.2, 0.46, ACCENT)
            write(tab, "CHAPTER 3  ·  WEEK 2", 14, WHITE, True, PP_ALIGN.CENTER)
            textbox(slide, 0.7, 1.5, 11.5, 1.3, [lines[0]], 44, WHITE, True)
            textbox(slide, 0.7, 3.1, 11.5, 1.0, [lines[1]], 28, MIST, True)
            textbox(slide, 0.7, 5.6, 11.5, 0.6, ["Measurement / Data"], 20, MIST)
        else:
            tab = rect(slide, 0.6, 0.58, 5.3, 0.4, PRIMARY)
            write(tab, "CHAPTER 3  ·  ENERGY AND SPEED", 12, WHITE, True, PP_ALIGN.CENTER)
            label = DISPLAY_LABELS.get(row["anchor"], row["anchor"])
            chip_w = max(1.5, 0.20 * len(label) + 0.55)
            chip = rect(slide, 0.6, 1.15, chip_w, 0.46, ACCENT)
            chip.text_frame.word_wrap = False
            write(chip, label, 16, WHITE, True, PP_ALIGN.CENTER)
            textbox(slide, 0.75 + chip_w, 1.1, 10.1 - chip_w, 0.56, [titles.get(row["anchor"], row["task"])], 28, PRIMARY, True)
            status = row.get("status") or session["status"]
            badge = rect(slide, 11.0, 0.58, 1.7, 0.4, CHARCOAL if status == "FLEX" else ACCENT)
            write(badge, status, 14, WHITE, True, PP_ALIGN.CENTER)
            textbox(slide, 0.6, 1.85, 12.1, 4.9, lines, 28, INK, True)
        note = "\n".join([
            "ANCHOR %s" % row["anchor"],
            "TIME %g min" % row["minutes"],
            "PLAN Session %d · %s · %s" % (row["session"], session["date"], session["status"]),
            "SAY %s" % row["speakerNote"],
        ])
        slide.notes_slide.notes_text_frame.text = note
    prs.save(OUT)
    print(OUT, len(SPEC["slides"]))


if __name__ == "__main__":
    build()
