# PHASE 4 — CHAPTER 1 SLIDESHOW REVIEW

> Independent final review of the Chapter 1 instructional slideshow build.
> Gate results: Source Fidelity **PASS** · PPTX Technical QA **PASS** · Render QA **PASS** · Notes↔Slide Sync **PASS** · Visual System Compliance **PASS** · Playbook Sync **PASS** · Independent QA **PASS**.

## 1. What Works

- **Canonical 45-slide deck** built notes-first from the finalized Guided Notes; exact BQ/V/N anchors (BQ 2/3/33 · V1 10–12 · V2 20–22 · N1 13–16 · N2 17–19 · N3 23–27 · N4 28–31) mirror the notes verbatim with reveal-not-front-load.
- **Full instructional choreography**: title → BQ → phenomenon (light switch) → live sharpener demo (observe/predict/what-changed/evidence) → vocabulary → Reader-supported instruction → notes/conceptual synthesis → application → check → return to BQ.
- **Visual theme** DISCOVERY/EVIDENCE with frozen tokens only; spacious, one core idea per slide, 40–65% visual weight where visuals teach.
- **Typography floors** enforced programmatically (chrome ≥ 12 pt, body ≥ 28 pt, vocab ≥ 48 pt, title 40 pt); zero text overflow measured against the actual Avenir Next font metrics.
- **Review section**: 6 multiple-choice A/B/C/D with question-state then answer-state, plausible distractors, shuffled correct letters (A/B/C/D/B/C), no all-of-the-above / none-of-the-above.
- **Speaker notes** on every slide (MODE · TIME · ASK · LISTEN FOR · REVEAL · NEXT).
- **Three QA artifacts** all pass: `PHASE_4_CH1_SLIDESHOW_QA.md` (20/20), `PHASE_4_CH1_SLIDESHOW_SOURCE_FIDELITY.md`, `PHASE_4_CH1_SLIDESHOW_INDEPENDENT_QA.md`.

## 2. What's Missing

- **Nothing blocking.** No required note anchor, model chain, or Reader page cue is absent.
- The virtual sharpener video remains **OPTIONAL / DEFERRED** (the previously failed AI-generated video is correctly not a dependency); live demo is the preferred path.
- Chapters 2–7 slideshows remain PLANNED (out of Phase 4 scope, untouched).

## 3. Fixes — specific problems + exact fixes

1. **Text overflow in 13 textboxes** (BQ banner mirrors, V2/N3 fill lines, CHECK YOUR THINKING question, demo evidence caption, review question/answer text). *Fix:* re-measured every run against real Avenir Next metrics; resized/reflowed boxes, reduced the N3 fill line to 28 pt, shortened non-contract scaffolding text (demo caption, review explanations), and gave long questions two-line boxes. Result: **0 overflow candidates**.
2. **HUD bubble width** ("TURN & TALK" overflowed the fixed 1.55" pill). *Fix:* `hud_bubble` now right-aligns and auto-sizes from a label-width table; no header overlaps.
3. **N3 notes overlap** (fill-in line sat on the last table row, slides 26–27). *Fix:* compressed model strip/table geometry and moved the fill line to y=5.2 for a clean gap.
4. **All review answers were "A".** *Fix:* shuffled correct letters to A/B/C/D/B/C.
5. **Low-contrast small gold labels** ("VOCABULARY"/"CHANGES"/"CHECK YOUR THINKING"/"SAMPLE"). *Fix:* switched them from accent gold `#A67C16` to neutral amber `#7A5620` (5.4–6.6:1), reserving gold for the mandated iconic uses (section-code chips, model arrows, BEFORE/AFTER labels, answer highlights).

## 4. Enhancements / Suggestions / New Ideas

- Consider a single low-stakes **voting HUD (VOTE)** on review question slides to formalize the A/B/C/D signal (currently implied in speaker notes).
- A future optional **virtual sharpener backup** could reuse the before/after component; keep it deferred per contract.
- The HUD right-alignment table could be derived from font metrics at build time instead of a static width map, if the pipeline ever gains a font-metrics dependency.

## 5. Edge Cases & Failure Modes

- **Font substitution**: deck specifies Avenir Next; if a viewer lacks it, a wider fallback (Arial) was used as the conservative upper bound during measurement — all text still fits at the Arial widths.
- **2-line BQ mirror**: the Big Question is 56 chars; at ≥28 pt it must wrap. Allocated two-line boxes so no renderer clips it.
- **Long MCQ options** (e.g. "Yes — stored energy that can cause change later") fit on one line at 28 pt in the 10.1" option box; no option wraps.
- **Reveal integrity**: QA gates confirm no front-loaded answers and no hidden note answers on non-anchor slides.

## 6. Performance Concerns

- Build (`tools/build_ch1_slides.py`) is deterministic and fast (~0.5 s). LibreOffice PDF render ~5 s; PNG previews ~6 s. No persistent processes, no watch-mode runners.
- No external assets are fetched at build time; all visuals are programmatic, so there is no network/asset-resolution risk.

## 7. Readability / Maintainability

- Single canonical builder with small composable helpers (`rect`, `tb`, `run`, `rich`, `chapter_tab`, `mode_badge`, `hud_bubble`, `anchor_chip`, `vocab_card`, `model_strip`, `before_after`, `review_question`, `review_answer`).
- QA is deterministic and structural (python-pptx text inspection, not OCR); re-run with `.venv/bin/python tools/qa_ch1_slides.py`.
- Manifest (`docs/chapter-01/CH1_SLIDESHOW_MANIFEST.md`) and the playbook "Chapter 1 — Slideshow Map" keep the slide map in sync; the legacy `01-ch1-…-slide-spec.md` is marked superseded to prevent a competing deck path.
