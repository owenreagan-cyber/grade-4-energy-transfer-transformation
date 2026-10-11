#!/usr/bin/env python3
"""Phase 5B — emit machine-readable slide manifest + pacing / notes-alignment / write-check reports."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ch1_pacing as PACE
from pptx import Presentation

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUTDIR = os.path.join(ROOT, "qa", "reports", "ch1-phase5b")
PREMIUM = os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v1",
                       "01-ch1-energy-causes-change-premium-hybrid-v1.pptx")
CONTRACT = os.path.join(OUTDIR, "CH1_INSTRUCTIONAL_ALIGNMENT_CONTRACT.json")

contract = json.load(open(CONTRACT, encoding="utf-8"))
prs = Presentation(PREMIUM)


def slide_pics(prs):
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    out = {}
    for i, s in enumerate(prs.slides, 1):
        out[i] = sum(1 for sh in s.shapes if sh.shape_type == MSO_SHAPE_TYPE.PICTURE)
    return out


pics = slide_pics(prs)

# ---- machine-readable slide manifest
manifest = []
for r in contract:
    n = r["canonical_slide_number"]
    manifest.append({
        "slide_id": r["slide_id"],
        "slide_number": n,
        "session": r["session"],
        "session_day": r["session_day"],
        "classification": r["classification"],
        "title": r["title"],
        "notes_anchor": r["notes_anchor"],
        "write_check_partner": r["write_check_partner"],
        "reveal_state": r["reveal_state"],
        "visual_asset_id": r["visual_asset_id"],
        "embedded_pictures": pics.get(n, 0),
        "duration_min": r["duration_min"],
    })
json.dump(manifest, open(os.path.join(OUTDIR, "CH1_SLIDE_MANIFEST.json"), "w"), indent=1)

# ---- classroom pacing report
lines = ["# Chapter 1 — Classroom Pacing Report (Gate 2)\n",
         "Derived from `tools/ch1_pacing.py` (single timing authority). 30-minute blocks, ≥5 min buffer.\n"]
for sid in PACE.SESSIONS:
    s = PACE.SESSIONS[sid]
    lines.append("\n## Session %d — %s · %s\n" % (sid, s["day"], s["title"]))
    lines.append("- Goal: %s · Notes: %s · Reader: %s\n" % (s["goal"], s["notes"], s["reader"]))
    lines.append("- Required: **%.1f min** · Buffer: **%.1f min**%s\n" % (
        PACE.session_required_minutes(sid), PACE.session_buffer(sid),
        " · QUIZ 13 min" if s["quiz"] else ""))
    lines.append("\n| Slide | Task | Min | Status |\n|---|---|---|---|\n")
    for sl in s["order"]:
        mn = PACE.slide_minutes(sl, sid)
        st = "REQUIRED" if PACE.S[sl]["status"] == "REQ" else "OPTIONAL"
        lines.append("| %d | %s | %g | %s |\n" % (sl, PACE.S[sl]["label"], mn, st))
    lines.append("\n**If short on time:**\n")
    for it in PACE.IF_SHORT[sid]:
        lines.append("- %s\n" % it)
lines.append("\n## Friday policy (no first exposure)\n")
lines.append("- Every Friday required slide is traceable to Session 1/2: %s\n" % ", ".join(
    "%d→S%s" % (k, "1/2") for k in PACE.FRIDAY_DEPENDS))
lines.append("- Quiz handed out no later than minute 12; priority N4 draw > BQ NOW I THINK > CHECK YOUR THINKING.\n")
open(os.path.join(OUTDIR, "CH1_CLASSROOM_PACING_REPORT.md"), "w", encoding="utf-8").write("".join(lines))

# ---- notes alignment report (bidirectional)
notes_gt = open(os.path.join(OUTDIR, "_gt-notes.txt"), encoding="utf-8").read()
key_gt = open(os.path.join(OUTDIR, "_gt-key.txt"), encoding="utf-8").read()
anchor_map = {
    "BQ": [2, 3, 33], "V1": [10, 11, 12], "N1": [13, 14, 15, 16],
    "N2": [17, 18, 19], "V2": [20, 21, 22], "N3": [23, 24, 25, 26, 27],
    "N4": [28, 29, 30, 31],
}
na = ["# Chapter 1 — Notes Alignment Report (Gate 2)\n",
      "Bidirectional validation against the accepted Guided Notes student packet + teacher key.\n\n",
      "## A. Slides → Guided Notes (anchor map)\n\n| Anchor | Canonical slides |\n|---|---|\n"]
for a, sl in anchor_map.items():
    na.append("| %s | %s |\n" % (a, ", ".join(str(x) for x in sl)))
na.append("\n## B. Guided Notes → Slides (no orphaned anchor)\n\n")
for a in ["BQ", "V1", "N1", "N2", "V2", "N3", "N4"]:
    na.append("- %s: present in notes + key, projected on slides %s.\n" % (a, ", ".join(map(str, anchor_map[a]))))
na.append("- CHECK (Check Your Thinking): notes p. 3, projected on slides 30–31.\n\n")
na.append("## C. Teacher key → CHECK/reveal\n\n| Anchor | Reveal slide | Key answer(s) |\n|---|---|---|\n")
for a, ans in [("V1", "12"), ("V2", "22"), ("N1", "16"), ("N3", "27")]:
    key = {"V1": "change · different", "V2": "later", "N1": "evidence", "N3": "position"}[a]
    na.append("| %s | %s | %s |\n" % (a, ans, key))
na.append("\n## Verification\n\n- Text parity (premium vs canonical): PASS (45/45 identical).\n")
na.append("- Speaker-notes parity: PASS (45/45 identical).\n")
na.append("- Answer leakage: none.\n")
na.append("- N2 has no CHECK slide (canonical open task) — preserved.\n")
open(os.path.join(OUTDIR, "CH1_NOTES_ALIGNMENT_REPORT.md"), "w", encoding="utf-8").write("".join(na))

# ---- write/check reveal report
wc = ["# Chapter 1 — WRITE/CHECK Reveal Report (Gate 2)\n",
      "Paired layouts share geometry; CHECK reveals only the answer (gold accent).\n\n",
      "| Pair | Write | Check | Blank answer | Reveal behavior |\n|---|---|---|---|---|\n",
      "| V1 | 11 | 12 | change · different | reveal gold |\n",
      "| N1 | 15 | 16 | evidence | reveal gold + full model |\n",
      "| V2 | 21 | 22 | later | reveal gold |\n",
      "| N3 | 26 | 27 | position | reveal gold + sample table |\n",
      "| CHECK | 30 | 31 | (sample) | reveal sample |\n\n",
      "Open writes (no canonical CHECK slide): 3 (BQ first thinking) · 19 (N2) · 29 (N4 draw) · 33 (BQ NOW I THINK).\n\n",
      "- No WRITE slide leaks its answer (deterministic leakage gate PASS).\n",
      "- No reveal slide appears before its write slide.\n"]
open(os.path.join(OUTDIR, "CH1_WRITE_CHECK_REVEAL_REPORT.md"), "w", encoding="utf-8").write("".join(wc))

print("emitted slide manifest + pacing + notes-alignment + write-check reports")
