# Chapter 1 — Automated Visual QA Upgrade

## New tools
| Tool | Purpose |
|---|---|
| `tools/qa_slide_visual_v2.py` | rendered-layout QA (tests below); JSON + MD output; exit 1 on FAIL. Deck-agnostic. |
| `tools/qa_slide_visual_v2_negative_tests.py` | regression fixtures + historical 5B regression (11 assertions) |
| `tools/render_slides_isolated.py` | font-faithful one-shot PPTX → PDF → PNG (checks exit code, PDF freshness, page count) |
| `tools/slide_layout_kit.py` | build-time fit guard (prevention rather than detection) |
| `tools/qa_ch1_premium_v2.py` | frozen 28-gate canonical suite re-pointed at v2 (report: `CH1_STRUCTURAL_QA_V2.md`) |
| `tools/qa_ch1_premium_v2_parity.py` | text/notes parity vs canonical and 5B, review letters, leakage, media SHA-256 |

## Test map (prompt §9)
| § | Test | Implementation | v1 result | v2 result |
|---|---|---|---|---|
| A | canonical text existence | 28-gate suite + parity | PASS | PASS |
| B | PDF text completeness | `pdf_text_completeness` (token multiset) | PASS | PASS |
| C | visible text bounds | `text_containment` (glyph core vs owning frame); `safe_margin` WARN | FAIL 4, 8, 15, 24, 25 | PASS |
| D | image/caption collision | `occlusion`, `text_over_photo` (opaque chip/scrim is a permitted overlay), `card_edge_straddle` | FAIL 1, 4, 8 | PASS |
| E | paired geometry | `paired_geometry` over 11/12, 15/16, 21/22, 26/27 and 6 review pairs | FAIL 15/16 | PASS |
| F | font fidelity | document-level, glyph-coverage-aware | WARN (→ fallback) | WARN (→ fallback) |
| G | readability | `min_rendered_size` WARN; `image_resolution` (WARN < 120 dpi, FAIL < 72); canonical font-tier gate | PASS | PASS (min photo dpi ≥ 120) |
| H | full-page diff | `pixel_diff` vs reference previews | — | KEEP slides 0–2% (title font only) |
| I | slide-family regression | full suite re-run after every constructor change | — | done |
| J | independent visual inspection | **not automatable** | not done in 5B | builder-agent vision review done; independent review pending |

## Results on v1 vs v2
- Old checker (`qa_visual_pdf.py`): v1 **PASS 45/45** (blind spot), v2 PASS.
- New checker: v1 **7 FAIL slides** (1, 4, 8, 15, 16, 24, 25); v2 **0 FAIL**, 1 WARN slide (2: "BQ" mode chip 0.23in from the edge; inherited chrome) and 1 document WARN (→ glyph fallback).

## False positives / negatives observed
- FP (fixed): per-page font test flagged LucidaGrande on all pages (RC-7).
- Arguable: slides 15/24/25 are frame overflows with no visible collision. They are kept as FAIL because frame overflow is
  renderer-dependent and PowerPoint/Keynote may draw it differently.
- WARN noise: `safe_margin` on the "BQ" chrome chip.
- No false negatives found against the known defects.

## Known limitations
- Owner matching is by token + position; duplicate short tokens in adjacent shapes could be mis-attributed (not seen in Ch1).
- Semi-transparent scrims are not modelled (opaque backing only).
- No contrast measurement of text on photos (the v2 deck has no text on photos).
- Semantic image correctness (e.g. "is the pencil tip flat?") cannot be automated; see decision D3.
- Only the LibreOffice renderer is verified; PowerPoint/Keynote layout is not.
