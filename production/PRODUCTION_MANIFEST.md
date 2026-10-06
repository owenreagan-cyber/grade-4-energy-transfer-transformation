# PRODUCTION MANIFEST

> Tracked register of every produced artifact, its status, and its provenance. Update whenever an artifact changes status.

## Status vocabulary
`PLANNED` · `DRAFT` · `QA` · `ACCEPTED` · `RELEASED`

End-of-life states (never canonical, never listed as current): `RETIRED` · `SUPERSEDED` (always with the superseding path and the phase that retired it).

## Phase 11 — Chapter 1 Note-Format Study (comparison artifacts)

> Controlled comparison of INB vs full-size Guided Notes. Prototypes are comparison-only — they do NOT replace released Chapter 1 artifacts.

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| C1 | INB comparison prototype (master + PDF) | `production/comparisons/chapter-01-notes/inb/01-ch1-inb-comparison-master.docx` + `.pdf` | QA | ADAPTED/CUSTOM |
| C2 | Guided Notes comparison prototype (master + PDF) | `production/comparisons/chapter-01-notes/guided-notes/01-ch1-guided-notes-comparison-master.docx` + `.pdf` | QA | ADAPTED/CUSTOM |
| C3 | Teaching-comparison slide set | `production/comparisons/chapter-01-notes/01-ch1-note-system-teaching-comparison.pptx` | QA | CUSTOM |
| C4 | Study QA + recommendation | `qa/comparisons/ch1-notes/` + `docs/reviews/CH1_INB_VS_GUIDED_NOTES_STUDY.md` | QA | CUSTOM |

## Chapter 1 — Energy Causes Change

| ID | Artifact | Master path | Release path | Status | Provenance |
|---|---|---|---|---|---|
| P1 | Teacher package reference (Ch1) | `docs/chapter-01/CH1_PACKAGE_MANIFEST.md` + Teacher Playbook Ch1 spread (`production/teacher-playbook/unit1-teacher-playbook.docx`) | `production/teacher-playbook/unit1-teacher-playbook.pdf` | RELEASED (v1.1 FROZEN; Playbook binary ships with the Ch2 commit) | SOURCE/ADAPTED |
| P2 | Slide Deck | `production/slides/01-ch1-energy-causes-change-slides.pptx` | `production/releases/chapter-01/` | RELEASED | ADAPTED |
| P3 | Guided Notes (student + teacher key) | `production/premium-notes/01-ch1-energy-causes-change-guided-notes.docx` + `…-guided-notes-key.docx` | `production/releases/chapter-01/` (PDFs) | RELEASED (v1.1 FROZEN) | ADAPTED |
| P4 | Energy Detectives (OPTIONAL · ungraded · no points) | `production/labs/01-ch1-energy-detectives-teacher-spec.md` + `production/worksheets/01-ch1-energy-detectives-student.docx` | `production/releases/chapter-01/` | RELEASED | ADAPTED |
| P5 | Practice Worksheet | `production/worksheets/01-ch1-energy-causes-change-practice.docx` | `production/releases/chapter-01/` | RELEASED | ADAPTED |
| P6 | Friday Flex | `curriculum/chapter-01/student/01-ch1-friday-flex.md` | `production/releases/chapter-01/` | RELEASED | CUSTOM |
| P7 | Chapter Quiz | `production/quizzes/01-ch1-energy-causes-change-quiz.docx` | `production/releases/chapter-01/` | RELEASED | ADAPTED |
| P8 | Teacher Keys (quiz · practice · Detectives; notes key = P3) | `production/answer-keys/01-ch1-*-key.md` | `production/releases/chapter-01/` (combined teacher-key PDF) | RELEASED | SOURCE/ADAPTED |
| P9 | Media Plan | `curriculum/chapter-01/media/01-ch1-media-plan.md` + `01-ch1-explainer-script.md` | — | RELEASED | CUSTOM |
| P10 | QA Package | `curriculum/chapter-01/qa/` | — | RELEASED | CUSTOM |
| P11 | Interactive Science Notebook | `production/student-notebook/chapter-01/01-ch1-interactive-notebook.docx` | `production/archive/retired/chapter-01-release-v1.0/01-ch1-interactive-science-notebook.pdf` | RETIRED (Phase 6.1) | ADAPTED |
| P12 | Pacing plan (the ONE Ch1 timing system) | `docs/chapter-01/CH1_PACING_PLAN.md` (generated from `tools/ch1_pacing.py`) | — | RELEASED (includes the Friday fallback) | CUSTOM |
| P13 | Release package manifest | `production/releases/chapter-01/RELEASE_MANIFEST.json` (built by `tools/build_ch1_release.py`; verified by `tools/qa_release_parity.py --chapter 1`) | `production/releases/chapter-01/` | RELEASED (v1.1 FROZEN) | CUSTOM |
| P14 | Teacher Chapter Map (pre-canonical staging file) | `curriculum/chapter-01/teacher/01-ch1-energy-causes-change-teacher-map.md` | — | RETIRED / SUPERSEDED (Phase 6.1B) → superseded by P1 + P12 | SOURCE/ADAPTED |
| P15 | Legacy Guided Notes ("WHAT WE NOTICE" architecture) | `production/student-notes/01-ch1-energy-causes-change-guided-notes.docx` | — | RETIRED / SUPERSEDED (Phase 6.1B) → superseded by P3 (`production/premium-notes/`) | ADAPTED |

> **Chapter 1 lifecycle:** v1.0 FROZEN (history preserved) · v1.1 `STATUS = FROZEN` (external decision APPROVE PROPAGATION, 2026-10-05; record: `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`). P14 and P15 are historical/retired and must never be cited as canonical or current. Chapter 1 is complete (Phase 3). **Phase 6.1:** the Interactive Science Notebook (P11) is RETIRED from the Ch1 release (moved to `production/archive/retired/chapter-01-release-v1.0/`); the release package is built by `tools/build_ch1_release.py` and verified by `tools/qa_release_parity.py --chapter 1`. Guided Notes are the primary student artifact. **Playbook (P1):** the Playbook binary is one combined file that also holds Chapter 2 pages, so it ships with the Chapter 2 v1.0 freeze. Chapter 1 timing is governed by P12.

## Chapter 2 — Moving Objects Have Energy

| ID | Artifact | Master path | Release path | Status | Provenance |
|---|---|---|---|---|---|
| P1 | Teacher package reference (Ch2) | `docs/chapter-02/CH2_PACKAGE_MANIFEST.md` + Teacher Playbook Ch2 spread | `production/teacher-playbook/unit1-teacher-playbook.pdf` | FROZEN (v1.0) | SOURCE/ADAPTED |
| P2 | Slide Deck | `production/slides/02-ch2-moving-objects-have-energy-slides.pptx` | `production/releases/chapter-02/` | FROZEN (v1.0) | ADAPTED |
| P3 | Guided Notes (student + teacher key) | `production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx` + `…-guided-notes-key.docx` | `production/releases/chapter-02/` (PDFs) | FROZEN (v1.0) | ADAPTED |
| P4 | Moving Marbles (OPTIONAL · ungraded) | `production/labs/02-ch2-moving-marbles-teacher-spec.md` + `production/worksheets/02-ch2-moving-marbles-student.docx` | `production/releases/chapter-02/` | OPTIONAL | ADAPTED |
| P5 | Practice Worksheet | `production/worksheets/02-ch2-moving-objects-have-energy-practice.docx` | `production/releases/chapter-02/` | FROZEN (v1.0) | ADAPTED |
| P6 | Friday Flex (after the quiz; not Week 1 Friday) | `curriculum/chapter-02/student/02-ch2-friday-flex.md` | `production/releases/chapter-02/` | OPTIONAL | CUSTOM |
| P7 | Chapter Quiz | `production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx` | `production/releases/chapter-02/` | FROZEN (v1.0) | ADAPTED |
| P8 | Teacher Keys (quiz · practice · Moving Marbles; notes key = P3) | `production/answer-keys/02-ch2-*-key.md` | `production/releases/chapter-02/` (combined teacher-key PDF) | FROZEN (v1.0) | SOURCE/ADAPTED |
| P9 | Media Plan | `curriculum/chapter-02/media/02-ch2-media-plan.md` + `02-ch2-explainer-script.md` | — | AVAILABLE | CUSTOM |
| P10 | QA Package | `curriculum/chapter-02/qa/` | — | AVAILABLE | CUSTOM |
| P11 | Interactive Science Notebook | retired pre-canonical notebook PDF | `production/archive/retired/chapter-02-pre-7.1/` | RETIRED / SUPERSEDED (Phase 7.1) → superseded by P3 | ADAPTED |
| P12 | Pacing plan (the ONE Ch2 timing system) | `docs/chapter-02/CH2_PACING_PLAN.md` (generated from `tools/ch2_pacing.py`) | — | FROZEN (v1.0) | CUSTOM |
| P13 | Release package manifest | `production/releases/chapter-02/RELEASE_MANIFEST.json` (built by `tools/build_ch2_release.py`; verified by `tools/qa_release_parity.py --chapter 2`) | `production/releases/chapter-02/` | FROZEN (v1.0) | CUSTOM |
| P14 | Teacher Chapter Map (pre-canonical staging file) | `curriculum/chapter-02/teacher/02-ch2-moving-objects-have-energy-teacher-map.md` | — | RETIRED / SUPERSEDED (Phase 7) → superseded by P1 + P12 | SOURCE/ADAPTED |
| P15 | Absent-student recovery | `production/worksheets/02-ch2-absent-student-recovery.docx` | `production/releases/chapter-02/02-ch2-absent-student-recovery.pdf` | FROZEN (v1.0) | Teacher: finish N1–N3 and CHECK; quiz makeup within 2 school days; Moving Marbles optional. |

> **Chapter 2 lifecycle:** `UNIT1_CH2_GOLD_STANDARD_VERSION = 1.0`, `STATUS = FROZEN` (external decision APPROVE PROPAGATION, 2026-10-06; record: `docs/chapter-02/CH2_GOLD_STANDARD_FREEZE.md`). Guided Notes are the primary student artifact. The Interactive Science Notebook (P11) is RETIRED from the Chapter 2 release. P14 is historical and must not be cited as current. Timing is P12 (Wed 10/14 · Thu 10/15). Friday 10/16 is Chapter 1.

## Chapter 3 — Energy and Speed Are Related

| ID | Artifact | Master path | Release path | Status | Provenance |
|---|---|---|---|---|---|
| P1 | Teacher Chapter Map | `curriculum/chapter-03/teacher/03-ch3-energy-speed-teacher-map.md` | — | RELEASED | SOURCE/ADAPTED |
| P2 | Slide Deck | `production/slides/03-ch3-energy-speed-slides.pptx` | `production/releases/chapter-03/` | RELEASED | ADAPTED |
| P3 | Interactive Science Notebook | `production/student-notebook/chapter-03/03-ch3-interactive-notebook.docx` | `production/releases/chapter-03/03-ch3-interactive-science-notebook.pdf` | RELEASED | ADAPTED |
| P4 | Ramp It Up! 2.0 Investigation | `production/labs/03-ch3-ramp-it-up-teacher-spec.md` + `production/worksheets/03-ch3-ramp-it-up-student.docx` | `production/releases/chapter-03/` | RELEASED | ADAPTED |
| P5 | Drop It Investigation | `production/labs/03-ch3-drop-it-teacher-spec.md` + `production/worksheets/03-ch3-drop-it-student.docx` | `production/releases/chapter-03/` | RELEASED | ADAPTED |
| P6 | Practice Worksheet | `production/worksheets/03-ch3-energy-speed-practice.docx` | `production/releases/chapter-03/` | RELEASED | ADAPTED |
| P7 | Friday Flex | `curriculum/chapter-03/student/03-ch3-friday-flex.md` | `production/releases/chapter-03/` | RELEASED | CUSTOM |
| P8 | Chapter Quiz | `production/quizzes/03-ch3-energy-speed-quiz.docx` | `production/releases/chapter-03/` | RELEASED | ADAPTED |
| P9 | Teacher Keys | `production/answer-keys/03-ch3-*-key.md` | `production/releases/chapter-03/` | RELEASED | SOURCE/ADAPTED |
| P10 | Media Plan + Scripts | `curriculum/chapter-03/media/` (plan + 4 scripts) | — | RELEASED | CUSTOM |
| P11 | Absent-Student Recovery | `curriculum/chapter-03/student/recovery/03-ch3-absent-student-recovery.md` | — | RELEASED | SOURCE/ADAPTED |
| P12 | QA Package (10 gates) | `curriculum/chapter-03/qa/` | — | RELEASED | CUSTOM |

> Chapter 3 is complete (Phase 5). Chapters 4–7 will be added in Phase 6+.

## Chapter 4 — Energy Transfer (Weeks 4–5, two-week chapter)

| ID | Artifact | Master path | Release path | Status | Provenance |
|---|---|---|---|---|---|
| P1 | Teacher Chapter Map | `curriculum/chapter-04/teacher/04-ch4-energy-transfer-teacher-map.md` | — | RELEASED | SOURCE/ADAPTED |
| P2 | Daily Lessons (W4 + W5) | `curriculum/chapter-04/teacher/04-ch4-daily-lessons-week{4,5}.md` | — | RELEASED | SOURCE/ADAPTED |
| P3 | Slide Deck | `production/slides/04-ch4-energy-transfer-slides.pptx` | `production/releases/chapter-04/` | RELEASED | ADAPTED |
| P4 | Interactive Science Notebook | `production/student-notebook/chapter-04/04-ch4-interactive-notebook.docx` | `production/releases/chapter-04/04-ch4-interactive-science-notebook.pdf` | RELEASED | ADAPTED |
| P5 | Sound Transfer Investigation | `production/labs/04-ch4-sound-transfer-teacher-spec.md` + `production/worksheets/04-ch4-sound-transfer-student.docx` | `production/releases/chapter-04/` | RELEASED | SOURCE/ADAPTED |
| P6 | Light Transfer Investigation | `production/labs/04-ch4-light-transfer-teacher-spec.md` + `production/worksheets/04-ch4-light-transfer-student.docx` | `production/releases/chapter-04/` | RELEASED | ADAPTED |
| P7 | Heat Transfer Investigation | `production/labs/04-ch4-heat-transfer-teacher-spec.md` + `production/worksheets/04-ch4-heat-transfer-student.docx` | `production/releases/chapter-04/` | RELEASED | ADAPTED |
| P8 | Electricity Transfer Investigation | `production/labs/04-ch4-electricity-transfer-teacher-spec.md` + `production/worksheets/04-ch4-electricity-transfer-student.docx` | `production/releases/chapter-04/` | RELEASED | ADAPTED |
| P9 | Practice Worksheet | `production/worksheets/04-ch4-energy-transfer-practice.docx` | `production/releases/chapter-04/` | RELEASED | ADAPTED |
| P10 | Friday Flex | `curriculum/chapter-04/student/04-ch4-friday-flex.md` | `production/releases/chapter-04/` | RELEASED | CUSTOM |
| P11 | Chapter Quiz | `production/quizzes/04-ch4-energy-transfer-quiz.docx` | `production/releases/chapter-04/` | RELEASED | ADAPTED |
| P12 | Teacher Keys | `production/answer-keys/04-ch4-*-key.md` (6) | `production/releases/chapter-04/` | RELEASED | SOURCE/ADAPTED |
| P13 | Media Plan + Scripts | `curriculum/chapter-04/media/` (plan + 5 scripts) | — | RELEASED | CUSTOM |
| P14 | Absent-Student Recovery | `curriculum/chapter-04/student/recovery/04-ch4-absent-student-recovery.md` | — | RELEASED | SOURCE/ADAPTED |
| P15 | QA Package (11 gates) | `curriculum/chapter-04/qa/` | — | RELEASED | CUSTOM |

> Chapter 4 is complete (Phase 6). Safe redesigns (no hot plate / wall outlet / chalk dust) recorded in `curriculum/chapter-04/source-map.md`. Chapters 5–7 to come (Phase 7+).

## Chapter 5 — Collisions Transfer Energy (Week 6, one-week chapter)

| ID | Artifact | Master path | Release path | Status | Provenance |
|---|---|---|---|---|---|
| P1 | Teacher Chapter Map | `curriculum/chapter-05/teacher/05-ch5-collisions-transfer-energy-teacher-map.md` | — | RELEASED | SOURCE/ADAPTED |
| P2 | Daily Lessons (Week 6) | `curriculum/chapter-05/teacher/05-ch5-daily-lessons-week6.md` | — | RELEASED | SOURCE/ADAPTED |
| P3 | Slide Deck | `production/slides/05-ch5-collisions-slides.pptx` | `production/releases/chapter-05/` | RELEASED | ADAPTED |
| P4 | Interactive Science Notebook | `production/student-notebook/chapter-05/05-ch5-interactive-notebook.docx` | `production/releases/chapter-05/05-ch5-interactive-science-notebook.pdf` | RELEASED | ADAPTED |
| P5 | Crash Lab Investigation | `production/labs/05-ch5-crash-lab-teacher-spec.md` + `production/worksheets/05-ch5-crash-lab-student.docx` | `production/releases/chapter-05/` | RELEASED | SOURCE/ADAPTED |
| P6 | Practice Worksheet | `production/worksheets/05-ch5-collisions-practice.docx` | `production/releases/chapter-05/` | RELEASED | ADAPTED |
| P7 | Friday Flex | `curriculum/chapter-05/student/05-ch5-friday-flex.md` | `production/releases/chapter-05/` | RELEASED | CUSTOM |
| P8 | Chapter Quiz | `production/quizzes/05-ch5-collisions-quiz.docx` | `production/releases/chapter-05/` | RELEASED | ADAPTED |
| P9 | Teacher Keys | `production/answer-keys/05-ch5-*-key.md` (3) | `production/releases/chapter-05/` | RELEASED | SOURCE/ADAPTED |
| P10 | Media Plan + Scripts | `curriculum/chapter-05/media/` (plan + 4 scripts) | — | RELEASED | CUSTOM |
| P11 | Absent-Student Recovery | `curriculum/chapter-05/student/recovery/05-ch5-absent-student-recovery.md` | — | RELEASED | SOURCE/ADAPTED |
| P12 | QA Package (11 gates) | `curriculum/chapter-05/qa/` | — | RELEASED | CUSTOM |

> Chapter 5 is complete (Phase 7). Two-part variable isolation (Part A speed · Part B mass/weight) + target-displacement measurement recorded in `curriculum/chapter-05/source-map.md`. Chapters 6–7 to come (Phase 8+).

## Chapter 6 — Energy Transformations + Engineering Design (Weeks 7–8, two-week chapter)

| ID | Artifact | Master path | Release path | Status | Provenance |
|---|---|---|---|---|---|
| P1 | Teacher Chapter Map | `curriculum/chapter-06/teacher/06-ch6-energy-transformations-teacher-map.md` | — | RELEASED | SOURCE/ADAPTED |
| P2 | Daily Lessons (W7 + W8) | `curriculum/chapter-06/teacher/06-ch6-daily-lessons-week{7,8}.md` | — | RELEASED | SOURCE/ADAPTED |
| P3 | Slide Deck | `production/slides/06-ch6-energy-transformations-slides.pptx` | `production/releases/chapter-06/` | RELEASED | ADAPTED |
| P4 | Interactive Science Notebook | `production/student-notebook/chapter-06/06-ch6-interactive-notebook.docx` | `production/releases/chapter-06/06-ch6-interactive-notebook.pdf` | RELEASED | ADAPTED |
| P5 | Engineering Capstone | `production/labs/06-ch6-engineering-capstone-teacher-spec.md` + `production/worksheets/06-ch6-engineering-performance-task.docx` (7 pages) | `production/releases/chapter-06/` | RELEASED | SOURCE/ADAPTED |
| P6 | Practice Worksheet | `production/worksheets/06-ch6-energy-transformations-practice.docx` | `production/releases/chapter-06/` | RELEASED | ADAPTED |
| P7 | Concept Checkpoint | `production/quizzes/06-ch6-concept-checkpoint.docx` | `production/releases/chapter-06/` | RELEASED | ADAPTED |
| P8 | Engineering Rubric | `production/rubrics/06-ch6-engineering-rubric.docx` (15-point) | `production/releases/chapter-06/` | RELEASED | ADAPTED |
| P9 | Friday Flex | `curriculum/chapter-06/student/06-ch6-friday-flex.md` | `production/releases/chapter-06/` | RELEASED | CUSTOM |
| P10 | Teacher Keys | `production/answer-keys/06-ch6-{practice,checkpoint,engineering,engineering-teacher}-key.md` | `production/releases/chapter-06/` | RELEASED | SOURCE/ADAPTED |
| P11 | Media Plan + Scripts | `curriculum/chapter-06/media/` (plan + 5 scripts) | — | RELEASED (scripts) / videos PENDING | CUSTOM |
| P12 | Absent-Student Recovery | `curriculum/chapter-06/student/recovery/06-ch6-absent-student-recovery.md` | — | RELEASED | SOURCE/ADAPTED |
| P13 | Student Exemplar | `curriculum/chapter-06/teacher/06-ch6-engineering-student-exemplar.md` | — | RELEASED | CUSTOM |
| P14 | QA Package (11 gates) | `curriculum/chapter-06/qa/` | — | RELEASED | CUSTOM |

> Chapter 6 is complete (Phase 8). Capstone = tabletop alert/signal device (ADAPTED — replaces source solar-oven default + wired doorbell; non-electrical, safe). Recorded in `curriculum/chapter-06/source-map.md`.

## Chapter 7 — Solving Problems and Designing Solutions: Thomas A. Edison (+ Unit Final) (Week 9)

| ID | Artifact | Master path | Release path | Status | Provenance |
|---|---|---|---|---|---|
| P1 | Teacher Chapter Map | `curriculum/chapter-07/teacher/07-ch7-edison-unit-synthesis-teacher-map.md` | — | RELEASED | SOURCE/ADAPTED |
| P2 | Daily Lessons (Week 9) | `curriculum/chapter-07/teacher/07-ch7-daily-lessons.md` | — | RELEASED | SOURCE/ADAPTED |
| P3 | Slide Deck (27) | `production/slides/07-ch7-edison-unit-synthesis-slides.pptx` | `production/releases/chapter-07/` | RELEASED | ADAPTED |
| P4 | Interactive Science Notebook (3 inserts) | `production/student-notebook/chapter-07/07-ch7-interactive-notebook.docx` | `production/releases/chapter-07/07-ch7-interactive-science-notebook.pdf` | RELEASED | ADAPTED/CUSTOM |
| P5 | Unit Synthesis Review | `production/worksheets/07-unit-synthesis-review.docx` | `production/releases/chapter-07/` | RELEASED | ADAPTED |
| P6 | Energy's Big Questions | `production/worksheets/07-energy-big-questions.docx` | `production/releases/chapter-07/` | RELEASED | ADAPTED |
| P7 | Final Assessment (25 items / 50 pts — Phase 13X rebuild) | `production/quizzes/07-unit-final-assessment.docx` | `production/releases/chapter-07/` + `production/releases/unit-final/` | RELEASED | ADAPTED |
| P8 | Final Assessment Key (DOCX/PDF) | `production/quizzes/07-unit-final-assessment-key.docx` | `production/releases/chapter-07/` + `production/releases/unit-final/` | RELEASED | ADAPTED |
| P9 | Scoring Guide | `production/quizzes/07-unit-final-assessment-scoring-guide.md` | `production/releases/unit-final/` | RELEASED | ADAPTED |
| P10 | Corrections / Recovery | `curriculum/chapter-07/student/recovery/07-final-assessment-corrections-recovery.md` | `production/releases/chapter-07/` + `production/releases/unit-final/` | RELEASED | CUSTOM |
| P11 | Absent-Student Recovery | `curriculum/chapter-07/student/recovery/07-ch7-absent-student-recovery.md` | — | RELEASED | SOURCE/ADAPTED |
| P12 | Friday Flex | `curriculum/chapter-07/student/07-friday-flex-unit-close.md` | `production/releases/chapter-07/` | RELEASED | CUSTOM |
| P13 | Media Plan + Scripts (5) | `curriculum/chapter-07/media/` | — | RELEASED (scripts) / videos PENDING | CUSTOM |
| P14 | QA Package (14 gates) | `curriculum/chapter-07/qa/` + `docs/reviews/PHASE_9_*` | — | RELEASED | CUSTOM |

> Chapter 7 + unit final complete (Phase 9). Original written final ADAPTED from the official 50-pt Unit Assessment blueprint. Media PENDING/UNSTAGED (Phase 10).

## Student Note Architecture (current)
- **Guided Notes are the PRIMARY structured student-note/reference artifact** (current standard: `docs/standards/GUIDED_NOTES_STANDARD.md`; decision record: `docs/planning/CURRENT_DECISIONS.md`).
- **Science Journal is SECONDARY** — predictions, phenomena, sketches, reflections, evidence, concept maps, engineering sketches, and optional creative/FLEX work.
- The former Interactive Science Notebook / glue-in architecture is **RETIRED for Chapter 1** (P11, archived) and must not be propagated as the primary note system. Its standards (`docs/planning/INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md`, `docs/planning/SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md`) and templates (`production/templates/student-notebook/`) are historical only.
- Chapter 2–7 notebook rows in this register are legacy entries pending their own phases; they do not change the architecture above.

## Phase 13B — Unit 2 "Using Natural Resources for Energy" + Final 8.5-Week Package

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| U2-A | Authoritative Teacher Guide (178 pp) | `assets/authoritative/unit-02/teacher-guide/` | RELEASED | SOURCE |
| U2-B | Authoritative Student Reader (64 pp) | `assets/authoritative/unit-02/student-reader/complete/` | RELEASED | SOURCE |
| U2-C | 9 chapter derivatives + Glossary | `assets/authoritative/unit-02/student-reader/chapters/` | RELEASED | SOURCE (qpdf extract) |
| U2-D | Premium guided notes Ch1–9 (DOCX+PDF) | `production/premium-notes/unit-02/` | RELEASED | ADAPTED |
| U2-E | Slideshow outlines Ch1–9 | `production/slides/outlines/unit-02/` | RELEASED | ADAPTED |
| U2-F | Video/explainer scripts (7) | `production/media/scripts/unit-02/UNIT2_VIDEO_SCRIPTS.md` | RELEASED (scripts) / videos PENDING | CUSTOM |
| U2-G | Water Wheel flagship lab (student + teacher) | `production/labs/unit-02/` | RELEASED | ADAPTED |
| U2-H | Unit 2 written assessment — student + key (25 items / 50 pts — Phase 13X rebuild) | `production/quizzes/unit-02/` | RELEASED | ADAPTED |
| U2-I | Activities (Detective Chart, Scenario, Sort, Fast & Curious, cookie-mining FLEX, certificate) | `production/activities/unit-02/` | RELEASED | ADAPTED/CUSTOM |
| U2-J | Friday Flex bank (8.5 weeks) | `production/friday-flex/FRIDAY_FLEX_BANK.md` | RELEASED | CUSTOM |
| U2-K | Master pacing · supply list · printing guide | `production/final-8.5-week/` | RELEASED | CUSTOM |
| U2-L | Media map · resource disposition · QA reports | `docs/planning/TWO_UNIT_MEDIA_MAP.md` · `docs/reviews/TWO_UNIT_RESOURCE_DISPOSITION.md` · `qa/reports/PHASE13B_*` | RELEASED | CUSTOM |

## Phase 13C — Final Hardening + Release (this phase)

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| V1 | Unit 2 slide decks Ch1–9 (9 PPTX) | `production/slides/01–09-u2-ch*.pptx` | RELEASED | ADAPTED |
| V2 | Energy Resource Detective Chart (2-page DOCX+PDF) | `production/activities/unit-02/energy-resource-detective-chart.{docx,pdf}` | RELEASED | ADAPTED |
| V3 | Transfer/Transformation/BOTH sort (mat + 15 cards + key) | `production/activities/unit-02/transfer-transformation-both-sort.{docx,pdf}` | RELEASED | CUSTOM |
| V4 | Scenario Challenge (cards + frame + key) | `production/activities/unit-02/energy-resource-scenario-challenge.{docx,pdf}` | RELEASED | CUSTOM |
| V5 | Fast & Curious (worksheet + key) | `production/activities/unit-02/fast-and-curious.{docx,pdf}` | RELEASED | ADAPTED |
| V6 | Chocolate-chip mining FLEX model | `production/activities/unit-02/chocolate-chip-mining-flex-model.{docx,pdf}` | FLEX | ADAPTED |
| V7 | Solar device mini-investigation sheet | `production/activities/unit-02/solar-device-mini-investigation.{docx,pdf}` | RELEASED | ADAPTED |
| V8 | Teacher Prep Guide | `production/final-8.5-week/TEACHER_PREP_GUIDE.md` | RELEASED | CUSTOM |
| V9 | Master Resource Index | `production/final-8.5-week/MASTER_RESOURCE_INDEX.md` | RELEASED | CUSTOM |
| V10 | Resource Completeness Audit | `docs/reviews/PHASE13C_RESOURCE_COMPLETENESS_AUDIT.md` | RELEASED | CUSTOM |
| V11 | Whole-track QA (science · controversial · visual · simulation) | `qa/reports/PHASE13C_RELEASE_QA.md` | RELEASED | CUSTOM |
| V12 | Slide/blueprint vocabulary cleanups (Ch4 outline "thermal energy" · Ch1 quiz blueprint "prove") | `production/slides/outlines/04-ch4-slideshow-outline.md` · `production/quizzes/01-ch1-energy-causes-change-quiz-blueprint.md` | RELEASED | ADAPTED |

> Unit 2 media (video scripts) remains **PENDING GENERATION** — not a release blocker (`docs/planning/TWO_UNIT_MEDIA_MAP.md`).

## Phase 13K — High-Value Gap Closure

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| K1 | Unit 2 absent-recovery index | `production/final-8.5-week/UNIT2_ABSENT_RECOVERY_INDEX.md` | RELEASED | CUSTOM |
| K2 | Unit 2 written study/review sheet (student + key, DOCX+PDF) | `production/review/unit-02/unit2-written-study-review.{docx,pdf}` + `unit2-written-study-review-key.{docx,pdf}` | RELEASED | ADAPTED |
| K3 | Teacher lab setup diagrams ×4 (DOCX+PDF) | `production/lab-setup-guides/{ramp-it-up,crash-lab,water-wheel,solar-device}-setup-guide.{docx,pdf}` | RELEASED | CUSTOM |
| K4 | Unit 1 assessment administration note | `production/final-8.5-week/UNIT1_ASSESSMENT_ADMINISTRATION_NOTE.md` | RELEASED | CUSTOM |
| K5 | Unit 1 review resource keys ×2 | `production/answer-keys/07-energy-big-questions-key.md` + `07-unit-synthesis-review-key.md` | RELEASED | SOURCE/ADAPTED |
| K6 | Retired curriculum artifact policy | `docs/architecture/RETIRED_CURRICULUM_ARTIFACT_POLICY.md` | RELEASED | CUSTOM |
| K7 | Master map/index/inventory/printing/prep sync | `production/final-8.5-week/` + quickstarts | RELEASED | CUSTOM |
| K8 | Gap-closure QA report | `qa/reports/PHASE13K_QA.md` | RELEASED | CUSTOM |

## Phase 13R — Final Infographic + Study Guide Reconciliation

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| R1 | Unit 1 study guide (student, DOCX+PDF, 3 pp) | `production/review/unit-01/unit1-study-guide.docx` + `.pdf` | RELEASED | ADAPTED |
| R2 | Unit 1 study guide teacher key (DOCX+PDF, 1 p) | `production/review/unit-01/unit1-study-guide-key.docx` + `.pdf` | RELEASED | SOURCE/ADAPTED |
| R3 | Infographic — Energy Detective anchor | `production/infographics/unit1-energy-detective-anchor.png` | RELEASED | ADAPTED |
| R4 | Infographic — Transfer vs Transformation | `production/infographics/unit1-transfer-vs-transformation.png` | RELEASED | ADAPTED |
| R5 | Infographic — Engineering design cycle | `production/infographics/unit1-engineering-design-cycle.png` | RELEASED | ADAPTED |
| R6 | Infographic — Collision energy transfer | `production/infographics/unit1-collision-energy-transfer.png` | RELEASED | ADAPTED |
| R7 | Infographic — Renewable vs nonrenewable matrix | `production/infographics/unit2-renewable-nonrenewable-resources.png` | RELEASED | ADAPTED |
| R8 | Infographic — Turbine/generator pathways | `production/infographics/unit2-turbine-generator-pathways.png` | RELEASED | ADAPTED |
| R9 | Infographic reference slides (×6 embedded) | `production/slides/` (01-ch1 S26 · 04-ch4 S47 · 05-ch5 S29 · 06-ch6 S45 · 01-u2-ch1 S22 · 03-u2-ch3 S20) | RELEASED | ADAPTED |
| R10 | Reconciliation review doc | `docs/reviews/PHASE13R_INFOGRAPHIC_STUDY_GUIDE_RECONCILIATION.md` | RELEASED | CUSTOM |
| R11 | QA report | `qa/reports/PHASE13R_QA.md` | RELEASED | CUSTOM |

> Rejected delivered sources: `Motion_Energy_Investigation_Matrix.png` (prefilled results), `4_Steps_of_Land_Reclamation.png` (not in course; teacher reference), combined `unit1-and-unit2-study-guide-review-worksheet.pdf` (split/rebuilt). Unit 2 review KEPT as existing Phase 13K sheet.

## Phase 13Z — Clickable Unit 1 Review Game Deck

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| Z1 | Unit 1 clickable Jeopardy review game (16:9 PPTX, 53 slides) | `production/review/unit-01/unit1-review-game.pptx` | RELEASED | ADAPTED |
| Z2 | Revised squad scorecard + Team Explain/Challenge cards (PDF) | `production/review/unit-01/unit1-review-game-scorecards.pdf` | RELEASED | ADAPTED |
| Z3 | Scorecard + cards editable masters | `production/review/unit-01/unit1-review-game-scorecards.docx` + `unit1-review-game-cards.docx` | RELEASED | ADAPTED |
| Z4 | Teacher answer key / game guide | `production/review/unit-01/unit1-review-game-guide.md` | RELEASED | SOURCE/ADAPTED |
| Z5 | Build + QA tooling | `tools/build_u1_review_game.js` · `tools/build_u1_review_scorecards.py` · `tools/qa_u1_review_game.py` · `tools/review_game_lib.js` (shared) · `tools/qa_review_game.py` (shared) · `tools/package.json` | RELEASED | CUSTOM |

> Board = 5 categories × 5 values (25 clues), fully clickable: tile → question → reveal answer → back to board. No external links or file dependencies. CER/Action-Stunt wording replaced with Team Explain / Team Challenge. All off-scope terms removed (kinetic, potential, mechanical/chemical/thermal energy, radiant, momentum, force, impulse, deformation, proves). (Phase 13AA refactored the deck + QA into shared builders; Unit 1 output verified byte-identical for all slide content and links.)

## Phase 13AA — Clickable Unit 2 Review Game + Review-Day Package

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| AA1 | Unit 2 clickable review game (16:9 PPTX, 55 slides incl. Final Challenge) | `production/review/unit-02/unit2-review-game.pptx` | RELEASED | ADAPTED |
| AA2 | Squad scorecard + Team Explain/Challenge cards (PDF, 3 pp) | `production/review/unit-02/unit2-review-game-scorecards.pdf` | RELEASED | ADAPTED |
| AA3 | Scorecard + cards editable masters | `production/review/unit-02/unit2-review-game-scorecards.docx` + `unit2-review-game-cards.docx` | RELEASED | ADAPTED |
| AA4 | Teacher answer key / game guide + source alignment | `production/review/unit-02/unit2-review-game-guide.md` | RELEASED | SOURCE/ADAPTED |
| AA5 | Build + QA + iPad capture tooling | `tools/build_u2_review_game.js` · `tools/build_u2_review_scorecards.py` · `tools/ipad_qa_u2_capture.py` (shared: `review_game_lib.js` · `qa_review_game.py`) | RELEASED | CUSTOM |

> Board = 5 categories × 5 values (25 clues) + a FINAL CHALLENGE button, fully clickable: tile → question → reveal answer → back to board. Categories: Resource Detective · Fossil Fuels · Turbines & Generators · Renewable Power · Resource Challenge. 3 arrow-chain visual questions (no answer leakage). Locked Unit 2 vocabulary avoided (fission, U-235, kinetic, mechanical/chemical/thermal energy, radiant, electron, photon, semiconductor, baseload, dispatch, grid stabilization, peak demand, climate change, global warming, carbon footprint, green/clean energy, zero emissions, policy, activism). Physical iPad (A16) capture verified.

## Phase 13AB — Final Study Guide Reconciliation + Assessment-Prep Certification

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| AB1 | Assessment-prep alignment matrix (Unit 1 + Unit 2, 25/25 each) | `docs/assessment/FINAL_ASSESSMENT_PREP_ALIGNMENT.md` | RELEASED | CUSTOM |
| AB2 | Unit 2 study/review sheet — hybrid concept added (Section D) + HR header standard | `production/review/unit-02/unit2-written-study-review.{docx,pdf}` + `-key.{docx,pdf}` | RELEASED | ADAPTED |
| AB3 | Study-guide iPad spot-check tooling | `tools/ipad_qa_studyguides.py` | RELEASED | CUSTOM |

> Unit 1 study guide verified aligned (25/25) — no change. Unit 2 study/review sheet revised to add the tested `hybrid` concept (final assessment Q20) via a single fill-in (no page bloat, 3 pp maintained) and the `Name + HR 4A 4B 4C 4D` header (no Date field). Both study guides scanned clean of off-scope vocabulary; physical iPad (A16) spot check verified both PDFs open crisply. Teacher prep + pacing updated to reference the clickable review game.

## Phase 13AC — Final Classroom Package Organization + Release Backup Preparation

| ID | Artifact | Path | Status | Provenance |
|---|---|---|---|---|
| AC1 | Teacher-facing delivery structure (relative-symlink tree: Energy / Natural Resources / Shared) | `production/final-delivery/` | RELEASED | CUSTOM |
| AC2 | Delivery builder (reproducible symlink + hash + mirror generator) | `tools/build_final_delivery.py` | RELEASED | CUSTOM |
| AC3 | Release hash manifest (SHA-256 + size) | `production/final-delivery/RELEASE_HASH_MANIFEST.csv` | RELEASED | CUSTOM |
| AC4 | Google Drive mirror metadata | `docs/reviews/GOOGLE_DRIVE_MIRROR_MANIFEST.md` | RELEASED | CUSTOM |
| AC5 | Teacher "Start Here" navigation guide | `production/final-delivery/START_HERE_TEACHER_GUIDE.md` | RELEASED | CUSTOM |

> Delivery view is symlink-only (no file duplication); single source of truth stays in `production/`. Dereference for Drive/USB with `cp -RL`. No classroom artifact was modified, copied, or regenerated in this phase.

## Provenance tags
`SOURCE` · `ADAPTED` · `CUSTOM` · `EXTENSION`
