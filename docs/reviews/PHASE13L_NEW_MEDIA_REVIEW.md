# PHASE 13L — NEW MEDIA REVIEW, TRIMMING, AND PRESENTATION INTEGRATION

> Review of the three newly delivered videos (`The_Journey_of_Energy.mp4`, `Energy___Speed_Are_Related.mp4`, `Unit_2_Synthesis__Energy_Detective_Masterclass.mp4`).
> Result: **2 accepted (trimmed + embedded in Unit 1 decks) · 1 rejected (DO NOT USE).** No curriculum architecture reopened.

---

## 1. Intake (copy, not move)

All three were located in `~/Downloads` and copied (not moved) into the supplemental-media convention (`assets/supplemental/media/`, git-excluded). No gitignored binaries were force-added. Transcript tooling (whisper) is **not installed**; review relied on the strongest deterministic frame review available: `ffprobe` metadata + dense frame sampling (1 frame / 6 s) + macOS Vision OCR (Swift `VNRecognizeTextRequest`) + direct visual inspection of representative frames + a full re-encode decode-integrity pass.

| # | Filename | SHA-256 | Bytes | Runtime | Res / fps | Codec | Audio |
|---|---|---|---|---|---|---|---|
| 1 | `The_Journey_of_Energy.mp4` | `ed3f5005f8143f58dc1abb77e38411b42e96d56ba4eb131bc834b2f9f8289895` | 42,506,751 | 8:03 | 1280×720 / 24 | h264 | aac ✓ |
| 2 | `Energy___Speed_Are_Related.mp4` | `a5c83c50703839fb4bbfd7cc04417be8fdfc44b86fdb68af6df1aa1fe7b7839f` | 32,776,547 | 7:17 | 1280×720 / 24 | h264 | aac ✓ |
| 3 | `Unit_2_Synthesis__Energy_Detective_Masterclass.mp4` | `8882d42e94c39d764825de41a63ad488f64da119135e3e7c70ce09efbb0add6c` | 51,885,280 | 6:26 | 1280×720 / 30 | h264 | aac ✓ |

All three decode cleanly (`ffmpeg -f null` exit 0) with intact A/V streams. All are AI-generated ("Gemini Notebook" watermark on most frames).

---

## 2. Video 1 — The Journey of Energy (8:03)

**Actual content (frame/OCR):** title → Big Question "How do we know energy is there if we can't see it?" → **Evidence of Energy** → "Energy is the ability to cause change" → ENERGY → CHANGE → EVIDENCE model → **Transfer & Transformation** ("how it moves and morphs") → **Source → Path → Receiver** → "Energy does NOT disappear" → *(then)* The Fossil Fuel Age → coal pathway (mined → burned → boils water → spins turbine → generates electricity) → resource benefits/costs → renewable resources → geothermal ("thermal energy") → engineering cycle → "How will we balance growing needs with constraints?"

**Best-fit lesson:** Unit 1 synthesis (Chapters 1, 4, 5, 6 recap). The first ~2:49 is a faithful, grade-appropriate walkthrough of the *entire* Unit 1 core model. The back half (fossil fuels / renewables / benefits-costs) belongs to Unit 2.

**Science review:** ✅ Accurate. ENERGY→CHANGE→EVIDENCE and SOURCE→PATH→RECEIVER match the locked model; transfer (moves) vs transformation (morphs) distinguished; "energy does not disappear" is correct. ❌ One advanced term: "**thermal energy**" (geothermal wastewater slide, ~6:36) — outside the Grade 4 vocabulary and outside the trimmed excerpt.

**Vocabulary review:** ⚠️ "thermal energy" (×4, geothermal section). "No emissions" / "Low pollution" (renewable benefits table) are mild emissions framing in the Unit 2 half. Both are **outside** the trimmed excerpt.

**Climate/policy scan:** ⚠️ "No emissions" / "Low pollution" in the Unit 2 half (benefits column); no climate-change/crisis/policy/activism language. Not present in the trimmed excerpt.

**Redundancy:** DUPLICATES Unit 1 Ch1/Ch4/Ch6 slide + guided-note content, but there is **no existing accepted Unit 1 video**, so the excerpt is UNIQUE among media. COMPLEMENTS the `07-ch7` review slide section.

**Trim decision:** TRIM. Contiguous excerpt **28 s → 197 s (2:49)** = Big Question → Evidence of Energy → energy = cause change → transfer/transformation → source/path/receiver → energy does not disappear. Clean start (Big Question card) and clean end (before "The Fossil Fuel Age" card at 198 s).

**Final placement / embed:** **EMBEDDED** in `07-ch7-edison-unit-synthesis-slides.pptx` at **S13** (after "Engineering is a cycle", before the Ch1–6 review section). Tagged **"WATCH — Unit 1 Energy Core Recap" · Optional video · 2:49 · Week 4**. Post-video prompt: *"THINK: What evidence tells us energy is there, even when we can't see it?"*

**Final classification:** ROLE **SUPPORT** · CLASSROOM **OPTIONAL** (SHOW as synthesis recap) · MEDIA STATUS **TRIM → USE**.

---

## 3. Video 2 — Energy & Speed Are Related (7:17)

**Actual content (frame/OCR):** title → hook "If you catch a fast-moving ball, why does it sting?" → **Activity 4.1 Ramp It Up!** (rubber ball · cardboard ramp · paper cup · starting line; Big Question "does a higher roll push the cup farther?") → **The Fair Test: Isolating Variables** ("Keep the SAME mass… CHANGE the ramp height") → **Ramp Results** ("Low Height = Slower, High Height = Faster"; draw cup position) → **data table** (1 book = 4 cm, 3 books = 11 cm) → "Move Faster → Greater Change → More Energy — **Proves** more energy of motion" → **Golden Rule of Speed**: "For the SAME object, faster motion means MORE energy of motion" → final question.

**Best-fit lesson:** Unit 1 · Week 2 · Chapter 3 (Ramp It Up! investigation).

**Science review:** ✅ Strong. Correctly isolates the SAME object (locks ball/mass) while changing ramp height → inferred speed → measured cup displacement → inferred energy of motion. Matches the locked science model exactly (SAME object · different speeds · ramp height · cup displacement; relative speed/energy are *inferred*, never measured). No fake m/s; no mass comparison; no unsupported proportionality. ❌ One violation: the conclusion slide says "**Proves** more energy of motion" (~5:30–6:06) — "proves" is on the locked reject list.

**Vocabulary review:** ⚠️ "**proves**" (×6, conclusion slide only). No kinetic/potential/mechanical/thermal vocabulary. No invented units.

**Climate/policy scan:** ✅ Clean. No climate/carbon/policy language anywhere.

**Redundancy:** UNIQUE — no existing accepted Unit 1 Ch3 media; the animated fair-test + data walkthrough is not covered by any existing cut. Complements (does not replace) the Ramp It Up setup diagram and guided notes.

**Trim decision:** TRIM. Contiguous excerpt **136 s → 285 s (2:29)** = Ramp It Up setup → fair test → results → data table. Ends cleanly at the data table (transition to blank at ~287 s), **before** the "Proves" conclusion (~356–366 s).

**Final placement / embed:** **EMBEDDED** in `03-ch3-energy-speed-slides.pptx` at **S17** (after "Procedure", before "Data table"). Tagged **"WATCH — Ramp It Up in Action" · Optional video · 2:29 · Week 2**. Post-video prompt: *"THINK: Which variable changed, and which stayed the same?"*

**Final classification:** ROLE **SUPPORT** · CLASSROOM **OPTIONAL** (SHOW before the lab, teacher-clicked) · MEDIA STATUS **TRIM → USE**.

---

## 4. Video 3 — Unit 2 Synthesis: Energy Detective Masterclass (6:26)

**Actual content (frame/OCR):** renewable vs nonrenewable timescale (Human Lifespan ~80 yrs vs Geologic Time) → **FOSSIL FUEL COMBUSTION / THERMAL GENERATION STATION** ("High Energy Density Dispatchable Power", "24/7 BASELOAD RELIABILITY", "100% UNBROKEN DISPATCH", "ATMOSPHERIC ACCUMULATION", "CO₂, CH₄ & GHG LAYER (TRAPS HEAT)", "CUMULATIVE WARMING IMPACT") → **THE CORE MECHANISM / DIRECT KINETIC ENERGY CONVERSION** → wind turbine "energy of motion in action" → hydro (garbled) → **PHOTOVOLTAIC CELL** (n-type silicon / p-n junction / depletion zone / electron holes) → OUTLIER TECHNOLOGY / BIOFUELS → EVALUATION → combustion & steam pressure → **ENERGY DETECTIVE MATRIX / ENERGY RESOURCES SUMMARY GRID** ("Fossil Fuels: − Drives climate change", "Nuclear: + Carbon-free − Radioactive waste", "Wind: + Clean − Intermittent", "Hydro: − Disrupts ecosystems", "Solar: + Clean − Intermittent") → GRID TRANSMISSION NETWORK / SUBSTATION / ENGINEER CONTROL DESK.

**Best-fit lesson:** None. It is a technical "masterclass" pitched above Grade 4 and above the locked content boundary.

**Science review:** ❌ Mis-leveled and boundary-violating throughout: baseload/dispatch/grid economics, kinetic energy conversion, photovoltaic p-n junction electron mechanics.

**Vocabulary review:** ❌ Pervasive advanced vocabulary: "baseload" (16), "dispatch" (19), "kinetic" (3), "electron" (7), "nuclear" (8), "intermittent" (2), "ecosystem". Not brief, not harmless, not trim-able (they are the substance of the middle and end).

**Climate/policy scan:** ❌ FAIL. "Drives climate change", "CUMULATIVE WARMING IMPACT", "Carbon-free", "Clean" (energy framing), "GHG LAYER (TRAPS HEAT)", "Disrupts ecosystems". This is exactly the locked climate/advocacy/ranking framing that is forbidden.

**Redundancy:** The only clean sections (renewable-vs-nonrenewable timescale; wind "energy of motion in action") DUPLICATE `fossil-fuel-formation-classroom-cut.mp4`, the Ch1 renewable/nonrenewable deck, and `wind-hydro-power-classroom-cut.mp4`. No unique value.

**Trim decision:** REJECT. No single contiguous clean excerpt that is uniquely valuable and non-duplicative (the banned content is the majority of the runtime).

**Final placement / embed:** Not embedded.

**Final classification:** ROLE **DO NOT USE** · CLASSROOM **SKIP** · MEDIA STATUS **REJECT**.

---

## 5. Redundancy review

| New video | vs existing accepted media | Verdict |
|---|---|---|
| Journey of Energy (Unit 1 core excerpt) | No existing Unit 1 video; complements `07-ch7` review slides | **COMPLEMENTS / UNIQUE** |
| Energy & Speed (Ramp It Up excerpt) | No existing Unit 1 Ch3 media; complements setup guide + notes | **UNIQUE** |
| Masterclass | Duplicates fossil-fuel + wind-hydro cuts + Ch1 deck; adds only banned content | **DUPLICATES / INFERIOR → REJECT** |

No accepted media was replaced or deleted.

---

## 6. Trimmed cuts created

| Cut | Source | Trim | Runtime | SHA-256 | Bytes |
|---|---|---|---|---|---|
| `speed-and-energy-ramp-it-up-classroom-cut.mp4` | `Energy___Speed_Are_Related.mp4` | 136–285 s | 2:29 | `e37776710249f75c1596d302060199c0b9e4a02b81106d02e954dca42f69c9c9` | 4,868,741 |
| `journey-of-energy-unit1-recap-classroom-cut.mp4` | `The_Journey_of_Energy.mp4` | 28–197 s | 2:49 | `8dc946665f0db32e164205821fe39ab09896d405de7433acbe39c8110a6f7664` | 6,778,034 |

Both re-encoded h264 High / yuv420p + aac 44.1 kHz mono, `+faststart`, single contiguous excerpt each (no stitching). Both pass decode + audio + sync.

---

## 7. Presentation integration

- `03-ch3-energy-speed-slides.pptx` (28 → **29** slides): embedded `speed-and-energy-ramp-it-up-classroom-cut.mp4` at **S17** (poster = fair-test frame).
- `07-ch7-edison-unit-synthesis-slides.pptx` (26 → **27** slides): embedded `journey-of-energy-unit1-recap-classroom-cut.mp4` at **S13** (poster = source/path/receiver frame).

Embedding = native portable media relationship (`<a:videoFile r:link>` + `<p14:media r:embed>` + `<a:blip>` poster), not a file-path hyperlink. Teacher-clicked (no timing → "On Click"). No static instructional slide was deleted. Later slide numbers shifted +1 in each deck; the affected quickstart/map references were updated (see §8–9).

---

## 8. Media map updates

- `docs/planning/TWO_UNIT_MEDIA_MAP.md`: corrected the "No MP4 is embedded" header (stale since Phase 13J); added a **Phase 13L delivered files** table (3 sources + 2 cuts); added the masterclass to the DO NOT USE list; added the two Unit 1 cuts to load rules.
- `production/final-8.5-week/VIDEO_PRESENTATION_INTEGRATION_MATRIX.md`: added the two Unit 1 EMBEDDED rows; added the masterclass to the rejected list.
- `production/final-8.5-week/MASTER_CURRICULUM_MAP.md`: Week 2 Ch3 and Week 4 Ch7 slide ranges updated to reflect the +1 shifts and the new embedded slides.
- `SOURCE_INVENTORY.md`: added entries #100–#102 (3 new media) + discovery paths + Phase 13L intake note.

---

## 9. Quickstart updates

- `WEEK1_2_TEACHER_QUICKSTART.md` (Week 2): Wed → `03-ch3 S15–S19` (optional WATCH S17); Thu → `S16 + S18`; Fri → `S19–S24`; one-line day map updated.
- `WEEK3_4_TEACHER_QUICKSTART.md` (Week 4): Wed notes optional S13 recap; Fri → `07-ch7 S25–S27`.

No guided notes, labs, assessments, study sheets, Friday Flex, Resource Detective Chart, absent-recovery, or pacing objectives were changed.

---

## 10. QA results

**Video QA (accepted cuts):** decode ✓ · audio ✓ · sync ✓ · no frozen/black frames (spot-checked) ✓ · no unresolved forbidden vocabulary in the trimmed excerpt ✓ · no climate/policy framing in the trimmed excerpt ✓ · science aligned ✓ · Grade 4 understandable ✓ · self-contained ✓ · runtime 2:29 / 2:49 (within 90 s–3 min) ✓ · clean start/end ✓.

**PPTX embed QA (both decks):** `video/mp4` + `image/jpeg` content types present ✓ · slide relationship points to embedded `../media/video1.mp4` (rId3) + poster (rId2) ✓ · poster image present ✓ · no absolute local path ✓ · opens in python-pptx (29 / 27 slides) ✓ · renders to PDF via LibreOffice (29 / 27 pages) ✓ · no slide corruption ✓ · no overlap/clipping (video frame 16:9, prompt below) ✓. **Playback itself is a documented limitation** (not exercised headlessly).

**Science vocabulary scan (OCR across all three):** kinetic 3 · thermal energy 4 · electron 7 · baseload 16 · dispatch 19 · intermittent 2 — all confined to Video 3 (rejected) or to the *untrimmed* tails of Video 1. "proves" ×6 confined to Video 2's conclusion slide, excluded by the trim.

**Climate / controversial content scan:** carbon 13 · climate 2 · emissions 6 · "Drives climate change" · "CUMULATIVE WARMING IMPACT" · "Carbon-free" · "Clean" — all confined to Video 3 (rejected) or Video 1's untrimmed Unit 2 tail.

---

## 11. Final classification table

| FILE | RUNTIME | ACTUAL TOPIC | PLACEMENT | ROLE | ACTION | EMBED STATUS |
|---|---|---|---|---|---|---|
| `Energy___Speed_Are_Related.mp4` | 7:17 | Ramp It Up fair test + speed→change→energy of motion | U1 Ch3 · Wk 2 (S17) | SUPPORT | TRIM (136–285 s) → 2:29 | **EMBEDDED** `03-ch3` S17 |
| `The_Journey_of_Energy.mp4` | 8:03 | Unit 1 energy core: evidence → transfer/transformation → source/path/receiver | U1 synthesis · Wk 4 (S13) | SUPPORT | TRIM (28–197 s) → 2:49 | **EMBEDDED** `07-ch7` S13 |
| `Unit_2_Synthesis__Energy_Detective_Masterclass.mp4` | 6:26 | Grid/baseload/dispatch + photovoltaic + resource "ranking" | none | DO NOT USE | REJECT | — |

---

## 12. Remaining useful media gaps

No new gaps introduced by this review. (Pre-existing, already-documented PENDING slots are unchanged: Unit 1 Ch3–7 script slots and Unit 2 #2/#4/#7.)

## 13. Whole-course media status

**COMPLETE WITH OPTIONAL GAPS** — Unit 1 and Unit 2 now each have accepted, embedded classroom cuts; the only open slots are the long-documented script-only PENDING slots, which do not block the classroom package.
