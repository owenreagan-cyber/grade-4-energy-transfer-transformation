# BUILD PROMPT — Chapter 4 Guided Notes (Teacher Key)

> Standalone production prompt. Companion to `CH04_GUIDED_NOTES_STUDENT_BUILD_PROMPT.md`. A build agent must be able to produce this key from **this file alone** plus the student notes file.

---

## 1. Mission

Produce the **teacher key** for the Chapter 4 Guided Notes. It is a page-for-page, blank-for-blank mirror of the student notes with answers filled into the student geometry. **Chapter 4 is about ENERGY TRANSFER only — the key must not introduce transformation/BOTH.**

## 2. Exact resource name

`04-ch4-energy-transfer-guided-notes-key` — **Chapter 4: Energy Transfer — Guided Notes Key (Teacher)**

## 3. Audience

Teacher only. Never handed to students.

## 4. Required / optional status

**REQUIRED · CORE · teacher-only**. Ships in the teacher bundle / combined teacher key, not on any student page.

## 5. Instructional purpose

Give the teacher the exact expected fill for every blank, acceptable alternatives, and — concisely — one major misconception per section and the source page, so grading/checking is instant and consistent.

## 6. Source authority (order is authoritative — do not invert)

1. **Authoritative CKSci Student Reader** (Ch4, printed pp. 17–24 / PDF pp. 23–30).
2. **Authoritative CKSci Teacher Guide** (L6–9, TG pp. 46–63).
3. **Current accepted pacing** (`docs/playbook/UNIT1_PACING_CALENDAR.md`; `curriculum/chapter-04/source-map.md`).
4. **Current Guided Notes architecture** (`docs/standards/GUIDED_NOTES_STANDARD.md`; `CH1_GOLD_STANDARD_PROPAGATION_SPEC.md` §B).
5. **Slides after re-sync** (not yet authoritative).
6. **Assessment blueprint** (`docs/assessment/UNIT1_FINAL_ASSESSMENT_BLUEPRINT.md` — Q1, Q13, Q17, Q25).

> **RULING:** the assessment blueprint is a **traceability check, not curriculum authority.** If it conflicts with Reader/TG or pacing, fix or flag the blueprint — do not distort the curriculum to satisfy the assessment. The key's correctness is bounded by the Reader/TG/AP, not by the builder's inference.

## 7. Required content — the answer set

Mirror the student anchor set exactly (BQ · V1 · N1–N4 · CHECK · BQ·NOW I THINK). Representative answers:

- **V1 — energy transfer:** "movement of energy from one object to another or from one place to another." **V1 — sound:** "a form of energy that comes from a vibrating object."
- **N1 model:** ENERGY → MOVES → TARGET CHANGES → EVIDENCE. Evidence line: "the target changed (moved, lit up, got warmer, turned on)."
- **N2 sound evidence:** "the paper moved when the cup was tapped." **N2 light evidence:** "the card lit up / the light reached the target."
- **N3 heat evidence:** "the cooler object got warmer; the thermometer reading went up." **N3 electric-current evidence:** "the bulb/buzzer/motor turned on."
- **N4 organizer (sample rows):** sound — source: tapped cup · receiver: paper · what changed: paper moved · evidence: the paper moved because sound reached it. (Student wording may vary.)
- **CHECK / BQ·NOW I THINK:** sample responses with "Sample answer — student wording may vary."

## 8. Explicit exclusions

Same locked boundaries as the student prompt. The key must **not** introduce: transformation/BOTH classification (Ch6), compression-wave/particle-level sound, electron flow, conduction/convection/radiation as required, kinetic/potential/mechanical/radiant vocabulary, Ch5 collisions or Ch6 engineering as required. The key never appears on a student page.

## 9. Page count target

Identical to the student file (target 4 pages, same page order, same geometry). The key must never drift to a different page count than the student notes.

## 10–17. Layout, margins, typography, spacing, handwriting, tables, header, page-by-page

Inherit the student file's layout **exactly** (US Letter portrait; margins 0.50–0.55 in; typography hierarchy identical; same tables/diagrams/geometry; same page breaks; same line placement).

**Geometry parity rule (locked):** the teacher key must preserve the student page geometry exactly wherever possible — page count, section positions, tables, diagrams, writing boxes, **Name/Homeroom header geometry**, anchor positions, page breaks, margins, line placement. **Do NOT reflow the page.** Do NOT remove or simplify the Name/Homeroom line. Add a small, non-reflowing `TEACHER KEY` badge in a fixed corner/header position only.

## 18. Key architecture / answer treatment

- Answer color: **gold or dark blue**, bold; no red by default.
- Small `ANSWER` / `SAMPLE` label near each fill.
- Fill answers **into** the student blank geometry (do not re-typeset the page).
- Open responses carry: `Sample answer — student wording may vary.` + acceptable alternatives.

**Commentary limit (locked):** keep teacher-only notes concise — expected answer, acceptable variants, one major misconception if needed, source page if helpful. If commentary exceeds available space **without distorting student geometry**, use one of: (1) small keyed margin note if genuine room exists; (2) compact footer keyed to anchor code; (3) separate one-page teacher notes appendix. **Never shrink student geometry or typography merely to fit teacher commentary.**

## 19. Answer / scoring rules

Not scored. Where wording varies, list acceptable alternatives and **what NOT to require**. Include one concise misconception line per N-section (e.g., "we don't see energy — we see the change"; "electricity is not 'used up'").

## 20. Slideshow / notes mapping

The key carries the same BQ/V/N anchor codes as the student notes and the re-synced slideshow. Add a compact `CHECK/REVEAL` slide-reference note where useful.

## 21. Print / grayscale

Same as student. The key must remain readable in grayscale (gold/dark-blue answers must survive B/W).

## 22–27. QA (accessibility, source, semantic, visual, student, teacher)

- Source QA: every fill matches Reader/TG/AP wording; no transformation/BOTH content.
- Semantic QA: no key answer supplied where the student could not have derived it from taught/supplied evidence.
- Visual QA: `tools/qa_visual_pdf.py` on the key PDF; rendered inspection of all pages.
- Teacher usability: a teacher can check a class set in minutes without hunting.

## 28. Exact filenames

- Editable master: `production/premium-notes/04-ch4-energy-transfer-guided-notes-key.docx`
- Release export: `production/premium-notes/04-ch4-energy-transfer-guided-notes-key.pdf` → `production/releases/chapter-04/`

## 29. Editable source requirements

DOCX master mirroring the student master geometry (do not re-typeset). Same theme tokens (Ch4 violet/cyan).

## 30. Render requirements

PDF export via `tools/export_pdf_previews.py`; confirm target page count matches student, US Letter.

## 31. Acceptance gate

Key parity verified **blank-for-blank** against the student notes (every blank has exactly one answer treatment; no student blank left unanswered; no extra content that breaks geometry or page count). Pass source + semantic + visual + teacher-usability gates. Do not freeze, commit, or push.
