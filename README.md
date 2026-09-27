# Grade 4 — Energy Transfer and Transformation

## Project name
Grade 4 Science Unit: **Energy Transfer and Transformation**

## Mission
Build a complete 8–9 week Grade 4 science curriculum system (Core Knowledge / CKSci-aligned) around Energy Transfer and Transformation, containing authoritative source references, chapter packages, teacher curriculum maps, presentations, guided notes, worksheets, labs, quizzes, enrichment, Friday Flex resources, assessments, engineering performance tasks, explainer-video scripts, media references, supply lists, answer keys, production specs, and QA standards.

## Current phase
**Phase 9 — Chapter 7 + Unit Synthesis + Final Assessment (COMPLETE).** The closing week (Week 9) delivers Edison/engineering persistence, whole-unit synthesis, an original written final (26 items / 50 pts) with key + scoring guide, corrections/recovery, Friday close, and 14 whole-unit QA gates. Chapters 1–7 are complete and RELEASED; the unit is instructionally complete. Media remains PENDING/UNSTAGED (Phase 10 — whole-unit media staging).

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
- **Phase 5**: Chapter 3 complete — teacher map, daily lessons, slide deck (28 slides), 3-insert notebook, Ramp It Up! 2.0 + Drop It investigations, practice, Friday Flex, quiz (10 items), 4 answer keys, media plan + 4 scripts, supply/prep, absent recovery, 10-gate QA (all PASS), release set in `production/releases/chapter-03/`. See `docs/reviews/PHASE_5_SYSTEM_CONSISTENCY.md`.
- **Phase 6**: Chapter 4 complete — two-week teacher map, Week 4 + Week 5 daily lessons, 46-slide deck, 5-insert notebook (transfer/transformation/BOTH flap), sound/light/heat/electricity investigations, practice, Friday Flex (both weeks), quiz (11 items), 6 answer keys, media plan + 5 scripts, supply/prep, absent recovery, 11-gate QA (all PASS), release set in `production/releases/chapter-04/`. Safe redesigns (no hot plate / wall outlet / chalk dust) documented in `curriculum/chapter-04/source-map.md`. See `docs/reviews/PHASE_6_SYSTEM_CONSISTENCY.md` and `docs/reviews/PHASE_6_MISCONCEPTION_AUDIT.md`.
- **Phase 7**: Chapter 5 complete — teacher map, Week 6 daily lessons, 28-slide deck, 3-insert notebook (lift-the-flap), Crash Lab (Part A speed · Part B mass/weight, target-displacement data), practice, Friday Flex, quiz (10 items), 3 answer keys, media plan + 4 scripts, supply/prep, absent recovery, 11-gate QA (all PASS), release set in `production/releases/chapter-05/`. Variable isolation documented in `curriculum/chapter-05/source-map.md`. Supplemental media (9 MP4s ~250 MB) + 2 review PDFs staged on-disk (git-ignored); metadata in `docs/planning/MEDIA_ASSET_MANIFEST.md`.
- **Phase 8**: Chapter 6 complete — teacher map, Week 7 + Week 8 daily lessons, 44-slide deck, 5-insert notebook (Test→Change→Retest flap), tabletop alert/signal-device engineering capstone (7-page task + 15-point rubric), practice, concept checkpoint (10 items), Friday Flex (both weeks), 4 answer keys, media plan + 5 scripts, supply/prep, absent recovery + student exemplar, 11-gate QA (all PASS), release set in `production/releases/chapter-06/`. Capstone ADAPTED from TG L13 (non-electrical, safe, weather-independent) — see `curriculum/chapter-06/source-map.md`. Supplemental Ch.1 slideshow (`Energy_Detectives.pptx`) staged on-disk (git-ignored); review in `docs/reviews/CH1_SUPPLEMENTAL_SLIDESHOW_REVIEW.md`. See `docs/reviews/PHASE_8_SYSTEM_CONSISTENCY.md` and `docs/reviews/PHASE_8_MISCONCEPTION_AUDIT.md`.
- **Phase 9**: Chapter 7 + Unit Final complete — teacher map, Week 9 daily lessons, 26-slide deck, 3-insert notebook (Engineering Cycle · Unit Concept Map · Reflection), unit synthesis review (3–4 pp), Energy's Big Questions, original written final (26 items / 50 pts) + key + scoring guide, corrections/recovery, absent recovery, Friday Flex, media plan + 5 scripts, 14-gate whole-unit QA (all PASS), release sets in `production/releases/chapter-07/` and `production/releases/unit-final/`. Original final ADAPTED from the official 50-pt Unit Assessment blueprint — see `curriculum/chapter-07/source-map.md`. Whole-unit alignment/regression/notebook reviews in `docs/reviews/PHASE_9_*`. Media PENDING/UNSTAGED (Phase 10).
- See `SOURCE_INVENTORY.md` for the hash-verified manifest and `docs/reviews/` for system validation/consistency reviews.

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
curriculum/  unit + chapter-01..07 + assessment           (chapters 01–07 complete)
production/  slides · student-notes · student-notebook · worksheets · labs · quizzes · rubrics · answer-keys · releases/chapter-0{1..7} · releases/unit-final
docs/     chat-history · planning · reviews · provenance
curriculum/chapter-0{1..6}/qa/   source-validation · cross-artifact-alignment · educational-suitability · data-quality · classroom-simulation · acceptance-report
```

## Hard rule
**No generated artifact is authoritative merely because it looks polished.**
Do not call curriculum assets final/ready until **source, educational, visual, technical, and classroom-use QA** are all completed.
