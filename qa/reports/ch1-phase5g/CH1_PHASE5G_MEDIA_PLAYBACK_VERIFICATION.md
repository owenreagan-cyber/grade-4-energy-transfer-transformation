# Chapter 1 — Media Playback Verification Report (Phase 5G)

> Honest record: **no video is embedded in the candidate PPTX**, so there is no embedded-playback claim to verify. The deck is byte-identical to the accepted `ch1-premium-hybrid-v4` (SHA-256 `1f85244f…`).

## What was verified

| Check | Result |
|---|---|
| Candidate videos exist and are decodable (h264 video + AAC audio) | PASS (ffprobe on all candidates) |
| Representative frames extract cleanly | PASS (ffmpeg frame extraction) |
| On-screen language sampled via OCR | PASS (tesseract) |
| Spoken-narration transcription | **NOT PERFORMED** — no speech-to-text tool available |
| Embedded MP4 media relationships | N/A — nothing embedded |
| Slide placement of video objects | N/A — nothing embedded |
| Poster frames / autoplay flags | N/A — nothing embedded |
| PowerPoint playback of an embedded clip | **PLAYBACK_UNVERIFIED** — nothing to play (no embed) |

## Playback status

`PLAYBACK_UNVERIFIED` (no embedded video exists to play). The three standalone MP4 fallbacks are the previously reviewed, byte-identical files (SHA-256 matches `MEDIA_ASSET_MANIFEST.md`): `Stored_Energy.mp4` (`38381321…`), `How_Scientists_Spot_Invisible_Energy.mp4` (`3b47afea…`), `Why_Still_Objects_Secretly_Have_Energy.mp4` (`915d7389…`).

## Why this is the correct outcome

The phase directive requires that only *genuinely content-approved* clips be embedded, that actual narration be inspected before approval, and that a static thumbnail never be treated as proof of playability. The content audit found the named candidates to be wrong-chapter / off-scope / interactive-workbook format, and no transcription tool was available to verify narration of the rest. Embedding unverified media would risk a science-accuracy defect — the #1 locked priority. Therefore: **no embedding**, standalone fallbacks only.

## Unblocking embedded playback

1. Independent narration transcription (or human review) of the three fallback clips.
2. On approval, embed only `Stored_Energy.mp4` (and trimmed shorts) via `python-pptx` `add_movie()` (present in v1.0.2, experimental) into a slide region that does not cover canonical text, with a poster frame and teacher-controlled (no-autoplay) timing.
3. Re-run media-specific QA (relationships, geometry, poster, decodability, no autoplay, no collision) plus full parity/structural/visual QA.
