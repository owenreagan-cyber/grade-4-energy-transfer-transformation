# PHASE 13F — Unit 2 Media Review

> Intake + scientific review of the three newly supplied Unit 2 videos. Reviewed by filename-independent inspection: SHA-256, byte size, `ffprobe` metadata (runtime/resolution/codec/frame rate/audio), full-decode integrity check, and frame-by-frame OCR of on-screen text (macOS Vision `VNRecognizeTextRequest`) — not by title alone.

**Headline result:** all three delivered videos are AI-generated "Gemini Notebook"-style explainers that overshoot the Grade 4 content boundary. **None is classroom-ready as delivered.** Two are DO NOT USE; one needs trimming (Week 7 — deferred to Phase 13G). No video is placed in the live Week 5–6 pacing.

---

## On-disk intake record

| File | Source path | SHA-256 (first 16) | Bytes | Runtime | Resolution | Video codec / fps | Audio | Integrity |
|---|---|---|---|---|---|---|---|---|
| `Where_Does_Energy_Come_From_.mp4` | `~/Downloads/` | `f49baa4eae364f03…` | 35,694,516 | 7:19 | 1280×720 | h264 / 24 | aac ✓ | decodes clean |
| `Power_Plant_Energy_Transformations__Tracing_the_Grid.mp4` | `~/Downloads/` | `ce8f4052b50c5526…` | 42,974,182 | 5:00 | 1280×720 | h264 / 30 | aac ✓ | decodes clean |
| `Wind___Hydro_Power.mp4` | `~/Downloads/` | `db03356e8b3aea0b4…` | 46,136,929 | 9:09 | 1280×720 | h264 / 24 | aac ✓ | decodes clean |

Full hashes recorded in `docs/planning/TWO_UNIT_MEDIA_MAP.md`.

Copied (not moved) into the project convention: `assets/supplemental/media/unit-02/chapter-0X/` (supplemental media is git-excluded; metadata is tracked in the media map).

---

## 1. Where Does Energy Come From? — DO NOT USE (needs regeneration)

- **Runtime cost:** 7:19 — too long for a 30-min Unit 2 launch block.
- **Content summary (from OCR):** "When you flip a switch, what actually changed?" → renewable vs nonrenewable definitions → "Abundant" + "Deep time/Near-time" → fossil-fuel formation ("layers of coal take millions of years") → coal mining → "burn coal → boil water → steam → turbine → generator → electricity" → "energy changes form … like motion becoming electricity" → costs/benefits → "How will this shape our future grid?"

- **Science accuracy:** core transfer/transformation and steam→turbine→generator pathway are sound.
- **Vocabulary concerns:** ⚠️ "**mechanical energy**" (forbidden); "**intermittent**" (advanced); "**energy grid / future grid**" (jargon beyond Grade 4 need).
- **Framing concerns:** ⚠️ "**Our energy grid is mostly nonrenewable (83% / 17%)**" statistic; "**Carbon emissions**", "**Zero carbon**", "**Clean**" — climate/advocacy-adjacent framing that violates the conservative-school content boundary ("no climate change instruction", "no carbon footprint", "remain neutral").
- **Visual quality:** clean, legible; Gemini Notebook watermark.
- **Pacing value:** the renewable/nonrenewable + abundant≠renewable content matches Ch1, but is buried under grid statistics and carbon framing.
- **Overlap with slides:** heavy — `01-u2-ch1` deck already covers the same core in clean, neutral language.
- **Verdict:** **DO NOT USE** as delivered. Needs regeneration against the approved script #1 ("Where Does Our Energy Come From?", ~90 s, clean). **SHOW: no · OPTIONAL: no · SKIP.**

---

## 2. Power Plant Energy Transformations: Tracing the Grid — DO NOT USE

- **Runtime cost:** 5:00.
- **Content summary (from OCR):** power-plant pathway with **nuclear fission equations** (U-235 + neutron → fission products, helium nuclei), "**CHEMICAL → THERMAL → MECHANICAL → ELECTRICAL**" energy-chain labels, "**Kinetic Motion**", "**K = ½·m·v²**", "FISSION", "NUCLEUS", "DECAY", "COMBUSTION", "Reactor Core → Boiler/Steam → Turbine → Generator".

- **Science accuracy:** technically correct, but at a high-school/college level.
- **Vocabulary concerns:** ❌ **fission detail** (explicitly NOT required), **kinetic / potential / mechanical / chemical / thermal energy** (all forbidden), "grid" (jargon).
- **Grade 4 fit:** ❌ far beyond the course ceiling.
- **Framing concerns:** none political, but fundamentally mis-leveled.
- **Pacing value:** none for Grade 4; the shared pathway is already taught cleanly in `03-u2-ch3` S6 and `04-u2-ch4` S6.
- **Verdict:** **DO NOT USE.** Not salvageable by trimming. **SHOW: no · SKIP.**

---

## 3. Wind + Hydro Power — needs trimming (Week 7 · deferred to Phase 13G)

- **Runtime cost:** 9:09 — too long for one block.
- **Content summary (from OCR):** "Moving air transfers energy to cause blades to rotate" → "Energy of Motion" (course-approved term ✓) → gravity pulls water through a dam/reservoir → turbine → generator → "generator transforms motion to electricity" → "offshore wind … faces severe constraints" → "Zero Combustion" → "How will **climate change** affect renewable power?" → "Carbon?" → "Coal Combusts?" / SMOKE / FLAME comparison.
- **Science accuracy:** wind + hydro pathway is sound; uses the course-approved "Energy of Motion" consistently.
- **Vocabulary concerns:** mostly clean ("Energy of Motion", transfer/transform, gravity, turbine, generator). "climate change" is the single term-boundary violation.
- **Framing concerns:** ⚠️ "**How will climate change affect renewable power?**" (forbidden climate-change instruction); "**Zero Combustion**" + SMOKE/FLAME coal comparison (mild advocacy tilt); "**Carbon?**".
- **Visual quality:** clean; Gemini Notebook watermark.
- **Pacing value:** good Week 7 Ch5/Ch6 anchor IF the climate/carbon lines are trimmed.
- **Verdict:** **DO NOT USE as delivered — needs trimming** (remove climate-change + carbon + "zero combustion" lines; cut to ≤3 min). Week 7 review deferred to Phase 13G; no Week 7 pacing changes made here beyond a media-map status note. **SHOW: no · SKIP (pending trim).**

---

## Media safety / scope scan (automated, across all three)

| Term | Where | Grid | Wind |
|---|---|---|---|
| climate change | — | — | ✓ |
| carbon / carbon footprint | ✓ (Carbon emissions, Zero carbon) | ✓ (CLEAN) | ✓ (Carbon?) |
| mechanical energy | ✓ (×3) | ✓ | — |
| kinetic / potential | — | ✓ (KINETIC, POTENTIAL, K=½mv²) | — |
| chemical / thermal / electrical energy labels | — | ✓ | — |
| fission | — | ✓ (×7+) | — |
| electrons / charged particles | — | ✓ (nuclear notation) | — |
| grid / base-load / grid stabilization | ✓ (×7) | ✓ (title) | — |
| intermittent | ✓ (×4) | — | — |
| save the planet / advocacy | — | — | ✓ (Zero Combustion, smoke/flame) |

## Classification summary

| Video | CORE / SUPPORT / FLEX / DO NOT USE | SHOW / OPTIONAL / SKIP |
|---|---|---|
| Where Does Energy Come From? | DO NOT USE (needs regeneration) | SKIP |
| Power Plant Energy Transformations | DO NOT USE | SKIP |
| Wind + Hydro Power | DO NOT USE as-is (needs trimming) | SKIP (Week 7, Phase 13G) |

**Final disposition:** no video earns CORE/SUPPORT placement in Week 5–6. The Unit 2 script slots in `TWO_UNIT_MEDIA_MAP.md` remain the authoritative generation targets; the delivered files are recorded as STAGED-but-rejected/needs-trimming so a future pass does not re-classify them by filename.
