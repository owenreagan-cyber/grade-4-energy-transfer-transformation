# CH1 COMPLETE ASSET INVENTORY

Phase 4 — Chapter 1 Complete Visual Asset Audit (investigation only).
Date: 2026-10-09. Scope: every reusable asset for the definitive Chapter 1 visual library.
Provenance preserved; **no original file was modified, rebuilt, or promoted.**

Method: deterministic PPTX/PDF text extraction, ZIP media forensics, SHA-256, Pillow dimension
inspection, `ffprobe` (video), `tesseract` OCR (to detect baked-in text), and contact-sheet
rendering. Visual *content* judgments are flagged `[VISUAL]` where they require director sign-off.

---

## 1. Canonical (frozen) deck — the authority for content/sequence

| Field | Value |
|---|---|
| File | `production/slides/01-ch1-energy-causes-change-slides.pptx` (172 KB) + `.pdf` (817 KB) |
| Version | `UNIT1_CH1_GOLD_STANDARD_VERSION = 1.1` — **FROZEN** (2026-10-05) |
| Slides | 45 (16:9, 13.333″ × 7.5″) |
| Fonts | Avenir Next (539 text runs) — single family |
| Embedded images | **0** — every visual is a programmatic PPTX shape/diagram |
| Release SHA-256 (PPTX) | `5278f96c7dfab4f4b6809a3677f714c566c212e7c74af3d03f502abb77f022f7` |

Implication: the frozen deck has **no raster artwork**; it is the text/sequence/model source.
The hybrid rebuild supplies raster visuals *around* this deck's exact content.

---

## 2. Codex visual candidates (v2 → v5)

All four use the **same 45-slide blueprint architecture** (see `CH1_SOURCE_DECK_COMPARISON.md`).

| Deck | Slides | Embedded media | Notes |
|---|---|---|---|
| `…-visual-candidate-v5.pptx` (51 MB) | 45 | 29 PNG entries → **11 unique** | current candidate |
| `…-visual-candidate-v4.pptx` | 45 | 29 → 11 unique (identical hashes) | superseded |
| `…-visual-candidate-v3.pptx` | 45 | 29 → 11 unique (identical hashes) | superseded |
| `…-visual-candidate-v2.pptx` | 45 | 29 entries, **0 bytes** (placeholders) | pre-embed build; no artwork to recover |

v3/v4/v5 embed byte-identical artwork → **no additional artwork exists in v2/v3/v4 beyond v5's set.**

Fonts: Avenir Next (902) + Georgia (158, titles).

### 2.1 Unique embedded images (the "candidate-v2" generation set)

Source dir: `assets/ch1/candidate-v2/`. Manifest: `assets/ch1/candidate-v2/IMAGE_GENERATION_MANIFEST.md`.
All text-free (OCR-confirmed), no watermarks, no logos.

| Asset | Dims | SHA-256 (short) | Used on v5 slide(s) | Purpose |
|---|---|---|---|---|
| `slide-01-opener.png` | 1672×941 | `9d491261…` | 1 | chapter opener (lamp/desk) |
| `slide-04-dark-bright.png` | 1672×941 | `f8cd572a…` | 4, 5 (×2 crops) | matched dark→bright |
| `slide-09-pencil-before-after.png` | 1942×809 | `920594e1…` | 6, 9, 11, 36, 37 | matched pencil before/after |
| `slide-10-energy.png` | 1448×1086 | `34288875…` | 10 | energy vocab (toy car) |
| `slide-14-seashore.png` | 1672×941 | `0ddcef14…` | 14 | seashore reader bridge |
| `slide-17-five-forms.png` | 2172×724 | `a66f6048…` | 17, 19 (×5 crops) | 5-panel forms strip |
| `slide-22-stored-energy.png` | 1448×1086 | `ee367676…` | 22, 38, 39 | rubber-band stored energy |
| `slide-25-stored-examples.png` | 2172×724 | `f054ae25…` | 25 (×3 crops), 44 | 3-panel battery/rubber/apple |
| `slide-28-evidence.png` | 1942×809 | `c3778532…` | 28 (×3 crops) | 3-panel evidence strip |
| `slide-33-reflection.png` | 1672×941 | `2c47ce30…` | 33 | BQ reflection background |
| `slide-45-close.png` | 1672×941 | `60762733…` | 45 | chapter-close still life |
| `slide-06-pencil-before.png` | 1536×1024 | `5d78ecfb…` | **none (rejected)** | single close-up — rejected for lacking matched comparison |

Note: v5 stores the 3-panel/5-panel strips once and crops per card (efficient; single source of truth per strip).

---

## 3. Gemini intake decks (5 PPTX/PDF pairs)

Dir: `source-intake/2026-10-09-chapter-1/slideshows/gemini/`.

**Deterministic finding:** every Gemini slide is a **full-slide baked raster** (1376×768 PNG).
No `<a:t>` text runs exist in any deck; `pdftotext` and `tesseract` (default + autocontrast + psm 11)
return **zero text**. These are **image-only, non-editable** decks — usable only as visual
reference/photograph sources, never as editable slide masters.

| Deck | Slides | Physical size | Media | Resolution |
|---|---|---|---|---|
| `Energy_Causes_Change` | 10 | 17.778″ × 10″ (16:9) | 10 PNG | 1376×768 |
| `Energy_Causes_Change-2` | 16 | 17.778″ × 10″ | 16 PNG | 1376×768 |
| `Energy_Causes_Change-3` | 15 | 17.778″ × 10″ | 15 PNG | 1376×768 |
| `Forms_of_Energy` | 11 | 17.778″ × 10″ | 11 PNG | 1376×768 |
| `Forms_of_Energy-2` | 11 | 17.778″ × 10″ | 11 PNG | 1376×768 |

`Forms_of_Energy` and `Forms_of_Energy-2` are treated as **two independent creative alternatives
for Session 2** (not a before/after sequence). All images warm-cream toned (avg RGB ≈ 222,217,199)
with full black/white range → light slide aesthetics, `[VISUAL]` content enumeration pending.

---

## 4. Standalone intake images (highest-resolution candidates)

Dir: `source-intake/2026-10-09-chapter-1/images/` — 20 files, 19 unique (`ch1-model-ece-01.jpg`
≡ `ch1-model-ece-01 (1).jpg`, identical SHA `de5c900c…`). All text-free except
`science-chapter-opener.jpg` (baked "Grade 4 Elementary Science Chapter Opener" title → watermark risk).

| File | Dims | Purpose (from filename) |
|---|---|---|
| `candidate-a-clean-chapter-opener-v2.jpg` | 1920×1080 | chapter opener A |
| `candidate-a-lamp-lit-chapter-opener-final.jpg` | 1920×1080 | chapter opener A "final" |
| `science-chapter-opener.jpg` | 1920×1088 | opener (baked title — reject as-is) |
| `ch1-dark-bright-01.jpg` | 1920×1080 | dark→bright |
| `ch1-forms-motion-01.jpg`, `…-03.jpg` | 1440×1080 | motion (2 alts) |
| `ch1-forms-light-01.jpg`, `…-02.jpg` | 1536×1152 | light (2 alts) |
| `ch1-forms-heat-01.jpg` | 1440×1080 | heat |
| `ch1-forms-sound-02.jpg` | 1536×1152 | sound |
| `ch1-forms-electrical-01.jpg` | 1440×1080 | electrical |
| `ch1-model-ece-01.jpg` | 1920×1080 | ENERGY→CHANGE→EVIDENCE model (concept) |
| `ch1-pencil-evidence-01.jpg` | 1920×1234 | pencil evidence |
| `ch1-voc-energy-01.jpg`, `…-refined.jpg` | ~1918×1233 | energy vocab (2 alts) |
| `ch1-voc-change-01-refined.jpg` | 1920×1234 | change vocab |
| `ch1-voc-stored-energy-01.jpg` | 1920×1234 | stored-energy vocab |
| `ch1-stored-battery-01.jpg` | 1920×1440 | battery stored |
| `ch1-stored-raised-apple-01.jpg` | 1440×1920 (portrait) | raised apple |

These are generally **higher resolution** than the Codex embedded set (e.g., 1920×1080 openers vs
1672×941; 1920×1234 vocab cards vs 1448×1086). They are candidate *replacements* or *alternates*.

---

## 5. Legacy "panel" asset set (not embedded in any current deck)

Dir: `assets/ch1/` — 12 PNGs, an earlier storyboard generation (text-free per OCR).

| File | Dims |
|---|---|
| `panel-01-bedroom-light.png` | 1650×795 |
| `panel-02-single-bulb.png` | 1190×795 |
| `panel-03-candle-change.png` | 1340×795 |
| `panel-04-flashlight-cut.png` | 1307×577 |
| `panel-05-rubber-band.png` | 1400×577 |
| `panel-06-apple-drop.png` | 1472×577 |
| `panel-07-change-cards.png` | 1190×515 |
| `panel-08-forms-of-energy.png` | 1635×515 |
| `panel-09-blank-model-chain.png` | 1355×515 |
| `panel-10-living-room.png` | 1370×465 |
| `panel-11-three-stored.png` | 1470×465 |
| `panel-12-diurnal-energy.png` | 1340×465 |

`[VISUAL]` Not referenced by any slide; retained as available alternate artwork (e.g., `panel-08
forms-of-energy`, `panel-11-three-stored` may be recoverable alternates to the Codex strips).

---

## 6. Other relevant files

- `assets/Cinematic Energy Concepts Storyboard (1).png` (2.0 MB) — untracked storyboard reference.
- `assets/supplemental/presentations/Energy - Lesson 1..11.pptx` — external (non-authoritative) decks.
- `assets/authoritative/student-reader/chapters/Chapter_1_Energy_Causes_Change.pdf` — curriculum source (read-only).

---

## 7. Machine-readable manifest

Companion: `CH1_ASSET_MANIFEST.json` (same directory) — full SHA-256, dims, and per-deck media maps.
