"""Phase 13AA — Unit 2 review-game printable: squad scorecard + Team Explain/Challenge cards.

Same architecture as Unit 1 (Phase 13Z). No vault-combination theme; instead a
"Mystery Town clue" mechanic that feeds the final challenge. No CER wording.
No off-scope terms (fission/U-235/kinetic/mechanical/chemical/thermal/radiant/
electron/photon/semiconductor/baseload/dispatch/grid/peak demand/climate terms).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *
from gn_design import OxmlElement, qn
from ch1_notes_common import (
    NAVY, NAVY_HEX, CORAL, CORAL_HEX, GOLD, GOLD_HEX, INK, INK_HEX, GRAY,
    LIGHT_HEX, MID_HEX, BODY_FONT, HEAD_FONT,
    set_run, shade_cell, set_cell_border, set_cell_margins, set_cell_width,
    set_row_height, no_table_borders, add_paragraph_bottom_border,
)

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "review", "unit-02"))
os.makedirs(OUT_DIR, exist_ok=True)

WHITE = RGBColor(0xFF, 0xFF, 0xFF)

CATS = [
    ("File 1", "Resource Detective"),
    ("File 2", "Fossil Fuels"),
    ("File 3", "Turbines & Generators"),
    ("File 4", "Renewable Power"),
    ("File 5", "Resource Challenge"),
]

def save(doc, fn):
    doc.save(os.path.join(OUT_DIR, fn))
    print("saved", fn)

# ---------------------------------------------------------------- scorecard
def build_scorecard():
    doc = new_doc()

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run("RESOURCE DETECTIVE: SOLVE THE ENERGY SOURCE CASE!"), size=21, bold=True, color=NAVY, font=HEAD_FONT)
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p2.add_run("Squad Scorecard & Clue Tracker · Unit 2 Review Game"), size=12, italic=True, color=GRAY)

    n = doc.add_paragraph()
    set_run(n.add_run("Detective Squad Name: "), size=12, bold=True, color=INK)
    r = n.add_run("____________________________________"); r.underline = True; set_run(r, size=12, color=INK)
    set_run(n.add_run("      Detectives: "), size=12, bold=True, color=INK)
    r2 = n.add_run("______________________________"); r2.underline = True; set_run(r2, size=12, color=INK)
    sp = doc.add_paragraph(); spPr = sp._p.get_or_add_pPr()
    e = OxmlElement('w:spacing'); e.set(qn('w:after'), '120'); spPr.append(e)

    headers = ["Category", "$100", "$200", "$300", "$400", "$500", "Clue Unlocked"]
    col_w = [2400, 1000, 1000, 1300, 1000, 1300, 2080]
    t = doc.add_table(rows=1 + len(CATS), cols=len(headers))
    no_table_borders(t)

    for j, h in enumerate(headers):
        hc = t.cell(0, j)
        set_cell_width(hc, col_w[j])
        set_cell_margins(hc, top=50, left=30, bottom=50, right=30)
        shade_cell(hc, NAVY_HEX)
        hp = hc.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(hp.add_run(h), size=11, bold=True, color=WHITE, caps=True)
    set_row_height(t.rows[0], 440, rule='exact')

    for i, (tag, cat) in enumerate(CATS):
        cells = t.cell(i + 1, 0)
        set_cell_width(cells, col_w[0])
        set_cell_margins(cells, top=60, left=60, bottom=60, right=60)
        cp = cells.paragraphs[0]
        set_run(cp.add_run(tag + "  "), size=11, bold=True, color=CORAL)
        set_run(cp.add_run(cat), size=12, bold=True, color=NAVY)
        for j in range(1, 6):
            vc = t.cell(i + 1, j)
            set_cell_width(vc, col_w[j])
            set_cell_margins(vc, top=60, left=30, bottom=60, right=30)
            vp = vc.paragraphs[0]; vp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_run(vp.add_run("\u25A1"), size=16, color=INK)
        dc = t.cell(i + 1, 6)
        set_cell_width(dc, col_w[6])
        set_cell_margins(dc, top=60, left=40, bottom=60, right=40)
        dp = dc.paragraphs[0]; dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(dp.add_run("Clue #%d: " % (i + 1)), size=11, bold=True, color=GRAY)
        rr = dp.add_run("___"); rr.underline = True; set_run(rr, size=12, color=INK)
        set_row_height(t.rows[i + 1], 760, rule='atLeast')

    lg = doc.add_paragraph()
    spPr = lg._p.get_or_add_pPr()
    e = OxmlElement('w:spacing'); e.set(qn('w:before'), '120'); e.set(qn('w:after'), '60'); spPr.append(e)
    set_run(lg.add_run("$300 = Team Challenge · $500 = Team Explain · Each correct clue earns the points AND unlocks that file's clue."), size=11, italic=True, color=GRAY)

    # --- Mystery Town clues ---
    heading(doc, "THE MYSTERY TOWN — CLUES", 14, before=60)
    body(doc, "Complete a file to earn its clue. Use the clues to win the Final Challenge.", size=11, color=GRAY, after=60)
    v = doc.add_table(rows=1, cols=5)
    no_table_borders(v)
    for k in range(5):
        c = v.cell(0, k)
        set_cell_width(c, FULL_W // 5)
        set_cell_margins(c, top=60, left=40, bottom=60, right=40)
        set_cell_border(c, top=dict(sz=10, val='single', color=NAVY_HEX),
                        left=dict(sz=10, val='single', color=NAVY_HEX),
                        bottom=dict(sz=10, val='single', color=NAVY_HEX),
                        right=dict(sz=10, val='single', color=NAVY_HEX))
        cp = c.paragraphs[0]; cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(cp.add_run("Clue %d" % (k + 1)), size=10, bold=True, color=GRAY)
        cp2 = c.add_paragraph(); cp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(cp2.add_run("____"), size=16, bold=True, color=NAVY)
    set_row_height(v.rows[0], 900, rule='exact')

    ts = doc.add_paragraph()
    spPr = ts._p.get_or_add_pPr()
    e = OxmlElement('w:spacing'); e.set(qn('w:before'), '120'); spPr.append(e)
    set_run(ts.add_run("TOTAL SCORE: "), size=14, bold=True, color=NAVY)
    rr = ts.add_run("______________ pts"); rr.underline = True; set_run(rr, size=14, color=INK)

    save(doc, "unit2-review-game-scorecards.docx")

# ---------------------------------------------------------------- cards
def card(doc, tag, cat, kind, prompt, expected):
    t = doc.add_table(rows=1, cols=1)
    no_table_borders(t)
    c = t.cell(0, 0)
    set_cell_width(c, FULL_W)
    set_cell_margins(c, top=46, left=120, bottom=46, right=120)
    set_cell_border(c, top=dict(sz=10, val='single', color=NAVY_HEX),
                    left=dict(sz=10, val='single', color=NAVY_HEX),
                    bottom=dict(sz=10, val='single', color=NAVY_HEX),
                    right=dict(sz=10, val='single', color=NAVY_HEX))
    shade_cell(c, LIGHT_HEX)
    p = c.paragraphs[0]
    set_run(p.add_run(tag + " · " + cat + "   "), size=12, bold=True, color=CORAL)
    set_run(p.add_run("— " + kind), size=12, bold=True, color=NAVY)
    pp = c.add_paragraph()
    set_run(pp.add_run(prompt), size=12.5, bold=True, color=INK)
    pe = c.add_paragraph()
    set_run(pe.add_run("Expected: "), size=10.5, italic=True, bold=True, color=GRAY)
    set_run(pe.add_run(expected), size=10.5, italic=True, color=GRAY)
    sp = doc.add_paragraph(); spPr = sp._p.get_or_add_pPr()
    e = OxmlElement('w:spacing'); e.set(qn('w:after'), '30'); spPr.append(e)
    return t

def build_cards():
    doc = new_doc()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run("TEACHER CARDS · Unit 2 Review Game"), size=16, bold=True, color=NAVY, font=HEAD_FONT)
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p2.add_run("Cut these out. Team Explain ($500) = short spoken answer · Team Challenge ($300) = 30-second demo."), size=11, italic=True, color=GRAY)

    heading(doc, "TEAM EXPLAIN CARDS  ($500 clues)", 14, before=40)
    body(doc, "Teams discuss, then explain in one or two spoken sentences. No long writing.", size=11, color=GRAY, after=50)

    card(doc, "File 1", "Resource Detective", "TEAM EXPLAIN",
         "Why does it matter how quickly a resource is restored?",
         "A resource is renewable only if it comes back as fast as (or faster than) we use it.")
    card(doc, "File 2", "Fossil Fuels", "TEAM EXPLAIN",
         "How are coal and petroleum alike? How are they different?",
         "Alike: both form from the remains of organisms over millions of years. Different: coal is solid from swamp plants; petroleum is liquid from ocean organisms.")
    card(doc, "File 3", "Turbines & Generators", "TEAM EXPLAIN",
         "What stays the same in a coal plant and a nuclear plant?",
         "Heat boils water into steam → steam spins a turbine → the turbine turns a generator → electricity.")
    card(doc, "File 4", "Renewable Power", "TEAM EXPLAIN",
         "Why is solar power renewable but not always available?",
         "The sun keeps shining (renewable), but solar depends on location, weather, and time of day (cloudy days, nighttime).")
    card(doc, "File 5", "Resource Challenge", "TEAM EXPLAIN",
         "Name ONE renewable resource. Give one benefit AND one limitation, and where it works well.",
         "Example: wind — benefit: no fuel to burn; limitation: needs a windy location; works well where wind blows steadily.")

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.page_break_before = True
    set_run(p.add_run("TEAM CHALLENGE CARDS  ($300 clues)"), size=16, bold=True, color=NAVY, font=HEAD_FONT)
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p2.add_run("30-second team demos. Act it out, then explain in one sentence."), size=11, italic=True, color=GRAY)

    card(doc, "File 1", "Resource Detective", "TEAM CHALLENGE",
         "Sort It Fast — call out a resource (coal, wind, sunlight, petroleum). The team points to RENEWABLE or NONRENEWABLE and says why.",
         "Renewable comes back quickly; nonrenewable does not.")
    card(doc, "File 2", "Fossil Fuels", "TEAM CHALLENGE",
         "Three States — act out the three fossil fuels: solid (coal), liquid (petroleum), and gas (natural gas).",
         "Coal is solid, petroleum is liquid, natural gas is a gas.")
    card(doc, "File 3", "Turbines & Generators", "TEAM CHALLENGE",
         "Spin the Path — spin your arms like a turbine, turn an imaginary generator, and shout \u201CElectricity!\u201D",
         "A spinning turbine turns the generator to make electricity.")
    card(doc, "File 4", "Renewable Power", "TEAM CHALLENGE",
         "Four Sources — act out wind (spin arms), moving water (flow arms), sunlight (spread rays), and Earth's heat (rise from the ground).",
         "Wind, moving water, sunlight, and Earth's heat are all renewable.")
    card(doc, "File 5", "Resource Challenge", "TEAM CHALLENGE",
         "Pick the Best — for a town with steady wind, cloudy days, and no river, act out wind power and explain your choice.",
         "Steady wind makes wind power the most reliable choice there.")

    save(doc, "unit2-review-game-cards.docx")

if __name__ == "__main__":
    build_scorecard()
    build_cards()
    print("DONE")
