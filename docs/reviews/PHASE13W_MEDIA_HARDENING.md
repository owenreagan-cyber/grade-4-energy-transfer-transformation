# PHASE 13W — MEDIA HARDENING & PLACEMENT RECORD

> Narrow media-completion pass after the Phase 13V release freeze. No pacing, assessment, guided-note, science-scope, or brand changes. Release status preserved.

## Scope

Verified every accepted video is in the correct deck at the correct instructional moment, hardened video-slide speaker notes, confirmed poster frames and package relationships, and reconciled media documentation.

## Findings & Actions

### Media placement — PASS (no moves required)

All 5 embedded classroom cuts were verified against actual PPTX package structure (not prior notes):

| Video | Deck · Slide | Slide before → after | Placement |
|---|---|---|---|
| Ramp It Up | `03-ch3` S17 | Procedure → **WATCH** → Data table | Correct (investigation support) |
| Journey of Energy | `07-ch7` S13 | Notes Insert 1 → **WATCH** → Review Ch1 | Correct (synthesis recap) |
| Fossil Fuel Formation | `02-u2-ch2` S7 | How They Form → **WATCH** → Check Your Thinking | Correct (formation support) |
| Turbine & Generator | `03-u2-ch3` S7 | Electricity Pathway → **WATCH** → Benefits/Limitations | Correct (pathway support) |
| Wind & Hydro | `05-u2-ch5` S6 | Electricity Pathway → **WATCH** → Benefits/Limitations | Correct (wind support) |

Every slide sets up the concept before the video and uses/checks it after. No video is too late, redundant, or stranded. Runtime fits the 30-minute block. Role = SUPPORT for all 5.

### Speaker notes — ADDED

Added `ROLE / PLAY / PURPOSE / SKIP IF` notes to all 5 video slides (previously no notes slide). Student view unchanged (notes are teacher-only).

### Poster frames — PASS (no changes)

All 5 posters are 1280×720 (match video), sharp (edge-variance 1498–2863), and well-lit (mean 157–240). No mid-transition, blurry, dark, or title-card-clutter frames. Prior Phase 13U image audit already KEEP-classified these posters.

### WATCH slide standard — PASS

All 5 slides use the consistent premium pattern: `WATCH — <title>` + `Optional video · m:ss · Week X` + `WATCH` pill + one-line `THINK:` prompt. No file names, paths, or build notes on student view.

### Package relationship hardening — PASS

- No external media/video/image relationships in any deck (all packaged internal).
- Media MIME = `video/mp4`; poster = `image/jpeg`.
- No duplicate/orphaned media parts; no filename or relationship-ID collisions.
- Isolated-copy portability test passed (media persists outside the repo).

### Decode QA — PASS

All 5 embedded MP4s: H.264 + AAC, 1280×720@24, clean decode, no truncated tail, no missing audio, correct durations (2:29 / 2:49 / 3:39 / 3:41 / 1:35).

### Optional scripts — NO NEW BINARY

Searched `~/Downloads`, `~/Desktop`, `assets/supplemental/media/`, `production/media/`. No approved final binary for the 3 script-ready videos. The `Where_Does_Energy_Come_From_.mp4` / `Solar___Geothermal_Energy.mp4` present are the REJECTED raw sources (DO NOT USE). Status stays `PRODUCTION READY — OPTIONAL — NO BINARY`.

### Science regression & content boundary — PASS

No active (non-rejected-list) hits for forbidden science terms or climate/policy framing. The only occurrences are inside the DO-NOT-USE documentation, correctly explaining each rejection.

### Physical iPad — NOT REQUIRED

The only artifact change is teacher speaker notes, which do not render on slides. Rendered media slides are byte-identical; Phase 13T physical-device certification remains authoritative.

## Artifacts changed

- `production/slides/02-u2-ch2-slides.pptx` (speaker note)
- `production/slides/03-ch3-energy-speed-slides.pptx` (speaker note)
- `production/slides/03-u2-ch3-slides.pptx` (speaker note)
- `production/slides/05-u2-ch5-slides.pptx` (speaker note)
- `production/slides/07-ch7-edison-unit-synthesis-slides.pptx` (speaker note)
- `production/final-8.5-week/FINAL_VIDEO_INVENTORY.md` (created — authoritative media registry)
- `production/final-8.5-week/RELEASE_FREEZE.md` (updated — MEDIA_HARDENING record)

## Final decision

**MEDIA HARDENED — RELEASE READY**
