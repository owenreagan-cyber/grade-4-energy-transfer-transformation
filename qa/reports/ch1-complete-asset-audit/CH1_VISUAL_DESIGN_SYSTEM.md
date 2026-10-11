# CH1 VISUAL DESIGN SYSTEM

Phase 4 — Chapter 1 Complete Visual Asset Audit. Consolidates the canonical design tokens with the
observed Codex-v5 implementation, and states the rebuild treatment for the hybrid.

## 1. Canonical tokens (frozen authority)

Source: `assets/visual-system/design-tokens.json` (`design_system_version = 1.0`, FROZEN),
`docs/standards/VISUAL_DESIGN_SYSTEM.md`, `docs/standards/SLIDESHOW_STANDARD.md`.

**Chapter 1 theme — Discovery / Evidence:**

| Token | Hex | Use |
|---|---|---|
| primary (Deep Navy) | `#1F2A5A` | titles, nodes, chrome |
| accent (Classic Gold) | `#A67C16` | arrows, reveals, section codes |
| surface (Warm Cream) | `#F5EEDC` | slide background |
| neutral (Muted Amber) | `#7A5620` | captions, secondary |
| Dark Media Navy | `#0E1428` | media shells, cinematic |
| Card Border | `#E4DAC4` | card outlines |

**Typography:** Avenir Next (fallback Helvetica Neue → Helvetica → Arial). Slide deck major 50 pt ·
title 42 pt · body 32 pt · label 28 pt (projector floor 28 pt). Vocab terms 48–68 pt.

**Observed in Codex v5:** Avenir Next (body/chrome) + Georgia (titles, 158 runs) — an accepted
deviation per the candidate's validation receipt (`approvedFamilies = ["Avenir Next","Georgia"]`).
The canonical frozen deck uses **Avenir Next only**. Decide: keep Georgia titles (premium serif,
matches blueprint "Georgia or similarly safe serif") or normalize to Avenir Next for exact parity.

**HUD set:** OBSERVE · WRITE · CHECK · TURN & TALK · PREDICT · RECITE · WATCH · VOTE · DRAW ·
EXPLAIN · TRACE · EVIDENCE. Notes badges: `BQ · V1 · V2 · N1 · N2 · N3 · N4`.

**Diagram style:** arrows = "model, not mechanism". `ENERGY → CHANGE → EVIDENCE` (N1) ·
`STORED ENERGY → RELEASE → CHANGE` (N3) · BEFORE/AFTER boxes (N4). Nodes = navy rounded rects,
gold arrows; the student N1 model keeps the last box empty until the check.

## 2. Photo/asset treatment (rebuild rule)

- Text, labels, arrows, models, badges, tables rendered **deterministically** in PPTX — never baked
  into raster. (Blueprint §6.4–6.8.)
- No visible "energy" (glow/aura/beams/particles); no cartoon mascots; no stock watermark look.
- Matched before/after pairs keep camera/scale/lighting stable.
- Generated artwork must be text-free, logo-free, watermark-free (OCR-verified across the Codex set).
- Only rejected raster on record: `slide-06-pencil-before.png` (no matched comparison).
- Grayscale-safe throughout (color never the only signal).

## 3. Recommended per-function visual treatment

| Function | Treatment |
|---|---|
| Chapter opener | full-bleed 16:9 hero, dark-left negative space for title, scrim if needed |
| Big Question | centered white card on cream; faint `ENERGY→CHANGE→?` at low opacity |
| Pencil phenomenon | matched BEFORE/AFTER composite (one asset, crop halves) |
| Energy/change vocab | two premium vocab cards (hero image + term + definition banner) |
| Five forms | one coordinated 5-panel strip for overview + per-form crops for the card row |
| Stored energy | rubber-band hero (stretched-still) on vocab card |
| Battery/rubber/apple | 3-panel coordinated strip, cropped per card |
| N1/N3 models | PPTX shape chains (navy nodes + gold arrows), never baked |
| N4 | two empty BEFORE/AFTER draw boxes + one gold arrow |
| WRITE/CHECK | identical geometry; CHECK reveals only the answer (gold emphasis) |
| Review | text-only 2×2 A/B/C/D cards; add raster only where the question is about an observable object (Q2 pencil, Q3 rubber band, Q6 battery) |
| Media shells | dark media navy 16:9 frame + gold border + skip fallback line |

## 4. Resolution / crop guidance

- Codex embedded set: 1448–2172 px wide (≥ projector-safe at 1080p for full-bleed and cards).
- Standalone intake images are generally **higher resolution** (1920×1080 / 1920×1234) and are the
  preferred substitutes where available (`[VISUAL]` director-graded).
- Panel set (1190–1650 px) is lower-resolution — alternates only, not first choice.
- Gemini rasters (1376×768) are below 1080p and non-editable — reference only.

## 5. Parity checks the hybrid must pass (post-build)

16:9 (13.333″×7.5″) · Avenir Next (or approved Avenir Next + Georgia) · body ≥ 28 pt · no clipped
text · no required text below projector floor · notes-mapped slides mirror the Guided Notes exactly ·
write slides leak no answer · no out-of-scope vocabulary · before/after truly matched · no baked
labels/watermarks · grayscale-safe · contact-sheet review with 0 blocking defects.
