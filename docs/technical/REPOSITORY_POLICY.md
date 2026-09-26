# REPOSITORY POLICY

> Single source of truth for what lives in Git and why. Finalized in Phase 2. Supersedes the open items in `docs/planning/GIT_STRATEGY.md`.

## Repository model
- **Branching:** `main` + `feature/<scope>` (no Git-flow complexity).
- **Remote:** none. Do not push. Do not configure GitHub.
- **First commit (baseline):** Phase 0 intake + approved Phase 1 architecture + these policies.

## What is TRACKED
| Path | Tracked? | Rationale |
|---|---|---|
| `*.md` (root, `docs/`, `curriculum/`, `production/`, `qa/`) | ✅ yes | architecture, specs, manifests, provenance, QA |
| `assets/authoritative/` | ✅ yes | canonical sources + derivatives (reproducibility, hashes) |
| `curriculum/` editable sources | ✅ yes | chapter source files |
| `production/` editable masters + templates + release PDFs | ✅ yes | production source of truth |
| project scripts/tools | ✅ yes | reproducibility |
| `AGENTS.md`, `.gitignore` | ✅ yes | agent + repo governance |

## What is EXCLUDED (tracked via inventory/provenance Markdown instead)
| Path | Excluded? | Rationale |
|---|---|---|
| `assets/supplemental/` (large binaries + cloud pointers) | ✅ excluded | ~219 MB; non-authoritative; inventory + hashes + doc IDs already tracked in `SOURCE_INVENTORY.md` / `SOURCE_PROVENANCE.md` |
| `assets/drafts/` (AI draft PDFs) | ✅ excluded | Level 4 idea banks; documented in `SOURCE_INVENTORY.md` + `docs/reviews/PHASE_1_DRAFT_COMPATIBILITY.md` |

## Binary rules (see `BINARY_ASSET_POLICY.md`)
- Authoritative PDFs are **intentionally tracked** (modest ~23 MB total).
- Supplemental binaries are **excluded by precise path**, never by a global `*.pdf` rule.
- Generated release PDFs are **tracked** (see `GENERATED_FILE_POLICY.md`).
- **No Git LFS** — ordinary Git is sufficient for this modest source set.

## Ignore rules are documented inline in `.gitignore` and summarized here
macOS (`.DS_Store`), temp (`*.tmp`, `*.temp`, `*.bak`, `*~`), Office locks (`~$*`), render/cache dirs (`.cache/`, `tmp/`, `temp/`, `renders/`, `_review_renders/`), Python (`__pycache__/`, `*.pyc`, `.venv/`, `venv/`), Node (`node_modules/`), plus the two precise binary exclusions above.

## Rules for future agents
- Never force-add an excluded path without updating this policy + the manifest first.
- Authoritative files are **never** edited in place or renamed.
- If a supplemental item becomes an approved production dependency, it may be admitted **intentionally** (documented in the manifest + provenance).
