# CH1 VIDEO INVENTORY

Phase 4 — Chapter 1 Complete Visual Asset Audit. All 18 intake media files under
`source-intake/2026-10-09-chapter-1/media/`.

Method: `ffprobe` (deterministic). SHA-256 from `SHA256SUMS.txt` (all verified `OK` in
`verification.log`). Content-level curriculum review is `[VISUAL/AUDIO]` (needs transcription;
flagged, not decided here).

## 1. Deterministic metadata

All 18 are **H.264 + AAC (mono, 44.1 kHz)**. No byte-identical duplicates (18 distinct SHA-256).

| # | File | Dur (s) | Size | Res | FPS | Orient | SHA-256 (short) |
|---|---|---|---|---|---|---|---|
| 1 | `Chapter_1_Review.mp4` | 436.9 | 35.7 MB | 1280×720 | 24 | L | `501b8e7e…` |
| 2 | `Chapter_1_Science_Notebook.mp4` | 505.9 | 44.3 MB | 1280×720 | 24 | L | `90266f21…` |
| 3 | `Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4` | 185.3 | 19.3 MB | 1280×720 | 30 | L | `ec61b59d…` |
| 4 | `Energy_Causes_Change__The_Energy_Detective.mp4` | 228.6 | 29.1 MB | 1280×720 | 30 | L | `21a29000…` |
| 5 | `Energy_Causes_Change.mp4` | 403.3 | 36.6 MB | 1280×720 | 24 | L | `514b4344…` |
| 6 | `Energy_Detective.mp4` | 347.9 | 27.0 MB | 1280×720 | 24 | L | `45fb8766…` |
| 7 | `Energy_Detectives_Briefing.mp4` | 472.6 | 45.1 MB | 1280×720 | 24 | L | `a018652d…` |
| 8 | `Energy_Detectives.mp4` | 437.4 | 40.5 MB | 1280×720 | 24 | L | `e341dec3…` |
| 9 | `How_Change_Proves_Energy_Exists.mp4` | 83.4 | 9.1 MB | 720×1280 | 30 | **P** | `8d0880d7…` |
| 10 | `How_Physical_Change_Proves_Energy_Exists.mp4` | 78.8 | 10.9 MB | 720×1280 | 30 | **P** | `0d00e203…` |
| 11 | `How_Scientists_Spot_Invisible_Energy.mp4` | 76.0 | 6.2 MB | 720×1280 | 30 | **P** | `3b47afea…` |
| 12 | `Stored_Energy.mp4` | 276.7 | 21.7 MB | 1280×720 | 24 | L | `38381321…` |
| 13 | `The_Energy_Detective-2.mp4` | 406.7 | 29.3 MB | 1280×720 | 24 | L | `647f1038…` |
| 14 | `The_Energy_Detective-3.mp4` | 332.1 | 31.6 MB | 1280×720 | 24 | L | `2bc2e5f2…` |
| 15 | `The_Energy_Detective-4.mp4` | 355.0 | 31.9 MB | 1280×720 | 24 | L | `1f0ab58a…` |
| 16 | `The_Energy_Detective.mp4` | 404.8 | 33.7 MB | 1280×720 | 24 | L | `4396afab…` |
| 17 | `The_Invisible_Boss_of_Change.mp4` | 170.3 | 23.0 MB | 1280×720 | 30 | L | `9636469c…` |
| 18 | `The_Unseen_Mover.mp4` | 326.8 | 25.9 MB | 1280×720 | 24 | L | `8e6a056b…` |

L = landscape 16:9 · P = portrait 9:16.

## 2. Clusters / near-duplicates (by name + duration)

- **"Energy Detective" cluster (8 files, highly redundant):** #4, #6, #7, #8, #13, #14, #15, #16.
  Durations 228–473 s. `[AUDIO]` These are very likely multiple edits of one concept video; at most
  one is needed (and only as optional review — never core-required).
- **"How … Proves Energy" shorts (3 files, portrait):** #9, #10, #11. Conceptually near-duplicate
  9:16 shorts. Titles use **"Proves"** → conflicts with Chapter 1 "evidence, not proof" language
  (see `CH1_SLIDESHOW_HANDOFF.md` §7: "Use 'evidence', never 'proof/proves/prove'").
- **Full-chapter / notebook:** #1 (`Review`), #2 (`Science_Notebook`), #5 (`Energy_Causes_Change`).
- **Stored energy:** #12.
- **"Invisible" concept:** #11, #17, #18.

## 3. Prior decision (authoritative)

`production/classroom-ready/week-2026-10-12/chapter-01/05_OPTIONAL_MEDIA/MEDIA_GUIDE.md`:

- **No video is required or recommended** for the classroom-ready sequence; use the **live electric
  pencil-sharpener demonstration**.
- `How_Scientists_Spot_Invisible_Energy.mp4` was already reviewed → **DO NOT USE** (misleading:
  "zero state", "null result", "verified proof", "all physical actions").

## 4. Chapter 1 appropriateness (structural)

| Verdict | Files | Reason |
|---|---|---|
| Rejected already | #11 | misleading proof/technical language (prior decision) |
| Drift risk | #9, #10 | "Proves" in title → evidence-language violation; portrait (not projector 16:9) |
| Drift risk | #17, #18 | "Invisible Boss"/"Unseen Mover" framing risks personifying energy |
| Candidate (optional only) | #3 | `Electric_Pencil_Sharpener` — the only on-topic demo video; verify it shows a **dull→sharp** change, no energy glow, no proof language |
| Candidate (optional review) | #6/#16 | single "Energy Detective" edit if it matches evidence-not-proof language |
| Candidate (optional) | #12 | `Stored_Energy` — verify no kinetic/potential terminology |

## 5. Best instructional use & hard rules

- **Do not make any video core-required.** All four media slots in the blueprint (slides 8, 16, 27, 32)
  must keep a live-demo / skip fallback (the canonical decision).
- Best single use, if any: slide 8 demo slot ← `Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4`
  **only after** a full curriculum-fidelity review (evidence-not-proof, Grade 4 scope, no energy glow).
- 9:16 portrait videos (#9, #10, #11) are not projector-appropriate and carry the "Proves" drift;
  recommend exclusion unless re-cut landscape and re-worded.
- Any future video approval must re-run the §4 checks; a video never becomes the sole delivery of
  required content.

## 6. `[VISUAL/AUDIO]` follow-up

Full content verification (transcription / frame review) of the 17 un-vetted files is a
**vision/audio-capable reviewer task** and is out of scope for this deterministic pass. The 8-file
"Energy Detective" redundancy should be resolved by that reviewer to a single approved edit.
