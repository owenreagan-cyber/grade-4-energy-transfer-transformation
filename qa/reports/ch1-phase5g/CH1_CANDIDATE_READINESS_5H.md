# Chapter 1 — Candidate Readiness Report (Phase 5H)

Build ID: **`ch1-premium-hybrid-v6-embedded-media`** · Date: 2026-10-10.

## Final classification: **CH1_EMBEDDED_VIDEO_BUILT_UNCERTIFIED**

Genuine embedding succeeded (package-integrity PASS, canonical instruction preserved), but actual
Microsoft PowerPoint playback is **UNVERIFIED** (no PowerPoint in this environment). This is the
exact outcome the phase directive anticipates for "video packaging succeeds but actual PowerPoint
playback is unverified."

## What was produced

| Deliverable | Path | Status |
|---|---|---|
| Editable 45-slide PPTX (embedded video) | `production/candidates/chapter-01/ch1-premium-hybrid-v6-embedded-media/01-ch1-energy-causes-change-premium-hybrid-v6-embedded-media.pptx` | built (38 MB) |
| PDF fallback | same dir `.pdf` | rendered (45 pp) |
| PNG previews (45) + contact sheet | same dir `previews/` + `contact-sheet.png` | rendered |
| Media manifest + hashes | `qa/reports/ch1-phase5g/CH1_MEDIA_MANIFEST_5H.json` | emitted |
| Video inventory (approve/reject) | `CH1_VIDEO_INVENTORY_5H.md` | emitted |
| Slide-to-video map | `CH1_SLIDE_TO_VIDEO_MAP_5H.md` | emitted |
| Video content + narration review | `CH1_VIDEO_NARRATION_REVIEW.md` (+ `transcripts/`) | emitted |
| Embedding/package integrity | `CH1_EMBEDDING_INTEGRITY.md` | PASS (11/11) |
| Playback verification | `CH1_PLAYBACK_VERIFICATION_5H.md` | UNVERIFIED |
| Pacing comparison | `CH1_PACING_5H.md` | unchanged |
| Instructional parity | `CH1_INSTRUCTIONAL_PARITY_5H.md` | PASS |
| Structural QA (28 gates) | `CH1_STRUCTURAL_QA_5H.md` | PASS |
| Visual/layout QA | `CH1_VISUAL_LAYOUT_QA_5H.md` | PASS (45/45) |
| Teacher media + fallback guide | `CH1_TEACHER_MEDIA_GUIDE_5H.md` | emitted |
| This readiness report | `CH1_CANDIDATE_READINESS_5H.md` | — |

## Gate summary

| Gate | Result |
|---|---|
| 45-slide sequence preserved (no new slides) | PASS |
| Student-facing text parity vs canonical (45/45) | PASS |
| Speaker notes: canonical text preserved (prefix) + delineated media block on slide 25 only | PASS |
| All 5 WRITE/CHECK pairs + review answers C·A·D·B·A·C | PASS |
| No answer leakage · no advanced vocabulary | PASS |
| Genuine MP4 embed (media part + rels + content type + poster + click-to-play) | PASS (11/11) |
| Poster frame renders in PDF fallback | PASS |
| No overlap with instructional elements (video vs 10 text shapes) | PASS |
| Narration content verification (all 19 videos) | COMPLETE (17 reject · 1 embed · 1 alternate) |
| Microsoft PowerPoint playback | **UNVERIFIED** |

## Why 17 of 19 videos are rejected

Full narration transcription (faster-whisper) revealed that the vast majority of the intake videos
carry off-scope or banned language — "proof/prove" (banned; project standard uses "evidence"),
"transfer"/"transforms" (Chapters 4/6 scope), "collision" (Ch.2/5), "wind turbine"/"grid" (Unit 2),
"electrical current"/"physical work"/"kinetic"/"potential"/"mechanical"/"radiant", or an
interactive-workbook format. Only `Stored_Energy.mp4` (landscape) and
`Why_Still_Objects_Secretly_Have_Energy.mp4` (portrait) are clean. The former is embedded; the latter
is kept as an un-embedded alternate (portrait + it answers the slide-23 prediction).

## Repository protection

- Frozen canonical deck, Guided Notes, teacher key, and releases: **unchanged** (not touched).
- Baseline v4 candidate: **unchanged** (byte-identical to v5; v6 is a separate new candidate).
- v1/v2/v3/v5 candidates: unchanged.
- Nothing staged, committed, pushed, frozen, or promoted.
- Headless rendering only; the pre-existing LibreOffice process was not disturbed.

## Path to `CH1_EMBEDDED_VIDEO_PASS`

Open the v6 PPTX in Microsoft PowerPoint (or a certified-compatible runtime) on a real machine and
confirm: (1) the slide-25 video starts on click, (2) audio plays, (3) it stays on slide 25, (4) the
teacher can advance, (5) the file reopens with no missing-media error. Record that evidence to
upgrade this candidate from `BUILT_UNCERTIFIED` to `PASS`. Gold/production certification additionally
requires the external adversarial audit, reproducible-build attestation, and release acceptance.
