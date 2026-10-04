# PHASE 6 — CHAPTER 1 GOLD-STANDARD FINAL CERTIFICATION

> Independent certification/freeze of the complete Chapter 1 package before propagation to Chapters 2–7.
> Verdict: **PASS** — Chapter 1 frozen as `UNIT1_CH1_GOLD_STANDARD_VERSION = 1.0`.
> Date: 2026-10-04

## Acceptance gates

| Gate | Result |
|---|---|
| SOURCE FIDELITY | **PASS** |
| GUIDED NOTES | **PASS** |
| SLIDESHOW | **PASS** |
| SUPPORTING RESOURCES | **PASS** |
| PLAYBOOK | **PASS** |
| PACKAGE MANIFEST | **PASS** (21/21 files on disk) |
| ACTIVE REFERENCE CHECK | **PASS** |
| REPRODUCIBILITY | **PASS** |
| AUTOMATED QA MASTER RUN | **PASS** |
| INDEPENDENT FINAL CERTIFICATION | **PASS** |

---

## 1. What Works

- **Source fidelity.** Chapter title `Energy Causes Change`, the locked Big Question, Reader pp. 1–6, TG L1–L2, vocabulary (`energy` · `change` · `stored energy`), the five energy forms, the three stored-energy examples, and the evidence-of-change concept are consistent across Reader, notes, slides, practice, recovery, playbook, and quiz/key. No advanced required terminology (kinetic/potential/mechanical/radiant/compression-wave/inertia); no later-chapter leakage.
- **Notes.** Clean BQ → V1/V2 → N1–N4 → CHECK YOUR THINKING → BQ · NOW I THINK architecture; 3-page student ⇄ 3-page teacher-key parity; adequate blanks and handwriting clearance; grayscale/print-safe.
- **Slideshow.** Canonical 45-slide 16:9 deck; BQ/V/N anchors mirror the notes exactly; demo choreography (predict → observe → before/after → change = evidence); 6-question A/B/C/D review with shuffled letters; HUD distinct from permanent navigation; no hidden note answers on non-anchor slides.
- **Supporting resources.** Lean ecosystem — practice is a distinct APPLY task (evidence judgment), journal stays secondary/OPTIONAL, Energy Detectives correctly reclassified OPTIONAL/FLEX, absent/makeup pathway self-contained, teacher keys and blueprints present where required, study-guide contribution and assessment trace complete.
- **Playbook.** 29-page playbook with Chapter 1 spread, demo guide, slideshow map, and supporting-resource index using real filenames, page/slide counts, and honest statuses.
- **Reproducibility.** Build scripts (`build_ch1_guided_notes.py`, `build_ch1_slides.py`, `build_teacher_playbook.py`) produce deterministic, byte-identical internal XML to HEAD; PDF export via headless LibreOffice is stable.

## 2. What’s Missing

- Nothing required. The package is complete for a 30-minute-block Grade 4 unit; Chapter 1 has no missing CORE artifact, key, or teacher reference.

## 3. Fixes — specific problems + exact fixes

1. **Stale worksheet header + BQ paraphrase.** `production/worksheets/01-ch1-energy-detectives-student.docx` header read `Chapter 1 · Use with Lesson 1` and paraphrased the BQ. Fixed to `Chapter 1 · Week 1 · Friday FLEX · OPTIONAL` and BQ aligned to the locked `Where can we observe evidence of energy causing change?`.
2. **Ambiguous quiz-key total.** `production/answer-keys/01-ch1-energy-causes-change-quiz-key.md` carried a dangling `see OPEN_QUESTIONS` pointer. Fixed to `16 points · raw score + percentage (score out of 16; adjust the denominator only if an item is dropped)`.
3. **Recovery Q4 reference drift.** `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md` Step 4 Q4 referenced `flashlight` while the Step 3 class-data table used `light bulb`. Fixed to `light bulb`.
4. **Playbook "collect/grade" contradiction (found in Phase 6).** The Chapter 1 daily "Collect / grade" field said `No scored chapter item` while the same playbook's Resource Map and Supporting Resource Index mark the Chapter 1 quiz `Formative (graded)`. Fixed in `tools/build_teacher_playbook.py` to `Scored chapter item: Chapter 1 quiz (9-item, end of chapter)`; playbook DOCX/PDF/29 previews regenerated and `qa_teacher_playbook.py` re-run → OVERALL PASS.

## 4. Enhancements / Suggestions / New Ideas

- (Non-blocking, deferred to Chapters 2–7 build.) Consider 150-DPI playbook previews for final visual certification; current previews are 90 DPI and sufficient for projector/QA reference.
- Future chapters may need lab/build artifacts (e.g. Ramp It Up 2.0, Pom-Pom Launcher) that Chapter 1's lean ecosystem intentionally omits — decide per-chapter by the distinct-instructional-job rule in the propagation spec.

## 5. Edge Cases & Failure Modes

- **Multi-word blanks** widen correctly and don't collide with handwriting space (verified).
- **Grayscale/print** — chapter primaries desaturate darker than accents; color is never the only signal (verified by visual-system QA).
- **Absent students** — recovery guide substitutes the live sharpener demo with a printed/observed change, so no student is blocked by a missed live demo.
- **Friday FLEX** — never carries essential new core content; Energy Detectives/FLEX items are optional and safe to drop.

## 6. Performance Concerns

- None. All builds are one-shot and fast (notes/slides ~0.5 s; playbook DOCX ~0.4 s; PDF export ~2–5 s; previews ~1–6 s). No persistent processes, watch-mode runners, or servers.

## 7. Readability / Maintainability

- Editable-first masters (DOCX/PPTX) tracked; PDF/PNG are release exports. Anchors and statuses are centralized (manifest + playbook + freeze record) so Chapters 2–7 can be reproduced without reverse-engineering Chapter 1. The propagation spec (`docs/chapter-01/CH1_GOLD_STANDARD_PROPAGATION_SPEC.md`) distinguishes INHERIT EXACTLY / ADAPT BY CHAPTER / DO NOT COPY MECHANICALLY, preventing mechanical copying (slide count, N-section count, palette).
