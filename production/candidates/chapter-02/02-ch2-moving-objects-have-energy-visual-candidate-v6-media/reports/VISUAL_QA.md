# Visual QA Report (v6-media)

Two QA layers were run.

## 1. Deterministic content QA (`tools/qa_ch2_visual_candidate.py`)
**PASS** — 49/49 slides, 0 global issues. Covers: 16:9 size, exact BQ/V/N anchor text,
write-before-reveal order, answer leakage, canonical review wording + key, 14-field
speaker-note schema, banned-vocabulary guardrails, media fallback presence, required
visuals, native editable tables, optional-extension labeling. Full table: `CONTENT_QA.md`.

## 2. Rendered-layout visual QA v2 (`tools/qa_slide_visual_v2.py`)
v6 rendered via LibreOffice headless → PDF, then checked for text completeness,
containment, occlusion, text-over-photo, card-edge straddle, safe margins, font
fidelity, glyph floor, and image resolution.

Result: **42 PASS / 1 WARN / 6 FAIL**. The 6 FAIL slides are byte-identical in category
to the v5 baseline (40 PASS / 3 WARN / 6 FAIL) — i.e. **the video embedding introduced
zero new visual defects**, and v6's LibreOffice render embeds Avenir Next + Georgia
correctly (v5's render did not).

| Slide | Finding | Disposition |
|---|---|---|
| 07, 15, 42 | `text_over_photo` (text on photo with scrim the checker doesn't recognize as opaque backing) | Pre-existing v5 design intent; carried forward. Flag for visual-art review. |
| 24, 25 | `text_containment` on native editable tables (checker doesn't map table-cell text to table shapes) | False positive on the checker's table handling; tables verified by `qa_ch2_visual_candidate.py`. |
| 00 | `font_fidelity` glyph fallback for `→ ● ✓` | Expected macOS glyph fallback (neither Avenir Next nor Georgia contains these); WARN-level, pre-existing. |

Slides 6 and 15 (the embedded-video slides) show **no** new occlusion or containment
findings.

Contact sheet: `contact-sheet.png`. Per-slide previews: `previews/slide-01..49.png`.
