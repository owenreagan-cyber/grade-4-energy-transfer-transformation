# Chapter 1 — Video Content & Narration Review (Phase 5H)

Method: `ffprobe` metadata + full-frame `ffmpeg` extraction + `tesseract` OCR of on-screen text +
**faster-whisper (base.en, CPU int8) spoken-word transcription** of all 19 candidate videos.
Transcripts are preserved in `transcripts/`. This is the first Chapter 1 media pass with full
narration verification — Phase 5G could only OCR frames (no STT), which is why it embedded zero videos.

## What narration transcription changed

Phase 5G could not verify spoken words, so it embedded nothing. Phase 5H transcribed all 19 videos and
found that **17 of 19 contain off-scope or banned narration** ("proof/prove", "transfer", "transforms",
"collision", "wind turbine", "grid", "kinetic/potential/mechanical/radiant", "electrical current",
"physical work"). Exactly **2** are clean.

## Narration term audit (deterministic grep of transcripts)

| File | Off-scope / banned terms found in narration |
|---|---|
| `Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4` | proof, prove, transfer, electrical current, work against, baseline |
| `Energy_Causes_Change__The_Energy_Detective.mp4` | (technical: acoustic output / baseline inventory / visual geometry) |
| `Energy_Causes_Change.mp4` | renewable / grid (Unit 2) |
| `Energy_Detective.mp4` | collision (Ch.2/Ch.5) |
| `Energy_Detectives.mp4` | wind turbines / generation (Unit 2) |
| `Energy_Detectives_Briefing.mp4` | prove, proves |
| `The_Energy_Detective.mp4` | transfer (×3), collision (×3), turbine, transforms, proves, proof |
| `The_Energy_Detective-2.mp4` | proves (×2), prove, proof |
| `The_Energy_Detective-3.mp4` | proof |
| `The_Energy_Detective-4.mp4` | (marble collision, Ch.2/Ch.5) |
| `Chapter_1_Review.mp4` | (electrical-to-light transformation, Ch.6) |
| `Chapter_1_Science_Notebook.mp4` | transforms (×3), grid (×3), transfer, radiant, proves, proof, potential, mechanical |
| `The_Invisible_Boss_of_Change.mp4` | (Ch.2 opener per manifest) |
| `The_Unseen_Mover.mp4` | (motion hook, Ch.2) |
| `How_Change_Proves_Energy_Exists.mp4` | proves, transfer, transforms |
| `How_Physical_Change_Proves_Energy_Exists.mp4` | proof, transfer, mechanical |
| `How_Scientists_Spot_Invisible_Energy.mp4` | prove, proof, "zero scientific proof of energy" |
| **`Stored_Energy.mp4`** | **none** |
| **`Why_Still_Objects_Secretly_Have_Energy.mp4`** | **none** |

## Approved clips (full narration verified)

### `Stored_Energy.mp4` (4:37, 1280×720, h264+aac) — APPROVED_EMBEDDED
- Quotes the canonical V2 definition verbatim: *"Stored energy is simply energy that has the ability
  to cause change at a later time."*
- Covers N3 examples exactly: battery in a flashlight (still → bulb later), stretched rubber band,
  raised apple "because of its high position."
- No "proof/prove", no "transfer/transform", no advanced vocabulary.
- Minor notes (non-blocking, consistent with `MEDIA_ASSET_MANIFEST.md` "KEEP WITH NOTES"): the limp
  rubber band is called "zero stored energy" (a defensible elastic contrast); "ready to change into
  motion and sound" is a colloquial release description, not a formal transformation lesson.

### `Why_Still_Objects_Secretly_Have_Energy.mp4` (1:16, 720×1280 portrait) — APPROVED_ALTERNATE
- Clean: "Energy is just the ability to cause a change"; "hidden ability to cause a change at a later
  time is stored energy"; "stillness doesn't mean it has zero energy."
- Correctly refutes the "still = zero energy" misconception (the on-screen "Stillness + Zero Energy"
  frame is the question being corrected).
- NOT embedded: portrait 9:16 letterboxes poorly in a 16:9 deck, and it directly answers the slide-23
  "still battery" prediction, so it must come after slide 25's reveal. Provided as a Friday-FLEX option.

## Rejected clips (17)

All 17 rejected — banned "proof/prove" language and/or off-scope content (formal transfer, formal
transformation, collisions, wind turbines, power grid, electrical current, "physical work", or an
interactive-workbook format that injects student prompts). Rejection rationale per file is in
`CH1_VIDEO_INVENTORY_5H.md`.

## Decision

Only `Stored_Energy.mp4` meets the embedding bar (on-scope, no banned narration, landscape, already
manifest-REVIEWED). It is genuinely embedded on slide 25.
