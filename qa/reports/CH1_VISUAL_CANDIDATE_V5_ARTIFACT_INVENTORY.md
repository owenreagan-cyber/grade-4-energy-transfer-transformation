# Chapter 1 Visual Candidate v5 — Phase Artifact Inventory

Date: 2026-10-09  
Status: **candidate generated and locally validated; not frozen or promoted to canonical**

## Deliverables

| Artifact | Purpose | SHA-256 |
|---|---|---|
| `production/candidates/chapter-01/01-ch1-energy-causes-change-visual-candidate-v5.pptx` | Editable 45-slide classroom candidate | `fdcc0efb9df13318d231ca36289b2a29ca34d47425d578a2cd41b17760ccbb54` |
| `production/candidates/chapter-01/01-ch1-energy-causes-change-visual-candidate-v5.pdf` | Rendered review/export derivative | `deae12a232b31a2bd20ed4bb273b8510584a0ac6baeec0db79355155315d4a7f` |
| `production/candidates/chapter-01/ch1-visual-candidate-v5-contact-sheet.png` | 45-slide navigation/contact sheet | not a release artifact |
| `production/candidates/chapter-01/review-sheets-v5/review-01-09.png` | Visual QA sheet | not a release artifact |
| `production/candidates/chapter-01/review-sheets-v5/review-10-18.png` | Visual QA sheet | not a release artifact |
| `production/candidates/chapter-01/review-sheets-v5/review-19-27.png` | Visual QA sheet | not a release artifact |
| `production/candidates/chapter-01/review-sheets-v5/review-28-36.png` | Visual QA sheet | not a release artifact |
| `production/candidates/chapter-01/review-sheets-v5/review-37-45.png` | Visual QA sheet | not a release artifact |

## Source and generation records

- `work/ch1-candidate-v2/build-ch1-candidate.mjs` — editable-first Artifact Tool build source.
- `tools/qa_ch1_visual_candidate.py` — candidate-specific deterministic content/structure validator.
- `assets/ch1/candidate-v2/IMAGE_GENERATION_MANIFEST.md` — accepted prompt set, tool mode, provenance, and rejected visual record.
- `assets/ch1/candidate-v2/*.png` — generated raster source assets. The manifest identifies the unused rejected image.

## QA records

- `qa/reports/CH1_VISUAL_CANDIDATE_V5_CONTENT_QA.md` — PASS, 45/45 slides.
- `qa/reports/CH1_VISUAL_CANDIDATE_V5_DETERMINISTIC_VISUAL_QA.md` — PASS, 45/45 rendered pages; 0 WARN, 0 FAIL.
- `.codex-build/ch1-candidate-v5/candidate.validation.json` — finalizer receipt: package integrity PASS, layout PASS with 0 findings/0 warnings, first-party import PASS, approved fonts PASS, and four native tables detected.

## Scope accounting

- The tracked canonical deck `production/slides/01-ch1-energy-causes-change-slides.pptx` was inspected but not modified.
- Authoritative CKSci files under `assets/authoritative/` were inspected but not modified.
- Superseded local generations v2–v4 and their temporary QA renders were moved to `.codex-build/ch1-candidate-archive/`; they are not delivery candidates.
- No commit, push, freeze, or canonical promotion was performed.
- The repository-required external Grok adversarial audit has not been run in this environment; therefore this candidate is not declared phase-complete or frozen.

