# AGENTS.md

> Guide for future Cursor/Codex agents working in this repository. Read before acting.

## PROJECT MISSION
Build a complete Grade 4 science unit (CKSci-aligned) for **Energy Transfer and Transformation** — chapter packages, teacher maps, presentations, guided notes, worksheets, labs, quizzes, enrichment, Friday Flex, assessments, engineering performance task, media, supply lists, keys, and QA.

## SOURCE HIERARCHY
- **LEVEL 1 — AUTHORITATIVE:** CKSci Student Reader (`assets/authoritative/student-reader/complete/Science 4 - Energy Transfer - Student Book.pdf`), Teacher Guide (`assets/authoritative/teacher-guide/`), official Activity Pages/Worksheets/Answer Key/Vocabulary.
- **LEVEL 2 — AUTHORITATIVE DERIVATIVE:** chapter splits + glossary.
- **LEVEL 3 — SUPPLEMENTAL:** teacher-created / third-party (may inspire, never override).
- **LEVEL 4 — DRAFT:** AI-generated idea banks (never authority).

## DO NOT
- silently override authoritative sources
- invent chapter titles (7 exact Reader titles)
- introduce advanced vocabulary as required (kinetic, potential, gravitational potential, mechanical, radiant, compression wave, inertia)
- call drafts final without QA (8 gates)
- alter authoritative files in place
- use supplemental material as authority
- conflate transfer (moves place/object) with transformation (changes form) — allow BOTH
- confound speed comparisons when teaching the core same-object relationship (compare SAME object at different speeds)
- force one-page student layouts
- reveal expected lab results on student pages
- add essential new content to Friday (Friday is FLEX only)

## DO
- inspect sources before authoring (prefer direct source inspection over summaries)
- label provenance: `SOURCE` / `ADAPTED` / `CUSTOM` / `EXTENSION`
- use editable-first production (PPTX/DOCX/Markdown masters; PDF = release export)
- preserve generous Grade 4 writing space
- run required QA and record results in `qa/reports/`
- update manifests/status (`production/PRODUCTION_MANIFEST.md`, chapter manifests)
- keep Friday nonessential
- favor low-prep, safe, reusable-heavy classroom investigations
- update `SOURCE_INVENTORY.md` + provenance when adding/regenerating assets

## REPOSITORY RULES
- See `docs/technical/REPOSITORY_POLICY.md`, `BINARY_ASSET_POLICY.md`, `GENERATED_FILE_POLICY.md`.
- Track `assets/authoritative/`; exclude `assets/supplemental/` and `assets/drafts/` (metadata lives in Markdown).
- No Git remote; do not push.
- Never force-add an excluded path without updating policy + manifest first.

## DEVELOPMENT / TESTING RULE
Do **not** use the user's visible desktop as the default automation environment.

Prefer:
- CLI
- headless tools
- isolated rendering
- test harnesses

If visible GUI testing is truly necessary, **stop and ask** before driving the user's desktop.

## PROCESS SAFETY
- Never run test/watch-mode runners in watch mode; prefer one-shot commands.
- Never start duplicate dev servers or test runners.
- Before starting a long-lived process, state what will run, why it stays alive, and how it will be stopped.
- Do not use detached jobs, `nohup`, or background `&` without approval.
- At task end, verify one-shot commands exited and report any remaining processes.
