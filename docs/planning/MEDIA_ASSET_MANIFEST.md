# MEDIA ASSET MANIFEST

> Supplemental/generated media intake record (2026-09-27). These videos are **SUPPLEMENTAL / REVIEW / GENERATED MEDIA** — NOT authoritative CKSci, NOT canonical Reader/TG, NOT official Activity Pages. Terminology here never overrides the locked curriculum.

## Local-asset policy (videos remain UNTRACKED)
- The 9 MP4s total **~250 MB**, far exceeding normal Git expectations for this repo (the tracked authoritative set is ~23 MB).
- Per `docs/technical/BINARY_ASSET_POLICY.md`, `assets/supplemental/` is already git-ignored. Videos are copied there **on disk only**; they are **not** committed to Git.
- The single source of truth for video metadata (hashes, sizes, review status) is **this manifest** (tracked).
- Final day/slide placement stays **PENDING** until chapter/unit media libraries are complete.
- **No Git LFS** (not justified — the repo does not track these binaries at all).
- **No MP4 is embedded in any PPTX.** Future staging references the single `assets/supplemental/media/` location.
- Originals remain in `~/Downloads` untouched; repo copies are byte-for-byte (SHA-256 verified).

## Status vocabulary
- **MEDIA REVIEW:** `REVIEWED` · `NEEDS REVIEW` · `MAJOR FAIL`
- **CURRICULUM:** `KEEP` · `KEEP WITH NOTES` · `DO NOT USE`
- **STAGING:** `UNSTAGED` · `CANDIDATE` · `STAGED`

## CHAPTER 1 — Video Library

| File | Working title | Role | Format | Duration | Resolution | Size (bytes) | SHA-256 | Review | Curriculum | Staging | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `The_Invisible_Boss_of_Change.mp4` | The Invisible Boss of Change | Chapter-opening cinematic / mystery hook | MP4 (h264+aac) | 2:50 | 1280×720 | 23,019,061 | `9636469cbd32fcf174acb502c58bf7d568bcaadaa816b01e16e4127dc9fc4b91` | REVIEWED | KEEP WITH NOTES | UNSTAGED | Visually strong; some terminology may extend beyond Ch.1. Regenerate only on MAJOR fail. |
| `The_Energy_Detective.mp4` | The Energy Detective | Core Ch.1 concept explainer (VIDEO #2, NOT the lab briefing) | MP4 (h264+aac) | 6:45 | 1280×720 | 33,677,981 | `4396afabfe42127b4e3fd83298ad38188a2857f8582e38d5b8216e3d52309403` | REVIEWED | KEEP | UNSTAGED | How scientists infer energy through observable change/evidence. |
| `Stored_Energy.mp4` | Stored Energy | Stored-energy concept explainer | MP4 (h264+aac) | 4:37 | 1280×720 | 21,733,498 | `38381321a79e16ae602d1b9f16c5bab7975aea75d6560926a727052a9e78e674` | REVIEWED | KEEP WITH NOTES | UNSTAGED | Minor wording issues; not a regenerate trigger. |
| `Energy_Detectives_Briefing.mp4` | Energy Detectives Briefing | Pre-lab briefing / Energy Scavenger Hunt support | MP4 (h264+aac) | 7:53 | 1280×720 | 45,073,636 | `a018652d4262fd37d520dde8768a85fc5a19b27b858371ccee29906c00b4d028` | REVIEWED | KEEP | UNSTAGED | Longer than ideal; cost of regeneration not justified absent major fail. |
| `Chapter_1_Science_Notebook.mp4` | Chapter 1 Science Notebook | Notebook support / student walkthrough | MP4 (h264+aac) | 8:26 | 1280×720 | 44,257,292 | `90266f21fc1ab475713355c3413a82535521546913eca9a9258b5d4daeeac65a` | REVIEWED | KEEP | UNSTAGED | — |
| `How_Scientists_Spot_Invisible_Energy.mp4` | How Scientists Spot Invisible Energy | Short retrieval / ENERGY → CHANGE → EVIDENCE | MP4 (h264+aac) | 1:16 | 720×1280 (vertical) | 6,183,642 | `3b47afea3aaee36aba05dd276cec9c211242924c789be067bc518f43bccba914` | REVIEWED | KEEP | UNSTAGED | Short / vertical. |
| `Why_Still_Objects_Secretly_Have_Energy.mp4` | Why Still Objects Secretly Have Energy | Stored-energy retrieval short | MP4 (h264+aac) | 1:16 | 720×1280 (vertical) | 10,426,210 | `915d7389526bc6195d8aa89f33253a076dc9d467297864b39c1f78f23bc66821` | REVIEWED | KEEP | UNSTAGED | Short / vertical. |
| `Chapter_1_Review.mp4` | Chapter 1 Review | End-of-chapter review / quiz prep | MP4 (h264+aac) | 7:17 | 1280×720 | 35,702,141 | `501b8e7e3450e9d664d827fd0c73bfc5b860044e21ee32212fcb22cb684dc8ef` | REVIEWED | KEEP | UNSTAGED | — |

## CHAPTER 2 — Video Library

| File | Working title | Role | Format | Duration | Resolution | Size (bytes) | SHA-256 | Review | Curriculum | Staging | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `Things_on_the_Move.mp4` | Things on the Move | Ch.2 opening/core explainer | MP4 (h264+aac) | 7:21 | 1280×720 | 41,874,205 | `708483c50ad0c940ac5bb6965ca4406200cd901eb9a77c5231228e0f047951aa` | REVIEWED | KEEP | UNSTAGED | Fits Ch.2 "Moving Objects Have Energy" (NOT Ch.1). Long-form explainer, not a quick hook. |

## SUPPLEMENTAL PDFs (review assets)

| File | Class | Repo path | Size (bytes) | SHA-256 |
|---|---|---|---|---|
| `chapter-reading-worksheet-assessments.pdf` | SUPPLEMENTAL / REVIEW | `assets/supplemental/review/assessments/` | 32,095 | `18ea86ed0e1dd6555e6b8b5bd462fa64c8377180c618f05eb3ce07ef96e7e558` |
| `ch1-interactive-notebook-packet.pdf` | SUPPLEMENTAL / REVIEW | `assets/supplemental/review/notebooks/` | 14,872 | `44a9c99464d0ce4defbbc11170a4bc3d43680d3c7633f7725ea98e24be769490` |
| `Energy_Detectives.pptx` | SUPPLEMENTAL / REVIEW / CHAPTER 1 / SLIDESHOW | `assets/supplemental/review/slides/` | 25,756,291 | `75ece737c2c4c1f32898f14ddf42d100131a321b04012da8c9e65f13c10e179c` |

> Review decisions for the PDFs live in `docs/reviews/SUPPLEMENTAL_READING_ASSESSMENTS_REVIEW.md` and `docs/reviews/CH1_SUPPLEMENTAL_NOTEBOOK_PACKET_REVIEW.md`. The slideshow review lives in `docs/reviews/CH1_SUPPLEMENTAL_SLIDESHOW_REVIEW.md`.

## SUPPLEMENTAL SLIDESHOW (review asset, 2026-09-27)

| File | Chapter | Class | Status | Slide count | Size (bytes) | SHA-256 |
|---|---|---|---|---|---|---|
| `Energy_Detectives.pptx` | 1 — Energy Causes Change | SUPPLEMENTAL / REVIEW / SLIDESHOW | KEEP AS SUPPLEMENTAL · NOT AUTHORITATIVE · NOT CURRENT RELEASE DECK · NOT STAGED | 15 | 25,756,291 | `75ece737c2c4c1f32898f14ddf42d100131a321b04012da8c9e65f13c10e179c` |

- **Role:** visual reference / supplemental presentation / possible design inspiration.
- **Source path:** `~/Downloads/Energy_Detectives.pptx` (original left untouched).
- **Repo path:** `assets/supplemental/review/slides/Energy_Detectives.pptx` (git-ignored on disk per `BINARY_ASSET_POLICY.md`; ~24.6 MiB).
- No macros/VBA; no broken media references; opens cleanly (15 slides, 16:9, 15 embedded PNGs).

## MAJOR FAIL standard (regeneration threshold)
Reject an existing video **only** for a MAJOR failure: scientifically false central concept · directly contradicts the unit standard · serious safety instruction · teaches a curriculum-harming misconception · corrupted/unplayable file · inappropriate student-facing content.

**NOT** major fails (record as NOTES, do NOT regenerate): longer than ideal · minor vocabulary leakage · slightly early terminology · stylistic preference · redundant example · minor wording the teacher can contextualize · imperfect pacing.

## Current verdict
- All 9 videos: **REVIEWED** (technical + sampled-frame), all **KEEP** (2 = KEEP WITH NOTES), all **UNSTAGED**. No MAJOR FAIL. No regeneration requested.
- Placement: PENDING (awaiting complete chapter/unit media libraries).
