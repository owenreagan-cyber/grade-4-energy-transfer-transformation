"""Build Chapter 1 "Energy Causes Change" — PREMIUM HYBRID candidate (PPTX, 16:9).

Phase 5B / Gate 2. A visual reconstruction of the FROZEN canonical deck v1.1.
Instructional text, sequence, speaker notes, and write/check behavior are preserved
verbatim from tools/build_ch1_slides.py. Premium additions: Georgia display type and
the Phase 5A-approved text-free raster photography (Codex v5 + standalone). New
candidate only — does not touch the frozen deck, Guided Notes, or teacher key.

Run: .venv/bin/python tools/build_ch1_premium_slides.py
Then: soffice --headless --convert-to pdf  (see render step)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ch1_pacing as PACE   # SINGLE authoritative Ch1 timing source (Phase 6.1 / F1)

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v1")
STAGE = os.path.join(OUT, "assets")
os.makedirs(STAGE, exist_ok=True)

# Premium asset sources (Phase 5A provisional selections; text-free, OCR-verified).
ASSET_DIR = os.path.join(ROOT, "assets", "ch1", "candidate-v2")
INTAKE_DIR = os.path.join(ROOT, "source-intake", "2026-10-09-chapter-1", "images")

def _crop(src, box, dst):
    """Deterministic crop (left, upper, right, lower) → staging file. Returns path."""
    im = Image.open(src).convert("RGB")
    im = im.crop(box)
    p = os.path.join(STAGE, dst)
    im.save(p)
    return p

def _pic_fit(s, path, x, y, w, h, center=True):
    """Insert image, aspect-FIT within (x,y,w,h); letterbox with slide background (no distortion)."""
    im = Image.open(path)
    iw, ih = im.size
    ar = iw / ih
    bw, bh = w, h
    if ar > bw / bh:
        nw = bw; nh = bw / ar
    else:
        nh = bh; nw = bh * ar
    px = x + (w - nw) / 2 if center else x
    py = y + (h - nh) / 2 if center else y
    s.shapes.add_picture(path, Inches(px), Inches(py), Inches(nw), Inches(nh))
    return (px, py, nw, nh)

# Crop the 3-panel / 2-panel strips once into staging.
_pen = os.path.join(ASSET_DIR, "slide-09-pencil-before-after.png")   # 1942x809 (2 panels)
_pen_before = _crop(_pen, (0, 0, 971, 809), "pencil-before.png")
_pen_after  = _crop(_pen, (971, 0, 1942, 809), "pencil-after.png")
_db  = os.path.join(ASSET_DIR, "slide-04-dark-bright.png")            # 1672x941 (2 panels)
_db_dark   = _crop(_db, (0, 0, 836, 941), "dark.png")
_db_bright = _crop(_db, (836, 0, 1672, 941), "bright.png")
_store = os.path.join(ASSET_DIR, "slide-25-stored-examples.png")      # 2172x724 (3 panels)
_store_battery = _crop(_store, (0, 0, 724, 724), "stored-battery.png")
_store_rubber  = _crop(_store, (724, 0, 1448, 724), "stored-rubber.png")
_store_apple   = _crop(_store, (1448, 0, 2172, 724), "stored-apple.png")

def _img(name):
    return os.path.join(ASSET_DIR, name)

# ---------------------------------------------------------------- FROZEN Ch1 tokens
PRIMARY = RGBColor(0x1F, 0x2A, 0x5A)   # deep navy
ACCENT  = RGBColor(0xA6, 0x7C, 0x16)   # warm gold
NEUTRAL = RGBColor(0x7A, 0x56, 0x20)   # muted amber
SURFACE = RGBColor(0xF5, 0xEE, 0xDC)   # cream
INK     = RGBColor(0x1A, 0x1D, 0x26)
INK_SOFT= RGBColor(0x4A, 0x52, 0x68)
PAPER   = RGBColor(0xFF, 0xFF, 0xFF)
MIST    = RGBColor(0xF6, 0xF7, 0xF9)
RULE    = RGBColor(0xD8, 0xDC, 0xE4)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)

# gold 10% tint (card definition/visual panel) — a light warm fill
GOLD_TINT = RGBColor(0xF3, 0xE8, 0xCF)
NAVY_TINT = RGBColor(0xE3, 0xE7, 0xF2)

FONT = "Avenir Next"
FONT_DISPLAY = "Georgia"   # Phase 5A verified display face (installed; headless-safe)

# Type scale (task §4 + frozen tokens)
T_MAJOR  = 48   # chapter title
T_TITLE  = 40   # slide title
T_HEAD   = 32   # notes section heading
T_BODY   = 30   # instructional body
T_BODY_S = 28   # body (denser lines)
T_OPT    = 28   # MCQ options
T_DEF    = 28   # vocab definition on card
T_KICK   = 24   # kicker / subtitle / Reader-page instruction
T_PAGE   = 16   # Reader page refs
T_TAB    = 12   # chapter tab / chrome
T_HUD    = 24   # HUD bubble text (action word students must read)

CHAPTER_TAB = "CHAPTER 1 · ENERGY CAUSES CHANGE"

# ---------------------------------------------------------------- presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
# Widescreen metadata (F14): python-pptx's default template stamps type="screen4x3" on a 16:9 deck.
_sz = prs.part._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}sldSz')
if _sz is not None and 'type' in _sz.attrib:
    del _sz.attrib['type']
BLANK = prs.slide_layouts[6]

SLIDE_NO = [0]  # mutable counter

def new_slide(bg=SURFACE):
    SLIDE_NO[0] += 1
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg
    r.line.fill.background(); r.shadow.inherit = False
    return s

# ---------------------------------------------------------------- low-level helpers
def rect(s, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, line_color=None, line_w=None, rounded=False):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else shape,
                            Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        try:
            sp.adjustments[0] = 0.08
        except Exception:
            pass
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line_color is not None:
        sp.line.color.rgb = line_color
        sp.line.width = Pt(line_w or 1.25)
    else:
        sp.line.fill.background()
    sp.shadow.inherit = False
    return sp

def tb(s, x, y, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    return box, tf

def run(p, text, size=T_BODY, color=INK, bold=False, italic=False, underline=False, font=FONT, caps=False):
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font
    if underline:
        r.font.underline = True
    if caps:
        r.font.caps = True
    return r

def text(s, x, y, w, h, lines, size=T_BODY, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, italic=False, gap=10, caps=False, font=FONT):
    """lines = str or list of str (each becomes a paragraph)."""
    if isinstance(lines, str):
        lines = [lines]
    box, tf = tb(s, x, y, w, h, anchor=anchor)
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(gap)
        run(p, ln, size=size, color=color, bold=bold, italic=italic, caps=caps, font=font)
    return box

def rich(s, x, y, w, h, segs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, gap=12):
    """segs = list of paragraphs; each paragraph = list of (text, fmt_dict)."""
    box, tf = tb(s, x, y, w, h, anchor=anchor)
    for i, para_segs in enumerate(segs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(gap)
        for (txt, fmt) in para_segs:
            run(p, txt, size=fmt.get('size', T_BODY), color=fmt.get('color', INK),
                bold=fmt.get('bold', False), italic=fmt.get('italic', False),
                underline=fmt.get('underline', False))
    return box

def blank_str(n):
    return "_" * n

# ---------------------------------------------------------------- chrome / header
def chapter_tab(s, x=0.55, y=0.40, w=3.55, h=0.44):
    sp = rect(s, x, y, w, h, PRIMARY, rounded=True)
    tf = sp.text_frame; tf.word_wrap = False; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.12); tf.margin_right = Inches(0.12)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, CHAPTER_TAB, size=T_TAB, color=WHITE, bold=True)
    return sp

def mode_badge(s, mode, x=12.5, y=0.36, w=0.6, h=0.52, fill=PRIMARY, color=WHITE):
    sp = rect(s, x, y, w, h, fill, rounded=True)
    tf = sp.text_frame; tf.word_wrap = False; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, mode, size=T_HUD, color=color, bold=True)
    return sp

HUD_W = {  # 18pt bold Avenir widths + 0.34 padding, right-aligned to 12.5 (clear of mode badge)
    "TURN & TALK": 2.75, "OBSERVE": 2.15, "PREDICT": 2.0, "EVIDENCE": 2.25,
    "WRITE": 1.6, "CHECK": 1.7, "RECITE": 1.75, "TRACE": 1.65, "DRAW": 1.5,
    "EXPLAIN": 1.95, "VOTE": 1.4, "WATCH": 1.7, "DATA": 1.55, "ENGINEER": 2.25,
}
def hud_bubble(s, text_label, x=None, y=0.36, h=0.52):
    w = HUD_W.get(text_label, 2.2)
    if x is None:
        x = 12.4 - w
    sp = rect(s, x, y, w, h, ACCENT, rounded=True)
    tf = sp.text_frame; tf.word_wrap = False; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.08); tf.margin_right = Inches(0.08)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, text_label, size=T_HUD, color=WHITE, bold=True)
    return sp

def slide_number(s, n=None):
    n = n or SLIDE_NO[0]
    text(s, 12.2, 7.02, 0.9, 0.4, str(n), size=T_PAGE, color=INK_SOFT, align=PP_ALIGN.RIGHT)

def anchor_chip(s, code, x=0.55, y=1.02, w=0.78, h=0.5):
    sp = rect(s, x, y, w, h, ACCENT, rounded=True)
    tf = sp.text_frame; tf.word_wrap = False; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, code, size=24, color=WHITE, bold=True)
    return sp

def header(s, title, kicker=None, mode=None, hud=None, anchor=None, title_size=T_TITLE):
    chapter_tab(s)
    if mode:
        mode_badge(s, mode)
    if hud:
        hud_bubble(s, hud)
    tx = 0.55
    if anchor:
        anchor_chip(s, anchor)
        tx = 1.5
    text(s, tx, 1.02, 12.75 - tx, 0.7, title, size=title_size, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE, font=FONT_DISPLAY)
    if kicker:
        text(s, 0.55, 1.72, 11.7, 0.4, kicker, size=T_KICK, color=INK_SOFT, italic=True)
    slide_number(s)

# ---------------------------------------------------------------- model / diagrams
def model_strip(s, items, x=0.75, y=None, w=11.8, box_h=0.82, gap=0.5, size=26, fills=None):
    """Horizontal arrow chain (boxes + gold arrows)."""
    n = len(items)
    box_w = (w - (n - 1) * gap) / n
    cx = x
    for i, it in enumerate(items):
        f = (fills[i] if fills else (PRIMARY if i % 2 == 0 else NEUTRAL))
        sp = rect(s, cx, y, box_w, box_h, f, rounded=True)
        tf = sp.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.08); tf.margin_right = Inches(0.08)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        run(p, it, size=size, color=WHITE, bold=True)
        if i < n - 1:
            ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(cx + box_w + 0.02),
                                    Inches(y + box_h/2 - 0.16), Inches(gap - 0.04), Inches(0.32))
            ar.fill.solid(); ar.fill.fore_color.rgb = ACCENT
            ar.line.fill.background(); ar.shadow.inherit = False
        cx += box_w + gap
    return box_h

def before_after(s, x=0.75, y=2.5, w=5.6, h=2.6, left="BEFORE", right="AFTER", left_hint="", right_hint=""):
    """Two-panel BEFORE / AFTER comparison."""
    gap = 0.35
    bw = (w - gap) / 2
    for idx, (lab, hint) in enumerate([(left, left_hint), (right, right_hint)]):
        cx = x + idx * (bw + gap)
        rect(s, cx, y, bw, h, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
        text(s, cx + 0.2, y + 0.15, bw - 0.4, 0.5, lab, size=28, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
        if hint:
            text(s, cx + 0.2, y + 0.75, bw - 0.4, h - 0.9, hint, size=T_BODY_S, color=INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def before_after_photo(s, x, y, w, h, left_img, right_img, left="BEFORE", right="AFTER",
                       left_hint="", right_hint=""):
    """Premium BEFORE/AFTER with matched photos in each panel (labels/hints preserved)."""
    gap = 0.35
    bw = (w - gap) / 2
    for idx, (lab, hint, img) in enumerate([(left, left_hint, left_img), (right, right_hint, right_img)]):
        cx = x + idx * (bw + gap)
        rect(s, cx, y, bw, h, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
        text(s, cx + 0.2, y + 0.14, bw - 0.4, 0.5, lab, size=28, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
        _pic_fit(s, img, cx + 0.15, y + 0.68, bw - 0.3, h - 1.3)
        if hint:
            text(s, cx + 0.2, y + h - 0.6, bw - 0.4, 0.5, hint, size=T_BODY_S, color=INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------------------------------------------------------------- vocab card
def vocab_card(s, x, y, w, h, term, definition, page, visual=None):
    """One vocabulary TEACH card (frozen component)."""
    rect(s, x, y, w, h, PAPER, line_color=RULE, line_w=1.25, rounded=True)
    # navy top band
    rect(s, x, y, w, 0.16, PRIMARY)
    # TEACH pill (top-right)
    pill = rect(s, x + w - 1.85, y + 0.42, 1.6, 0.5, NAVY_TINT, rounded=True)
    tf = pill.text_frame; tf.word_wrap = False; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, "TEACH", size=24, color=PRIMARY, bold=True)
    # label
    text(s, x + 0.35, y + 0.42, w - 2.3, 0.4, "VOCABULARY", size=24, color=NEUTRAL, bold=True, caps=True)
    # huge term
    text(s, x + 0.35, y + 0.78, w - 0.7, 1.05, term, size=54, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE, font=FONT_DISPLAY)
    # definition
    text(s, x + 0.35, y + 1.95, w - 0.7, 0.95, definition, size=T_DEF, color=INK)
    # visual panel (gold-tinted)
    if visual:
        rect(s, x + 0.35, y + 3.0, w - 0.7, h - 3.7, GOLD_TINT, line_color=ACCENT, line_w=0.75, rounded=True)
        visual(s, x + 0.35, y + 3.0, w - 0.7, h - 3.7)
    # reader page
    text(s, x + 0.35, y + h - 0.55, w - 0.7, 0.4, page, size=T_PAGE, color=INK_SOFT, bold=True)

def card_visual_chain(panel_words):
    """Return a visual-draw function that renders a small arrow chain inside a panel."""
    def draw(s, x, y, w, h):
        n = len(panel_words)
        cw = (w - 0.5 * (n - 1) - 0.3) / n
        cx = x + 0.15
        cy = y + h / 2 - 0.28
        for i, word in enumerate(panel_words):
            sp = rect(s, cx, cy, cw, 0.62, PRIMARY if i == 0 else NEUTRAL, rounded=True)
            tf = sp.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = Inches(0.05); tf.margin_right = Inches(0.05)
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            run(p, word, size=24, color=WHITE, bold=True)
            if i < n - 1:
                ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(cx + cw + 0.02),
                                        Inches(cy + 0.14), Inches(0.46), Inches(0.28))
                ar.fill.solid(); ar.fill.fore_color.rgb = ACCENT
                ar.line.fill.background(); ar.shadow.inherit = False
            cx += cw + 0.5
    return draw

def card_visual_image(path):
    """Return a visual-draw function that fits a photograph into a vocab-card visual panel."""
    def draw(s, x, y, w, h):
        _pic_fit(s, path, x + 0.06, y + 0.06, w - 0.12, h - 0.12)
    return draw

# ---------------------------------------------------------------- notes mirror
def notes_heading(s, code, title_text, reader_ref):
    anchor_chip(s, code)
    text(s, 1.5, 1.02, 11.0, 0.6, title_text, size=T_HEAD, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 1.5, 1.62, 8.0, 0.35, reader_ref, size=T_KICK, color=INK_SOFT, italic=True)

def write_line(s, x, y, w, color=INK_SOFT):
    rect(s, x, y, w, 0.035, color)

def _plan_line(n):
    info = PACE.S[n]
    mins = ("%g" % info["minutes"])
    if info["session"] == 0:
        return "PLAN OPTIONAL · end-of-chapter review (review day / Friday FLEX only; never inside a required block) · %s min" % mins
    sess = PACE.SESSIONS[info["session"]]
    tag = "REQUIRED" if info["status"] == "REQ" else "OPTIONAL - skip freely"
    extra = ""
    if n == PACE.REENTRY_SLIDE:
        extra = " · RE-ENTRY: Sessions 2 and 3 also open on this slide (re-read the Big Question; ask 'What evidence have we collected so far?') - %g / %g min" % (
            PACE.REENTRY_MIN[2], PACE.REENTRY_MIN[3])
    return "PLAN Session %d (%s) · %s · %s min%s" % (info["session"], sess["day"], tag, mins, extra)

def set_note(slide, lines):
    n = SLIDE_NO[0]
    out = [ln for ln in lines if not ln.startswith("TIME ")]
    out.insert(1, "TIME %g min" % PACE.S[n]["minutes"])
    out.insert(2, _plan_line(n))
    slide.notes_slide.notes_text_frame.text = "\n".join(out)

# ================================================================================
# SLIDE 1 — TITLE
# ================================================================================
s = new_slide(PRIMARY)
# chapter tab (inverted: gold-on-navy)
sp = rect(s, 0.9, 0.75, 4.4, 0.55, ACCENT, rounded=True)
tf = sp.text_frame; tf.word_wrap = False; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.15); tf.margin_right = Inches(0.15)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
run(p, "CHAPTER 1 · GRADE 4 · WEEK 1", size=14, color=WHITE, bold=True)
text(s, 0.9, 1.75, 11.5, 1.0, "Energy Causes Change", size=T_MAJOR, color=WHITE, bold=True, font=FONT_DISPLAY)
text(s, 0.9, 2.75, 11.5, 0.5, "Discovery / Evidence", size=T_KICK, color=RGBColor(0xD8, 0xDC, 0xE4), bold=True)
text(s, 0.9, 3.25, 11.9, 0.6, "Where can we observe evidence of energy causing change?", size=28, color=WHITE, italic=True)
# small model teaser
model_strip(s, ["ENERGY", "CHANGE", "?"], x=0.9, y=4.3, w=8.4, box_h=0.75, gap=0.45, size=24, fills=[PRIMARY, NEUTRAL, ACCENT])  # 6.1C L-C: open last chip - EVIDENCE is revealed at N1
text(s, 0.9, 5.95, 11.5, 0.5, "Unit 1 · Energy Transfer & Transformation", size=T_KICK, color=RGBColor(0xD8, 0xDC, 0xE4), italic=True)
# premium: cinematic still life on the right (text-free, Phase 5A R01-opener)
_pic_fit(s, _img("slide-01-opener.png"), 9.6, 1.0, 3.3, 4.6)
slide_number(s)
set_note(s, ["MODE Title · orient", "TIME 2 min", "STUDENT RESOURCE Guided Notes (not yet open)",
             "ASK What do you think energy does?", "LISTEN FOR words like move, change, power",
             "NEXT Flip the lights as you open the Big Question.",
             "SESSIONS Mon: slides 1-3, 6-16 (optional 4-5) · Tue: slides 2, 17, 19-27 (18 is OPTIONAL) · Fri: slides 2 then 28-31, 33 (optional 32), then the quiz. Slides 34-45 = optional review."])

# ================================================================================
# SLIDE 2 — BIG QUESTION (intro)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s)
mode_badge(s, "BQ")
hud_bubble(s, "TURN & TALK")
text(s, 0.55, 1.1, 11.7, 0.5, "Big Question", size=T_KICK, color=NEUTRAL, bold=True, caps=True)
# navy BQ banner
rect(s, 0.55, 1.7, 12.23, 1.9, PRIMARY, rounded=True)
text(s, 0.9, 1.95, 11.5, 1.4, "Where can we observe evidence of energy causing change?",
     size=34, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.9, 4.0, 11.5, 0.5, "Keep it in mind all chapter. We will come back to it.", size=T_BODY_S, color=INK_SOFT, align=PP_ALIGN.CENTER)
text(s, 0.55, 4.9, 11.7, 0.6, "Think: What is ONE change you have seen happen?", size=T_BODY, color=INK, align=PP_ALIGN.CENTER, bold=True)
slide_number(s)
set_note(s, ["MODE BQ · introduce", "TIME 3 min", "STUDENT RESOURCE Guided Notes p.1 (BQ box)",
             "ASK What change have you seen happen today?", "LISTEN FOR any observable change (light, sound, movement)",
             "REVEAL Do not answer the BQ yet — we collect evidence first.", "NEXT Session 1: My first thinking (slide 3) · Session 2: Forms of energy (slide 17) · Session 3: Recognizing evidence (slide 28)."])

# ================================================================================
# SLIDE 3 — BQ · MY FIRST THINKING (notes mirror)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "BQ", "Big Question — My first thinking", "Guided Notes p. 1")
text(s, 1.5, 2.3, 11.0, 1.0, "Where can we observe evidence of energy causing change?", size=T_BODY, color=PRIMARY, bold=True)
text(s, 1.5, 3.5, 6.0, 0.55, "My first thinking", size=T_BODY, color=INK, bold=True)
write_line(s, 1.5, 4.1, 10.5)
write_line(s, 1.5, 4.8, 10.5)
text(s, 1.5, 5.55, 10.5, 0.5, "Write 1–2 quick ideas. No wrong answer yet.", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · BQ anchor", "TIME 2 min", "STUDENT RESOURCE Guided Notes p.1 top",
             "ASK What change have you seen? Write your first idea.", "LISTEN FOR students naming a change (not 'energy')",
             "MISCONCEPTION Accept any change; do not correct yet.", "NEXT Observe the light switch."])

# ================================================================================
# SLIDE 4 — PHENOMENON: dark → light
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "D"); hud_bubble(s, "OBSERVE")
text(s, 0.55, 1.02, 11.7, 0.7, "What changed?", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader p. 1 — you walk into a dark room and flip a switch.", size=T_KICK, color=INK_SOFT, italic=True)
before_after_photo(s, x=0.75, y=2.5, w=7.4, h=2.6,
                   left_img=_db_dark, right_img=_db_bright,
                   left="DARK room", right="BRIGHT room",
                   left_hint="hard to see", right_hint="light fills the room")
text(s, 8.7, 2.5, 3.8, 2.6, "Something became different.\nThat is a change.", size=T_BODY, color=INK, bold=True, anchor=MSO_ANCHOR.MIDDLE)
slide_number(s)
set_note(s, ["MODE Demo · observe", "TIME 3 min", "STUDENT RESOURCE Reader p.1",
             "ASK What changed when I flipped the switch?", "LISTEN FOR 'the room got bright' / 'light came on'",
             "REVEAL The room changed from dark to light — a change.", "NEXT Notice & wonder."])

# ================================================================================
# SLIDE 5 — NOTICE & WONDER
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "D"); hud_bubble(s, "TURN & TALK")
text(s, 0.55, 1.02, 11.7, 0.7, "I notice…  I wonder…", size=T_TITLE, color=PRIMARY, bold=True)
rect(s, 0.75, 2.2, 5.6, 3.2, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
text(s, 1.05, 2.5, 5.0, 0.5, "I NOTICE", size=T_HEAD, color=ACCENT, bold=True, caps=True)
text(s, 1.05, 3.2, 5.0, 1.8, "The room is different now.\nLight is everywhere.", size=T_BODY_S, color=INK)
rect(s, 7.0, 2.2, 5.6, 3.2, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
text(s, 7.3, 2.5, 5.0, 0.5, "I WONDER", size=T_HEAD, color=ACCENT, bold=True, caps=True)
text(s, 7.3, 3.2, 5.0, 1.8, "What made the light\nchange so fast?", size=T_BODY_S, color=INK)
text(s, 0.55, 5.8, 11.7, 0.5, "Share one notice and one wonder with a partner.", size=T_BODY, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Demo · discuss", "TIME 2 min", "STUDENT RESOURCE none",
             "ASK What did you notice? What do you wonder?", "LISTEN FOR change words and curiosity",
             "NEXT Electric pencil sharpener demo."])

# ================================================================================
# SLIDE 6 — DEMO: observe dull pencil
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "D"); hud_bubble(s, "OBSERVE")
text(s, 0.55, 1.02, 11.7, 0.7, "Electric Pencil Sharpener", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Observe the pencil BEFORE we sharpen it.", size=T_KICK, color=INK_SOFT, italic=True)
_pic_fit(s, _pen_before, 0.75, 2.5, 4.4, 3.3)
rect(s, 5.35, 2.5, 7.35, 3.3, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
text(s, 5.65, 2.8, 6.75, 0.5, "BEFORE", size=T_HEAD, color=ACCENT, bold=True, caps=True)
text(s, 5.65, 3.5, 6.75, 1.6, "A dull pencil — tip is flat, and it is quiet.",
     size=T_BODY, color=INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.55, 6.15, 11.7, 0.5, "Look closely. What do you see? What do you hear?", size=T_BODY, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Demo · observe", "TIME 2 min", "STUDENT RESOURCE none (live demo)",
             "ASK What does the pencil look and sound like right now?", "LISTEN FOR dull, flat, quiet, still",
             "NEXT Predict before sharpening."])

# ================================================================================
# SLIDE 7 — DEMO: predict
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "D"); hud_bubble(s, "PREDICT")
text(s, 0.55, 1.02, 11.7, 0.7, "Predict: what will change?", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Think before we turn it on.", size=T_KICK, color=INK_SOFT, italic=True)
rect(s, 1.5, 2.6, 10.3, 2.6, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
text(s, 1.8, 2.9, 9.7, 0.5, "When the sharpener runs, the pencil will…", size=T_BODY, color=INK, bold=True)
text(s, 1.8, 3.6, 9.7, 1.3, "get  ____________________", size=T_BODY, color=INK)
text(s, 0.55, 5.6, 11.7, 0.5, "Make a prediction. Say it to your partner.", size=T_BODY, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Demo · predict", "TIME 2 min", "STUDENT RESOURCE none",
             "ASK What will change about the pencil? The sharpener?", "LISTEN FOR shorter, sharper, noise",
             "REVEAL Do not confirm yet — run the demo.", "NEXT Observe the change."])

# ================================================================================
# SLIDE 8 — DEMO: what changed (before/after)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "D"); hud_bubble(s, "OBSERVE")
text(s, 0.55, 1.02, 11.7, 0.7, "What changed?", size=T_TITLE, color=PRIMARY, bold=True)
before_after_photo(s, x=0.75, y=2.4, w=7.4, h=3.0,
                   left_img=_pen_before, right_img=_pen_after,
                   left="BEFORE", right="AFTER",
                   left_hint="dull tip · quiet", right_hint="shorter · sharper · humming")
rect(s, 8.7, 2.4, 3.8, 3.0, GOLD_TINT, line_color=ACCENT, line_w=0.75, rounded=True)
text(s, 8.95, 2.6, 3.3, 0.5, "CHANGES", size=24, color=NEUTRAL, bold=True, caps=True)
text(s, 8.95, 3.2, 3.3, 2.0, "• the tip is sharper\n• the pencil is shorter\n• it makes a sound", size=T_BODY_S, color=INK)
slide_number(s)
set_note(s, ["MODE Demo · observe", "TIME 3 min", "STUDENT RESOURCE none",
             "ASK Name every change you saw or heard.", "LISTEN FOR shorter, sharper, noise",
             "REVEAL Record all three changes.", "NEXT Turn changes into evidence."])

# ================================================================================
# SLIDE 9 — DEMO: evidence
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "D"); hud_bubble(s, "EXPLAIN")
text(s, 0.55, 1.02, 11.7, 0.7, "How do we know energy was involved?", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Energy can be invisible. We look for the change.", size=T_KICK, color=INK_SOFT, italic=True)
model_strip(s, ["ENERGY", "CHANGE", "?"], x=0.75, y=2.7, w=11.8, box_h=1.0, gap=0.5, size=28, fills=[PRIMARY, NEUTRAL, ACCENT])
text(s, 0.55, 4.3, 11.7, 1.4,
     "The pencil got shorter and sharper and made a sound.\nThose changes are clues that energy was involved.",
     size=T_BODY, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Demo · evidence", "TIME 3 min", "STUDENT RESOURCE Reader p.2 (Change Is Evidence of Energy)",
             "ASK How do we know energy was here if we can't see it?", "LISTEN FOR 'we saw the change' / 'clues'",
             "REVEAL The word EVIDENCE is introduced from the Reader on slide 14 - do not name it here; the '?' box stays open.",
             "MISCONCEPTION We see the change, not the energy itself.", "NEXT Vocabulary: energy + change."])

# ================================================================================
# SLIDE 10 — V1 VOCABULARY CARDS (energy + change)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "V")
text(s, 0.55, 1.02, 11.7, 0.7, "Vocabulary — Energy & Change", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.72, 11.7, 0.4, "Reader p. 1", size=T_KICK, color=INK_SOFT, italic=True)
cw = 5.95
vocab_card(s, 0.55, 2.25, cw, 4.5, "energy",
           "the ability to cause change",
           "Reader p. 1",
           visual=card_visual_chain(["ENERGY", "CHANGE"]))
vocab_card(s, 0.55 + cw + 0.33, 2.25, cw, 4.5, "change",
           "to become different",
           "Reader p. 1",
           visual=card_visual_chain(["BEFORE", "AFTER"]))
slide_number(s)
set_note(s, ["MODE Vocabulary · TEACH", "TIME 4 min", "STUDENT RESOURCE Guided Notes V1",
             "ASK Read each definition together. Use each word in a sentence.",
             "LISTEN FOR 'energy causes change' and 'to become different'",
             "REVEAL Full definitions shown — these are the two V1 terms.", "NEXT Record V1 on notes."])

# ================================================================================
# SLIDE 11 — V1 NOTES (write)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "V1", "Vocabulary — Energy & Change", "Guided Notes · Reader p. 1")
rich(s, 1.5, 2.6, 11.0, 1.0, [
    [("energy — the ability to cause ", {}), (blank_str(7), {"underline": True, "color": INK}), (" .", {})],
])
rich(s, 1.5, 3.6, 11.0, 1.0, [
    [("change — to become ", {}), (blank_str(9), {"underline": True, "color": INK}), (" .", {})],
])
text(s, 1.5, 4.9, 11.0, 0.5, "Write the missing word in each blank.", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · V1 anchor", "TIME 3 min", "STUDENT RESOURCE Guided Notes V1 (Reader p.1)",
             "ASK Fill in each blank.", "LISTEN FOR 'change' and 'different'",
             "REVEAL Reveal after students write.", "NEXT Check answers."])

# ================================================================================
# SLIDE 12 — V1 NOTES (check/reveal)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "CHECK")
notes_heading(s, "V1", "Vocabulary — Energy & Change", "Guided Notes · Reader p. 1")
rich(s, 1.5, 2.6, 11.0, 1.0, [
    [("energy — the ability to cause ", {}), ("change", {"bold": True, "color": ACCENT}), (" .", {})],
])
rich(s, 1.5, 3.6, 11.0, 1.0, [
    [("change — to become ", {}), ("different", {"bold": True, "color": ACCENT}), (" .", {})],
])
text(s, 1.5, 4.9, 11.0, 0.5, "change  ·  different", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · V1 reveal", "TIME 1 min", "STUDENT RESOURCE Guided Notes V1",
             "REVEAL change · different", "NEXT Energy Causes Change (N1)."])

# ================================================================================
# SLIDE 13 — N1 CONCEPT: energy causes change
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "R"); hud_bubble(s, "RECITE")
text(s, 0.55, 1.02, 11.7, 0.7, "What is energy?", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader p. 1", size=T_KICK, color=INK_SOFT, italic=True)
rect(s, 0.75, 2.5, 11.8, 2.2, PRIMARY, rounded=True)
text(s, 1.2, 2.9, 10.9, 1.4, "Energy is the ability to cause change.", size=38, color=WHITE, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.75, 5.0, 11.8, 1.0, "Say it together: “Energy is the ability to cause change.”", size=T_BODY, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Read · concept", "TIME 3 min", "STUDENT RESOURCE Reader p.1",
             "ASK What is energy?", "LISTEN FOR 'the ability to cause change'",
             "REVEAL Energy is the ability to cause change.", "NEXT Change is evidence."])

# ================================================================================
# SLIDE 14 — N1 READ + DISCUSS: seashore (model's last box withheld until the N1 reveal)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "R"); hud_bubble(s, "TRACE")
text(s, 0.55, 1.02, 11.7, 0.7, "Look at the seashore", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader p. 2 — the seashore changes all around us.", size=T_KICK, color=INK_SOFT, italic=True)
model_strip(s, ["ENERGY", "CHANGE", "?"], x=0.75, y=2.6, w=11.8, box_h=1.1, gap=0.5, size=30, fills=[PRIMARY, NEUTRAL, ACCENT])
text(s, 0.75, 4.15, 11.8, 1.9,
     "Read Reader p. 2.\nWaves move. Sand shifts. Water makes sound.\nWhat are these changes a clue about?",
     size=T_BODY, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Read · model", "TIME 3 min", "STUDENT RESOURCE Reader p.2",
             "ASK What changes can you find at the seashore? What are those changes a clue about?",
             "LISTEN FOR 'evidence' / 'a clue' / 'energy is there'",
             "LANGUAGE The Reader says 'evidence, or proof.' Teach and use the word EVIDENCE (it is in the Big Question). If a student says 'proof', accept it and restate: 'Yes - we say evidence.'",
             "REVEAL Keep the third box as '?' - students name it on the next slide's notes, then slide 16 completes the model.",
             "NEXT Record N1 on notes."])

# ================================================================================
# SLIDE 15 — N1 NOTES (write)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "N1", "Energy Causes Change", "Guided Notes · Reader pp. 1–2")
text(s, 1.5, 2.45, 11.0, 0.7, "Energy has the ability to cause change.", size=T_BODY, color=INK, bold=True)
rich(s, 1.5, 3.55, 11.0, 1.4, [
    [("When you see a change, you are seeing ", {}), (blank_str(9), {"underline": True, "color": INK}), (" of energy.", {})],
])
text(s, 1.5, 5.3, 11.0, 0.5, "Write the missing word in the sentence. Leave the last box of your model empty for now.", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · N1 anchor", "TIME 2 min", "STUDENT RESOURCE Guided Notes N1 (Reader pp.1–2)",
             "ASK Fill in the one blank in the sentence. The last box of the model on the notes page is empty on purpose - do not fill it yet.", "LISTEN FOR evidence",
             "REVEAL Reveal after writing.", "NEXT Check answer."])

# ================================================================================
# SLIDE 16 — N1 NOTES (check/reveal)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "CHECK")
notes_heading(s, "N1", "Energy Causes Change", "Guided Notes · Reader pp. 1–2")
text(s, 1.5, 2.3, 11.0, 0.7, "Energy has the ability to cause change.", size=T_BODY, color=INK, bold=True)
rich(s, 1.5, 3.15, 11.0, 1.0, [
    [("When you see a change, you are seeing ", {}), ("evidence", {"bold": True, "color": ACCENT}), (" of energy.", {})],
])
model_strip(s, ["ENERGY", "CHANGE", "EVIDENCE"], x=1.5, y=4.5, w=10.0, box_h=0.9, gap=0.45, size=28)
text(s, 1.5, 5.75, 11.0, 0.5, "Now write the same word in the last box of your model.", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · N1 reveal", "TIME 1 min", "STUDENT RESOURCE Guided Notes N1",
             "REVEAL evidence (accept 'proof' once, then restate 'evidence'). Students check their sentence, then copy the word into the empty last box of the model on the notes page.", "NEXT Close Session 1. Session 2 opens on slide 2 (the Big Question)."])

# ================================================================================
# SLIDE 17 — N2 CONCEPT: energy has forms
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "R")
text(s, 0.55, 1.02, 11.7, 0.7, "Energy has different forms", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader p. 3 — think of a spinning carousel.", size=T_KICK, color=INK_SOFT, italic=True)
forms = ["motion", "sound", "light", "heat", "electrical energy"]
cw = 2.2; gap = 0.3; total = 5*cw + 4*gap
x0 = 0.55 + (12.23 - total)/2
for i, f in enumerate(forms):
    cx = x0 + i*(cw+gap)
    sp = rect(s, cx, 2.7, cw, 1.2, PRIMARY, rounded=True)
    tf = sp.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.08); tf.margin_right = Inches(0.08)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, f, size=24, color=WHITE, bold=True)
text(s, 0.55, 4.3, 11.7, 1.9,
     "On the carousel, the horses spin and move up and down.\nThat is motion.\nFind the other forms in the Reader.",
     size=T_BODY_S, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Read · forms", "TIME 4 min", "STUDENT RESOURCE Reader p.3",
             "ASK What forms of energy do you see or hear on a carousel?", "LISTEN FOR motion, sound, light, heat, electrical",
             "REVEAL Model ONLY the motion example. Do not supply examples for the other four forms - students write their own on slide 19.",
             "NEXT Record examples on notes (N2)."])

# ================================================================================
# SLIDE 18 — N2 FORMS: clap check
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "C"); hud_bubble(s, "OBSERVE")
text(s, 0.55, 1.02, 11.7, 0.7, "Clap three times", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "What forms of energy do you observe?", size=T_KICK, color=INK_SOFT, italic=True)
rect(s, 1.5, 2.5, 10.3, 3.2, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
text(s, 1.8, 2.85, 9.7, 0.5, "When you clap…", size=T_HEAD, color=PRIMARY, bold=True)
text(s, 1.8, 3.6, 9.7, 1.7, "What do you SEE?\nWhat do you HEAR?\nWhat do you FEEL in your hands?", size=T_BODY, color=INK)
slide_number(s)
set_note(s, ["MODE Check · forms", "TIME 2 min", "STUDENT RESOURCE Reader p.3",
             "ASK What forms of energy can you observe when you clap?",
             "LISTEN FOR motion, sound, and maybe heat (students name them - not shown on the slide)", "NEXT Record N2 table."])

# ================================================================================
# SLIDE 19 — N2 NOTES (table)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "N2", "Energy Occurs in Different Forms", "Guided Notes · Reader p. 3")
text(s, 1.5, 2.3, 11.0, 0.5, "Write one example that shows a change for each form.", size=T_BODY_S, color=INK, italic=True)
# table header
hx, hy, hw, hh = 1.5, 2.95, 3.4, 0.6
ex, ew = hx + hw + 0.15, 11.0 - hw - 0.15
rect(s, hx, hy, hw, hh, PRIMARY, rounded=False)
text(s, hx+0.15, hy+0.1, hw-0.3, 0.4, "FORM", size=24, color=WHITE, bold=True)
rect(s, ex, hy, ew, hh, PRIMARY, rounded=False)
text(s, ex+0.15, hy+0.12, ew-0.3, 0.4, "ONE EXAMPLE THAT SHOWS A CHANGE", size=22, color=WHITE, bold=True)
rows = ["motion", "sound", "light", "heat", "electrical energy"]
ry = hy + hh
for i, rname in enumerate(rows):
    rh = 0.62
    cy = ry + i*rh
    rect(s, hx, cy, hw, rh, PAPER, line_color=RULE, line_w=0.75)
    text(s, hx+0.15, cy+0.08, hw-0.3, 0.45, rname, size=24, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, ex, cy, ew, rh, PAPER, line_color=RULE, line_w=0.75)
slide_number(s)
set_note(s, ["MODE Notes · N2 anchor", "TIME 5 min", "STUDENT RESOURCE Guided Notes N2 (Reader p.3)",
             "ASK Write one example per form. Then turn & talk: share two examples with a partner and add one new idea from your partner.",
             "LISTEN FOR carousel examples, clap examples, home/school examples - accept any real example that shows a change",
             "REVEAL There is no answer slide for N2. Circulate; use student examples as the check.",
             "NEXT Stored energy (V2)."])

# ================================================================================
# SLIDE 20 — V2 VOCABULARY CARD (stored energy)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "V")
text(s, 0.55, 1.02, 11.7, 0.7, "Vocabulary — Stored Energy", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.72, 11.7, 0.4, "Reader p. 4", size=T_KICK, color=INK_SOFT, italic=True)
vocab_card(s, 3.0, 2.25, 7.3, 4.5, "stored energy",
           "energy that has the ability to cause change at a later time",
           "Reader p. 4",
           visual=card_visual_chain(["STILL", "LATER", "CHANGE"]))
slide_number(s)
set_note(s, ["MODE Vocabulary · TEACH", "TIME 3 min", "STUDENT RESOURCE Guided Notes V2 (Reader p.4)",
             "ASK What does the word 'later' tell us about when the change can happen? (Save examples for slide 23.)", "LISTEN FOR 'not right now - after'",
             "REVEAL stored energy = ability to cause change at a later time.", "NEXT Record V2."])

# ================================================================================
# SLIDE 21 — V2 NOTES (write)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "V2", "Vocabulary — Stored Energy", "Guided Notes · Reader p. 4")
rich(s, 1.5, 2.65, 11.0, 1.15, [
    [("stored energy — energy that has the ability to cause change at a ", {}),
     (blank_str(6), {"underline": True, "color": INK}), (" time.", {})],
])
text(s, 1.5, 4.15, 11.0, 0.5, "Write the missing word in the blank.", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · V2 anchor", "TIME 2 min", "STUDENT RESOURCE Guided Notes V2 (Reader p.4)",
             "ASK Fill in the blank.", "LISTEN FOR 'later'", "REVEAL Reveal after writing.", "NEXT Check answer."])

# ================================================================================
# SLIDE 22 — V2 NOTES (check/reveal)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "CHECK")
notes_heading(s, "V2", "Vocabulary — Stored Energy", "Guided Notes · Reader p. 4")
rich(s, 1.5, 2.65, 11.0, 1.15, [
    [("stored energy — energy that has the ability to cause change at a ", {}),
     ("later", {"bold": True, "color": ACCENT}), (" time.", {})],
])
text(s, 1.5, 4.15, 11.0, 0.5, "later", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · V2 reveal", "TIME 1 min", "STUDENT RESOURCE Guided Notes V2",
             "REVEAL later", "NEXT Objects can store energy (N3)."])

# ================================================================================
# SLIDE 23 — N3 CONCEPT: still objects can store energy (predict)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "R"); hud_bubble(s, "PREDICT")
text(s, 0.55, 1.02, 11.7, 0.7, "Does a still battery have energy?", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader p. 4 — think about a battery inside a flashlight.", size=T_KICK, color=INK_SOFT, italic=True)
_pic_fit(s, _store_battery, 0.75, 2.6, 4.2, 3.0)
rect(s, 5.2, 2.6, 7.5, 3.0, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
text(s, 5.5, 2.95, 6.9, 1.1, "A battery sits still in a flashlight that is switched off.", size=T_BODY, color=INK, bold=True)
text(s, 5.5, 4.15, 6.9, 1.2,
     "Yes or no? Make a prediction.\nTell your partner why.",
     size=T_BODY_S, color=INK)
slide_number(s)
set_note(s, ["MODE Read · predict", "TIME 3 min", "STUDENT RESOURCE Reader p.4",
             "ASK Does a still battery have energy? Take yes/no predictions and reasons - do not confirm yet.", "LISTEN FOR 'yes' / 'no' with a reason; accept any prediction",
             "REVEAL After students predict, read the battery paragraph on Reader p. 4 aloud: the chemicals inside a battery store energy. The screen stays a question; slide 25 shows the Reader fact.",
             "MISCONCEPTION Only moving objects have energy → pair moving + stored.", "NEXT Position."])

# ================================================================================
# SLIDE 24 — N3 CONCEPT: stored energy of position
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "R")
text(s, 0.55, 1.02, 11.7, 0.7, "The stored energy of position", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader p. 5 — an object held up can cause a change later.", size=T_KICK, color=INK_SOFT, italic=True)
_pic_fit(s, _store_apple, 0.75, 2.5, 4.2, 3.0)
rect(s, 5.2, 2.5, 7.5, 3.0, GOLD_TINT, line_color=ACCENT, line_w=0.75, rounded=True)
text(s, 5.5, 2.85, 6.9, 0.5, "Raised apple → let go → ?", size=T_HEAD, color=PRIMARY, bold=True)
text(s, 5.5, 3.6, 6.9, 1.4,
     "An apple held above the ground has stored energy\nbecause of its position. Imagine you let go. What will happen?",
     size=T_BODY_S, color=INK)
slide_number(s)
set_note(s, ["MODE Read · position", "TIME 3 min", "STUDENT RESOURCE Reader p.5",
             "ASK Why does a raised apple have stored energy?", "LISTEN FOR 'because of its position'",
             "NEXT Build the stored-energy model."])

# ================================================================================
# SLIDE 25 — N3 MODEL: STORED ENERGY → RELEASE → CHANGE
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "R"); hud_bubble(s, "TRACE")
text(s, 0.55, 1.02, 11.7, 0.7, "Stored energy can cause a change later", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader p. 4 — back to our battery: the chemicals inside it store energy.", size=T_KICK, color=INK_SOFT, italic=True)
_pic_fit(s, _store_rubber, 0.75, 2.5, 4.2, 3.0)
model_strip(s, ["STORED ENERGY", "RELEASE", "CHANGE"], x=5.2, y=2.7, w=7.5, box_h=1.1, gap=0.45, size=26)
text(s, 5.2, 4.3, 7.5, 1.6,
     "Stretch a rubber band — it now stores energy.\nLet it go. What change will you see and hear?",
     size=T_BODY, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Read · model", "TIME 2 min", "STUDENT RESOURCE Reader p.4",
             "REVEAL (closes the slide 23 prediction) The Reader says chemicals inside a battery store energy - so yes, a still battery has energy. Do not say what the flashlight does yet: students write that in the N3 table.",
             "ASK Trace: stored → release → change.", "LISTEN FOR rubber band SNAP example",
             "NEXT Record N3 on notes."])

# ================================================================================
# SLIDE 26 — N3 NOTES (write)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "N3", "Objects Can Store Energy", "Guided Notes · Reader pp. 4–5")
model_strip(s, ["STORED ENERGY", "RELEASE", "CHANGE"], x=1.0, y=2.1, w=10.5, box_h=0.65, gap=0.4, size=24)
# table
hx, hy, hw, hh = 1.0, 2.95, 4.8, 0.5
ex, ew = hx + hw + 0.15, 11.5 - hw - 0.15
rect(s, hx, hy, hw, hh, PRIMARY)
text(s, hx+0.12, hy+0.07, hw-0.24, 0.35, "EXAMPLE", size=22, color=WHITE, bold=True)
rect(s, ex, hy, ew, hh, PRIMARY)
text(s, ex+0.12, hy+0.07, ew-0.24, 0.35, "WHAT CHANGE COULD HAPPEN LATER?", size=20, color=WHITE, bold=True)
rows = ["battery (in a flashlight)", "stretched rubber band", "raised object (apple)"]
ry = hy + hh
for i, rname in enumerate(rows):
    rh = 0.58
    cy = ry + i*rh
    rect(s, hx, cy, hw, rh, PAPER, line_color=RULE, line_w=0.75)
    text(s, hx+0.12, cy+0.06, hw-0.24, 0.45, rname, size=24, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, ex, cy, ew, rh, PAPER, line_color=RULE, line_w=0.75)
rich(s, 1.0, 5.4, 11.5, 0.7, [
    [("Objects also have stored energy because of their ", {"size": T_BODY_S}),
     (blank_str(8), {"underline": True, "color": INK, "size": T_BODY_S}), (" .", {"size": T_BODY_S})],
])
slide_number(s)
set_note(s, ["MODE Notes · N3 anchor", "TIME 5 min", "STUDENT RESOURCE Guided Notes N3 (Reader pp.4–5)",
             "ASK Fill in the blank; note the three examples.", "LISTEN FOR 'position'",
             "REVEAL Reveal after writing.", "NEXT Check answer."])

# ================================================================================
# SLIDE 27 — N3 NOTES (check/reveal)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "CHECK")
notes_heading(s, "N3", "Objects Can Store Energy", "Guided Notes · Reader pp. 4–5")
model_strip(s, ["STORED ENERGY", "RELEASE", "CHANGE"], x=1.0, y=2.1, w=10.5, box_h=0.65, gap=0.4, size=24)
hx, hy, hw, hh = 1.0, 2.95, 4.8, 0.5
ex, ew = hx + hw + 0.15, 11.5 - hw - 0.15
rect(s, hx, hy, hw, hh, PRIMARY)
text(s, hx+0.12, hy+0.07, hw-0.24, 0.35, "EXAMPLE", size=22, color=WHITE, bold=True)
rect(s, ex, hy, ew, hh, PRIMARY)
text(s, ex+0.12, hy+0.07, ew-0.24, 0.35, "WHAT CHANGE COULD HAPPEN LATER?", size=20, color=WHITE, bold=True)
rows = ["battery (in a flashlight)", "stretched rubber band", "raised object (apple)"]
ry = hy + hh
for i, rname in enumerate(rows):
    rh = 0.58
    cy = ry + i*rh
    rect(s, hx, cy, hw, rh, PAPER, line_color=RULE, line_w=0.75)
    text(s, hx+0.12, cy+0.06, hw-0.24, 0.45, rname, size=24, color=PRIMARY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, ex, cy, ew, rh, PAPER, line_color=RULE, line_w=0.75)
    text(s, ex+0.12, cy+0.06, ew-0.24, 0.45, ["the flashlight lights up", "it snaps and makes a sound", "it falls down"][i],
         size=28, color=NEUTRAL, italic=True, anchor=MSO_ANCHOR.MIDDLE)
rich(s, 1.0, 5.4, 11.5, 0.7, [
    [("Objects also have stored energy because of their ", {"size": T_BODY_S}),
     ("position", {"bold": True, "color": ACCENT, "size": T_BODY_S}), (" .", {"size": T_BODY_S})],
])
text(s, 1.5, 6.3, 11.0, 0.5, "position  ·  Sample answers shown - yours may differ.", size=T_BODY_S, color=INK_SOFT, italic=True)
slide_number(s)
set_note(s, ["MODE Notes · N3 reveal", "TIME 1 min", "STUDENT RESOURCE Guided Notes N3",
             "REVEAL position. Table cells show SAMPLE answers only - accept any reasonable later change.", "NEXT Close Session 2. Session 3 opens on slide 2 (the Big Question), then N4."])

# ================================================================================
# SLIDE 28 — N4 CONCEPT: recognizing evidence
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "R"); hud_bubble(s, "EVIDENCE")
text(s, 0.55, 1.02, 11.7, 0.7, "Recognizing evidence", size=T_TITLE, color=PRIMARY, bold=True)
text(s, 0.55, 1.75, 11.7, 0.4, "Reader pp. 1–5 — think about the clues we can see, hear, or feel.", size=T_KICK, color=INK_SOFT, italic=True)
rect(s, 0.75, 2.5, 11.8, 2.6, PRIMARY, rounded=True)
text(s, 1.2, 2.85, 10.9, 1.9,
     "Energy can be invisible.\nWhat clues could show that energy is at work?",
     size=T_BODY, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.75, 5.4, 11.8, 0.7, "Think of a change you have seen. What did you see, hear, or feel?", size=T_BODY_S, color=INK, align=PP_ALIGN.CENTER, italic=True)
slide_number(s)
set_note(s, ["MODE Read · evidence", "TIME 2 min", "STUDENT RESOURCE Reader pp.1–5",
             "ASK What clues could show that energy is at work? (Do not give the CHECK YOUR THINKING answer yet.)", "LISTEN FOR movement, sound, light, heat, something different",
             "LANGUAGE Say evidence (not proof).",
             "FRIDAY CLOCK The quiz is handed out NO LATER THAN MINUTE 12. Priority: N4 draw > BQ NOW I THINK > CHECK YOUR THINKING. Minute 6: N4 should be done.", "NEXT Draw before/after (N4)."])

# ================================================================================
# SLIDE 29 — N4 NOTES (before/after draw)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "DRAW")
notes_heading(s, "N4", "Recognizing Evidence", "Guided Notes · Reader pp. 1–5")
text(s, 1.5, 2.25, 11.0, 1.0, "Draw a change you observed. Show what it looked like BEFORE and AFTER.", size=T_BODY_S, color=INK, italic=True)
before_after(s, x=1.5, y=3.3, w=8.0, h=1.9, left="BEFORE", right="AFTER", left_hint="draw", right_hint="draw")
text(s, 1.5, 5.45, 11.0, 0.5, "What changed?", size=T_BODY_S, color=INK, bold=True)
write_line(s, 1.5, 6.15, 10.5)
write_line(s, 1.5, 6.65, 10.5)
slide_number(s)
set_note(s, ["MODE Notes · N4 anchor", "TIME 4 min", "STUDENT RESOURCE Guided Notes N4 (Reader pp.1–5)",
             "ASK Draw one change before and after; write what changed.",
             "LISTEN FOR clear before/after pairs", "NEXT Check your thinking."])

# ================================================================================
# SLIDE 30 — CHECK YOUR THINKING (write)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "N4", "Check Your Thinking", "Guided Notes · Reader pp. 1–5")
rect(s, 1.5, 2.4, 11.0, 1.7, GOLD_TINT, line_color=ACCENT, line_w=0.75, rounded=True)
text(s, 1.8, 2.55, 10.4, 0.45, "CHECK YOUR THINKING", size=24, color=NEUTRAL, bold=True, caps=True)
text(s, 1.8, 3.05, 10.4, 1.05, "How do we know energy is involved if we cannot see energy itself?", size=T_BODY, color=INK, bold=True)
text(s, 1.5, 4.35, 11.0, 0.5, "Start with: “We know because we see …”", size=T_BODY, color=INK, italic=True)
write_line(s, 1.5, 5.15, 10.5)
write_line(s, 1.5, 5.85, 10.5)
slide_number(s)
set_note(s, ["MODE Notes · Check Your Thinking", "TIME 3 min", "STUDENT RESOURCE Guided Notes N4",
             "FRIDAY CLOCK Past minute 6 when you reach this slide? SKIP slides 30-31 (CHECK YOUR THINKING goes home / catch-up) and go straight to slide 33.",
             "ASK Complete the sentence starter.", "LISTEN FOR 'a change, like a ball starting to move'",
             "REVEAL Do not show slide 31 until most students have written.", "NEXT Reveal a sample response."])

# ================================================================================
# SLIDE 31 — CHECK YOUR THINKING (sample + classify)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "C"); hud_bubble(s, "CHECK")
text(s, 0.55, 1.02, 11.7, 0.7, "We know because we see a change", size=T_TITLE, color=PRIMARY, bold=True)
rect(s, 1.5, 2.4, 10.3, 2.2, GOLD_TINT, line_color=ACCENT, line_w=0.75, rounded=True)
text(s, 1.8, 2.6, 9.7, 0.5, "SAMPLE", size=24, color=NEUTRAL, bold=True, caps=True)
text(s, 1.8, 3.15, 9.7, 1.3,
     "“We know because we see a change — like a ball starting to move or a light turning on.”",
     size=T_BODY_S, color=INK, italic=True)
text(s, 1.5, 4.9, 10.3, 0.6, "Any change you observe is evidence of energy.", size=T_BODY_S, color=INK, align=PP_ALIGN.CENTER)
slide_number(s)
set_note(s, ["MODE Check · evidence", "TIME 2 min", "STUDENT RESOURCE Guided Notes N4",
             "REVEAL Sample response (accept any change-as-evidence).", "NEXT Apply: classify evidence."])

# ================================================================================
# SLIDE 32 — APPLICATION: which change shows energy?
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "C"); hud_bubble(s, "EVIDENCE")
text(s, 0.55, 1.02, 11.7, 0.7, "Which change shows energy at work?", size=T_TITLE, color=PRIMARY, bold=True)
opts = [
    ("A toy car starts to roll.", True),
    ("A rock keeps sitting still.", False),
    ("A room stays dark.", False),
]
y = 2.5
for i, (txt, is_yes) in enumerate(opts):
    cy = y + i * 1.25
    rect(s, 1.5, cy, 10.3, 1.0, PAPER, line_color=PRIMARY, line_w=1.25, rounded=True)
    text(s, 1.8, cy + 0.22, 9.7, 0.6, txt, size=T_BODY, color=INK, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.55, 6.4, 11.7, 0.5, "Pick one. Tell your partner why.", size=T_BODY_S, color=INK_SOFT, align=PP_ALIGN.CENTER, italic=True)
slide_number(s)
set_note(s, ["MODE Apply · evidence", "TIME 3 min", "STUDENT RESOURCE none",
             "ASK Which one shows a change (energy at work)?", "LISTEN FOR 'the toy car'",
             "REVEAL The toy car starts to roll — a change. Then say aloud: 'Look for a change — that is the evidence of energy.' (Spoken after the vote; it is not on the question slide.)", "NEXT Return to the Big Question."])

# ================================================================================
# SLIDE 33 — BQ · NOW I THINK (return)
# ================================================================================
s = new_slide(SURFACE)
chapter_tab(s); mode_badge(s, "N"); hud_bubble(s, "WRITE")
notes_heading(s, "BQ", "BQ · Now I Think", "Guided Notes p. 3")
rect(s, 1.5, 2.3, 11.0, 1.75, PRIMARY, rounded=True)
text(s, 1.8, 2.45, 10.4, 0.45, "BIG QUESTION", size=24, color=ACCENT, bold=True, caps=True)
text(s, 1.8, 2.9, 10.4, 1.05, "Where can we observe evidence of energy causing change?", size=T_BODY, color=WHITE, bold=True)
text(s, 1.5, 4.3, 11.0, 0.5, "Now I think…", size=T_BODY, color=INK, bold=True)
write_line(s, 1.5, 5.0, 10.5)
write_line(s, 1.5, 5.7, 10.5)
write_line(s, 1.5, 6.4, 10.5)
slide_number(s)
set_note(s, ["MODE Notes · BQ return", "TIME 3 min", "STUDENT RESOURCE Guided Notes p.3",
             "FRIDAY CLOCK Start this slide by minute 9.5; if you are later, do NOT start it before the quiz - students write it after handing in the quiz or at home / in catch-up. The quiz is handed out by minute 12.",
             "ASK Answer the Big Question now.", "LISTEN FOR any change named as evidence",
             "NEXT Friday quiz (Session 3). Optional end-of-chapter review slides 34-45 are for a review day or FLEX only."])

# ================================================================================
# END-OF-CHAPTER REVIEW (4–6 MCQ, question state + answer state)
# ================================================================================
REVIEW = [
    {"q": "Energy is best described as —",
     "opts": ["a visible glow", "something only batteries have", "the ability to cause change", "a kind of fuel"],
     "correct": 2, "type": "concept",
     "explain": "Energy is the ability to cause change (Reader p. 1)."},
    {"q": "A pencil is dull, then you sharpen it. What change do you observe?",
     "opts": ["It gets shorter and sharper", "It gets longer", "It changes color", "It disappears"],
     "correct": 0, "type": "visual",
     "explain": "The pencil becomes shorter and sharper — a change."},
    {"q": "Which object has stored energy that can cause a change LATER?",
     "opts": ["A ball already rolling", "A toy already moving", "A flashlight already on", "A stretched rubber band"],
     "correct": 3, "type": "scenario",
     "explain": "The rubber band stores energy; it changes when released."},
    {"q": "A carousel spins and plays music. Which two forms of energy come from the spinning and the music?",
     "opts": ["only light", "motion and sound", "motion and silence", "sound and stillness"],
     "correct": 1, "type": "comparison",
     "explain": "The spinning is motion; the music is sound (Reader p. 3)."},
    {"q": "How do we know energy is involved if we cannot see it?",
     "opts": ["We observe a change happen", "Energy can always be seen", "We guess without evidence", "Nothing can change"],
     "correct": 0, "type": "concept",
     "explain": "We see a change — like movement — as evidence."},
    {"q": "A battery sits still in a flashlight. Does it have energy?",
     "opts": ["No — still objects have no energy", "Only when it is moving", "Yes — stored energy that can cause change later", "Only when the flashlight is on"],
     "correct": 2, "type": "scenario",
     "explain": "A battery stores energy. It can cause a change later."},
]

def review_question(slide_q, num, item):
    chapter_tab(slide_q); mode_badge(slide_q, "C")
    text(slide_q, 0.55, 1.02, 11.7, 0.7, f"Review {num} — {item['type']}", size=T_HEAD, color=PRIMARY, bold=True, font=FONT_DISPLAY)
    text(slide_q, 0.55, 1.66, 11.7, 1.05, item["q"], size=T_BODY, color=INK, bold=True)
    y = 2.78
    letters = ["A", "B", "C", "D"]
    for i, opt in enumerate(item["opts"]):
        cy = y + i * 0.88
        rect(slide_q, 1.0, cy, 11.3, 0.74, PAPER, line_color=RULE, line_w=1.0, rounded=True)
        text(slide_q, 1.25, cy + 0.13, 0.6, 0.5, letters[i], size=T_OPT, color=ACCENT, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(slide_q, 1.95, cy + 0.11, 10.1, 0.54, opt, size=T_OPT, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    slide_number(slide_q)

def review_answer(slide_a, num, item):
    chapter_tab(slide_a); mode_badge(slide_a, "C"); hud_bubble(slide_a, "CHECK")
    text(slide_a, 0.55, 1.02, 11.7, 0.7, f"Review {num} — answer", size=T_HEAD, color=PRIMARY, bold=True, font=FONT_DISPLAY)
    text(slide_a, 0.55, 1.66, 11.7, 1.05, item["q"], size=T_BODY, color=INK, bold=True)
    y = 2.78
    letters = ["A", "B", "C", "D"]
    for i, opt in enumerate(item["opts"]):
        cy = y + i * 0.88
        is_correct = (i == item["correct"])
        fill = GOLD_TINT if is_correct else PAPER
        line_c = ACCENT if is_correct else RULE
        rect(slide_a, 1.0, cy, 11.3, 0.74, fill, line_color=line_c, line_w=1.5 if is_correct else 1.0, rounded=True)
        text(slide_a, 1.25, cy + 0.13, 0.6, 0.5, letters[i], size=T_OPT, color=ACCENT, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(slide_a, 1.95, cy + 0.11, 10.1, 0.54, opt, size=T_OPT, color=INK, bold=is_correct, anchor=MSO_ANCHOR.MIDDLE)
    rect(slide_a, 0.55, 6.35, 12.23, 0.72, MIST, line_color=RULE, line_w=1.0, rounded=True)
    text(slide_a, 0.8, 6.47, 11.2, 0.5, item["explain"], size=T_BODY_S, color=INK, anchor=MSO_ANCHOR.MIDDLE)
    slide_number(slide_a)

for idx, item in enumerate(REVIEW, 1):
    sq = new_slide(SURFACE)
    review_question(sq, idx, item)
    set_note(sq, [f"MODE Check · review Q{idx}", "STUDENT RESOURCE none",
                  "ASK Read aloud; students vote A/B/C/D.", "REVEAL Do not reveal yet.",
                  "NEXT Reveal the answer."])
    sa = new_slide(SURFACE)
    review_answer(sa, idx, item)
    set_note(sa, [f"MODE Check · review Q{idx} answer", "REVEAL " + REVIEW[idx-1]["opts"][item["correct"]],
                  "NEXT Next question (or close)."])

# ================================================================================
# save
# ================================================================================
out = os.path.join(OUT, "01-ch1-energy-causes-change-premium-hybrid-v1.pptx")
prs.save(out)
print("built slides:", len(prs.slides._sldIdLst))
print("saved:", out)
