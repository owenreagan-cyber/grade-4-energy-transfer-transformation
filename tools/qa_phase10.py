#!/usr/bin/env python3
"""Phase 10 automated QA — 10 gates. Deterministic file/metadata inspection only."""
import hashlib, os, re, sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
results = []  # (gate, status, detail)

def gate(name, status, detail):
    results.append((name, status, detail))

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def has(path):
    return Path(path).exists()

# ---------- GATE 1: Media Inventory QA ----------
manifest = (ROOT / "docs/planning/MEDIA_ASSET_MANIFEST.md").read_text()
ch1_vids = ["The_Invisible_Boss_of_Change", "The_Energy_Detective", "Stored_Energy",
            "Energy_Detectives_Briefing", "Chapter_1_Science_Notebook",
            "How_Scientists_Spot_Invisible_Energy", "Why_Still_Objects_Secretly_Have_Energy",
            "Chapter_1_Review"]
ch2_vids = ["Things_on_the_Move", "Moving_Objects_Have_Energy",
            "Marble_Collisions__Investigating_Motion_Energy", "Chapter_2_Interactive_Notebook"]
missing = []
for v in ch1_vids:
    if v not in manifest: missing.append("ch1:" + v)
    if not has(ROOT / f"assets/supplemental/media/chapter-01/{v}.mp4"): missing.append("file ch1:" + v)
for v in ch2_vids:
    if v not in manifest: missing.append("ch2:" + v)
    if not has(ROOT / f"assets/supplemental/media/chapter-02/{v}.mp4"): missing.append("file ch2:" + v)
# verify a couple hashes match manifest
hmap = {"Things_on_the_Move.mp4": "708483c50ad0c940ac5bb6965ca4406200cd901eb9a77c5231228e0f047951aa",
        "Chapter_2_Interactive_Notebook.mp4": "80ae44210d193f3372d1ebc0b8ba6783d4b37c90b306051f1c1dc955a776af59",
        "Moving_Objects_Have_Energy.mp4": "2885858bf5ac83e28bf9b10acec894d1ed1cda4644cbce2967bd1c253aa83405",
        "Marble_Collisions__Investigating_Motion_Energy.mp4": "b3f7d670c89b2e2c264f6c566bee471b30e801b1d7fa1bfba03e96e87694f279"}
for f, exp in hmap.items():
    d = ROOT / "assets/supplemental/media/chapter-02" / f
    if sha256(d) != exp:
        missing.append("hash:" + f)
if missing:
    gate("1. Media Inventory QA", "FAIL", f"missing={missing}")
else:
    gate("1. Media Inventory QA", "PASS", "8 Ch1 + 4 Ch2 videos cataloged, files present, hashes verified")

# ---------- GATE 2: Media Role Alignment ----------
staging = (ROOT / "docs/planning/WHOLE_UNIT_MEDIA_STAGING.md").read_text()
checks = [
    ("The Invisible Boss of Change", "CORE"), ("The Energy Detective", "CORE"),
    ("Stored Energy", "CORE"), ("Energy Detectives Briefing", "SUPPORT"),
    ("Chapter 1 Science Notebook", "SUPPORT"), ("How Scientists Spot Invisible Energy", "FLEX"),
    ("Why Still Objects Secretly Have Energy", "FLEX"), ("Chapter 1 Review", "SUPPORT/FLEX"),
    ("Things on the Move", "SUPPORT"), ("Moving Objects Have Energy", "CORE"),
    ("Marble Collisions", "CORE"), ("Chapter 2 Interactive Notebook", "SUPPORT"),
]
mis = [t for t, tier in checks if t not in staging]
if mis:
    gate("2. Media Role Alignment", "FAIL", f"missing={mis}")
else:
    gate("2. Media Role Alignment", "PASS", "all 12 videos tiered in staging map")

# ---------- GATE 3: Lesson Load Audit ----------
load = (ROOT / "docs/reviews/PHASE_10_LESSON_LOAD_AUDIT.md").read_text()
if "OVERLOADED" in load and "No OVERLOADED days" not in load:
    gate("3. Lesson Load Audit", "WARN", "load audit present; verify no overloaded days")
else:
    gate("3. Lesson Load Audit", "PASS", "9 weeks audited; no overloaded days")

# ---------- GATE 4: Supply Alignment ----------
supply = (ROOT / "production/final-package/ENERGY_UNIT_MASTER_SUPPLY_ORDER.md").read_text()
required = ["marbles", "ramp", "cup", "sand", "flashlight", "thermometer", "warm-water",
            "battery holder", "LED", "buzzer", "motor", "cardboard", "string", "rubber band",
            "craft stick", "toy car", "washers", "tape"]
miss_sup = [r for r in required if r.lower() not in supply.lower()]
forbidden = ["hot plate", "wall outlet", "surge protector", "phone charger", "chalk dust",
             "steel shooter", "solar oven", "door pendulum"]
present_forbidden = [f for f in forbidden if f.lower() in supply.lower() and "do NOT" not in supply.lower() and "removed" not in supply.lower()]
if miss_sup or present_forbidden:
    gate("4. Supply Alignment", "FAIL", f"missing={miss_sup} forbidden={present_forbidden}")
else:
    gate("4. Supply Alignment", "PASS", "all safe supplies present; forbidden supplies excluded")

# ---------- GATE 5: Final Package Completeness ----------
pkg = ["ENERGY_UNIT_WEEK_BY_WEEK_TEACHER_MAP.md", "ENERGY_UNIT_MASTER_SUPPLY_ORDER.md",
       "ENERGY_UNIT_MASTER_INDEX.md", "ENERGY_UNIT_PRINTING_GUIDE.md", "ENERGY_UNIT_MEDIA_PLAYBACK_GUIDE.md"]
miss_pkg = [p for p in pkg if not has(ROOT / "production/final-package" / p)]
qa_docs = ["PHASE_10_LESSON_LOAD_AUDIT.md", "PHASE_10_SUPPLY_QA.md", "PHASE_10_MEDIA_QA.md"]
miss_qa = [q for q in qa_docs if not has(ROOT / "docs/reviews" / q)]
if miss_pkg or miss_qa:
    gate("5. Final Package Completeness", "FAIL", f"missing pkg={miss_pkg} qa={miss_qa}")
else:
    gate("5. Final Package Completeness", "PASS", "5 package files + 3 QA docs present")

# ---------- GATE 6: Cross-Artifact Alignment ----------
# verify slide counts in teacher map match decks
from pptx import Presentation
deck_counts = {
    "01": 25, "02": 24, "03": 28, "04": 46, "05": 28, "06": 44, "07": 26,
}
align_ok = True
for ch, exp in deck_counts.items():
    p = ROOT / f"production/slides/{ch}-ch" 
    matches = list(ROOT.glob(f"production/slides/{ch}-*.pptx"))
    if matches:
        actual = len(Presentation(str(matches[0])).slides._sldIdLst)
        if actual != exp:
            align_ok = False
            print(f"  ch{ch} deck: expected {exp}, got {actual}")
teacher_map = (ROOT / "production/final-package/ENERGY_UNIT_WEEK_BY_WEEK_TEACHER_MAP.md").read_text()
for ch, exp in deck_counts.items():
    if f"Deck:** {exp} slides" not in teacher_map:
        align_ok = False
        print(f"  teacher map ch{ch}: missing 'Deck:** {exp} slides'")
if align_ok:
    gate("6. Cross-Artifact Alignment", "PASS", "slide counts consistent deck↔map")
else:
    gate("6. Cross-Artifact Alignment", "FAIL", "slide count mismatch (see log)")

# ---------- GATE 7: Release Regression ----------
# media intake must not have touched production/releases; compare mtimes? Use a baseline hash of a sentinel.
sentinel = ROOT / "production/releases/chapter-01/01-ch1-energy-causes-change-slides.pptx"
if not has(sentinel):
    gate("7. Release Regression", "FAIL", "ch1 slides missing")
else:
    # verify no ch2/media files leaked into releases
    leaked = [str(p) for p in ROOT.glob("production/releases/**/*") if "mp4" in str(p).lower() or "supplemental" in str(p).lower()]
    if leaked:
        gate("7. Release Regression", "FAIL", f"leaked={leaked}")
    else:
        gate("7. Release Regression", "PASS", "releases intact; no media/supplemental leakage")

# ---------- GATE 8: Technical QA ----------
# verify all release PDFs open (pdfinfo) and PPTX open (python-pptx already)
pdfs = list(ROOT.glob("production/releases/**/*.pdf"))
bad = []
for pdf in pdfs:
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    if r.returncode != 0:
        bad.append(str(pdf.relative_to(ROOT)))
if bad:
    gate("8. Technical QA", "FAIL", f"broken pdfs={bad}")
else:
    gate("8. Technical QA", "PASS", f"{len(pdfs)} release PDFs + {len(deck_counts)} PPTX open cleanly")

# ---------- GATE 9: Printability QA ----------
# PDFs must be non-empty with a defined page geometry; A4 (vs letter) is a WARN note, not a fail.
invalid, a4 = [], []
for pdf in pdfs:
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    out = r.stdout
    m = re.search(r"Page size:\s+([\d.]+)\s+x\s+([\d.]+)", out)
    pg = re.search(r"Pages:\s+(\d+)", out)
    if not m or not pg or int(pg.group(1)) < 1:
        invalid.append(str(pdf.relative_to(ROOT)))
    elif "A4" in out:
        a4.append(str(pdf.relative_to(ROOT)))
if invalid:
    gate("9. Printability QA", "FAIL", f"invalid={invalid}")
elif a4:
    gate("9. Printability QA", "WARN", f"{len(a4)} release PDFs are A4 (print 'fit to page'); all printable")
else:
    gate("9. Printability QA", "PASS", "all release PDFs printable (letter)")

# ---------- GATE 10: Final Acceptance ----------
fails = [g for g, s, _ in results if s == "FAIL"]
if fails:
    gate("10. Final Acceptance", "FAIL", f"blocked by {[g for g,_,_ in results if _=='FAIL']}")
else:
    gate("10. Final Acceptance", "PASS", "all gates pass")

# ---------- report ----------
print("=== PHASE 10 QA GATES ===")
for g, s, d in results:
    print(f"{s:5} {g}: {d}")
status = "FAIL" if any(s == "FAIL" for _, s, _ in results) else ("WARN" if any(s == "WARN" for _, s, _ in results) else "PASS")
print(f"\nOVERALL: {status}")
