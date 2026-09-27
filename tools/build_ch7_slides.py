"""Build Chapter 7 Edison + Unit Synthesis slide deck (PPTX, 16:9)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT = os.path.join(os.path.dirname(__file__), '..', 'production', 'slides')

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
TEAL = RGBColor(0x2E, 0x6E, 0x8E)
AMBER = RGBColor(0xD9, 0xA4, 0x41)
GREEN = RGBColor(0x3E, 0x8E, 0x5A)
RED = RGBColor(0xC0, 0x4A, 0x4A)
LIGHT = RGBColor(0xF5, 0xF3, 0xEC)
INK = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x55, 0x55, 0x55)
PALE = RGBColor(0xD5, 0xDE, 0xEA)

CUE_COLORS = {
    "NOTEBOOK": RGBColor(0x6B, 0x4F, 0xA0),
    "WRITE": RGBColor(0x2E, 0x6E, 0x8E),
    "DRAW": RGBColor(0x3E, 0x8E, 0x5A),
    "LABEL": RGBColor(0xD9, 0xA4, 0x41),
    "THINK": RGBColor(0xC0, 0x4A, 0x4A),
    "REVIEW": RGBColor(0x6B, 0x4F, 0xA0),
}

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def add_slide():
    return prs.slides.add_slide(BLANK)

def rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill; sp.line.fill.background(); sp.shadow.inherit = False
    return sp

def textbox(slide, x, y, w, h, text, size=24, color=INK, bold=False, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = line
        r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = color; r.font.name = "Arial"
    return tb

def cue_badge(slide, cue):
    if not cue: return
    c = CUE_COLORS.get(cue, GRAY)
    sp = rect(slide, 12.25, 0.25, 0.9, 0.5, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = sp.text_frame; tf.word_wrap = False; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = cue
    r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Arial"

def model_strip(slide, items, y=5.6, x=0.8, w=11.7, box_h=0.7, gap=0.3):
    n = len(items); box_w = (w - (n - 1) * gap) / n; cx = x
    for i, it in enumerate(items):
        sp = rect(slide, cx, y, box_w, box_h, NAVY if i == 0 else (AMBER if i == n - 1 else TEAL),
                  shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        tf = sp.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = it
        r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Arial"
        if i < n - 1:
            ar = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(cx + box_w + 0.02),
                                        Inches(y + box_h / 2 - 0.12), Inches(gap - 0.04), Inches(0.24))
            ar.fill.solid(); ar.fill.fore_color.rgb = GRAY; ar.line.fill.background(); ar.shadow.inherit = False
        cx += box_w + gap

def header(slide, title, subtitle, cue=None, num=None):
    rect(slide, 0, 0, 13.333, 1.0, NAVY)
    textbox(slide, 0.5, 0.12, 11.6, 0.75, title, size=30, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if subtitle:
        textbox(slide, 0.5, 0.86, 11.6, 0.3, subtitle, size=13, color=PALE)
    if num:
        textbox(slide, 11.4, 0.32, 0.7, 0.4, str(num), size=14, color=PALE, align=PP_ALIGN.RIGHT)
    cue_badge(slide, cue)

def body(slide, lines, x=0.8, y=1.5, w=11.7, h=3.9, size=24, gap=8):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.color.rgb = INK; r.font.name = "Arial"
    return tb

def concept(title, subtitle, lines, cue=None, num=None, strip=None, size=24):
    s = add_slide()
    rect(s, 0, 0, 13.333, 7.5, LIGHT)
    header(s, title, subtitle, cue, num)
    body(s, lines, size=size)
    if strip:
        model_strip(s, strip)
    return s

CYCLE = ["PROBLEM", "DESIGN", "TEST", "EVIDENCE", "IMPROVE"]

# ===== Title + Big Question =====
s = add_slide(); rect(s, 0, 0, 13.333, 7.5, NAVY)
textbox(s, 0.8, 2.0, 11.7, 1.2, "Solving Problems and Designing Solutions", size=44, color=WHITE, bold=True)
textbox(s, 0.8, 3.2, 11.7, 0.6, "Thomas A. Edison · Chapter 7 · Grade 4 · Week 9", size=20, color=PALE)
model_strip(s, CYCLE, y=5.0)

s = add_slide(); rect(s, 0, 0, 13.333, 7.5, LIGHT)
rect(s, 0, 2.6, 13.333, 2.2, NAVY)
textbox(s, 0.8, 2.75, 11.7, 1.9, "How did Thomas Edison use his knowledge of energy transfer and transformation to solve problems?",
        size=30, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.8, 2.0, 11.7, 0.5, "Big Question", size=16, color=GRAY, align=PP_ALIGN.CENTER)

# ===== Chapter 7 content =====
concept("The problem", "Life before light bulbs",
        ["Before light bulbs, people lit the dark with open flames — torches, candles, oil lanterns.",
         "Open flames can be unsafe. Early bulbs burned out fast and cost too much."],
        num=3, strip=["PROBLEM", "UNSAFE LIGHT", "→ SOLVE IT"])
concept("Edison saw a chance", "Improve, don't invent",
        ["Edison did NOT invent the first light bulb. Other engineers had already built bulbs.",
         "He improved their designs — safer, longer-lasting, more affordable."],
        num=4, strip=["EXISTING BULB", "→", "BETTER BULB"])
concept("Testing materials", "More than 6,000 materials",
        ["Edison's team tested more than six thousand materials for a filament.",
         "They wanted a material that glows a long time without burning up — and costs less."],
        cue="THINK", num=5, strip=["TEST", "EVIDENCE", "REPEAT"])
concept("The solution", "1879 — bamboo + carbon",
        ["In 1879, a bamboo filament coated with carbon worked.",
         "Electrical energy transformed to light energy."],
        num=6, strip=["ELECTRICAL", "→ LIGHT", "BULB GLOWS"])
concept("The filament", "Where the change happens",
        ["The filament is the wire in a bulb that glows when electricity moves through it.",
         "The glass protects the filament."],
        cue="LABEL", num=7)
concept("Persistence", "Keep trying",
        ["'I haven't failed. I've just found ten thousand ways that won't work.'",
         "Persistence = keep trying to solve a problem, even when you find ways that don't work."],
        num=8, strip=["FAILURE", "= DATA", "KEEP GOING"])
concept("Not alone", "Lewis Howard Latimer",
        ["Latimer improved Edison's bulb — securing the wire to the filament,",
         "and making the filament stronger and longer-lasting. Design improves over time."],
        num=9)
concept("Beyond light bulbs", "The alkaline battery",
        ["In 1901, Edison made the first alkaline battery — lighter and more powerful.",
         "His electric-car idea did not succeed then, but his battery still affects your life."],
        num=10, strip=["STORED", "→ ELECTRICAL", "POWER DEVICES"])
concept("Design never ends", "Incandescent → CFL → LED",
        ["Each new design improves an earlier one: less electricity, less heat, longer life.",
         "As long as there are problems, people keep designing solutions."],
        num=11, strip=["IMPROVE", "→", "IMPROVE AGAIN"])

# ===== Engineering cycle notebook =====
concept("Notebook — Insert 1", "Engineering is a cycle",
        ["PROBLEM → DESIGN → TEST → EVIDENCE → IMPROVE.",
         "Add one Edison example and one example from your own tabletop device."],
        cue="NOTEBOOK", num=12, strip=CYCLE)

# ===== Unit retrieval (Ch.1-6) =====
concept("Review — Chapter 1", "Energy causes change",
        ["Energy = the ability to cause change.", "We see a change → we infer energy was involved.",
         "ENERGY → CHANGE → EVIDENCE."],
        cue="REVIEW", num=13, strip=["ENERGY", "CHANGE", "EVIDENCE"])
concept("Review — Chapter 2", "Moving objects have energy",
        ["A moving object has energy of motion.", "It can cause a change when it hits or pushes."],
        cue="REVIEW", num=14)
concept("Review — Chapter 3", "Same object, different speed",
        ["For the SAME object, faster = more energy of motion = bigger change.",
         "We MEASURE ramp height and cup movement; we INFER the speed."],
        cue="REVIEW", num=15, strip=["SAME OBJECT", "FASTER", "BIGGER CHANGE"])
concept("Review — Chapter 4", "Energy transfers",
        ["Energy transfers by sound, light, heat, and electric current.",
         "TRANSFER = energy moves place/object. TRANSFORMATION = form changes."],
        cue="REVIEW", num=16, strip=["TRANSFER", "TRANSFORMATION", "BOTH"])
concept("Review — Chapter 5", "Collisions transfer energy",
        ["In a collision, energy of motion transfers to the target — and some becomes sound.",
         "Energy does NOT disappear."],
        cue="REVIEW", num=17, strip=["MOTION", "→ TARGET", "+ SOUND"])
concept("Review — Chapter 6", "Transformations + engineering",
        ["INPUT → TRANSFORMATION → OUTPUT. Engineers solve problems with energy changes,",
         "judged by criteria under constraints."],
        cue="REVIEW", num=18, strip=["INPUT", "TRANSFORMATION", "OUTPUT"])

# ===== Unit synthesis =====
concept("Notebook — Insert 2", "Energy Unit Concept Map",
        ["Center: ENERGY. Branches: causes change · motion · speed · transfer · collisions ·",
         "transformation · engineering. Add one example under each."],
        cue="NOTEBOOK", num=19)
concept("Data / graph review", "Same-object speed",
        ["Read a ramp-height vs cup-displacement table.",
         "What pattern do you see? What do we measure vs infer?"],
        cue="REVIEW", num=20, strip=["RAMP HEIGHT ↑", "→", "CUP MOVEMENT ↑"])
concept("Transfer / Transformation / BOTH", "Retrieval sort",
        ["Classify: warm spoon · flashlight · dominoes · buzzer · toy-car collision.",
         "State the system boundary first."],
        cue="REVIEW", num=21, strip=["TRANSFER", "TRANSFORMATION", "BOTH"])
concept("Fair test", "One thing at a time",
        ["A fair test changes ONE thing and keeps everything else the same.",
         "That way we know what caused the change."],
        cue="REVIEW", num=22, strip=["CHANGE ONE", "KEEP REST SAME", "COMPARE"])
concept("Criteria & constraints", "Engineering review",
        ["Criteria = what a good solution must do.", "Constraints = the limits (materials, time, safety)."],
        cue="REVIEW", num=23, strip=["CRITERIA", "CONSTRAINTS", "SOLUTION"])

# ===== Assessment + close =====
concept("Assessment expectations", "What to expect",
        ["Multiple choice · diagrams · data tables · graph reading · short answers · one CER.",
         "Show your evidence. Use your Core Vocabulary cards if allowed."],
        num=24, strip=["READ", "SHOW EVIDENCE", "EXPLAIN"])
concept("Correction process", "Learn from mistakes",
        ["MISSED ITEM → ORIGINAL THINKING → CORRECT IDEA → EVIDENCE → NEW EXAMPLE.",
         "Corrections are about learning, not punishment."],
        num=25, strip=["MISSED", "EVIDENCE", "REPAIR"])
concept("Unit closure", "From change to engineering",
        ["ENERGY → CHANGE → EVIDENCE → ENGINEERING.",
         "Notebook Insert 3 — Unit Reflection: something I can explain, strong evidence,",
         "one improvement, one question."],
        cue="NOTEBOOK", num=26, strip=["ENERGY", "CHANGE", "ENGINEERING"])

prs.save(os.path.join(OUT, "07-ch7-edison-unit-synthesis-slides.pptx"))
print("built slides:", len(prs.slides._sldIdLst))
