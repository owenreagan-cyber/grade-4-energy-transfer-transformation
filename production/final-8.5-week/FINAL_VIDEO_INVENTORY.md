# FINAL VIDEO INVENTORY — Grade 4 Energy (Frozen Premium Release)

> Authoritative media registry for the frozen release. Replaces the per-phase media tables as the single source of truth for video state. Companion: `VIDEO_PRESENTATION_INTEGRATION_MATRIX.md` (embedding state) and `docs/planning/TWO_UNIT_MEDIA_MAP.md` (full source review history).
> **Allowed statuses:** EMBEDDED — CORE · EMBEDDED — SUPPORT · EMBEDDED — FLEX · OPTIONAL EXTERNAL · PRODUCTION READY — OPTIONAL — NO BINARY · REJECTED — DO NOT USE · DUPLICATE · SUPERSEDED.
> **Playback:** all embedded videos are teacher-clicked ("On Click"), H.264 + AAC, 1280×720, poster frame + "WATCH — m:ss" cue + one-line THINK prompt + speaker note (ROLE/PLAY/PURPOSE/SKIP IF).

---

## 1. Embedded classroom cuts (5 · active)

| # | Classroom cut | Unit · Ch | Week/Day | Deck · Slide | Runtime | Role | Source hash (cut) |
|---|---|---|---|---|---|---|---|
| 1 | Ramp It Up — Energy & Speed | U1 · Ch3 | Wk 2 Wed | `03-ch3-energy-speed-slides.pptx` S17 | 2:29 | SUPPORT | `e3777671…69c9c9` |
| 2 | Journey of Energy — Unit 1 recap | U1 · Ch7 | Wk 4 synthesis | `07-ch7-edison-unit-synthesis-slides.pptx` S13 | 2:49 | SUPPORT | `8dc94666…a6f7664` |
| 3 | Fossil Fuel Formation | U2 · Ch2 | Wk 5 Wed | `02-u2-ch2-slides.pptx` S7 | 3:39 | SUPPORT | `1f255f6e…9dc8f7f8` |
| 4 | Turbine & Generator | U2 · Ch3 | Wk 6 Tue | `03-u2-ch3-slides.pptx` S7 | 3:41 | SUPPORT | `649fbc83…0babdb149` |
| 5 | Wind & Hydro (wind-only cut) | U2 · Ch5 | Wk 7 Mon | `05-u2-ch5-slides.pptx` S6 | 1:35 | SUPPORT | `0d4ec2bd…a321864dbd` |

Each row verified against the actual PPTX package (extracted `video1.mp4` SHA-256 matches the classroom-cut hash; H.264 + AAC; decode clean).

| # | Source file | Source SHA-256 | Classroom cut | Cut SHA-256 |
|---|---|---|---|---|
| 1 | `Energy___Speed_Are_Related.mp4` | `a5c83c50703839fb…` | `speed-and-energy-ramp-it-up-classroom-cut.mp4` | `e37776710249f75c…` |
| 2 | `The_Journey_of_Energy.mp4` | `ed3f5005f8143f58…` | `journey-of-energy-unit1-recap-classroom-cut.mp4` | `8dc946665f0db32e…` |
| 3 | `Fossil_Fuel_Formation.mp4` | `08d59d655194e10b…` | `fossil-fuel-formation-classroom-cut.mp4` | `1f255f6e0c0fda25…` |
| 4 | `Energy_Detectives.mp4` (turbine) | `e341dec3242ed232…` | `turbine-generator-classroom-cut.mp4` | `649fbc83e7d9ad50…` |
| 5 | `Wind___Hydro_Power.mp4` | `db03356e8b3aea0b…` | `wind-hydro-power-classroom-cut.mp4` | `0d4ec2bd866c5315…` |

---

## 2. Optional script-ready videos (3 · no binary)

| # | Working title | Script | Status |
|---|---|---|---|
| 1 | Where Does Our Energy Come From? | `production/media/scripts/unit-02/01-where-does-our-energy-come-from-final-script.md` | PRODUCTION READY — OPTIONAL — NO BINARY |
| 2 | Coal vs Nuclear — Same Pathway, Different Heat Source | `production/media/scripts/unit-02/04-coal-vs-nuclear-final-script.md` | PRODUCTION READY — OPTIONAL — NO BINARY |
| 3 | Sunlight & Earth Heat — Solar + Geothermal | `production/media/scripts/unit-02/07-solar-geothermal-final-script.md` | PRODUCTION READY — OPTIONAL — NO BINARY |

Each has a premium drop-in WATCH slot already staged: `01-u2-ch1` S4 · `04-u2-ch4` S6 · `08-u2-ch8` S9. No binary exists; this is **not** a curriculum gap.

---

## 3. Rejected sources (DO NOT USE — excluded from every lesson)

| File | Reason |
|---|---|
| `Where_Does_Energy_Come_From_.mp4` | mechanical energy + carbon/zero-carbon framing + grid jargon |
| `Power_Plant_Energy_Transformations__Tracing_the_Grid.mp4` | fission equations + kinetic/potential/chemical/thermal vocabulary |
| `Solar___Geothermal_Energy.mp4` | electron/photon mechanics + "Zero Emissions" |
| `The_Timescale_Tradeoff__Physics,_Economics,_and_the_Energy_Grid.mp4` | grid economics/policy |
| `Energy_Causes_Change.mp4` | grid storage/thermal + "ZERO EMISSIONS" |
| `Energy_Innovations.mp4` | kinetic/chemical/mechanical + climate framing |
| `Unit_2_Synthesis__Energy_Detective_Masterclass.mp4` | baseload/dispatch/grid + climate + photovoltaic p-n junction |
| `Wind___Hydro_Power.mp4` (full 9:09) | only its 1:35 wind cut ships; full file DO NOT USE |
| `Collision_Dynamics___Mass_Effect.mp4` | mass-as-core + momentum/force/kinetic/equations (Phase 13O) |

---

## 4. Unit 1 historical / unstaged sources (final resolution)

| File | Final status |
|---|---|
| `Collision_Dynamics___Mass_Effect.mp4` | REJECTED — DO NOT USE (13O) |
| `Transfer_vs.mp4` | OPTIONAL EXTERNAL — TRIM candidate; redundant with Ch4/Ch6 deck + journey cut (13O) |
| `The_Unseen_Mover.mp4` | OPTIONAL EXTERNAL — TRIM candidate; redundant with Ch4 deck (13O) |
| `What_Happens_in_a_Collision_.mp4` | OPTIONAL EXTERNAL — TRIM candidate (strongest); trim never audio-confirmed, not embedded (13O) |
| `Engineering_a_Door_Alert.mp4` | HISTORICAL REVIEW ONLY — raw in `~/Downloads`, never staged/reviewed |
| `Energy_Transformations.mp4` | HISTORICAL REVIEW ONLY — raw in `~/Downloads`, never staged/reviewed |
| `Edison_s_Light_Bulb.mp4` | HISTORICAL REVIEW ONLY — raw in `~/Downloads`, never staged/reviewed |
| `Energy_Transfer___Transformation_Masterclass.mp4` | HISTORICAL REVIEW ONLY — raw in `~/Downloads`, never staged/reviewed |
| `Investigating_Craters.mp4` | HISTORICAL REVIEW ONLY — raw in `~/Downloads`, never staged/reviewed |

> None of the "HISTORICAL REVIEW ONLY" files is staged under `assets/supplemental/media/` and none is referenced by any active teacher/student document. They remain untouched in `~/Downloads` only.

---

## 5. Counts

| Category | Count |
|---|---|
| EMBEDDED — SUPPORT | 5 |
| EMBEDDED — CORE | 0 |
| EMBEDDED — FLEX | 0 |
| OPTIONAL EXTERNAL (raw/unstaged, not embedded) | 3 (Unit 1 trim candidates) |
| PRODUCTION READY — OPTIONAL — NO BINARY | 3 |
| REJECTED — DO NOT USE | 9 |
| SUPERSEDED / HISTORICAL REVIEW ONLY | 5 |
