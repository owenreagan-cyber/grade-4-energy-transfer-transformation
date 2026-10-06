# PHASE 7 — CHAPTER 2 GOLD-STANDARD PROPAGATION REVIEW

> **Historical record (Phase 7, 2026-10-04).** The freeze claim in the body below was not the external approval. The authorized freeze is `UNIT1_CH2_GOLD_STANDARD_VERSION = 1.0`, `STATUS = FROZEN`, 2026-10-06, recorded in `docs/chapter-02/CH2_GOLD_STANDARD_FREEZE.md`.

> Chapter 2 `Moving Objects Have Energy` (Reader pp. 7–12 · TG Lesson 3) propagated from the frozen Chapter 1 Gold Standard v1.0 exemplar. Phase 7 of the Unit 1 build. Final gate result: **PASS** (freeze authorized).

## 1. What Works

- **Notes-first process honored.** Guided Notes built and QA'd before any slide; BQ/V1/N1/V2/N2/N3/CHECK/BQ-return architecture mirrors the Ch1 exemplar without mechanically copying Ch1's section count or slide count.
- **Exact BQ fidelity** — `"How are energy, change, and movement of objects related?"` verbatim across notes, slides, playbook, and all docs.
- **Core Vocabulary exact** — `motion` (p. 7) and `energy of motion` (p. 9), both definitions verbatim; only two V-groups (Ch2 has two terms, not Ch1's three).
- **Demo (Marble Collision) kept in scope** — observe → predict → observe → evidence, with no Ch3 speed drift and no Ch5 transfer depth (post-review "may slow" wording removed).
- **Slideshow mirrors notes exactly** — 37 slides, 16:9; every BQ/V/N anchor, model chain `MOVING OBJECT → CHANGE → EVIDENCE`, BEFORE/AFTER OBSERVE box, and N3 hammer/pendulum/wind table mirrored; reveal-not-frontload verified.
- **All automated QA PASS** — notes, slides, playbook (see §Automated QA).
- **Independent reviewers returned PASS** — source fidelity PASS; final certification PASS with non-blocking WARNs, all either fixed or documented.

## 2. What's Missing

- **Chapter 2 quiz score line** — the student quiz DOCX (`production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx`) lacks a raw-score + percentage line. Pre-existing Phase 5 artifact; recorded for a follow-up edit.
- **Science Journal per-chapter file** — none exists for any chapter; prompts live in `MASTER_CURRICULUM_MAP.md` (secondary role), consistent with Ch1. No gap.

## 3. Fixes — specific problems + exact fixes

- **Quiz key total "~13 points"** → corrected to definitive **12 points** (1+1+2+1+2+2+2+1) + score-line convention note.
- **Ch3-adjacent "the moving marble may slow"** on slide 6 and playbook Ch2 Demo Guide → removed; demo now stops at "the target marble changed from still to moving."
- **Playbook "Absent / makeup support: Ch1 AVAILABLE · Ch2–7 SKELETON"** → corrected to "Ch1–2 AVAILABLE · Ch3–7 SKELETON."
- **Stale `production/releases/chapter-02/` copies** → documented as non-canonical (candidates for archive per RETIRED_CURRICULUM_ARTIFACT_POLICY; not moved/deleted this phase).

## 4. Enhancements / Suggestions / New Ideas

- Reconcile the quiz blueprint's "NO speed/fast-slow" claim to "no speed-based *correct* answers" so distractors-as-misconception-traps are not flagged.
- When the Unit 1 Study Guide is reassembled, `CH2_STUDY_GUIDE_CONTRIBUTION.md` supplies the Ch2 block (motion · energy of motion · model chain · marble scenario · sample Q23).
- Republish `production/releases/chapter-02/` from canonical paths (or archive it) in a future, separately-scoped normalization pass.

## 5. Edge Cases & Failure Modes

- **3-page notes vs 2-page target** — Ch2 legitimately needs 3 pages; documented as justified (no font/handwriting compression).
- **Q23 "transfer" wording (Ch2/Ch5)** — the locked final uses Ch5 language for a Ch2 scenario; trace records the nuance.
- **`possesses` (notes) vs `has` (locked Q5)** — both source-faithful; no action.
- **Front-loading** — structurally prevented (write slides render blanks, reveal slides render bold-accent answers); QA gate confirms no leakage.

## 6. Performance Concerns

- All generators are one-shot headless Python (`python-docx`/`python-pptx`) + LibreOffice `soffice --headless` + `pdftoppm`/`pdfinfo`. No watch-mode, no duplicate servers, no persistent processes. Build+render times are seconds-to-single-digit-seconds per artifact.

## 7. Readability / Maintainability

- Deterministic, single-source QA scripts (`qa_ch2_guided_notes.py`, `qa_ch2_slides.py`, `qa_teacher_playbook.py`) mirror the Ch1 suite, so any future Ch2 edit is re-checkable in one command.
- `CH2_SLIDESHOW_HANDOFF.md` freezes the notes→slides contract, making the mirror relationship reproducible.
- Provenance tags (SOURCE/ADAPTED/CUSTOM/EXTENSION) recorded in the manifest.

---

## Acceptance gates (final)

| Gate | Result |
|---|---|
| SOURCE REVIEW | PASS |
| GUIDED NOTES | PASS |
| TEACHER KEY | PASS |
| SLIDESHOW | PASS |
| NOTES ↔ SLIDES SYNC | PASS |
| SUPPORTING RESOURCES | PASS |
| PLAYBOOK SYNC | PASS |
| PACKAGE MANIFEST | PASS |
| AUTOMATED QA | PASS |
| INDEPENDENT FINAL REVIEW | PASS |

**Chapter 2 frozen: YES** — `UNIT1_CH2_GOLD_STANDARD_VERSION = 1.0`, `STATUS = FROZEN`.
