# Final Classroom Delivery Package

> Teacher-facing delivery view of the frozen Grade 4 Energy curriculum.
> Everything here is a **relative symlink** to the single canonical file in
> `production/` (or `curriculum/`). Nothing is copied, modified, or regenerated.

## Layout

```
final-delivery/
├── START_HERE_TEACHER_GUIDE.md
├── RELEASE_HASH_MANIFEST.csv
├── Energy/                     (Unit 1 — Energy Transfer & Transformation)
│   ├── Unit 1 Teacher Guide
│   ├── Unit 1 Slide Decks
│   ├── Unit 1 Guided Notes
│   ├── Unit 1 Student Resources
│   ├── Unit 1 Labs
│   ├── Unit 1 Assessments
│   ├── Unit 1 Review Game
│   ├── Unit 1 Study Guide
│   └── Infographics
├── Natural Resources/          (Unit 2 — Using Natural Resources for Energy)
│   ├── Unit 2 Teacher Guide
│   ├── Unit 2 Slide Decks
│   ├── Unit 2 Guided Notes
│   ├── Unit 2 Student Resources
│   ├── Unit 2 Labs
│   ├── Unit 2 Assessments
│   ├── Unit 2 Review Game
│   ├── Unit 2 Study Guide
│   └── Infographics
└── Shared/                     (cross-unit teacher docs)
```

## Delivery method — relative symlinks

- Each entry is a **relative symlink** to the canonical file. The single source of
  truth remains the production paths; the delivery tree is a navigable index, so
  it can never go stale or duplicate an old copy.
- Symlinks resolve inside this repository on macOS/Linux. If you move the whole
  repository, relative links continue to resolve.

### Materializing real copies (for Google Drive / USB / zip)

To hand a teacher a self-contained folder without symlinks, dereference them:

```bash
# from the repository root
cp -RL production/final-delivery /path/to/delivery-copy
```

This follows every symlink and writes real files into the copy — leaving the
frozen repository untouched. (Drive upload should use a `cp -RL` copy, never the
symlink tree itself.)

## Regenerating

```bash
python tools/build_final_delivery.py
```

This re-creates all symlinks, refreshes `RELEASE_HASH_MANIFEST.csv`, and
regenerates `docs/reviews/GOOGLE_DRIVE_MIRROR_MANIFEST.md`.

## What is intentionally NOT here

- Rejected/retired files (INB notebooks, legacy `final-package/*`, `releases/*`
  export copies, `student-notes/` superseded copies, draft PDFs).
- Git-excluded supplemental media (`assets/supplemental/`) — the 5 embedded
  classroom-cut MP4s are listed in the hash/mirror manifests for backup, but are
  referenced inside the slide decks, not mirrored as loose files here.
- Historical QA reports / draft assessments / old study guides.

## Related records

- Frozen release: `production/final-8.5-week/FINAL_RELEASE_MANIFEST.md`
- Freeze record: `production/final-8.5-week/RELEASE_FREEZE.md`
- Full inventory: `production/final-8.5-week/MASTER_RESOURCE_INVENTORY.md`
- Hash + Drive backup: `RELEASE_HASH_MANIFEST.csv` · `docs/reviews/GOOGLE_DRIVE_MIRROR_MANIFEST.md`
