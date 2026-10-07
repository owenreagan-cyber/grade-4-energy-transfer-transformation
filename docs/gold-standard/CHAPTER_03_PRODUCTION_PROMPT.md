# Chapter 3 Production Prompt

Use this as the next Cursor prompt. Do not treat it as permission to skip the Chapter Factory.

```
cd /Users/owen/Projects/grade-4-energy-transfer-transformation

CHAPTER 3 PRODUCTION — CHAPTER FACTORY v1.0

You are producing Chapter 3 classroom artifacts through the accepted Chapter Factory.
Baseline: c637615afdc9dbcb157949e978dc250dad682534 and later acceptance commit.
Hard Cursor enforcement is active. Do not disable hooks. Do not bypass the Release Judge.
Do not modify frozen Chapter 1 or Chapter 2 classroom artifacts.
Do not configure MCP servers. MCP tooling is NONE and is not required.
Do not invent science, page numbers, dates, or vocabulary.

MAXIMUM 3 INTERNAL REMEDIATION LOOPS.
Each loop is: BUILD → seal evidence → render → deterministic QA → visual QA →
PDF/OOXML QA → adversarial mutations → provenance → independent review →
verify findings → fix only verified defects → invalidate stale evidence →
rerun the required gates.
Builder prose is not evidence. Do not assign PASS yourself. seal() and the
Release Judge set status.

==================================================
SOURCE — verified, do not replace with memory
==================================================

Title: Energy and Speed Are Related
Reader printed pages: 13–16
Reader file: assets/authoritative/student-reader/chapters/Chapter_3_Energy_and_Speed_Are_Related.pdf
Full Reader: assets/authoritative/student-reader/complete/Science 4 - Energy Transfer - Student Book.pdf
Teacher Guide: assets/authoritative/teacher-guide/Science 4 - Energy Transfer - TG .pdf
TG contents: Lesson 4 Investigating Energy and Speed, printed p. 33;
Lesson 5 Energy and Speed Are Related, printed p. 39.
Big Question, Reader p. 13 and TG Lessons 4 and 5: How are energy and speed related?
New Reader vocabulary: speed. Definition on p. 13: a measurement of the distance
an object travels over an amount of time.
TG Lesson 4 activities named in the guide: Ramp It Up (Day 1, AP 4.1) and
Drop It (Day 2, AP 4.2).
Re-read these files before writing the chapter spec. If a sentence is not in
them, do not teach it as required.

Science boundary from those pages:
- Compare the SAME object at different speeds.
- Greater speed of that object is related to greater energy of motion.
- The evidence is a greater observed change.
- Do not compare different masses.
- Do not require kinetic, potential, or mechanical energy.
- Do not claim students measured speed in m/s or measured an energy quantity.
- Assessment boundary in the TG: students are not required to quantitatively
  measure speed or energy. They compare observable changes.

==================================================
CALENDAR — dated authority
==================================================

docs/playbook/UNIT1_PACING_CALENDAR.md

Week 2: Mon 2026-10-19 through Fri 2026-10-23.
Mon 10/19: Chapter 3, Reader pp. 13–14.
Tue 10/20: Ramp It Up 2.0, day 1.
Wed 10/21: Ramp It Up 2.0, day 2, graph.
Thu 10/22: Chapter 3 synthesis, Reader pp. 15–16.
Fri 10/23: FLEX. Catch-up, review, completion, Big Question synthesis,
quiz or makeup, optional enrichment.

Friday is not the first exposure to essential new required content.
The Teacher Guide lists Drop It as Lesson 4 Day 2. The dated calendar lists
Drop It as Friday FLEX. The chapter spec must resolve that before any
artifact is built: required TG content is taught Monday–Thursday; Friday
does not introduce it for the first time. Do not invent a third calendar.

==================================================
RAMP IT UP 2.0 — locked investigation
==================================================

One investigation. Do not build a second ramp lab.
Same ball. Heights from 1, 2, and 3 books.
Measure the actual vertical ramp height in centimeters.
Measure target displacement in centimeters.
One unrecorded calibration trial.
Three measured trials at each height. Nine measured trials total.
Graph actual ramp height against average displacement.
No fake meters per second.
Do not claim ramp height is a measurement of speed.
Engineering challenge: move the target as close as possible to 30 cm
without going past.
Speed and the energy relationship are inferred from the measured change.

Chapter 3 must teach, before the flagship trials, the same-object rule,
what speed means, and that a greater change is the evidence of greater
energy of motion. Those ideas are on Reader pp. 13–14.

==================================================
ORDER
==================================================

1. Re-read the Reader and Teacher Guide.
2. Write the Chapter 3 chapter spec and run CHAPTER_SPEC until it PASSes.
   No DOCX and no PPTX before that PASS.
   The spec includes identity, title, Reader pages, TG pages, Big Question,
   required concepts, exclusions, vocabulary, BQ/V/N anchors, canonical note
   text, blank positions, answers, reveal sequence, speaker-note requirements,
   demo/activity/lab class, materials, session date, REQUIRED or OPTIONAL,
   timing, assessment scope, recovery, release inventory, Playbook region,
   and the Measurement/Data visual theme.
3. Independent source and curriculum review.
4. Guided Notes, then the key.
5. Notes structure evidence.
6. Slides and speaker notes. Do not build slides first.
7. Notes/slides sync.
8. Practice, the Ramp It Up investigation, and any other activity.
9. Assessment.
10. Recovery.
11. Playbook region for this chapter.
12. Render at 300 DPI. Suspicious regions at 600 DPI.
13. Deterministic QA, visual QA, PDF quality, OOXML.
14. Adversarial QA, including held-out cases. Project bad green 0,
    held-out bad green 0, clean red 0, canonical tree untouched.
15. Provenance and clean-room reproduction.
16. Release Judge.
17. Internal certification only if the Judge returns PASS and the stop hook
    allows the claim.
18. Stop at external-audit readiness. Do not freeze. Do not pretend an
    external audit happened.

==================================================
VISUALS
==================================================

Use the existing Chapter 3 theme: Measurement / Data.
Palette already in assets/visual-system/chapter-themes/ch3-palette.svg:
cobalt #1B4FC2, chartreuse #5E8A18, charcoal #2B2F36, light gray #E9EBEF.
Do not redesign the unit visual system.
Show same-object speed comparison, measured data, a fair test, and the
ramp investigation. Do not draw fake speed values.

==================================================
GATES
==================================================

All mandatory gates in qa/gold-standard/gates.json apply.
Evidence comes only from the registered producer for that gate.
Do not write a filler PASS. Do not mark a mandatory gate optional.
A missing producer is a FAIL.
After any edit, stale evidence cannot be reused.
Hooks stay on. git add is allowed only for an explicit authorized path list.
No git add . and no git add -A.

==================================================
STOP
==================================================

Stop when the Release Judge PASSes and the stop hook allows
INTERNALLY_CERTIFIED for this build, or when three remediation loops
are exhausted. Then the next step is one external red-team audit, not a freeze.
If the external audit finds a factory defect, fix the factory, not only
a Chapter 3 string.
```
