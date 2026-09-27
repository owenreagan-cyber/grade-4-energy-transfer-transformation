"""Build the Chapter 1 note-system teaching-comparison slide deck (16:9, matched INB vs Guided Notes)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

OUT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "production",
    "comparisons", "chapter-01-notes", "01-ch1-note-system-teaching-comparison.pptx"))

NAVY = RGBColor(0x2F, 0x3C, 0x7E)
NAVY_D = RGBColor(0x1F, 0x29, 0x55)
CORAL = RGBColor(0xF9, 0x61, 0x67)
GOLD = RGBColor(0xE8, 0xC5, 0x4A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1F, 0x1F, 0x1F)
GRAY = RGBColor(0x55, 0x55, 0x55)
LIGHT = RGBColor(0xEA, 0xEC, 0xF5)
MINT = RGBColor(0x3B, 0xA7, 0x8D)

HEAD = "Cambria"
BODY = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5


def slide(bg=None):
    s = prs.slides.add_slide(BLANK)
    if bg:
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        r.fill.solid(); r.fill.fore_color.rgb = bg
        r.line.fill.background()
        no_shadow(r)
    return s


def no_shadow(shape):
    try:
        shape.shadow.inherit = False
    except Exception:
        pass
    return shape


def txt(s, x, y, w, h, runs, size=30, color=INK, bold=False, align=PP_ALIGN.LEFT,
        font=BODY, anchor=MSO_ANCHOR.TOP, line_spacing=1.0, wrap=True):
    """runs: str or list of (text, dict-overrides)."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    if isinstance(runs, str):
        runs = [(runs, {})]
    first = True
    for text, ov in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = ov.get("align", align)
        p.line_spacing = ov.get("line_spacing", line_spacing)
        r = p.add_run(); r.text = text
        f = r.font
        f.size = Pt(ov.get("size", size))
        f.bold = ov.get("bold", bold)
        f.color.rgb = ov.get("color", color)
        f.name = ov.get("font", font)
    return tb


def chip(s, x, y, d, fill, label, label_size=22, label_color=WHITE, bold=True):
    c = no_shadow(s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d)))
    c.fill.solid(); c.fill.fore_color.rgb = fill
    c.line.color.rgb = fill
    tf = c.text_frame
    tf.word_wrap = False
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(label_size); r.font.bold = bold; r.font.color.rgb = label_color; r.font.name = BODY
    return c


def card(s, x, y, w, h, fill=LIGHT, line=None):
    c = no_shadow(s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)))
    c.fill.solid(); c.fill.fore_color.rgb = fill
    if line:
        c.line.color.rgb = line; c.line.width = Pt(1.5)
    else:
        c.line.fill.background()
    return c


def arrow(s, x, y, w, h, color=CORAL):
    a = no_shadow(s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h)))
    a.fill.solid(); a.fill.fore_color.rgb = color
    a.line.fill.background()
    return a


# ============================================================
# Slide 1 — Title
# ============================================================
s = slide(NAVY_D)
txt(s, 1.0, 2.0, 11.3, 1.6, "Chapter 1 Note Systems", size=54, color=WHITE, bold=True, font=HEAD)
txt(s, 1.0, 3.5, 11.3, 1.0, "INB vs Guided Notes — Teaching Comparison", size=30, color=GOLD, bold=False)
txt(s, 1.0, 4.7, 11.3, 0.6, "Grade 4 · Energy Transfer & Transformation · same content, two formats", size=20, color=RGBColor(0xC9, 0xCE, 0xE8))


def step_slide(step_no, step_name, instruction, tag_color, diagram):
    s = slide(WHITE)
    # header band area (no stripe): number chip + title
    chip(s, 0.9, 0.8, 1.3, NAVY, str(step_no), label_size=40)
    txt(s, 2.5, 0.75, 9.5, 0.5, step_name, size=40, color=NAVY, bold=True, font=HEAD)
    txt(s, 2.5, 1.45, 9.5, 0.5, "STUDENT-FACING", size=22, color=CORAL, bold=True)
    txt(s, 0.9, 2.4, 11.5, 1.2, instruction, size=30, color=INK, bold=False)
    diagram(s)
    return s


def flow_ribbon(s, steps, x=0.9, y=5.6, w=11.5, color=NAVY):
    n = len(steps)
    gap = 0.35
    cellw = (w - gap * (n - 1)) / n
    for i, st in enumerate(steps):
        cx = x + i * (cellw + gap)
        card(s, cx, y, cellw, 1.0, fill=color if i == 0 else LIGHT)
        txt(s, cx, y + 0.18, cellw, 0.6, st, size=22,
            color=WHITE if i == 0 else NAVY, bold=True, align=PP_ALIGN.CENTER)
        if i < n - 1:
            arrow(s, cx + cellw + 0.02, y + 0.32, gap - 0.04, 0.36, color=CORAL)


# ============================================================
# Slide 2 — INB section divider
# ============================================================
s = slide(NAVY)
txt(s, 1.0, 1.0, 11.3, 0.6, "FORMAT A", size=24, color=GOLD, bold=True)
txt(s, 1.0, 1.7, 11.3, 1.3, "Interactive Science Notebook", size=52, color=WHITE, bold=True, font=HEAD)
txt(s, 1.0, 3.1, 11.3, 0.8, "Trimmed inserts glued into a composition book", size=28, color=RGBColor(0xC9, 0xCE, 0xE8))
flow_ribbon(s, ["NOTEBOOK", "TRIM/GLUE", "WRITE", "DRAW", "REVEAL"], color=NAVY_D, y=4.9)

# ============================================================
# Slide 3 — INB NOTEBOOK
# ============================================================
def d_inb_notebook(s):
    # composition book mock
    card(s, 2.0, 3.8, 2.6, 1.7, fill=WHITE, line=NAVY)
    txt(s, 2.0, 4.15, 2.6, 1.0, "SCIENCE\nNOTEBOOK", size=20, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 5.0, 4.35, 1.0, 0.6, color=CORAL)
    txt(s, 6.4, 3.9, 5.0, 1.6, "Open to the next\nblank page.", size=28, color=INK)
step_slide(1, "NOTEBOOK", "Get your composition book and find the next blank page.", NAVY, d_inb_notebook)

# ============================================================
# Slide 4 — INB TRIM/GLUE
# ============================================================
def d_inb_trim(s):
    c = card(s, 1.6, 3.8, 3.6, 1.7, fill=LIGHT, line=GRAY)
    # dashed trim look: inner dashed rectangle
    txt(s, 1.6, 4.2, 3.6, 0.8, "INSERT\n(trim on dashed line)", size=20, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 5.5, 4.35, 1.0, 0.6, color=CORAL)
    txt(s, 6.9, 3.9, 5.4, 1.6, "Cut on the dashed line,\nthen glue the top edge.", size=28, color=INK)
step_slide(2, "TRIM / GLUE", "Cut on the dashed line. Glue only the top edge into your notebook.", CORAL, d_inb_trim)

# ============================================================
# Slide 5 — INB WRITE
# ============================================================
def d_inb_write(s):
    card(s, 1.8, 4.0, 4.4, 1.5, fill=WHITE, line=NAVY)
    txt(s, 2.1, 4.15, 3.8, 1.2, "Energy is the ability\nto cause ________.", size=24, color=INK)
    arrow(s, 6.6, 4.4, 1.0, 0.6, color=CORAL)
    txt(s, 8.0, 4.0, 4.0, 1.4, "Fill in the blanks\nwith the class.", size=28, color=INK)
step_slide(3, "WRITE", "Fill in the vocabulary blanks together with the class.", GOLD, d_inb_write)

# ============================================================
# Slide 6 — INB DRAW
# ============================================================
def d_inb_draw(s):
    card(s, 1.6, 3.9, 2.6, 1.6, fill=WHITE, line=NAVY)
    txt(s, 1.6, 4.1, 2.6, 0.4, "BEFORE", size=24, color=CORAL, bold=True, align=PP_ALIGN.CENTER)
    card(s, 4.5, 3.9, 2.6, 1.6, fill=WHITE, line=NAVY)
    txt(s, 4.5, 4.1, 2.6, 0.4, "AFTER", size=24, color=CORAL, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 7.5, 4.4, 1.0, 0.6, color=CORAL)
    txt(s, 8.9, 3.9, 3.5, 1.6, "Draw what changed\nbefore and after.", size=28, color=INK)
step_slide(4, "DRAW", "Draw one change: before and after.", NAVY, d_inb_draw)

# ============================================================
# Slide 7 — INB REVEAL
# ============================================================
def d_inb_reveal(s):
    card(s, 1.6, 3.9, 3.0, 1.6, fill=GOLD)
    txt(s, 1.6, 4.05, 3.0, 0.5, "LIFT THE FLAP", size=24, color=INK, bold=True, align=PP_ALIGN.CENTER)
    txt(s, 1.6, 4.55, 3.0, 0.8, "the light\nturns on", size=22, color=INK, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 5.0, 4.4, 1.0, 0.6, color=CORAL)
    txt(s, 6.4, 3.9, 5.2, 1.6, "Lift the flap to reveal\nwhat stored energy can do later.", size=28, color=INK)
step_slide(5, "REVEAL", "Lift the flap to reveal the change stored energy can cause.", CORAL, d_inb_reveal)

# ============================================================
# Slide 8 — GUIDED section divider
# ============================================================
s = slide(NAVY)
txt(s, 1.0, 1.0, 11.3, 0.6, "FORMAT B", size=24, color=GOLD, bold=True)
txt(s, 1.0, 1.7, 11.3, 1.3, "Full-Size Guided Notes", size=52, color=WHITE, bold=True, font=HEAD)
txt(s, 1.0, 3.1, 11.3, 0.8, "Students write directly on a US Letter sheet", size=28, color=RGBColor(0xC9, 0xCE, 0xE8))
flow_ribbon(s, ["NOTES", "WRITE", "DRAW", "CHECK"], color=NAVY_D, y=4.9)

# ============================================================
# Slide 9 — GUIDED NOTES
# ============================================================
def d_gn_notes(s):
    card(s, 2.0, 3.9, 2.6, 1.7, fill=WHITE, line=NAVY)
    txt(s, 2.0, 4.2, 2.6, 1.0, "GUIDED\nNOTES\n(page 1)", size=20, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 5.0, 4.4, 1.0, 0.6, color=CORAL)
    txt(s, 6.4, 3.9, 5.0, 1.6, "Pass out one sheet\n(3 pages total).", size=28, color=INK)
step_slide(1, "NOTES", "Get your guided-notes sheet — no cutting, no gluing.", NAVY, d_gn_notes)

# ============================================================
# Slide 10 — GUIDED WRITE
# ============================================================
def d_gn_write(s):
    card(s, 1.8, 4.0, 4.4, 1.5, fill=WHITE, line=NAVY)
    txt(s, 2.1, 4.15, 3.8, 1.2, "Energy is the ability\nto cause ________.", size=24, color=INK)
    arrow(s, 6.6, 4.4, 1.0, 0.6, color=CORAL)
    txt(s, 8.0, 4.0, 4.0, 1.4, "Fill in the blanks\nwith the class.", size=28, color=INK)
step_slide(2, "WRITE", "Fill in the vocabulary blanks together with the class.", GOLD, d_gn_write)

# ============================================================
# Slide 11 — GUIDED DRAW
# ============================================================
def d_gn_draw(s):
    card(s, 1.6, 3.9, 2.6, 1.6, fill=WHITE, line=NAVY)
    txt(s, 1.6, 4.1, 2.6, 0.4, "BEFORE", size=24, color=CORAL, bold=True, align=PP_ALIGN.CENTER)
    card(s, 4.5, 3.9, 2.6, 1.6, fill=WHITE, line=NAVY)
    txt(s, 4.5, 4.1, 2.6, 0.4, "AFTER", size=24, color=CORAL, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 7.5, 4.4, 1.0, 0.6, color=CORAL)
    txt(s, 8.9, 3.9, 3.5, 1.6, "Draw what changed\nbefore and after.", size=28, color=INK)
step_slide(3, "DRAW", "Draw one change: before and after.", NAVY, d_gn_draw)

# ============================================================
# Slide 12 — GUIDED CHECK
# ============================================================
def d_gn_check(s):
    card(s, 2.0, 3.9, 2.8, 1.6, fill=MINT)
    txt(s, 2.0, 4.35, 2.8, 0.7, "✓ CHECK", size=30, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 5.2, 4.4, 1.0, 0.6, color=CORAL)
    txt(s, 6.6, 3.9, 5.2, 1.6, "Check your answers\nas a class.", size=28, color=INK)
step_slide(4, "CHECK", "Check your answers together — keep the sheet in your folder.", MINT, d_gn_check)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
