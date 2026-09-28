# PHASE 13C — WHOLE-TRACK RELEASE QA

> Automated scientific-scope sweep, controversial-content sweep, visual/projection QA, and
> 30-minute classroom simulation for the final 8.5-week Energy and Natural Resources package.
> Companion to `docs/reviews/PHASE13C_RESOURCE_COMPLETENESS_AUDIT.md`.

## 1. Scientific Scope QA (automated)

Swept **201 files** in `production/` (`.md`, `.txt`, `.docx`, `.pptx`) for the locked
out-of-scope / forbidden term set:

`proof` · `proves` · `kinetic` · `potential` · `mechanical energy` · `radiant` ·
`momentum` · `impulse` · `electron` · `compression wave` · `base-load` · `peak demand` ·
`grid stabilization` · `energy density` · `storeable` · `storable` · `thermal energy` ·
`chemical energy`.

### Result: PASS — zero illegal positive usage in student-facing material

Every match resolved into one of four benign classes:

| Class | Example | Verdict |
|---|---|---|
| **Negative guardrail** | `"Use 'supports' — NOT 'proves'"` (Ch6 slide 42) · `"use observed evidence (not 'proves')"` (rubric) · `"Use EVIDENCE, not proof"` (Ch7 Big Questions) | Intentional boundary teaching |
| **Substring false positive** | `geothermal energy` contains `thermal energy` · `improves` contains `proves` | Not a real match |
| **Teacher-only technical language** | `kinetic` / `potential` / `momentum` / `impulse` / `electron` / `radiant` / `compression wave` / `chemical energy` in teacher specs, answer keys, and blueprints only | Allowed by locked rule ("Teacher-only notes may use technical language when helpful") |
| **Historical changelog** | `PRODUCTION_MANIFEST.md` V12 note describing a past cleanup | Documentation, not curriculum |

**Student-facing confirmation:** no student worksheet, guided-note, slide deck, activity sheet,
or student assessment uses any forbidden term as required vocabulary. Unit 2 vocabulary is
locked to the permitted set (stored energy · energy of motion · heat · light · electric
current · transfer · transformation).

## 2. Controversial / Climate Content QA (automated)

Swept the same 201 files for:

`climate change` · `global warming` · `carbon footprint` · `carbon tax` · `cap and trade` ·
`climate crisis` · `climate activism` · `energy policy` · `community energy plan` ·
`sustainable community energy plan` · `mass & collision` · `mechanical motion`.

### Result: PASS — zero hits in production text

- No climate instruction, no political energy framing, no renewable/nonrenewable moral
  framing anywhere in student- or teacher-facing release material.
- Certificate (`energy-detective-certificate.docx`) confirmed clean: no `Mass & Collision`,
  no `Mechanical Motion`, no `community energy plan`, no climate reference; contains locked
  wording "Using fair tests to investigate speed and energy of motion" and
  "Tracing energy pathways through power systems".

## 3. Unit 2 Slide Deck QA (visual / projection)

All 9 decks rebuilt from `tools/build_u2_slides.py` and rendered headlessly
(LibreOffice → PDF). Page counts match slide counts; **no blank pages**, no overflow.

| Deck | Ch | Slides | Render pages |
|---|---|---|---|
| 01 renewable-nonrenewable | Ch1 | 20 | 20 |
| 02 types-of-fossil-fuels | Ch2 | 17 | 17 |
| 03 using-fossil-fuels | Ch3 | 18 | 18 |
| 04 nuclear-energy | Ch4 | 18 | 18 |
| 05 wind-energy | Ch5 | 15 | 15 |
| 06 hydroelectric-energy | Ch6 | 15 | 15 |
| 07 solar-energy | Ch7 | 16 | 16 |
| 08 geothermal-energy | Ch8 | 16 | 16 |
| 09 innovations | Ch9 | 17 | 17 |

**Back-of-room font floors verified:**
- Major/title-slide title: **48 pt** (floor 44)
- Slide titles: **38 pt** (floor 38)
- Body: **32 pt** (floor 30)
- Diagram/pathway labels: **26 pt** (floor 26)
- Review options: **28 pt**

**Pathway banners:** single full-width navy rounded bar with 26 pt gold/white arrow chain
(e.g. `WATER → DAM → TURBINE → GENERATOR → ELECTRICITY`), confirmed single-line in render —
no wrap, no overlap. Each deck follows the locked structure: title → Big Question →
phenomenon hook → guided-note teaching sequence → 4–6 MCQ review.

## 4. Unit 2 Activity Printable QA (DOCX + PDF)

Six print-ready artifacts built and exported to PDF via LibreOffice:

| Artifact | Pages | Notes |
|---|---|---|
| `energy-resource-detective-chart` | 2 | Page 1 nonrenewable · Page 2 renewable; Grade-4 language, no base-load/peak-demand/storeable |
| `energy-resource-scenario-challenge` | card + frame + key | fictional locations; "reasonable to investigate" framing, no policy question |
| `transfer-transformation-both-sort` | mat + 15 cards + key | 3 categories, teacher key included |
| `fast-and-curious` | worksheet + key | ramp height vs cup displacement; averages; measured vs inferred; "Relative Energy of Motion" |
| `chocolate-chip-mining-flex-model` | flex model | explicit "THIS IS A MODEL"; before/after sketch; qualitative disturbance; model-limits prompts; no ratio/calculations |
| `solar-device-mini-investigation` | data sheet | Wk 8 Thu; primary DV only |

## 5. 30-Minute Classroom Simulation

Reviewed via `docs/reviews/PHASE13C_RESOURCE_COMPLETENESS_AUDIT.md` day-by-day matrix
(8.5 weeks × 5 blocks) plus `qa/reports/PHASE13B_CLASSROOM_SIMULATION.md`. Each day verified
for launch → instruction → note-taking → activity → cleanup → exit check within ~30 min,
20 students / 5 groups of 4.

- **Thursday labs** (Moving Marbles, Ramp It Up, Crash Lab, Water Wheel, solar
  mini-investigation) sized for setup + testing + cleanup; graphing/explanation/redesign
  moved to Friday where needed.
- **Friday** is FLEX only (recover / practice / extend); no essential first exposure placed
  on Friday.
- **Same-object speed relationship** preserved throughout (Ramp It Up uses one ball,
  1/2/3-book ramps, repeated trials, cup displacement → average displacement; no invented
  m/s, no fake direct speed measurement).
- **Water Wheel** isolates a single independent variable (pour height) with one primary
  dependent variable (paperclips lifted); teacher connection = real hydroelectric
  turbines + generators.

## 6. Release Classification

| Artifact | Class |
|---|---|
| Master pacing, guided notes (U1 Ch1–7 · U2 Ch1–9), slide decks (U1 · U2), flagship labs, assessments + keys, certificate, supply list, printing guide, teacher prep guide, media map, master resource index, detective chart, scenario challenge, sort, Fast & Curious, solar sheet | **RELEASED** |
| Chocolate Chip Mining model | **FLEX** |
| Unit 2 + Unit 1 Ch3–7 video generation | **PENDING MEDIA** (not a release blocker) |

## Verdict

**All 8 gates pass.** No MUST-BUILD gaps remain. No forbidden scientific or controversial
content leaks into student-facing material. Slide decks and activity printables are render-,
print-, and projection-clean. The final 8.5-week package is release-ready.
