# CH1 Regression Results (Phase 5D)

> `ch1-premium-hybrid-v3` vs `ch1-premium-hybrid-v2` (Phase 5C) and vs frozen canonical.

## Instructional regression

| Test | v3 result |
|---|---|
| 45 slides | PASS |
| Exact ordering | PASS |
| 45/45 text parity (vs canonical) | PASS |
| 45/45 speaker-notes parity | PASS |
| Anchor mapping (V1/N1/N2/V2/N3/N4) | PASS |
| WRITE/CHECK pairing | PASS |
| Answer sequence C·A·D·B·A·C | PASS |
| No new essential science | PASS (transfer/transform scope PASS) |
| N3 progression intact | PASS |
| Slide 32 application preserved | PASS |

## Technical regression

| Test | v3 result |
|---|---|
| All 45 slides render | PASS |
| Fonts correct (Avenir Next / Georgia embedded) | PASS |
| No clipped instructional text | PASS (0 containment FAIL) |
| No caption/card overflow | PASS |
| No unintended picture occlusion | PASS (0 occlusion FAIL) |
| No safe-margin violations (instructional) | 1 WARN (slide 2 "BQ" chip — pre-existing) |
| Image resolution/crops | PASS (no image_resolution FAIL/WARN) |
| No missing media relationships | PASS (25 embedded media, manifest emitted) |
| Valid PowerPoint XML | PASS (build succeeded; opens in python-pptx + LibreOffice) |

## Visual regression

| Test | v3 result |
|---|---|
| Original critical failures fixed (1, 4, 8 occlusion/overflow) | PASS (no recurrence) |
| Pencil BEFORE matches canonical text | **BLOCKED** (no asset) |
| Raised-object position clarity | FIXED |
| Stored-energy sequence respected | FIXED |
| Student-facing text readable (deterministic floor) | PASS |
| No new visual regressions | PASS (44/1/0 == v2) |
| No answer leakage via images | PASS (parity leakage gate PASS) |

## Classroom regression

| Test | v3 result |
|---|---|
| Monday 30-min route viable | PASS (single pacing plan; S1 24.5 min + 5.5 buffer) |
| Tuesday 30-min route viable | PASS (S2 24.5 min + 5.5 buffer) |
| Friday core synthesis viable | PASS (S3 25.0 min + 5.0 buffer) |
| Review appropriately optional | PASS |
| No video essential for core | PASS (media slot only; no required video) |
| Writing time realistic | PASS |

## Summary

3 targeted fixes applied (slides 20, 24, 27); no regressions introduced across instruction, technical, or automated visual QA. The **pencil asset** remains the single unresolved photographic-accuracy item (BLOCKED).
