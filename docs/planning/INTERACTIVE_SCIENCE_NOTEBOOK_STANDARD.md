# INTERACTIVE SCIENCE NOTEBOOK STANDARD

> ⚠️ **RETIRED / HISTORICAL (Phase 0A.1).** The Interactive Science Notebook-primary architecture is retired. **Guided Notes are PRIMARY; Science Journal is SECONDARY.** Current authoritative standard: `docs/standards/GUIDED_NOTES_STANDARD.md`. This file is retained for historical reference only — do not use it to author new student artifacts.

## SYSTEM NAME
**Student Interactive Science Notebook**

Student-facing unit title:
> **Energy Transfer & Transformation — Interactive Science Notebook**

## PURPOSE
Provide a practical, cumulative, composition-book notebook that captures the full 8–9 week unit. It is a **learning tool**, not a craft project. Drawing, labeling, models, evidence, and short explanations are the primary modes; interactive elements are selective.

## STUDENT EXPERIENCE
- Most pages are simple paste-ins (flat inserts, trim-and-glue pieces, drawing boxes, fill-ins, diagrams, evidence tables).
- Students draw and label often; drawing is a major learning mode.
- Students are NOT required to copy long paragraphs.
- Interactive features (flaps, foldables, pockets, sort-and-glue) appear only when they serve the science.

## PAGE TYPES (standard set)
| Code | Type | Use |
|---|---|---|
| A | VOCAB + DRAW | short fill-in/definition + large drawing box + label |
| B | BEFORE / AFTER MODEL | two drawing frames + "what changed?" line |
| C | EVIDENCE PAGE | NOTICE / EVIDENCE / EXPLAIN / CONNECT |
| D | DATA / GRAPH PAGE | lab table + graph + short conclusion |
| E | LIFT-THE-FLAP | outside question/old idea → inside correct model |
| F | SORT-AND-GLUE | sparingly; pieces must fit cleanly |
| G | ENGINEERING INSERT | later phases only (criteria/constraints/blueprint/test/redesign) |

## VOCABULARY FORMAT
- Short fill-in definition + a drawing/example + a label.
- Grade 4 wording only; no advanced terminology (kinetic/potential/mechanical/radiant/electron mechanics).

## DRAWING FORMAT
- Large drawing boxes; arrows encouraged.
- Slides show suggested drawing ideas + one completed example.
- Student drawings do not need to match the example exactly.

## INTERACTIVE ELEMENT RULES
- Default maximum: **~1 meaningful interactive feature per chapter**.
- More than one requires an explicit instructional justification.
- Each interactive feature needs a **low-motor accessibility alternative** (pre-cut copy or flat equivalent).
- Science mastery must never depend on cutting/folding skill.

## NOTICE / EVIDENCE / EXPLAIN / CONNECT
- Use as a recurring thinking routine where appropriate.
- Do NOT force all four labels onto every page; use enough that students recognize the routine.

## RECURRING SCIENCE MODELS
- Chapter 1: `ENERGY → CHANGE → EVIDENCE`
- Chapter 2: `MOVING OBJECT → CAUSES CHANGE → EVIDENCE OF ENERGY`
- Later chapters may extend these; do not introduce future concepts early merely to complete a graphic.

## SLIDE-TO-NOTEBOOK MODELING
- Slides support notebook completion directly (see `SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md`).
- For each notebook-writing moment, slides show: page title/icon · exact fill-in answer (reveal) · one drawing idea · where to write/draw · teacher pause cue.
- Labels: `NOTEBOOK` · `WRITE` · `DRAW` · `LABEL` · `CHECK`.

## COMPOSITION BOOK DIMENSIONS / SAFE AREA
- Standard composition book: **9.75" × 7.5"**.
- Usable page after binding: ~**9.75" wide × 7.0" tall**, with a **0.5" binding gutter** on the left (right page) or right (left page).
- All inserts must fit within a **7.0" × 9.0" safe area** leaving the gutter clear.
- Full-page inserts trimmed to ~**7.0" × 9.0"**; half-page inserts ~**7.0" × 4.25"** (glued across the top or side).

## TRIM / GLUE RULES
- Print on ordinary classroom copier paper (20 lb), single-sided.
- Provide clear **trim lines** (dashed border) and labeled **GLUE area**.
- Glue areas are a thin strip (top edge for half-page; top or left edge for full-page).
- Avoid loose pieces that easily disappear; every glued piece has a defined home.

## WRITING SPACE
- Grade 4 handwriting space: ruled answer lines, ≥2 lines for explanations.
- No paragraph copying.

## ACCESSIBILITY
- Every interactive feature has a pre-cut or flat alternative.
- Grayscale-safe (no color-dependent meaning); high contrast.

## ABSENT STUDENT HANDLING
- See `NOTEBOOK_ABSENT_STUDENT_WORKFLOW.md`.
- Absent students receive: missed insert + completed slide model + class/sample data + optional pre-cut piece.

## QA REQUIREMENTS
- Run the 8-gate QA (Source Validation, Content Priority, Cross-Artifact Alignment, Educational Suitability, Visual/Layout, Technical, Physical Notebook Usability, Classroom Simulation) before any notebook release.
- Physical Notebook Usability is mandatory: trim size, fit, binding clearance, glue areas, fold direction, flap clearance, page thickness.

## FILE NAMING
- Notebook masters: `NN-chN-<shortname>-interactive-notebook.docx` under `production/student-notebook/chapter-0N/`.
- Release PDF: `NN-chN-<shortname>-interactive-science-notebook.pdf` under `production/releases/chapter-0N/`.
- Page-spec files: `NN-chN-<shortname>-notebook-page-<page>.md` under `curriculum/chapter-0N/notebook/`.

## RELEASE RULES
- Notebook release is separate from guided-notes release.
- Old guided-notes PDFs become `OPTIONAL` (historical) unless otherwise noted; editable masters are retained.
- No notebook release until all gates PASS.
