# CH1 VISUAL CANDIDATE COMPARISON

Phase 5A. Compares rendered visual candidates across the three source families for each instructional
function. **Subjective scores are intentionally unset** (see "Vision status" below). Deterministic
facts (resolution, provenance, editability, SHA-256, text-free status) are authoritative; the
"Recommended default" column is a **provisional, non-visual default** pending vision review.

## Vision status (honest disclosure)

This Cursor environment does **not** surface image pixels to the agent (the Read tool returns an
acknowledgment only; OCR/`pdftotext` confirmed no text layer in the Gemini decks). Therefore:

- **Selection status for every subjective visual choice = `VISUAL_REVIEW_REQUIRED`.**
- **Subjective scores (science accuracy, composition, engagement, consistency, projector
  readability, extractability) are NOT assigned.** Metadata and scripted heuristics cannot substitute
  for human/vision judgment.
- Comparison sheets (side-by-side, labeled) are produced in `_comparison_sheets/` for a vision-capable
  reviewer to grade. See `CH1_PREMIUM_VISUAL_SELECTIONS.md` for the exact per-asset review list.

## Evaluation rubric (for the vision reviewer; weights per brief)

| Criterion | Weight |
|---|---|
| Scientific accuracy & instructional clarity | 30% |
| Photographic/compositional quality | 20% |
| Grade 4 engagement | 15% |
| Visual-system consistency | 15% |
| Classroom projector readability | 10% |
| Extractability/reconstruction feasibility | 10% |

Any asset depicting **magical glow, energy beams, invented visible energy, incorrect wording, or
watermarks** is ineligible regardless of score.

## Function-by-function comparison

Legend: **C** = Codex v5 (editable deck, embedded); **G1** = Gemini Session 1 (`Energy_Causes_Change`
×3 edits); **G2v1** = Gemini Session 2 `Forms_of_Energy`; **G2v2** = Gemini Session 2
`Forms_of_Energy-2`; **S** = standalone intake photographs.

| Function | Candidates (deterministic) | Recommended default (non-visual) | Status |
|---|---|---|---|
| Chapter opener | C `slide-01-opener.png` 1672×941 · S `candidate-a-clean…v2.jpg` 1920×1080 · S `candidate-a-lamp-lit…final.jpg` 1920×1080 · S `science-chapter-opener.jpg` (baked title → reject) | S lamp-lit (1920×1080, higher-res, no baked title); C fallback | VISUAL_REVIEW_REQUIRED |
| Big Question | deterministic (cream card + navy banner) | rebuild | (deterministic) |
| Pencil phenomenon | C `slide-09-pencil-before-after.png` 1942×809 · S `ch1-pencil-evidence-01.jpg` 1920×1234 · C `slide-06-pencil-before.png` (single close-up → reject) | C matched pair (proven matched; reuse across 6/8/11/36/37) | VISUAL_REVIEW_REQUIRED |
| Before/after (dark→bright) | C `slide-04-dark-bright.png` 1672×941 · S `ch1-dark-bright-01.jpg` 1920×1080 | S (higher-res) or C (proven matched) | VISUAL_REVIEW_REQUIRED |
| Energy vocab | C `slide-10-energy.png` 1448×1086 · S `ch1-voc-energy-01-refined.jpg` 1918×1233 · S `ch1-voc-energy-01.jpg` | S refined (higher-res) or C | VISUAL_REVIEW_REQUIRED |
| Change vocab | C `slide-09` pencil pair (reuse) · S `ch1-voc-change-01-refined.jpg` 1920×1234 | S refined or C reuse | VISUAL_REVIEW_REQUIRED |
| Five forms | C `slide-17-five-forms.png` strip 2172×724 · S 7 individual `ch1-forms-*.jpg` 1440–1536 · legacy `panel-08` | C strip for overview + S individual for cards (higher-res) | VISUAL_REVIEW_REQUIRED |
| Stored-energy hero | C `slide-22-stored-energy.png` 1448×1086 · S `ch1-voc-stored-energy-01.jpg` 1920×1234 · legacy `panel-05` | S (higher-res) or C | VISUAL_REVIEW_REQUIRED |
| Battery/rubber/apple | C `slide-25-stored-examples.png` strip 2172×724 · S `ch1-stored-battery-01.jpg` 1920×1440 · S `ch1-stored-raised-apple-01.jpg` 1440×1920 (portrait) · legacy `panel-11` | C strip + S individual battery/apple | VISUAL_REVIEW_REQUIRED |
| Evidence photos | C `slide-28-evidence.png` 1942×809 · legacy `panel-07-change-cards.png` | C 3-panel | VISUAL_REVIEW_REQUIRED |
| N1–N4 diagrams | deterministic PPTX shapes (navy nodes + gold arrows) — no raster | rebuild | (deterministic) |
| WRITE/CHECK layouts | deterministic | rebuild | (deterministic) |
| Friday synthesis | deterministic + C `slide-33-reflection.png` | C (or deterministic only) | VISUAL_REVIEW_REQUIRED |
| BQ return | C `slide-33-reflection.png` · C `slide-45-close.png` | C reflection (subdued) | VISUAL_REVIEW_REQUIRED |
| Review Q/A | text cards (deterministic); photos for Q2/Q3/Q6 from C pencil/rubber/battery | C photos on Q2/Q3/Q6 | VISUAL_REVIEW_REQUIRED (photo choice only) |
| Gemini Session 1 | G1 `Energy_Causes_Change` (10) / `-2` (16) / `-3` (15) — image-only slides | reference only; cannot be a slide master | VISUAL_REVIEW_REQUIRED |
| Gemini Session 2 | G2v1 `Forms_of_Energy` (11) vs G2v2 `Forms_of_Energy-2` (11) | see `CH1_GEMINI_SESSION2_A_B_COMPARISON.md` | VISUAL_REVIEW_REQUIRED |

## Deterministic disqualifications

- `science-chapter-opener.jpg` — baked title text ("Grade 4 Elementary Science Chapter Opener").
- `slide-06-pencil-before.png` — single close-up, no matched before/after.
- All Gemini decks — image-only (no editable text layer), 1376×768 (< 1080p), cannot be slide masters.
- Portrait `ch1-stored-raised-apple-01.jpg` — needs crop to fit a horizontal card.

## What a vision reviewer must decide (exact list)

1. Opener: which of 3 valid openers (1 Codex + 2 standalone) is strongest.
2. Dark/bright: Codex vs standalone matched pair.
3. Pencil pair: Codex vs standalone.
4. Energy/change/stored vocab heroes: Codex vs standalone (`-refined` vs base).
5. Five forms: use the single Codex strip, or rebuild cards from 7 standalone per-form photos.
6. Battery/rubber/apple: Codex strip vs standalone individuals.
7. Evidence 3-panel: Codex vs legacy panel.
8. BQ reflection/close: `slide-33` vs `slide-45`.
9. Gemini Session 2 A/B: any composition worth harvesting (per-slide, not whole-deck).
10. Gemini Session 1: any cinematic treatment worth harvesting.
