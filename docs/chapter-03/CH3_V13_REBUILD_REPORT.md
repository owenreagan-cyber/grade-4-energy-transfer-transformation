# CHAPTER 3 v1.3 PRODUCT REBUILD + INTERNAL AUDIT REPORT

## A. Baseline
- **HEAD at start:** `51f824a` (main)
- **Factory state:** all integrity blockers CLOSED (F-3…F-10 PASS)
- **Test baseline:** 233 passed
- **Frozen gate:** ALLOW (42 files)
- **New buildId:** `ch3-rebuild-v13-2026-10-07` (workspace not yet populated with
  evidence — certification is the next continuation)

## B. Blind Source Derivation
`docs/chapter-03/CH3_BLIND_SOURCE_DERIVATION.md` — derived independently from
Reader pp. 13–16 and TG Lessons 4–5. Required science, measured vs inferred
variables, fair-test controls, vocabulary, do-not-overteach, misconceptions,
assessment boundary, reasoning sequence, reading and lab needs.

## C. Spec Reconciliation
Fixed the spec to match the source derivation (not the reverse):
- N2 rewritten (ramp height cm + cup movement cm; no "infer the speed
  relationship"; TG Lesson 4 / AP 4.1 attribution).
- Reader p.15 steeper-ramp fact added to `concepts` and N3.
- `notesExpectation.blankCount` corrected 9 → 10.
- `revealSequence` N2 writes/reveals corrected (height, cup, height, same) and
  N3 (speed, greater).
- Quiz Q4 ("what did we measure in centimeters? name both") and Q7 (full
  question) de-vagued.

## D. Guided Notes
Regenerated via `tools/build_ch3_guided_notes.py` (tracked). 3 pages, anchors
BQ/V1/N1/N2/N3/N4/CHECK/BQ_NOW, 10 blanks, N2 names both measured quantities,
N3 teaches the p.15 fact as a blank ("Objects pick up more ____ on steeper
ramps", key fills "speed"). No "infer" wording. Key generated in parallel.

## E. Ramp It Up 2.0
Regenerated via `tools/build_ch3_handouts.py`. Added: QUESTION, PREDICT, fair-test
controls (same ball/ramp/release/let-go/cup/start/measuring), CHANGE/MEASURE,
calibration, a 6-column table with an **Average (cm)** column, a graph (axes
named, "do not label an axis as speed"), the 30 cm challenge, and guided
READ→COMPARE→NOTICE→CONNECT TO SPEED→CLAIM→EVIDENCE→REASONING→EXTEND. Key includes
expected claim, acceptable wording, evidence/reasoning expectations, misconception.

## F. Practice
Regenerated. Q1 names the evidence; Q2 "different ball" (removed heavy/light);
Q3 "measured … / figured out from that change" (removed "inferred"). Key updated.

## G. Quiz
Regenerated. 8 items / 12 points, score line `______ / 12 = ______ %`, Q4/Q7
de-vagued. Key and blueprint updated (no "inferred").

## H. Recovery
Regenerated. Added BIG IDEA, READ pp. 13–16, one direct question per major anchor,
missed-lab alternative (no fabricated data), Drop-It-not-required, quiz-makeup window.

## I. Friday FLEX
Drop It remains FLEX/optional (tag: "FLEX … Ramp It Up 2.0 is the only required
investigation"). Removed the "inferred" phrasing from the teacher-spec debrief.

## J. Playbook Region
Regenerated from the corrected spec (`CH3_PLAYBOOK_REGION.md`). The frozen
combined playbook was **not** edited.

## K. Slides
Regenerated via `tools/build_ch3_slides.py` (41 slides). Fixed S16/S17/S28
(removed "infer"), added the p.15 steeper-ramp fact (S30–S32, two blanks),
and replaced raw `BQ_NOW`/`RECOVER` chips with clean display labels (`BQ NOW`,
`RECOVER`, `DROP IT`) via a DISPLAY_LABELS map.

## L. Clean-Room Build
Tracked builders only (`build_ch3_guided_notes.py`, `build_ch3_slides.py`,
`build_ch3_handouts.py`). No `tools/ch3_*.py` participated. Output hashes not yet
recorded (clean-room closure/reproduction is part of certification, not yet run).

## M–R. Deterministic QA / Sensor / Blind Visual / Blind Science / Walk-through / Cross-Artifact Trace
**NOT RUN.** These are the blind-audit + certification steps and are the next
continuation. No blind visual or blind science review has been performed on the
rebuilt artifacts yet.

## S. Frozen Non-Regression
- Chapter 1: unchanged.
- Chapter 2: unchanged.
- Combined playbook: unchanged.
- Frozen gate: ALLOW (42 files, 0 mismatches) — verified before and after rebuild.

## T. Tests
- Total: 233 · Passed: 233 · Failed: 0 · Skipped: 0 (post-rebuild).

## U. Chapters 4–7 Preflight
`docs/preflight/unit1-chapters-04-07/UNIT1_CH4_7_PREFLIGHT.md` +
`docs/preflight/UNIT1_CH4_7_RISK_MATRIX.md`. Per-chapter derivation (title, BQ,
Reader/TG pages, vocabulary, facts, measured/inferred, misconceptions, demo/lab,
prompt/Friday risks, factory gaps) and a cross-chapter risk matrix.
**Production: NOT STARTED (read-only only).**

## V. Commits
- `e00fa15` — Rebuild Chapter 3 product under Grade 4 standards (v1.3).
- push: NONE · tag: NONE.

## W. Remaining Findings
- **BLOCKER:** none identified in the rebuild itself.
- **HIGH:** certification pipeline not yet run (blind visual, blind science,
  canaries, held-out mutations, Judge, lifecycle) — Chapter 3 is NOT yet
  internally certified.

## X. Final Decision

FACTORY v1.3 INTEGRITY:
**PASS**

CHAPTER 3 PRODUCT REBUILD:
**PASS (artifacts regenerated via tracked builders)** — but certification
pipeline NOT yet run.

CHAPTER 3 INTERNALLY CERTIFIED:
**NO**

READY FOR EXTERNAL RED-TEAM AUDIT:
**NO**

CHAPTERS 4–7 PREFLIGHT:
**COMPLETE (read-only; production not started)**

RELEASE PROPAGATED:
**NO**

FROZEN:
**NO**

PUSHED:
**NO**

---

**Status note:** the Chapter 3 classroom artifacts have been rebuilt to the
Grade 4 prompt/lab standards with the source corrections applied, and the
Chapters 4–7 read-only preflight is complete. The **blind-audit + certification
pipeline** (Parts IX–XIII, XV) is the next continuation and has not been run, so
Chapter 3 is not yet internally certified and not ready for external red-team
audit.
