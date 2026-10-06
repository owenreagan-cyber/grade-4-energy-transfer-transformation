# CHAPTER 2 — GOLD-STANDARD RECORD

> Authoritative freeze record for Chapter 2 (`Moving Objects Have Energy`, Reader pp. 7–12 · TG Lesson 3).
> This is the single source of truth for the frozen Chapter 2 version. Do not create a competing version source.

## Declaration (current)

```
UNIT1_CH2_GOLD_STANDARD_VERSION = 1.0
STATUS                         = FROZEN
EXTERNAL APPROVAL              = APPROVE PROPAGATION
FREEZE DATE                    = 2026-10-06
```

- **External decision (verbatim): APPROVE PROPAGATION.** Issued after the Phase 7.6A Playbook golden-coverage sign-off.
- **Freeze action:** metadata only. Classroom artifacts rebuilt for the freeze: **0**. The Teacher Playbook binary is included in this freeze because it was deferred from the Chapter 1 commit; its Chapter 2 instructional text is unchanged.
- **Timing authority:** `docs/chapter-02/CH2_PACING_PLAN.md` (`tools/ch2_pacing.py`)
- **Reference standard:** Chapter 1 v1.1 (`UNIT1_CH1_GOLD_STANDARD_VERSION = 1.1`, FROZEN)
- **Tag:** none.

## Pre-freeze record (not in force; preserved)

> Phase 7.4 remediation candidate. The Phase 7 "FROZEN" claim below is **historical and not in force**. Chapter 2 was **not frozen** until 2026-10-06.

- **UNIT1_CH2_GOLD_STANDARD_VERSION = not assigned** (superseded 2026-10-06 by v1.0)
- **STATUS = PHASE 7.3 REMEDIATION CANDIDATE — NOT FROZEN** (superseded)
- **Timing authority:** `docs/chapter-02/CH2_PACING_PLAN.md` (`tools/ch2_pacing.py`)
- **Reference standard:** Chapter 1 v1.1 (`UNIT1_CH1_GOLD_STANDARD_VERSION = 1.1`, FROZEN)

## Historical Phase 7 claim (not in force)

> Phase 7 freeze record. Chapter 2 passed internal QA. The designated external reviewer was not reachable, so that pass was an integrator stopgap, not an external approval.

- **Historical label:** UNIT1_CH2_GOLD_STANDARD_VERSION = 1.1
- **Historical status:** FROZEN — remediated; external (Grok) sign-off pending
- **External audit record:** `qa/reports/PHASE_7_CH2_EXTERNAL_ADVERSARIAL_AUDIT.md` — 4 blocking findings (F1–F4), all remediated (see "Post-review fixes applied"). Final external sign-off is still pending: the designated external reviewer (Grok) was not reachable from the environment, so the integrator ran a read-only adversarial audit as a stopgap.

## Canonical artifacts (source of truth)

| Artifact | Path | Status |
|---|---|---|
| Source map | `docs/chapter-02/CH2_SOURCE_MAP.md` | FROZEN (v1.0) |
| Slideshow handoff contract | `docs/chapter-02/CH2_SLIDESHOW_HANDOFF.md` | FROZEN (v1.0) |
| Guided Notes (student) | `production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.{docx,pdf}` | FROZEN (v1.0) (3 pp) |
| Guided Notes key | `production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes-key.{docx,pdf}` | FROZEN (v1.0) (3 pp) |
| Slideshow | `production/slides/02-ch2-moving-objects-have-energy-slides.pptx` | FROZEN (v1.0) (37 slides) |
| Slideshow PDF + previews | `production/slides/02-ch2-moving-objects-have-energy-slides.pdf` · `previews/ch2-slides-*.png` | FROZEN (v1.0) |
| Playbook Ch2 spread/demo/slide-map/support-index | `production/teacher-playbook/unit1-teacher-playbook.{docx,pdf}` | FROZEN (v1.0) |
| Study-guide contribution | `docs/chapter-02/CH2_STUDY_GUIDE_CONTRIBUTION.md` | FROZEN (v1.0) |
| Assessment trace | `docs/chapter-02/CH2_ASSESSMENT_TRACE.md` | FROZEN (v1.0) |
| Package manifest | `docs/chapter-02/CH2_PACKAGE_MANIFEST.md` | FROZEN (v1.0) |

## QA reports (all PASS)

- `qa/reports/PHASE_7_CH2_GUIDED_NOTES_QA.md` — PASS
- `qa/reports/PHASE_7_CH2_SLIDESHOW_QA.md` — PASS
- `qa/reports/PHASE_2_PLAYBOOK_QA.md` — PASS (Ch2 spread integrated)

## Non-blocking warnings

- **Page count 3 (not the ~2-page planning target).** Ch2 carries two Core Vocabulary terms + three note sections + a Marble Collision BEFORE/AFTER box + a three-example table + CHECK + BQ return. Compressing to 2 pages would have violated the "generous Grade 4 writing space" non-negotiable. Recorded as a deliberate, justified deviation.
- **Q23 wording is Ch2/Ch5.** The locked final's Q23 correct option uses "transferred" (Ch5 depth). Chapter 2 grounds the scenario via N2 change-as-evidence, but the transfer vocabulary is formally Chapter 4–5. Not a Ch2 defect; recorded for the unit-assembly phase.
- **Notes define `energy of motion` with "possesses"; the locked final Q5 uses "has".** Both are source-faithful to Reader p. 9; no corrective action required.
- **`production/releases/chapter-02/` holds stale release exports** (a 2-page guided-notes PDF, a 4-page teacher-key PDF, and a retired `…-interactive-science-notebook.pdf`). These are non-canonical export copies — candidates for `archive/retired/` per `docs/architecture/RETIRED_CURRICULUM_ARTIFACT_POLICY.md` — but are **documented only** (not moved/deleted this phase, per that policy). The canonical sources of truth are under `production/premium-notes/` and `production/slides/`.
- **Quiz blueprint "No out-of-scope content: NO speed/fast-slow"** is slightly imprecise: two *distractor* options mention "fast"/"speed" as misconception traps (correct answers are never speed-based). No corrective action required; distractors are defensible.

## Post-review fixes applied (Phase 7)

- Quiz key point total corrected from "~13 points" → definitive **12 points** (1+1+2+1+2+2+2+1).
- Removed the Ch3-adjacent "the moving marble may slow" observation from slideshow slide 6 and the playbook Ch2 Demo Guide "Do This" step (demo now stays strictly at "the target marble changed from still to moving").
- Playbook "Absent / makeup support" status corrected to "Ch1–2 AVAILABLE · Ch3–7 SKELETON".

## External adversarial audit — findings + remediation (Phase 7 · 2026-10-04)

- **F1 (quiz score line)** — Added `Score: ______ / 12 = ______ %` to `production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx` (AGENTS.md "raw score + percentage").
- **F2 (schedule conflict)** — Corrected `production/worksheets/02-ch2-moving-marbles-student.docx` header to "Chapter 2 · Week 1 · Friday FLEX · OPTIONAL"; fixed `curriculum/chapter-02/student/02-ch2-friday-flex.md` "Tuesday's page" → the student-file reference.
- **F3 (Moving Marbles status)** — Retagged `production/labs/02-ch2-moving-marbles-teacher-spec.md` from CORE → **OPTIONAL/FLEX** (formerly Lab 2 of the 8-lab backbone; RECLASSIFIED Phase 7), "Week 1 (Thu)" → "Week 1 (Friday FLEX)", and added the reclassification rationale (core concept taught live via the Wednesday Marble Collision demonstration).
- **F4 (stale `curriculum/chapter-02/` tree)** — Marked the retired files **SUPERSEDED** in place (document-only, per `docs/architecture/RETIRED_CURRICULUM_ARTIFACT_POLICY.md`): `README.md`, `CHAPTER_MANIFEST.md`, `source-map.md`, `teacher/02-ch2-moving-objects-have-energy-teacher-map.md`, `teacher/02-ch2-daily-lessons.md`, `teacher/02-ch2-supply-prep-guide.md`, `qa/acceptance-report.md`. The active `student/recovery/` + `student/02-ch2-friday-flex.md` remain KEEP.
- Verification: both edited DOCX files open cleanly (python-docx) and round-trip to PDF via LibreOffice (quiz 2 pp, marbles 2 pp) with no corruption.

## Future edit rules

1. Chapter 2 is **FROZEN** as `UNIT1_CH2_GOLD_STANDARD_VERSION = 1.0` (2026-10-06, external decision APPROVE PROPAGATION). Any further edit re-runs the Chapter 2 QA suite and requires a reviewed baseline update. Post-freeze text comparison reads the golden file from the freeze commit, not a working-tree rewrite.
2. Any edit to Guided Notes **must** update `CH2_SLIDESHOW_HANDOFF.md` and the slideshow (and re-run notes QA + slides QA + sync QA).
3. Any edit to the slideshow **must** re-run `qa_ch2_slides.py`.
4. Do **not** introduce speed-energy comparison (Ch3), transfer/transformation classification (Ch4–6), or advanced vocabulary (kinetic/potential/mechanical/radiant/momentum/inertia/compression wave).
5. Do **not** modify the frozen Unit 1 Visual System v1.0, Chapter 1, or Chapters 3–7 as part of Chapter 2 work.
