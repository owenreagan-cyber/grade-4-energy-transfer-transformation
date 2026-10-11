# CH1 PHASE 5B IMPLEMENTATION PLAN

Phase 5A. Planning only — **no implementation starts in this phase.** Uses the existing native PPTX
builder pattern (`tools/build_ch1_slides.py` + `python-pptx`), NOT HTML/React/Marp/Canva/Keynote.

## 1. Build architecture

- **Builder:** new `tools/build_ch1_premium_slides.py` (editable-first), modeled on the canonical
  `tools/build_ch1_slides.py` so helper parity (header/tab/badge/HUD/anchor/model/before-after/vocab/
  notes/review) is preserved. It consumes:
  - the locked 45-slide spec (`CH1_45_SLIDE_SPEC.json`),
  - the selected-asset manifest (`CH1_SELECTED_ASSET_MANIFEST.json`),
  - the frozen design tokens (`assets/visual-system/design-tokens.json`),
  - `tools/ch1_pacing.py` (single timing authority).
- **Raster ingestion:** read from `assets/ch1/candidate-v2/` (Codex) and
  `source-intake/2026-10-09-chapter-1/images/` (standalone); crop via Pillow (halves/strips) into a
  staging dir; never mutate originals.
- **Speaker notes:** reuse the canonical `MODE/TIME/PLAN/STUDENT RESOURCE/ASK/LISTEN FOR/REVEAL/
  MISCONCEPTION/NEXT/IF SHORT` schema, driven by `tools/ch1_pacing.py`.
- **Output:** new candidate under `production/candidates/chapter-01/` (new filename) — never the
  frozen canonical deck or release.

## 2. Implementation order (essential path first)

1. **Constructors + tokens** (chrome, header, model, before-after, vocab card, table, review).
2. **Monday path** — slides 1,2,3,6,7,8,9,10,11,12,13,14,15,16 (+ optional 4,5).
3. **Tuesday path** — slides 2(re-entry),17,19,20,21,22,23,24,25,26,27 (+ optional 18).
4. **Friday path** — slides 2(re-entry),28,29,30,31,33 (+ optional 32).
5. **Optional review** — slides 34–45.
6. **Asset swap pass** — apply any vision-review overrides from the unresolved-decision register.
7. **Render + QA** (below).

## 3. Rendering (headless)

- `soffice --headless --convert-to pdf` (LibreOffice) → PDF.
- `pdftoppm -r 150` → PNG previews.
- Contact sheets via the existing Phase 5A/4 scripts.

## 4. QA gates (deterministic, isolated)

- `tools/qa_ch1_visual_candidate.py` (45-slide count, 16:9, anchor text, write/reveal, leakage,
  review verbatim, speaker-note schema, vocab guardrails, media fallback, picture placement, native
  tables) — **retarget slide numbers to the canonical map**.
- `tools/qa_visual_pdf.py` (rendered 45/45, no WARN/FAIL).
- Notes-to-slide exact-match + answer-leakage (reuse canonical QA).
- Classroom time simulation (`tools/ch1_pacing.py` gates) — verify Mon/Tue/Fri ≤ 25 min, Friday
  fallback intact, no Friday first-exposure.

## 5. Freeze path (not in 5B)

After deterministic QA + visual QA + contact-sheet review, follow the phase pipeline: external Grok
adversarial audit → verified remediation → final QA → owner approval → freeze. **No promotion or
freeze without explicit owner approval.**

## 6. Scope guardrails (5B)

- Do not modify the frozen deck, Guided Notes, teacher key, or authoritative sources.
- Do not promote a candidate; do not commit/push without request.
- Keep all new files under `production/candidates/chapter-01/` and `qa/reports/`.
