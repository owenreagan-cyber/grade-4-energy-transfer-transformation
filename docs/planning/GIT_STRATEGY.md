# GIT STRATEGY

> **FINALIZED in Phase 2.** The authoritative implementation detail now lives in `docs/technical/REPOSITORY_POLICY.md`, `BINARY_ASSET_POLICY.md`, and `GENERATED_FILE_POLICY.md`. This file remains as the strategy summary.

## Model
- **Branching:** `main` + `feature/<scope>`.
- **Remote:** none — no push, no GitHub configuration.
- **Baseline commit:** Phase 0 intake + approved Phase 1 architecture.
- **Second commit:** Phase 2 production system + Chapter 1 staging.

## Tracking decisions (final)
| Content | Decision |
|---|---|
| Markdown architecture/spec/manifests/provenance/QA | ✅ tracked |
| Editable masters (PPTX/DOCX) + release PDFs | ✅ tracked |
| `assets/authoritative/` (incl. alternate Reader backup) | ✅ tracked (~23 MB) |
| `assets/supplemental/` binaries + cloud pointers | ❌ excluded (metadata tracked in Markdown) |
| `assets/drafts/` PDFs | ❌ excluded (idea banks; review tracked in Markdown) |
| project scripts/tools | ✅ tracked |
| `AGENTS.md`, `.gitignore` | ✅ tracked |

## Binary strategy (final)
- Ordinary Git (no LFS) — modest authoritative source set.
- Path-precise exclusions, never a global `*.pdf` ignore.

## Closed Phase 1 open items
- `.gitignore` → created (Step 3).
- Git LFS → not adopted.
- Authoritative PDFs → tracked.
- Alternate Reader → retained (6.56 MB acceptable within 23 MB authoritative set).
