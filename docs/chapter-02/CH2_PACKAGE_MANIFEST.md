# CHAPTER 2 — PACKAGE MANIFEST

> Complete, canonical Chapter 2 teaching package (`Moving Objects Have Energy`, Reader pp. 7–12 · TG Lesson 3).
> Supersedes the historical `curriculum/chapter-02/CHAPTER_MANIFEST.md` (INB-era, retired). The retired INB-era files in `curriculum/chapter-02/` are now explicitly marked **SUPERSEDED** in place (document-only, per `docs/architecture/RETIRED_CURRICULUM_ARTIFACT_POLICY.md`); the active `student/recovery/` + `student/02-ch2-friday-flex.md` remain KEEP.
> `UNIT1_CH2_GOLD_STANDARD_VERSION = 1.0`. `STATUS = FROZEN` (2026-10-06). Guided Notes are the primary student artifact.
> External adversarial audit (2026-10-04): 4 findings remediated — see `qa/reports/PHASE_7_CH2_EXTERNAL_ADVERSARIAL_AUDIT.md` and `CH2_GOLD_STANDARD_FREEZE.md`.

## A. Core Required

| Resource | Canonical path | Status | Role |
|---|---|---|---|
| Guided Notes (student) | `production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.{docx,pdf}` | **FROZEN (v1.0)** (3 pp) | Primary structured content/reference |
| Guided Notes key (teacher) | `production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes-key.{docx,pdf}` | **FROZEN (v1.0)** (3 pp) | Mirrored teacher key |
| Slideshow (editable) | `production/slides/02-ch2-moving-objects-have-energy-slides.pptx` | **FROZEN (v1.0)** (37 slides) | Canonical instructional deck |
| Slideshow (rendered) | `production/slides/02-ch2-moving-objects-have-energy-slides.pdf` | **FROZEN (v1.0)** | Release export |
| Slideshow previews | `production/slides/previews/ch2-slides-*.png` (37) | **FROZEN (v1.0)** | Visual QA + projector reference |
| Reader pages | CKSci Student Reader Ch.2, printed pp. 7–12 | Authoritative | Source of truth |
| Teacher Guide | CKSci TG Lesson 3 | Authoritative | Source of truth |
| Playbook chapter section | `production/teacher-playbook/unit1-teacher-playbook.{docx,pdf}` — Ch2 spread + demo guide + slide map + support index | **FROZEN (v1.0)** | Teacher-facing documentation |
| Demo | Marble Collision (live DEMO; playbook Ch2 Demo Guide) | **FROZEN (v1.0)** | Moving object → change → evidence |

## B. Supporting Required

| Resource | Canonical path | Status | Role |
|---|---|---|---|
| Practice / application | `production/worksheets/02-ch2-moving-objects-have-energy-practice.docx` | **KEEP** (AVAILABLE) | Apply: identify mover + change + evidence (NOT note recopy) |
| Practice key | `production/answer-keys/02-ch2-moving-objects-have-energy-practice-key.md` | **AVAILABLE** | Mirrored key |
| Chapter 2 quiz | `production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx` | **KEEP** (AVAILABLE, scored) | 8-item formative chapter assessment |
| Quiz key | `production/answer-keys/02-ch2-moving-objects-have-energy-quiz-key.md` | **AVAILABLE** | Mirrored key |
| Quiz blueprint | `production/quizzes/02-ch2-moving-objects-have-energy-quiz-blueprint.md` | **AVAILABLE** | Balance/difficulty/source record |
| Absent / makeup | `production/worksheets/02-ch2-absent-student-recovery.docx` | **FROZEN (v1.0)** | Canonical recovery page. Teacher guidance: finish Guided Notes N1–N3 and CHECK; quiz makeup within 2 school days; Moving Marbles optional. |

## C. Optional / FLEX

| Resource | Canonical path | Status | Role |
|---|---|---|---|
| Science Journal prompts | `production/final-8.5-week/MASTER_CURRICULUM_MAP.md` (Ch2 days: draw the marble before/after) | **OPTIONAL/FLEX** (secondary role, already covered) | Reflection / drawing |
| Moving Marbles | `production/worksheets/02-ch2-moving-marbles-student.docx` + key `production/answer-keys/02-ch2-moving-marbles-key.md` + spec `production/labs/02-ch2-moving-marbles-teacher-spec.md` | **OPTIONAL/FLEX** (RECLASSIFIED) | AP 3.1 investigation (ADAPTED) |
| Friday FLEX | `curriculum/chapter-02/student/02-ch2-friday-flex.md` | **OPTIONAL/FLEX** (AVAILABLE) | RECOVER / PRACTICE / EXTEND |

## D. Teacher Keys

| Student artifact | Teacher key |
|---|---|
| Guided Notes | `…-guided-notes-key.{docx,pdf}` |
| Practice | `production/answer-keys/02-ch2-moving-objects-have-energy-practice-key.md` |
| Quiz | `production/answer-keys/02-ch2-moving-objects-have-energy-quiz-key.md` |
| Moving Marbles | `production/answer-keys/02-ch2-moving-marbles-key.md` |

## E. Future Unit-Level Integration

| Contribution | Canonical path | Status |
|---|---|---|
| Study-guide contribution | `docs/chapter-02/CH2_STUDY_GUIDE_CONTRIBUTION.md` | **AVAILABLE** (Phase 7) |
| Assessment trace | `docs/chapter-02/CH2_ASSESSMENT_TRACE.md` | **AVAILABLE** (Phase 7) — 2 items / 4 pts + motion distractor, direct coverage |
| Review-game contribution | Study-guide + assessment trace cover the Ch2 material for later review-game assembly | **AVAILABLE** via trace |

## Big Question / Vocabulary / Notes anchors (locked, all resources agree)

- **BQ:** "How are energy, change, and movement of objects related?"
- **V1:** motion (Reader p. 7) — **V2:** energy of motion (Reader p. 9)
- **N1** Moving Objects Can Cause Changes · **N2** Moving Objects Have Energy (MOVING OBJECT → CHANGE → EVIDENCE + Marble Collision OBSERVE) · **N3** People Use the Energy of Motion (hammer / pendulum / wind) · **CHECK** Your Thinking

## Provenance tags

- AP/Reader/TG content → **SOURCE** · adapted activity pages → **ADAPTED** · new scaffolds/models → **CUSTOM** · enrichment → **EXTENSION**.
- Priority: Guided Notes/Slideshow/Practice/Quiz = **CORE** · Moving Marbles + Journal + Friday FLEX = **FLEX**.

## Non-canonical export note

`production/releases/chapter-02/` is a **release-export area, not a canonical source**. Phase 7.6 rebuilds it with `tools/build_ch2_release.py` and checks it with `tools/qa_release_parity.py --chapter 2`. The pre-7.1 copies, including the interactive science notebook PDF, are archived under `production/archive/retired/chapter-02-pre-7.1/`. Canonical sources of truth live under `production/premium-notes/` (notes/key), `production/slides/` (slideshow), `production/worksheets/`, and `production/quizzes/`. Status: **FROZEN (v1.0)**.
