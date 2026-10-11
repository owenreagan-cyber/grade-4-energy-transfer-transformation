# CH1 PREMIUM VISUAL SELECTIONS

Phase 5A. Every selected/eligible asset with provenance, SHA-256, dimensions, intended slide, crop,
text-safe area, lettering/watermark check, alternative, rationale, and verification state.

**Selection state convention:** `LOCKED` = deterministic rebuild (no raster) · `DEFAULT` = provisional
non-visual default (replaced if vision review picks an alternative) · `VISUAL_REVIEW_REQUIRED` =
subjective winner undecided. No subjective score is assigned in this environment.

## Selected raster assets (provisional defaults)

| ID | Source file | SHA-256 (short) | Dims | Canonical slide(s) | Crop | Lettering? | Alt | State |
|---|---|---|---|---|---|---|---|---|
| R01-opener | `assets/ch1/candidate-v2/slide-01-opener.png` | `9d491261…` | 1672×941 | 1 | full-bleed; title-safe left 42% | none | `candidate-a-lamp-lit…final.jpg` (1920×1080) | VISUAL_REVIEW_REQUIRED |
| R02-darkbright | `…/slide-04-dark-bright.png` | `f8cd572a…` | 1672×941 | 4, 5 | split halves for 5 | none | `ch1-dark-bright-01.jpg` (1920×1080) | VISUAL_REVIEW_REQUIRED |
| R03-pencil | `…/slide-09-pencil-before-after.png` | `920594e1…` | 1942×809 | 6, 8, 10(change), 36, 37 | crop before/after halves | none | `ch1-pencil-evidence-01.jpg` (1920×1234) | VISUAL_REVIEW_REQUIRED |
| R04-energy | `…/slide-10-energy.png` | `34288875…` | 1448×1086 | 10 (energy) | hero card 4:3 | none | `ch1-voc-energy-01-refined.jpg` (1918×1233) | VISUAL_REVIEW_REQUIRED |
| R05-change | reuse R03 (pencil pair) | `920594e1…` | 1942×809 | 10 (change) | landscape pair | none | `ch1-voc-change-01-refined.jpg` (1920×1234) | VISUAL_REVIEW_REQUIRED |
| R06-seashore | `…/slide-14-seashore.png` | `0ddcef14…` | 1672×941 | 14 | full-bleed; top text-safe | none | — | VISUAL_REVIEW_REQUIRED |
| R07-forms-strip | `…/slide-17-five-forms.png` | `a66f6048…` | 2172×724 | 17 | 5-panel strip | none | 7× `ch1-forms-*.jpg` (1440–1536) | VISUAL_REVIEW_REQUIRED |
| R08-stored | `…/slide-22-stored-energy.png` | `ee367676…` | 1448×1086 | 20, 38, 39 | hero 4:3 | none | `ch1-voc-stored-energy-01.jpg` (1920×1234) | VISUAL_REVIEW_REQUIRED |
| R09-stored-strip | `…/slide-25-stored-examples.png` | `f054ae25…` | 2172×724 | 23, 24, 25, 44 | crop per object | none | `ch1-stored-battery-01.jpg` · `ch1-stored-raised-apple-01.jpg` | VISUAL_REVIEW_REQUIRED |
| R10-evidence | `…/slide-28-evidence.png` | `c3778532…` | 1942×809 | 28 | 3-panel strip | none | `panel-07-change-cards.png` | VISUAL_REVIEW_REQUIRED |
| R11-reflection | `…/slide-33-reflection.png` | `2c47ce30…` | 1672×941 | 33 | subdued bg 20–30% | none | `slide-45-close.png` | VISUAL_REVIEW_REQUIRED |
| R12-close | `…/slide-45-close.png` | `60762733…` | 1672×941 | 45 | close still life | none | — | VISUAL_REVIEW_REQUIRED |

## Disqualified assets

| File | Reason |
|---|---|
| `science-chapter-opener.jpg` | baked title text |
| `slide-06-pencil-before.png` | single close-up, no matched pair |
| Gemini decks (5) | image-only, non-editable, <1080p |
| `How_Scientists_Spot_Invisible_Energy.mp4` | rejected (misleading "proof"/technical language) |
| `ch1-model-ece-01.jpg` (+ `(1)` dup) | text model should be PPTX shapes, not raster (use as reference only) |

## Crop rules (deterministic)

- Pencil pair → two halves for slides 6 (before) and 8 (full pair).
- Dark/bright → two halves for slide 5 notice/wonder crops.
- Five-forms strip → five equal crops for the per-form card row (slide 17 preview).
- Stored strip → three equal crops (battery / rubber band / apple) for 23/24/25 and 44.
- Evidence strip → three equal crops (light / pencil / motion).
- Apple standalone is portrait (1440×1920) → center-crop to 4:3 or 1:1 for the card.

## Text-safe areas

Every raster is text-free (OCR-verified). Editable text/labels are always placed on top by the
builder in the safe margins (0.45–0.55″ edge) — never baked. For full-bleed heroes (opener, seashore,
reflection, close) a navy scrim or gold rule is added only if contrast requires it.

## Confidence & verification state

- Deterministic metadata (hash, dims, text-free, editability): **high confidence**.
- Subjective fit (accuracy/composition/engagement/consistency/readability): **unset — vision review
  required**; no fabricated winner.
