# Chapter 1 — Instructional Parity Report (Phase 5C)

Tools: `tools/qa_ch1_premium_v2_parity.py` (→ `CH1_INSTRUCTIONAL_PARITY_V2.json`) and `tools/qa_ch1_premium_v2.py`
(frozen 28-gate canonical suite → `CH1_STRUCTURAL_QA_V2.md`). Overall: **PASS**.

| Check | Result |
|---|---|
| Slide count / sequence | 45, canonical order |
| Per-slide run text vs frozen canonical deck | identical on 45/45 (same comparison function as Phase 5B) |
| Speaker notes vs canonical | identical on 45/45 (teacher notes, TIME / PLAN / FRIDAY CLOCK lines unchanged) |
| Text + notes identical to Phase 5B candidate | yes |
| BQ / V / N anchors and order; BQ exact wording; note-wording mirror | PASS (28-gate) |
| Vocab definitions; V1/V2 grouping; N2 five forms; N3 three examples; model chains | PASS |
| Answers revealed on CHECK slides; no front-loaded answers; open tasks not pre-answered | PASS |
| Write-slide leakage phrases (11, 15, 21, 26, 30) | none |
| Review answer letters | C · A · D · B · A · C (unchanged); canonical "not patterned" gate PASS |
| Phase 6.1B gates (M1 M2 M3 L1 L4 L5 L6) | PASS |
| Banned vocabulary; transfer/transform scope | PASS |
| Font tiers (24 labels / 28 sentences) | PASS |
| Guided Notes, teacher key, canonical deck, Phase 5B candidate, releases | byte-identical to the session baseline (168 files) |
| N3 restored and in order (23 predict → 24 position → 25 model) | yes |
| Slide 32 application | preserved (KEEP) |
| New required media | none; no video embedded |
| Instructional text editable | all text is native PPTX text; photos carry no text |

New images were checked for answer leakage: review photos show only the question's scenario (Q2 before-state). Slide 28
photos carry no labels (see D2). Slide 33 adds no text (see D6).
