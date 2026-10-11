# CH1 Instructional Parity Report (Phase 5D)

> Candidate `ch1-premium-hybrid-v3` vs. frozen canonical deck (`production/slides/01-ch1-energy-causes-change-slides.pptx`).
> Tool: `tools/qa_ch1_premium_v2_parity.py` (paths overridden to v3).

## Results

| Check | Result |
|---|---|
| Slide count | **45** (canonical 45) |
| Text parity (45/45) | **PASS** — no slide text differs from canonical |
| Speaker-notes parity (45/45) | **PASS** — no slide notes differ |
| Text + notes identical to Phase 5B candidate | **True** |
| Review answer letters | **C · A · D · B · A · C** (canonical) |
| Embedded media files | 25 (all PNG, SHA-256 manifest emitted) |
| Answer leakage (WRITE slides 11, 15, 21, 26, 30) | **none** |

## Invariants preserved

- Exactly 45 slides; canonical ordering.
- Exact core text, titles, captions, labels, model meanings.
- Big Question wording exact.
- Reader references intact.
- Notes anchors (V1 11–12 · N2 19 no-CHECK · V2 21–22 · N3 23–27 · N4 28–31 · application 32).
- WRITE/CHECK reveal relationships unchanged.
- Review answer choices and answers unchanged.
- Required/optional slide classification unchanged.
- Monday/Tuesday/Friday sequencing unchanged (single pacing plan; no session opens on a reveal).
- No transfer/transformation instruction introduced into Chapter 1.
- No core-required media.

## Structural gates (28-gate canonical suite, `tools/qa_ch1_slides.py` against v3)

**OVERALL: PASS.** Including: font floor, font tiers, widescreen metadata, pacing plan, no reveal-opener, open-task-not-preanswered, review letters not patterned, rendered geometry (0 out-of-bounds / 0 overlap / 0 empty), vocab ≥48pt, no shape overflow, visual-token compliance, BQ/V/N anchors+order, note wording mirror, reveal correctness, no front-loaded answers, Reader refs, vocab grouping, N2 five forms, N3 three examples, model chains, A/B/C/D review, no banned language, transfer/transform scope, render QA, slide count.

## Final status

**PASS** — instructional parity fully intact. The v3 candidate differs from v2 only in the three scoped visual fixes (slide 20 photo removal, slide 24 apple crop, slide 27 answer contrast), none of which alter canonical text or notes.
