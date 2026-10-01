"""Unit 1 study guide — student + teacher key (Phase 13R).

Week 4 assessment prep. Aligned to the released Unit 1 assessment (25 items / 50 pts).
Covers: energy = ability to cause change, evidence, stored energy, energy of motion,
same-object speed, transfer, transformation, BOTH, collisions, criteria, constraints,
design/test/refine, Edison/Latimer.
Locked vocabulary only — no kinetic/potential/mechanical/chemical/thermal/radiation/mass/deformation.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *
from gn_design import OxmlElement, qn

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "review", "unit-01"))
os.makedirs(OUT_DIR, exist_ok=True)
SUB = "Unit 1 Study Guide · Energy Transfer & Transformation"

def save(doc, fn):
    doc.save(os.path.join(OUT_DIR, fn))
    print("saved", fn)

def page_head(doc, label, new_page=True):
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
    half = (len(meanings) + 1) // 2
    rows = list(zip(meanings[:half], meanings[half:] + [""] * (half - len(meanings[half:]))))
    t = doc.add_table(rows=len(rows), cols=2)
    no_table_borders(t)
    for r, (a, b) in enumerate(rows):
        for c, txt in ((0, a), (1, b)):
            cell = t.cell(r, c)
            set_cell_width(cell, FULL_W // 2)
            set_cell_margins(cell, top=4, left=80, bottom=4, right=80)
            if txt:
                set_run(cell.paragraphs[0].add_run(txt), size=size, color=INK)
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '24'); spPr.append(spelm)

def term_grid(doc, terms, size=13):
    """Compact 2-column numbered term list with a write-on line for the matching letter."""
    half = (len(terms) + 1) // 2
    rows = list(zip(terms[:half], terms[half:] + [""] * (half - len(terms[half:]))))
    t = doc.add_table(rows=len(rows), cols=2)
    no_table_borders(t)
    for r, (a, b) in enumerate(rows):
        for c, txt in ((0, a), (1, b)):
            cell = t.cell(r, c)
            set_cell_width(cell, FULL_W // 2)
            set_cell_margins(cell, top=12, left=80, bottom=12, right=80)
            p = cell.paragraphs[0]
            if txt:
                set_run(p.add_run(txt + "  "), size=size, bold=True, color=NAVY)
                rr = p.add_run("___________"); rr.underline = True
                set_run(rr, size=size, color=INK)
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '20'); spPr.append(spelm)

def classify_row(doc, prompt, after=26):
    """Scenario prompt + 'Circle: TRANSFER / TRANSFORMATION / BOTH' line."""
    body(doc, prompt, size=13, bold=True, after=10)
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    sp = OxmlElement('w:spacing'); sp.set(qn('w:after'), str(after * 20)); pPr.append(sp)
    set_run(p.add_run("Circle:  "), size=13, color=INK)
    for lab in ("TRANSFER", "TRANSFORMATION", "BOTH"):
        set_run(p.add_run("   " + lab + "  "), size=13, bold=True, color=NAVY)
    return p

def build_student():
    doc = new_doc()
    title_block(doc, "What Have I Learned About Energy?", SUB + " · Student")
    body(doc, "Use this sheet to get ready for the Unit 1 assessment.", size=12, italic=True, color=GRAY, after=6)

    # --- Section A: Match ---
    heading(doc, "A · Match the Word", 16, before=30)
    body(doc, "Write the letter of the correct meaning on the line.", size=12, color=GRAY, after=8)
    term_grid(doc, ["1. energy", "2. evidence", "3. stored energy", "4. energy of motion",
                    "5. transfer", "6. transformation", "7. collision", "8. criteria",
                    "9. constraints", "10. refine"])
    body(doc, "Meanings:", size=12, bold=True, after=4)
    meaning_grid(doc, [
        "A. energy changing form",
        "B. the energy a moving object has",
        "C. the limits (materials, time, safety)",
        "D. energy ready to cause change later",
        "E. what a good solution must do",
        "F. the ability to cause change",
        "G. to improve using test evidence",
        "H. two or more objects coming together",
        "I. energy moving from place to place or object to object",
        "J. what we observe that shows a change occurred"])

    # --- Section B: Fill-in ---
    heading(doc, "B · Fill in the Blank", 16, before=30)
    body(doc, "Use a word from the bank. Some words may be used more than once.", size=12, color=GRAY, after=8)
    wbank_words = ["cause change", "evidence", "stored", "motion", "faster", "transfer", "transformation"]
    body(doc, "Word bank:  " + "    ".join(wbank_words), size=12, bold=True, color=NAVY, after=12)
    fill(doc, "1. Energy is the ability to", blank="______________", trail=".", size=13, after=8)
    fill(doc, "2. A change we observe is our", blank="______________", trail=" that energy was involved.", size=13, after=8)
    fill(doc, "3. A battery, a stretched rubber band, and a raised object all have", blank="______________", trail=" energy.", size=13, after=8)
    fill(doc, "4. A moving object has energy of", blank="______________", trail=".", size=13, after=8)
    fill(doc, "5. For the SAME object, moving at a", blank="______________", trail=" speed means more energy of motion.", size=13, after=8)
    fill(doc, "6. During a collision, energy of motion can", blank="______________", trail=" to the target.", size=13, after=8)

    # PAGE 2
    page_head(doc, "Sections C–E · Page 2")

    # --- Section C: Classify ---
    heading(doc, "C · Transfer, Transformation, or BOTH?", 16, before=0)
    body(doc, "Circle the right answer for each one.", size=12, color=GRAY, after=10)
    classify_row(doc, "1. Warm water warms a cool spoon. The heat moves, and it stays heat.")
    classify_row(doc, "2. A flashlight battery turns stored energy into light.")
    classify_row(doc, "3. A domino falls and clicks: motion passes to the next domino AND some becomes sound.")
    classify_row(doc, "4. A fan changes electric current into spinning motion.")

    # --- Section D: Same object / speed ---
    heading(doc, "D · Same Object, Different Speed", 16, before=30)
    body(doc, "For the SAME object:  faster speed → more energy of motion → a bigger change.",
         size=13, bold=True, color=NAVY, after=10)
    fill(doc, "As ramp height goes up, the cup moves", blank="______________", trail=" (farther / not as far).", size=13, after=8)
    fill(doc, "This is evidence that a faster car has", blank="______________", trail=" energy of motion (more / less).", size=13, after=10)
    body(doc, "In the Ramp It Up investigation:", size=13, bold=True, after=6)
    fill(doc, "We MEASURE", blank="________________________________________", trail=".", size=13, after=8)
    fill(doc, "We INFER", blank="________________________________________", trail=".", size=13, after=8)

    # --- Section E: Diagram (flashlight) ---
    heading(doc, "E · Label the Energy Change", 16, before=30)
    body(doc, "Label the INPUT and the OUTPUT for a flashlight.", size=12, color=GRAY, after=10)
    model_boxes(doc, ["INPUT: ______________", "OUTPUT: ______________"], box_w=2400, arr_w=700, size=13)

    # PAGE 3
    page_head(doc, "Sections F–I · Page 3")

    # --- Section F: Collisions ---
    heading(doc, "F · What Happens in a Collision?", 16, before=30)
    model_boxes(doc, ["BEFORE: a moving object", "COLLISION", "AFTER: target moves + sound may happen"],
                box_w=2150, arr_w=450, size=12)
    fill(doc, "After a collision, energy does NOT", blank="______________", trail=".", size=13, after=6)
    fill(doc, "Instead, the energy of motion", blank="______________", trail=" to the target, and some becomes sound.", size=13, after=10)
    body(doc, "Hint: it does NOT disappear.", size=12, italic=True, color=GRAY, after=8)

    # --- Section G: Engineering ---
    heading(doc, "G · Engineering Words", 16, before=30)
    fill(doc, "Criteria =", blank="________________________________________", trail=".", size=13, after=8)
    fill(doc, "Constraints =", blank="________________________________________", trail=".", size=13, after=8)
    fill(doc, "Refine =", blank="________________________________________", trail=".", size=13, after=8)

    # --- Section H: Edison & Latimer ---
    heading(doc, "H · Edison & Latimer", 16, before=30)
    fill(doc, "Edison did NOT invent the first light bulb; he", blank="______________", trail=" earlier designs.", size=13, after=8)
    fill(doc, "His team tested more than", blank="______________", trail=" materials.", size=13, after=8)
    fill(doc, "In 1879, Edison found a", blank="______________", trail=" filament with a carbon coating.", size=13, after=8)
    fill(doc, "Latimer improved the bulb with a stronger, more durable", blank="______________", trail=".", size=13, after=8)

    # --- Section I: Short Response (CER) ---
    heading(doc, "I · Short Response", 16, before=30)
    body(doc, "Pick ONE device: a flashlight, a buzzer, or a ramp toy. Write a claim, give evidence, and explain your reasoning. Use \u201csupports,\u201d not \u201cproves.\u201d", size=13, bold=True, after=10)
    body(doc, "Claim: ______________________________________________________", size=13, after=8)
    wline(doc, 1, gap=26, after=8)
    body(doc, "Evidence: ___________________________________________________", size=13, after=8)
    wline(doc, 1, gap=26, after=8)
    body(doc, "Reasoning: _________________________________________________", size=13, after=8)
    wline(doc, 1, gap=26, after=8)

    save(doc, "unit1-study-guide.docx")

def build_key():
    doc = new_doc()
    title_block(doc, "What Have I Learned About Energy?", SUB + " · Teacher Key")
    heading(doc, "A · Match the Word")
    body(doc, "1-F · 2-J · 3-D · 4-B · 5-I · 6-A · 7-H · 8-E · 9-C · 10-G", size=13, after=16)
    heading(doc, "B · Fill in the Blank")
    body(doc, "1. cause change · 2. evidence · 3. stored · 4. motion · 5. faster · 6. transfer", size=13, after=16)
    heading(doc, "C · Transfer, Transformation, or BOTH?")
    body(doc, "1. TRANSFER (heat moves, stays heat) · 2. TRANSFORMATION (stored → light) · 3. BOTH (motion passes + sound) · 4. TRANSFORMATION (electric current → motion)", size=13, after=16)
    heading(doc, "D · Same Object, Different Speed")
    body(doc, "cup moves FARTHER · a faster car has MORE energy of motion.  MEASURE: ramp height / how far the cup moves.  INFER: speed and energy of motion.", size=13, after=16)
    heading(doc, "E · Label the Energy Change")
    body(doc, "INPUT: stored energy (battery) → OUTPUT: light (and a little heat).", size=13, after=16)
    heading(doc, "F · What Happens in a Collision?")
    body(doc, "energy does NOT disappear · transfers to the target (some becomes sound).", size=13, after=16)
    heading(doc, "G · Engineering Words")
    body(doc, "Criteria = what a good solution must do · Constraints = the limits (materials, time, safety) · Refine = to improve using test evidence.", size=13, after=16)
    heading(doc, "H · Edison & Latimer")
    body(doc, "improved · 6,000 · bamboo · filament.", size=13, after=16)
    heading(doc, "I · Short Response")
    body(doc, "Any device: claim (what it does) + evidence (what is observed) + reasoning (why the evidence supports the claim), using \u201csupports.\u201d Example: flashlight — claim: a flashlight changes stored energy into light; evidence: the room gets brighter when it turns on; reasoning: the brightness is the change that supports the claim.", size=13, after=16)
    save(doc, "unit1-study-guide-key.docx")

if __name__ == "__main__":
    build_student()
    build_key()
    print("DONE")
