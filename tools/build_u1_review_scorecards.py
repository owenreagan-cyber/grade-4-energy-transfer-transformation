"""Phase 13Z — Unit 1 review-game printable: squad scorecard + Team Explain/Challenge cards.

Replaces the old CER/Action-Stunt cards with clean "Team Explain" ($500) and
"Team Challenge" ($300) cards. All off-scope terms removed (no kinetic/potential/
mechanical/chemical/thermal/radiant/momentum/force/impulse/deformation/proves/CER).
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
    "production", "review", "unit-01"))
os.makedirs(OUT_DIR, exist_ok=True)

WHITE = RGBColor(0xFF, 0xFF, 0xFF)

CATS = [
    ("Case 1", "Energy Causes Change"),
    ("Case 2", "Speed & Energy of Motion"),
    ("Case 3", "Transfer or Transformation"),
    ("Case 4", "Collisions"),
    ("Case 5", "Engineering & Edison/Latimer"),
]

def save(doc, fn):
    doc.save(os.path.join(OUT_DIR, fn))
    print("saved", fn)

# ---------------------------------------------------------------- scorecard
def build_scorecard():
    doc = new_doc()

    # title
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run("ENERGY DETECTIVE: CRACK THE VAULT!"), size=22, bold=True, color=NAVY, font=HEAD_FONT)
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p2.add_run("Squad Scorecard & Combination Tracker · Unit 1 Review Game"), size=12, italic=True, color=GRAY)

    # squad name / detectives
    n = doc.add_paragraph()
    set_run(n.add_run("Detective Squad Name: "), size=12, bold=True, color=INK)
    r = n.add_run("____________________________________"); r.underline = True; set_run(r, size=12, color=INK)
    set_run(n.add_run("      Detectives: "), size=12, bold=True, color=INK)
    r2 = n.add_run("______________________________"); r2.underline = True; set_run(r2, size=12, color=INK)
    sp = doc.add_paragraph(); spPr = sp._p.get_or_add_pPr()
    e = OxmlElement('w:spacing'); e.set(qn('w:after'), '120'); spPr.append(e)

    # --- grid ---
    headers = ["Category", "$100", "$200", "$300", "$400", "$500", "Digit Unlocked"]
    col_w = [2400, 1000, 1000, 1300, 1000, 1300, 2080]
    t = doc.add_table(rows=1 + len(CATS), cols=len(headers))
    no_table_borders(t)

    # header row
    for j, h in enumerate(headers):
        hc = t.cell(0, j)
        set_cell_width(hc, col_w[j])
        set_cell_margins(hc, top=50, left=30, bottom=50, right=30)
        shade_cell(hc, NAVY_HEX)
        hp = hc.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(hp.add_run(h), size=11, bold=True, color=WHITE, caps=True)
    set_row_height(t.rows[0], 440, rule='exact')

    # body rows
    for i, (tag, cat) in enumerate(CATS):
        cells = t.cell(i + 1, 0)
        set_cell_width(cells, col_w[0])
        set_cell_margins(cells, top=60, left=60, bottom=60, right=60)
        cp = cells.paragraphs[0]
        set_run(cp.add_run(tag + "  "), size=11, bold=True, color=CORAL)
        set_run(cp.add_run(cat), size=12, bold=True, color=NAVY)
        # value checkboxes
        for j in range(1, 6):
            vc = t.cell(i + 1, j)
            set_cell_width(vc, col_w[j])
            set_cell_margins(vc, top=60, left=30, bottom=60, right=30)
            vp = vc.paragraphs[0]; vp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_run(vp.add_run("\u25A1"), size=16, color=INK)
        # digit
        dc = t.cell(i + 1, 6)
        set_cell_width(dc, col_w[6])
        set_cell_margins(dc, top=60, left=40, bottom=60, right=40)
        dp = dc.paragraphs[0]; dp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(dp.add_run("Digit #%d: " % (i + 1)), size=11, bold=True, color=GRAY)
        rr = dp.add_run("___"); rr.underline = True; set_run(rr, size=12, color=INK)
        set_row_height(t.rows[i + 1], 760, rule='atLeast')

    # legend
    lg = doc.add_paragraph()
    spPr = lg._p.get_or_add_pPr()
    e = OxmlElement('w:spacing'); e.set(qn('w:before'), '120'); e.set(qn('w:after'), '60'); spPr.append(e)
    set_run(lg.add_run("$300 = Team Challenge · $500 = Team Explain · Each correct clue earns the points AND unlocks that case's digit."), size=11, italic=True, color=GRAY)

    # --- vault ---
    heading(doc, "MASTER VAULT COMBINATION", 14, before=60)
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
        set_run(cp.add_run("Digit %d" % (k + 1)), size=10, bold=True, color=GRAY)
        cp2 = c.add_paragraph(); cp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(cp2.add_run("____"), size=16, bold=True, color=NAVY)
    set_row_height(v.rows[0], 900, rule='exact')

    # total score
    ts = doc.add_paragraph()
    spPr = ts._p.get_or_add_pPr()
    e = OxmlElement('w:spacing'); e.set(qn('w:before'), '120'); spPr.append(e)
    set_run(ts.add_run("TOTAL SCORE: "), size=14, bold=True, color=NAVY)
    rr = ts.add_run("______________ pts"); rr.underline = True; set_run(rr, size=14, color=INK)

    save(doc, "unit1-review-game-scorecards.docx")

# ---------------------------------------------------------------- cards
def card(doc, tag, cat, kind, prompt, expected):
    """kind: 'TEAM EXPLAIN' or 'TEAM CHALLENGE'"""
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
    # Page header (teacher-facing)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run("TEACHER CARDS · Unit 1 Review Game"), size=16, bold=True, color=NAVY, font=HEAD_FONT)
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p2.add_run("Cut these out. Team Explain ($500) = short spoken answer · Team Challenge ($300) = 30-second demo."), size=11, italic=True, color=GRAY)

    heading(doc, "TEAM EXPLAIN CARDS  ($500 clues)", 14, before=40)
    body(doc, "Teams discuss, then explain in one or two spoken sentences. No long writing.", size=11, color=GRAY, after=50)

    card(doc, "Case 1", "Energy Causes Change", "TEAM EXPLAIN",
         "A battery, a stretched rubber band, and a raised ball are not moving. Explain how they can still have energy.",
         "They have stored energy that can cause a change later.")
    card(doc, "Case 2", "Speed & Energy of Motion", "TEAM EXPLAIN",
         "The same marble moved the cup farther from a higher ramp. Explain what this shows about speed and energy of motion.",
         "The faster marble had more energy of motion (a greater change).")
    card(doc, "Case 3", "Transfer or Transformation", "TEAM EXPLAIN",
         "A flashlight lights a card across the room. Explain whether energy transferred, transformed, or both.",
         "Both — stored energy changes into light (transformation), and the light moves to the card (transfer).")
    card(doc, "Case 4", "Collisions", "TEAM EXPLAIN",
         "A rolling car stops when it hits a target, and the target moves. Explain where the energy went.",
         "It transferred to the target (and some became sound). It did not disappear.")
    card(doc, "Case 5", "Engineering & Edison/Latimer", "TEAM EXPLAIN",
         "Edison's first filaments burned out fast. Explain why testing more than 6,000 materials was useful.",
         "Each test was evidence that helped him improve the design.")

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.page_break_before = True
    set_run(p.add_run("TEAM CHALLENGE CARDS  ($300 clues)"), size=16, bold=True, color=NAVY, font=HEAD_FONT)
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p2.add_run("30-second team demos. Act it out, then explain in one sentence."), size=11, italic=True, color=GRAY)

    card(doc, "Case 1", "Energy Causes Change", "TEAM CHALLENGE",
         "Stored Energy Freeze — freeze and show three examples of stored energy (a held book, a stretched rubber band, a battery).",
         "Each object is ready to cause a change later.")
    card(doc, "Case 2", "Speed & Energy of Motion", "TEAM CHALLENGE",
         "Human Ramp — use your arms to model a low ramp and a high ramp. Show how ramp height changes speed and impact distance.",
         "A higher ramp means faster motion and a bigger change.")
    card(doc, "Case 3", "Transfer or Transformation", "TEAM CHALLENGE",
         "Sound Transfer — model how sound moves energy across space without touching anything (vibrate to move a paper strip).",
         "The paper moving shows energy was transferred.")
    card(doc, "Case 4", "Collisions", "TEAM CHALLENGE",
         "Collision Acting — act out a fast collision. Show motion transfer and sound.",
         "The moving object's energy transfers, and some becomes sound.")
    card(doc, "Case 5", "Engineering & Edison/Latimer", "TEAM CHALLENGE",
         "Design Cycle Freeze — act out the design cycle: Problem → Design → Build → Test → Improve.",
         "Test results, even failures, are evidence to improve.")

    save(doc, "unit1-review-game-cards.docx")

if __name__ == "__main__":
    build_scorecard()
    build_cards()
    print("DONE")
