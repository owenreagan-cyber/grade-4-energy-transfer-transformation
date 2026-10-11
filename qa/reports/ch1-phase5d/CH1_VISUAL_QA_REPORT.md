# CH1 Visual QA Report (Phase 5D)

> Candidate `ch1-premium-hybrid-v3`. Rendered via `tools/render_slides_isolated.py` (font-faithful isolated LibreOffice profile). Deterministic checks via `tools/qa_slide_visual_v2.py` + `tools/qa_ch1_slides.py`.

## Deterministic rendered-layout QA v2

**Slides PASS/WARN/FAIL = 44 / 1 / 0.**

- The single per-slide WARN is the pre-existing `safe_margin` on slide 2's "BQ" mode chip (cosmetic, already documented in Phase 5C as non-blocking).
- Document-level `font_fidelity` WARN: the `→` (U+2192) glyph is drawn by a fallback font (LinuxLibertineGB) because neither Avenir Next nor Georgia contains it. This matches the Phase 5C baseline exactly; the arrow renders correctly. (The isolated render stages LucidaGrande for this glyph; LibreOffice still selected its internal fallback — cosmetic, non-blocking, and identical to v2.)

## Deterministic structural QA (28 gates)

**OVERALL: PASS.** Includes rendered geometry: 0 out-of-bounds, 0 overlapping-word pages, 0 empty pages.

## Coverage

All 45 slides rendered (PDF + 45 PNG previews + contact sheet). No slide was skipped.

## Remaining defects

1. **BLOCKED (visual, content-level):** pencil BEFORE photograph (slides 6, 8, 10, 36, 37) reads pointed, not dull — see `CH1_PENCIL_IMAGE_ROOT_CAUSE_AND_REPLACEMENT.md`. This is a *photographic-accuracy* defect that deterministic geometry QA cannot detect and that no existing asset resolves.
2. **VISUAL_REVIEW_REQUIRED:** projector-distance readability of slides 17, 19, 26, 44, 45 — see `CH1_PROJECTOR_READABILITY_REPORT.md`.

## Regressions vs Phase 5C (v2)

- Automated visual QA: v2 = 44/1/0; v3 = 44/1/0 — **no regression**.
- Structural QA: v2 OVERALL PASS; v3 OVERALL PASS — **no regression**.
- Parity: v3 text/notes identical to v2 — **no regression**.

## Visual-review limitations

- Deterministic QA (geometry, containment, occlusion, fonts, DPI) was performed and is fully passing.
- A **genuine human/independent visual inspection** of the rendered slides was **not** available in this environment beyond the builder's own view of the rendered PNGs. Per governance (`docs/standards` + the Phase 5D directive), a builder reviewing its own output is **not** a fully independent visual audit.
- The two original critical FAILs (slides 1, 4, 8 caption occlusion/overflow) remain fixed from Phase 5C (verified: no text-over-photo, no card-edge straddle, no containment FAILs).

## Final status

Automated visual QA **PASS** (0 FAIL); photographic-accuracy and projector-readability items require independent review. The candidate is **not** classroom-ready until the pencil asset is resolved and an independent whole-slide review is performed.
