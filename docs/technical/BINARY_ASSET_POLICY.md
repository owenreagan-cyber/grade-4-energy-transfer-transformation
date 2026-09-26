# BINARY ASSET POLICY

> How binary (non-text) files are handled in Git. Finalized in Phase 2.

## Principle
Track binaries only when their exact version matters for reproducibility. Exclude large, non-authoritative binaries and preserve them on disk + via hash manifest.

## Authoritative binaries — TRACKED
`assets/authoritative/` (~23 MB total) is tracked intentionally:
- canonical Student Reader (`Science 4 - Energy Transfer - Student Book.pdf`, 2.95 MB)
- alternate Reader backup (`Energy+Transfer+and+Transformation+SR.pdf`, 6.56 MB) — retained; repo impact is acceptable
- Teacher Guide (4.85 MB)
- official Activity Pages / Worksheets / Answer Key + Safety Contract / Vocabulary Study Guide
- chapter derivatives (Ch.1–7) + Glossary

Rationale: curriculum work depends on exact source versions; hashes/provenance must be reproducible; source changes must be visible.

## Supplemental binaries — EXCLUDED
`assets/supplemental/` (~219 MB) is excluded. This includes large PPTX/PDF files **and** the tiny `.gdoc`/`.gslides` cloud-pointer files. Their metadata (filenames, hashes, classification, doc IDs) is fully preserved in:
- `SOURCE_INVENTORY.md`
- `docs/provenance/SOURCE_PROVENANCE.md`

If a specific supplemental item later becomes a production dependency, it may be admitted **intentionally** (recorded in both the manifest and provenance).

## Draft binaries — EXCLUDED
`assets/drafts/` (3 AI-generated PDFs, ~72 KB) is excluded. They are Level 4 idea banks, not authority. Their inventory + compatibility review are tracked in Markdown.

## Generated/release PDFs — TRACKED
Production release PDFs under `production/` (e.g., `production/releases/`) are tracked when practical (see `GENERATED_FILE_POLICY.md`).

## Git LFS
Not adopted. Ordinary Git handles a ~23 MB authoritative set fine. LFS would add tooling complexity with no benefit here.

## Enforcement
- Exclusion is **path-precise** in `.gitignore`, never a global `*.pdf` rule.
- A CI/pre-commit size guard may be added later if the repo grows unexpectedly (not required now).
