"""Shared helpers for the Chapter 1 note-format comparison builders."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# --- palette (energy theme, grayscale-safe) ---
NAVY = RGBColor(0x2F, 0x3C, 0x7E)
NAVY_HEX = "2F3C7E"
CORAL = RGBColor(0xC0, 0x3D, 0x3D)   # slightly deepened coral for print contrast
CORAL_HEX = "C03D3D"
GOLD = RGBColor(0xE8, 0xC5, 0x4A)
GOLD_HEX = "E8C54A"
INK = RGBColor(0x1F, 0x1F, 0x1F)
INK_HEX = "1F1F1F"
GRAY = RGBColor(0x55, 0x55, 0x55)
MID_HEX = "E8EAF2"   # light navy tint
LIGHT_HEX = "F4F4F8" # near-white
GLUE_HEX = "D9DBE6"  # glue strip tint
DASH_HEX = "9AA0B4"

BODY_FONT = "Calibri"
HEAD_FONT = "Cambria"


def set_run(run, size=12, bold=False, italic=False, color=INK, font=BODY_FONT, caps=False):
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    if caps:
        run.font.all_caps = True
    # ensure east-asian + cs fonts set
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font)
    rFonts.set(qn('w:hAnsi'), font)
    rFonts.set(qn('w:cs'), font)
    return run


def set_cell_border(cell, **kwargs):
    """kwargs: top/bottom/left/right = dict(sz=8, val='dashed'|'single'|'none', color='XXXXXX')."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right'):
        if edge in kwargs:
            spec = kwargs[edge]
            el = tcBorders.find(qn('w:%s' % edge))
            if el is None:
                el = OxmlElement('w:%s' % edge)
                tcBorders.append(el)
            for k, v in spec.items():
                el.set(qn('w:%s' % k), str(v))


def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tcPr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_cell_margins(cell, top=40, left=80, bottom=40, right=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.find(qn('w:tcMar'))
    if tcMar is None:
        tcMar = OxmlElement('w:tcMar')
        tcPr.append(tcMar)
    for edge, val in (('top', top), ('left', left), ('bottom', bottom), ('right', right)):
        el = tcMar.find(qn('w:%s' % edge))
        if el is None:
            el = OxmlElement('w:%s' % edge)
            tcMar.append(el)
        el.set(qn('w:w'), str(val))
        el.set(qn('w:type'), 'dxa')


def set_cell_width(cell, dxa):
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn('w:tcW'))
    if tcW is None:
        tcW = OxmlElement('w:tcW')
        tcPr.append(tcW)
    tcW.set(qn('w:w'), str(dxa))
    tcW.set(qn('w:type'), 'dxa')


def set_row_height(row, dxa, rule='atLeast'):
    trPr = row._tr.get_or_add_trPr()
    trHeight = trPr.find(qn('w:trHeight'))
    if trHeight is None:
        trHeight = OxmlElement('w:trHeight')
        trPr.append(trHeight)
    trHeight.set(qn('w:val'), str(dxa))
    trHeight.set(qn('w:hRule'), rule)


def set_table_borders(table, val='single', sz=8, color=INK_HEX):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = tblPr.find(qn('w:tblBorders'))
    if borders is None:
        borders = OxmlElement('w:tblBorders')
        tblPr.append(borders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = borders.find(qn('w:%s' % edge))
        if el is None:
            el = OxmlElement('w:%s' % edge)
            borders.append(el)
        el.set(qn('w:val'), val)
        el.set(qn('w:sz'), str(sz))
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), color)


def no_table_borders(table):
    set_table_borders(table, val='none', sz=0, color='FFFFFF')


def add_paragraph_bottom_border(paragraph, sz=8, val='single', color=INK_HEX):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is None:
        pBdr = OxmlElement('w:pBdr')
        pPr.append(pBdr)
    bottom = pBdr.find(qn('w:bottom'))
    if bottom is None:
        bottom = OxmlElement('w:bottom')
        pBdr.append(bottom)
    bottom.set(qn('w:val'), val)
    bottom.set(qn('w:sz'), str(sz))
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), color)


def add_writing_line(container, count=1, space_after=18, indent=0, line_color=INK_HEX):
    """Add `count` writing-line paragraphs (bottom-border) into a cell or document body."""
    for _ in range(count):
        if hasattr(container, 'add_paragraph'):
            p = container.add_paragraph()
        else:
            p = container.add_paragraph() if False else None
        # normalize: container is a cell or document
        p = _add_para(container)
        pPr = p._p.get_or_add_pPr()
        if indent:
            pPr.set(qn('w:ind'), str(int(indent * 20)))
        spacing = pPr.find(qn('w:spacing'))
        if spacing is None:
            spacing = OxmlElement('w:spacing')
            pPr.append(spacing)
        spacing.set(qn('w:after'), str(space_after))
        spacing.set(qn('w:line'), '360')  # ~ 1.15 line
        add_paragraph_bottom_border(p, sz=8, val='single', color=line_color)
    return p


def _add_para(container):
    if hasattr(container, 'add_paragraph'):
        return container.add_paragraph()
    return container.add_paragraph()


def para(container, text="", size=12, bold=False, italic=False, color=INK, font=BODY_FONT,
         align=None, space_before=0, space_after=6, line=None, caps=False):
    p = container.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before * 20)))
    spacing.set(qn('w:after'), str(int(space_after * 20)))
    if line:
        spacing.set(qn('w:line'), str(int(line * 240)))
        spacing.set(qn('w:lineRule'), 'auto')
    pPr.append(spacing)
    if align is not None:
        p.alignment = align
    if text:
        set_run(p.add_run(text), size=size, bold=bold, italic=italic, color=color, font=font, caps=caps)
    return p


def cell_para(cell, text="", size=12, bold=False, italic=False, color=INK, font=BODY_FONT,
              align=None, space_before=0, space_after=4, line=None, caps=False):
    p = cell.paragraphs[0] if (len(cell.paragraphs) == 1 and not cell.paragraphs[0].text) else cell.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(space_before * 20)))
    spacing.set(qn('w:after'), str(int(space_after * 20)))
    if line:
        spacing.set(qn('w:line'), str(int(line * 240)))
        spacing.set(qn('w:lineRule'), 'auto')
    pPr.append(spacing)
    if align is not None:
        p.alignment = align
    if text:
        set_run(p.add_run(text), size=size, bold=bold, italic=italic, color=color, font=font, caps=caps)
    return p


def vcenter(cell):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def set_page(doc, width_in=8.5, height_in=11.0, left=0.75, right=0.75, top=1.0, bottom=1.0):
    sec = doc.sections[0]
    sec.page_width = Inches(width_in)
    sec.page_height = Inches(height_in)
    sec.left_margin = Inches(left)
    sec.right_margin = Inches(right)
    sec.top_margin = Inches(top)
    sec.bottom_margin = Inches(bottom)
    return sec
