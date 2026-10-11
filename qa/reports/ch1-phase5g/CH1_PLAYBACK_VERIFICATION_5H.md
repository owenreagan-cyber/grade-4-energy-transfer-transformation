# Chapter 1 — Playback Verification Results (Phase 5H)

## Status: **PLAYBACK_UNVERIFIED**

Genuine embedding is confirmed (package-integrity PASS), but actual **Microsoft PowerPoint playback
was not verified** — this environment has no Microsoft PowerPoint, and LibreOffice headless rendering
does not exercise embedded-video playback.

## What WAS verified (deterministic, package level)

| Check | Result | Evidence |
|---|---|---|
| MP4 physically inside the PPTX ZIP | PASS | `ppt/media/media1.mp4`, 21,733,498 bytes |
| MP4 decodes (not corrupt) | PASS | `ffprobe` duration 276.69 s |
| `video/mp4` content type declared | PASS | `[Content_Types].xml` |
| Slide 25 relationship → video | PASS | `slide25.xml.rels` `…/media/media1.mp4` |
| `p:videoFile` on slide 25 | PASS | `slide25.xml` |
| Poster frame (image) present + referenced | PASS | poster image in `ppt/media/`; blip in slide 25 |
| Click-to-play timing (no autoplay) | PASS | `<p:cond delay="indefinite"/>` — starts on click only |
| No auto-advance | PASS | no `<p:afterEffect>`/advance condition on the video node |
| Self-contained (no external path) | PASS | media part is inside the ZIP; no absolute path |
| Not byte-identical to no-video baseline | PASS | v6 SHA-256 differs from v4 |
| Exactly one MP4 packaged (no unused media) | PASS | only `media1.mp4` |

## What was NOT verified (honest gap)

| Check | Result | Reason |
|---|---|---|
| Video starts on teacher click in PowerPoint | UNVERIFIED | no PowerPoint available |
| Video plays in place / full-screen correctly | UNVERIFIED | no PowerPoint available |
| Audio plays | UNVERIFIED | no PowerPoint available |
| Playback completes / teacher can continue | UNVERIFIED | no PowerPoint available |
| Reopens without missing-media error | UNVERIFIED | no PowerPoint available |

## Environment limitation (documented)

- Host: macOS (darwin), LibreOffice 26.8.0.3 (headless) — renders slides and poster frames but does
  not validate PowerPoint video playback.
- The embedded MP4 is H.264 (High) + AAC 44.1 kHz mono, 1280×720@24 — the most portable combination
  for Microsoft PowerPoint (Windows + macOS).

## Conclusion

Embedding is **technically genuine and package-valid**, but the playback gate is **UNVERIFIED**, not
PASS. Per the phase directive, this yields `CH1_EMBEDDED_VIDEO_BUILT_UNCERTIFIED` — the only way to
upgrade to `PASS` is to open the PPTX in Microsoft PowerPoint (or a certified-compatible runtime) and
confirm click-to-play. That test requires a human on a PowerPoint-capable machine and is outside this
isolated/headless environment.
