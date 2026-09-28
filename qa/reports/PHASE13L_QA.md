# PHASE 13L — NEW MEDIA REVIEW, TRIMMING, AND PRESENTATION INTEGRATION QA

> Automated + content QA for the Phase 13L media batch (3 new videos → 2 trimmed classroom cuts embedded in 2 Unit 1 decks, 1 rejected).

## 1. Video intake + decode QA

| Source | Duration | Res | Codec | Audio | Decode (`-f null`) | Verdict |
|---|---|---|---|---|---|---|
| `The_Journey_of_Energy.mp4` | 8:03 | 1280×720 | h264 | aac ✓ | exit 0 | PASS |
| `Energy___Speed_Are_Related.mp4` | 7:17 | 1280×720 | h264 | aac ✓ | exit 0 | PASS |
| `Unit_2_Synthesis__Energy_Detective_Masterclass.mp4` | 6:26 | 1280×720 | h264 | aac ✓ | exit 0 | PASS |

## 2. Trimmed cuts QA

| Cut | Trim | Runtime | Decode | Audio | Frozen/black frames | Sync | Clean start/end | Verdict |
|---|---|---|---|---|---|---|---|---|
| `speed-and-energy-ramp-it-up-classroom-cut.mp4` | 136–285 s | 2:29 | ✓ | ✓ | none | ✓ | scene boundaries | PASS |
| `journey-of-energy-unit1-recap-classroom-cut.mp4` | 28–197 s | 2:49 | ✓ | ✓ | none | ✓ | scene boundaries | PASS |

Both re-encoded h264 High / yuv420p + aac 44.1 kHz mono, `+faststart`, single contiguous excerpt (no stitching).

## 3. Science / vocabulary scan

Word-boundary scan of OCR across all three sources for: kinetic, potential, mechanical energy, chemical energy, thermal energy, radiant, momentum, impulse, electron, compression wave, fission, base-load, peak demand, grid stabilization, m/s, proves.

- **Video 1 (Journey):** "thermal energy" (×4), "No emissions"/"Low pollution" — all in the **untrimmed** Unit 2 tail (≥ 6:30), absent from the 28–197 s cut. No "proves".
- **Video 2 (Speed):** "proves" (×6) — conclusion slide only (~5:30–6:06), absent from the 136–285 s cut.
- **Video 3 (Masterclass):** kinetic (3) · electron (7) · baseload (16) · dispatch (19) · intermittent (2) · nuclear (8) — pervasive; not brief/trim-able. **REJECTED.**

**Result: the two accepted cuts are clean of forbidden vocabulary.** Video 3 rejected on vocabulary + content-boundary grounds.

## 4. Climate / controversial content scan

Scan for: climate change, global warming, climate crisis, carbon footprint, zero-carbon, clean/dirty/green energy, zero emissions, carbon tax, cap and trade, save-the-planet, energy policy/advocacy.

- **Video 1:** "No emissions"/"Low pollution" (Unit 2 tail only, excluded from cut). No climate/advocacy language.
- **Video 2:** clean.
- **Video 3:** "Drives climate change", "CUMULATIVE WARMING IMPACT", "Carbon-free", "Clean", "GHG LAYER (TRAPS HEAT)", "Disrupts ecosystems" → **FAIL / REJECTED.**

## 5. PPTX embed QA

| Deck | Slides (before → after) | `video/mp4` content type | slide rel → `../media/video1.mp4` (rId3) + poster (rId2) | Poster present | No absolute path | python-pptx opens | PDF renders (LibreOffice) | No overlap/clipping |
|---|---|---|---|---|---|---|---|---|
| `03-ch3-energy-speed-slides.pptx` | 28 → 29 (WATCH @ S17) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (29 pp) | ✓ |
| `07-ch7-edison-unit-synthesis-slides.pptx` | 26 → 27 (WATCH @ S13) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (27 pp) | ✓ |

- Video frames are 16:9, large (not corner thumbnail); prompt text sits below the frame (no overlap).
- Teacher-clicked playback (no `<p:timing>` → "On Click"); decks remain fully teachable without the video. **Automated playback itself is a documented limitation** (not exercised headlessly).

## 6. Doc-consistency QA

- `TWO_UNIT_MEDIA_MAP.md`, `VIDEO_PRESENTATION_INTEGRATION_MATRIX.md`, `MASTER_CURRICULUM_MAP.md`, `SOURCE_INVENTORY.md`, `WEEK1_2` + `WEEK3_4` quickstarts updated to the two new embedded slides and the +1 slide shifts.
- No guided notes / labs / assessments / study sheets / Friday Flex / Detective Chart / absent-recovery / pacing objectives changed.

**Overall: PASS.**
