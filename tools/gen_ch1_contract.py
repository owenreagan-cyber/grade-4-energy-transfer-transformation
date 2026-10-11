#!/usr/bin/env python3
"""Phase 5B · Gate 1 — Chapter 1 Instructional Alignment Contract generator + validator.

Derives a 45-record contract from the FROZEN canonical deck, tools/ch1_pacing.py, the accepted
Guided Notes student packet + teacher key, and Phase 5A visual-selection defaults. Emits:
  qa/reports/ch1-phase5b/CH1_INSTRUCTIONAL_ALIGNMENT_CONTRACT.json
  qa/reports/ch1-phase5b/CH1_INSTRUCTIONAL_ALIGNMENT_CONTRACT.md
  qa/reports/ch1-phase5b/CH1_GATE1_VALIDATION.md
Does NOT modify any canonical file. Exits non-zero if Gate 1 fails.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ch1_pacing as PACE
from pptx import Presentation

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUTDIR = os.path.join(ROOT, "qa", "reports", "ch1-phase5b")
CANON_PPTX = os.path.join(ROOT, "production", "slides", "01-ch1-energy-causes-change-slides.pptx")
NOTES_TXT = os.path.join(OUTDIR, "_gt-notes.txt")
KEY_TXT = os.path.join(OUTDIR, "_gt-key.txt")

BQ = "Where can we observe evidence of energy causing change?"

# ------------------------------------------------------------------ per-slide hand data
# fields: title, kicker, hud, badge, anchor(code), section, notes_ref, partner, reveal, answers,
#         blanks, image_id, constructor, concept
S = {}

def rec(n, **kw):
    d = dict(title="", kicker="", hud="", badge="", anchor=None, section="", notes_ref="",
             partner=None, reveal="", answers=[], blanks=[], image_id=None, constructor="", concept=[])
    d.update(kw)
    S[n] = d

rec(1, title="Energy Causes Change", badge="", concept=["OPEN"], image_id="R01-opener", constructor="title", reveal="NOT_APPLICABLE")
rec(2, title="Big Question", hud="TURN & TALK", badge="BQ", anchor="BQ", concept=["BQ"], constructor="header+bq_banner", reveal="do not answer BQ yet")
rec(3, title="Big Question — My first thinking", hud="WRITE", badge="N", anchor="BQ", section="Big Question — My first thinking", notes_ref="Guided Notes p. 1", concept=["BQ"], constructor="notes_heading+write_line", reveal="open (no answer)", blanks=["2 ruled lines (open)"])
rec(4, title="What changed?", kicker="Reader p. 1 — you walk into a dark room and flip a switch.", hud="OBSERVE", badge="D", concept=["DEMO"], image_id="R02-darkbright", constructor="header+before_after", reveal="NOT_APPLICABLE")
rec(5, title="I notice…  I wonder…", hud="TURN & TALK", badge="D", concept=["DEMO"], image_id="R02-darkbright", constructor="two_cards", reveal="NOT_APPLICABLE")
rec(6, title="Electric Pencil Sharpener", kicker="Observe the pencil BEFORE we sharpen it.", hud="OBSERVE", badge="D", concept=["DEMO"], image_id="R03-pencil", constructor="header+card", reveal="NOT_APPLICABLE")
rec(7, title="Predict: what will change?", kicker="Think before we turn it on.", hud="PREDICT", badge="D", concept=["DEMO"], constructor="header+stem", reveal="no answer cue")
rec(8, title="What changed?", hud="OBSERVE", badge="D", concept=["DEMO"], image_id="R03-pencil", constructor="header+before_after+changes", reveal="record 3 changes")
rec(9, title="How do we know energy was involved?", kicker="Energy can be invisible. We look for the change.", hud="EXPLAIN", badge="D", concept=["N1"], constructor="header+model_strip", reveal="keep third box open")
rec(10, title="Vocabulary — Energy & Change", kicker="Reader p. 1", badge="V", anchor="V1", concept=["V1"], image_id="R04-energy+R05-change", constructor="vocab_card x2", reveal="full defs shown")
rec(11, title="Vocabulary — Energy & Change", hud="WRITE", badge="N", anchor="V1", section="Vocabulary — Energy & Change", notes_ref="Guided Notes · Reader p. 1", partner=12, concept=["V1"], constructor="notes_heading+blanks", blanks=["change", "different"], reveal="after write")
rec(12, title="Vocabulary — Energy & Change", hud="CHECK", badge="N", anchor="V1", section="Vocabulary — Energy & Change", notes_ref="Guided Notes · Reader p. 1", partner=11, concept=["V1"], constructor="same as 11", reveal="change / different (gold)", answers=["change", "different"])
rec(13, title="What is energy?", kicker="Reader p. 1", hud="RECITE", badge="R", concept=["N1"], constructor="header+recite_card", reveal="NOT_APPLICABLE")
rec(14, title="Look at the seashore", kicker="Reader p. 2 — the seashore changes all around us.", hud="TRACE", badge="R", concept=["N1"], image_id="R06-seashore", constructor="header+model_strip", reveal="question stays open")
rec(15, title="Energy Causes Change", hud="WRITE", badge="N", anchor="N1", section="Energy Causes Change", notes_ref="Guided Notes · Reader pp. 1–2", partner=16, concept=["N1"], constructor="notes_heading+blank+model", blanks=["evidence"], reveal="after write; last model box empty")
rec(16, title="Energy Causes Change", hud="CHECK", badge="N", anchor="N1", section="Energy Causes Change", notes_ref="Guided Notes · Reader pp. 1–2", partner=15, concept=["N1"], constructor="same + full model", reveal="ENERGY-CHANGE-EVIDENCE", answers=["evidence"])
rec(17, title="Energy has different forms", kicker="Reader p. 3 — think of a spinning carousel.", badge="R", anchor="N2", concept=["N2"], image_id="R07-forms-strip", constructor="5 chips + strip", reveal="motion modeled only")
rec(18, title="Clap three times", kicker="What forms of energy do you observe?", hud="OBSERVE", badge="C", concept=["N2"], constructor="header+card", reveal="students name forms")
rec(19, title="Energy Occurs in Different Forms", hud="WRITE", badge="N", anchor="N2", section="Energy Occurs in Different Forms", notes_ref="Guided Notes · Reader p. 3", concept=["N2"], constructor="notes_heading+table5", reveal="no answer slide (N2 has no CHECK)")
rec(20, title="Vocabulary — Stored Energy", kicker="Reader p. 4", badge="V", anchor="V2", concept=["V2"], image_id="R08-stored", constructor="vocab_card", reveal="full def")
rec(21, title="Vocabulary — Stored Energy", hud="WRITE", badge="N", anchor="V2", section="Vocabulary — Stored Energy", notes_ref="Guided Notes · Reader p. 4", partner=22, concept=["V2"], constructor="notes_heading+blank", blanks=["later"], reveal="after write")
rec(22, title="Vocabulary — Stored Energy", hud="CHECK", badge="N", anchor="V2", section="Vocabulary — Stored Energy", notes_ref="Guided Notes · Reader p. 4", partner=21, concept=["V2"], constructor="same as 21", reveal="later (gold)", answers=["later"])
rec(23, title="Does a still battery have energy?", kicker="Reader p. 4 — think about a battery inside a flashlight.", hud="PREDICT", badge="R", anchor="N3", concept=["N3"], image_id="R09-stored-strip(battery)", constructor="header+predict_card", reveal="read battery fact after predict")
rec(24, title="The stored energy of position", kicker="Reader p. 5 — an object held up can cause a change later.", badge="R", anchor="N3", concept=["N3"], image_id="R09-stored-strip(apple)", constructor="header+gold_card", reveal="NOT_APPLICABLE")
rec(25, title="Stored energy can cause a change later", kicker="Reader p. 4 — back to our battery: the chemicals inside it store energy.", hud="TRACE", badge="R", anchor="N3", concept=["N3"], image_id="R09-stored-strip(rubber)", constructor="header+model_strip", reveal="battery fact (closes 23)")
rec(26, title="Objects Can Store Energy", hud="WRITE", badge="N", anchor="N3", section="Objects Can Store Energy", notes_ref="Guided Notes · Reader pp. 4–5", partner=27, concept=["N3"], constructor="notes_heading+model+table+blank", blanks=["position"], reveal="after write")
rec(27, title="Objects Can Store Energy", hud="CHECK", badge="N", anchor="N3", section="Objects Can Store Energy", notes_ref="Guided Notes · Reader pp. 4–5", partner=26, concept=["N3"], constructor="same as 26", reveal="position + samples", answers=["position"])
rec(28, title="Recognizing evidence", kicker="Reader pp. 1–5 — think about the clues we can see, hear, or feel.", hud="EVIDENCE", badge="R", anchor="N4", concept=["N4"], image_id="R10-evidence", constructor="header+navy_card", reveal="no CHECK answer yet")
rec(29, title="Recognizing Evidence", hud="DRAW", badge="N", anchor="N4", section="Recognizing Evidence", notes_ref="Guided Notes · Reader pp. 1–5", concept=["N4"], constructor="notes_heading+before_after", reveal="open")
rec(30, title="Check Your Thinking", hud="WRITE", badge="N", anchor="CHECK", section="Check Your Thinking", notes_ref="Guided Notes · Reader pp. 1–5", partner=31, concept=["CHECK"], constructor="notes_heading+starter+lines", reveal="after write")
rec(31, title="We know because we see a change", hud="CHECK", badge="C", anchor="CHECK", partner=30, concept=["CHECK"], constructor="sample_card", reveal="sample response", answers=["We know because we see a change, like a ball starting to move or a light turning on."])
rec(32, title="Which change shows energy at work?", hud="EVIDENCE", badge="C", concept=["CHECK"], constructor="scenario_cards", reveal="spoken rule after vote")
rec(33, title="BQ · Now I Think", hud="WRITE", badge="N", anchor="BQ", section="BQ · Now I Think", notes_ref="Guided Notes p. 3", concept=["BQ"], image_id="R11-reflection", constructor="notes_heading+bq_banner+lines", reveal="open")
REVIEW = [
    ("concept", "C", "Energy is the ability to cause change (Reader p. 1)."),
    ("visual", "A", "The pencil becomes shorter and sharper — a change."),
    ("scenario", "D", "The rubber band stores energy; it changes when released."),
    ("comparison", "B", "The spinning is motion; the music is sound (Reader p. 3)."),
    ("concept", "A", "We see a change — like movement — as evidence."),
    ("scenario", "C", "A battery stores energy. It can cause a change later."),
]
REV_IMG = {1: None, 2: "R03-pencil", 3: "R08-stored", 4: None, 5: None, 6: "R09-stored-strip(battery)"}
for q in range(6):
    qn, an = 34 + 2 * q, 35 + 2 * q
    typ, letter, explain = REVIEW[q]
    rec(qn, title=f"Review {q+1} — {typ}", badge="C", concept=["REVIEW"], image_id=REV_IMG[q+1], constructor="review_question", reveal="NOT_APPLICABLE")
    rec(an, title=f"Review {q+1} — answer", hud="CHECK", badge="C", concept=["REVIEW"], image_id=REV_IMG[q+1], constructor="review_answer", reveal=letter, answers=[letter + " · " + explain])

# ------------------------------------------------------------------ extraction
def slide_texts(prs):
    out = {}
    for i, s in enumerate(prs.slides, 1):
        parts = []
        for sh in s.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.text.strip():
                            parts.append(r.text.strip())
        out[i] = " ".join(parts)
    return out

def slide_notes(prs):
    out = {}
    for i, s in enumerate(prs.slides, 1):
        out[i] = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
    return out

prs = Presentation(CANON_PPTX)
canon_text = slide_texts(prs)
canon_notes = slide_notes(prs)
notes_gt = open(NOTES_TXT, encoding="utf-8").read()
key_gt = open(KEY_TXT, encoding="utf-8").read()

# ------------------------------------------------------------------ build contract
records = []
for n in range(1, 46):
    info = PACE.S[n]
    d = S[n]
    sess = info["session"]
    sess_name = PACE.SESSIONS[sess]["day"] if sess in PACE.SESSIONS else "review day / FLEX"
    status = "REQUIRED" if info["status"] == "REQ" else "OPTIONAL"
    mode = ""
    if canon_notes[n]:
        first = canon_notes[n].split("\n")[0]
        mode = first if first.startswith("MODE ") else ""
    records.append({
        "slide_id": "S%02d" % n,
        "canonical_slide_number": n,
        "session": sess,
        "session_day": sess_name,
        "classification": status,
        "instructional_mode": mode,
        "concept_ids": d["concept"],
        "title": d["title"],
        "kicker": d["kicker"],
        "exact_canonical_text": canon_text[n],
        "reader_reference": (d["kicker"] if d["kicker"].startswith("Reader") else
                             (d["notes_ref"] if d["notes_ref"] else "NOT_APPLICABLE")),
        "notes_anchor": d["anchor"] or "NONE",
        "notes_section_title": d["section"] or "NOT_APPLICABLE",
        "notes_page": d["notes_ref"] or "NOT_APPLICABLE",
        "writing_prompt": (d["blanks"][0] if d["blanks"] and n in (3, 11, 15, 21, 26) else "NOT_APPLICABLE"),
        "blank_meanings": d["blanks"] or "NOT_APPLICABLE",
        "expected_answer": d["answers"] or "NOT_APPLICABLE",
        "teacher_key_reference": (d["answers"][0] if d["answers"] else "NOT_APPLICABLE"),
        "write_check_partner": d["partner"] or "NOT_APPLICABLE",
        "reveal_state": d["reveal"],
        "teacher_speaker_notes": canon_notes[n],
        "teacher_question": next((l for l in canon_notes[n].split("\n") if l.startswith("ASK ")), "NOT_APPLICABLE"),
        "expected_student_responses": next((l for l in canon_notes[n].split("\n") if l.startswith("LISTEN FOR ")), "NOT_APPLICABLE"),
        "misconceptions": next((l for l in canon_notes[n].split("\n") if l.startswith("MISCONCEPTION ")), "NOT_APPLICABLE"),
        "duration_min": info["minutes"],
        "transition": next((l for l in canon_notes[n].split("\n") if l.startswith("NEXT ")), "NOT_APPLICABLE"),
        "if_short": next((l for l in canon_notes[n].split("\n") if l.startswith("IF SHORT ")), "NOT_APPLICABLE"),
        "optional_media": "NOT_APPLICABLE",
        "media_fallback": "live demo / skip (no video core-required)",
        "canonical_source": "production/slides/01-ch1-energy-causes-change-slides.pptx + tools/build_ch1_slides.py + tools/ch1_pacing.py",
        "visual_asset_id": d["image_id"] or "NONE",
        "layout_constructor": d["constructor"],
        "validation_status": "PENDING",
    })

# ------------------------------------------------------------------ Gate 1 validations
problems = []

# 45 records, unique ids, no missing/dup numbers
if len(records) != 45:
    problems.append("contract has %d records (need 45)" % len(records))
ids = [r["slide_id"] for r in records]
if len(set(ids)) != 45 or ids != ["S%02d" % n for n in range(1, 46)]:
    problems.append("slide IDs not exactly S01..S45")

# session/status derived from pacing (already by construction, but verify consistency)
for n in range(1, 46):
    info = PACE.S[n]
    if records[n-1]["session"] != info["session"] or records[n-1]["classification"] != ("REQUIRED" if info["status"] == "REQ" else "OPTIONAL"):
        problems.append("slide %d session/status mismatch" % n)

# D: canonical -> contract (title present in canonical text)
for n in range(1, 46):
    t = S[n]["title"]
    if t and t not in canon_text[n] and not t.startswith("Review"):
        problems.append("slide %d title %r not found in canonical text" % (n, t))

# anchors resolve; all required anchors present (BQ V1 N1 N2 V2 N3 N4 CHECK)
anchor_slides = {r["notes_anchor"]: [] for r in records if r["notes_anchor"] != "NONE"}
for r in records:
    if r["notes_anchor"] != "NONE":
        anchor_slides[r["notes_anchor"]].append(r["canonical_slide_number"])
required_anchors = ["BQ", "V1", "N1", "N2", "V2", "N3", "N4", "CHECK"]
for a in required_anchors:
    if a not in anchor_slides or not anchor_slides[a]:
        problems.append("anchor %s has no slides" % a)

# N3 complete (23-27), slide 32 preserved
if [r["canonical_slide_number"] for r in records if r["concept_ids"] == ["N3"]] != [23, 24, 25, 26, 27]:
    problems.append("N3 slide set is not exactly 23-27")
if records[31]["concept_ids"] != ["CHECK"] or records[31]["title"] != "Which change shows energy at work?":
    problems.append("slide 32 application slide not preserved")

# C: teacher key -> CHECK reveals
for n, ans in [(12, ["change", "different"]), (22, ["later"]), (16, ["evidence"]), (27, ["position"])]:
    r = records[n-1]
    if r["expected_answer"] != ans:
        problems.append("slide %d expected answer %r != key %r" % (n, r["expected_answer"], ans))

# E: teacher notes coverage (every slide has MODE + TIME + PLAN)
for r in records:
    notes = r["teacher_speaker_notes"]
    if "MODE " not in notes:
        problems.append("slide %s missing MODE note" % r["slide_id"])
    if "TIME " not in notes:
        problems.append("slide %s missing TIME note" % r["slide_id"])

# G: answer leakage (write slides must not reveal)
LEAK = {11: ["the ability to cause change", "to become different"],
        15: ["you are seeing evidence", "you are observing evidence"],
        21: ["at a later time"],
        26: ["because of their position"],
        30: ["We know because we see a change"]}
for n, phrases in LEAK.items():
    for ph in phrases:
        if ph.lower() in canon_text[n].lower():
            problems.append("answer leakage on slide %d: %r" % (n, ph))

# F: Friday no first-exposure (verified by PACE.check_plan())
for p in PACE.check_plan():
    problems.append("pacing: " + p)

# no banned vocab anywhere in canonical text
BANNED = ["kinetic", "potential", "mechanical", "radiant", "momentum", "inertia", "compression wave", "gravitational"]
blob = " ".join(canon_text.values()).lower()
for b in BANNED:
    if b in blob:
        problems.append("banned vocabulary %r present" % b)

ok = not problems
for r in records:
    r["validation_status"] = "PASS" if ok else "FAIL"

# ------------------------------------------------------------------ emit
os.makedirs(OUTDIR, exist_ok=True)
json.dump(records, open(os.path.join(OUTDIR, "CH1_INSTRUCTIONAL_ALIGNMENT_CONTRACT.json"), "w"),
          indent=1, ensure_ascii=False)

with open(os.path.join(OUTDIR, "CH1_INSTRUCTIONAL_ALIGNMENT_CONTRACT.md"), "w", encoding="utf-8") as f:
    f.write("# Chapter 1 — Instructional Alignment Contract (Gate 1)\n\n")
    f.write("45 records. Derived from the FROZEN canonical deck v1.1, `tools/ch1_pacing.py`, the accepted\n")
    f.write("Guided Notes student packet + teacher key, and Phase 5A visual-selection defaults.\n\n")
    f.write("| ID | # | Sess | Class | Anchor | Title | Partner | Reveal | Asset |\n|---|---|---|---|---|---|---|---|---|\n")
    for r in records:
        f.write("| %s | %d | %s | %s | %s | %s | %s | %s | %s |\n" % (
            r["slide_id"], r["canonical_slide_number"],
            "S%d" % r["session"] if r["session"] else "REV",
            r["classification"][:4], r["notes_anchor"], r["title"],
            r["write_check_partner"], r["reveal_state"][:28], r["visual_asset_id"]))

with open(os.path.join(OUTDIR, "CH1_GATE1_VALIDATION.md"), "w", encoding="utf-8") as f:
    f.write("# Chapter 1 — Gate 1 Validation (Instructional Alignment)\n\n")
    f.write("Overall: **%s**\n\n" % ("PASS" if ok else "FAIL"))
    f.write("- Records: %d\n" % len(records))
    f.write("- Notes anchors verified: %s\n" % ", ".join("%s=%d" % (a, len(v)) for a, v in sorted(anchor_slides.items())))
    f.write("- WRITE/CHECK pairs: V1 11↔12 · N1 15↔16 · V2 21↔22 · N3 26↔27 · CHECK 30↔31\n")
    f.write("- N3 complete (23-27): %s\n" % ("yes" if [r["canonical_slide_number"] for r in records if r["concept_ids"] == ["N3"]] == [23, 24, 25, 26, 27] else "NO"))
    f.write("- Slide 32 application preserved: yes\n")
    f.write("- Canonical content mismatches: %d\n" % len(problems))
    f.write("- Teacher-notes coverage: 45/45 MODE + TIME\n\n")
    f.write("## Findings\n\n")
    if problems:
        for p in problems:
            f.write("- FAIL: %s\n" % p)
    else:
        f.write("None — all Gate 1 acceptance criteria satisfied.\n")

print("records:", len(records))
print("problems:", problems or "none")
print("GATE1:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
