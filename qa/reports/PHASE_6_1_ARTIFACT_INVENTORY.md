# PHASE 6.1 — ARTIFACT INVENTORY (Chapter 1 external-audit remediation)

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: `tools/qa_phase_inventory.py` (every changed Ch1-scope path must be covered by a row below).
> Status key — **Content QA / Visual QA / Key parity / Release parity**: PASS · n/a · PENDING. **External audit**: `PENDING-GROK` = included in `docs/reviews/GROK_CH1_V1_1_AUDIT_PACKET.md`; Grok is read-only and has not yet returned a verdict (see §Status).
> Type: **C** created · **M** modified · **A** affected-by-reference (content unchanged, references checked/updated in text only where listed).
> Paths with `*` are glob groups.

## 1. Student-facing artifacts

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes.docx` | M | Student | PASS (`PHASE_6_1_CH1_GUIDED_NOTES_QA`) | PASS (3 pp) | PASS (key matches blanks) | n/a (PDF released) | PENDING-GROK |
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes.pdf` | M | Student | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |
| `production/premium-notes/previews/ch1-notes-student-*.png` | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `production/worksheets/01-ch1-energy-causes-change-practice.docx` | M | Student | PASS (`PHASE_6_1_CH1_ASSESSMENT_QA`) | PASS (2 pp) | PASS | n/a | PENDING-GROK |
| `production/worksheets/01-ch1-energy-causes-change-practice.pdf` | C | Student | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |
| `production/quizzes/01-ch1-energy-causes-change-quiz.docx` | M | Student | PASS | PASS (2 pp) | PASS (9 items / 16 pts) | n/a | PENDING-GROK |
| `production/quizzes/01-ch1-energy-causes-change-quiz.pdf` | C | Student | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |
| `production/worksheets/01-ch1-energy-detectives-student.docx` | M | Student (optional) | PASS | PASS (2 pp) | PASS | n/a | PENDING-GROK |
| `production/worksheets/01-ch1-energy-detectives-student.pdf` | C | Student (optional) | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |

## 2. Projected artifacts

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/slides/01-ch1-energy-causes-change-slides.pptx` | M | Projected | PASS (`PHASE_6_1_CH1_SLIDESHOW_QA`, 28 gates) | PASS (geometry, tiers, 45 slides) | PASS (reveal answers = key) | PASS (identical copy) | PENDING-GROK |
| `production/slides/01-ch1-energy-causes-change-slides.pdf` | M | Projected | PASS | PASS (45/45) | n/a | PASS (identical copy) | PENDING-GROK |
| `production/slides/previews/ch1-slides-*.png` (45) | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `tools/build_ch1_slides.py` (speaker notes TIME/PLAN lines from `tools/ch1_pacing.py`) | M | Builder | PASS | n/a | n/a | n/a | PENDING-GROK |

## 3. Teacher-facing artifacts

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.docx`, `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.pdf` | M | Teacher | PASS | PASS (3 pp) | PASS (all 5 blanks + samples) | PASS (PDF identical copy) | PENDING-GROK |
| `production/premium-notes/previews/ch1-notes-key-*.png` | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `production/answer-keys/01-ch1-energy-causes-change-quiz-key.md` | M | Teacher | PASS (explicit YES/NO/YES; exact MC options; refs corrected) | n/a | PASS | PASS (derived into bundle PDF) | PENDING-GROK |
| `production/answer-keys/01-ch1-energy-causes-change-practice-key.md` | M | Teacher | PASS (book-on-table science corrected; no unsupported battery) | n/a | PASS | PASS (derived) | PENDING-GROK |
| `production/answer-keys/01-ch1-energy-detectives-key.md` | M | Teacher | PASS (ungraded look-fors) | n/a | PASS | PASS (derived) | PENDING-GROK |
| `production/quizzes/01-ch1-energy-causes-change-quiz-blueprint.md` | M | Teacher | PASS (points, note policy, refs) | n/a | PASS | n/a | PENDING-GROK |
| `production/labs/01-ch1-energy-detectives-teacher-spec.md` | M | Teacher | PASS | n/a | n/a | n/a | PENDING-GROK |
| `production/teacher-playbook/unit1-teacher-playbook.docx`, `production/teacher-playbook/unit1-teacher-playbook.pdf` | M | Teacher | PASS (`PHASE_6_1_PLAYBOOK_QA`, Ch1 sync gate) | PASS pp. 1–21 (Ch1 scope); 3 pre-existing out-of-scope WARN (pp. 22–33) | n/a | n/a | PENDING-GROK |
| `production/teacher-playbook/previews/playbook-*.png` | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `tools/build_teacher_playbook.py`, `tools/qa_teacher_playbook.py` | M | Builder | PASS | n/a | n/a | n/a | PENDING-GROK |
| `qa/reports/PHASE_2_PLAYBOOK_QA.md` | A | Record | historical (was already modified before Phase 6.1; superseded by `PHASE_6_1_PLAYBOOK_QA.md`) | n/a | n/a | n/a | PENDING-GROK |

## 4. Release package

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/releases/chapter-01/*` (9 files + `RELEASE_MANIFEST.json` + `README.md`) | M/C | Teacher/Student | PASS (stale-language scan) | PASS (derived PDFs) | PASS | **PASS** (`PHASE_6_1_CH1_RELEASE_PARITY_QA`) | PENDING-GROK |
| `production/archive/retired/chapter-01-release-v1.0/*` | C | Archive | n/a | n/a | n/a | PASS (retired files excluded from release) | PENDING-GROK |
| `production/final-delivery/RELEASE_HASH_MANIFEST.csv` (Ch1 rows only) | M | Delivery index | n/a | n/a | n/a | PASS (rows == live hashes) | PENDING-GROK |
| `production/final-package/ENERGY_UNIT_MASTER_INDEX.md`, `production/PRODUCTION_MANIFEST.md` | M | Index | PASS (`PHASE_6_1_CH1_STALE_REFERENCE_SCAN`) | n/a | n/a | n/a | PENDING-GROK |

## 5. Pacing, manifests, traces (docs)

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `docs/chapter-01/CH1_PACING_PLAN.md` | C | Teacher/agents | PASS (`check_plan()`; simulation) | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_PACKAGE_MANIFEST.md` | M | Agents | PASS (stale scan) | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_SLIDESHOW_MANIFEST.md`, `docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md` | M | Agents | PASS | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_ASSESSMENT_TRACE.md`, `docs/chapter-01/CH1_STUDY_GUIDE_CONTRIBUTION.md` | M | Agents | PASS (F13 refs) | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`, `docs/chapter-01/CH1_GOLD_STANDARD_PROPAGATION_SPEC.md` | M | Agents | PASS | n/a | n/a | n/a | PENDING-GROK |
| `docs/playbook/UNIT1_PACING_CALENDAR.md`, `docs/playbook/UNIT1_RESOURCE_MAP.md` | M | Teacher/agents | PASS | n/a | n/a | n/a | PENDING-GROK |
| `production/final-8.5-week/MASTER_CURRICULUM_MAP.md`, `production/final-8.5-week/WEEK1_2_TEACHER_QUICKSTART.md` | M | Teacher | PASS | n/a | n/a | n/a | PENDING-GROK |
| `production/final-8.5-week/MASTER_RESOURCE_INDEX.md`, `production/final-8.5-week/ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md`, `production/final-8.5-week/MASTER_RESOURCE_INVENTORY.md`, `production/final-8.5-week/VIDEO_PRESENTATION_INTEGRATION_MATRIX.md`, `production/final-package/ENERGY_UNIT_WEEK_BY_WEEK_TEACHER_MAP.md`, `production/friday-flex/FRIDAY_FLEX_BANK.md` | M | Teacher (Ch1 schedule sync, N1) | PASS (stale scan) | n/a | n/a | n/a | PENDING-GROK |
| `docs/planning/CURRENT_DECISIONS.md`, `docs/planning/FRIDAY_FLEX_FRAMEWORK.md` | M | Governance (owner Friday policy 2026-10-04, DECIDED) | n/a | n/a | n/a | n/a | PENDING-GROK |
| `qa/reports/PHASE_6_1_CH1_CLASSROOM_TIME_SIMULATION.md` | C | Record | PASS | n/a | n/a | n/a | PENDING-GROK |
| `qa/reports/PHASE_6_1_INVENTORY_COMPLETENESS.md` | C | Record (output of `qa_phase_inventory.py`) | PASS | n/a | n/a | n/a | PENDING-GROK |

## 6. Legacy / support content

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `curriculum/chapter-01/student/01-ch1-friday-flex.md` | M | Teacher/student | PASS (cards listed inline; Detectives optional) | PASS (derived release PDF) | n/a | PASS (derived) | PENDING-GROK |
| `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md` | M | Student (absent) | PASS (5 blanks; no re-copy of printed text) | n/a | n/a | n/a | PENDING-GROK |
| `curriculum/chapter-01/README.md`, `curriculum/chapter-01/qa/*.md`, `curriculum/chapter-01/teacher/01-ch1-daily-lessons.md`, `curriculum/chapter-01/teacher/01-ch1-energy-causes-change-teacher-map.md`, `curriculum/chapter-01/teacher/01-ch1-supply-prep-guide.md` | M (SUPERSEDED banner only) | Archive | n/a (body untouched) | n/a | n/a | n/a | PENDING-GROK |
| `curriculum/chapter-01/CHAPTER_MANIFEST.md`, `curriculum/chapter-01/source-map.md`, `curriculum/chapter-01/teacher/01-ch1-teacher-notes.md`, `curriculum/chapter-01/media/*` | A | Archive | unchanged (already SUPERSEDED / source record) | n/a | n/a | n/a | PENDING-GROK |
| `production/final-delivery/Energy/Unit 1 *` (symlinks to canonical) | A | Delivery | resolve to current masters; legacy Teacher Guide copies are SUPERSEDED-bannered | n/a | n/a | PASS (CSV) | PENDING-GROK |

## 7. Tools and QA reports (created/modified)

| Artifact | Type | Notes | External audit |
|---|---|---|---|
| `tools/ch1_pacing.py` | C | single pacing data source | PENDING-GROK |
| `tools/gen_ch1_pacing_plan.py` | C | writes the pacing plan + simulation | PENDING-GROK |
| `tools/build_ch1_guided_notes.py`, `tools/qa_ch1_guided_notes.py` | M | notes fixes + new gates | PENDING-GROK |
| `tools/qa_ch1_slides.py` | M | new gates | PENDING-GROK |
| `tools/build_ch1_assessments.py`, `tools/qa_ch1_assessments.py` | C | practice/quiz/Detectives builder + QA | PENDING-GROK |
| `tools/build_ch1_release.py`, `tools/qa_release_parity.py` | C | reusable release build + parity QA | PENDING-GROK |
| `tools/qa_ch1_stale_refs.py`, `tools/qa_phase_inventory.py` | C | stale-reference scan; inventory completeness | PENDING-GROK |
| `tools/qa_visual_pdf.py`, `tools/qa_render_geometry.py`, `tools/pdf_page_ink.py`, `tools/export_pdf_previews.py` | C | reusable visual QA + export helpers | PENDING-GROK |
| `qa/reports/PHASE_6_1_*` (notes, slides, assessments, playbook, release parity, stale scan, visual, simulation, inventory) | C | evidence | PENDING-GROK |
| `qa/visual/phase6_1/*` | C | rendered review PNGs | PENDING-GROK |

## 8. Governance and review docs (created/modified)

| Artifact | Type | External audit |
|---|---|---|
| `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | C | PENDING-GROK |
| `docs/reviews/PHASE_6_1_CH1_EXTERNAL_AUDIT_REMEDIATION.md` | C | PENDING-GROK |
| `docs/reviews/GROK_CH1_V1_1_AUDIT_PACKET.md`, `docs/reviews/GROK_CH1_V1_1_AUDIT_PROMPT.md` | C | n/a (the audit input) |
| `AGENTS.md`, `.cursor/rules/30-qa-and-release.mdc`, `.cursor/rules/00-project-governance.mdc`, `docs/planning/QA_GATES.md`, `docs/agent-workflows/PHASE_PIPELINE.md` | M/C | PENDING-GROK |

## 9. Not touched (explicit)

Chapters 3–7 artifacts; Unit 1 Visual System v1.0 (`qa_visual_system.py` PASS, tokens unchanged); locked Unit 1 final assessment; authoritative CKSci sources. Chapter 2 files that appear modified in the working tree belong to the separate Phase 7 work and were **not** edited by Phase 6.1 (the Playbook's shared `_page_break` helper change affects Ch2 page layout only by removing blank-page risk; Ch2 text unchanged).

## 10. Status

- Internal gates: see `docs/reviews/PHASE_6_1_CH1_EXTERNAL_AUDIT_REMEDIATION.md`.
- External audit: **not yet returned**. Every row above is `PENDING-GROK`; the freeze to v1.1 is therefore **not** performed.
