# Chapter 2 Video Audit & Selection Report (v6-media)

## Scope
Gate B evidence: inspect the actual clip metadata and (sampled) content, distinguish
approved material from unverified candidates, and record the embedding decision.

## Inventory (project-authored Chapter 2 media, `assets/supplemental/media/chapter-02/`)

| File | Runtime | Resolution | Codec | Audio | Orientation |
|---|---|---|---|---|---|
| Marble_Collisions__Investigating_Motion_Energy.mp4 | 5:59 | 1280×720 | H.264 | AAC (mono) | landscape |
| Ch_2__Motion_Energy_in_Action.mp4 | 6:21 | 1280×720 | H.264 | AAC (mono) | landscape |
| Things_on_the_Move.mp4 | 7:21 | 1280×720 | H.264 | AAC (mono) | landscape |
| Moving_Objects_Have_Energy.mp4 | 4:50 | 1280×720 | H.264 | AAC (mono) | landscape |
| How_Motion_Proves_Energy_Exists.mp4 | 1:12 | 720×1280 | H.264 | AAC (mono) | portrait |
| How_We_See_Invisible_Energy_of_Motion.mp4 | 1:03 | 720×1280 | H.264 | AAC (mono) | portrait |
| Chapter_2_Interactive_Notebook.mp4 | 6:42 | 1280×720 | H.264 | AAC (mono) | landscape |

All files are valid H.264+AAC MP4s (verified with `ffprobe`). They are the project's
own narrated explainer media (matching `curriculum/chapter-02/media/02-ch2-explainer-script.md`),
not silent raw demonstration footage.

## Selection

| Role | Subject | Source video | Derivative | Placement |
|---|---|---|---|---|
| VIDEO A (Highest) | Marble collision: one moving marble strikes a still target | Marble_Collisions__Investigating_Motion_Energy.mp4 | 0:00–0:40 (40 s) | Slide 6 (media shell) — EMBEDDED |
| VIDEO B (High) | A moving object causes an observable change | Ch_2__Motion_Energy_in_Action.mp4 | 0:00–0:40 (40 s) | Slide 15 (basketball application) — EMBEDDED |
| VIDEO C (Optional) | Pendulum / moving air (N3 useful motion) | Things_on_the_Move.mp4 | 0:00–0:40 (40 s) | STANDALONE FALLBACK (see note) |

## Bounded derivatives
Each clip is a 40 s bounded derivative (opening hook/observation segment) of a longer
project-authored explainer, re-encoded H.264 (libx264, crf 22) + AAC 128 kbps with
`+faststart`. Poster frames were extracted from within each clip. Full source videos
are retained as standalone fallbacks in `media/`.

## Verification status (honest)
- **Metadata:** VERIFIED (ffprobe: codec, resolution, runtime, audio stream).
- **Scientific fit:** The subjects (marble collision, moving object → change, moving
  pendulum/air) are all explicit Reader pp. 7–12 / TG Lesson 3 phenomena.
- **Frame-level visual + narration content:** assessed via sampled frames + titles +
  the project's own explainer script. **Full frame-by-frame and narration verification
  is NOT claimed** — it is a GOLD-gate task for independent visual review. The clips
  carry narration (not the "silent 15–30 s raw clip" ideal in the build brief); this is
  a documented deviation because the inventory contains no silent raw footage.

## Residual risk (flagged for external audit)
1. Clip boundaries target the opening hook; a title card or intro animation may occupy
   the first seconds. Teacher notes instruct playing after the live demo as an optional
   replay, so no instructional content is gated on the clip.
2. VIDEO C has no clean embed slot in the 49-slide layout (slide 23 is a dense 3-panel
   concept). It is provided standalone; re-embedding in a future revision is optional.
