"""Phase 7 — Chapter 2 Guided Notes automated student-artifact QA.

Headless gates against the FINAL Ch2 guided notes (student + teacher key):
  US Letter · margins · font floors · page count · blank widths · multi-word
  blank separation · handwriting vertical clearance · visual-system token
  compliance · grayscale contrast · Reader page refs · BQ/V/N consistency ·
  no stale INB/26-item language · no unsupported advanced vocabulary ·
  key/student pagination parity · all blanks answered in key.

Run: .venv/bin/python tools/qa_ch2_guided_notes.py
"""
import os, re, subprocess, sys
from docx import Document
from docx.oxml.ns import qn

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DIR = os.path.join(ROOT, "production", "premium-notes")
STUDENT = os.path.join(DIR, "02-ch2-moving-objects-have-energy-guided-notes")
KEY = os.path.join(DIR, "02-ch2-moving-objects-have-energy-guided-notes-key")
REPORT_DIR = os.path.join(ROOT, "qa", "reports")

# ---- FROZEN tokens (Ch2 + unit neutrals) -----------------------------------
ALLOWED_FILLS = {
    "1A1D26", "4A5268", "FFFFFF", "F6F7F9", "D8DCE4",   # unit neutrals (incl. MIST panel)
    "0F5A5C", "0E8A97", "5B6770",                        # Ch2 Motion (surface = white)
}

# Exact authoritative wording (verified vs Student Reader pp.7-12 + TG Lesson 3)
BQ_EXACT = "How are energy, change, and movement of objects related?"
V_GROUPS = ["V1", "V2"]
N_SECTIONS = ["N1", "N2", "N3"]
VOCAB_ANSWERS = ["position", "moving"]
CONCEPT_ANSWERS = ["change", "outside", "motion"]
KEY_SAMPLE_MARKERS = ["Sample:", "Accept any"]

EXPECT_PAGES = 3

BANNED = [
    "26 items", "26 questions", "26Q", "26 Q", "26-item",
    "Interactive Science Notebook is the primary", "INB-primary", "INB",
    "kinetic", "potential", "mechanical", "radiant", "momentum", "inertia",
    "compression wave", "gravitational potential", "proof", "proves",
]

def iter_paragraphs(container):
    if hasattr(container, "paragraphs"):
        for p in container.paragraphs:
            yield p
    if hasattr(container, "tables"):
        for t in container.tables:
            for row in t.rows:
                for c in row.cells:
                    yield from iter_paragraphs(c)

def all_runs(doc):
    for p in iter_paragraphs(doc):
        for r in p.runs:
            yield r, p

def full_text(doc):
    return "\n".join(p.text for p in iter_paragraphs(doc))

def pdf_pages(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", info)
    return int(m.group(1)) if m else -1

def pdf_size(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
    return (float(m.group(1)), float(m.group(2))) if m else (0, 0)

def underline_blank_runs(doc):
    out = []
    for r, _p in all_runs(doc):
        t = r.text or ""
        if t and t.strip("_") == "" and "_" in t and r.font.underline:
            sz = r.font.size.pt if r.font.size else 0
            out.append((len(t) * sz / 144.0, sz))
    return out

# ---------------------------------------------------------------- gates
def gate_page_size(doc):
    sec = doc.sections[0]
    w, h = sec.page_width / 914400, sec.page_height / 914400
    ok = abs(w - 8.5) < 0.01 and abs(h - 11.0) < 0.01
    return ("PASS" if ok else "FAIL", f"{w:.2f} x {h:.2f} in (expect 8.5 x 11)")

def gate_margins(doc):
    sec = doc.sections[0]
    vals = {"left": sec.left_margin / 914400, "right": sec.right_margin / 914400,
            "top": sec.top_margin / 914400, "bottom": sec.bottom_margin / 914400}
    ok = all(0.50 <= vals[k] <= 0.60 for k in ("left", "right")) and \
         vals["top"] >= 0.49 and vals["bottom"] >= 0.49
    return ("PASS" if ok else "WARN", f"margins { {k: round(v, 2) for k, v in vals.items()} }")

def gate_font_floors(doc):
    sizes = [r.font.size.pt for r, _ in all_runs(doc) if r.font.size and (r.text or "").strip()]
    if not sizes:
        return ("FAIL", "no sized runs")
    lo = min(sizes)
    return ("PASS" if lo >= 8.0 else "FAIL", f"min run size {lo:.1f} pt (floor 8)")

def gate_fill_line_clearance(doc):
    low = []
    for p in iter_paragraphs(doc):
        if p.runs and any((r.text or "").strip("_") == "" and "_" in (r.text or "") for r in p.runs):
            ls = p.paragraph_format.line_spacing
            if ls is not None and ls.pt < 24:
                low.append(round(ls.pt, 1))
    return ("PASS" if not low else "WARN", f"fill lines below 24pt: {low or 'none'}")

def gate_blank_widths(blanks):
    bad = [round(w, 2) for w, s in blanks if w < 0.4 or w > 2.3]
    return ("PASS" if not bad else "WARN", f"blank widths out of 0.4-2.3in: {bad or 'none'}")

def gate_multiword_separation(doc):
    return gate_blank_widths(underline_blank_runs(doc))

def gate_tokens(doc):
    fills = set()
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                tcPr = cell._tc.find(qn("w:tcPr"))
                if tcPr is not None:
                    for el in tcPr.findall(qn("w:shd")):
                        f = el.get(qn("w:fill"))
                        if f and f != "auto":
                            fills.add(f.lstrip("#").upper())
    unknown = fills - ALLOWED_FILLS
    return ("PASS" if not unknown else "WARN", f"fills: {sorted(fills)}; unknown: {sorted(unknown) or 'none'}")

def gate_grayscale_contrast():
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    def lum(h):
        return 0.2126 * lin(int(h[0:2], 16)) + 0.7152 * lin(int(h[2:4], 16)) + 0.0722 * lin(int(h[4:6], 16))
    bad = []
    for h in ("0F5A5C", "0E8A97", "5B6770"):
        ratio = 1.05 / (lum(h) + 0.05)
        if ratio < 3.0:
            bad.append(f"{h}:{ratio:.1f}")
    return ("PASS" if not bad else "WARN", f"chapter tokens vs white <3:1: {bad or 'none'}")

def gate_bq_vn(doc):
    text = full_text(doc)
    missing = []
    if BQ_EXACT not in text:
        missing.append("BQ exact wording")
    for code in V_GROUPS + N_SECTIONS:
        if code not in text:
            missing.append(code)
    seq = ["BQ", "V1", "N1", "V2", "N2", "N3"]
    idx = [text.find(c) for c in seq]
    order_ok = all(a >= 0 for a in idx) and all(a < b for a, b in zip(idx, idx[1:]))
    if not order_ok:
        missing.append("BQ/V/N order")
    return ("PASS" if not missing else "FAIL", f"missing/out-of-order: {missing or 'none'}")

def gate_reader_refs(doc):
    text = full_text(doc)
    refs = ["Reader p. 7", "Reader p. 8", "Reader p. 9", "Reader pp. 10"]
    present = [r for r in refs if r in text]
    return ("PASS" if len(present) >= 4 else "WARN", f"Reader page refs found: {present}")

def gate_banned(doc):
    text = full_text(doc).lower()
    hits = [b for b in BANNED if b.lower() in text]
    return ("PASS" if not hits else "FAIL", f"banned/stale language: {sorted(set(hits)) or 'none'}")

def gate_no_ch3_leak(doc):
    """No Chapter 3 speed-energy depth: 'speed' must not appear as a required/blanked term."""
    text = full_text(doc)
    hits = [m for m in re.findall(r"[Ss]peed", text)]
    return ("PASS" if not hits else "WARN", f"'speed' occurrences (Ch3 term): {len(hits)}")

def gate_answers_in_key(key_doc):
    text = full_text(key_doc)
    missing = [a for a in VOCAB_ANSWERS + CONCEPT_ANSWERS if a not in text]
    samples_ok = all(m in text for m in KEY_SAMPLE_MARKERS)
    return ("PASS" if not missing and samples_ok else "FAIL",
            f"missing answers: {missing or 'none'}; sample markers: {samples_ok}")

def gate_draw_box(doc):
    """The marble BEFORE/AFTER row must be at least 2.0 inches (2880 twips)."""
    from docx.oxml.ns import qn
    highs = []
    for t in doc.tables:
        blob = " ".join(c.text for r in t.rows for c in r.cells)
        if "BEFORE" not in blob or "AFTER" not in blob:
            continue
        for tr in t._tbl.tr_lst:
            for h in tr.findall(".//" + qn("w:trHeight")):
                highs.append(int(h.get(qn("w:val")) or 0))
    ok = bool(highs) and max(highs) >= 2880
    return ("PASS" if ok else "FAIL", "tallest BEFORE/AFTER row %s twips (need >= 2880)" % (max(highs) if highs else "missing"))

def gate_key_no_unanswered_blanks(key_doc):
    unders = [w for w, s in underline_blank_runs(key_doc)]
    content_blanks = [round(w, 2) for w in unders if w < 1.9]
    return ("PASS" if not content_blanks else "FAIL", f"unfilled content blanks in key: {content_blanks or 'none'}")

def main():
    import argparse
    global ROOT, DIR, STUDENT, KEY, REPORT_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    a, _unknown = ap.parse_known_args()
    if a.root:
        ROOT = os.path.abspath(a.root)
        DIR = os.path.join(ROOT, "production", "premium-notes")
        STUDENT = os.path.join(DIR, "02-ch2-moving-objects-have-energy-guided-notes")
        KEY = os.path.join(DIR, "02-ch2-moving-objects-have-energy-guided-notes-key")
        REPORT_DIR = os.path.join(ROOT, "qa", "reports")
    s_doc = Document(STUDENT + ".docx")
    k_doc = Document(KEY + ".docx")
    s_pages = pdf_pages(STUDENT + ".pdf")
    k_pages = pdf_pages(KEY + ".pdf")
    s_size = pdf_size(STUDENT + ".pdf")

    gates = []
    def add(name, result):
        gates.append((name, result))

    add("US Letter (student DOCX)", gate_page_size(s_doc))
    add("US Letter (key DOCX)", gate_page_size(k_doc))
    add("Margins 0.50-0.60in", gate_margins(s_doc))
    add("Font floors >= 8pt", gate_font_floors(s_doc))
    add("Fill-line clearance >= 24pt", gate_fill_line_clearance(s_doc))
    add("Blank widths 0.4-2.3in", gate_blank_widths(underline_blank_runs(s_doc)))
    add("Multi-word blank separation", gate_multiword_separation(s_doc))
    add("Visual token compliance", gate_tokens(s_doc))
    add("Grayscale contrast", gate_grayscale_contrast())
    add("BQ/V/N consistency + order", gate_bq_vn(s_doc))
    add("Reader page refs", gate_reader_refs(s_doc))
    add("No banned/stale language", gate_banned(s_doc))
    add("No Ch3 speed leakage", gate_no_ch3_leak(s_doc))
    add("Key/student pagination parity", ("PASS" if s_pages == k_pages == EXPECT_PAGES else "FAIL",
        f"student={s_pages} key={k_pages} (expect {EXPECT_PAGES}/{EXPECT_PAGES})"))
    add("PDF page count = 3", ("PASS" if s_pages == EXPECT_PAGES else "FAIL", f"student={s_pages}"))
    add("PDF US Letter size", ("PASS" if (abs(s_size[0] - 612) < 2 and abs(s_size[1] - 792) < 2) else "FAIL",
        f"student {s_size} (expect 612x792)"))
    add("All blanks answered in key", gate_answers_in_key(k_doc))
    add("No unanswered blanks in key", gate_key_no_unanswered_blanks(k_doc))
    add("BEFORE/AFTER draw box >= 2.0 in", gate_draw_box(s_doc))

    print("=" * 74)
    print("CH2 GUIDED NOTES — AUTOMATED STUDENT-ARTIFACT QA (Phase 7)")
    print("=" * 74)
    overall = "PASS"
    for name, (s, note) in gates:
        if s == "FAIL":
            overall = "FAIL"
        elif s == "WARN" and overall == "PASS":
            overall = "WARN"
        print(f"[{s:4}] {name:38} {note}")
    print("=" * 74)
    print(f"OVERALL: {overall}")

    os.makedirs(REPORT_DIR, exist_ok=True)
    out = os.path.join(REPORT_DIR, "PHASE_7_CH2_GUIDED_NOTES_QA.md")
    with open(out, "w") as f:
        f.write("# Phase 7 — Chapter 2 Guided Notes Automated QA\n\n")
        f.write(f"Overall: **{overall}**\n\n")
        for name, (s, note) in gates:
            f.write(f"- [{s}] {name} — {note}\n")
    print(f"report: {out}")
    if overall == "FAIL":
        sys.exit(1)

if __name__ == "__main__":
    main()
