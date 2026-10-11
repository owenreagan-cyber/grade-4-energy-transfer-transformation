# Chapter 1 — Premium Hybrid Candidate Readiness Report (Phase 5B)

Build ID: **`ch1-premium-hybrid-v1`** · Date: 2026-10-10 · Status: **BUILT_UNCERTIFIED**

## A. Gate 1 — Instructional Alignment

**PASS.**

- Mapped slides: **45 / 45** (S01–S45, no gaps/duplicates).
- Notes anchors verified: **8** (BQ · V1 · N1 · N2 · V2 · N3 · N4 · CHECK) — all resolve to canonical slides.
- WRITE/CHECK relationships verified: **5** (V1 11↔12 · N1 15↔16 · V2 21↔22 · N3 26↔27 · CHECK 30↔31); N2/N4/BQ are open writes (no CHECK slide) — preserved.
- Canonical content mismatches: **0**.
- Teacher-notes coverage: **45/45** (MODE + TIME + PLAN on every slide).
- Unresolved source conflicts: **0** (no authoritative source contradicted another).

Contract + report: `CH1_INSTRUCTIONAL_ALIGNMENT_CONTRACT.{json,md}` · validation: `CH1_GATE1_VALIDATION.md`.

## B. Gate 2 — Hybrid Presentation

- Build ID: `ch1-premium-hybrid-v1`.
- Candidate directory: `production/candidates/chapter-01/ch1-premium-hybrid-v1/`.
- PPTX: `01-ch1-energy-causes-change-premium-hybrid-v1.pptx` (12 MB) · SHA-256 `4f9b2ab4542ff2b3bb502a4cf460c4d92d591f81e99e4e286a2b2933db517a2c`.
- PDF: `01-ch1-energy-causes-change-premium-hybrid-v1.pdf` · SHA-256 `a812c35f9dffcb3b3cb7e6edfbf85dfd93663397771df18c69435cce315114b3`.
- Slide count: **45** (16:9, 13.333″ × 7.5″).
- Asset selections (8 photos, all text-free/OCR-verified): opener · dark/bright pair · pencil before/after pair · battery · raised apple · rubber band (stored strip crops).
- Editable text/shape confirmation: **PASS** — all titles, vocab, definitions, captions, prompts, anchors, model arrows/labels, tables, write fields, check answers, review Q/A are native PPTX text; photos are raster only.
- Teacher notes: **PASS** — 45/45 speaker notes, byte-identical to canonical.
- Display font: Georgia (titles/vocab) + Avenir Next (body) — both installed.

## C. QA

| Gate | Result |
|---|---|
| Structural (28 frozen canonical gates) | **PASS** |
| Source-content parity (premium text == canonical, 45 slides) | **PASS** |
| Speaker-notes parity (45 slides) | **PASS** |
| Notes parity (bidirectional, key→reveal) | **PASS** |
| Answer-leakage | **PASS** (none) |
| Image/diagram accuracy (deterministic: text-free, matched pairs, no glow/watermark) | **PASS** (deterministic only) |
| Rendering QA (`qa_visual_pdf.py`) | **PASS** (45/45, 0 WARN, 0 FAIL) |
| Full-slide visual inspection | **NOT PERFORMED** (no vision in this environment) — see remaining-issues |
| Classroom simulation (Mon 24.5 min · Tue 24.5 · Fri 25 + quiz 13 · buffer ≥5) | **PASS** |

## D. Safety — CONFIRMED

- Frozen canonical deck: **unchanged** (SHA-256 `5278f96c…` matches freeze record).
- Guided Notes: **unchanged** (`8fc5e400…`).
- Teacher key: **unchanged** (`909fbbbd…`).
- Existing release: **unchanged**.
- Unrelated working-tree changes: **preserved** (only `tools/hooks/protect_git.py` modified, pre-existing).
- Nothing staged, committed, pushed, or promoted.
- No visible-desktop automation (headless `soffice`/`pdftoppm` only; pre-existing LibreOffice process untouched).

## E. Readiness — **BUILT_UNCERTIFIED**

The candidate is instructionally exact, editable, and passes all deterministic QA. It is **not**
`CLASSROOM_READY` or Gold, because the required independent **whole-slide visual review** could not be
performed in this environment (no vision) — that is the sole remaining gate for `CLASSROOM_READY`,
and Gold additionally requires provenance/reproducibility/freeze/multimodal audit.

**Recommended next steps (Phase 5C/visual review, not part of this phase):**
1. Vision reviewer inspects `previews/` + `contact-sheet.png` + Phase 5A comparison sheets.
2. Apply any photo-placement overrides (and optionally add the 6 deferred image slides).
3. Re-render + re-run QA, then proceed toward freeze with owner approval.
