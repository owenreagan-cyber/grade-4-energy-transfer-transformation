# Chapter 1 — Video Content Audit & Classification (Phase 5G)

> Audited the actual video content (ffprobe metadata + extracted frames + tesseract OCR of on-screen text). **A filename or metadata report is not proof of suitability.** Narration (spoken audio) could not be transcribed — no speech-to-text tool is available in this environment — so no candidate can be fully content-verified for spoken language.

## Method

- `ffprobe` for codec/duration/audio/resolution.
- `ffmpeg` frame extraction at 5–240 s across all candidates.
- `tesseract` OCR of extracted frames for on-screen language.
- Cross-checked the existing `docs/planning/MEDIA_ASSET_MANIFEST.md` verdicts.

## Classification

| File | Duration | Codec | OCR evidence | Verdict |
|---|---|---|---|---|
| `Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4` | 3:05 | h264+aac 720p | "Your Turn: Log Your Evidence", "Draw the BEFORE and the AFTER", "moving toy car, ringing bell" | **REJECTED** — interactive workbook video with baked student prompts, not a clean pencil-sharpener demonstration |
| `Energy_Causes_Change__The_Energy_Detective.mp4` | 3:49 | h264+aac 720p | "PRE-ACTION BASELINE INVENTORY", "STRUCTURAL FORM", "VISUAL GEOMETRY (BASELINE) Ho=180 mm", "ACOUSTIC OUTPUT", "SOUND EMISSION (BASELINE)" | **REJECTED** — advanced measurement/technical terminology off-scope for Grade 4 Ch.1 |
| `Energy_Causes_Change.mp4` | 6:43 | h264+aac 720p | "wind stops or the sun sets", "Renewable Energy", "Balancing the grid" | **REJECTED** — renewable energy / power grid = Unit 2 content, not Ch.1 |
| `Energy_Detective.mp4` | 5:48 | h264+aac 720p | "Moving Car / Target Car", "the collision caused a change in shape", "The dent is evidence" | **REJECTED** — collision content = Ch.2/Ch.5 |
| `Energy_Detectives.mp4` | 7:17 | h264+aac 720p | "Wind Turbines", "generate electricity" | **REJECTED** — wind turbines/generation = Unit 2 |
| `The_Energy_Detective-4.mp4` | 5:48 | h264+aac 720p | "Target marble changes position", "Moving marble hits the target" | **REJECTED** — marble collision = Ch.2/Ch.5 |
| `Chapter_1_Review.mp4` | 7:17 | h264+aac 720p | "Explanation: Electrical to light", "Light energy" | **REJECTED** — transformation ("electrical to light") = Ch.6 scope |
| `The_Invisible_Boss_of_Change.mp4` | 2:50 | h264+aac 720p | (manifest: "terminology may extend beyond Ch.1") | **REJECTED** for Ch.1 — cinematic Ch.2 opener per manifest |
| `The_Unseen_Mover.mp4` | (26 MB) | h264+aac | motion/hook, wrong-chapter | **REJECTED** — motion hook (Ch.2) |
| `How_Change_Proves_Energy_Exists.mp4` · `How_Physical_Change_Proves_Energy_Exists.mp4` | 1:16 / — | h264+aac | title uses "Proves" | **REJECTED** — "proves" is banned terminology (project standard: "supports/shows") |
| `Stored_Energy.mp4` | 4:37 | h264+aac 720p | "Stored Energy", "The Battery · Sitting still · Not causing change… yet · Ready to power the bulb", "Apple held high", "Book on a tall shelf" | **MEDIA_REVIEW_REQUIRED** — visuals match Ch.1 N3 exactly; narration unverified (could contain "potential/gravitational") |
| `How_Scientists_Spot_Invisible_Energy.mp4` | 1:16 | h264+aac 720×1280 | "Ability to Cause Change", "CHANGE", "EVIDENCE", "Acoustic Vibration" | **MEDIA_REVIEW_REQUIRED** — ENERGY→CHANGE→EVIDENCE is on-scope but "Acoustic Vibration" is off-scope; vertical aspect |
| `Why_Still_Objects_Secretly_Have_Energy.mp4` | 1:16 | h264+aac 720×1280 | "Stillness + Zero Energy", "object resting" | **MEDIA_REVIEW_REQUIRED** — "Stillness + Zero Energy" frame risks a misconception; narration unverified |

## Result

- **APPROVED_EMBEDDED: 0** — no candidate passed the full content-verification bar (spoken narration unverified, and every named candidate either was wrong-chapter, off-scope terminology, or interactive-workbook format).
- **REJECTED: 10** — wrong chapter, off-scope/advanced/banned terminology, or non-demonstration format.
- **MEDIA_REVIEW_REQUIRED: 3** — `Stored_Energy.mp4`, `How_Scientists_Spot_Invisible_Energy.mp4`, `Why_Still_Objects_Secretly_Have_Energy.mp4`.

## Decision

**No video was embedded** into the PPTX, because only genuinely content-approved clips may be embedded and none met that bar. The three `MEDIA_REVIEW_REQUIRED` clips are provided as **standalone MP4 fallbacks** (copied into the candidate's `media/` folder, byte-identical to previously reviewed files) with explicit teacher caveats. This honors the directive's rule: *"If actual video content cannot be evaluated, classify the candidate MEDIA_REVIEW_REQUIRED rather than automatically embedding it."*

## Unblocking path

1. Provide a speech-transcription pass (or a human reviewer) on the three `MEDIA_REVIEW_REQUIRED` clips to confirm narration has no off-scope terminology.
2. Only then may `Stored_Energy.mp4` (and, if trimmed, the others) be promoted to `APPROVED_EMBEDDED` and embedded — and only into an already-safe slide without covering canonical content.
