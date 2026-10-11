# Chapter 1 — Full Render Visual QA (ch1-premium-hybrid-v2)

Render: `tools/render_slides_isolated.py` (LibreOffice 26.8.0.3 headless, isolated profile with staged fonts; exit 0;
PDF fresh; 45 pages = 45 slides). Embedded fonts: Avenir Next Regular/Bold/Italic, Georgia Bold, plus a LinuxLibertineGB
glyph fallback for "→" on slide 24.
Machine output: `CH1_VISUAL_QA_V2_FULL.json`, table `_visual_qa_v2_full.md`.

## Deterministic (DETERMINISTIC PASS)
- Rendered-layout QA v2: **44 PASS / 1 WARN / 0 FAIL** slides. WARNs: slide 2 "BQ" chrome chip 0.23in from the edge
  (inherited); document glyph fallback for "→".
- Old checker `qa_visual_pdf.py`: PASS. 28-gate canonical suite: PASS (includes rendered geometry and render page count).
- Image resolution: every placed photo ≥ 120 effective dpi (no WARN).
- Pixel diff vs v1: KEEP slides 0–2.1% (Georgia titles only); rebuilt slides 17–41%.

## Visual review (VISUAL PASS — builder-agent vision; NOT independent)
I reviewed the full contact sheet (`contact-sheet.png`) of the final build. I inspected these slides individually at full
resolution after their final change: 1, 4, 6, 8, 10, 14, 17, 19, 20, 23, 24, 25, 28, 29, 31, 33, 34, 36, 37, 42, 44, 45.
KEEP slides were reviewed on the contact sheet only; their layout is unchanged from 5B apart from the title face.

| Finding | Slides | Action |
|---|---|---|
| Apple cropped at the top | 24 | fixed (top-aligned crop) |
| CHANGES bullets broke awkwardly | 8 | fixed (wider column) |
| Sharpener / pencil tip cut by crop | 6 | fixed (frame aspect 1.65) |
| Centred caption with in-run LF rendered ragged | 17 | left-aligned; root cause logged (D4) |
| Pencil "BEFORE" tip not visibly flat | 6, 8 | owner decision D3 |
| Slide 4 statement wraps to 5 short lines in its 3in column | 4 | accepted (large, readable); cosmetic |
| Vocab card navy top rule is square while the card corners are rounded (frozen component, as in v1) | 10, 20 | cosmetic; unchanged |
| Opener slide number is low-contrast on navy | 1 | chrome; unchanged from v1 |

No text clipping, caption overflow, text-on-photo, or misalignment was found in the final render.

**Status:** DETERMINISTIC PASS · VISUAL PASS (builder-agent) · **independent visual review required** before visual
certification (AGENTS.md pipeline: internal specialist review + external audit).
