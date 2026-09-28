# PHASE 13H — Final Media Intake, Review, Trimming, and Placement

> Media-only enhancement phase. The 8.5-week course is already complete and classroom-ready; this phase
> reviews the six newly delivered videos and places only genuinely valuable, Grade-4-safe media into the map.

## Method & limitations

- **Frame inspection:** dense sample (every 8 s) plus fine boundary frames via macOS Vision OCR. These videos
  are heavily text-driven (AI explainer style), so on-screen text captures the core content reliably.
- **Transcript extraction:** **UNAVAILABLE.** `SFSpeechRecognizer` (URL-based, `en-US`) hangs awaiting a Speech
  privacy prompt that cannot be approved headlessly; no whisper/vosk tooling is installed. Narration that is
  **not** on screen could not be verified. This limitation is factored into trim/reject decisions — where the
  on-screen text already shows forbidden content, the video is rejected; where on-screen text is clean, the
  trimmed cut was additionally OCR-scanned (zero forbidden hits) and is treated as low-risk.
- **Decode integrity:** all six sources + both cuts fully decode (`ffmpeg -f null -`) with no errors.

---

## Video 1 — Fossil_Fuel_Formation.mp4

### Source metadata
- Path: `assets/supplemental/media/unit-02/chapter-02/Fossil_Fuel_Formation.mp4` (copied from `~/Downloads`)
- SHA-256: `08d59d655194e10b68b46d45ec5ddd57e61af14d1192eee106ecf70c9ea80ac2` · 45,107,778 bytes
- Runtime: 7:48 (467.8 s) · 1280×720 · h264 24 fps · aac 44.1 kHz mono · decode clean

### Content Summary
Hook ("What powers a train, a fork, and a heater?") → "ancient, dead organisms" → fossil-fuel definition
(petrified remains) → oil & gas from ancient oceans (microscopic marine life → ocean-floor burial; natural gas
rises and gets trapped) → coal from ancient swamps (plants → peat) → shared mechanism (burial → rock forms →
pressure/cooking → coal, oil, or gas) → brown vs black coal (low vs high pressure) → timescale timeline
(millions/thousands/today) → nonrenewable punchline ("forms in millions of years, burns in minutes") → closing
question ("What happens when the nonrenewable recipe runs out?").

### Scientific Accuracy
Accurate and age-appropriate. Correctly separates marine (oil/gas) vs swamp (coal) sources — matching Reader
Ch2 — and the shared "buried + heat + pressure + time" mechanism. No oversimplification that "all fossil fuels
form the same way."

### Vocabulary
Clean. Uses "petrified remains" (glossable as "turned to stone/fossilized"), "sediment", "peat". No
chemical-energy / carbon / climate / kinetic-potential terms.

### Grade-Level Fit
Strong. Short sentences, concrete visuals, digestible diagrams.

### Visual Quality
Clear, consistent card/diagram style; diagrams for ocean burial, swamp burial, and the burial→rock→pressure→
cooking sequence.

### Runtime
7:48 source (too long) → trimmed 3:39 (within "up to ~4 min" target).

### School-Content Boundary
Clean. No climate/carbon/advocacy framing. The closing "runs out" question is scarcity-neutral, not policy.

### Alignment
Directly matches Ch2 (Types of Fossil Fuels / How They Form) and the "buried remains + heat + pressure + time"
essential in guided notes + slides.

### Best Placement
Week 5 Wednesday (Ch2) — SUPPORT / OPTIONAL. Also supports Thursday's formation demo.

### Trim Analysis
Contiguous excerpt **94–313 s** (3:39): definition → oil/gas (ocean) → coal (swamp) → burial/pressure/cooking.
Excluded: 0–93 s (hook), 314–344 s (coal grades — nice-to-have), 352–467 s (timescale + nonrenewable punchline +
closing question). All excluded ranges are benign (no forbidden content); cut purely for runtime.

### Classification
SUPPORT · OPTIONAL · TRIM THEN USE · AS-IS role would exceed runtime.

### Final Decision
**TRIM → USE.** `fossil-fuel-formation-classroom-cut.mp4` (3:39), Week 5 Wednesday.

---

## Video 2 — Energy_Detectives.mp4

### Source metadata
- Path: `assets/supplemental/media/unit-02/chapter-03/Energy_Detectives.mp4` (copied from `~/Downloads`)
- SHA-256: `e341dec3242ed232617f9b7b6c0ed5e3cd62db7dfc34b24b7f92eeb9bac807ce` · 40,516,861 bytes
- Runtime: 7:17 (437.4 s) · 1280×720 · h264 24 fps · aac 44.1 kHz mono · decode clean

### Content Summary
**Misnamed.** Despite the title, this is NOT the Unit 1 "ENERGY → CHANGE → EVIDENCE" detective concept. Its
actual content is "How do we make electricity?" → turbine definition (fan-like blades spun by water/air/steam) →
generator definition (spinning motion → electricity) → wind pathway → water/hydro pathway → steam pathway
(boiler → steam → turbine → generator) → "The Big Comparison / Spot the Difference" → Input/Transformation/
Output table (Wind/Water/Steam → Spins Turbine → Electricity).

### Scientific Accuracy
Accurate. Correctly shows the shared turbine → generator → electricity pathway across three sources.

### Vocabulary
Minor variants only (glossable): "motion energy" (locked term is "energy of motion"), "electrical energy"
(locked term is "electric current"/"electricity"), "Power created" (loose). No kinetic/potential/mechanical/
chemical/thermal terms.

### Grade-Level Fit
Strong. Clear definitions and repeated, parallel visuals.

### Visual Quality
Consistent; clean pathway cards and a comparison table.

### Runtime
7:17 source → trimmed 3:41.

### School-Content Boundary
Clean. No climate/carbon/advocacy.

### Alignment
Best match is the **shared turbine → generator pathway** (Ch3 Week 6 Tue "burn → heat → steam → turbine →
generator" and Ch4 Week 6 Thu SAME/DIFFERENT), not Week 1. Satisfies script #5 ("How a Turbine Helps Make
Electricity").

### Best Placement
Week 6 Tuesday (Ch3 electricity pathway) — SUPPORT / OPTIONAL. The comparison section (302–368 s) also previews
Thursday's SAME/DIFFERENT, but a second cut is not warranted (avoid over-trimming).

### Trim Analysis
Contiguous excerpt **80–301 s** (3:41): turbine def → generator def → wind → water → steam pathways. Excluded:
0–79 s (hook), 302–437 s (comparison + table + closing). Exclusion is benign; cut for runtime.

### Classification
SUPPORT · OPTIONAL · TRIM THEN USE.

### Final Decision
**TRIM → USE.** `turbine-generator-classroom-cut.mp4` (3:41), Week 6 Tuesday.

---

## Video 3 — Solar___Geothermal_Energy.mp4

### Source metadata
- Path: `assets/supplemental/media/unit-02/chapter-07/Solar___Geothermal_Energy.mp4` (copied from `~/Downloads`)
- SHA-256: `d1a173f325bbf94295b920e10beea36cce6166188337c7fdc2962eca93232901` · 36,972,264 bytes
- Runtime: 6:48 (408.5 s) · 1280×720 · h264 24 fps · aac 44.1 kHz mono · decode clean

### Content Summary
Solar cell definition → **photon/electron mechanics** ("Photons Strike… the light excites the electrons,
freeing them from their atoms… Current Flows") → concentrated solar power → geothermal definition → geothermal
pathway (tap reservoir → steam → spin turbine → recycle water) → benefits/drawbacks table ("Solar Power:
Renewable, **Zero Emissions** / Weather Dependent"; "Geothermal Power: Renewable, **Zero Emissions** / Rare
Locations, Methane Risk") → "Energy is never destroyed; it transfers and/or transforms" recap.

### Scientific Accuracy
Mechanistically correct but mis-leveled for Grade 4.

### Vocabulary
**FAIL.** "photons", "electrons", "excites the electrons … from their atoms" (forbidden electron mechanics /
charged-particle mechanics).

### Grade-Level Fit
Poor. The solar-cell explanation is high-school physics.

### Visual Quality
Good, but does not redeem the content.

### Runtime
6:48 (too long regardless).

### School-Content Boundary
**FAIL.** "Zero Emissions" (renewable = good, simplified moral framing) on the benefits table; borderline
"methane risk".

### Alignment
Would target Ch7 (solar) / Ch8 (geothermal), but the solar core is unusable and the "Zero Emissions" framing is
forbidden. No clean Grade-4-safe contiguous excerpt exists — the electron/photon content sits in the solar core
and "Zero Emissions" sits in the shared benefits table, contaminating both halves.

### Best Placement
None.

### Trim Analysis
Not viable — forbidden content is woven through both solar and geothermal halves; a geothermal-only excerpt
(160–216 s) is only ~56 s and would still leave the surrounding source (and its "Zero Emissions" table) as the
delivered artifact.

### Classification
DO NOT USE · SKIP · REJECT.

### Final Decision
**REJECT.** Script #7 remains a regeneration target (or leave the slot empty — Ch7/Ch8 already teach well).

---

## Video 4 — The_Timescale_Tradeoff__Physics,_Economics,_and_the_Energy_Grid.mp4

### Source metadata
- Path: `assets/supplemental/media/unit-02/chapter-01/The_Timescale_Tradeoff__Physics,_Economics,_and_the_Energy_Grid.mp4`
- SHA-256: `e773c74ce51f5a07540e49e4bd7aeb292d5e0deb704a7b0bead4827720b6f517` · 55,406,093 bytes
- Runtime: 6:47 (407.0 s) · 1280×720 · h264 30 fps · aac 44.1 kHz mono · decode clean

### Content Summary
Mostly narration over sparse diagrams: "Legacy Systems Dominate U.S. Grid" (10% renewables / 90% nonrenewable),
"Power Plant", "Human Lifespan (100 Years)" vs "Millions of Years" (timescale), "The Renewable Intermittency
Gap" (wind & solar generation vs demand curve), "Capital Inversion In Energy" (infrastructure & storage cost vs
fuel cost), "Power Meter".

### Scientific Accuracy
Not assessed at depth — content is economics/policy, not Grade-4 science.

### Vocabulary
**FAIL.** Grid, intermittency, demand curve, capital/storage cost — all out of scope.

### Grade-Level Fit
Poor — high-school/adult economics.

### Visual Quality
Chart-heavy; sparse text (mostly narration, which could not be transcribed).

### Runtime
6:47.

### School-Content Boundary
**FAIL.** Grid economics and energy-transition framing; the only candidate-safe concept (replenishment
timescale, "100 years vs millions of years") is embedded in an economics/policy narrative that cannot be
verified narration-clean.

### Alignment
Would target Week 5 Tue ("abundant ≠ renewable"), but the safe timescale concept is already fully taught by
guided notes, slides, and the Detective Chart — the video adds no value for the risk.

### Best Placement
None.

### Trim Analysis
Not viable — the "safe" timescale idea is only ~15 s of on-screen text in a 6:47 economics/policy piece with
unverifiable narration.

### Classification
DO NOT USE · SKIP · REJECT.

### Final Decision
**REJECT.**

---

## Video 5 — Energy_Causes_Change.mp4

### Source metadata
- Path: `assets/supplemental/media/unit-02/chapter-01/Energy_Causes_Change.mp4` (copied from `~/Downloads`)
- SHA-256: `514b434431ee34185241d17b1eceb879f4b6518a0fafcf6bc359ba8ce2df2a95` · 36,562,945 bytes
- Runtime: 6:43 (403.3 s) · 1280×720 · h264 24 fps · aac 44.1 kHz mono · decode clean

### Content Summary
**Misnamed.** Not the Week 1 "energy causes change / observable evidence" concept. Actual content: "What
happens when wind stops or the sun sets?" → "Renewable Energy Problem: Balancing the grid" → offshore wind →
Energy Source → Turbine → **Power Grid** → Your Home → Stored Energy definition → "**thermal**: a solar tower
superheating liquid" → Hydropower Reservoir Tradeoffs (Costs: expensive/disrupts habitats/blocks migration;
Benefits: "**No carbon emissions**", "**ZERO EMISSIONS**", cost-effective) → pumped-hydro storage + engineering
cycle (Problem/Design/Test/Improve) → "How will engineering shape energy storage?"

### Scientific Accuracy
Storage/grid content, not the Week 1 concept.

### Vocabulary
**FAIL.** "thermal", "Power Grid", "Balancing the grid", "pumped-hydro", "storage".

### Grade-Level Fit
Poor — grid/storage engineering.

### Visual Quality
Good, but does not redeem content.

### Runtime
6:43.

### School-Content Boundary
**FAIL.** "No carbon emissions" / "ZERO EMISSIONS" framing; grid-balancing is out-of-scope economics.

### Alignment
Does not match Week 1 Monday (energy → change → evidence). Existing Ch1 media
(`The_Invisible_Boss_of_Change`, `The_Energy_Detective`, `Stored_Energy`, `How_Scientists_Spot_Invisible_Energy`)
already covers Week 1 well; this video must "earn" a place and fails on both alignment and boundary.

### Best Placement
None.

### Trim Analysis
Not viable — the only aligned fragment is the Stored Energy definition (~192–216 s), but it is sandwiched in a
grid/storage piece with forbidden framing; existing `Stored_Energy.mp4` already covers this concept.

### Classification
DO NOT USE · SKIP · REJECT.

### Final Decision
**REJECT.** Week 1 media is already complete; do not overload.

---

## Video 6 — Energy_Innovations.mp4

### Source metadata
- Path: `assets/supplemental/media/unit-02/chapter-09/Energy_Innovations.mp4` (copied from `~/Downloads`)
- SHA-256: `43500449da73e621fa80073df91c81b691c40b2929b3d3bed4d30cc5ee3115b5` · 34,808,180 bytes
- Runtime: 6:19 (379.4 s) · 1280×720 · h264 24 fps · aac 44.1 kHz mono · decode clean

### Content Summary
Title card listing "**Kinetic Energy / Chemical Energy** / biomass → electricity" → tidal energy ("**Mechanical
energy of motion** pushes against turbine blades") → wave energy (point absorber) → biofuels (definition,
fermentation, ethanol mix) → benefits/costs ("Emits **carbon dioxide**", "**Changes climate**", "Takes land
space") → tide/wave benefits/costs → closing "what unexpected energy is in your backyard?"

### Scientific Accuracy
Factually mixed and mis-leveled.

### Vocabulary
**FAIL.** "Kinetic Energy", "Chemical Energy", "Mechanical energy" on screen (forbidden terminology).

### Grade-Level Fit
Poor — fermentation chemistry, piston mechanics.

### Visual Quality
Good, but does not redeem content.

### Runtime
6:19.

### School-Content Boundary
**FAIL.** "Emits carbon dioxide" + "Changes climate" (climate framing); "Mechanical energy" terminology.

### Alignment
Would target Ch9 (Energy Resource Innovations), but the delivered video is terminologically and
boundary-violating. Ch9 is already well-served by deck + notes; no media is required.

### Best Placement
None.

### Trim Analysis
Not viable — forbidden terminology appears on the title card and in the biofuels benefits/costs; the biofuel
definition itself is clean but insufficient alone to justify a cut.

### Classification
DO NOT USE · SKIP · REJECT.

### Final Decision
**REJECT.** Ch9 media is not needed; the course is fine without it.

---

## Trimmed Classroom Cuts (produced)

| Output | Source | Range | Output runtime | SHA-256 |
|---|---|---|---|---|
| `fossil-fuel-formation-classroom-cut.mp4` | `Fossil_Fuel_Formation.mp4` | 94–313 s | 3:39 | `1f255f6e0c0fda2540753c085a4fe8b2905706858e35ed7c9730046f9dc8f7f8` |
| `turbine-generator-classroom-cut.mp4` | `Energy_Detectives.mp4` | 80–301 s | 3:41 | `649fbc83e7d9ad50d3b833ea00144c94f88119f61c555922bfd059d0babdb149` |

Both: single contiguous excerpts (no stitches) · h264 1280×720 24 fps · aac 44.1 kHz mono · full decode clean ·
first/last frames show clean card boundaries (no black frames) · dense OCR scan = **zero forbidden hits**.

## Unit 1 Media Redundancy Review

- New `Energy_Detectives.mp4` and `Energy_Causes_Change.mp4` are **both misnamed** — neither is a Week 1
  "ENERGY → CHANGE → EVIDENCE" video (one is electricity generation, one is grid storage). They do **not**
  duplicate or supersede the existing Ch1 set (`The_Invisible_Boss_of_Change`, `The_Energy_Detective`,
  `Stored_Energy`, `How_Scientists_Spot_Invisible_Energy`, `Why_Still_Objects_Secretly_Have_Energy`).
- No Week 1 lesson gains a video from this batch. Existing Week 1 media stays as-is (PRIMARY/OPTIONAL/SKIP
  unchanged).

## Unit 2 Script Coverage

| # | Script | Status |
|---|---|---|
| 1 | Where Does Our Energy Come From? | **REJECTED DELIVERY — REGENERATION NEEDED** (`Where_Does_Energy_Come_From_.mp4` rejected) |
| 2 | Renewable vs Nonrenewable | **PENDING** |
| 3 | Fossil Fuel Formation | **FULFILLED** — `fossil-fuel-formation-classroom-cut.mp4` |
| 4 | Coal vs Nuclear: Similar Pathway | **PARTIALLY FULFILLED** — shared steam→turbine→generator shown in turbine-generator cut; dedicated coal-vs-nuclear comparison still PENDING |
| 5 | How a Turbine Helps Make Electricity | **FULFILLED** — `turbine-generator-classroom-cut.mp4` |
| 6 | Moving Air & Water: Wind + Hydro | **FULFILLED** — `wind-hydro-power-classroom-cut.mp4` (Phase 13G) |
| 7 | Sunlight & Earth Heat: Solar + Geothermal | **REJECTED DELIVERY — REGENERATION NEEDED** (`Solar___Geothermal_Energy.mp4` rejected) |
| — | Energy Resource Innovations (Ch9) | **REJECTED DELIVERY** — `Energy_Innovations.mp4` rejected; Ch9 media not required |

## Media QA (accepted cuts)

Both accepted cuts pass: (1) decode integrity ✓ (2) audio present ✓ (3) audio sync ✓ (single contiguous
stream copy) (4) no black/frozen frames ✓ (5) no forbidden text (OCR) ✓ (6) narration not independently
verifiable — documented limitation, mitigated by clean on-screen text ✓ (7) correct science ✓
(8) understandable without missing context ✓ (9) runtime 3:39 / 3:41 ✓ (10) clean begin/end ✓.

## Guardrail scans

- **Science vocabulary:** zero hits in accepted cuts for proof/proves/kinetic/potential/mechanical energy/
  chemical energy/thermal/radiant/momentum/impulse/electron/charged particle/compression wave/base-load/
  peak demand/grid stabilization.
- **Climate/controversial:** zero hits in accepted cuts for climate change/global warming/carbon/zero carbon/
  carbon footprint/climate crisis/activism/save the planet/energy policy/carbon tax/cap and trade/green/dirty
  energy.
- Rejected sources **do** contain the flagged terms (electron, photons, Zero Emissions, thermal, kinetic/
  chemical/mechanical energy, carbon dioxide, "changes climate") — this is precisely why they were rejected.
