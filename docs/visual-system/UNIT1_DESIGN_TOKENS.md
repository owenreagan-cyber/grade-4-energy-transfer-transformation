# UNIT 1 DESIGN TOKENS

> Authoritative machine-readable source: `assets/visual-system/design-tokens.json`.
> This document is the human-readable reference. If they disagree, the JSON governs.

## Version & freeze

- **`UNIT1_VISUAL_SYSTEM_VERSION = 1.0`** — stored in `design-tokens.json` (`design_system_version`, `status: FROZEN`). No competing version source.
- `design-tokens.json` is the single source of truth: **Figma mirrors it**, **exported SVGs mirror it**, and **DOCX/PPTX generators consume or reproduce it**.
- Any change requires: token update → `tools/build_visual_system.py` regen → `tools/qa_visual_system.py` all-PASS.
- **Component dimensions (canonical, frozen):** chapter tab 320×52 · vocabulary card 560×360 · BQ panel 96pt tall (full-width) · HUD bubble 240×64 · resource badge 260×44. These live in `design-tokens.json` (`components`) and are cross-checked against the Figma parity manifest and the generated SVGs.
- **Font substitution note:** canonical Avenir Next (local SVG/PDF); Figma pilot substitutes Inter (Avenir Next not bundled in Figma).

## Art direction

- **Target:** modern museum exhibit + excellent elementary science textbook + strong teacher presentation.
- **Avoid:** busy Canva-marketplace look, childish clip art, excessive gradients, heavy decorative frames, cramped textbook pages.
- **Principles:** every visual teaches; family resemblance + clear mode shifts; color is never the only signal; generous Grade 4 writing space; premium but restrained.

## Fonts

| Role | Value |
|---|---|
| Primary family | **Avenir Next** |
| Fallback | Helvetica Neue → Helvetica → Arial → sans-serif |
| Secondary / mono | none (single family, weight + size for hierarchy) |

## Type hierarchy

### Slide (16:9, 1280 × 720 pt)

| Level | Size | Weight |
|---|---|---|
| Deck major (unit title) | 50 pt | Bold |
| Slide title | 42 pt | Bold |
| Body | 32 pt | Regular |
| Label / diagram | 28 pt | DemiBold |
| **Projector floor** | **28 pt** | — |

Compact UI chrome (chapter tab, mode/resource badge, HUD pill) may sit below 28 pt — they are *signals*, not instructional content — but never below 14 pt.

### Handout (US Letter, 612 × 792 pt)

| Level | Size | Weight |
|---|---|---|
| Page title | 26 pt | Bold |
| Section header | 16 pt | Bold |
| Body | 14 pt | Regular |
| Caption / page ref | 11 pt | DemiBold |
| **Body floor** | **12 pt** (11 pt captions only) | — |

## Spacing, margins, grid

| Scale | xs 4 · sm 8 · md 12 · lg 16 · xl 24 · 2xl 32 · 3xl 48 (pt) |
|---|---|
| Slide margins | 40 pt sides · 32 top · 28 bottom (40 pt safe inset for overscan) |
| Handout margins | 54 pt sides · 48 top · 54 bottom (0.75") |
| Slide grid | 12 columns · 24 pt gutter |
| Handout grid | 8 columns · 18 pt gutter |

## Radius

| Element | Radius |
|---|---|
| Card / panel | 12 pt |
| Badge / pill / HUD / button | 999 (full round) |
| Image frame | 8 pt |

## Line weights

| Element | Weight |
|---|---|
| Hairline / rule | 0.75 pt |
| Panel border | 1.25 pt |
| Diagram arrow | 2.5 pt |
| Emphatic (BQ band bottom, tab underline) | 3 pt |
| Icon stroke | 2 pt |

## Icons

- 48 × 48 grid, viewBox `0 0 48 48`, 2 pt stroke, round caps/joins, single-color (`currentColor`).
- Filled state only for active status. Never mix outline and filled styles for the same meaning.

## Arrows (diagrams)

- **Transfer** — solid straight arrow, filled head, 2.5 pt, chapter accent.
- **Motion** — curved arrow, filled head, 2.5 pt, chapter accent.
- **Transformation** — arrow with a solid diamond marker at the midpoint (form change).
- **Cause/effect** — arrow with chevron, 2.5 pt, ink.
- Arrows are "model, not mechanism" — no compression-wave/electron detail.

## Callouts

- Left accent bar (3 pt, chapter accent) + surface fill + 12 pt radius + icon.
- Teacher callouts use a 3 pt `primary` bar and a convention tag (`LIVE` / `BACKUP` / `TIME` / `ASK` / `LISTEN-FOR` / `NEXT` / `IF-SHORT-ON-TIME`).

## Tables & charts

- **Tables:** shaded header row (10% `primary` tint) + bold ink header text + 1.5 pt `primary` rule under header; 0.75 pt row rules; min row height 0.5" (portrait) / 1.1" (landscape investigation).
- **Charts:** 2 pt axes, 1 pt ticks, data marks in chapter accent + ink, light grid that does not compete.

## Contrast (WCAG AA)

| Element | Floor |
|---|---|
| Body text | ≥ 4.5:1 |
| Large text (≥ 24 pt) | ≥ 3:1 |
| Primary (heading + band) | ≥ 4.5:1 vs white and vs surface |
| Accent (arrows / graphics) | ≥ 3:1 vs white and vs surface |
| Neutral (secondary text) | ≥ 4.5:1 vs surface |
| Projector target | ≥ 4.5:1 |

## Grayscale

- Color is never the only signal — use label text + shape + position.
- After desaturation, primary and accent stay ≥ 3:1 vs white; primary desaturates darker than accent.

## Chapter palettes

See `docs/visual-system/CHAPTER_THEME_MAP.md` (values live in the JSON `colors.chapters`).
