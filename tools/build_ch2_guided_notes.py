"""Phase 7 — Chapter 2 Guided Notes FINAL (student + teacher key).

Notes-first architecture: BQ / V1 / V2 / N1 / N2 / N3 (permanent student navigation).
Consumes the FROZEN Unit 1 Visual System v1.0 tokens (assets/visual-system/design-tokens.json).
Ch2 theme = Motion (primary #0F5A5C · accent #0E8A97 · neutral #5B6770 · surface #FFFFFF).

Outputs:
  production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.{docx,pdf}
  production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes-key.{docx,pdf}

Authoritative source: CKSci Student Reader Chapter 2 "Moving Objects Have Energy" (Reader pp. 7-12)
+ Teacher Guide Lesson 3. See docs/chapter-02/CH2_SOURCE_MAP.md.
Run: .venv/bin/python tools/build_ch2_guided_notes.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT_DIR = os.path.join(ROOT, "production", "premium-notes")

# ---------------------------------------------------------------- FROZEN tokens (Ch2 + unit neutrals)
INK       = RGBColor(0x1A, 0x1D, 0x26)
INK_SOFT  = RGBColor(0x4A, 0x52, 0x68)
PAPER     = RGBColor(0xFF, 0xFF, 0xFF)
MIST      = RGBColor(0xF6, 0xF7, 0xF9)
RULE      = RGBColor(0xD8, 0xDC, 0xE4)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

CH2_PRIMARY = RGBColor(0x0F, 0x5A, 0x5C)   # deep teal
CH2_ACCENT  = RGBColor(0x0E, 0x8A, 0x97)   # aqua
CH2_NEUTRAL = RGBColor(0x5B, 0x67, 0x70)   # slate
CH2_SURFACE = RGBColor(0xFF, 0xFF, 0xFF)   # white

PRIMARY_HEX = "0F5A5C"
ACCENT_HEX  = "0E8A97"
NEUTRAL_HEX = "5B6770"
SURFACE_HEX = "FFFFFF"
INK_HEX     = "1A1D26"
INK_SOFT_HEX= "4A5268"
MIST_HEX    = "F6F7F9"
RULE_HEX    = "D8DCE4"

FONT = "Avenir Next"
BODY_SZ    = 14.0
PROMPT_SZ  = 14.5
SECTION_SZ = 16.0
TITLE_SZ   = 23.0
CAPTION_SZ = 12.0
ATTR_SZ    = 9.5

# Margins 0.55". Usable width = 7.4"
MARGIN = Inches(0.55)
USABLE_IN = 8.5 - 2 * 0.55
FULL_W = Inches(USABLE_IN)

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
        r = p.add_run(""); r.font.size = Pt(2)
    return p

def _bottom_rule(p, sz=8, color=INK_HEX):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), str(sz)); b.set(qn('w:space'), '4'); b.set(qn('w:color'), color)
    bdr.append(b); pPr.append(bdr)
    return p

def _writing_line(doc, size=BODY_SZ, gap_pt=28, n=1):
    """n ruled lines as table rows. Adjacent paragraph borders collapse to one rule."""
    t = doc.add_table(rows=n, cols=1)
    _no_borders(t)
    for r in t.rows:
        c = r.cells[0]
        c.width = FULL_W
        _margins(c, top=0, left=0, bottom=0, right=0)
        _border(c, bottom=dict(sz=8, color=INK_HEX))
        pp = c.paragraphs[0]
        _spacing(pp, 0, 0, line_pt=2)
        _run(pp, "", size=2)
        _row_height(r, int(gap_pt * 20), rule='exact')
    return t

# ---------------------------------------------------------------- fill-in blanks
def _blank_run(p, answer, width_in, size=BODY_SZ, is_key=False):
    if is_key:
        _run(p, answer, size=size, bold=True, color=CH2_NEUTRAL)
    else:
        n = blank_count(width_in, size)
        _run(p, "_" * n, size=size, underline=True, color=INK)

def _fill_line(doc, lead, blanks, trail="", size=BODY_SZ, lead_bold=False, is_key=False,
               after=4, line_pt=26):
    p = doc.add_paragraph()
    _spacing(p, 0, after, line_pt=line_pt)
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

def _section_head(doc, code, title, color=CH2_PRIMARY, size=SECTION_SZ):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t)
    c = t.cell(0, 0); c.width = FULL_W
    _margins(c, top=12, left=0, bottom=18, right=0)
    p = c.paragraphs[0]
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '10'); b.set(qn('w:color'), PRIMARY_HEX)
    bdr.append(b); pPr.append(bdr)
    _run(p, code + "   ", size=size, bold=True, color=CH2_ACCENT, caps=True)
    _run(p, title, size=size, bold=True, color=color, caps=True)
    return t

def _page_ref(doc, text):
    return _para(doc, text, size=ATTR_SZ, italic=True, color=INK_SOFT, after=4)

def _caption(doc, text, after=4):
    return _para(doc, text, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=after)

def _panel(doc, lead, text, lead_color=CH2_NEUTRAL, fill_hex=MIST_HEX, size=BODY_SZ):
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

def _model_chain(doc, words, size=12, fill_hex=PRIMARY_HEX, arrow_color=CH2_ACCENT, box_w=2.1):
    n = len(words); cols = n * 2 - 1
    arr_w = Inches(0.5)
    t = doc.add_table(rows=1, cols=cols)
    _no_borders(t); t.alignment = 1
    for idx in range(cols):
        c = t.cell(0, idx)
        c.width = Inches(box_w) if idx % 2 == 0 else arr_w
        _margins(c, top=40, left=6, bottom=40, right=6); _vcenter(c)
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if idx % 2 == 0:
            _shade(c, fill_hex)
            _run(p, words[idx // 2], size=size, bold=True, color=WHITE)
        else:
            _run(p, "\u2192", size=size + 2, bold=True, color=arrow_color)
        _row_height(t.rows[0], 500, rule='exact')
    return t

# ---------------------------------------------------------------- header / BQ / vocab
def header(doc, is_key=False):
    _para(doc, "UNIT 1 \u00b7 ENERGY TRANSFER & TRANSFORMATION", size=ATTR_SZ,
          bold=True, color=INK_SOFT, after=4, caps=True)
    _para(doc, "", after=2)
    _para(doc, "Chapter 2 \u00b7 Moving Objects Have Energy", size=TITLE_SZ, bold=True,
          color=CH2_PRIMARY, after=2)
    if is_key:
        _para(doc, "Teacher Key \u00b7 Guided Notes", size=CAPTION_SZ, bold=True,
              color=CH2_NEUTRAL, after=4)
    else:
        _badge(doc, "GUIDED NOTES")
        _para(doc, "", after=4)
    p = doc.add_paragraph()
    _spacing(p, 0, 40, line_pt=26)
    _run(p, "Name: ", size=CAPTION_SZ, bold=True, color=INK)
    _run(p, "_" * 26, size=CAPTION_SZ, underline=True, color=INK)
    _run(p, "     Homeroom:  ", size=CAPTION_SZ, bold=True, color=INK)
    for i, lbl in enumerate(("4A", "4B", "4C", "4D")):
        _run(p, ("  " if i else "") + "\u25CB  " + lbl, size=CAPTION_SZ, color=INK)

_ANCHORS = json.load(open(os.path.join(ROOT, "curriculum/chapter-02/ch2_anchor_map.json"), encoding="utf-8"))["anchors"]

def _cloze(code, index=0):
    lines = _ANCHORS[code]["lines"]
    lead, trail = lines[index].split("____", 1)
    blank_no = sum(1 for i in range(index) if "____" in lines[i])
    return lead.rstrip(), _ANCHORS[code]["answers"][blank_no], trail.lstrip()

BQ_EXACT = _ANCHORS["BQ"]["wording"] if "wording" in _ANCHORS["BQ"] else _ANCHORS["BQ"]["lines"][0]

def big_question(doc, is_key=False, sample=None):
    _band(doc, "BQ   " + BQ_EXACT, PRIMARY_HEX, size=16)
    _para(doc, "", after=4)
    _para(doc, "My first thinking", size=PROMPT_SZ, bold=True, color=CH2_PRIMARY, after=4)
    if is_key and sample:
        _para(doc, sample, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=4)
    _writing_line(doc, size=PROMPT_SZ, n=2)

def vocab_v1(doc, is_key=False):
    _section_head(doc, "V1", "Vocabulary \u2014 Motion", color=CH2_PRIMARY)
    _page_ref(doc, "Reader p. 7")
    lead, answer, trail = _cloze("V1")
    _fill_line(doc, lead, [(answer, 1.4)], trail, is_key=is_key)

def vocab_v2(doc, is_key=False):
    _section_head(doc, "V2", "Vocabulary \u2014 Energy of Motion", color=CH2_PRIMARY)
    _page_ref(doc, "Reader p. 9")
    lead, answer, trail = _cloze("V2")
    _fill_line(doc, lead, [(answer, 1.4)], trail, is_key=is_key)

# ---------------------------------------------------------------- core notes
def note_n1(doc, is_key=False):
    _section_head(doc, "N1", "Moving Objects Can Cause Changes", color=CH2_PRIMARY)
    _page_ref(doc, "Reader p. 8")
    lead, answer, trail = _cloze("N1", 0)
    _fill_line(doc, lead, [(answer, 1.4)], trail, is_key=is_key, lead_bold=True)
    _caption(doc, _ANCHORS["N1"]["lines"][1], after=6)
    lead, answer, trail = _cloze("N1", 2)
    _fill_line(doc, lead, [(answer, 1.2)], trail, is_key=is_key)

def observe_box(doc, is_key=False, sample=None):
    """Marble Collision BEFORE / AFTER observation box (the Chapter 2 demo)."""
    _panel(doc, "OBSERVE", "Marble collision \u2014 one moving marble rolls into a target marble.",
           lead_color=CH2_ACCENT, fill_hex=MIST_HEX)
    _para(doc, "", after=4)
    t = doc.add_table(rows=1, cols=2)
    _no_borders(t)
    half = Inches((USABLE_IN - 0.2) / 2)
    for idx, lab in enumerate(("BEFORE", "AFTER")):
        c = t.cell(0, idx); c.width = half
        _margins(c, top=20, left=60, bottom=20, right=60)
        for edge in ('top', 'left', 'bottom', 'right'):
            _border(c, **{edge: dict(sz=8, color=PRIMARY_HEX)})
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _run(p, lab, size=14, bold=True, color=CH2_ACCENT, caps=True)
        if is_key:
            p2 = c.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            sketch = ("Target marble is still.\nThe other marble rolls toward it." if lab == "BEFORE"
                      else "The target marble is moving.\nIt changed from still to moving.")
            _run(p2, sketch, size=11, italic=True, color=INK_SOFT)
        _row_height(t.rows[0], 3200, rule='exact')
    if is_key:
        _caption(doc, "Accept any sketch that shows the target still, then moving. The change matters more than the drawing.", after=2)
    _para(doc, "", after=4)
    _para(doc, "What changed?", size=BODY_SZ, bold=True, color=INK, after=4)
    if is_key and sample:
        _para(doc, sample, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=4)
    _writing_line(doc, size=BODY_SZ, n=2)

def note_n2(doc, is_key=False, sample=None):
    _section_head(doc, "N2", "Moving Objects Have Energy", color=CH2_PRIMARY)
    _page_ref(doc, "Reader p. 9")
    lead, answer, trail = _cloze("N2")
    _fill_line(doc, lead, [(answer, 1.4)], trail, is_key=is_key, lead_bold=True)
    _caption(doc, _ANCHORS["N2"]["lines"][1], after=6)
    _model_chain(doc, ["MOVING OBJECT", "CHANGE", "EVIDENCE"], size=12)
    _para(doc, "", after=6)
    observe_box(doc, is_key=is_key, sample=sample)

def note_n3(doc, is_key=False, samples=None):
    _section_head(doc, "N3", "People Use the Energy of Motion", color=CH2_PRIMARY)
    _page_ref(doc, "Reader pp. 10\u201312")
    _caption(doc, "Write or draw the change each moving object causes.", after=6)
    examples = ["hammer (swinging)", "pendulum (swinging)", "wind (moving air)"]
    t = doc.add_table(rows=1 + len(examples), cols=2)
    _no_borders(t)
    widths = [Inches(2.6), Inches(USABLE_IN - 2.6)]
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w
    hc0, hc1 = t.cell(0, 0), t.cell(0, 1)
    for c in (hc0, hc1):
        _margins(c, top=40, left=80, bottom=40, right=80); _shade(c, PRIMARY_HEX); _vcenter(c)
    _run(hc0.paragraphs[0], "MOVING OBJECT", size=CAPTION_SZ, bold=True, color=WHITE, caps=True)
    _run(hc1.paragraphs[0], "WHAT CHANGE DOES IT CAUSE?", size=CAPTION_SZ, bold=True, color=WHITE, caps=True)
    _row_height(t.rows[0], 420, rule='exact')
    for i, ex in enumerate(examples):
        c0, c1 = t.cell(i + 1, 0), t.cell(i + 1, 1)
        _margins(c0, top=40, left=80, bottom=40, right=80)
        _margins(c1, top=40, left=80, bottom=40, right=80)
        _vcenter(c0); _vcenter(c1)
        _run(c0.paragraphs[0], ex, size=BODY_SZ, bold=True, color=CH2_PRIMARY)
        _border(c1, bottom=dict(sz=8, color=INK_HEX))
        if is_key and samples and ex in samples:
            _run(c1.paragraphs[0], samples[ex], size=CAPTION_SZ, italic=True, color=INK_SOFT)
        _row_height(t.rows[i + 1], 1200, rule='atLeast')
    return t

def check_your_thinking(doc, is_key=False, sample=None):
    _section_head(doc, "CHECK", "Your Thinking", color=CH2_PRIMARY, size=14)
    _para(doc, "How do we know a moving object has energy?",
          size=PROMPT_SZ, bold=True, color=INK, after=6)
    _caption(doc, "Start with: \u201cWe know because the moving object causes \u2026\u201d", after=4)
    if is_key and sample:
        _para(doc, sample, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=4)
    _writing_line(doc, size=PROMPT_SZ, n=2)
    _para(doc, "", after=4)

def bq_return(doc, is_key=False, sample=None):
    _band(doc, "BQ \u00b7 NOW I THINK   " + BQ_EXACT, PRIMARY_HEX, size=15)
    _para(doc, "", after=4)
    if is_key and sample:
        _para(doc, sample, size=CAPTION_SZ, italic=True, color=INK_SOFT, after=4)
    _writing_line(doc, size=PROMPT_SZ, n=3)

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
    _footer(doc, "Unit 1 \u00b7 Chapter 2 \u00b7 Guided Notes \u00b7 Moving Objects Have Energy")
    header(doc, is_key=False)
    big_question(doc, is_key=False)
    vocab_v1(doc, is_key=False)
    note_n1(doc, is_key=False)
    _page_break(doc)
    vocab_v2(doc, is_key=False)
    note_n2(doc, is_key=False)
    _page_break(doc)
    note_n3(doc, is_key=False)
    check_your_thinking(doc, is_key=False)
    bq_return(doc, is_key=False)
    out = os.path.join(OUT_DIR, "02-ch2-moving-objects-have-energy-guided-notes.docx")
    doc.save(out)
    return out

def build_key():
    doc = new_doc()
    _footer(doc, "Unit 1 \u00b7 Chapter 2 \u00b7 Guided Notes \u00b7 Teacher Key")
    header(doc, is_key=True)
    p = doc.add_paragraph()
    _spacing(p, 0, 6, line_pt=16)
    _run(p, "KEY  ", size=CAPTION_SZ, bold=True, color=CH2_NEUTRAL, caps=True)
    _run(p, "Bold slate = exact answer \u00b7 Italic gray = sample / acceptable response.",
         size=CAPTION_SZ, italic=True, color=INK_SOFT)
    big_question(doc, is_key=True,
                 sample="Sample: \u201cA moving marble makes another marble move.\u201d (Accept any moving-object-causes-change response.)")
    vocab_v1(doc, is_key=True)
    note_n1(doc, is_key=True)
    _page_break(doc)
    vocab_v2(doc, is_key=True)
    note_n2(doc, is_key=True,
            sample="Sample: \u201cThe target marble changed from sitting still to moving.\u201d (Accept any before/after change.)")
    _page_break(doc)
    note_n3(doc, is_key=True, samples={
        "hammer (swinging)": "drives a nail into the wood",
        "pendulum (swinging)": "turns the clock gears",
        "wind (moving air)": "spins the turbine blades",
    })
    check_your_thinking(doc, is_key=True,
            sample="Sample: \u201cWe know because it causes a change.\u201d Accept any change-as-evidence response.")
    bq_return(doc, is_key=True,
              sample="Sample: \u201cA moving object has energy, and that energy causes a change.\u201d Accept any link among energy, change, and motion.")
    out = os.path.join(OUT_DIR, "02-ch2-moving-objects-have-energy-guided-notes-key.docx")
    doc.save(out)
    return out

if __name__ == "__main__":
    a = build_student()
    b = build_key()
    print("saved", a)
    print("saved", b)
