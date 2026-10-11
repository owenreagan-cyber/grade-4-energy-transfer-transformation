# Chapter 1 — Why Phase 5B Visual QA Missed Visible Defects (Root-Cause Analysis)

Every root cause below was confirmed by reproduction. Hypotheses I could not prove are listed separately at the end.

## RC-1 — Text regions were fixed numbers, never derived from their text (F02, F03, F04–F07)
- **Symptom:** captions and prompts spill out of their boxes.
- **Reproduction:** `before_after_photo()` puts the hint at `y + h − 0.6` with `h = 0.5`. "light fills the room" at 28pt
  measures 3.19in against a 3.125in box (Pillow, real Avenir Next metrics), so it wraps to 2 lines that need 0.93in. The
  render shows the words at y 316–373pt against a frame of 324–360pt.
- **Code:** `tools/build_ch1_premium_slides.py::before_after_photo` (and fixed heights on slides 15, 24, 25).
- **Why old QA passed:** nothing compared the text's needed height with its box.
- **Correction:** `tools/slide_layout_kit.py` (`need_h`, `wrap`, `check_fit`). The v2 builder's `text()`, `rich()`,
  `model_strip()` and chips call `check_fit` and raise `FitError` at build time. The guard caught 5 real
  overflows during this phase (slide 1 column, slide 10 card, slide 33 BQ, review 3 grid, review 6 list) before any render.
- **Calibration:** run over every v1 text box, it predicts exactly the rendered overflows (4, 8, 15, 24, 25) and leans
  conservative elsewhere.

## RC-2 — Photos were added after full-width text, with no reserved region (F01)
- **Reproduction:** slide 1 `text(s, 0.9, 3.25, 11.9, …BQ…)`, then `_pic_fit(s, opener, 9.6, 1.0, 3.3, 4.6)`.
  The picture's spTree index is higher, so it paints over the words. `pdftotext` still extracts "causing change?".
- **Why old QA passed:** text parity reads the PPTX; geometry QA compared words only with the page and with other
  words; `overflow_shapes` compared shapes only with the slide.
- **Correction:** the opener reserves two disjoint regions and draws the photo first. The new `occlusion` test fails any word
  covered by a picture that sits above the word's owning shape.

## RC-3 — The QA measured existence, not visibility (all critical failures)
`qa_render_geometry.check` flags only (a) words outside the page and (b) word-vs-word overlap above 30%. It never asks which
shape *owns* a word or what is painted near it. A caption that crosses a photo or a card edge overlaps no other word and stays
inside the page, so it is invisible to this check. Text parity likewise proves the PPTX holds the words, not that students can see them.
- **Correction:** `tools/qa_slide_visual_v2.py` relates every rendered word (PDF bbox, trimmed to its glyph core) to its owning
  PPTX shape (by token and position) and to every picture and filled card, in z-order: containment, occlusion,
  text-over-photo-without-backing, card-edge straddle, paired geometry, font fidelity, rendered size, image DPI, and pixel diff.

## RC-4 — Photos were aspect-FIT into leftover space (F02, F09)
`_pic_fit` letterboxes into whatever rectangle remained, so photos ended up 1.3–4.4in wide with uneven bands. The new kit's
`cover()` crops each source to the exact region aspect around a focus point. `before_after_compare` gives matched photos
identical sizes.

## RC-5 — python-pptx text boxes default to `spAutoFit`
Every v1 text box carries `<a:spAutoFit/>`, so renderers may grow the box past its declared height. The "0.5in caption region"
was never a real limit. v2 sets `MSO_AUTO_SIZE.NONE`; declared, measured boxes are authoritative.

## RC-6 — The render environment silently substitutes fonts (process risk, found this phase)
A fresh `-env:UserInstallation` profile launched from this agent shell (sandboxed or not, in /tmp or $TMPDIR) did not
enumerate macOS system fonts. `pdffonts` showed Linux Libertine / Frank Ruhl Hofshi, with no Avenir or Georgia. Any QA run on
such a render would measure the wrong glyphs. **Correction:** `tools/render_slides_isolated.py` copies the deck's font files
into the isolated profile's `user/fonts`. This is verified: Avenir Next + Georgia are embedded, and the v1 re-render is
pixel-identical to the 5B previews.

## RC-7 — Per-page font checks were impossible as designed
LibreOffice writes one shared font resource dict, so `pdffonts -f N -l N` lists the whole document. My first font test
falsely flagged LucidaGrande on all 45 pages; LucidaGrande is the fallback for the single "→" glyph on slide 24.
**Correction:** a document-level, glyph-coverage-aware `font_fidelity` test (required Avenir/Georgia embeds; fallback
allowed only for glyphs that Avenir/Georgia lack).

## RC-8 — A canonical structural gate is coupled to v1 geometry
`qa_ch1_slides.gate_review_letters` finds option boxes with `top >= 2.7in`. When I moved review options higher, it reported
`BADB?B` although the letters were correct (independently verified C·A·D·B·A·C). **Mitigation:** I did not edit the canonical
gate; the v2 layouts keep options at ≥ 2.75in (`OPT_TOP_MIN`). **Recommendation:** derive option order from the A/B/C/D
letter shapes, not from a y threshold.

## RC-9 — Design-spec drift went undetected
The Phase 5A spec requires Georgia slide titles, but v1 applied it only through `header()`. No test compared fonts with the
spec. Fixed in `text()`.

## RC-10 — No whole-slide visual inspection
Phase 5B reports that its environment could not view pixels. Deterministic checks cannot judge crops, hierarchy or
aesthetics. In this phase every changed slide was inspected at full resolution, and the full deck via contact sheet, by a
vision-capable agent (the builder — not independent).

## Regression fixtures
`tools/qa_slide_visual_v2_negative_tests.py` builds a 5-slide fixture deck at run time (F01-class occlusion, F02-class
caption overflow, unbacked text-on-photo, and two controls), renders it font-faithfully, and also re-checks the frozen 5B PDF.
Result: **11/11 pass**. All defect classes are detected, both controls pass, and the old checker is recorded as blind to them.

## Unproven hypotheses (not claimed)
- Renderer-specific glyph clipping: not observed; no clipping beyond the frame overflows above.
- Parent-coordinate errors: none (all shapes are top-level; no group transforms).
