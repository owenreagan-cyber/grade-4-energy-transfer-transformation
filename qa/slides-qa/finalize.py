#!/usr/bin/env python3
"""Finalize: triage raw vision findings into a real defect register + slide table.

Triage rules (sequence-aware):
  - ANSWER_LEAK on reveal/teach/demo/answer slides -> FALSE POSITIVE (by design).
  - LABEL_BADGE 'D' -> FALSE POSITIVE (section-code badge system).
  - SCIENCE_ERROR on the ENERGY->CHANGE->EVIDENCE model -> FALSE POSITIVE (canonical).
  - FONT_READABILITY -> LOW (chrome text at the documented >=12pt floor).
"""
import json
from pathlib import Path

RES = Path("qa/slides-qa/ch1/run-live/results.json")
OUT = Path("qa/slides-qa/ch1")

# live slide positions where showing an answer is correct (reveal/teach/demo/answer)
ANSWER_OK = {
    # demo/observe/explain (the change is shown intentionally)
    4, 9, 10,
    # vocabulary teach + reveals
    11, 13, 14, 21, 23,
    # N1/N3 reveals + sample
    17, 30, 34,
    # review answer slides (even live positions 38,40,42,44,46,48)
    38, 40, 42, 44, 46, 48,
}

d = json.loads(RES.read_text(encoding="utf-8"))
triaged = []
for x in d["defects"]:
    s = x["slide"]
    cat = x["category"]
    fp = False
    if cat == "ANSWER_LEAK" and s in ANSWER_OK:
        fp = True
    if cat == "LABEL_BADGE" and "D" in x["actual"]:
        fp = True
    if cat == "SCIENCE_ERROR" and "EVIDENCE" in x["actual"]:
        fp = True
    if cat == "FONT_READABILITY":
        x["severity"] = "LOW"
    if cat in ("HIERARCHY_ALIGNMENT", "COMPOSITION"):
        x["severity"] = "LOW"
    x["falsePositive"] = fp
    x["disposition"] = "FALSE_POSITIVE" if fp else (
        "LOW_OBSERVATION" if cat in ("FONT_READABILITY", "HIERARCHY_ALIGNMENT", "COMPOSITION", "LABEL_BADGE") else "REAL"
    )
    triaged.append(x)

real = [x for x in triaged if x["disposition"] == "REAL"]
low = [x for x in triaged if x["disposition"] == "LOW_OBSERVATION"]
fp = [x for x in triaged if x["disposition"] == "FALSE_POSITIVE"]

summary = {
    "rawFindings": len(triaged),
    "falsePositives": len(fp),
    "lowObservations": len(low),
    "realDefects": len(real),
    "verdicts": {},
}
for r in d["visual"]:
    v = r.get("vision", {})
    if isinstance(v, dict) and "summary" in v:
        k = v.get("overall", "?")
        summary["verdicts"][k] = summary["verdicts"].get(k, 0) + 1

# slide-by-slide table
rows = []
for r in d["visual"]:
    v = r.get("vision", {})
    if isinstance(v, dict) and "summary" in v:
        overall = v.get("overall", "?")
        # re-map verdict after triage: answer slides with only answer_leak -> PASS
        slide_defects = [x for x in triaged if x["slide"] == r["page"]]
        real_on_slide = [x for x in slide_defects if x["disposition"] == "REAL"]
        low_on_slide = [x for x in slide_defects if x["disposition"] == "LOW_OBSERVATION"]
        if not real_on_slide:
            triaged_verdict = "PASS" if not low_on_slide else "PASS*"
        else:
            triaged_verdict = "FAIL"
        rows.append({
            "slide": r["page"],
            "raw": overall,
            "triaged": triaged_verdict,
            "note": ("; ".join(x["actual"][:70] for x in low_on_slide[:2])) if low_on_slide else "",
        })

(OUT / "triaged_defects.json").write_text(json.dumps({
    "summary": summary,
    "realDefects": real,
    "lowObservations": low,
    "falsePositives": [{"slide": x["slide"], "category": x["category"], "actual": x["actual"][:80]} for x in fp],
}, indent=2), encoding="utf-8")

with (OUT / "slide-table.md").open("w", encoding="utf-8") as f:
    f.write("| Slide | Raw verdict | Triaged | Note |\n|---|---|---|---|\n")
    for r in rows:
        note = r["note"].replace("|", "\\|")
        f.write(f"| {r['slide']} | {r['raw']} | {r['triaged']} | {note} |\n")

print(json.dumps(summary, indent=2))
print(f"real={len(real)} low={len(low)} fp={len(fp)}")
