# GENERATED FILE POLICY

> How project-generated (derived) files are handled. Finalized in Phase 2.

## Editable-first principle
Every classroom artifact has an **editable master**; PDF is a **release/export** format, never the only editable source.

| Artifact | Editable master | Release export |
|---|---|---|
| Presentations | PPTX / Google Slides | PDF (optional) |
| Notes / worksheets / quizzes / keys | DOCX / Google Docs / structured source | PDF |
| Planning / specs / manifests | Markdown | — |

## Release flow
```
EDITABLE MASTER → QA RENDER → FINAL RELEASE (PDF/PPTX)
```
- Never overwrite the master during rendering.
- Renders go to `_review_renders/` (gitignored); final releases go to `production/releases/` (tracked).

## Status vocabulary
`DRAFT → QA → ACCEPTED → RELEASED` (see `production/RELEASE_STANDARD.md`).

## Versioning
- Working drafts: no semantic-version noise; use the status tag.
- Final releases: `NN-chN-<name>-vX.Y.pdf`, e.g. `01-ch1-energy-causes-change-notes-v1.0.pdf`.

## What gets tracked
- **Editable masters** — always tracked.
- **Final release PDFs** — tracked (they are the classroom output).
- **Intermediate QA renders** — excluded (regenerable, under `_review_renders/`).

## Naming
- Zero-padded chapter numbering, kebab-case (see `production/FILE_NAMING_STANDARD.md`).
- Authoritative source files are **never** renamed.
