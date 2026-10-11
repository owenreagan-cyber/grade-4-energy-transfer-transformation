# Chapter 1 — Build Environment & Dependency Report

Phase 5B candidate `ch1-premium-hybrid-v1`.

## Toolchain

| Component | Version |
|---|---|
| Python | 3.14.7 (`.venv/bin/python`) |
| python-pptx | 1.0.2 |
| Pillow | 12.3.0 |
| LibreOffice (soffice, headless render) | 26.8.0.3 |
| poppler (pdftoppm / pdfinfo / pdftotext) | 26.10.0 |

## Fonts (verified installed → headless-safe)

| Role | Family | Status |
|---|---|---|
| Display / titles / vocab term | Georgia | installed (`/System/Library/Fonts/Supplemental/Georgia.ttf`) |
| Body / chrome | Avenir Next | installed (`/System/Library/Fonts/Avenir Next.ttc`) |
| Fallbacks | Helvetica / Helvetica Neue | installed |

Note: Inter / Source Sans / Aptos / Merriweather are **not** installed and would silently
substitute in headless LibreOffice — hence the Phase 5A decision to use Georgia + Avenir Next.

## Inputs (read-only, unchanged)

- `production/slides/01-ch1-energy-causes-change-slides.pptx` (frozen v1.1) — text/notes source.
- `tools/build_ch1_slides.py` (copied → `tools/build_ch1_premium_slides.py`, then edited).
- `tools/ch1_pacing.py` — single timing authority.
- `assets/ch1/candidate-v2/*.png` (Codex v5 raster) — 8 files used.
- `production/premium-notes/01-ch1-energy-causes-change-guided-notes{,-key}.pdf` — alignment ground truth.

## Builders (new, scoped to this candidate)

- `tools/build_ch1_premium_slides.py` — premium builder (copy of canonical + Georgia display + 8 photos).
- `tools/gen_ch1_contract.py` — Gate 1 contract generator + validator.
- `tools/qa_ch1_premium.py` — re-runs the frozen 28-gate canonical QA against the candidate.
- `tools/qa_ch1_premium_parity.py` — text/notes parity + leakage + asset manifest.
- `tools/gen_ch1_5b_reports.py` — slide manifest + pacing/notes/write-check reports.

## Outputs (new candidate; no canonical file touched)

`production/candidates/chapter-01/ch1-premium-hybrid-v1/`

- `01-ch1-energy-causes-change-premium-hybrid-v1.pptx` (12 MB) · SHA-256 `4f9b2ab4542ff2b3bb502a4cf460c4d92d591f81e99e4e286a2b2933db517a2c`
- `01-ch1-energy-causes-change-premium-hybrid-v1.pdf` · SHA-256 `a812c35f9dffcb3b3cb7e6edfbf85dfd93663397771df18c69435cce315114b3`
- `previews/slide-01..45.png` (45) · `contact-sheet.png` · `assets/` (5 staged crops)
