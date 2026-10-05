# CURRENT DECISIONS

> Phase 3 state. Full registers: `docs/planning/PHASE_1_DECISIONS.md` and `docs/planning/PHASE_3_DECISIONS.md`; this file is the quick-reference summary.

> **⚠️ PHASE 0A.1 RECONCILIATION (2026-10-03):** **Guided Notes are PRIMARY** (current standard: `docs/standards/GUIDED_NOTES_STANDARD.md`); **Science Journal is SECONDARY**; the Interactive Science Notebook-primary architecture is **RETIRED**. **Unit 1 final assessment = 25 questions / 50 points** (see `docs/standards/ASSESSMENT_LAYOUT_STANDARD.md`). Historical Phase 4.5 / Phase 9 entries below are retained for provenance only and no longer govern.

## Phase 3 additions (Chapter 1 prototype)
- **Slide density** → one core idea per slide; ≤3 short bullets on direction/lab slides; prediction-before-reveal for demos.
- **Writing space** → ruled answer lines; ≥2 lines for explain prompts.
- **Tables** → min row height 0.5" (portrait) / 1.1" (landscape investigation tables); shaded header row.
- **Quiz length** → 8–12 items / 10–15 min / ~50% core, ~25% application, ~25% evidence (no forced prior-unit spiral).
- **Friday Flex** → 3 tracks (Recover/Practice/Extend), no Week-2 dependency.
- Chapter 1 released; system validated (see `docs/reviews/PHASE_3_SYSTEM_VALIDATION.md`).

## Phase 4 additions (Chapter 2)
- **Chapter 2 boundary** → moving object causes change only; speed/mass/ramp-height/transfer/collision deferred to Ch.3–5.
- **Lab spec** → adds "setup constants" (identical-object control) + troubleshooting table.
- Chapter 2 released; consistency verified (see `docs/reviews/PHASE_4_SYSTEM_CONSISTENCY.md`).

## Phase 4.5 additions (Interactive Science Notebook) — RETIRED / HISTORICAL

> ⚠️ **RETIRED (Phase 0A.1).** The INB-primary architecture below is historical only. **Guided Notes are PRIMARY** (`docs/standards/GUIDED_NOTES_STANDARD.md`); **Science Journal is SECONDARY**.

- ~~**Primary student-note system → Basic Interactive Science Notebook**~~ → **RETIRED** (superseded; see `docs/standards/GUIDED_NOTES_STANDARD.md`).
- **Drawing/modeling** as an intentional core feature → retained within Guided Notes (draw/label/model).
- **Interactive elements are selective** → historical INB rule (retired with the INB system).
- **Slides model notebook work** → superseded by the notes-mirror rule (`docs/standards/SLIDESHOW_LOGIC_LOCKDOWN.md`).
- ~~**Chapters 1–2 retrofitted; guided notes remain OPTIONAL (historical)**~~ → Guided Notes are **PRIMARY**, not OPTIONAL.
- Notebook system validated (historical; see `docs/reviews/PHASE_4_5_NOTEBOOK_SYSTEM_VALIDATION.md`).

## Phase 5 additions (Chapter 3)
- **Chapter 3 boundary** → same-object speed↔energy relationship only; mass/collision/transfer/transformation/engineering deferred to Ch.4–7.
- **Measured vs inferred is the chapter's core distinction** → students measure ramp height, cup displacement, drop height, crater width; they INFER relative speed and the speed↔energy relationship. No "we measured energy/speed" anywhere.
- **Graph title is locked** → "Ramp Height vs. Average Cup Displacement" (both axes measured). "Speed vs. Energy" is prohibited.
- **Ramp It Up! 2.0 (ADAPTED)** → adds 3 heights (1/2/3 books), 3 trials, cm displacement, averaging, and a pre-ruled graph over the qualitative AP 4.1.
- **Drop It (ADAPTED)** → fixed heights 30/60/90 cm + cm crater width (depth qualitative) replace the official knee/waist body-relative heights, for a fairer test across student sizes.
- **Data Quality gate added** → dedicated `qa/data-quality.md` (trials, units, axes, averaging, precision, no invented speed/energy numbers). QA now 10 gates.
- Chapter 3 released; consistency verified (see `docs/reviews/PHASE_5_SYSTEM_CONSISTENCY.md`).

## Phase 6 additions (Chapter 4 — Energy Transfer, Weeks 4–5)
- **Chapter 4 boundary** → energy TRANSFER only; no compression-wave/electron/conduction mechanics; collisions (Ch.5) and engineering (Ch.6) deferred.
- **Transfer vs transformation vs BOTH is the chapter's core distinction** → TRANSFER = energy moves; TRANSFORMATION = energy changes form; BOTH = moves AND changes form. BOTH is explicitly valid; no forced either/or.
- **Safe investigation redesigns (ADAPTED from TG L8)** → light = flashlight + target (no chalk dust) · heat = warm water + thermometer (no hot plate) · electricity = low-voltage battery circuit (no wall outlet/charger). Science preserved; recorded in `curriculum/chapter-04/source-map.md`.
- **Locked safety** → no student wall outlets/chargers/hot plates/open flames; heat = teacher-controlled warm water (~40 °C max); electricity = AA/AAA/D cell only; no coin cells by default.
- **Notebook insert count is flexible** → 5 inserts for a two-week chapter (not forced to 3); interactive Transfer/Transformation/BOTH classification + flat low-motor alternative.
- **CER progression** → Chapter 4 uses the "I know ___ because ___" claim + evidence + reasoning scaffold (stronger than Ch.1–3).
- **QA now 11 gates** → adds Data Quality (Phase 5) + Misconception Audit (Phase 6, `docs/reviews/PHASE_6_MISCONCEPTION_AUDIT.md`).
- Chapter 4 released; consistency verified (see `docs/reviews/PHASE_6_SYSTEM_CONSISTENCY.md`).

## Phase 7 additions (Chapter 5 — Collisions Transfer Energy, Week 6)
- **Chapter 5 boundary** → collisions transfer energy only; no momentum/impulse/force calculations/contact-force/deformation terms; no kinetic/potential/mechanical vocabulary; sound qualitative; heat NOT measured.
- **Variable isolation is the chapter's core** → Crash Lab splits the official "change one variable" investigation into **Part A (Speed): same car, vary ramp height** and **Part B (Mass/Weight): same ramp, vary mass/weight**; measured outcome = **target displacement (cm)**. Speed and mass are NEVER confounded.
- **Primary data = target displacement** → cm displacement with 3 trials + averaging (rejects clay-depth/loudness as primary data, consistent with Phase 6).
- **Prediction scaffold** → PREDICT → TEST → OBSERVE → COMPARE → EXPLAIN formalized; Newton's cradle = demo/phenomenon only.
- **Energy-does-not-disappear is the synthesis anchor** → COLLISION → MOTION CAN CHANGE → ENERGY CAN TRANSFER → ENERGY DOES NOT DISAPPEAR.
- **Supplemental media intake merged** → 9 MP4 videos (~250 MB) + 2 review PDFs staged on-disk (git-ignored); metadata in `docs/planning/MEDIA_ASSET_MANIFEST.md`; reviews in `docs/reviews/SUPPLEMENTAL_READING_ASSESSMENTS_REVIEW.md` + `docs/reviews/CH1_SUPPLEMENTAL_NOTEBOOK_PACKET_REVIEW.md`; idea bank `docs/planning/SUPPLEMENTAL_IDEA_BANK.md`. Videos UNSTAGED; no LFS; no MP4 embedded in PPTX.
- Chapter 5 released; consistency verified (see `docs/reviews/PHASE_7_SYSTEM_CONSISTENCY.md`).

## Phase 8 additions (Chapter 6 — Energy Transformations + Engineering Design, Weeks 7–8)
- **Chapter 6 boundary** → energy TRANSFORMATION + engineering design only; no kinetic/potential/mechanical/radiant/chemical (required), joules, power, efficiency, voltage/current, electron flow, momentum, force calcs.
- **Core model** → INPUT → CHANGE IN FORM (TRANSFORMATION) → OUTPUT/CHANGE, with the three-way verdict TRANSFER / TRANSFORMATION / BOTH (BOTH remains valid; no forced either/or).
- **Capstone SELECTED (ADAPTED)** → **tabletop alert/signal device** (non-electrical, safe, weather-independent) replaces the source TG L13 solar-oven default + wired-doorbell Scenario 2. No wall electricity, no open flame/hot plate, no real-door hardware. Solar oven = optional EXTENSION only.
- **Engineering cycle locked** → DESIGN → BUILD → TEST → REFINE; Test 1 failure = data (not a penalty); redesign = ONE evidence-based change; evidence **supports** (never "proves").
- **Evidence ≠ proof** re-standardized across student artifacts (source AP 13.5 "prove/disprove" and supplemental slideshow reworded).
- **Supplemental slideshow intake merged** → `assets/supplemental/review/slides/Energy_Detectives.pptx` (Ch.1 slideshow, 15 slides, ~24.6 MiB) staged on-disk (git-ignored); review in `docs/reviews/CH1_SUPPLEMENTAL_SLIDESHOW_REVIEW.md`; KEEP AS SUPPLEMENTAL (NOT the Ch.1 release deck).
- Chapter 6 released; consistency verified (see `docs/reviews/PHASE_8_SYSTEM_CONSISTENCY.md`; misconception audit `docs/reviews/PHASE_8_MISCONCEPTION_AUDIT.md`).

## LOCKED / HIGH-CONFIDENCE
- **Grade 4**, CKSci-aligned, "Energy Transfer and Transformation", **9 weeks** (M–Th core + Friday Flex).
- **Content authorities** = CKSci Student Reader + Teacher Guide (13 lessons across 7 chapters).
- **Canonical Reader** = `Science 4 - Energy Transfer - Student Book.pdf`; personal copy retained as backup.
- **7-chapter backbone** — exact Reader titles; never invent/substitute chapters. **Reader chapter ≠ TG lesson.**
- **Friday = FLEX** (RECOVER / PRACTICE / EXTEND; nonessential to Monday). *Superseded in scope by the 2026-10-04 Friday policy below: Friday may also hold scored quizzes/tests, review and synthesis; it is never first exposure to essential core content.*
- **Transfer vs transformation** distinction is core (transfer = moves; transformation = changes form; BOTH allowed).
- **Grade-4 terminology** — Core Vocabulary (14 terms) + Language of Instruction; **not** required: kinetic, potential, radiant, mechanical, compression wave, inertia.
- **Speed-energy** = same object at different speeds (no mass+speed confound).
- **8-lab backbone** (Labs 1–8); Lab 6 redesigned (safe light/heat/electricity stations); Lab 7 variable-isolated (target displacement).
- **Week 8 = performance** (Engineering Capstone) · **Week 9 = written** summative (separate from capstone build).
- **Chapter package schema** + **8 QA gates** + **editable-first production** + provenance tags.

## PROVISIONAL
- ~~Engineering challenge = tabletop alert/signal/motion device~~ → **SELECTED in Phase 8** (tabletop alert/signal device, non-electrical).
- Formative checkpoints after Ch.1–3, Ch.4–5, Ch.6–7.

## REJECTED / SUPERSEDED
- Lab 6 hot-plate/surge-protector → superseded.
- Lab 2 & 7 mass+speed confounds → rejected in core.
- Kinetic/potential as required → rejected.
- Solar/weather-dependent capstone as sole pathway → rejected.
- "Pendulum Bell Alert" shown before independent design → rejected (exemplar only).
- Clay-depth/loudness as primary collision data → rejected (target displacement).
- Drop It knee/waist/shoulder body-relative heights → rejected (inconsistent across student sizes); replaced with fixed 30/60/90 cm (Phase 5).
- Millimeter crater-depth precision → rejected (false precision); crater depth stays qualitative shallow/medium/deep (Phase 5).

## OPEN
- See `OPEN_QUESTIONS.md` — class size/group count, period length, engineering final selection, media choices, slide toolchain, Git binary strategy, assessment weighting.

## Phase 9 additions (Chapter 7 + Unit Final)
- **Chapter 7 is the Unit Review lesson** (TG pp. 94–98), not a separately numbered lesson — no new Core Vocabulary.
- **Original written final** = 25 questions / 50 points, ADAPTED from the official 50-pt Unit Assessment blueprint (pp. 129–136) — re-authored, not copied. Core Vocabulary deck allowed.
- **Engineering cycle locked:** PROBLEM → DESIGN → TEST → EVIDENCE → IMPROVE.
- **Edison framing locked:** improved (did NOT invent) the bulb; Latimer collaborator; "ten thousand ways" quoted only as the Reader phrases it; no lone-genius myth.
- **Unit concept map** = ENERGY center + 7 branches (change · motion · speed · transfer · collisions · transformation · engineering).
- **Assessment balance (by points):** core 26% · data/diagram 30% · application 26% · engineering 18% (written/diagram items weighted higher than MC, matching official philosophy).
- **Final timing:** 25 questions ≈ 30–45 min; splits Wed/Thu at 30-min periods (documented).
- **Media:** Ch.7 = scripts only (5); videos PENDING/UNSTAGED. Whole-unit staging → Phase 10.
- **14 QA gates** run; all PASS. Unit instructionally complete; media staging not complete.
- Evidence ≠ proof reaffirmed across all final-assessment + student-facing language ("supports/shows").

## Friday policy (DECIDED · owner · 2026-10-04) — supersedes the Phase 6.1 open question
Friday is not reserved for "FLEX only." Friday may be used for: catch-up · review · completion of previously taught work · BQ reflection/synthesis · scored quizzes/tests · makeup work · optional FLEX/enrichment.
Friday must NOT be the first instructional exposure to essential new core content. Therefore: required Chapter 1 science concepts are taught by Thursday (for Ch1, Mon–Tue); Friday may contain the Ch1 graded quiz; Friday may finish reflection/synthesis that depends on content already taught.
- **Effect on Ch1:** Session 3 (N4 recognition, CHECK YOUR THINKING, BQ NOW I THINK, quiz) is **compliant** — each Friday slide is traceable to a concept first taught in Session 1 or 2 (`tools/ch1_pacing.py::FRIDAY_DEPENDS`, gated by `check_plan()`). The earlier fallback (moving N4 or the quiz) is withdrawn.
- **Standing rule for every chapter:** a Friday slot may not introduce new vocabulary, models, or required note content; `check_plan()`-style traceability is required where Friday carries notes (propagation spec G16).
