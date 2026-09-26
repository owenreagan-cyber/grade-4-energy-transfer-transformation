# Grade 4 — Energy Transfer and Transformation

## Project name
Grade 4 Science Unit: **Energy Transfer and Transformation**

## Mission
Build a complete 8–9 week Grade 4 science curriculum system (Core Knowledge / CKSci-aligned) around Energy Transfer and Transformation, containing authoritative source references, chapter packages, teacher curriculum maps, presentations, guided notes, worksheets, labs, quizzes, enrichment, Friday Flex resources, assessments, engineering performance tasks, explainer-video scripts, media references, supply lists, answer keys, production specs, and QA standards.

## Current phase
**Phase 4.5 — Interactive Science Notebook System Alignment.** The primary student-note system is now the **Basic Interactive Science Notebook** (composition-book paste-ins), superseding flat guided-notes-only. Chapters 1–2 were retrofitted with notebook inserts + slide cue alignment and released. Chapter 3 (Phase 5) will use this system from the start.

## Status
- 65 source/asset files inventoried (Phase 0) + Chapter 4 derivative regenerated in Phase 1.
- All copies verified byte-for-byte (SHA-256) against originals; originals untouched.
- **Canonical Student Reader** locked = `Science 4 - Energy Transfer - Student Book.pdf` (backup copy retained).
- **22 architecture docs** authored under `docs/planning/` (curriculum, scope & sequence, labs, vocabulary, misconception map, assessment, standards, supply, formats, QA, Git, decisions).
- 3 AI drafts reviewed in `docs/reviews/PHASE_1_DRAFT_COMPATIBILITY.md` (all REBUILD, none used as-is).
- **Phase 2**: production templates (25) + QA checklists (12) + Git baseline established.
- **Phase 3**: Chapter 1 complete — teacher map, daily lessons, slide deck (22 slides, editable PPTX), guided notes, Energy Detectives investigation, practice, Friday Flex, quiz (9 items), 3 answer keys, media plan + explainer script, supply/prep, absent recovery, full QA (all PASS), release set in `production/releases/chapter-01/`.
- **Phase 4**: Chapter 2 complete — teacher map, daily lessons, slide deck (22 slides, editable PPTX), guided notes, Moving Marbles investigation, practice, Friday Flex, quiz (8 items), 3 answer keys, media plan + explainer script, supply/prep, absent recovery, full QA (all PASS), release set in `production/releases/chapter-02/`. Speed/mass comparisons correctly deferred to Chapter 3/5.
- **Phase 4.5**: Interactive Science Notebook system established (`docs/planning/INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md`); Chapters 1–2 retrofitted with 3 notebook inserts each + slide cue slides + release PDFs; all 8 QA gates PASS. Old guided-notes remain OPTIONAL (historical).
- See `SOURCE_INVENTORY.md` for the hash-verified manifest, `docs/reviews/PHASE_3_SYSTEM_VALIDATION.md` for the system validation verdict, `docs/reviews/PHASE_4_SYSTEM_CONSISTENCY.md` for the consistency review, and `docs/reviews/PHASE_4_5_NOTEBOOK_SYSTEM_VALIDATION.md` for the notebook-system validation.

## Authoritative sources
- **Student Reader** (complete): `assets/authoritative/student-reader/complete/` — "Science 4 - Energy Transfer - Student Book.pdf" (+ second-copy encoding).
- **Teacher Guide**: `assets/authoritative/teacher-guide/Science 4 - Energy Transfer - TG .pdf` (13 lessons across 7 chapters).
- **Official Activity Pages / Worksheets / Answer Key / Vocabulary**: `assets/authoritative/official-activity-pages/`.
- **Chapter splits (1–3, 5–7) + Glossary**: `assets/authoritative/student-reader/`.

> The chat-cited filenames `CKSci_G4UsingNaturalResources_SR.pdf` (Student Reader) and `CKSci_G4_U1_Energy_TG.pdf` (Teacher Guide) were not present under those names locally. Their content is preserved under the local Drive filenames listed above. Original filenames are preserved; none were silently renamed.

## High-level 9-week planning baseline (locked in Phase 1)
1. Ch.1 Energy Causes Change · 2. Ch.2 Moving Objects Have Energy · 3. Ch.3 Energy and Speed Are Related · 4. Ch.4 Part 1 (Sound + Light Transfer) · 5. Ch.4 Part 2 (Heat + Electricity + CER) · 6. Ch.5 Collisions Transfer Energy · 7. Ch.6 Part 1 (Transformations) · 8. Ch.6 Part 2 (Engineering Capstone = performance) · 9. Ch.7 Edison + synthesis + written assessment.
Full detail: `docs/planning/NINE_WEEK_SCOPE_SEQUENCE.md`.

## Directory map
```
assets/   authoritative · supplemental · drafts · staging   (consolidated sources)
curriculum/  unit + chapter-01..07 + assessment           (chapters 01–02 complete; 03–07 to come)
production/  slides · student-notes · student-notebook · worksheets · labs · quizzes · answer-keys · releases/chapter-0{1,2}
docs/     chat-history · planning · reviews · provenance
curriculum/chapter-0{1,2}/qa/   source-validation · cross-artifact-alignment · educational-suitability · classroom-simulation · acceptance-report
```

## Hard rule
**No generated artifact is authoritative merely because it looks polished.**
Do not call curriculum assets final/ready until **source, educational, visual, technical, and classroom-use QA** are all completed.
