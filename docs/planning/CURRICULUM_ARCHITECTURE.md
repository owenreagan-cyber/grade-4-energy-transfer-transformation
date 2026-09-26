# CURRICULUM ARCHITECTURE

> Top-level project logic. All other planning docs hang off this one.

## Course identity
- **Grade:** 4
- **Subject:** Science (Physical Science — Energy)
- **Framework:** Core Knowledge Science (CKSci), 2019 Core Knowledge Science Sequence, informed by NGSS
- **Unit title:** Energy Transfer and Transformation
- **Length:** 9 weeks (Monday–Thursday core + Friday Flex)

## Official backbone (do not alter)

### Student Reader — 7 chapters (+ Glossary)
| # | Chapter title | Reader printed pages | Reader PDF pages |
|---|---|---|---|
| 1 | Energy Causes Change | 1–6 | 7–12 |
| 2 | Moving Objects Have Energy | 7–12 | 13–18 |
| 3 | Energy and Speed Are Related | 13–16 | 19–22 |
| 4 | Energy Transfer | 17–24 | 23–30 |
| 5 | Collisions Transfer Energy | 25–30 | 31–36 |
| 6 | How Can Energy Transformations Solve Problems? | 31–36 | 37–42 |
| 7 | Solving Problems and Designing Solutions: Thomas A. Edison | 37–42 | 43–48 |
| — | Glossary | 43 | 49 |

### Teacher Guide — 13 lessons across 5 parts
- **Part A — Introduction to Energy:** L1 Energy Causes Change · L2 Forms of Energy
- **Part B — Energy and Motion (4-PS3-1):** L3 Moving Objects Have Energy · L4 Investigating Energy and Speed (2 sessions) · L5 Energy and Speed Are Related
- **Part C — Energy Transfer (4-PS3-2):** L6 Sound Transfers Energy · L7 Energy Transfer · L8 Investigating Energy Transfer · L9 Evidence of Energy Transfer
- **Part D — Collisions (4-PS3-3):** L10 Collisions Transfer Energy · L11 Investigating Collisions (2 sessions)
- **Part E — Energy Transformation and Engineering (4-PS3-4):** L12 How Can Energy Transformations Solve Problems? · L13 Designing Devices to Transform Energy (4 sessions)
- **Unit Review:** Ch.7 Thomas A. Edison + Unit Assessment

> Key structural fact: **Student Reader chapter ≠ Teacher Guide lesson.** Reader = reading spine; TG = investigation spine.

## NGSS Performance Expectations
- **4-PS3-1** Use evidence to construct an explanation relating the speed of an object to the energy of that object.
- **4-PS3-2** Make observations to provide evidence that energy can be transferred from place to place by sound, light, heat, and electric currents.
- **4-PS3-3** Ask questions and predict outcomes about the changes in energy that occur when objects collide.
- **4-PS3-4** Apply scientific ideas to design, test, and refine a device that converts energy from one form to another.

## Core concept model (recurring unit-wide)
```
ENERGY SOURCE → ENERGY FORM → TRANSFER → TRANSFORMATION → OBSERVABLE CHANGE / EVIDENCE
```
- Not every system uses every box.
- **TRANSFER** = energy moves from one object/place to another.
- **TRANSFORMATION** = energy changes from one form to another.
- Some systems involve **BOTH**.
- Recurring question: *"What changed, and what does that change tell us about energy?"*

## Terminology policy (Grade 4)
- **Required core:** stored energy, energy of motion, energy transfer, energy transformation, collision, convert, plus the full 14-term Core Vocabulary.
- **NOT required core:** kinetic energy, potential energy, gravitational potential energy, mechanical energy, radiant energy, compression wave, inertia.
- Teacher/enrichment language is labeled separately and never required for independent student use.

## Daily rhythm (Monday–Thursday)
Four options, chosen to fit the day — see `DAILY_LESSON_ARCHITECTURE.md`:
- **A** Standard concept day · **B** Lab day · **C** Reading/synthesis day · **D** Assessment day
- Preferred science flow: **phenomenon → prediction → investigation → evidence → discussion → reading/notes → explanation/application.**

## Friday
- **Flex Science Friday** — never introduces essential new core content.
- Modes: RECOVER · PRACTICE · EXTEND. See `FRIDAY_FLEX_FRAMEWORK.md`.

## Assessment architecture
- Daily checks · chapter quizzes (10–15 min) · formative checkpoints (after Ch.1–3, Ch.4–5, Ch.6–7) · Week 8 performance (engineering capstone) · Week 9 written summative. See `ASSESSMENT_BLUEPRINT.md`.

## Lab architecture
- 8-lab backbone (Labs 1–8) with Lab 6 redesign and Lab 7 variable-isolation rule. See `LAB_ARCHITECTURE.md` and `ENGINEERING_CAPSTONE.md`.

## Chapter package model
- Each chapter ships TEACHER + STUDENT + MEDIA bundles, tagged `CORE`/`FLEX`/`EXTENSION` and `SOURCE`/`ADAPTED`/`CUSTOM`/`EXTENSION`. See `CHAPTER_PACKAGE_STANDARD.md`.

## Production & QA
- Editable-first masters (PPTX/DOCX/Markdown) → PDF release exports. See `PRODUCTION_FORMATS.md`.
- 8-gate QA before anything is called FINAL/READY/COMPLETE/RELEASED. See `QA_GATES.md`.
