# Chapter 1 — Phase 5B Independent Visual Failure Register (Phase 5C)

Subject: `production/candidates/chapter-01/ch1-premium-hybrid-v1/` (Phase 5B, unchanged by this phase).
Machine-readable copy: `CH1_PHASE5B_VISUAL_FAILURE_REGISTER.json`.
Evidence: v1 previews + side-by-side comparisons in `comparisons/`. A font-faithful re-render of v1 with
`tools/render_slides_isolated.py` is pixel-identical to the 5B previews except the slide 24 "→" glyph (0.4%).

| ID | Slide | Severity | Observed | Confirmed mechanism | Old QA | New test on v1 | Status |
|---|---|---|---|---|---|---|---|
| F01 | 1 | CRITICAL | BQ "cut off" at "energy causin…" | **Not truncation.** The full sentence is in an 11.9in text box; a photo added *afterwards* at x = 9.6in paints over "causing change?" (z-order occlusion). | PASS | `occlusion` FAIL ("change?" 100% covered) | FIXED |
| F02 | 4 | CRITICAL | "light fills the room" overlaps photo/card; photos small | 28pt caption = 3.19in in a 3.125in × 0.50in box → 2 lines (needs 0.93in). Middle-anchored overflow paints up into the photo and down across the card edge. Photos letterboxed to 1.33 × 1.48in. | PASS | `text_containment`, `text_over_photo`, `card_edge_straddle` FAIL | FIXED |
| F03 | 8 | CRITICAL | AFTER caption overflows | Same constructor and mechanism as F02 ("humming" glyph core ends 5pt below its frame and crosses the card edge). | PASS | same three tests FAIL | FIXED |
| F04 | 15 | latent | — | 2-line instruction in a 0.5in frame | PASS | `text_containment` FAIL | FIXED |
| F05 | 24 | latent | — | body needs 1.87in in a 1.40in frame (still inside the gold card) | PASS | `text_containment` FAIL | FIXED |
| F06 | 25 | latent | — | prompt needs 2.00in in a 1.60in frame | PASS | `text_containment` FAIL | FIXED |
| F07 | 15→16 | minor | N1 sentence jumps on reveal | WRITE and CHECK place the sentence 0.15in / 0.40in apart | not tested | `paired_geometry` FAIL | FIXED |
| F08 | all | minor | Titles mix Avenir and Georgia | Spec says Georgia titles; v1 applied it only via `header()`, which most slides bypass | not tested | visible; pixel diff | FIXED |
| F09 | 6, 10, 14, 17, 20, 23–25, 28, 33, 34–45 | high | Undersized or absent photography; repetitive review | aspect-FIT letterboxing into leftover regions; no slot reserved for photos | not tested | visual review | FIXED (see matrix) |
| F10 | render env | high (process) | — | A fresh isolated LibreOffice profile launched from an agent shell renders Avenir/Georgia as Linux Libertine / Frank Ruhl | not tested | `font_fidelity` FAIL on the substituted render | FIXED (render tool) |

F01–F03 were reproduced from the v1 PPTX geometry and the PDF word boxes, and visually from the previews.
All three now PASS every test in the v2 candidate, and I confirmed the fix visually at full resolution.
