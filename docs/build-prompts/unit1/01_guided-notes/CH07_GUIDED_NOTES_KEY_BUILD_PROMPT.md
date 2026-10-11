# BUILD PROMPT — Chapter 7 Guided Notes (Teacher Key)

> Standalone production prompt. Companion to `CH07_GUIDED_NOTES_STUDENT_BUILD_PROMPT.md`.

## 1. Mission

Produce the teacher key for Chapter 7 Guided Notes — a page-for-page, blank-for-blank mirror of the student file with answers filled into the student geometry. **All history answers are source-derived from the authoritative Reader/TG.**

## 2. Exact resource name

`07-ch7-edison-unit-synthesis-guided-notes-key` — **Chapter 7: Solving Problems and Designing Solutions: Thomas A. Edison — Guided Notes Key (Teacher)**

## 3. Audience

Teacher only.

## 4. Required / optional status

**REQUIRED · CORE · teacher-only**.

## 5. Instructional purpose

Give the teacher exact expected fills, acceptable alternatives, and — concisely — one major misconception per section and the source page, with special attention to historical-accuracy guardrails.

## 6. Source authority (order is authoritative)

1. **Authoritative Student Reader** (Ch7, pp. 37–42 / PDF 43–48). 2. **Authoritative Teacher Guide** (Unit Review, pp. 94–98). 3. **Current accepted pacing** (`curriculum/chapter-07/source-map.md`). 4. **Current Guided Notes architecture**. 5. **Slides after re-sync**. 6. **Assessment blueprint** (Q24).

> **RULING:** the assessment blueprint is a **traceability check, not curriculum authority.** Do not distort the curriculum to satisfy it.

## 7. Required content — the answer set

Mirror the student anchors exactly (BQ · KEY WORD recap · WORDS YOU MAY SEE · N1–N3 · CHECK · BQ·NOW I THINK). Representative answers (all source-anchored):

- **N1 (source-anchored):** "Edison improved earlier light bulb designs (he did not invent the first bulb — Reader p.38); his team tested more than six thousand materials for the filament (p.39); Lewis Howard Latimer also improved the bulb and worked for Edison's competitors and later Edison's company (p.41); Edison persisted through failures ('ten thousand ways', p.41)."
- **N2 cycle:** PROBLEM → DESIGN → TEST → EVIDENCE → IMPROVE. "A failed test tells you what to change next (it is information, not a reason to stop)."
- **N3 concept map:** center = ENERGY; branches = change · motion · speed · transfer · collisions · transformation · engineering.
- **CHECK / BQ·NOW I THINK:** "Sample answer — student wording may vary."

## 8. Explicit exclusions

Same locked boundaries (no lone-genius myth; no unsourced historical claims or invented dates/quotes; no kinetic/potential/mechanical/radiant required). No answer on any student page.

> **History rule (locked):** preserve the Reader's own wording. The Reader explicitly states Edison did not invent the first bulb (p.38) and that Latimer improved the bulb and worked for Edison's company (p.41) — preserve those accurately. Do not add external historical corrections the source does not make; do not invent dates, roles, collaborators, patents, or quotes.

## 9. Page count target

Identical to the student file (target 3 pages). The key must never drift to a different page count.

## 10–17. Layout, margins, typography, spacing, handwriting, tables, header, page-by-page

Inherit the student file layout **exactly** (US Letter portrait; margins 0.50–0.55 in; same typography/tables/diagrams/geometry; same page breaks; same line placement).

**Geometry parity rule (locked):** preserve the student page geometry exactly wherever possible — including **Name/Homeroom header geometry**, anchor positions, page breaks, margins, line placement. **Do NOT reflow the page.** Do NOT remove or simplify the Name/Homeroom line. Add a small, non-reflowing `TEACHER KEY` badge in a fixed corner/header position only.

## 18. Key architecture / answer treatment

Gold or dark blue, bold; no red. `ANSWER`/`SAMPLE` labels. Fill into student blank geometry. Open responses: `Sample answer — student wording may vary.` Misconception note per section (e.g., "Do not accept 'Edison invented the light bulb' — he improved it (Reader p.38)"; "failure is information, not failure of the engineer").

**Commentary limit (locked):** concise per section — expected answer, acceptable variants, one major misconception if needed, source page if helpful. If commentary exceeds space without distorting student geometry, use (1) a small keyed margin note if room exists, (2) a compact footer keyed to anchor code, or (3) a separate one-page teacher appendix. **Never shrink student geometry or typography to fit teacher commentary.**

## 19. Answer / scoring rules

Not scored. List acceptable alternatives and what NOT to require. Historical-accuracy note: "Accept 'improved earlier designs' and 'worked with Lewis Latimer' (source-supported); do not require the lone-genius story or any unsourced quote."

## 20. Slideshow / notes mapping

Same anchor codes; reveal-slide references where useful.

## 21. Print / grayscale

Same as student; readable in B/W.

## 22–27. QA

Source QA (Edison framing verified against Reader) · semantic QA · visual QA (`tools/qa_visual_pdf.py` + rendered inspection) · teacher usability.

## 28. Exact filenames

- Editable: `production/premium-notes/07-ch7-edison-unit-synthesis-guided-notes-key.docx`
- Release: `…-key.pdf` → `production/releases/chapter-07/`

## 29. Editable source requirements

DOCX master mirroring student geometry; Ch7 theme (sepia/brown).

## 30. Render requirements

PDF via `tools/export_pdf_previews.py`; page count matches student.

## 31. Acceptance gate

Key parity verified blank-for-blank (every student blank answered; no extra content breaking geometry or page count). Pass source + semantic + visual + teacher-usability gates. Do not freeze, commit, or push.
