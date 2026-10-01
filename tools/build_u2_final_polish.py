#!/usr/bin/env python3
"""Phase 13X.3 — Unit 2 final certification polish.

Builds the FINAL Unit 2 student assessment + teacher key (25 questions / 50 points)
from the Downloads "unit2_final_assessment_*-2.pdf" approved source, preserving the
approved diagrams (extracted from that PDF) and applying only the targeted fixes:

  FIX 1  Q21  "proves" -> "shows"
  FIX 2  terminology drift alignment to final guided notes:
         "Electrical energy"       -> "Electricity"
         "Chemical energy"         -> "Heat energy"
         "Stored chemical energy"  -> "Heat energy"
         "generate electrical energy" -> "generate electricity"
         "electrical battery power"   -> "battery power"

PDF export is done separately via soffice (see __main__ / build steps).
"""
import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DIAG_DIR = os.path.join(ROOT, "assets", "assessment-diagrams")
OUT_DIR = os.path.join(ROOT, "production", "quizzes", "unit-02")
FONT = "Calibri"

STUDENT_PATH = os.path.join(OUT_DIR, "unit-2-written-assessment-student.docx")
KEY_PATH = os.path.join(OUT_DIR, "unit-2-written-assessment-key.docx")

# ---------------------------------------------------------------- helpers
def _set_font(run, size, bold=False, name=FONT):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:ascii'), name)
    rfonts.set(qn('w:hAnsi'), name)


def _para(doc, text=None, size=13.5, bold=False, align=None, space_after=4, space_before=0):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    if text is not None:
        r = p.add_run(text)
        _set_font(r, size, bold)
    return p


def _rich(doc, parts, size=13.5, space_after=4, space_before=0, align=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    for text, bold in parts:
        r = p.add_run(text)
        _set_font(r, size, bold)
    return p


def add_image_centered(doc, path, width_in):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run()
    run.add_picture(path, width=Inches(width_in))
    return p


def set_cell_margins(cell, top=20, bottom=20, left=80, right=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for tag, val in (('top', top), ('bottom', bottom), ('start', left), ('end', right)):
        e = OxmlElement(f'w:{tag}')
        e.set(qn('w:w'), str(val))
        e.set(qn('w:type'), 'dxa')
        mar.append(e)
    tcPr.append(mar)


def _cell_para(cell, text, bold=False, size=13, bold_term=False, bold_letter=False):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    if bold_term:
        num, rest = text.split("____", 1)
        r1 = p.add_run(num)
        _set_font(r1, size, False)
        r2 = p.add_run("____")
        _set_font(r2, size, False)
        r3 = p.add_run(rest)
        _set_font(r3, size, True)
        return
    if bold_letter:
        letter, rest = text.split(".", 1)
        r1 = p.add_run(letter + ".")
        _set_font(r1, size, True)
        r2 = p.add_run(rest)
        _set_font(r2, size, False)
        return
    r = p.add_run(text)
    _set_font(r, size, bold)


# ---------------------------------------------------------------- data
# Matching terms in locked order (Q1–8) with correct definition letter.
U2_TERMS = [
    ("Renewable Resource", "F"),
    ("Nonrenewable Resource", "A"),
    ("Fossil Fuel", "E"),
    ("Petroleum", "C"),
    ("Uranium", "J"),
    ("Turbine", "I"),
    ("Generator", "B"),
    ("Solar Energy", "H"),
]
# (letter, definition, is_distractor)
U2_DEFS = [
    ("A", "A natural resource that cannot be restored as quickly as it is used by humans.", False),
    ("B", "A machine that helps produce electricity when a turbine spins.", False),
    ("C", "A liquid fossil fuel formed deep underground that is refined into gasoline and diesel.", False),
    ("D", "Heat transferred from Earth's interior.", True),
    ("E", "An energy-dense fuel formed from the fossilized remains of ancient living organisms.", False),
    ("F", "A natural resource that can be restored or replenished as fast as or faster than it is used.", False),
    ("G", "The energy of moving water flowing through rivers or ocean tides.", True),
    ("H", "Energy from sunlight that can be used to produce electricity.", False),
    ("I", "A machine with blades that spins when moving air, water, or steam pushes against it.", False),
    ("J", "A mined resource used in nuclear power plants to produce heat.", False),
]

# MC (stem, [A,B,C,D], correct_letter, diagram_path_or_None, diagram_width)
U2_MC = [
    ("What is the main difference between a renewable and a nonrenewable resource?",
     ["Nonrenewable resources are always safer for the environment.",
      "Renewable resources cause more air pollution than nonrenewable resources.",
      "Renewable resources can be restored quickly, while nonrenewable resources take millions of years to form.",
      "Nonrenewable resources can be restored quickly by planting trees."], "C", None, None),
    ("Based on the classification chart below, which energy source should be classified as a fossil fuel?",
     ["Sunlight", "Coal", "Wind", "Uranium"], "B", "u2-classification.png", 6.2),
    ("Why are fossil fuels like petroleum considered nonrenewable resources?",
     ["They are made in factories every day.",
      "They are being used much faster than nature can create them.",
      "They can never be completely used up.",
      "They are found everywhere on Earth's surface."], "B", None, None),
    ("Which fossil fuel is a liquid formed underground that is refined into gasoline and diesel?",
     ["Petroleum (Crude Oil)", "Coal", "Natural Gas", "Uranium"], "A", None, None),
    ("Nuclear energy plants use uranium as a resource. What happens next in the energy pathway?",
     ["Uranium produces heat that helps create steam",
      "Uranium turns directly into electricity",
      "Uranium absorbs sunlight",
      "Uranium moves water through rivers"], "A", None, None),
    ("The wind turbine in the diagram converts the energy of motion of moving air into what final form of energy?",
     ["Geothermal energy", "Electricity", "Heat energy", "Solar energy"], "B", "u2-wind-turbine.png", 5.0),
    ("How does a hydroelectric dam generate electricity?",
     ["The energy of moving water pushes a turbine connected to a generator.",
      "The dam burns water to create steam.",
      "The dam uses solar panels to heat the water.",
      "The water creates wind that blows across the dam."], "A", "u2-hydro-dam.png", 6.0),
    ("A town has strong sunlight most days but very little moving water. Which energy resource would be most reliable based on availability?",
     ["Hydroelectric power", "Coal power", "Wind power", "Solar power"], "D", None, None),
    ("What is one major limitation (cost) of using solar energy?",
     ["It produces large amounts of smoke and air pollution.",
      "It requires millions of years to form underground.",
      "Solar energy depends on available sunlight, so less sunlight can limit electricity production.",
      "It requires digging a deep underground coal mine."], "C", None, None),
    ("Geothermal energy relies on heat that comes from where?",
     ["The sun's surface rays", "Warm ocean surface waves", "Burning fossilized plants", "Deep inside Earth"], "D", None, None),
    ("In most power plant systems, a spinning turbine turns a generator. What is the final form of energy produced by the generator?",
     ["Electricity", "Sound energy", "Heat energy", "Solar energy"], "A", "u2-turbine-generator.png", 6.2),
    ("A hybrid car is engineered to use two different sources of energy. Which combination is commonly used in hybrid vehicles?",
     ["Coal combustion and natural gas", "Gasoline fuel and battery power", "Wind power and solar energy", "Uranium nuclear fuel and water"], "B", None, None),
    ("Propane gas is abundant in tanks today, but it takes millions of years to form deep underground alongside crude oil. This evidence shows that propane gas is a:",
     ["Renewable resource", "Biofuel", "Nonrenewable resource", "Geothermal resource"], "C", None, None),
    ("Which of the following is a major environmental cost associated with burning fossil fuels like coal and oil?",
     ["Releasing smoke and air pollutants into the air",
      "Cooling down Earth's ocean temperatures too fast",
      "Creating excessive wind currents around power plants",
      "Depleting the total amount of sunlight reaching Earth"], "A", None, None),
    ("Scientists are researching methane hydrate ('fire ice') frozen deep under ocean floors. Because it is a fossil fuel, scientists know that methane hydrate is:",
     ["Easy to replace quickly after it is burned",
      "A nonrenewable energy resource",
      "Powered directly by solar panels",
      "Completely free of any environmental costs"], "B", None, None),
    ("Although coal power plants and nuclear power plants use different fuels, what shared step do both use to generate electricity?",
     ["They both burn fossil fuel plants underground.",
      "They both use rooftop solar cells to heat water.",
      "They both use heat to turn water into steam that spins a turbine generator.",
      "They both rely directly on flowing river currents."], "C", "u2-coal-nuclear.png", 6.2),
    ("A mountain town wants to switch to renewable energy. The area has strong, steady wind gusts every day, but it is cloudy most of the year and has no large rivers. Which renewable resource is the most reliable choice for this town?",
     ["Hydroelectric power", "Solar power", "Coal energy", "Wind power"], "D", None, None),
]

# Source alignment: (Reader chapter, Guided notes section) for each matching Q then each MC Q.
U2_MATCH_SOURCES = [
    ("Ch 1", "unit-02-ch1 p.1"),
    ("Ch 1", "unit-02-ch1 p.1"),
    ("Ch 2", "unit-02-ch1 p.1"),
    ("Ch 2", "unit-02-ch2 p.1"),
    ("Ch 4", "unit-02-ch4 p.1"),
    ("Ch 5", "unit-02-ch5 p.1"),
    ("Ch 3", "unit-02-ch3 p.2"),
    ("Ch 7", "unit-02-ch7 p.1"),
]
U2_MC_SOURCES = [
    ("Ch 1", "unit-02-ch1 p.1"),
    ("Ch 1", "unit-02-ch1 p.1"),
    ("Ch 1", "unit-02-ch1 p.1"),
    ("Ch 2", "unit-02-ch2 p.1"),
    ("Ch 4", "unit-02-ch4 p.1"),
    ("Ch 5", "unit-02-ch5 p.1"),
    ("Ch 6", "unit-02-ch6 p.1"),
    ("Ch 7", "unit-02-ch7 p.2"),
    ("Ch 7", "unit-02-ch7 p.2"),
    ("Ch 8", "unit-02-ch8 p.1"),
    ("Ch 3", "unit-02-ch3 p.2"),
    ("Ch 9", "unit-02-ch9 p.1"),
    ("Ch 1", "unit-02-ch1 p.1"),
    ("Ch 3", "unit-02-ch3 p.3"),
    ("Ch 9", "unit-02-ch1 p.1"),
    ("Ch 4", "unit-02-ch4 p.1"),
    ("Ch 5", "unit-02-ch5 p.2"),
]


# ---------------------------------------------------------------- builders
def build_student():
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.7)
        sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    _para(doc, "Grade 4 Science", size=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    _para(doc, "Unit 2 Assessment — Using Natural Resources for Energy", size=15, bold=True,
          align=WD_ALIGN_PARAGRAPH.CENTER, space_after=5)
    _para(doc, "Name: " + "_" * 32 + "    HR: 4A 4B 4C 4D", size=13, space_after=6)

    _para(doc, "Directions: Read each question and choose the ONE BEST ANSWER.", size=13, space_after=6)

    # ---- Section 1: matching ----
    _para(doc, "Section 1: Vocabulary Matching (Questions 1–8)", size=16, bold=True, space_after=4)
    _para(doc, "Write the letter of the definition that matches each word. "
               "Note: Two definitions will not be used.", size=13, space_after=5)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    hdr = table.rows[0].cells
    _cell_para(hdr[0], "Vocabulary", bold=True, size=13)
    _cell_para(hdr[1], "Definitions", bold=True, size=13)
    set_cell_margins(hdr[0]); set_cell_margins(hdr[1])

    n_terms = len(U2_TERMS)
    n_defs = len(U2_DEFS)
    rows = max(n_terms, n_defs)
    for i in range(rows):
        row = table.add_row().cells
        if i < n_terms:
            t, _ans = U2_TERMS[i]
            _cell_para(row[0], f"{i+1}. ____ {t}", size=13.5, bold_term=True)
        else:
            _cell_para(row[0], "", size=13.5)
        if i < n_defs:
            letter, dtext, _extra = U2_DEFS[i]
            _cell_para(row[1], f"{letter}. {dtext}", size=13, bold_letter=True)
        else:
            _cell_para(row[1], "", size=13)
        set_cell_margins(row[0]); set_cell_margins(row[1])

    for row in table.rows:
        row.cells[0].width = Inches(2.6)
        row.cells[1].width = Inches(4.2)

    _para(doc, "", size=12, space_after=2)

    # ---- Section 2: multiple choice ----
    _para(doc, "Section 2: Multiple Choice (Questions 9–25)", size=16, bold=True, space_after=4)
    _para(doc, "Choose the ONE BEST ANSWER for each question.", size=13, space_after=6)

    letters = ["A", "B", "C", "D"]
    for qi, (stem, opts, correct, diag, diag_w) in enumerate(U2_MC):
        qnum = qi + 9
        if diag:
            pimg = add_image_centered(doc, os.path.join(DIAG_DIR, diag), diag_w)
            pimg.paragraph_format.keep_with_next = True
        stem_p = _rich(doc, [(f"{qnum}. ", True), (stem, False)], size=13.5, space_after=3, space_before=4)
        stem_p.paragraph_format.keep_with_next = True
        for li, opt in enumerate(opts):
            op = _rich(doc, [(f"{letters[li]}. ", True), (opt, False)], size=13, space_after=2)
            if li < len(opts) - 1:
                op.paragraph_format.keep_with_next = True

    doc.save(STUDENT_PATH)
    print("saved", STUDENT_PATH)


def build_key():
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.7); sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.8); sec.right_margin = Inches(0.8)

    _para(doc, "Grade 4 Science — ANSWER KEY", size=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    _para(doc, "Unit 2 Assessment — Using Natural Resources for Energy", size=15, bold=True,
          align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    _para(doc, "Teacher only. 25 questions × 2 points = 50 points.", size=13, space_after=10)

    # matching key
    _para(doc, "Section 1: Vocabulary Matching — Answer Key (Questions 1–8 | 16 points)", size=15, bold=True, space_after=4)
    def_by_letter = {l: (d, e) for l, d, e in U2_DEFS}
    for i, (term, ans) in enumerate(U2_TERMS):
        dtext, extra = def_by_letter[ans]
        _rich(doc, [(f"{i+1}. ", True), (term, True), (f"  →  {ans}. {dtext}", False)], size=12.5, space_after=2)
    # unused distractors
    unused = [l for l, d, e in U2_DEFS if e]
    _para(doc, "", size=12, space_after=2)
    for l in unused:
        dtext, _ = def_by_letter[l]
        _rich(doc, [(f"Unused distractor {l}: ", True), (dtext, False)], size=12.5, space_after=2)

    # MC key
    _para(doc, "", size=12, space_after=2)
    _para(doc, "Section 2: Multiple Choice — Answer Key (Questions 9–25 | 34 points)", size=15, bold=True, space_after=4)
    letters = ["A", "B", "C", "D"]
    for qi, (stem, opts, correct, diag, diag_w) in enumerate(U2_MC):
        qnum = qi + 9
        correct_text = opts[letters.index(correct)]
        _rich(doc, [(f"{qnum}. ", True), (correct + ". ", True), (correct_text, False)], size=12.5, space_after=2)

    # source alignment table
    _para(doc, "", size=12, space_after=2)
    _para(doc, "Source Alignment (Reader + Guided Notes)", size=15, bold=True, space_after=4)
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = 'Light Grid Accent 1'
    hdr = tbl.rows[0].cells
    _cell_para(hdr[0], "Q", bold=True, size=11)
    _cell_para(hdr[1], "Answer", bold=True, size=11)
    _cell_para(hdr[2], "Reader", bold=True, size=11)
    _cell_para(hdr[3], "Guided Notes", bold=True, size=11)
    # matching rows
    for i, (term, ans) in enumerate(U2_TERMS):
        r = tbl.add_row().cells
        _cell_para(r[0], str(i + 1), size=11)
        _cell_para(r[1], ans, size=11)
        _cell_para(r[2], U2_MATCH_SOURCES[i][0], size=11)
        _cell_para(r[3], U2_MATCH_SOURCES[i][1], size=11)
    # MC rows
    for qi, (stem, opts, correct, diag, diag_w) in enumerate(U2_MC):
        r = tbl.add_row().cells
        _cell_para(r[0], str(qi + 9), size=11)
        _cell_para(r[1], correct, size=11)
        _cell_para(r[2], U2_MC_SOURCES[qi][0], size=11)
        _cell_para(r[3], U2_MC_SOURCES[qi][1], size=11)

    doc.save(KEY_PATH)
    print("saved", KEY_PATH)


if __name__ == "__main__":
    build_student()
    build_key()
    print("DONE")
