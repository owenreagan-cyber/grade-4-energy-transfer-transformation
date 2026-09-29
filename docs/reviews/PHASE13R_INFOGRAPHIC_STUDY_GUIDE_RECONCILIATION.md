# PHASE 13R — FINAL INFOGRAPHIC + STUDY GUIDE RECONCILIATION

> Final reconciliation of newly delivered visual-study assets against the released course.
> Every delivered source receives a final disposition. No TBD / UNREVIEWED / UNKNOWN.

---

## 1. Delivered source intake (preserved unchanged in `~/Downloads`)

| # | Delivered file | SHA-256 (first 16) | Dimensions | Size |
|---|---|---|---|---|
| 1 | `Engineering_Design_Cycle_Infographic.png` | `97049988c31bd5c5` | 2752×1536 | 5,582,160 B |
| 2 | `Collision_Dynamics_Infographic.png` | `fdf1a71dcd16d0f` | 2752×1536 | 4,576,782 B |
| 3 | `Energy_Transfer_vs_Transformation.png` | `4671ef6d73405750` | 2752×1536 | 4,681,621 B |
| 4 | `Motion_Energy_Investigation_Matrix.png` | `e126fde61edacaec` | 2752×1536 | 4,367,021 B |
| 5 | `The_Energy_Detective_Anchor_Chart.png` | `ca7b5a5a357ee6fd` | 1536×2752 (portrait) | 4,057,952 B |
| 6 | `4_Steps_of_Land_Reclamation.png` | `e36863451ad4e003` | 2752×1536 | 5,356,141 B |
| 7 | `Renewable_vs_Nonrenewable_Resources_Matrix.png` | `8eea4ab498945e59` | 2752×1536 | 5,336,290 B |
| 8 | `How_Electricity_Generation_Works.png` | `e6206ca6499b43b8` | 2752×1536 | 5,537,111 B |
| 9 | `unit1-and-unit2-study-guide-review-worksheet.pdf` | `4512bf57caade7a6` | 5 pages · US Letter | 13,103 B |

## 2. Final classification table

| Delivered source | Status | Action | Final output | Unit · Ch | Placement | Student safe? |
|---|---|---|---|---|---|---|
| Engineering Design Cycle Infographic | REBUILD | rebuild → use | `unit1-engineering-design-cycle.png` | U1 · Ch6 | `06-ch6` deck S45 (REFERENCE) | ✅ |
| Collision Dynamics Infographic | REBUILD | rebuild → use | `unit1-collision-energy-transfer.png` | U1 · Ch5 | `05-ch5` deck S29 (REFERENCE) | ✅ |
| Energy Transfer vs Transformation | REBUILD | rebuild → use | `unit1-transfer-vs-transformation.png` | U1 · Ch4 | `04-ch4` deck S47 (LOOK/NOTICE) | ✅ |
| Motion Energy Investigation Matrix | REJECT | not used | — | — | — | — |
| The Energy Detective Anchor Chart | REBUILD | rebuild → use | `unit1-energy-detective-anchor.png` | U1 · Ch1 | `01-ch1` deck S26 (REFERENCE) | ✅ |
| 4 Steps of Land Reclamation | OPTIONAL | reject graphic (teacher reference only) | — | U2 (not assessed) | Week 5 FLEX / teacher reference | ❌ (teacher only) |
| Renewable vs Nonrenewable Matrix | REBUILD | rebuild → use | `unit2-renewable-nonrenewable-resources.png` | U2 · Ch1 | `01-u2-ch1` deck S22 (COMPARE) | ✅ |
| How Electricity Generation Works | REBUILD | rebuild → use | `unit2-turbine-generator-pathways.png` | U2 · Ch3–6 | `03-u2-ch3` deck S20 (COMPARE) | ✅ |

Print default: **PROJECT / DIGITAL**. No 20-color-copy requirement for infographics.

## 3. Per-source audit notes (why each disposition)

- **Engineering Design Cycle** — REBUILD. Kept 5-stage cycle, criteria/constraints, Edison/Latimer (source-supported: Edison improved earlier designs, tested 6,000+ materials, 1879 bamboo-carbon filament; Latimer improved filament durability — see `curriculum/chapter-07/qa/historical-claims.md`). Removed "Mechanical/Chemical Energy Solutions" categories and unsupported specifics.
- **Collision Dynamics** — REBUILD. Removed "deformation", "mass as core rule", "weight (mass)", "energy conservation" phrasing, and formula language. Rebuilt as simple BEFORE → COLLISION → AFTER with the one key idea "energy can transfer during a collision" and the optional note "some energy may transform to sound and tiny heat".
- **Transfer vs Transformation** — REBUILD. Removed "acoustic vibrations", "thermal conduction", "chemical energy", "thermal energy", and the incorrect "form stays the same" claim. Rebuilt as four panels (sound/light/heat/electric current) + the BOTH-possible note.
- **Motion Energy Investigation Matrix** — REJECT. Prefilled quantitative results (2 cm / 10 cm / 3 mm / 9 mm), "impact force", and expected-results framing = false precision + answer leakage. The Ch3 deck + Ramp It Up lab already teach the same-object relationship without prefilled numbers; no replacement needed.
- **Energy Detective Anchor** — REBUILD. Fixed "evidence = proof" → "what we observe that shows a change occurred"; stored-energy examples reworded (battery → light/sound/motion; rubber band → motion; raised object → change when released). Removed "chemical energy"/"potential energy".
- **Land Reclamation** — OPTIONAL / TEACHER REFERENCE. Four-step reclamation sequence is NOT supported by the authoritative Unit 2 Reader/TG (no reclamation coverage in `assets/authoritative/unit-02/`). Over-detailed (habitat claims, "sustainable repurposing", engineering language). Not assessed. Concept already covered by the Week 5 cookie-mining FLEX model. Graphic rejected for student shipping.
- **Renewable vs Nonrenewable Matrix** — REBUILD. Removed radiant/kinetic/thermal/fission detail, carbon/greenhouse framing, zero/near-zero-carbon claims, pros/cons moral framing, and ranking. Rebuilt as RESOURCE | RENEWABLE? | HOW USED | BENEFIT | LIMITATION for all eight resources + "abundant ≠ renewable" / "renewable ≠ available everywhere".
- **Electricity Generation** — REBUILD. Removed thermal/kinetic pathway labels, combustion, fission, U-235, electromagnetic induction, high-voltage grid, "mechanical motion", generator internals. Rebuilt as coal/nuclear + wind + hydro side-by-side with the bottom idea "different source / same turbine → generator".

## 4. Study guide audit

Delivered `unit1-and-unit2-study-guide-review-worksheet.pdf` (5 pages) combined Unit 1 review + Unit 2 review + a teacher key in ONE file. **Rejected as-is.**

Verified issues (all confirmed): Unit 1 uses "proof", "deformation", "mass (weight)", "carbon", "hot plate", "thermal"; Unit 2 uses "fission", "semiconductor/photovoltaics", "clean power", "zero fuel combustion", overemphasizes reclamation (3 of 10 fill-ins). Answer-key mapping had an ambiguity (U1 B7 "light (or heat)").

Split and rebuilt:
- **Unit 1** → new `production/review/unit-01/unit1-study-guide.docx` + `.pdf` (3 pages) + separate `unit1-study-guide-key.docx` + `.pdf` (1 page). 13-pt body / 12-pt floor. Covers all 13 required topics with matching, fill-in, diagram, classify transfer/transformation/BOTH, short scenario, one short response.
- **Unit 2** → existing Phase 13K `production/review/unit-02/unit2-written-study-review.docx` **KEPT** (already better-aligned: uses "solar cell" not "photovoltaic", "heat from inside Earth", no fission detail, no "clean power"). No merge needed — the uploaded Unit 2 content adds nothing aligned and would broaden scope.

## 5. Rebuilt visual outputs (`production/infographics/`)

| File | Unit · Ch | Placement | Purpose |
|---|---|---|---|
| `unit1-energy-detective-anchor.png` | U1 · Ch1 | `01-ch1` S26 | anchor: energy → change → evidence |
| `unit1-transfer-vs-transformation.png` | U1 · Ch4 | `04-ch4` S47 | transfer vs transformation vs both |
| `unit1-collision-energy-transfer.png` | U1 · Ch5 | `05-ch5` S29 | collision energy transfer |
| `unit1-engineering-design-cycle.png` | U1 · Ch6 | `06-ch6` S45 | design cycle + Edison/Latimer |
| `unit2-renewable-nonrenewable-resources.png` | U2 · Ch1 | `01-u2-ch1` S22 | renewable/nonrenewable matrix |
| `unit2-turbine-generator-pathways.png` | U2 · Ch3–6 | `03-u2-ch3` S20 | turbine → generator pathways |

Generated at 2752×1536 via headless Chromium from deterministic HTML/CSS (16:9, projector-readable, grayscale-safe).

## 6. Delivered sources intentionally NOT used (retired/rejected)

- `Motion_Energy_Investigation_Matrix.png` — REJECT (prefilled results + "impact force").
- `4_Steps_of_Land_Reclamation.png` — OPTIONAL/teacher reference only; not in core course; rejected for student shipping.
- `unit1-and-unit2-study-guide-review-worksheet.pdf` — REJECT as-is; split/rebuilt (Unit 1) and superseded by existing Phase 13K review (Unit 2).

All delivered files remain unchanged in `~/Downloads`. Rebuilt versions use new descriptive filenames.

## 7. Rebuilt study-guide outputs

- `production/review/unit-01/unit1-study-guide.docx` + `.pdf` (3 student pages)
- `production/review/unit-01/unit1-study-guide-key.docx` + `.pdf` (1 teacher key page)

No key page in the student packet. No blank pages. 12-pt floor honored.

## 8. Decision

VISUAL + STUDY RESOURCES COMPLETE
