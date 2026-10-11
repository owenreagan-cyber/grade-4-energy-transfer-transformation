# Chapter 1 — Phase 5C Readiness Report

**Candidate:** `ch1-premium-hybrid-v2` → `production/candidates/chapter-01/ch1-premium-hybrid-v2/`
**Status:** BUILT · DETERMINISTIC PASS · VISUAL PASS (builder-agent) · independent visual review REQUIRED · NOT Classroom Ready · NOT Gold

| Artifact | SHA-256 |
|---|---|
| `01-ch1-energy-causes-change-premium-hybrid-v2.pptx` | `f3d7e8be8949890951898b7deda915dd389dfc7e562388bc8592eac5047d0240` |
| `01-ch1-energy-causes-change-premium-hybrid-v2.pdf` | `6a59757382802848d29cf741efac875d330ffd50beea714a4f63b8af43adf4b2` |
| `contact-sheet.png` | `e43646333de79ca22a8fef6185210080d5fc37150c89769ab5f075736d66c6d6` |
| previews `slide-01..45.png`, staged crops, asset manifest, tool hashes | `BUILD_SHA256.json` (84 entries) |

Reproduce: `.venv/bin/python tools/build_ch1_premium_v2.py && .venv/bin/python tools/render_slides_isolated.py
production/candidates/chapter-01/ch1-premium-hybrid-v2/01-ch1-energy-causes-change-premium-hybrid-v2.pptx
production/candidates/chapter-01/ch1-premium-hybrid-v2 --sheet …/contact-sheet.png`

## Gates
| Gate | Result | Basis |
|---|---|---|
| A — Diagnosis | **PASS** | F01–F10 reproduced; RC-1…RC-10 documented; fixtures fail on v1 (11/11) |
| B — Instructional protection | **PASS** | text + notes identical to canonical (45/45); 28/28 gates; letters C·A·D·B·A·C; no leakage |
| C — Pilot | **PASS** | critical failures fixed; new tests pass; pilot rendered and reviewed by vision; open subjective items listed (D1–D7) |
| D — Full candidate | **PASS (deterministic) / visual certification pending** | 45 rendered; 0 FAIL; builder-agent full review; independent review not yet done |
| E — Classroom Ready | **NOT CLAIMED** | owner decisions D1–D3; PowerPoint rendering unverified; independent review pending |

## Repository safety
- 168 protected files (canonical deck + PDFs, premium Guided Notes and key, Phase 5B candidate, releases, both prior
  builders, `protect_git.py`) verified byte-identical to the session-start baseline.
- Pre-existing uncommitted work preserved (the `protect_git.py` diff is unchanged). No stage, commit, push, reset, stash, or
  release promotion. No desktop automation. The pre-existing LibreOffice process (PID 4624) was not touched; every render
  used its own temporary profile and exited.
- New files only: `tools/{build_ch1_premium_v2, slide_layout_kit, render_slides_isolated, qa_slide_visual_v2,
  qa_slide_visual_v2_negative_tests, qa_ch1_premium_v2, qa_ch1_premium_v2_parity, gen_ch1_5c_evidence}.py`,
  `qa/reports/ch1-phase5c/`, `production/candidates/chapter-01/ch1-premium-hybrid-v2/`.
