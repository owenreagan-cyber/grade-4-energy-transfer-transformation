# FILE NAMING STANDARD

> Naming rules for all project-generated files. Authoritative source files are **never** renamed.

## Pattern
```
NN-chN-shortname-<role>[-key][-vX.Y].<ext>
```
- `NN` — zero-padded chapter index: `01`…`07` chapters; `09` = unit review/assessment.
- `chN` — chapter number (matches the 7-chapter backbone).
- `shortname` — kebab-case, lowercase, no spaces/punctuation.
- `<role>` — artifact role.
- `[-key]` — appended for answer keys (`-key`).
- `[-vX.Y]` — release version only (working drafts omit it).

## Role names
`teacher-map` · `slides` · `guided-notes` · `notes` · `worksheet` · `lab` · `quiz` · `key` · `review` · `media-plan` · `friday-flex` · `supply` · `qa`

## Examples (Chapter 1)
```
01-ch1-energy-causes-change-teacher-map.md
01-ch1-energy-causes-change-slides.pptx
01-ch1-energy-causes-change-guided-notes.docx
01-ch1-energy-causes-change-worksheet.docx
01-ch1-energy-causes-change-quiz.docx
01-ch1-energy-causes-change-quiz-key.docx
```
Releases:
```
01-ch1-energy-causes-change-guided-notes-v1.0.pdf
```

## Rules
1. Zero-padded chapter numbering.
2. kebab-case, lowercase.
3. Never rename authoritative source assets (e.g., `Science 4 - Energy Transfer - Student Book.pdf`, `Chapter_1_Energy_Causes_Change.pdf`).
4. Teacher keys always end in `-key` and live in `production/answer-keys/` (never merged into student files).
