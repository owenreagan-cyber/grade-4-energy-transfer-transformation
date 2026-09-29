# PHASE 13R QA REPORT — Infographics + Study Guide Reconciliation

> Gates: visual, scientific vocabulary, controversial/climate, answer-key, path integrity, assessment alignment.
> Baseline `main` = `7a84a13` → branch `feature/phase13r-final-infographic-study-guide-reconciliation`.

---

## R · VISUAL QA — PASS

Six rebuilt infographics, rendered at 2752×1536 (16:9) via deterministic HTML/CSS → headless Chrome.
OCR-verified content (macOS Vision) confirms no clipping, no element overflow, large headline text,
single-concept layout, and grayscale-safe high-contrast fills.

| File | Concept | Large text | No clipping | Grayscale-safe |
|---|---|---|---|---|
| `unit1-energy-detective-anchor.png` | ENERGY → CHANGE → EVIDENCE | ✓ | ✓ | ✓ |
| `unit1-transfer-vs-transformation.png` | 4 panels + BOTH | ✓ | ✓ | ✓ |
| `unit1-engineering-design-cycle.png` | 5-stage cycle + Edison/Latimer | ✓ | ✓ | ✓ |
| `unit1-collision-energy-transfer.png` | BEFORE/COLLISION/AFTER | ✓ | ✓ | ✓ |
| `unit2-renewable-nonrenewable-resources.png` | 8-resource matrix | ✓ | ✓ | ✓ |
| `unit2-turbine-generator-pathways.png` | coal/nuclear · wind · hydro | ✓ | ✓ | ✓ |

No tiny text below Grade-4 projector threshold; no false precision (no quantitative values on student visuals).

---

## S · SCIENTIFIC VOCABULARY QA — PASS (1 reviewed hit, acceptable)

Scanned all six rebuilt infographics (OCR) + `unit1-study-guide.docx` + `unit1-study-guide-key.docx`
against the locked scientific guardrail list.

Forbidden terms **absent**: `kinetic`, `potential`, `mechanical energy`, `chemical energy`,
`thermal energy`, `radiant`, `momentum`, `impulse`, `inertia`, `electron`, `photon`,
`semiconductor`, `compression wave`, `base-load/baseload`, `dispatch`, `peak demand`,
`grid stabilization`, `fission`, `U-235`, `impact force`.

| Hit | Location | Disposition |
|---|---|---|
| `proves` | `unit1-study-guide.docx` — Short Response scaffold: *"Use 'supports,' not 'proves.'"* | **ACCEPTABLE** — the instruction explicitly directs students AWAY from `proves` toward the course-approved `supports`. Reinforces the guardrail; not a concept being taught. |

---

## T · CLIMATE / CONTROVERSIAL CONTENT QA — PASS (2 reviewed hits, acceptable)

Scanned the same corpus for climate/policy terms.

Forbidden terms **absent**: `climate change`, `global warming`, `climate crisis`, `zero carbon`,
`carbon-free`, `zero emissions`, `carbon footprint`, `clean energy`, `dirty energy`,
`green energy`, `carbon tax`, `cap and trade`, `energy policy`, `save the planet`, `activism`.

| Hit | Location | Disposition |
|---|---|---|
| `carbon` | `unit1-engineering-design-cycle.png` — *"1879: bamboo filament with a carbon coating."* | **ACCEPTABLE** — physical carbon filament material, source-supported (Reader p.39, `curriculum/chapter-07/qa/historical-claims.md`). Not emissions/policy framing. |
| `carbon` | `unit1-study-guide.docx` — fill-in *"…a ______ filament with a carbon coating."* | **ACCEPTABLE** — same source-supported historical fact (answer = "bamboo"). |

No policy/climate drift anywhere in student-facing output.

---

## U · ANSWER-KEY QA — PASS

`unit1-study-guide-key.docx` verified item-by-item against the student `unit1-study-guide.docx`:

- **A (match 10)** — all 10 mappings correct (1-F energy, 2-J evidence, 3-D stored, 4-B energy of motion,
  5-I transfer, 6-A transformation, 7-H collision, 8-E criteria, 9-C constraints, 10-G refine).
- **B (fill-in 6)** — cause change · evidence · stored · motion · faster · transfer — all correct.
- **C (T/T/BOTH 4)** — TRANSFER, TRANSFORMATION, BOTH, TRANSFORMATION — all correct.
- **D (same object/speed)** — FARTHER · MORE; MEASURE = ramp height + cup distance; INFER = speed + energy of motion — correct.
- **E (flashlight)** — INPUT stored energy (battery) → OUTPUT light (+ a little heat) — correct.
- **F (collision)** — does NOT disappear · transfers to target — correct.
- **G (engineering words)** — criteria/constraints/refine definitions — correct.
- **H (Edison/Latimer)** — improved · 6,000 · bamboo · filament — correct (source-supported).
- **I (short response)** — claim + evidence + reasoning example using "supports" — correct.

Student PDF contains **no** answer leakage; key is a separate 1-page file (never appended to the student packet).

---

## V · PATH INTEGRITY QA — PASS

- `production/infographics/` — 6 PNGs present (2752×1536).
- `production/review/unit-01/` — `unit1-study-guide.{docx,pdf}` (3 pp) + `unit1-study-guide-key.{docx,pdf}` (1 pp).
- `production/review/unit-02/` — `unit2-written-study-review.{docx,pdf}` (3 pp) + key (1 pp), reconciled & KEPT.
- Embedded slides verified byte-for-byte (SHA-256 of image blob == source PNG):

| Deck | Slide | Infographic |
|---|---|---|
| `01-ch1-energy-causes-change-slides.pptx` | S26 | `unit1-energy-detective-anchor.png` |
| `04-ch4-energy-transfer-slides.pptx` | S47 | `unit1-transfer-vs-transformation.png` |
| `05-ch5-collisions-slides.pptx` | S29 | `unit1-collision-energy-transfer.png` |
| `06-ch6-energy-transformations-slides.pptx` | S45 | `unit1-engineering-design-cycle.png` |
| `01-u2-ch1-renewable-nonrenewable-slides.pptx` | S22 | `unit2-renewable-nonrenewable-resources.png` |
| `03-u2-ch3-slides.pptx` | S20 | `unit2-turbine-generator-pathways.png` |

No broken references; all quickstart/prep/manifest paths point to existing files.

---

## N · ASSESSMENT ALIGNMENT — PASS (no unassessed emphasis)

Unit 1 study guide covers all 13 required review items (energy→cause change, evidence, stored energy,
energy of motion, same-object speed, transfer, transformation, BOTH, collisions, criteria, constraints,
design/test/refine, Edison/Latimer). No `mass`, `deformation`, `kinetic/potential/mechanical/chemical/thermal`
requirements. Unit 2 review = existing Phase 13K sheet, already aligned to the released 22-pt assessment;
uploaded Unit 2 content added no missing coverage worth merging.

---

## Z · RESULT — PASS

All six QA gates pass. Zero unresolved guardrail hits. Two `carbon` hits + one `proves` hit reviewed and
documented as source-supported / anti-proof scaffolding.
