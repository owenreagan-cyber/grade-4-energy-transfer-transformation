"""Unit 1 Teacher Playbook — editable master builder (Phase 2 foundation).

Consumes the FROZEN Unit 1 Visual System tokens (assets/visual-system/design-tokens.json).
Produces: production/teacher-playbook/unit1-teacher-playbook.docx (editable master).

Run: .venv/bin/python tools/build_teacher_playbook.py
Then: soffice --headless --convert-to pdf (see TOOLCHAIN.md)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------------------------------------------------------- frozen tokens
INK      = RGBColor(0x1A, 0x1D, 0x26)   # dark-navy unit identity
INK_SOFT = RGBColor(0x4A, 0x52, 0x68)
PAPER    = RGBColor(0xFF, 0xFF, 0xFF)
MIST     = RGBColor(0xF6, 0xF7, 0xF9)
RULE     = RGBColor(0xD8, 0xDC, 0xE4)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

INK_HEX, INK_SOFT_HEX, MIST_HEX, RULE_HEX = "#1A1D26", "#4A5268", "#F6F7F9", "#D8DCE4"

CHAPTERS = {
    1: dict(title="Energy Causes Change",
            primary="#1F2A5A", accent="#A67C16", surface="#F5EEDC",
            bq=["Where can we observe evidence of energy causing change?",
                "What are some forms of energy?"],
            reader="1–6", pdf="7–12", tg="L1 · L2",
            demo="Electric Pencil Sharpener", vocab=["energy", "change", "stored energy"]),
    2: dict(title="Moving Objects Have Energy",
            primary="#0F5A5C", accent="#0E8A97", surface="#FFFFFF",
            bq=["How are energy, change, and movement of objects related?"],
            reader="7–12", pdf="13–18", tg="L3",
            demo="Marble Collision", vocab=["motion", "energy of motion"]),
    3: dict(title="Energy and Speed Are Related",
            primary="#1B4FC2", accent="#5E8A18", surface="#E9EBEF",
            bq=["How are energy and speed related?"],
            reader="13–16", pdf="19–22", tg="L4 · L5",
            demo="Ramp + Target Preview", vocab=["speed"]),
    4: dict(title="Energy Transfer",
            primary="#6A3FB5", accent="#0E93A6", surface="#EFEDF6",
            bq=["What evidence shows that energy transfers from place to place?"],
            reader="17–24", pdf="23–30", tg="L6 · L7 · L8 · L9",
            demo="Balloon Drum / salt (sound)", vocab=["energy transfer"]),
    5: dict(title="Collisions Transfer Energy",
            primary="#A62626", accent="#C25A1E", surface="#F7EFE2",
            bq=["How is energy involved in collisions?",
                "What happens when objects collide? How are collisions predictable?"],
            reader="25–30", pdf="31–36", tg="L10 · L11",
            demo="Toy-Car Collision", vocab=["collide", "collision", "sound"]),
    6: dict(title="How Can Energy Transformations Solve Problems?",
            primary="#1F5C3D", accent="#8F6D24", surface="#F4F5F3",
            bq=["How do energy transformations help people?",
                "How can I design a device that transforms energy to solve a problem?"],
            reader="31–36", pdf="37–42", tg="L12 · L13",
            demo="Wind-Up Timer", vocab=["convert", "conversion", "energy transformation", "engineering design"]),
    7: dict(title="Solving Problems and Designing Solutions: Thomas A. Edison",
            primary="#3E2C1F", accent="#A06E16", surface="#EFE3CE",
            bq=["How did Thomas Edison use his knowledge of energy transfer and transformation to solve problems?",
                "What have I learned about energy?"],
            reader="37–42", pdf="43–48", tg="Unit Review",
            demo="Flashlight", vocab=["(synthesis — no new Core Vocabulary)"]),
}

BODY_FONT = "Avenir Next"
FULL_W = Inches(7.0)

def C(h):
    return RGBColor.from_string(h.lstrip('#'))

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
        e = OxmlElement(f'w:{tag}'); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa'); m.append(e)
    tcPr.append(m)

def _border(cell, **edges):
    tcPr = cell._tc.get_or_add_tcPr()
    tb = OxmlElement('w:tcBorders')
    for edge, spec in edges.items():
        e = OxmlElement(f'w:{edge}')
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
        e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'), 'none'); borders.append(e)
    tblPr.append(borders)

def _set_width(table, widths):
    table.autofit = False
    for row in table.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = w

def _vcenter(cell):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def _run(p, text, size=11, bold=False, italic=False, color=INK, caps=False, font=BODY_FONT):
    r = p.add_run(text.upper() if caps else text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.color.rgb = color; r.font.name = font
    r.font.caps = caps
    return r

def _para(doc, text="", size=11, bold=False, italic=False, color=INK, before=0, after=60, caps=False, align=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    if text:
        _run(p, text, size=size, bold=bold, italic=italic, color=color, caps=caps)
    return p

def _page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def _add_footer(doc):
    footer = doc.sections[0].footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement('w:pBdr'); top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single'); top.set(qn('w:sz'), '6'); top.set(qn('w:color'), RULE_HEX)
    b.append(top); pPr.append(b)
    _run(p, "Unit 1 Teacher Playbook  ·  Grade 4 Energy Transfer & Transformation  ·  Page ", size=9, color=INK_SOFT)
    run = p.add_run()
    fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = 'PAGE'
    fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1); run._r.append(instr); run._r.append(fld2)
    run.font.size = Pt(9); run.font.color.rgb = INK_SOFT; run.font.name = BODY_FONT

# ---------------------------------------------------------------- components
def title_band(doc, text, sub=None, color_hex=INK_HEX, size=15):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t)
    c = t.cell(0, 0)
    c.width = FULL_W
    _margins(c, top=70, left=110, bottom=70, right=110)
    _shade(c, color_hex)
    _vcenter(c)
    p = c.paragraphs[0]
    _run(p, text, size=size, bold=True, color=WHITE)
    if sub:
        p2 = c.add_paragraph()
        _run(p2, sub, size=9.5, italic=True, color=RGBColor(0xD8, 0xDC, 0xE4))
    return t

def section_heading(doc, text, color=INK, size=14):
    p = _para(doc, text, size=size, bold=True, color=color, before=120, after=30, caps=True)
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement('w:pBdr'); btm = OxmlElement('w:bottom')
    btm.set(qn('w:val'), 'single'); btm.set(qn('w:sz'), '10'); btm.set(qn('w:color'), INK_HEX)
    b.append(btm); pPr.append(b)
    return p

def sub_heading(doc, text, size=11.5):
    return _para(doc, text, size=size, bold=True, color=INK, before=60, after=20)

def callout(doc, tag, text, accent_hex=INK_HEX, fill_hex=MIST_HEX, size=10.5):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t)
    c = t.cell(0, 0)
    c.width = FULL_W
    _margins(c, top=60, left=110, bottom=60, right=110)
    _shade(c, fill_hex)
    _border(c, left=dict(sz=18, color=accent_hex))
    p = c.paragraphs[0]
    _run(p, tag + "   ", size=size, bold=True, color=C(accent_hex), caps=True)
    _run(p, text, size=size, color=INK)
    return t

def chapter_tab(doc, n, title, primary_hex):
    t = doc.add_table(rows=1, cols=1)
    _no_borders(t)
    c = t.cell(0, 0)
    c.width = Inches(4.6)
    _margins(c, top=60, left=120, bottom=60, right=120)
    _shade(c, primary_hex)
    _vcenter(c)
    p = c.paragraphs[0]
    _run(p, f"CHAPTER {n} · {title.upper()}", size=11, bold=True, color=WHITE)
    return t

def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true')
    trPr.append(th)

def data_table(doc, headers, rows, widths, size=9.5, header_fill=INK_HEX, first_bold=False, row_h=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    _no_borders(t)
    _set_width(t, widths)
    _repeat_header(t.rows[0])
    for j, h in enumerate(headers):
        hc = t.cell(0, j)
        _margins(hc, top=40, left=60, bottom=40, right=60)
        _shade(hc, header_fill)
        _vcenter(hc)
        _run(hc.paragraphs[0], h, size=size, bold=True, color=WHITE, caps=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i + 1, j)
            _margins(c, top=36, left=60, bottom=36, right=60)
            _vcenter(c)
            p = c.paragraphs[0]
            if j == 0:
                _run(p, str(val), size=size, bold=first_bold, color=INK)
            else:
                _run(p, str(val), size=size, color=INK_SOFT)
            _border(c, bottom=dict(sz=4, color=RULE_HEX))
    return t

# ---------------------------------------------------------------- document setup
def new_doc():
    doc = Document()
    for _p in list(doc.paragraphs):
        _p._p.getparent().remove(_p._p)
    sec = doc.sections[0]
    sec.page_width = Inches(8.5); sec.page_height = Inches(11)
    sec.left_margin = Inches(0.75); sec.right_margin = Inches(0.75)
    sec.top_margin = Inches(0.65); sec.bottom_margin = Inches(0.7)
    # default style font
    st = doc.styles['Normal']
    st.font.name = BODY_FONT; st.font.size = Pt(11); st.font.color.rgb = INK
    return doc

# ================================================================ SECTIONS
def cover(doc):
    _para(doc, "", after=30)
    title_band(doc, "UNIT 1 · TEACHER PLAYBOOK", size=22)
    _para(doc, "", after=20)
    p = _para(doc, "Energy Transfer & Transformation", size=20, bold=True, color=INK, align=WD_ALIGN_PARAGRAPH.CENTER, after=10)
    _para(doc, "Grade 4 · CKSci-aligned · Teacher Edition", size=12, italic=True, color=INK_SOFT, align=WD_ALIGN_PARAGRAPH.CENTER, after=30)

    # resource badge pill
    b = doc.add_table(rows=1, cols=1)
    _no_borders(b); b.alignment = 1
    bc = b.cell(0, 0); bc.width = Inches(2.6)
    _margins(bc, top=40, left=60, bottom=40, right=60); _shade(bc, INK_HEX)
    bp = bc.paragraphs[0]; bp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _run(bp, "TEACHER PLAYBOOK", size=10, bold=True, color=WHITE)

    _para(doc, "", after=30)
    callout(doc, "SCOPE", "Phase 2 foundation. Chapters 2–7 spreads and special sections are PLANNED placeholders pending Phases 3–4. Chapter 1 is fully prototyped. No student curriculum artifact was modified.", accent_hex="#1F2A5A")
    _para(doc, "", after=10)
    callout(doc, "AUTHORITY", "Authoritative curriculum = CKSci Student Reader + Teacher Guide. This playbook documents the final system; it does not drive curriculum decisions.", accent_hex="#1F2A5A")

def unit_at_a_glance(doc):
    section_heading(doc, "Unit at a Glance")
    data_table(doc,
        ["Field", "Detail"],
        [
            ["Unit title", "Energy Transfer & Transformation (Grade 4)"],
            ["Chapters", "1 Energy Causes Change · 2 Moving Objects Have Energy · 3 Energy and Speed Are Related · 4 Energy Transfer · 5 Collisions Transfer Energy · 6 How Can Energy Transformations Solve Problems? · 7 Solving Problems and Designing Solutions: Thomas A. Edison"],
            ["Unit Big Idea", "Energy can be transferred (moved) and transformed (changed in form). Both produce observable changes that are evidence of energy."],
            ["Transfer vs transformation", "Transfer = energy moves (place/object). Transformation = energy changes form. BOTH is valid — never force either/or."],
            ["Major vocabulary", "14 Core Vocabulary terms (see Unit Vocabulary Map): change, energy, stored energy, motion, energy of motion, speed, energy transfer, collide, collision, sound, convert, conversion, energy transformation, engineering design."],
            ["Flagship lab", "Ramp It Up 2.0 (Ch3 · 2-day quantitative investigation)"],
            ["Required build", "Pom-Pom Launcher (end of unit · formative)"],
            ["Assessment", "Unit 1 final = 25 questions / 50 points (matching Q1–8 · multiple choice Q9–25) + separate teacher key."],
            ["Duration", "Weeks 1–4 (16 core blocks, 30-min each) + Friday FLEX"],
            ["Primary student resources", "Guided Notes (primary) · Science Journal (secondary) · practice/application · labs · study guide · review game"],
        ],
        [Inches(1.8), Inches(5.2)], size=9.5, first_bold=True)

def pacing(doc):
    section_heading(doc, "Dated Pacing Calendar — Weeks 1–4")
    _para(doc, "30-minute blocks · M–Th core + Friday FLEX. Slides/notes are PLANNED placeholders until Phases 3–4 land.", size=9.5, italic=True, color=INK_SOFT, after=20)

    weeks = [
        ("WEEK 1 · 10/12–10/16 · Chapters 1–2", [
            ["Mon 10/12", "Ch1 Block 1 — Observe & Name", "1–2", "Key Words · Model It · Draw/Label", "Sharpener DEMO", "exit ticket"],
            ["Tue 10/13", "Ch1 Block 2 — Forms & Stored", "3–5", "Forms · Stored · Evidence table", "Flashlight + salt demos", "exit ticket"],
            ["Wed 10/14", "Ch2 Block 1", "7–9", "Key Words · Model It · Draw/Label", "Marble Collision DEMO", "exit ticket"],
            ["Thu 10/15", "Ch2 Block 2", "10–12", "Before/After · Example/Non-example", "—", "exit ticket"],
            ["Fri 10/16", "FLEX — RECOVER/PRACTICE/EXTEND", "—", "—", "Energy Detectives · Moving Marbles (FLEX)", "not graded"],
        ]),
        ("WEEK 2 · 10/19–10/23 · Chapter 3 + Ramp It Up 2.0", [
            ["Mon 10/19", "Ch3 Block 1", "13–14", "Key Words · Model It", "Ramp + Target Preview DEMO", "exit ticket"],
            ["Tue 10/20", "Ramp It Up 2.0 — Day 1", "13–14", "Data table (lab)", "LAB: calibration · 3 heights × 3 trials · cm", "lab sheet (formative)"],
            ["Wed 10/21", "Ramp It Up 2.0 — Day 2", "13–14", "Graph: Ramp Height vs Avg Cup Displacement", "LAB: averages · graph · Design-Your-Ramp", "lab + graph (formative)"],
            ["Thu 10/22", "Ch3 synthesis", "15–16", "Conclusion · Fair Test", "evidence-based conclusion", "exit ticket"],
            ["Fri 10/23", "FLEX", "—", "—", "Drop It (FLEX) · graph/data practice", "not graded"],
        ]),
        ("WEEK 3 · 10/26–10/30 · Chapters 4–5", [
            ["Mon 10/26", "Ch4 Block 1 — Sound + Light", "17–22", "Key Words · Source→Path→Receiver", "Balloon Drum / salt DEMO", "exit ticket"],
            ["Tue 10/27", "Ch4 Block 2 — Heat + Electricity", "23–24", "Source→Path→Receiver organizer", "Source→Path→Receiver organizer (ACTIVITY)", "organizer (formative)"],
            ["Wed 10/28", "Ch5 Block 1", "25–27", "Key Words · Before/After", "Toy-Car Collision DEMO", "exit ticket"],
            ["Thu 10/29", "Ch5 Block 2", "28–30", "Before/After diagram · Scenarios", "collision scenarios (ACTIVITY)", "application (formative)"],
            ["Fri 10/30", "FLEX", "—", "—", "Newton's cradle demo (teacher) · collision predictor", "not graded"],
        ]),
        ("WEEK 4 · 11/2–11/6 · Chapters 6–7 + Pom-Pom + review + assessment", [
            ["Mon 11/2", "Ch6 Block 1 — Transformations", "31–33", "Key Words · Input→Output model", "Wind-Up Timer DEMO", "exit ticket"],
            ["Tue 11/3", "Ch6 Block 2 — Engineering Design", "34–36", "Engineering cycle · criteria/constraints", "T/T/BOTH sort (ACTIVITY)", "exit ticket"],
            ["Wed 11/4", "Ch7 — Edison / Unit Synthesis", "37–42", "Unit Concept Map", "Flashlight DEMO", "exit ticket"],
            ["Thu 11/5", "Pom-Pom Launcher (REQUIRED BUILD) + review", "—", "—", "build + test/improve · study guide", "build (formative)"],
            ["Fri 11/6", "Review + Unit 1 assessment", "—", "—", "review game · 25Q/50pt written final", "GRADED (25 Q / 50 pts)"],
        ]),
    ]
    for label, rows in weeks:
        sub_heading(doc, label, size=10.5)
        data_table(doc, ["Day", "Chapter / activity", "Reader", "Guided Notes", "Demo / activity", "Collect / grade"],
                   rows, [Inches(0.7), Inches(2.3), Inches(0.5), Inches(1.55), Inches(1.3), Inches(0.65)], size=9, first_bold=True)
        _para(doc, "", after=20)

    callout(doc, "PACING FLAG", "Week 4 compresses Ch6 (2 blocks) + Ch7 (1 block) + Pom-Pom build + review + assessment into 5 days. Feasible only with the compact in-unit engineering cycle (RD-4) and a streamlined review. The 25Q/50pt final is ~30–45 min and may split Thu/Fri. See docs/playbook/UNIT1_PACING_CALENDAR.md.", accent_hex="#A62626", fill_hex="#F7EFE2")

def how_to_use_this_unit(doc):
    section_heading(doc, "How to Use This Unit")
    data_table(doc, ["Element", "What to know"],
        [
            ["Blocks", "30-minute science blocks · M–Th core + Friday FLEX. No essential new core content on Friday."],
            ["Primary artifact", "Guided Notes are PRIMARY · Science Journal is SECONDARY. Design notes first, then slides."],
            ["BQ/V/N mirror", "Slides' Big Question / Vocabulary / Notes anchors mirror the student notes exactly."],
            ["Status vocabulary", "AVAILABLE = exists · PLANNED = scheduled, not built (do NOT treat as a filename) · NOT REQUIRED · OPTIONAL/FLEX."],
            ["Friday FLEX", "RECOVER (catch-up/absent) · PRACTICE (skill) · EXTEND (enrichment). Never blocks Monday."],
            ["Transfer vs transformation", "Transfer = energy moves · transformation = energy changes form · BOTH is valid — never force either/or."],
            ["Same-object rule", "Speed–energy comparisons always use the SAME object at different speeds."],
        ],
        [Inches(1.5), Inches(5.5)], size=9.5, first_bold=True)
    callout(doc, "READ FIRST", "Front matter (At a Glance → Pacing → Resource Map → Grading → Materials → Vocabulary → Demo Map) gives the whole unit. Chapter spreads give the day-by-day. Start with the Pacing Calendar.", accent_hex="#1F2A5A")

def how_slides_notes_work(doc):
    section_heading(doc, "How Slides + Guided Notes Work")
    data_table(doc, ["Rule", "What it means"],
        [
            ["Notes-first", "Guided Notes are designed BEFORE the matching slideshow. Notes are the primary student reference."],
            ["Exact mirror (BQ/V/N)", "Every NOTES-mode slide matches the paper exactly — same section label, wording, bullets, blanks, order, diagram."],
            ["Scope of mirror", "Mirror applies to NOTES-mode slides only. Not every blank needs a cue slide. Hooks/review MCQ are DEMO/DISCUSSION."],
            ["Reveal discipline", "Fill-in answers are revealed, not front-loaded (prediction-before-reveal)."],
            ["Vocabulary TEACH vs RECORD", "TEACH = full-screen card (word + visual + exact source def + Reader page). RECORD = fill-in from memory, card covered."],
            ["9-step choreography", "BIG QUESTION → PHENOMENON → VOCAB CARDS → VOCAB NOTES → READ → CHECKS → CONCEPT NOTES → APPLICATION → RETURN TO BQ"],
            ["Mode badges", "BQ · D (demo) · V (vocab) · R (read) · C (check) · N (notes) · W (write) · T (talk) · P (practice) · J (journal)."],
            ["Notes navigation (permanent)", "BQ / V1 / V2 / N1 / N2 / N3 / N4 — distinct from temporary HUD action bubbles."],
        ],
        [Inches(1.6), Inches(5.4)], size=9.5, first_bold=True)
    callout(doc, "STATUS", "Chapter 1 Guided Notes are FINAL (AVAILABLE). Chapters 2–7 notes and all slide decks are being rebuilt in Phases 3–4 (add per-section Reader page refs, chapter badge, full-screen vocab cards, canonical slide sequence). Chapter 1 spread references are real; Chapters 2–7 spread references remain PLANNED placeholders until then.", accent_hex="#1F2A5A")

def resource_map(doc):
    section_heading(doc, "Resource Map")
    data_table(doc, ["Resource", "Audience", "Required", "Graded", "Status", "Teacher key"],
        [
            ["Guided Notes (Ch1–7)", "Student", "CORE", "No (formative)", "Ch1 AVAILABLE/FINAL · Ch2–7 PLANNED", "Ch1 AVAILABLE · Ch2–7 PLANNED"],
            ["Science Journal prompts", "Student", "CORE", "No", "AVAILABLE", "—"],
            ["Chapter practice/application", "Student", "CORE", "No (practice)", "AVAILABLE", "AVAILABLE"],
            ["Ramp It Up 2.0", "Student (lab)", "CORE", "Formative", "ADAPT — PLANNED", "PLANNED"],
            ["Pom-Pom Launcher", "Student (build)", "REQUIRED BUILD", "Formative", "PLANNED (net-new)", "PLANNED"],
            ["Study guide", "Student", "CORE", "No (practice)", "AVAILABLE", "AVAILABLE"],
            ["Review game", "Student", "CORE", "No", "AVAILABLE", "AVAILABLE"],
            ["Unit 1 test (25Q/50pt)", "Student", "CORE", "GRADED", "AVAILABLE (re-verify)", "AVAILABLE"],
            ["Teacher demos (7)", "Teacher", "CORE", "—", "AVAILABLE (content) / demo guide PLANNED", "—"],
            ["FLEX resources", "Student/Teacher", "OPTIONAL/FLEX", "No", "AVAILABLE", "—"],
            ["Absent recovery", "Student/Teacher", "CORE support", "No", "AVAILABLE", "—"],
            ["Media", "Teacher", "OPTIONAL/FLEX", "—", "PARTIAL (Ch1–2 staged · Ch3–7 scripts)", "—"],
        ],
        [Inches(1.55), Inches(1.05), Inches(0.85), Inches(0.95), Inches(1.85), Inches(0.75)], size=9, first_bold=True)
    _para(doc, "Full matrix with master locations: docs/playbook/UNIT1_RESOURCE_MAP.md", size=9, italic=True, color=INK_SOFT, after=20)

def assessment_grading(doc):
    section_heading(doc, "Assessment & Grading Plan")
    sub_heading(doc, "Unit 1 final (locked)")
    data_table(doc, ["Attribute", "Specification"],
        [
            ["Questions / points", "25 questions · 50 points · 2 points each"],
            ["Q1–8", "Matching (8 terms, 11 definitions, 3 extras)"],
            ["Q9–25", "Multiple choice (4 options each)"],
            ["Excluded", "No short answer · no CER · no fill-in-the-blank"],
            ["Key", "Separate teacher key (never mixed into student pages)"],
            ["Balance (by points)", "Core 26% · data/diagram 30% · application 26% · engineering 18%"],
        ],
        [Inches(1.8), Inches(5.2)], size=9.5, first_bold=True)
    sub_heading(doc, "Routine scoring convention")
    callout(doc, "SCORE", "Score: _____ / [raw max]      ______ %   —  All scored work is reported as raw score + percentage (out of 100).", accent_hex=INK_HEX)
    sub_heading(doc, "Weighing")
    _para(doc, "Teacher grading-weight policy: not specified by Unit materials. No assignment weights are invented here.", size=10, italic=True, color=INK_SOFT, after=20)

def materials(doc):
    section_heading(doc, "Master Materials List")
    data_table(doc, ["Category", "Items"],
        [
            ["Reusable classroom", "Plastic ramp (or ruler + books) · toy car · plastic target cup · identical glass marbles · meter stick/ruler · shallow sand tray · thermometer · low-voltage battery circuit (LED/bulb/buzzer/motor) · flashlight · stopwatch/timer"],
            ["Consumables", "Index cards (vocab deck) · masking tape · craft kit (string, bells, cups, cardboard, rubber bands — latex-free) · warm water (heat demo) · sand"],
            ["Chapter demos", "Electric pencil sharpener + pencil (Ch1) · marbles + cup (Ch2) · ramp + marble + cup (Ch3) · cup/balloon/salt + flashlight + warm water + thermometer + AA/AAA circuit (Ch4) · toy car + cup (Ch5) · wind-up timer (Ch6) · flashlight (Ch7)"],
            ["Ramp It Up 2.0", "Standardized track (28×6 in, 1-in rails) · 3 identical books · same marble · lightweight target cup · printed 0–50 cm strip · ruler + tape · role cards (Launcher / Target Manager / Measurer / Recorder)"],
            ["Pom-Pom Launcher", "Craft kit: cardboard tube, rubber bands (latex-free option), pom-poms, tape · safety note: pieces to adult if band breaks"],
            ["Optional / FLEX", "Newton's cradle (teacher demo only) · solar cell (optional) · Energy Detectives scavenger hunt items · Drop It supplies"],
        ],
        [Inches(1.5), Inches(5.5)], size=9, first_bold=True)
    _para(doc, "No specialty equipment invented beyond the locked demo/build requirements. Quantities scale by group count (class size is an open question).", size=9, italic=True, color=INK_SOFT, after=20)

def vocab_map(doc):
    section_heading(doc, "Unit Vocabulary Map (14 Core Vocabulary)")
    rows = [
        ["change", "1", "1", "Ch1", "Notes fill-in (Key Words)", "Eligible (matching/MC)", "—"],
        ["energy", "1", "1", "Ch1", "Notes fill-in (Key Words)", "Eligible (matching/MC)", "\u201cEnergy is a visible substance\u201d"],
        ["stored energy", "1", "4", "Ch1", "Notes fill-in (Key Words)", "Eligible (matching/MC)", "\u201cStored means moving now\u201d / \u201conly moving objects have energy\u201d"],
        ["motion", "2", "7", "Ch2", "Notes fill-in", "Eligible (matching/MC)", "motion (process) ≠ energy of motion (possession)"],
        ["energy of motion", "2", "9", "Ch2", "Notes fill-in", "Eligible (matching/MC)", "\u201cfaster always = more energy\u201d (must be SAME object)"],
        ["speed", "3", "13", "Ch3", "Notes fill-in", "Eligible (matching/MC)", "\u201cramp height = speed\u201d (speed is inferred)"],
        ["energy transfer", "4", "17", "Ch4", "Notes fill-in", "Eligible (matching/MC)", "\u201ctransfer = transformation\u201d · \u201cenergy disappears\u201d"],
        ["collide", "5", "25", "Ch5", "Notes fill-in", "Eligible (matching/MC)", "\u201cenergy disappears after collision\u201d"],
        ["collision", "5", "25", "Ch5", "Notes fill-in", "Eligible (matching/MC)", "same as collide"],
        ["sound", "5", "28", "Ch5 (L10)", "Notes fill-in", "Eligible (matching/MC)", "\u201csound is matter moving\u201d"],
        ["convert", "6", "32", "Ch6", "Notes fill-in", "Eligible (matching/MC)", "transfer vs transformation"],
        ["conversion", "6", "32", "Ch6", "Notes fill-in", "Eligible (matching/MC)", "transfer vs transformation"],
        ["energy transformation", "6", "32", "Ch6", "Notes fill-in", "Eligible (matching/MC)", "transfer vs transformation"],
        ["engineering design", "6", "36", "Ch6", "Notes fill-in", "Eligible (matching/MC)", "\u201cbiggest/loudest = best\u201d"],
    ]
    data_table(doc, ["Term", "Ch", "Reader p.", "V-group", "Notes status", "Assessment eligibility", "Common misconception"],
               rows, [Inches(1.25), Inches(0.4), Inches(0.7), Inches(0.85), Inches(1.35), Inches(1.25), Inches(1.2)], size=9, first_bold=True)
    callout(doc, "NOT REQUIRED", "Kinetic · potential · gravitational potential · mechanical · radiant · momentum · inertia · compression wave are NOT introduced as required (TG explicitly avoids them).", accent_hex="#A62626", fill_hex="#F7EFE2")

def demo_map(doc):
    section_heading(doc, "Demo / Activity / Lab / Build Map")
    data_table(doc, ["Chapter", "Experience", "Category"],
        [
            ["Ch1", "Electric Pencil Sharpener", "DEMO"],
            ["Ch2", "Marble Collision", "DEMO"],
            ["Ch3", "Ramp + Target Preview", "DEMO"],
            ["Ch3", "Ramp It Up 2.0 (Day 1 + Day 2)", "LAB / INVESTIGATION"],
            ["Ch4", "Balloon Drum / salt (sound transfer)", "DEMO"],
            ["Ch4", "Source → Path → Receiver → Evidence", "ACTIVITY"],
            ["Ch5", "Toy-Car Collision", "DEMO"],
            ["Ch5", "Collision application / before-after models", "ACTIVITY"],
            ["Ch6", "Wind-Up Timer", "DEMO"],
            ["Ch6", "Transfer / Transformation / Both sort", "ACTIVITY"],
            ["Ch7", "Flashlight", "DEMO"],
            ["End of unit", "Pom-Pom Launcher", "REQUIRED BUILD"],
            ["Post-assessment", "Open-ended engineering challenge", "POST-TEST STEM"],
            ["—", "Energy Detectives · Moving Marbles · Drop It", "OPTIONAL / FLEX"],
        ],
        [Inches(1.2), Inches(3.9), Inches(1.9)], size=9, first_bold=True)

def spread_template(doc):
    section_heading(doc, "Chapter Teacher Spread — Template (blank)")
    _para(doc, "Reusable two-page spread. LEFT = Teach It · RIGHT = Teacher Support. Populate in place; do not overfill.", size=9.5, italic=True, color=INK_SOFT, after=16)
    # LEFT
    title_band(doc, "LEFT PAGE — TEACH IT", color_hex=INK_SOFT_HEX, size=12)
    for label in ["Chapter number / title", "Big Question", "Reader pages", "Approximate instructional time",
                  "Student resources", "Vocabulary / V-groups", "N-anchor map", "Lesson blocks / sequence",
                  "What to project", "What students do"]:
        p = _para(doc, "", size=10, after=22)
        _run(p, label + ":  ", size=10, bold=True)
        r = p.add_run("________________________________")
        r.font.size = Pt(10); r.font.color.rgb = RULE
    _page_break(doc)
    # RIGHT
    title_band(doc, "RIGHT PAGE — TEACHER SUPPORT", color_hex=INK_SOFT_HEX, size=12)
    for label in ["Demo / activity", "Materials", "Setup", "Teacher moves", "Ask", "Listen For",
                  "Misconception / corrective move", "Do-not-overteach", "If short on time",
                  "Collect / grade", "Absent / makeup", "What comes next"]:
        p = _para(doc, "", size=10, after=22)
        _run(p, label + ":  ", size=10, bold=True)
        r = p.add_run("________________________________")
        r.font.size = Pt(10); r.font.color.rgb = RULE

def chapter1_spread(doc):
    c = CHAPTERS[1]
    section_heading(doc, "Chapter 1 — Teacher Spread (prototype)", color=C(c["primary"]))
    chapter_tab(doc, 1, c["title"], c["primary"])
    _para(doc, "", after=10)

    # LEFT — TEACH IT
    title_band(doc, "LEFT PAGE — TEACH IT", color_hex=c["primary"], size=12)
    data_table(doc, ["Field", "Content"],
        [
            ["Big Question", "Where can we observe evidence of energy causing change? (TG Lesson 2 adds \u201cWhat are some forms of energy?\u201d \u2192 addressed by N2 on the notes)"],
            ["Reader pages", "Printed 1–6 · PDF 7–12 (core instruction pp. 1–5; p. 6 = forward preview \u201cEnergy Can Move and Change\u201d)"],
            ["Approximate time", "Two 30-min blocks (Block 1 \u201cObserve & Name\u201d · Block 2 \u201cForms & Stored\u201d)"],
            ["Student resources", "Guided Notes — AVAILABLE/FINAL (01-ch1-energy-causes-change-guided-notes, 3 pp) · practice — AVAILABLE · Energy Detectives (FLEX) — AVAILABLE"],
            ["Vocabulary / V-groups", "V1: energy · change (Reader p. 1) · V2: stored energy (Reader p. 4). evidence + position = Language of Instruction (no Reader page) → concept blanks in N1/N3."],
            ["N-anchor map", "N1 Energy Causes Change (ENERGY→CHANGE→EVIDENCE) · N2 Energy Occurs in Different Forms (5-form table) · N3 Objects Can Store Energy (STORED→RELEASE→CHANGE + examples + position) · N4 Recognizing Evidence (BEFORE/AFTER + CHECK YOUR THINKING) · BQ · NOW I THINK"],
            ["Lesson blocks (Block 1)", "BQ → sharpener DEMO → discuss change → vocab cards (energy, change) → read pp. 1–2 → MODEL IT + DRAW/LABEL → exit"],
            ["Lesson blocks (Block 2)", "recall → read p. 3 (forms) → vocab card (stored) → read pp. 4–5 → FORMS + STORED + evidence table → application → return to BQ"],
            ["What to project", "01-ch1-energy-causes-change-slides.pptx — FINAL (45 slides, 16:9) · BQ 2/3/33 · V1 10–12 · V2 20–22 · N1 13–16 · N2 17–19 · N3 23–27 · N4 28–31 · demo 4, 6–9 · review 34–45 · Reader pp. 1–6"],
            ["What students do", "Predict → observe → fill Key Words → complete ENERGY→CHANGE→EVIDENCE model → draw before/after → record evidence → answer Big Question"],
        ],
        [Inches(1.6), Inches(5.4)], size=9, first_bold=True)
    _page_break(doc)

    # RIGHT — TEACHER SUPPORT
    title_band(doc, "RIGHT PAGE — TEACHER SUPPORT", color_hex=c["primary"], size=12)
    data_table(doc, ["Field", "Content"],
        [
            ["Demo / activity", "Electric Pencil Sharpener (live DEMO). Flashlight + cup/balloon/salt as secondary demos."],
            ["Materials", "Electric sharpener + unsharpened pencil · flashlight + D-cell · cup + balloon + salt"],
            ["Setup", "Sharpener on stable surface · balloon drumhead pre-stretched · flashlight checked"],
            ["Teacher moves", "Ask \u201cWhat changed?\u201d before naming energy · record every change · build model on the board"],
            ["Ask", "\u201cWhat changed?\u201d \u201cWhat makes it happen?\u201d \u201cHow is the change evidence of energy?\u201d"],
            ["Listen For", "\u201cpencil got shorter/sharper\u201d \u201cit made noise\u201d — evidence, not \u201cI saw the energy\u201d"],
            ["Misconception / fix", "\u201cOnly moving objects have energy\u201d → pair moving + stored examples. \u201cEnergy is a visible substance\u201d → we see the change, not the energy."],
            ["Do-not-overteach", "Do not introduce transfer/transformation or kinetic/potential. Keep p. 6 as a forward preview only."],
            ["If short on time", "Cut the cup/balloon/salt demo · move Energy Detectives to Friday FLEX."],
            ["Collect / grade", "Exit ticket (formative) · notes completion (not graded). No scored chapter item."],
            ["Absent / makeup", "Absent-student recovery guide — curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md"],
            ["What comes next", "Chapter 2 — Moving Objects Have Energy (marble collision demo)."],
        ],
        [Inches(1.6), Inches(5.4)], size=9, first_bold=True)
    _page_break(doc)

def chapter1_demo_guide(doc):
    c = CHAPTERS[1]
    section_heading(doc, "Chapter 1 Demo Guide — Electric Pencil Sharpener", color=C(c["primary"]))
    callout(doc, "LIVE", "Live demo is preferred. Virtual backup is OPTIONAL / DEFERRED (the previously attempted AI-generated sharpener video failed and must NOT be reused as a dependency).", accent_hex=c["primary"])
    _para(doc, "", after=10)
    data_table(doc, ["Section", "Guidance"],
        [
            ["Materials", "Electric pencil sharpener · unsharpened pencil · optional second (dull) pencil for BEFORE/AFTER side-by-side"],
            ["Set Up", "Sharpener on a stable, visible surface. Have one dull and one sharp pencil ready to compare."],
            ["Do This", "1) Show the dull pencil. 2) Ask students to predict what will change. 3) Sharpen the pencil. 4) Have students name every change (shorter, sharper, noise)."],
            ["Ask", "\u201cWhat changed?\u201d \u201cWhat did you notice with your eyes? with your ears?\u201d \u201cWhat made the change happen?\u201d"],
            ["Listen For", "\u201cThe pencil got shorter and sharper.\u201d \u201cThe sharpener made noise.\u201d Evidence language, not \u201cI saw energy.\u201d"],
            ["Connect", "Each change is evidence of energy. Energy = the ability to cause change (Reader p. 1). Build ENERGY → CHANGE → EVIDENCE on the board."],
            ["Do Not Overteach", "Do not claim the tip warms up as student-observed heat (TG \u201cKnow the Science 1\u201d — optional, teacher-observed only). No \u201cmechanical/electrical energy\u201d required terms."],
            ["If Students Ask", "\u201cWhere does the energy come from?\u201d → \u201cIt comes through the cord/battery \u2014 we\u2019ll learn more about that later.\u201d Keep it a preview."],
            ["If Short on Time", "Skip the side-by-side comparison · use a single sharpen. Fall back to \u201cflip the light switch\u201d as a backup change."],
        ],
        [Inches(1.5), Inches(5.5)], size=9, first_bold=True)

def chapter1_slide_map(doc):
    c = CHAPTERS[1]
    section_heading(doc, "Chapter 1 — Slideshow Map (FINAL)", color=C(c["primary"]))
    callout(doc, "FILE", "production/slides/01-ch1-energy-causes-change-slides.pptx — 45 slides (16:9). Rendered PDF + 45 PNG previews alongside. Speaker notes on every slide (MODE · TIME · ASK · LISTEN FOR · REVEAL · NEXT).", accent_hex=c["primary"])
    _para(doc, "", after=10)
    data_table(doc, ["Anchor", "Slides", "What happens on screen"],
        [
            ["BQ", "2 · 3 · 33", "2 = Big Question banner + TURN & TALK · 3 = My first thinking (write) · 33 = BQ · NOW I THINK (return, write)"],
            ["V1 (energy · change)", "10–12", "10 = two vocab cards · 11 = notes write · 12 = notes reveal (change · different)"],
            ["V2 (stored energy)", "20–22", "20 = one large vocab card · 21 = notes write · 22 = notes reveal (later)"],
            ["N1 Energy Causes Change", "13–16", "13 = definition · 14 = ENERGY → CHANGE → EVIDENCE model · 15 = write · 16 = reveal (cause · change · evidence)"],
            ["N2 Energy Occurs in Different Forms", "17–19", "17 = five forms · 18 = clap check · 19 = 5-row form/example table"],
            ["N3 Objects Can Store Energy", "23–27", "23 = still-battery predict · 24 = position · 25 = STORED → RELEASE → CHANGE model · 26 = write · 27 = reveal (position)"],
            ["N4 Recognizing Evidence", "28–31", "28 = evidence concept · 29 = BEFORE/AFTER draw · 30 = CHECK YOUR THINKING write · 31 = sample + classify"],
            ["Phenomenon / demo", "4 · 6–9", "4 = light-switch change · 6 = observe dull pencil · 7 = predict · 8 = before/after · 9 = change = evidence"],
            ["Application / evidence", "32", "Which change shows energy at work? (choose the change)"],
            ["End-of-chapter review", "34–45", "6 multiple-choice (A/B/C/D) — question state then answer state; letters shuffled A/B/C/D/B/C"],
        ],
        [Inches(1.9), Inches(1.1), Inches(4.0)], size=9, first_bold=True)
    _para(doc, "Reader cues on-slide: V1/N1 pp. 1–2 · N2 p. 3 · V2/N3 pp. 4–5 · N4 pp. 1–6 · BQ p. 1. Timing: two 30-min blocks (Block 1 = slides 1–12 · Block 2 = slides 13–33) + review slides 34–45 as a third short block or Friday FLEX.", size=9, italic=True, color=INK_SOFT, after=8)

def answer_key_architecture(doc):
    section_heading(doc, "Answer-Key Architecture")
    sub_heading(doc, "How keys are built")
    data_table(doc, ["Principle", "Requirement"],
        [
            ["Visual mirror", "Keys mirror student pages exactly — same layout, page numbers, section codes (BQ / V1 / V2 / N1 / N2)."],
            ["Fill directly", "Answers written onto the mirrored page; no separate answer list."],
            ["Accepted/sample responses", "Open items: sample response + range of acceptable alternatives (TEACHER_KEY_STANDARD)."],
            ["Scoring notes", "Only when needed: partial credit, point allocation, what NOT to penalize."],
            ["Separation", "Keys are never mixed into student PDFs; separate teacher file per assessment/quiz/worksheet/lab."],
        ],
        [Inches(1.8), Inches(5.2)], size=9.5, first_bold=True)
    sub_heading(doc, "Key index / status")
    data_table(doc, ["Key", "Resource", "Status"],
        [
            ["Ch1 practice key", "01-ch1-energy-causes-change-practice-key", "AVAILABLE"],
            ["Ch1 quiz key", "01-ch1-energy-causes-change-quiz-key", "AVAILABLE"],
            ["Ch1 guided-notes key", "01-ch1-energy-causes-change-guided-notes-key", "AVAILABLE (FINAL · 3 pp)"],
            ["Ramp It Up 2.0 key", "03-ch3-ramp-it-up (ADAPT)", "PLANNED / NOT YET GENERATED (update existing)"],
            ["Pom-Pom Launcher key", "net-new build", "PLANNED / NOT YET GENERATED"],
            ["Study guide key", "unit1 study guide", "AVAILABLE"],
            ["Review game guide", "unit1 review game", "AVAILABLE"],
            ["Unit 1 final key", "07-unit-final-assessment-key", "AVAILABLE (re-verify after note rebuild)"],
        ],
        [Inches(1.7), Inches(2.9), Inches(2.4)], size=9, first_bold=True)

def special_sections(doc):
    section_heading(doc, "Special Sections — Status (Phase 2)")
    data_table(doc, ["Section", "Status", "Pointer"],
        [
            ["Ramp It Up 2.0 teacher guide", "SKELETON · ADAPT — PLANNED", "production/labs/03-ch3-ramp-it-up-teacher-spec.md"],
            ["Pom-Pom Launcher teacher guide", "SKELETON · PLANNED (net-new)", "net-new (ADAPTED from colleague)"],
            ["Review plan", "SKELETON · points to AVAILABLE assets", "production/review/unit-01/ (study guide + game)"],
            ["Unit 1 assessment administration", "SKELETON · locked 25Q/50pt", "production/quizzes/07-unit-final-assessment.docx"],
            ["Answer-key index", "RENDERED", "see Answer-Key Architecture"],
            ["FLEX / enrichment / catch-up", "SKELETON · points to framework", "docs/planning/FRIDAY_FLEX_FRAMEWORK.md"],
            ["Absent / makeup support", "SKELETON · points to per-chapter recovery", "curriculum/chapter-0N/student/recovery/"],
            ["Media index", "SKELETON · Ch1–2 staged · Ch3–7 scripts-only", "docs/planning/WHOLE_UNIT_MEDIA_STAGING.md"],
        ],
        [Inches(2.0), Inches(2.2), Inches(2.8)], size=9, first_bold=True)

def chapter_placeholders(doc):
    section_heading(doc, "Chapters 2–7 — Spread Placeholders")
    _para(doc, "Each chapter will use the reusable spread template (LEFT Teach It / RIGHT Teacher Support). Populated in later phases.", size=9.5, italic=True, color=INK_SOFT, after=20)
    for n in range(2, 8):
        c = CHAPTERS[n]
        chapter_tab(doc, n, c["title"], c["primary"])
        _para(doc, "", after=4)
        data_table(doc, ["Big Question", "Reader pp.", "Demo", "New Core Vocabulary"],
            [[(" · ".join(c["bq"]))[:200], c["reader"], c["demo"], ", ".join(c["vocab"])]],
            [Inches(2.9), Inches(0.75), Inches(1.55), Inches(1.8)], size=9, first_bold=False)
        _para(doc, "", after=14)

# ================================================================ build
def build():
    doc = new_doc()
    _add_footer(doc)
    cover(doc); _page_break(doc)
    unit_at_a_glance(doc); _page_break(doc)
    pacing(doc); _page_break(doc)
    how_to_use_this_unit(doc); _page_break(doc)
    how_slides_notes_work(doc); _page_break(doc)
    resource_map(doc); _page_break(doc)
    assessment_grading(doc); _page_break(doc)
    materials(doc); _page_break(doc)
    vocab_map(doc); _page_break(doc)
    demo_map(doc); _page_break(doc)
    spread_template(doc); _page_break(doc)
    chapter1_spread(doc)
    chapter1_demo_guide(doc); _page_break(doc)
    chapter1_slide_map(doc); _page_break(doc)
    answer_key_architecture(doc); _page_break(doc)
    special_sections(doc); _page_break(doc)
    chapter_placeholders(doc)

    out_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "production", "teacher-playbook"))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "unit1-teacher-playbook.docx")
    doc.save(out)
    print("saved", out)

if __name__ == "__main__":
    build()
