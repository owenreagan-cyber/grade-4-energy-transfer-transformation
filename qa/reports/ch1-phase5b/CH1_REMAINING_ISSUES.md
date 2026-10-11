# Chapter 1 — Remaining-Issues Register (Phase 5B)

Candidate `ch1-premium-hybrid-v1`. These are **non-blocking** for the candidate's correctness; they
block full *visual* certification and Gold/production certification.

## 1. Whole-slide visual review NOT performed (blocking for visual certification)

This Cursor environment does **not** surface image pixels to the agent (the Read tool returns an
acknowledgment only; OCR/`pdftotext` confirmed no text layer in the Gemini decks). Therefore:

- **No independent whole-slide visual review was performed.** Deterministic QA (28 canonical gates +
  rendered-geometry QA: 0 out-of-bounds, 0 overlapping words, 0 small text, 0 overflow) passed, but
  that is not a substitute for human/vision inspection of layout aesthetics and photo–text interplay.
- **Subjective visual selection was not finalized** in Phase 5A (all 12 raster picks carry
  `VISUAL_REVIEW_REQUIRED`). The build used the deterministic provisional defaults.

**Recommended next step:** a vision-capable reviewer examines `contact-sheet.png` and
`previews/slide-*.png`, and the Phase 5A comparison sheets, to confirm/override photo placement and
aesthetic fit before any freeze.

## 2. Vocab-card photographs deferred (text-parity decision)

Slides 10 (energy/change) and 20 (stored energy) keep the canonical **mini-model chains**
(`ENERGY → CHANGE`, `BEFORE → AFTER`, `STILL → LATER → CHANGE`) rather than photographs. Rationale:
the mini-chains are instructionally meaningful, and the vocab card visual panel is too small for a
meaningful photo. Swapping to photos changed slide text (removed chain words) and failed the text
parity gate — so it was reverted to preserve exact instruction.

## 3. Image layer deferred on 6 slides (no safe deterministic slot)

Photos were NOT added to these slides because a clean, no-reflow slot did not exist and layout
changes there could not be visually verified:

- Slide 14 (seashore) — full-width model + text leaves no empty panel.
- Slide 17 (five forms) — 3:1 strip aspect conflicts with the teaching layout.
- Slide 28 (evidence) — full-width navy card leaves no empty panel.
- Slide 33 (BQ reflection) — full-width banner leaves no empty panel.
- Slides 34–45 (review) — full-width option cards leave no empty panel; Q2/Q3/Q6 photos deferred.

These are candidates for a follow-up premium pass **after** vision review establishes safe placement.

## 4. Video candidates remain unapproved

No video is embedded (correct — none is core-required). The 18 intake videos remain pending the
curriculum-fidelity review described in `qa/reports/ch1-complete-asset-audit/CH1_VIDEO_INVENTORY.md`
(one already rejected; three are portrait "Proves" shorts). This is unchanged by Phase 5B.

## 5. Provenance limitation (Gold gate)

Gold / production certification additionally requires complete provenance, reproducible build,
candidate freeze, and independent whole-page multimodal audit. This candidate is
**BUILT_UNCERTIFIED**, not Gold.

## 6. Cosmetic

`CH1_STRUCTURAL_QA.md` is emitted by the reused canonical QA (heading reads "Phase 4"); its artifact
line cites the canonical path. The checks themselves ran against the premium candidate (paths were
overridden); only the report's prose label is stale.
