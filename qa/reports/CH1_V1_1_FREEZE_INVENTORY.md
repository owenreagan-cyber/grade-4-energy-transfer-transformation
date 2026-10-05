# CHAPTER 1 v1.1 FREEZE — ARTIFACT INVENTORY

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: `tools/qa_phase_inventory.py` on this file.
> External decision: **APPROVE PROPAGATION** (Phase 6.1J final audit). Status key: PASS · n/a · APPROVED.
> Type: **M** modified · **C** created · **A** affected-by-reference.
> Section 1 = artifacts changed by the freeze (metadata only). Section 2 = carry-forward by reference of every artifact in the Phase 6.1 → 6.1J inventory chain (`qa/reports/PHASE_6_1J_ARTIFACT_INVENTORY.md`), all covered by the external audit that returned the decision above.

## 1. Freeze changes (metadata only; classroom artifacts rebuilt: 0)

| Finding | Artifact | Type | Content QA | External audit |
|---|---|---|---|---|
| Declaration 1.1 / FROZEN; approval record; history preserved | `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md` | M | PASS | APPROVED |
| Package status text; Playbook row notes the Ch2-commit exception | `docs/chapter-01/CH1_PACKAGE_MANIFEST.md` | M | PASS | APPROVED |
| Register rows P1, P3, P13 + lifecycle note | `production/PRODUCTION_MANIFEST.md` | M | PASS (guard 43/43 allowlisted) | APPROVED |
| Master index rows | `production/final-package/ENERGY_UNIT_MASTER_INDEX.md` | M | PASS | APPROVED |
| Release manifest version/status (no release file touched) | `production/releases/chapter-01/RELEASE_MANIFEST.json` · `production/releases/chapter-01/README.md` | C | PASS (release parity 14 gates) | APPROVED |
| Builder constants (VERSION 1.1 / STATUS FROZEN); builder not run | `tools/build_ch1_release.py` | C | PASS | APPROVED |
| Reviewed allowlist row for manifest row P3 (status text only; same classification; 42 entries) | `qa/baselines/ch1_note_architecture_allowlist.json` | C | PASS (43 sensitive / 43 allowlisted / 0 unreviewed / 0 stale / 0 auto-safe) | APPROVED |
| Round 11 freeze approval | `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | C | n/a | APPROVED |
| Final certification + inventory | `qa/reports/CH1_V1_1_FREEZE_CERTIFICATION.md` · `qa/reports/CH1_V1_1_FREEZE_INVENTORY.md` · `qa/reports/CH1_V1_1_FREEZE_INVENTORY_COMPLETENESS.md` | C | PASS | APPROVED |

> Playbook exception (owner decision 2026-10-05): the combined Playbook binary and previews are accounted for in the Section 2 chain but are **not** in the Chapter 1 freeze commit (they ship with the Ch2 commit); the committed `tools/build_teacher_playbook.py` and `tools/qa_teacher_playbook.py` carry the Chapter 1 hunks only.

## 2. Carry-forward by reference (Phase 6.1 → 6.1J chain)

- `.cursor/rules/00-project-governance.mdc`
- `.cursor/rules/30-qa-and-release.mdc`
- `AGENTS.md`
- `PHASE_6_1_PLAYBOOK_QA.md`
- `README.md`
- `curriculum/chapter-01/CHAPTER_MANIFEST.md`
- `curriculum/chapter-01/README.md`
- `curriculum/chapter-01/media/*`
- `curriculum/chapter-01/qa/*.md`
- `curriculum/chapter-01/source-map.md`
- `curriculum/chapter-01/student/01-ch1-friday-flex.md`
- `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md`
- `curriculum/chapter-01/teacher/01-ch1-daily-lessons.md`
- `curriculum/chapter-01/teacher/01-ch1-energy-causes-change-teacher-map.md`
- `curriculum/chapter-01/teacher/01-ch1-supply-prep-guide.md`
- `curriculum/chapter-01/teacher/01-ch1-teacher-notes.md`
- `docs/agent-workflows/PHASE_PIPELINE.md`
- `docs/chapter-01/CH1_ASSESSMENT_TRACE.md`
- `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`
- `docs/chapter-01/CH1_GOLD_STANDARD_PROPAGATION_SPEC.md`
- `docs/chapter-01/CH1_PACING_PLAN.md`
- `docs/chapter-01/CH1_PACKAGE_MANIFEST.md`
- `docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md`
- `docs/chapter-01/CH1_SLIDESHOW_MANIFEST.md`
- `docs/chapter-01/CH1_STUDY_GUIDE_CONTRIBUTION.md`
- `docs/planning/CURRENT_DECISIONS.md`
- `docs/planning/FRIDAY_FLEX_FRAMEWORK.md`
- `docs/planning/INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md`
- `docs/planning/QA_GATES.md`
- `docs/planning/SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md`
- `docs/planning/STUDENT_NOTES_STANDARD.md`
- `docs/playbook/UNIT1_PACING_CALENDAR.md`
- `docs/playbook/UNIT1_RESOURCE_MAP.md`
- `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md`
- `docs/reviews/GROK_CH1_V1_1_AUDIT_PACKET.md`
- `docs/reviews/GROK_CH1_V1_1_AUDIT_PROMPT.md`
- `docs/reviews/PHASE_6_1_CH1_EXTERNAL_AUDIT_REMEDIATION.md`
- `production/PRODUCTION_MANIFEST.md`
- `production/answer-keys/01-ch1-energy-causes-change-practice-key.md`
- `production/answer-keys/01-ch1-energy-causes-change-quiz-key.md`
- `production/answer-keys/01-ch1-energy-detectives-key.md`
- `production/archive/retired/chapter-01-release-v1.0/*`
- `production/final-8.5-week/ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md`
- `production/final-8.5-week/MASTER_CURRICULUM_MAP.md`
- `production/final-8.5-week/MASTER_RESOURCE_INDEX.md`
- `production/final-8.5-week/MASTER_RESOURCE_INVENTORY.md`
- `production/final-8.5-week/VIDEO_PRESENTATION_INTEGRATION_MATRIX.md`
- `production/final-8.5-week/WEEK1_2_TEACHER_QUICKSTART.md`
- `production/final-delivery/Energy/Unit 1 *`
- `production/final-delivery/RELEASE_HASH_MANIFEST.csv`
- `production/final-package/ENERGY_UNIT_MASTER_INDEX.md`
- `production/final-package/ENERGY_UNIT_WEEK_BY_WEEK_TEACHER_MAP.md`
- `production/friday-flex/FRIDAY_FLEX_BANK.md`
- `production/labs/01-ch1-energy-detectives-teacher-spec.md`
- `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.docx`
- `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.pdf`
- `production/premium-notes/01-ch1-energy-causes-change-guided-notes.docx`
- `production/premium-notes/01-ch1-energy-causes-change-guided-notes.pdf`
- `production/premium-notes/previews/ch1-notes-*.png`
- `production/premium-notes/previews/ch1-notes-key-*.png`
- `production/premium-notes/previews/ch1-notes-student-*.png`
- `production/quizzes/01-ch1-energy-causes-change-quiz-blueprint.md`
- `production/quizzes/01-ch1-energy-causes-change-quiz.docx`
- `production/quizzes/01-ch1-energy-causes-change-quiz.pdf`
- `production/releases/chapter-01/*`
- `production/releases/chapter-01/01-ch1-friday-flex.pdf`
- `production/slides/01-ch1-energy-causes-change-slides.pdf`
- `production/slides/01-ch1-energy-causes-change-slides.pptx`
- `production/slides/previews/ch1-slides-*.png`
- `production/teacher-playbook/previews/playbook-*.png`
- `production/teacher-playbook/unit1-teacher-playbook.docx`
- `production/teacher-playbook/unit1-teacher-playbook.pdf`
- `production/worksheets/01-ch1-energy-causes-change-practice.docx`
- `production/worksheets/01-ch1-energy-causes-change-practice.pdf`
- `production/worksheets/01-ch1-energy-detectives-student.docx`
- `production/worksheets/01-ch1-energy-detectives-student.pdf`
- `qa/baselines/ch1_note_architecture_allowlist.json`
- `qa/reports/PHASE_2_PLAYBOOK_QA.md`
- `qa/reports/PHASE_3_CH1_GUIDED_NOTES_QA.md`
- `qa/reports/PHASE_4_CH1_SLIDESHOW_QA.md`
- `qa/reports/PHASE_6_1B_*`
- `qa/reports/PHASE_6_1C_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1C_CH1_GUIDED_NOTES_QA.md`
- `qa/reports/PHASE_6_1C_CH1_RELEASE_PARITY.md`
- `qa/reports/PHASE_6_1C_CH1_SLIDESHOW_QA.md`
- `qa/reports/PHASE_6_1C_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1C_CH1_VISUAL_QA.md`
- `qa/reports/PHASE_6_1C_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1C_PLAYBOOK_QA.md`
- `qa/reports/PHASE_6_1D_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1D_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1D_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1E_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1E_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1E_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1F_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1F_CH1_CONTENT_STALE_SCAN.md`
- `qa/reports/PHASE_6_1F_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1F_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1G_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1G_CH1_CONTENT_STALE_SCAN.md`
- `qa/reports/PHASE_6_1G_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1G_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1H_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1H_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1H_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1I_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1I_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1I_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1J_ARTIFACT_INVENTORY.md`
- `qa/reports/PHASE_6_1J_CH1_STALE_REFERENCE_SCAN.md`
- `qa/reports/PHASE_6_1J_INVENTORY_COMPLETENESS.md`
- `qa/reports/PHASE_6_1_*`
- `qa/reports/PHASE_6_1_CH1_CLASSROOM_TIME_SIMULATION.md`
- `qa/reports/PHASE_6_1_INVENTORY_COMPLETENESS.md`
- `qa/visual/phase6_1/*`
- `qa_phase_inventory.py`
- `qa_visual_system.py`
- `tools/build_ch1_assessments.py`
- `tools/build_ch1_guided_notes.py`
- `tools/build_ch1_release.py`
- `tools/build_ch1_slides.py`
- `tools/build_teacher_playbook.py`
- `tools/ch1_pacing.py`
- `tools/export_pdf_previews.py`
- `tools/gen_ch1_pacing_plan.py`
- `tools/pdf_page_ink.py`
- `tools/qa_ch1_assessments.py`
- `tools/qa_ch1_guided_notes.py`
- `tools/qa_ch1_note_architecture.py`
- `tools/qa_ch1_note_architecture_negative_tests.py`
- `tools/qa_ch1_slides.py`
- `tools/qa_ch1_stale_refs.py`
- `tools/qa_notebook_primary_fixture.py`
- `tools/qa_phase_inventory.py`
- `tools/qa_release_parity.py`
- `tools/qa_render_geometry.py`
- `tools/qa_teacher_playbook.py`
- `tools/qa_visual_pdf.py`
