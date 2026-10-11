# Phase 2 — Classroom Artifact Preservation & GitHub Checkpoint — Final Report

Generated 2026-10-10. Branch `recovery/classroom-artifact-preservation-2026-10`.
Head before work: `e311180` (main, up to date with origin/main).

## 1. Total file counts
| Class | Files | Size |
|---|---|---|
| Tracked (already in Git) | 1,591 | — |
| Untracked | 3,070 | ~2.0 GB |
| Ignored | 44,577 | ~3.0 GB |
| **Standalone media (video/audio)** | **75** | **2.00 GB** |

## 2. File-family classification (summary)
See `PRESERVATION_CLASSIFICATION.json` for the machine-readable table. Headline:

| Category | Families (representative) | Storage |
|---|---|---|
| CANONICAL_SOURCE | curriculum/handouts, curriculum/slides, docs/build-prompts | Git |
| OWNER_APPROVED | source-intake/2026-10-10-chapter-1-approved-notes | Git |
| FROZEN_RELEASE | 42 frozen paths (already tracked) | Git (verified 42/42) |
| ACTIVE_CANDIDATE | latest ch1/ch2 candidate masters, assets/ch1, assets/ch2, classroom-ready | Git |
| HISTORICAL_PROVENANCE | earlier candidate versions, .codex-build, gemini slideshows, supplemental library, intake media | External |
| UNIQUE_QA_EVIDENCE | qa/reports (text), qa/slides-qa (source), ipad-artifact-qa, inventory analysis | Git |
| REPRODUCIBLE_OUTPUT | previews, .xcresult, render PNGs, large hash dumps | External |
| TEMPORARY_CACHE | .venv, node_modules, tmp, __pycache__, .DS_Store, qa/work, _review_renders | None |
| REJECTED | (none identified) | — |
| UNRESOLVED | which ch1 candidate is canonical; Google Drive verification | Owner |

## 3. Unique valuable files preserved (staged into Git)
- **Sources/builders:** `docs/build-prompts/**`, `curriculum/handouts/**`,
  `curriculum/slides/**`, `source-intake/…/documents`, `…/images`,
  `…/SHA256SUMS.txt`, `…/verification.log`.
- **Guided-notes approval evidence:** `source-intake/2026-10-10-chapter-1-approved-notes/**`
  (student v2 + teacher key v2 + REGISTRATION.md + SHA256SUMS.txt).
- **Candidate source imagery:** `assets/ch1/**`, `assets/ch2/**` (+ manifests).
- **Active candidates:** ch1 `ch1-premium-hybrid-v6-embedded-media` (pptx+pdf+contact-sheet),
  ch2 `02-ch2-…-visual-candidate-v6-media` (pptx+pdf+reports+SHA256_MANIFEST+contact-sheet).
- **Classroom packet:** `production/classroom-ready/week-2026-10-12/chapter-01/**`.
- **QA evidence:** `qa/reports/` text reports, `qa/slides-qa/` source + Xcode host,
  `qa/ipad-artifact-qa/` (Swift + project.yml + manifests), `work/` build/QA scripts.
- **Recovery inventory + preservation docs:** `inventory/*.md`, `*.csv` (small),
  `PRESERVATION_CLASSIFICATION.json`, `MEDIA_STORAGE_RECOMMENDATION.md`.

## 4. Files EXCLUDED from Git (and why)
| Path | Reason | Storage |
|---|---|---|
| `assets/supplemental/**` | policy-ignored supplemental library incl. 1.3 GB video | Drive + manifest |
| `source-intake/2026-10-09-chapter-1/media/**` (18 MP4) | media binaries, no verified storage yet | Drive + manifest |
| `production/candidates/*/media/**` | media binaries (derivatives + dup sources) | Drive + manifest |
| `source-intake/…/slideshows/**` (10 Gemini PPTX/PDF, 115 MB) | AI draft idea bank (like assets/drafts) | External archive |
| `.codex-build/**` (183 files, 411 MB) | Codex build snapshots superseded by production/candidates | External archive |
| intermediate candidate versions (v1–v5) + nested previews/assets | superseded + reproducible renders | External archive |
| `previews/**`, `qa/reports` PNG renders, `qa/slides-qa/*.xcresult` | reproducible output | External archive |
| `inventory/` large `.txt` hash dumps (>1 MB) | regenerable listings | — |
| `.venv/`, `node_modules/`, `tmp/`, `__pycache__/`, `.DS_Store`, `qa/work/`, `_review_renders/` | dependencies/cache/OS artifacts | — |

## 5. Files awaiting owner decisions
1. **Which Chapter 1 candidate is canonical** — `01-ch1-energy-causes-change-visual-candidate-v5`
   vs `ch1-premium-hybrid-v6-embedded-media`. I staged the later (v6) as ACTIVE and
   classified v1–v5 + visual-v5 as HISTORICAL_PROVENANCE.
2. **Google Drive verification** — school + personal Drive access must be confirmed and
   uploaded media re-hashed before media counts as "backed up."
3. **Archive location** for superseded candidates / `.codex-build` / gemini slideshows.

## 6. Commits created (local only, NOT pushed)
1. Sources & production configs.
2. Classroom candidates & release evidence.
3. QA tools, fixtures, and non-reproducible evidence.
4. Inventory, manifests, and preservation documentation.

## 7. Git status & branch
- Branch: `recovery/classroom-artifact-preservation-2026-10` (created from `main` @ `e311180`).
- `main` unchanged; no push, no PR, no merge.

## 8. Frozen-byte verification
- `qa/gold-standard/frozen_registry.json` → **42/42 paths byte-identical** (SHA-256).
- Release parity `tools/qa_release_parity.py --chapter 1` → PASS; `--chapter 2` → PASS.

## 9. Secrets / PII scan
- Scanned 1,456 text files (tracked + untracked). No API keys/tokens/passwords.
- One owner-identifying datum: owner's own Apple Developer email + team ID in
  `qa/slides-qa/ch1/ipad-pro/IPAD_PRO_QA_REPORT.md` (code-signing identity) — flagged, not blocking.
- No student-identifying data (notes/quiz name fields are blank templates).

## 10. Candidate provenance & dependencies
- Candidate PPTX editable masters are reproducible from `tools/build_ch1_premium_v4.py`,
  `tools/build_ch2_slides.py` + `assets/ch1`,`assets/ch2` + the visual system.
- Source generators require python-pptx + LibreOffice (per `docs/technical/TOOLCHAIN.md`).

## 11. Remaining resources NOT backed up (do not call it fully backed up)
- **All 2.0 GB of video media** (75 MP4) — local disk only; external copy not yet verified.
- Superseded candidate versions, `.codex-build`, gemini slideshows, render PNGs —
  local disk only, recommended for external archive but not yet copied.

## 12. Proposed push & PR workflow (DO NOT execute until owner reviews)
1. Owner reviews the staged file list + this report + the 4 commits.
2. Owner authorizes media upload to Drive; re-hash verifies `MEDIA_SHA256_MANIFEST.json`.
3. `git push -u origin recovery/classroom-artifact-preservation-2026-10`
4. Open PR → `main`; owner reviews diff; merge after approval.
5. (Optional) decide archive destination for superseded candidates + `.codex-build`.

## Verdict
**Critical source, QA-evidence, and editable-master artifacts are recoverable via Git.**
The **video library and superseded binaries remain local-only** and are **NOT yet
backed up off-site** — they require the external-storage step above.
