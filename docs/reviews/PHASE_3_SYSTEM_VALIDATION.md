# Phase 3 System Validation

> Evaluates the Phase 2 production system against the Chapter 1 prototype build. Verdict per standard: KEEP / REVISE / RETIRE.

| # | Standard / template | Verdict | Evidence from Chapter 1 |
|---|---|---|---|
| 1 | CHAPTER MANIFEST | **KEEP** | Captured identity, source map, vocab, sequence, queue. Minor: add release-status field (done in manifest update). |
| 2 | SOURCE MAP | **KEEP** | Provenance (SOURCE/ADAPTED/CUSTOM/EXTENSION) held through all artifacts; no memory-fill needed. |
| 3 | SLIDE SPEC | **KEEP** | Per-slide table (purpose/core idea/visual/teacher move/student action/source/accessibility) produced a clean 22-slide deck. Slightly heavy but worth it. |
| 4 | NOTES TEMPLATE | **KEEP** | Produced usable Grade 4 notes with ruled writing space, no paragraph copying. |
| 5 | WORKSHEET TEMPLATE | **KEEP** | Landscape option + ruled lines gave enough writing space for the 6-column evidence model. |
| 6 | LAB TEMPLATE | **KEEP** | Teacher spec (materials/safety/prediction/fair-test/troubleshooting/absent) was sufficient. |
| 7 | QUIZ TEMPLATE | **KEEP** | Blueprint drove a balanced 9-item quiz (core/application/evidence). |
| 8 | ANSWER KEY TEMPLATE | **KEEP** | Expected/alternatives/reasoning/misconception/scoring columns supported grading. |
| 9 | QA CHECKLISTS | **KEEP** | Caught real issues: writing overload, prep bottleneck, 30-min split, media-verification gap. |
| 10 | RELEASE WORKFLOW | **KEEP** | Editable (docx/pptx) → LibreOffice QA render (pdf) → release copy was practical and repeatable. |
| 11 | FILE NAMING | **KEEP** | `NN-ch1-<slug>-<kind>` remained manageable across ~30 artifacts. |
| 12 | GIT | **KEEP** | Feature branch, checkpoint commits, clean tree, no remote. |

## Standards REVISED as a result of Chapter 1
1. **Slide density** → formalized: one core idea per slide; ≤3 short bullets on lab/direction slides; prediction-before-reveal required for demo slides.
2. **Writing-space requirement** → ruled answer lines (bottom-border) instead of blank boxes for Grade 4; minimum 2 lines for explain prompts.
3. **Table minimum row height** → 0.5" portrait data tables; 1.1" landscape investigation tables; header row shaded.
4. **Quiz length** → LOCKED at 8–12 items / 10–15 min / ~50% core, ~25% application, ~25% evidence (no forced prior-unit spiral).
5. **Friday Flex** → LOCKED 3-track (Recover/Practice/Extend) with no Week-2 dependency.

## Templates RETIRED
- None. All Phase 2 templates held up under the prototype build.
