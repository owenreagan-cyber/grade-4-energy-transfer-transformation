"""Unit 2 written study/review sheet — student + teacher key.

Purpose: Week 8.5 Day 1, before the Unit 2 written assessment. A REVIEW, not a second test.
Covers the assessed scope: renewable vs nonrenewable, abundant != renewable, coal/petroleum/
natural gas, using fossil fuels, nuclear, wind, hydro, solar, geothermal, innovations,
benefits/limitations, energy pathways, resource-location reasoning.
Grade 4 friendly: body 13-15 pt, 12 pt floor, generous spacing.
No banned terms (climate/carbon/policy/fission/base-load/peak demand/grid/battery-only).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "review", "unit-02"))
os.makedirs(OUT_DIR, exist_ok=True)
SUB = "Unit 2 Study & Review · Using Natural Resources for Energy"

def save(doc, fn):
    doc.save(os.path.join(OUT_DIR, fn))
    print("saved", fn)

def wbank(doc, words, size=12):
    body(doc, "Word bank:  " + "    ".join(words), size=size, bold=True, color=NAVY, after=14)

def build_student():
    doc = new_doc()
    title_block(doc, "Using Natural Resources for Energy", SUB + " · Student")
    body(doc, "Use this sheet to get ready for the Unit 2 assessment. Take your time — this is for YOU.", size=12, italic=True, color=GRAY, after=18)

    # --- Section A: Match ---
    heading(doc, "A · Match the Word", 16)
    body(doc, "Draw a line from each word to its meaning.", size=12, color=GRAY, after=10)
    two_col_table(doc, ["Word", "Meaning (draw a line)"],
        [("1. renewable resource", ""), ("2. nonrenewable resource", ""),
         ("3. fossil fuel", ""), ("4. turbine", ""), ("5. generator", ""),
         ("6. solar cell", ""), ("7. geothermal energy", ""), ("8. hydroelectric power", "")],
        col_widths=(3600, FULL_W - 3600), row_h=300)
    body(doc, "Meanings:", size=12, bold=True, after=6)
    meaning_grid(doc, ["A. heat that is transferred from inside Earth",
                       "B. electricity made from moving water, usually through a dam",
                       "C. a machine with blades that spins when steam, wind, or water pushes it",
                       "D. a resource that cannot be restored as quickly as it is used",
                       "E. a device that converts sunlight to electricity",
                       "F. a machine that makes electricity when a turbine spins it",
                       "G. a fuel formed from the remains of organisms that lived long ago",
                       "H. a resource that can be restored as quickly as it is used"])

    # PAGE 2
    page_head(doc, "Sections B–D · Page 2", new_page=True)

    # --- Section B: Sort ---
    heading(doc, "B · Renewable or Nonrenewable?", 16, before=60)
    body(doc, "Write R for renewable or N for nonrenewable.", size=12, color=GRAY, after=10)
    sort_table(doc, [("coal", "wind"), ("petroleum", "natural gas"),
                     ("sunlight", "uranium"), ("flowing water", "geothermal heat")])

    heading(doc, "C · Fill the Pathway", 16, before=60)
    body(doc, "Write the missing steps so the electricity pathway is in order.", size=12, color=GRAY, after=10)
    wbank(doc, ["burn the fuel", "turn a generator", "spin a turbine", "heat water into steam", "electricity"])
    pathway_steps(doc, ["burn the fuel", "", "", "", "electricity"])

    body(doc, "Now write TWO shorter pathways.", size=12, bold=True, color=NAVY, after=6)
    body(doc, "Wind:    moving air  →  ______________  →  generator  →  electricity", size=13, after=6)
    body(doc, "Solar:   sunlight  →  ______________  →  electricity", size=13, after=8)

    heading(doc, "D · Compare", 16, before=60)
    body(doc, "Fill in the blank to finish each idea.", size=12, color=GRAY, after=8)
    fill(doc, "A renewable resource is restored", blank="________________", trail=".", size=13, after=6)
    fill(doc, "A nonrenewable resource is NOT restored", blank="________________", trail=".", size=13, after=6)
    fill(doc, "A resource can be abundant (plentiful) but still", blank="________________", trail=".", size=13, after=6)
    body(doc, "The three fossil fuels are coal, petroleum, and ______________.", size=13, bold=True, after=6)
    body(doc, "Nuclear power uses ______________ as its fuel; its pathway is the SAME as coal.", size=13, after=8)

    # PAGE 3
    page_head(doc, "Sections E–G · Page 3", new_page=True)

    heading(doc, "E · Label It", 16)
    body(doc, "Use the word bank to label the diagram.", size=12, color=GRAY, after=10)
    wbank(doc, ["turbine", "generator", "steam (or water)", "electricity"])
    label_boxes(doc, ["fuel (coal or nuclear)", "", "", ""])

    heading(doc, "F · Scenario", 16)
    body(doc, "A town has strong, steady wind most of the year. It has no large river nearby and many cloudy days.", size=13, bold=True, after=10)
    body(doc, "1. Which resource is most reasonable for this town to investigate? ______________________", size=13, after=8)
    body(doc, "2. Write ONE fact that supports your choice.", size=13, after=4)
    wline(doc, 1, gap=26, after=10)
    body(doc, "3. Write ONE limitation they would still need to consider.", size=13, after=4)
    wline(doc, 1, gap=26, after=12)

    heading(doc, "G · Short Response", 16)
    body(doc, "Pick ONE energy resource you studied. Write one benefit and one limitation, and where it works well.", size=13, bold=True, after=8)
    body(doc, "Resource: ______________________", size=13, after=6)
    body(doc, "Benefit:", size=13, bold=True, after=2)
    wline(doc, 1, gap=26, after=8)
    body(doc, "Limitation:", size=13, bold=True, after=2)
    wline(doc, 1, gap=26, after=8)
    body(doc, "Works well when / where:", size=13, bold=True, after=2)
    wline(doc, 1, gap=26, after=8)

    save(doc, "unit2-written-study-review.docx")

def page_head(doc, label, new_page=True):
    """Compact continuation-page header (no Name/Date block)."""
    p = doc.add_paragraph()
    if new_page:
        p.paragraph_format.page_break_before = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run(label), size=14, bold=True, color=NAVY, font=HEAD_FONT)
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p2.add_run(SUB), size=12, italic=True, color=GRAY)
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '60'); spPr.append(spelm)

def meaning_grid(doc, meanings, size=12):
    """Two-column meanings list (saves vertical space, keeps 12pt floor)."""
    half = (len(meanings) + 1) // 2
    rows = list(zip(meanings[:half], meanings[half:] + [""] * (half - len(meanings[half:]))))
    t = doc.add_table(rows=len(rows), cols=2)
    no_table_borders(t)
    for r, (a, b) in enumerate(rows):
        for c, txt in ((0, a), (1, b)):
            cell = t.cell(r, c)
            set_cell_width(cell, FULL_W // 2)
            set_cell_margins(cell, top=10, left=80, bottom=10, right=80)
            if txt:
                set_run(cell.paragraphs[0].add_run(txt), size=size, color=INK)
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '60'); spPr.append(spelm)

def sort_table(doc, pairs, row_h=300):
    """Compact 4-column sort: Resource | R/N | Resource | R/N (4 rows)."""
    t = doc.add_table(rows=1 + len(pairs), cols=4)
    no_table_borders(t)
    headers = ["Resource", "R or N", "Resource", "R or N"]
    for j, h in enumerate(headers):
        hc = t.cell(0, j)
        set_cell_width(hc, FULL_W // 4)
        set_cell_margins(hc, top=40, left=80, bottom=40, right=80)
        shade_cell(hc, NAVY_HEX)
        set_run(hc.paragraphs[0].add_run(h), size=12, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), caps=True)
    set_row_height(t.rows[0], 380, rule='exact')
    for i, (a, b) in enumerate(pairs):
        vals = [a, "", b, ""]
        for j, val in enumerate(vals):
            c = t.cell(i + 1, j)
            set_cell_width(c, FULL_W // 4)
            set_cell_margins(c, top=40, left=80, bottom=40, right=80)
            cp = c.paragraphs[0]
            if val:
                set_run(cp.add_run(val), size=13, bold=True, color=NAVY)
            add_paragraph_bottom_border(cp, sz=8, val='single', color=INK_HEX)
        set_row_height(t.rows[i + 1], row_h, rule='atLeast')
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '40'); spPr.append(spelm)

def pathway_steps(doc, steps, box_w=1500, size=13):
    """Horizontal 5-step arrow chain; empty string = blank fill box."""
    cols = len(steps) * 2 - 1
    t = doc.add_table(rows=1, cols=cols)
    no_table_borders(t)
    for idx in range(cols):
        mc = t.cell(0, idx)
        if idx % 2 == 0:
            set_cell_width(mc, box_w)
        else:
            set_cell_width(mc, 500)
        set_cell_margins(mc, top=40, left=8, bottom=40, right=8)
        vcenter(mc)
        mp = mc.paragraphs[0]
        mp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if idx % 2 == 0:
            word = steps[idx // 2]
            if word:
                shade_cell(mc, NAVY_HEX)
                set_run(mp.add_run(word), size=size, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
            else:
                set_cell_border(mc, top=dict(sz=8, val='single', color=INK_HEX),
                                left=dict(sz=8, val='single', color=INK_HEX),
                                bottom=dict(sz=8, val='single', color=INK_HEX),
                                right=dict(sz=8, val='single', color=INK_HEX))
        else:
            set_run(mp.add_run("→"), size=size + 2, bold=True, color=CORAL)
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '40'); spPr.append(spelm)

def label_boxes(doc, labels, box_w=1900, size=13):
    """Horizontal 4-box diagram for labeling; empty = blank."""
    cols = len(labels) * 2 - 1
    t = doc.add_table(rows=1, cols=cols)
    no_table_borders(t)
    for idx in range(cols):
        mc = t.cell(0, idx)
        if idx % 2 == 0:
            set_cell_width(mc, box_w)
        else:
            set_cell_width(mc, 500)
        set_cell_margins(mc, top=40, left=8, bottom=40, right=8)
        vcenter(mc)
        mp = mc.paragraphs[0]
        mp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if idx % 2 == 0:
            word = labels[idx // 2]
            if word:
                shade_cell(mc, MID_HEX)
                set_run(mp.add_run(word), size=size, bold=True, color=INK)
            else:
                set_cell_border(mc, top=dict(sz=8, val='single', color=INK_HEX),
                                left=dict(sz=8, val='single', color=INK_HEX),
                                bottom=dict(sz=8, val='single', color=INK_HEX),
                                right=dict(sz=8, val='single', color=INK_HEX))
        else:
            set_run(mp.add_run("→"), size=size + 2, bold=True, color=CORAL)
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '40'); spPr.append(spelm)

def build_key():
    doc = new_doc()
    title_block(doc, "Using Natural Resources for Energy", SUB + " · Teacher Key")
    heading(doc, "A · Match the Word")
    body(doc, "1-H · 2-D · 3-G · 4-C · 5-F · 6-E · 7-A · 8-B", size=13, after=16)
    heading(doc, "B · Renewable or Nonrenewable?")
    body(doc, "coal N · wind R · petroleum N · natural gas N · sunlight R · uranium N · flowing water R · geothermal heat R", size=13, after=16)
    heading(doc, "C · Fill the Pathway")
    body(doc, "burn the fuel → heat water into steam → spin a turbine → turn a generator → electricity", size=13, after=10)
    body(doc, "Wind: moving air → blades (turbine) → generator → electricity.  Solar: sunlight → solar cell → electricity.", size=13, after=16)
    heading(doc, "D · Compare")
    body(doc, "renewable: as quickly as it is used.  nonrenewable: as quickly as it is used (cannot be restored quickly).  abundant but still: nonrenewable.", size=13, after=10)
    body(doc, "Three fossil fuels: coal, petroleum, and natural gas.  Nuclear fuel: uranium.", size=13, after=16)
    heading(doc, "E · Label It")
    body(doc, "fuel (coal or nuclear) → steam (or water) → turbine → generator → electricity. (Boxes: steam/water, turbine, generator, electricity.)", size=13, after=16)
    heading(doc, "F · Scenario")
    body(doc, "1. Wind.  2. Strong, steady wind most of the year.  3. Wind can be calm some days / needs a windy location. (Accept any reasoned choice with one fact + one limitation.)", size=13, after=16)
    heading(doc, "G · Short Response")
    body(doc, "Any resource: one benefit + one limitation + a location/condition where it works well. Examples: wind — benefit: no fuel to burn; limitation: needs wind; works well where it is windy. Solar — benefit: sunlight is renewable; limitation: cloudy days/shade; works well in sunny places.", size=13, after=16)
    save(doc, "unit2-written-study-review-key.docx")

if __name__ == "__main__":
    build_student()
    build_key()
    print("DONE")
