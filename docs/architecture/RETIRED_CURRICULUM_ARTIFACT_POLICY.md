# RETIRED CURRICULUM ARTIFACT POLICY

> **Repository policy — documentation only.** This defines a clean vocabulary and target convention for retired artifacts. It does **not** move, delete, or relink any file. Paths change only when a safe, automated migration is explicitly performed.

## 1. Lifecycle states

| State | Meaning | In classroom use? | References in master maps? |
|---|---|---|---|
| **ACTIVE** | Current, authoritative, reachable from `MASTER_CURRICULUM_MAP.md` / `MASTER_RESOURCE_INVENTORY.md` | Yes | Yes |
| **SUPERSEDED** | Replaced by a newer active resource; still readable but no longer preferred | No | No (mentioned only as provenance) |
| **RETIRED** | Removed from the curriculum on purpose (e.g., a design decision); kept for history | No | No |
| **ARCHIVED** | RETIRED/SUPERSEDED, physically relocated to the archive area | No | No |

## 2. Target archive location (convention)

- Retired files **should eventually live** under `archive/retired/` (top level), preserving a mirrored sub-path so history stays traceable, e.g.:
  - `archive/retired/production/student-notebook/chapter-01/…`
  - `archive/retired/production/final-package/…`
- Keep a lightweight `archive/retired/README.md` listing what was moved, when, and why.

> No `archive/` directory is created by this policy alone. It is created only during an actual, safe migration.

## 3. The rule for moving or deleting (do NOT unless ALL hold)

Do **not** move or delete a retired file unless **all** of the following are true:

1. An `archive/` target directory already exists (or is created in the same change).
2. No active document references the old path (verified by a path-integrity scan).
3. Automated path checks pass after the move.
4. No active resource (map, inventory, index, printing, prep, quickstart) points to the old location.
5. The move is committed separately from content edits.

If **any** condition is uncertain: **document the state only** (rename is never required).

## 4. Current retired/superseded sets (documented, not moved)

- **Interactive Science Notebook (INB) chapters 1–7** — `production/student-notebook/chapter-0X/*.docx`. Retired in favor of `premium-notes` guided notes + Science Journal. → Candidate for `archive/retired/production/student-notebook/`.
- **Unit 1 release PDF exports** — `production/releases/chapter-0X/*.pdf`, `production/releases/unit-final/`. Export copies; masters live in production. → Candidate for `archive/retired/production/releases/`.
- **Legacy final-package index** — `production/final-package/*.md`. Superseded by `production/final-8.5-week/`. → Candidate for `archive/retired/production/final-package/`.
- **Chapter-01 note-system comparison** — `production/comparisons/`. Study artifact. → Candidate for `archive/retired/production/comparisons/`.

## 5. What to write in manifests

- When a resource is retired, update `MASTER_RESOURCE_INVENTORY.md` §18 (`Archived / Retired`) with the new state and reason.
- When a resource is physically archived, add the mirrored path under §18 and note the move date.

## 6. Constraints

- Do **not** delete anything while it is still referenced (even by an old quickstart).
- Do **not** archive authoritative sources under `assets/authoritative/`.
- Keep every migration reversible (a move, not a delete) and committed atomically.
