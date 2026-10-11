# Chapter 1 — Premium Pilot Comparison

Pilot package: `qa/reports/ch1-phase5c/pilot/` (nonrelease build via `CH1_V2_OUT`, full 45-slide render for context).
Side-by-side sheet: `pilot/PILOT_COMPARISON_SHEET.png`; per-slide pairs: `comparisons/slide-NN-v1-vs-v2.png`.
The final v2 candidate also includes the pilot-review fixes (slide 6 crop, review 6 family, opener chips at 24pt).

| Slide | Phase 5B | Phase 5C | Why it is better | Assets / crop |
|---|---|---|---|---|
| 1 | photo hid the end of the BQ | text column + full-bleed photo region | entire BQ readable; cinematic, not cluttered | R01 `slide-01-opener.png`, cover 6.43×7.5in, focus (0.72, 0.5) |
| 4 | caption over photo/card; 1.3in photos | matched 3.6×2.7in photos, reserved captions | the comparison is the visual focus; nothing collides | R02 halves, 4:3 cover |
| 8 | AFTER caption overflow | reserved 2-line captions, wider CHANGES | readable observation + change list | R03 halves, 4:3 cover |
| 10 | chains only (photos reverted for parity) | photos **and** chains | concept + example together; text untouched | R04; R03 pair stacked |
| 17 | five plain navy chips | five matched photo cards | each form has a concrete referent; labels stay editable | `ch1-forms-*` (R07 alternates) |
| 20 | small centred card | split photo + card | visible stored-energy situation next to the definition | R08 |
| 25 | small photo + squeezed model | full-width model + photo under STORED | the model reads left-to-right like the physical event | R08 alt rubber band |
| 28 | navy card, large empty area | card + two unlabeled evidence photos | students examine evidence; no answer text added | R10 panels 1–2 |
| 30/31 | card widths differ | SAMPLE card aligned to the WRITE card | the reveal visibly answers the card students wrote under | — |
| 34/35 | repeated list | list family (kept for concept items) | review system now varies across 3 families | — |

## Pilot gates
- Text + notes parity: PASS (identical to canonical) · 28-gate suite: PASS · visual QA v2: 0 FAIL.
- Visual review: every pilot slide inspected at full resolution by the builder agent (vision).
- Pilot-review findings acted on: slide 24 crop cut the apple → top-aligned; slide 8 CHANGES bullets broke awkwardly →
  column widened; slide 17 centred caption rendered ragged (in-run LF) → left-aligned; review 6 photo variant could not
  hold single-line options beside a readable photo → grid family (P-7).
- Subjective selections still open for the owner: see `CH1_PHASE5C_ASSET_SELECTIONS.md` decisions D1–D7.
