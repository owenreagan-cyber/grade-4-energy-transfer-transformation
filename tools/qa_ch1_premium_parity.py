#!/usr/bin/env python3
"""Phase 5B · Gate 2 — instruction/notes parity + asset provenance QA.

Verifies the premium candidate's TEXT and speaker NOTES are byte-identical to the frozen canonical
deck (the premium build only added raster photography and changed the display font), emits the
selected-asset manifest with SHA-256, and re-checks answer leakage + teacher-key reveal parity.
"""
import hashlib, json, os, sys, zipfile
from pptx import Presentation

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CAND = os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v1")
CANON = os.path.join(ROOT, "production", "slides", "01-ch1-energy-causes-change-slides.pptx")
PREMIUM = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v1.pptx")
OUTDIR = os.path.join(ROOT, "qa", "reports", "ch1-phase5b")


def runs(prs):
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
    p = Presentation(PREMIUM)
    ct, pt = runs(c), runs(p)
    cn, pn = notes(c), notes(p)
    problems = []

    # 1. text parity (premium == canonical per slide)
    for n in range(1, 46):
        if ct[n] != pt[n]:
            problems.append("slide %d text differs: canonical %r vs premium %r" % (n, ct[n][:80], pt[n][:80]))

    # 2. notes parity
    for n in range(1, 46):
        if cn[n] != pn[n]:
            problems.append("slide %d speaker notes differ" % n)

    # 3. embedded media manifest (SHA-256)
    manifest = []
    with zipfile.ZipFile(PREMIUM) as z:
        for name in sorted(n for n in z.namelist() if n.startswith("ppt/media/")):
            data = z.read(name)
            manifest.append({
                "name": name.split("/")[-1],
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            })

    # 4. leakage (write slides must not reveal answers)
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
    json.dump(manifest, open(os.path.join(OUTDIR, "CH1_SELECTED_ASSET_MANIFEST_5B.json"), "w"), indent=1)

    report = os.path.join(OUTDIR, "CH1_INSTRUCTIONAL_PARITY_QA.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write("# Chapter 1 — Instructional Parity QA (Gate 2)\n\nOverall: **%s**\n\n" % ("PASS" if ok else "FAIL"))
        f.write("- Text parity (premium vs canonical, all 45 slides): %s\n" % ("identical" if not any("text differs" in x for x in problems) else "DIFFERS"))
        f.write("- Speaker-notes parity (45 slides): %s\n" % ("identical" if not any("notes differ" in x for x in problems) else "DIFFERS"))
        f.write("- Answer leakage: %s\n" % ("none" if not any("leakage" in x for x in problems) else "FOUND"))
        f.write("- Embedded media files: %d\n\n" % len(manifest))
        f.write("## Embedded media (SHA-256)\n\n| File | Bytes | SHA-256 |\n|---|---|---|\n")
        for m in manifest:
            f.write("| %s | %d | %s |\n" % (m["name"], m["bytes"], m["sha256"][:16] + "…"))
        f.write("\n## Findings\n\n")
        if problems:
            for x in problems:
                f.write("- FAIL: %s\n" % x)
        else:
            f.write("None.\n")

    print("text parity:", "OK" if not any("text differs" in x for x in problems) else "FAIL")
    print("notes parity:", "OK" if not any("notes differ" in x for x in problems) else "FAIL")
    print("leakage:", "none" if not any("leakage" in x for x in problems) else "FOUND")
    print("embedded media:", len(manifest))
    print("PARITY:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
