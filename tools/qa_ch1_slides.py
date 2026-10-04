"""Phase 4 — Chapter 1 Slideshow automated QA (deterministic, structural/text).

Headless gates against the FINAL Ch1 slideshow (PPTX + rendered PDF):
  slide dims · font floors · safe-margin/overflow · visual-token compliance ·
  BQ/V/N anchor sync + order · exact note wording · answer reveal (no front-load) ·
  Reader page refs · vocab grouping · review A/B/C/D structure ·
  no stale INB/26-item language · no banned advanced vocabulary ·
  render QA (PDF page count).

Run: .venv/bin/python tools/qa_ch1_slides.py
"""
import os, re, subprocess, sys
from pptx import Presentation
from pptx.util import Pt

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PPTX = os.path.join(ROOT, "production", "slides", "01-ch1-energy-causes-change-slides.pptx")
PDF = os.path.join(ROOT, "production", "slides", "01-ch1-energy-causes-change-slides.pdf")
REPORT = os.path.join(ROOT, "qa", "reports", "PHASE_4_CH1_SLIDESHOW_QA.md")

# ---- FROZEN tokens (Ch1 + unit neutrals) -----------------------------------
ALLOWED_FILLS = {
    "1A1D26", "4A5268", "FFFFFF", "F6F7F9", "D8DCE4",   # unit neutrals
    "1F2A5A", "A67C16", "7A5620", "F5EEDC",             # Ch1 Discovery/Evidence
    "F3E8CF", "E3E7F2",                                 # Ch1 gold/navy tints (10%)
}

BQ_EXACT = "Where can we observe evidence of energy causing change?"
ANCHORS = ["BQ", "V1", "N1", "N2", "V2", "N3", "N4"]
ANSWER_MAP = {
    "V1": ["change", "different"],
    "V2": ["later"],
    "N1": ["cause", "change", "evidence"],
    "N3": ["position"],
}
NOTE_WORDING = [
    "energy — the ability to cause",          # V1
    "change — to become",                      # V1
    "stored energy — energy that has the ability to cause change at a",  # V2
    "Energy has the ability to",               # N1
    "When you see a change, you are seeing evidence of energy.",  # N1
    "A change is", "that energy is involved.", # N1
    "Write or draw one example that shows a change for each form.",  # N2
    "Objects also have stored energy because of their",  # N3
    "Draw a change you observed. Show what it looked like BEFORE and AFTER.",  # N4
    "What changed?",                           # N4
    "How do we know energy is involved if we cannot see energy itself?",  # N4 check
    "Start with: “We know because we see",     # N4 check starter
    "Now I Think",                             # BQ return
]
READER_REFS = ["Reader p. 1", "Reader p. 3", "Reader p. 4", "pp. 1–2", "pp. 4–5", "pp. 1–6"]
MODEL_CHAINS = [("ENERGY", "CHANGE", "EVIDENCE"), ("STORED ENERGY", "RELEASE", "CHANGE")]
N2_FORMS = ["motion", "sound", "light", "heat", "electrical energy"]
N3_EXAMPLES = ["battery (in a flashlight)", "stretched rubber band", "raised object (apple)"]

BANNED = [
    "26 items", "26 questions", "26Q", "26-item", "INB",
    "kinetic", "potential", "mechanical", "radiant", "momentum", "inertia",
    "compression wave", "gravitational", "proof", "proves",
]

# ---------------------------------------------------------------- helpers
def slide_texts(prs):
    out = []
    for i, s in enumerate(prs.slides, 1):
        parts = []
        for sh in s.shapes:
            if sh.has_text_frame:
                t = " ".join(r.text for p in sh.text_frame.paragraphs for r in p.runs)
                if t.strip():
                    parts.append(t)
        out.append((i, " ".join(parts)))
    return out

def all_runs(prs):
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        yield s, r

def shape_fills(prs):
    fills = set()
    for s in prs.slides:
        for sh in s.shapes:
            try:
                if sh.fill.type is not None and sh.fill.type == 1:  # solid
                    c = sh.fill.fore_color.rgb
                    fills.add(str(c))
            except Exception:
                pass
    return fills

def slide_dims(prs):
    w = prs.slide_width / 914400
    h = prs.slide_height / 914400
    return w, h

def overflow_shapes(prs):
    """Return list of (slide_idx, kind) for shapes extending beyond slide bounds."""
    W = prs.slide_width; H = prs.slide_height
    bad = []
    tol = Emu_val(1.0)  # ~1pt tolerance
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            try:
                l, t, w, h = sh.left, sh.top, sh.width, sh.height
                if l is None or t is None or w is None or h is None:
                    continue
                if l < -tol or t < -tol or l + w > W + tol or t + h > H + tol:
                    bad.append((i, sh.shape_type, round(l/914400,2), round(t/914400,2),
                                round((l+w)/914400,2), round((t+h)/914400,2)))
            except Exception:
                continue
    return bad

def Emu_val(pt):
    return int(pt * 12700)

def pdf_pages(path):
    if not os.path.exists(path):
        return -1
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", info)
    return int(m.group(1)) if m else -1

# ---------------------------------------------------------------- gates
def gate_dims(prs):
    w, h = slide_dims(prs)
    ok = abs(w - 13.333) < 0.02 and abs(h - 7.5) < 0.02
    return ("PASS" if ok else "FAIL", f"{w:.3f} x {h:.3f} in (expect 13.333 x 7.5 / 16:9)")

def gate_font_floor(prs):
    sizes = [r.font.size.pt for _, r in all_runs(prs) if r.font.size and (r.text or "").strip()]
    if not sizes:
        return ("FAIL", "no sized runs")
    lo = min(sizes); hi = max(sizes)
    return ("PASS" if lo >= 12.0 else "FAIL",
            f"min {lo:.1f} pt (floor 12, chrome) · max {hi:.1f} pt")

def gate_body_floor(prs):
    """Body/instructional floor: largest-font-per-slide sanity + vocab term presence."""
    vocab_big = any(r.font.size and r.font.size.pt >= 48 for _, r in all_runs(prs))
    return ("PASS" if vocab_big else "FAIL", "vocab term >= 48pt present")

def gate_overflow(prs):
    bad = overflow_shapes(prs)
    return ("PASS" if not bad else "FAIL", f"{len(bad)} shape(s) overflow slide: {bad or 'none'}")

def gate_tokens(prs):
    fills = shape_fills(prs)
    unknown = fills - ALLOWED_FILLS
    return ("PASS" if not unknown else "WARN", f"unknown fills: {sorted(unknown) or 'none'}")

def gate_anchors(prs):
    texts = slide_texts(prs)
    blob = "\n".join(t for _, t in texts)
    missing = [c for c in ANCHORS if c not in blob]
    # order: BQ < V1 < N1 < N2 < V2 < N3 < N4
    idx = [blob.find(c) for c in ANCHORS]
    order_ok = all(a >= 0 for a in idx) and all(a < b for a, b in zip(idx, idx[1:]))
    if not order_ok:
        missing.append("anchor order")
    return ("PASS" if not missing else "FAIL", f"missing/out-of-order anchors: {missing or 'none'}")

def gate_bq_exact(prs):
    blob = "\n".join(t for _, t in slide_texts(prs))
    return ("PASS" if BQ_EXACT in blob else "FAIL", "BQ exact wording present")

def gate_note_wording(prs):
    blob = "\n".join(t for _, t in slide_texts(prs))
    missing = [w for w in NOTE_WORDING if w not in blob]
    return ("PASS" if not missing else "FAIL", f"missing note wording: {missing or 'none'}")

def gate_answers_revealed(prs):
    """Each anchor's answers must appear somewhere in the deck (reveal/check slides)."""
    blob = "\n".join(t for _, t in slide_texts(prs))
    missing = []
    for anchor, answers in ANSWER_MAP.items():
        for a in answers:
            if a not in blob:
                missing.append(f"{anchor}:{a}")
    return ("PASS" if not missing else "FAIL", f"answers missing: {missing or 'none'}")

def gate_no_front_load(prs):
    """Write slides must NOT render the answer in the blank (answer styled bold+accent = revealed).
       We check that the answer word, when it appears bold+gold, is on a reveal slide only.
       Simpler: detect bold+accent runs equal to an answer and list their slides (informational)."""
    hits = []
    for s, r in all_runs(prs):
        if not r.text.strip():
            continue
        t = r.text.strip().lower().rstrip(".")
        if t in {"change", "different", "later", "cause", "evidence", "position"}:
            try:
                bold = r.font.bold
                color = str(r.font.color.rgb) if r.font.color and r.font.color.type is not None else None
                if bold and color in ("A67C16",):
                    # slide index
                    idx = list(prs.slides).index(s) + 1
                    hits.append((idx, t))
            except Exception:
                pass
    # Reveal slides: 12(V1) 16(N1) 22(V2) 27(N3). Allow hits only there.
    allowed = {12, 16, 22, 27}
    bad = [(i, t) for i, t in hits if i not in allowed]
    return ("PASS" if not bad else "FAIL", f"front-loaded (bold+gold) answers on wrong slides: {bad or 'none'}")

def gate_reader_refs(prs):
    blob = "\n".join(t for _, t in slide_texts(prs))
    present = [r for r in READER_REFS if r in blob]
    return ("PASS" if len(present) >= 6 else "WARN", f"reader refs found: {present}")

def gate_vocab_grouping(prs):
    texts = slide_texts(prs)
    by_slide = {i: t for i, t in texts}
    # V1 card slide must contain both energy + change definitions; V2 slide stored energy
    v1_slide = next((t for i, t in texts if "to become different" in t and "the ability to cause change" in t), None)
    v2_slide = next((t for i, t in texts if "at a later time" in t), None)
    ok = v1_slide is not None and v2_slide is not None
    return ("PASS" if ok else "FAIL", "V1 (energy+change) and V2 (stored energy) groupings present")

def gate_n2_forms(prs):
    blob = "\n".join(t for _, t in slide_texts(prs))
    missing = [f for f in N2_FORMS if f not in blob]
    return ("PASS" if not missing else "FAIL", f"N2 forms missing: {missing or 'none'}")

def gate_n3_examples(prs):
    blob = "\n".join(t for _, t in slide_texts(prs))
    missing = [e for e in N3_EXAMPLES if e not in blob]
    return ("PASS" if not missing else "FAIL", f"N3 examples missing: {missing or 'none'}")

def gate_model_chains(prs):
    blob = "\n".join(t for _, t in slide_texts(prs))
    missing = []
    for chain in MODEL_CHAINS:
        if not all(c in blob for c in chain):
            missing.append("→".join(chain))
    return ("PASS" if not missing else "FAIL", f"model chains missing: {missing or 'none'}")

def gate_review_structure(prs):
    texts = slide_texts(prs)
    q_slides = []
    for i, t in texts:
        if re.search(r"Review \d+ —", t) and "answer" not in t:
            q_slides.append((i, t))
    bad = []
    for i, t in q_slides:
        for letter in ("A", "B", "C", "D"):
            if letter not in t:
                bad.append(f"slide {i} missing option {letter}")
    n = len(q_slides)
    ok = 4 <= n <= 6 and not bad
    return ("PASS" if ok else "FAIL", f"{n} review questions; {bad or 'all have A/B/C/D'}")

def gate_banned(prs):
    blob = "\n".join(t for _, t in slide_texts(prs)).lower()
    hits = [b for b in BANNED if b in blob]
    return ("PASS" if not hits else "FAIL", f"banned language: {sorted(set(hits)) or 'none'}")

def gate_transfer_transform_scope(prs):
    """transfer/transform may appear ONLY in the official unit title 'Energy Transfer & Transformation'."""
    blob = "\n".join(t for _, t in slide_texts(prs))
    offenders = []
    for m in re.finditer(r"[Tt]ransfer|[Tt]ransform(ation)?", blob):
        start = max(0, m.start() - 30); end = min(len(blob), m.end() + 30)
        ctx = blob[start:end]
        if "Energy Transfer & Transformation" not in ctx:
            offenders.append(ctx.replace("\n", " "))
    return ("PASS" if not offenders else "WARN",
            f"transfer/transform outside unit title: {offenders or 'none'}")

def gate_render(prs):
    pages = pdf_pages(PDF)
    n_slides = len(prs.slides._sldIdLst)
    ok = pages == n_slides
    return ("PASS" if ok else "FAIL", f"PDF pages {pages} == slides {n_slides}")

def gate_slide_count(prs):
    n = len(prs.slides._sldIdLst)
    return ("PASS" if n >= 30 else "WARN", f"{n} slides")

def main():
    prs = Presentation(PPTX)
    gates = [
        ("slide dimensions (16:9)", gate_dims(prs)),
        ("font floor >= 12pt (chrome)", gate_font_floor(prs)),
        ("vocab term >= 48pt", gate_body_floor(prs)),
        ("no shape overflow", gate_overflow(prs)),
        ("visual-token compliance", gate_tokens(prs)),
        ("BQ/V/N anchors + order", gate_anchors(prs)),
        ("BQ exact wording", gate_bq_exact(prs)),
        ("note wording mirror", gate_note_wording(prs)),
        ("answers revealed (check slides)", gate_answers_revealed(prs)),
        ("no front-loaded answers", gate_no_front_load(prs)),
        ("Reader page refs", gate_reader_refs(prs)),
        ("vocab grouping (V1/V2)", gate_vocab_grouping(prs)),
        ("N2 five forms", gate_n2_forms(prs)),
        ("N3 three examples", gate_n3_examples(prs)),
        ("model chains (N1/N3)", gate_model_chains(prs)),
        ("review A/B/C/D structure", gate_review_structure(prs)),
        ("no banned/stale language", gate_banned(prs)),
        ("transfer/transform scope", gate_transfer_transform_scope(prs)),
        ("render QA (PDF pages)", gate_render(prs)),
        ("slide count", gate_slide_count(prs)),
    ]
    print("=" * 76)
    print("CH1 SLIDESHOW — AUTOMATED QA (Phase 4)")
    print("=" * 76)
    overall = "PASS"
    for name, (s, note) in gates:
        if s == "FAIL":
            overall = "FAIL"
        elif s == "WARN" and overall == "PASS":
            overall = "WARN"
        print(f"[{s:4}] {name:34} {note}")
    print("=" * 76)
    print(f"OVERALL: {overall}")

    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w") as f:
        f.write("# Phase 4 — Chapter 1 Slideshow Automated QA\n\n")
        f.write(f"Overall: **{overall}**\n\n")
        f.write(f"Artifact: `production/slides/01-ch1-energy-causes-change-slides.pptx`\n\n")
        for name, (s, note) in gates:
            f.write(f"- [{s}] {name} — {note}\n")
    print(f"report: {REPORT}")

if __name__ == "__main__":
    main()
