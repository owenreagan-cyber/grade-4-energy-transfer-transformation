#!/usr/bin/env python3
"""Phase 5H — instruction/text parity + notes parity (with delineated media allowance) + leakage.

Text runs must be byte-identical to canonical (the movie shape adds no text). Speaker notes must
have canonical text as a PREFIX; only slide 25 may carry a clearly-delineated supplemental media
block. Re-verifies no answer leakage and review letters.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CANON = os.path.join(ROOT, "production", "slides", "01-ch1-energy-causes-change-slides.pptx")
CAND = os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v6-embedded-media",
                    "01-ch1-energy-causes-change-premium-hybrid-v6-embedded-media.pptx")
OUTDIR = os.path.join(ROOT, "qa", "reports", "ch1-phase5g")

MEDIA_MARKER = "MEDIA (Phase 5H supplemental"


def textruns(prs):
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


def notes(prs):
    return {i: s.notes_slide.notes_text_frame.text for i, s in enumerate(prs.slides, 1)}


def main():
    c = Presentation(CANON)
    p = Presentation(CAND)
    ct, pt = textruns(c), textruns(p)
    cn, pn = notes(c), notes(p)
    problems = []

    # text parity (movie shape contributes no text)
    for n in range(1, 46):
        if ct[n] != pt[n]:
            problems.append("slide %d text differs" % n)

    # notes parity: canonical must be a prefix; only slide 25 may add the media block
    for n in range(1, 46):
        if not pn[n].startswith(cn[n]):
            problems.append("slide %d canonical notes not preserved as prefix" % n)
        extra = pn[n][len(cn[n]):].strip()
        if extra:
            if n != 25 or MEDIA_MARKER not in extra:
                problems.append("slide %d has unexpected note addition: %r" % (n, extra[:60]))

    # slide 25 must carry the media block
    if MEDIA_MARKER not in pn[25]:
        problems.append("slide 25 missing delineated media note")

    # leakage (unchanged canonical content)
    leak = {11: ["the ability to cause change", "to become different"],
            15: ["you are seeing evidence", "you are observing evidence"],
            21: ["at a later time"],
            26: ["because of their position"],
            30: ["We know because we see a change"]}
    for n, phrases in leak.items():
        for ph in phrases:
            if ph.lower() in pt[n].lower():
                problems.append("leakage slide %d: %r" % (n, ph))

    ok = not problems
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "CH1_INSTRUCTIONAL_PARITY_5H.md"), "w") as f:
        f.write("# Chapter 1 — Instructional Parity Report (Phase 5H)\n\nOverall: **%s**\n\n" % ("PASS" if ok else "FAIL"))
        f.write("- Text parity vs canonical (45 slides): %s\n" % ("identical" if not any("text differs" in x for x in problems) else "DIFFERS"))
        f.write("- Speaker-notes parity (canonical prefix preserved): %s\n" % ("yes" if not any("notes not preserved" in x for x in problems) else "NO"))
        f.write("- Slide 25 delineated media note: %s\n" % ("present" if MEDIA_MARKER in pn[25] else "MISSING"))
        f.write("- Answer leakage: %s\n\n" % ("none" if not any("leakage" in x for x in problems) else "FOUND"))
        if problems:
            for x in problems:
                f.write("- FAIL: %s\n" % x)
        else:
            f.write("None.\n")
    for x in problems:
        print("FAIL", x)
    print("PARITY:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
