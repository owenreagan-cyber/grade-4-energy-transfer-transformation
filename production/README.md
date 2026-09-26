# PRODUCTION

> Editable-first production workspace for the Grade 4 Energy Transfer and Transformation unit.

## Layout
```
production/
├── templates/        # reusable specs + checklists (slides, notes, worksheets, labs, quizzes, keys, qa)
├── slides/           # editable slide decks (per chapter) — empty until Phase 3+
├── student-notes/    # guided notes masters — empty until Phase 3+
├── worksheets/       # worksheet/activity masters — empty until Phase 3+
├── labs/             # lab teacher/student pages — empty until Phase 3+
├── quizzes/          # chapter quizzes — empty until Phase 3+
├── friday-flex/      # Friday Flex resources — empty until Phase 3+
├── videos/           # media plans + explainer scripts — empty until Phase 3+
├── answer-keys/      # teacher keys (separate from student pages) — empty until Phase 3+
└── releases/         # final QA'd release PDFs/PPTX — empty until Phase 3+
```

## Key files
- `PRODUCTION_MANIFEST.md` — tracked inventory of every produced artifact + status.
- `FILE_NAMING_STANDARD.md` — zero-padded kebab-case naming rules.
- `RELEASE_STANDARD.md` — editable → QA → release flow and status vocabulary.
- `SUPPLY_REQUEST_WORKING.md` — working supply request (per group of 4; class totals = GROUP_COUNT × qty).

## Rules
- Editable-first: PPTX/DOCX/Markdown masters; PDF = release export.
- Authoritative source files are never renamed or edited in place.
- No full classroom content is authored in Phase 2 — only the **system** Chapter 1 will use.
