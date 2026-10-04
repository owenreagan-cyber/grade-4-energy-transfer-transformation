# CHAPTER 1 — GOLD-STANDARD FREEZE

> Authoritative freeze record for Chapter 1 (`Energy Causes Change`, Reader pp. 1–6 · TG L1–L2).
> This is the single source of truth for the frozen Chapter 1 version. Do not create a competing version source.

## Declaration

```
UNIT1_CH1_GOLD_STANDARD_VERSION = 1.0
STATUS                         = FROZEN
```

- **Freeze date:** 2026-10-04
- **Freeze basis:** Phase 6 final independent certification — all required acceptance gates PASS (see `docs/reviews/PHASE_6_CH1_GOLD_STANDARD_CERTIFICATION.md`).

## Canonical artifacts

The complete, canonical Chapter 1 file inventory is **`docs/chapter-01/CH1_PACKAGE_MANIFEST.md`** (21 canonical files, all verified on disk). It is the single authoritative list; this freeze record does not duplicate it. Key groups:

| Group | Canonical location |
|---|---|
| Guided Notes (student + key) | `production/premium-notes/01-ch1-energy-causes-change-guided-notes{-key}.{docx,pdf}` (3 pp each) |
| Slideshow | `production/slides/01-ch1-energy-causes-change-slides.{pptx,pdf}` + `previews/ch1-slides-*.png` (45 slides) |
| Teacher Playbook (Ch1 section) | `production/teacher-playbook/unit1-teacher-playbook.{docx,pdf}` (29 pp) |
| Practice + key | `production/worksheets/01-ch1-energy-causes-change-practice.docx` · `production/answer-keys/01-ch1-energy-causes-change-practice-key.md` |
| Quiz + key + blueprint | `production/quizzes/01-ch1-energy-causes-change-quiz.{docx}` · `…-quiz-key.md` · `…-quiz-blueprint.md` (9-item · 16 pts) |
| Absent recovery | `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md` |
| Energy Detectives + key + spec | `production/worksheets/01-ch1-energy-detectives-student.docx` · `production/answer-keys/01-ch1-energy-detectives-key.md` · `production/labs/01-ch1-energy-detectives-teacher-spec.md` (OPTIONAL/FLEX) |
| Friday FLEX | `curriculum/chapter-01/student/01-ch1-friday-flex.md` |
| Study-guide contribution | `docs/chapter-01/CH1_STUDY_GUIDE_CONTRIBUTION.md` |
| Assessment trace | `docs/chapter-01/CH1_ASSESSMENT_TRACE.md` |

## Locked anchors (all resources agree)

- **BQ:** "Where can we observe evidence of energy causing change?"
- **V1:** energy · change (Reader p. 1) — **V2:** stored energy (Reader p. 4)
- **N1** Energy Causes Change (ENERGY → CHANGE → EVIDENCE) · **N2** Energy Occurs in Different Forms (motion · sound · light · heat · electrical energy) · **N3** Objects Can Store Energy (STORED → RELEASE → CHANGE) · **N4** Recognizing Evidence (BEFORE/AFTER)

## QA reports (all PASS)

| Report | Result |
|---|---|
| `qa/reports/PHASE_3_CH1_GUIDED_NOTES_QA.md` | PASS |
| `qa/reports/PHASE_4_CH1_SLIDESHOW_QA.md` + `…_INDEPENDENT_QA.md` + `…_SOURCE_FIDELITY.md` | PASS |
| `qa/reports/PHASE_5_CH1_PACKAGE_QA.md` | PASS |
| `qa/reports/PHASE_2_PLAYBOOK_QA.md` | PASS (re-run after Phase 6 collect/grade fix) |
| Visual-system QA (`tools/qa_visual_system.py`, FROZEN v1.0) | PASS (unchanged) |

## Known non-blocking warnings

- **None.** Every WARN surfaced during Phases 3–6 was corrected before freeze (worksheet header/BQ alignment, quiz-key point sum, absent-recovery Q4 reference, Energy Detectives BQ "find" → "observe", Friday-FLEX stale label, and the Phase 6 Playbook "No scored chapter item" → "Scored chapter item" fix).

## Rules for future edits (after freeze)

Any change to frozen Chapter 1 requires:

1. An **explicit, substantiated reason** (not preference-only redesign).
2. Rebuild of the **affected artifact(s)** from their editable master.
3. **Re-run of the affected QA gate(s)** (and the automated QA master run if any anchor/layout changes).
4. **Playbook resync** if the change touches filenames, page/slide counts, anchors, or statuses.
5. **Manifest update** if the file inventory changes.

Frozen and must NOT be altered in place:
- Unit 1 Visual System v1.0 (`assets/visual-system/design-tokens.json`).
- Authoritative CKSci Student Reader / Teacher Guide.
