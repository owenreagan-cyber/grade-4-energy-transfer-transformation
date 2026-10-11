# Chapter 1 — Layout Constructor Repair Plan (implemented)

Builder: `tools/build_ch1_premium_v2.py` (a copy of the Phase 5B builder; the Phase 5B and canonical builders are untouched).
Shared kit, reusable for Chapters 2–7: `tools/slide_layout_kit.py`.

| Constructor | v1 defect | Repair | Regression coverage |
|---|---|---|---|
| `text()` / `rich()` | fixed heights; `spAutoFit` | `check_fit` raises `FitError` when measured text exceeds its box; `MSO_AUTO_SIZE.NONE`; 40pt titles in Georgia | `qa_slide_visual_v2` text_containment; fixture slide 2 |
| `before_after_photo()` → `before_after_compare()` | caption box 0.5in regardless of text; photo letterboxed into leftovers; caption could paint over photo | panel = LABEL · PHOTO · CAPTION stacked regions; label and caption heights measured (worst case shared by both panels); photo = remaining height at a fixed aspect, cover-cropped, identical in both panels; text never enters the photo rect; raises if the photo drops below 1.2in | slides 4 and 8; fixture slides 2 and 4 |
| Slide 1 opener | photo appended above an 11.9in text box | two disjoint reserved regions; photo drawn first; every text row measured; assertion on column overflow | occlusion test; fixture slide 1 |
| `vocab_card()` | fixed offsets; photo variant changed text and was reverted in 5B | measured stack; optional `side` photo column beside term + definition; mini-model panel always kept; raises on overflow | slides 10 and 20 |
| `model_strip()` / `card_visual_chain()` | chip labels unmeasured | `check_fit` on every chip | all model slides |
| `photo()` / `photo_band()` | `_pic_fit` letterbox | `slide_layout_kit.cover()` exact-aspect crop around a focus point; every placement logged to `CANDIDATE_ASSET_MANIFEST.json` with SHA-256 | image_resolution test |
| `review_question()` / `review_answer()` | one repeated list layout | `review_slide(reveal=…)`: list / photo / grid families; question and reveal drawn by one function, so geometry is identical; options measured bold in both states; explanation band region pre-reserved; options start at ≥ 2.75in (canonical gate coupling, RC-8) | paired_geometry over all 6 pairs; canonical review-letters gate |

## Bounded-repair log (≤ 3 attempts per issue)
| Issue | Attempts | Outcome |
|---|---|---|
| Slide 1 column overflow (guard) | 2 (5.7in → 5.85in → 6.0in) | fixed |
| Slide 10 card overflow (guard) | 1 (top band → side column) | fixed |
| Slide 33 BQ height (guard) | 1 | fixed |
| Review 3 grid overflow (guard) | 1 | fixed |
| Review options top vs canonical gate | 1 | fixed (layout, not gate) |
| Review 6 photo variant | 3 (4.0in photo → 3.2in → adaptive width: 1.58in, unreadable) | stopped; moved to grid family (decision P-7) |
| Slide 24 apple crop | 1 | fixed (top-aligned) |
| Slide 6 crop | 2 (sharpener cut → tip cut → frame aspect 1.65) | fixed |

No shared-constructor change regressed another slide: the full 45-slide suite re-ran after every change.
