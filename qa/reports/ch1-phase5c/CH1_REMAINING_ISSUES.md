# Chapter 1 — Remaining Issues (Phase 5C)

## Owner decisions (block Classroom Ready, not the candidate)
D1–D7 are in `CH1_PHASE5C_ASSET_SELECTIONS.md`. The most material:
- **D3 — NEW_ASSET_RECOMMENDED:** the approved BEFORE pencil (R03) does not visibly show a *flat* tip, which the canonical
  text describes (slides 6, 8). No image was generated.
- **D1 — slide 20 photo vs. the teacher note "Save examples for slide 23".**
- **D4 — literal line feeds in canonical run text** render unevenly when centred in LibreOffice; PowerPoint is unverified.
  The fix (`<a:br/>`) needs the parity comparison to normalise whitespace — a canonical-tooling change.

## Verification gaps
- **Independent visual review not done.** My review was performed by the builder agent; AGENTS.md requires internal
  specialist review and an external (Grok) adversarial audit before freeze.
- **Only LibreOffice rendering verified.** PowerPoint/Keynote layout, line wrapping, and the "→" fallback glyph are untested.
  The build-time guard pads widths by 4%, which gives some margin for renderer differences.
- **Canonical gate brittleness (RC-8):** `gate_review_letters` depends on `top >= 2.7in`. I worked around it in layout and
  left the gate unchanged. A follow-up should make it letter-shape based.

## Cosmetic (non-blocking)
- Vocab card square navy rule over rounded corners (frozen component).
- Slide 4 statement wraps to 5 lines; slide 1 slide number is low-contrast.
- `safe_margin` WARN on the "BQ" mode chip (slide 2).

## Housekeeping
- `qa/reports/ch1-phase5c/pilot/build/` holds the nonrelease pilot build (PPTX/PDF/previews/staged crops). It is
  evidence only and may be deleted after review.
