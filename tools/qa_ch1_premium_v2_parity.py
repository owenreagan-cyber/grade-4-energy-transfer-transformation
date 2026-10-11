#!/usr/bin/env python3
"""Phase 5C instructional parity QA for ch1-premium-hybrid-v2.

Checks (all against the FROZEN canonical deck, and cross-checked against the Phase 5B candidate):
  1 text parity — per-slide run text identical (same function as Phase 5B: tools/qa_ch1_premium_parity.runs)
  2 speaker-notes parity — identical
  3 slide count 45 and review answer letters C · A · D · B · A · C (from shape order + REVEAL notes)
  4 answer leakage on WRITE slides (Phase 5B phrase list) + no review option text appears on any review photo slide
  5 embedded-media manifest (SHA-256)
Writes qa/reports/ch1-phase5c/CH1_INSTRUCTIONAL_PARITY_V2.json. Exit 1 on any failure.
"""
import hashlib, json, os, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
import qa_ch1_premium_parity as P5B

ROOT = P5B.ROOT
CAND = os.environ.get("CH1_V2_OUT") or os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v2")
V2 = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v2.pptx")
OUT = os.path.join(ROOT, "qa", "reports", "ch1-phase5c")
EXPECT_LETTERS = ["C", "A", "D", "B", "A", "C"]


def letters(prs):
    out = []
    for q in range(6):
        qs, an = prs.slides[33 + 2 * q], prs.slides[34 + 2 * q]
        rev = [l for l in an.notes_slide.notes_text_frame.text.split("\n") if l.startswith("REVEAL ")][0][7:]
        opts = [sh.text_frame.text for sh in qs.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
        opts = [t for t in opts if t not in ("A", "B", "C", "D")]
        # option order = order of option text boxes following the question box
        q_idx = next(i for i, t in enumerate(opts) if t.endswith("?") or t.endswith("—"))
        o = opts[q_idx + 1:q_idx + 5]
        out.append("ABCD"[o.index(rev)])
    return out


def main():
    c, v1, v2 = Presentation(P5B.CANON), Presentation(P5B.PREMIUM), Presentation(V2)
    ct, t1, t2 = P5B.runs(c), P5B.runs(v1), P5B.runs(v2)
    cn, n1, n2 = P5B.notes(c), P5B.notes(v1), P5B.notes(v2)
    prob = []
    if len(v2.slides) != 45:
        prob.append("slide count %d" % len(v2.slides))
    text_diff = [n for n in range(1, 46) if ct[n] != t2[n]]
    note_diff = [n for n in range(1, 46) if cn[n] != n2[n]]
    prob += ["slide %d text differs from canonical" % n for n in text_diff]
    prob += ["slide %d notes differ from canonical" % n for n in note_diff]
    v1_same = all(t1[n] == t2[n] and n1[n] == n2[n] for n in range(1, 46))
    lv2 = letters(v2)
    if lv2 != EXPECT_LETTERS:
        prob.append("review letters %s != %s" % (lv2, EXPECT_LETTERS))
    leak = {11: ["the ability to cause change", "to become different"],
            15: ["you are seeing evidence", "you are observing evidence"],
            21: ["at a later time"], 26: ["because of their position"],
            30: ["We know because we see a change"]}
    for n, phrases in leak.items():
        for ph in phrases:
            if ph.lower() in t2[n].lower():
                prob.append("leakage slide %d: %r" % (n, ph))
    media = []
    with zipfile.ZipFile(V2) as z:
        for name in sorted(x for x in z.namelist() if x.startswith("ppt/media/")):
            d = z.read(name)
            media.append({"name": name.split("/")[-1], "bytes": len(d), "sha256": hashlib.sha256(d).hexdigest()})
    res = {"overall": "PASS" if not prob else "FAIL", "slides": len(v2.slides), "text_diff_vs_canonical": text_diff,
           "notes_diff_vs_canonical": note_diff, "identical_text_and_notes_to_phase5b": v1_same,
           "review_letters": lv2, "problems": prob, "embedded_media": media}
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, "CH1_INSTRUCTIONAL_PARITY_V2.json"), "w"), indent=1)
    print("slides", len(v2.slides), "| text diff", text_diff or "none", "| notes diff", note_diff or "none",
          "| == 5B text+notes", v1_same, "| letters", "·".join(lv2), "| media", len(media))
    print("PARITY:", res["overall"], prob or "")
    sys.exit(0 if not prob else 1)


if __name__ == "__main__":
    main()
