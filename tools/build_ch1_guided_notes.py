"""Phase 3 — Chapter 1 Guided Notes FINAL (student + teacher key).

Notes-first architecture: BQ / V1 / V2 / N1 / N2 / N3 / N4 (permanent student navigation).
Consumes the FROZEN Unit 1 Visual System v1.0 tokens (assets/visual-system/design-tokens.json).
Ch1 theme = Discovery / Evidence (primary #1F2A5A · accent #A67C16 · surface #F5EEDC · neutral #7A5620).

Outputs:
  production/premium-notes/01-ch1-energy-causes-change-guided-notes.{docx,pdf}
  production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.{docx,pdf}

Authoritative source: CKSci Student Reader Chapter 1 "Energy Causes Change" (Reader pp. 1-6).
Run: .venv/bin/python tools/build_ch1_guided_notes.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT_DIR = os.path.join(ROOT, "production", "premium-notes")

# ---------------------------------------------------------------- FROZEN tokens (Ch1 + unit neutrals)
INK       = RGBColor(0x1A, 0x1D, 0x26)
INK_SOFT  = RGBColor(0x4A, 0x52, 0x68)
PAPER     = RGBColor(0xFF, 0xFF, 0xFF)
MIST      = RGBColor(0xF6, 0xF7, 0xF9)
RULE      = RGBColor(0xD8, 0xDC, 0xE4)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

CH1_PRIMARY = RGBColor(0x1F, 0x2A, 0x5A)   # deep navy
CH1_ACCENT  = RGBColor(0xA6, 0x7C, 0x16)   # warm gold
CH1_NEUTRAL = RGBColor(0x7A, 0x56, 0x20)   # muted amber-brown
CH1_SURFACE = RGBColor(0xF5, 0xEE, 0xDC)   # cream

PRIMARY_HEX = "1F2A5A"
ACCENT_HEX  = "A67C16"
NEUTRAL_HEX = "7A5620"
SURFACE_HEX = "F5EEDC"
INK_HEX     = "1A1D26"
INK_SOFT_HEX= "4A5268"
MIST_HEX    = "F6F7F9"
RULE_HEX    = "D8DCE4"

FONT = "Avenir Next"
BODY_SZ    = 14.0     # body 13.5-14
PROMPT_SZ  = 14.5     # prompts 14-15
SECTION_SZ = 16.0     # major sections 15-17
TITLE_SZ   = 23.0     # title 21-24
CAPTION_SZ = 12.0     # captions 11.5-12
ATTR_SZ    = 9.5      # attribution/page refs 9-10

# Margins 0.55" (within 0.50-0.60 target). Usable width = 7.4"
MARGIN = Inches(0.55)
USABLE_IN = 8.5 - 2 * 0.55   # 7.4"
FULL_W = Inches(USABLE_IN)

# Blank geometry (handwriting zone). Underscore advance ~= 0.5em in Avenir Next.
def blank_count(target_in, size_pt):
    return max(2, int(round(target_in * 144.0 / size_pt)))

# ---------------------------------------------------------------- low-level helpers
def _shade(cell, hexstr):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexstr)
    tcPr.append(shd)

def _margins(cell, top=60, left=90, bottom=60, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement('w:tcMar')
    for tag, v in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        e = OxmlElement('w:%s' % tag); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa'); m.append(e)
    tcPr.append(m)

def _border(cell, **edges):
    tcPr = cell._tc.get_or_add_tcPr()
    tb = OxmlElement('w:tcBorders')
    for edge, spec in edges.items():
        e = OxmlElement('w:%s' % edge)
        e.set(qn('w:val'), spec.get('val', 'single'))
        e.set(qn('w:sz'), str(spec.get('sz', 6)))
        e.set(qn('w:color'), spec.get('color', INK_HEX))
        tb.append(e)
    tcPr.append(tb)

def _no_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:%s' % edge); e.set(qn('w:val'), 'none'); borders.append(e)
    tblPr.append(borders)

def _row_height(row, dxa, rule='atLeast'):
    trPr = row._tr.get_or_add_trPr()
    trH = OxmlElement('w:trHeight'); trH.set(qn('w:val'), str(dxa)); trH.set(qn('w:hRule'), rule)
    trPr.append(trH)

def _vcenter(cell):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def _run(p, text, size=BODY_SZ, bold=False, italic=False, color=INK, caps=False,
         underline=False, font=FONT):
    r = p.add_run(text.upper() if caps else text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.color.rgb = color; r.font.name = font
    r.font.underline = underline
    rPr = r._element.get_or_add_rPr()
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), font); rf.set(qn('w:hAnsi'), font); rf.set(qn('w:cs'), font)
    rPr.append(rf)
    return r

def _spacing(p, before=0, after=4, line_pt=None):
    """Set spacing on a single w:spacing element (avoids duplicate spacing nodes)."""
    from docx.enum.text import WD_LINE_SPACING
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    if line_pt is not None:
        pf.line_spacing = Pt(line_pt)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    return p

def _para(doc, text="", size=BODY_SZ, bold=False, italic=False, color=INK, caps=False,
          before=0, after=4, line_pt=None, align=None, underline=False):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    _spacing(p, before, after, line_pt)
    if text:
        _run(p, text, size=size, bold=bold, italic=italic, color=color, caps=caps, underline=underline)
    else:
        r = p.add_run(""); r.font.size = Pt(2)   # keep empty spacers tiny
    return p

def _bottom_rule(p, sz=8, color=INK_HEX):
    """Add a bottom border = handwriting line."""
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), str(sz)); b.set(qn('w:space'), '4'); b.set(qn('w:color'), color)
    bdr.append(b); pPr.append(bdr)
    return p

def _writing_line(doc, size=BODY_SZ, gap_pt=28):
    """One ruled handwriting line (bottom border) with exact line spacing."""
    p = doc.add_paragraph()
    _spacing(p, after=0, line_pt=gap_pt)
    _bottom_rule(p, sz=8, color=INK_HEX)
    # add a thin spacer run so the paragraph has height
    _run(p, "", size=size)
    return p

# ---------------------------------------------------------------- fill-in blanks
def _blank_run(p, answer, width_in, size=BODY_SZ, is_key=False):
    """Render a blank (student) or the filled answer (key)."""
    if is_key:
        # exact answer: bold + neutral amber-brown (grayscale-safe, distinct)
        _run(p, answer, size=size, bold=True, color=CH1_NEUTRAL)
    else:
        n = blank_count(width_in, size)
        _run(p, "_" * n, size=size, underline=True, color=INK)

def _fill_line(doc, lead, blanks, trail="", size=BODY_SZ, lead_bold=False, is_key=False,
               after=4, line_pt=26):
    """blanks = list of (answer, width_in) tuples. Multi-word answers = separate blank tuples."""
    p = doc.add_paragraph()
    _spacing(p, 0, after, line_pt=line_pt)  # generous handwriting clearance
    if lead:
        _run(p, lead + " ", size=size, bold=lead_bold, color=INK)
    for i, (ans, w) in enumerate(blanks):
        if i > 0:
            _run(p, "  ", size=size, color=INK)
        _blank_run(p, ans, w, size=size, is_key=is_key)
    if trail:
        _run(p, " " + trail, size=size, color=INK)
    return p

# ---------------------------------------------------------------- structural components
def _band(doc, text, color_hex, size=15, sub=None, width=None, text_color=WHITE):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t)
    c = t.cell(0, 0)
    c.width = width or FULL_W
    _margins(c, top=70, left=110, bottom=70, right=110)
    _shade(c, color_hex); _vcenter(c)
    p = c.paragraphs[0]
    _run(p, text, size=size, bold=True, color=text_color)
    if sub:
        p2 = c.add_paragraph()
        _run(p2, sub, size=9.5, italic=True, color=RGBColor(0xD8, 0xDC, 0xE4))
    return t

def _badge(doc, text, fill_hex=INK_HEX, size=9.5):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t); t.alignment = 1
    c = t.cell(0, 0); c.width = Inches(2.1)
    _margins(c, top=35, left=50, bottom=35, right=50); _shade(c, fill_hex); _vcenter(c)
    p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(p, text, size=size, bold=True, color=WHITE)
    return t

def _section_head(doc, code, title, color=CH1_PRIMARY, size=SECTION_SZ):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t)
    c = t.cell(0, 0); c.width = FULL_W
    _margins(c, top=12, left=0, bottom=18, right=0)
    p = c.paragraphs[0]
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '10'); b.set(qn('w:color'), PRIMARY_HEX)
    bdr.append(b); pPr.append(bdr)
    _run(p, code + "   ", size=size, bold=True, color=CH1_ACCENT, caps=True)
    _run(p, title, size=size, bold=True, color=color, caps=True)
    return t

def _page_ref(doc, text):
    return _para(doc, text, size=ATTR_SZ, italic=True, color=INK_SOFT, after=4)

def _caption(doc, text, after=4):
    return _para(doc, text, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=after)

def _panel(doc, lead, text, lead_color=CH1_NEUTRAL, fill_hex=SURFACE_HEX, size=BODY_SZ):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t)
    c = t.cell(0, 0); c.width = FULL_W
    _margins(c, top=60, left=110, bottom=60, right=110)
    _shade(c, fill_hex)
    _border(c, left=dict(sz=18, color=ACCENT_HEX))
    p = c.paragraphs[0]
    _run(p, lead + "   ", size=size, bold=True, color=lead_color, caps=True)
    _run(p, text, size=size, color=INK)
    return t

def _model_chain(doc, words, size=14, fill_hex=PRIMARY_HEX, arrow_color=CH1_ACCENT):
    n = len(words); cols = n * 2 - 1
    box_w = Inches(1.9); arr_w = Inches(0.55)
    t = doc.add_table(rows=1, cols=cols)
    _no_borders(t); t.alignment = 1
    for idx in range(cols):
        c = t.cell(0, idx)
        c.width = box_w if idx % 2 == 0 else arr_w
        _margins(c, top=40, left=6, bottom=40, right=6); _vcenter(c)
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if idx % 2 == 0:
            _shade(c, fill_hex)
            _run(p, words[idx // 2], size=size, bold=True, color=WHITE)
        else:
            _run(p, "\u2192", size=size + 2, bold=True, color=arrow_color)
        _row_height(t.rows[0], 440, rule='exact')
    return t

# ---------------------------------------------------------------- header / BQ / vocab
def header(doc, is_key=False):
    # kicker
    _para(doc, "UNIT 1 \u00b7 ENERGY TRANSFER & TRANSFORMATION", size=ATTR_SZ,
          bold=True, color=INK_SOFT, after=4, caps=True)
    _para(doc, "", after=2)
    # title
    _para(doc, "Chapter 1 \u00b7 Energy Causes Change", size=TITLE_SZ, bold=True,
          color=CH1_PRIMARY, after=2)
    if is_key:
        _para(doc, "Teacher Key \u00b7 Guided Notes", size=CAPTION_SZ, bold=True,
              color=CH1_NEUTRAL, after=4)
    else:
        _badge(doc, "GUIDED NOTES")
        _para(doc, "", after=4)
    # name / homeroom line
    p = doc.add_paragraph()
    _spacing(p, 0, 40, line_pt=26)
    _run(p, "Name: ", size=CAPTION_SZ, bold=True, color=INK)
    _run(p, "_" * 26, size=CAPTION_SZ, underline=True, color=INK)
    _run(p, "     Homeroom:  ", size=CAPTION_SZ, bold=True, color=INK)
    for i, lbl in enumerate(("4A", "4B", "4C", "4D")):
        _run(p, ("  " if i else "") + "\u25CB  " + lbl, size=CAPTION_SZ, color=INK)

def big_question(doc, is_key=False, sample=None):
    _band(doc, "BQ   Where can we observe evidence of energy causing change?", PRIMARY_HEX, size=16)
    _para(doc, "", after=4)
    _para(doc, "My first thinking", size=PROMPT_SZ, bold=True, color=CH1_PRIMARY, after=4)
    if is_key and sample:
        _para(doc, sample, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=4)
    _writing_line(doc, size=PROMPT_SZ, gap_pt=28)
    _writing_line(doc, size=PROMPT_SZ, gap_pt=28)

def vocab_v1(doc, is_key=False):
    _section_head(doc, "V1", "Vocabulary \u2014 Energy & Change", color=CH1_PRIMARY)
    _page_ref(doc, "Reader p. 1")
    _fill_line(doc, "energy \u2014 the ability to cause", [("change", 1.4)], ".", is_key=is_key)
    _fill_line(doc, "change \u2014 to become", [("different", 1.6)], ".", is_key=is_key)

def vocab_v2(doc, is_key=False):
    _section_head(doc, "V2", "Vocabulary \u2014 Stored Energy", color=CH1_PRIMARY)
    _page_ref(doc, "Reader p. 4")
    _fill_line(doc, "stored energy \u2014 energy that has the ability to cause change at a",
               [("later", 1.1)], "time.", is_key=is_key)

# ---------------------------------------------------------------- core notes
def note_n1(doc, is_key=False):
    _section_head(doc, "N1", "Energy Causes Change", color=CH1_PRIMARY)
    _page_ref(doc, "Reader pp. 1\u20132")
    _fill_line(doc, "Energy has the ability to", [("cause", 0.9), ("change", 1.4)], ".",
               is_key=is_key, lead_bold=True)
    _caption(doc, "When you see a change, you are seeing evidence of energy.", after=6)
    _model_chain(doc, ["ENERGY", "CHANGE", "EVIDENCE"])
    _para(doc, "", after=4)
    _fill_line(doc, "A change is", [("evidence", 1.5)], "that energy is involved.", is_key=is_key)

def note_n2(doc, is_key=False, samples=None):
    _section_head(doc, "N2", "Energy Occurs in Different Forms", color=CH1_PRIMARY)
    _page_ref(doc, "Reader p. 3")
    _caption(doc, "Write or draw one example that shows a change for each form.", after=6)
    forms = ["motion", "sound", "light", "heat", "electrical energy"]
    t = doc.add_table(rows=1 + len(forms), cols=2)
    _no_borders(t)
    widths = [Inches(2.3), Inches(USABLE_IN - 2.3)]
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w
    # header
    hc0, hc1 = t.cell(0, 0), t.cell(0, 1)
    for c in (hc0, hc1):
        _margins(c, top=40, left=80, bottom=40, right=80); _shade(c, PRIMARY_HEX); _vcenter(c)
    _run(hc0.paragraphs[0], "FORM", size=CAPTION_SZ, bold=True, color=WHITE, caps=True)
    _run(hc1.paragraphs[0], "ONE EXAMPLE THAT SHOWS A CHANGE", size=CAPTION_SZ, bold=True, color=WHITE, caps=True)
    _row_height(t.rows[0], 420, rule='exact')
    for i, f in enumerate(forms):
        c0, c1 = t.cell(i + 1, 0), t.cell(i + 1, 1)
        _margins(c0, top=40, left=80, bottom=40, right=80)
        _margins(c1, top=40, left=80, bottom=40, right=80)
        _vcenter(c0); _vcenter(c1)
        _run(c0.paragraphs[0], f, size=BODY_SZ, bold=True, color=CH1_PRIMARY)
        _border(c1, bottom=dict(sz=8, color=INK_HEX))
        if is_key and samples and f in samples:
            _run(c1.paragraphs[0], samples[f], size=CAPTION_SZ, italic=True, color=INK_SOFT)
        _row_height(t.rows[i + 1], 680, rule='atLeast')
    return t

def note_n3(doc, is_key=False, samples=None):
    _section_head(doc, "N3", "Objects Can Store Energy", color=CH1_PRIMARY)
    _page_ref(doc, "Reader pp. 4\u20135")
    _model_chain(doc, ["STORED ENERGY", "RELEASE", "CHANGE"], size=12)
    _para(doc, "", after=4)
    examples = ["battery (in a flashlight)", "stretched rubber band", "raised object (apple)"]
    t = doc.add_table(rows=1 + len(examples), cols=2)
    _no_borders(t)
    widths = [Inches(3.0), Inches(USABLE_IN - 3.0)]
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w
    hc0, hc1 = t.cell(0, 0), t.cell(0, 1)
    for c in (hc0, hc1):
        _margins(c, top=40, left=80, bottom=40, right=80); _shade(c, PRIMARY_HEX); _vcenter(c)
    _run(hc0.paragraphs[0], "EXAMPLE", size=CAPTION_SZ, bold=True, color=WHITE, caps=True)
    _run(hc1.paragraphs[0], "WHAT CHANGE COULD HAPPEN LATER?", size=CAPTION_SZ, bold=True, color=WHITE, caps=True)
    _row_height(t.rows[0], 420, rule='exact')
    for i, ex in enumerate(examples):
        c0, c1 = t.cell(i + 1, 0), t.cell(i + 1, 1)
        _margins(c0, top=40, left=80, bottom=40, right=80)
        _margins(c1, top=40, left=80, bottom=40, right=80)
        _vcenter(c0); _vcenter(c1)
        _run(c0.paragraphs[0], ex, size=BODY_SZ, bold=True, color=INK)
        _border(c1, bottom=dict(sz=8, color=INK_HEX))
        if is_key and samples and ex in samples:
            _run(c1.paragraphs[0], samples[ex], size=CAPTION_SZ, italic=True, color=INK_SOFT)
        _row_height(t.rows[i + 1], 680, rule='atLeast')
    _para(doc, "", after=4)
    _fill_line(doc, "Objects also have stored energy because of their",
               [("position", 1.4)], ".", is_key=is_key)

def note_n4(doc, is_key=False, sample=None):
    _section_head(doc, "N4", "Recognizing Evidence", color=CH1_PRIMARY)
    _page_ref(doc, "Reader pp. 1\u20136")
    _caption(doc, "Draw a change you observed. Show what it looked like BEFORE and AFTER.", after=6)
    t = doc.add_table(rows=1, cols=2)
    _no_borders(t)
    half = Inches((USABLE_IN - 0.2) / 2)
    for idx, lab in enumerate(("BEFORE", "AFTER")):
        c = t.cell(0, idx); c.width = half
        _margins(c, top=20, left=60, bottom=20, right=60)
        for edge in ('top', 'left', 'bottom', 'right'):
            _border(c, **{edge: dict(sz=8, color=PRIMARY_HEX)})
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _run(p, lab, size=14, bold=True, color=CH1_ACCENT, caps=True)
        _row_height(t.rows[0], 2000, rule='exact')
    _para(doc, "", after=4)
    _para(doc, "What changed?", size=BODY_SZ, bold=True, color=INK, after=4)
    _writing_line(doc, size=BODY_SZ, gap_pt=28)
    _para(doc, "", after=6)
    # CHECK YOUR THINKING
    _section_head(doc, "CHECK", "Your Thinking", color=CH1_PRIMARY, size=14)
    _para(doc, "How do we know energy is involved if we cannot see energy itself?",
          size=PROMPT_SZ, bold=True, color=INK, after=6)
    _caption(doc, "Start with: \u201cWe know because we see \u2026\u201d", after=4)
    if is_key and sample:
        _para(doc, sample, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=4)
    _writing_line(doc, size=PROMPT_SZ, gap_pt=28)
    _writing_line(doc, size=PROMPT_SZ, gap_pt=28)

def bq_return(doc, is_key=False, sample=None):
    _band(doc, "BQ \u00b7 NOW I THINK   Where can we observe evidence of energy causing change?",
          PRIMARY_HEX, size=15)
    _para(doc, "", after=4)
    if is_key and sample:
        _para(doc, sample, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=4)
    for _ in range(3):
        _writing_line(doc, size=PROMPT_SZ, gap_pt=28)

def _footer(doc, label):
    footer = doc.sections[0].footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr'); top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single'); top.set(qn('w:sz'), '6'); top.set(qn('w:color'), RULE_HEX)
    bdr.append(top); pPr.append(bdr)
    _run(p, label, size=8.5, color=INK_SOFT)

# ---------------------------------------------------------------- document assembly
def new_doc():
    doc = Document()
    for _p in list(doc.paragraphs):
        _p._p.getparent().remove(_p._p)
    sec = doc.sections[0]
    sec.page_width = Inches(8.5); sec.page_height = Inches(11)
    sec.left_margin = MARGIN; sec.right_margin = MARGIN
    sec.top_margin = Inches(0.5); sec.bottom_margin = Inches(0.5)
    st = doc.styles['Normal']
    st.font.name = FONT; st.font.size = Pt(BODY_SZ); st.font.color.rgb = INK
    return doc

def _page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def build_student():
    doc = new_doc()
    _footer(doc, "Unit 1 \u00b7 Chapter 1 \u00b7 Guided Notes \u00b7 Energy Causes Change")
    header(doc, is_key=False)
    big_question(doc, is_key=False)
    vocab_v1(doc, is_key=False)
    note_n1(doc, is_key=False)
    _page_break(doc)
    note_n2(doc, is_key=False)
    _para(doc, "", after=4)
    vocab_v2(doc, is_key=False)
    note_n3(doc, is_key=False)
    note_n4(doc, is_key=False)
    bq_return(doc, is_key=False)
    out = os.path.join(OUT_DIR, "01-ch1-energy-causes-change-guided-notes.docx")
    doc.save(out)
    return out

def build_key():
    doc = new_doc()
    _footer(doc, "Unit 1 \u00b7 Chapter 1 \u00b7 Guided Notes \u00b7 Teacher Key")
    header(doc, is_key=True)
    # legend (compact single line)
    p = doc.add_paragraph()
    _spacing(p, 0, 6, line_pt=16)
    _run(p, "KEY  ", size=CAPTION_SZ, bold=True, color=CH1_NEUTRAL, caps=True)
    _run(p, "Bold brown = exact answer \u00b7 Italic gray = sample / acceptable response.",
         size=CAPTION_SZ, italic=True, color=INK_SOFT)
    big_question(doc, is_key=True,
                 sample="Sample: \u201cA pencil gets shorter and sharper.\u201d (Accept any observed change.)")
    vocab_v1(doc, is_key=True)
    note_n1(doc, is_key=True)
    _page_break(doc)
    note_n2(doc, is_key=True, samples={
        "motion": "a ball rolls across the floor",
        "sound": "a drum makes a noise",
        "light": "a flashlight lights up the room",
        "heat": "a warm mug warms my hands",
        "electrical energy": "a fan spins when plugged in",
    })
    _para(doc, "", after=4)
    vocab_v2(doc, is_key=True)
    note_n3(doc, is_key=True, samples={
        "battery (in a flashlight)": "the flashlight lights up",
        "stretched rubber band": "it snaps and makes a sound",
        "raised object (apple)": "it falls down",
    })
    note_n4(doc, is_key=True,
            sample="Sample: \u201cWe know because we see a change, like a ball starting to move or a light turning on.\u201d "
                   "(Accept any response connecting a change to evidence of energy.)")
    bq_return(doc, is_key=True,
              sample="Sample: \u201cWe observe evidence of energy causing change everywhere \u2014 things move, make sound, "
                     "light up, heat up, or change shape.\u201d (Accept any response naming a change as evidence.)")
    out = os.path.join(OUT_DIR, "01-ch1-energy-causes-change-guided-notes-key.docx")
    doc.save(out)
    return out

if __name__ == "__main__":
    a = build_student()
    b = build_key()
    print("saved", a)
    print("saved", b)
