# build-teacher-playbook

## When it applies
Building or updating the Unit 1 Teacher Playbook — the teacher-facing control system that answers *what to teach, when, with what Reader pages, what students have, what to project, what materials, what to demonstrate, what is collected/graded, what to do if time is short, and what comes next.*

## Required inputs
- Authoritative CKSci Teacher Guide + Student Reader (never edited in place).
- Dated pacing (Unit 1 = Weeks 1–4; see `docs/playbook/UNIT1_PACING_CALENDAR.md`).
- Approved student resources (guided notes, worksheets, labs, quizzes, final).
- Approved slide anchors (BQ/V/N mirror) — or explicit `PLANNED` placeholders.
- Materials lists (`docs/planning/MASTER_SUPPLY_MATRIX.md`).
- Assessment alignment (`docs/standards/ASSESSMENT_LAYOUT_STANDARD.md`).
- Visual-system tokens (`assets/visual-system/design-tokens.json`, FROZEN v1.0).

## Workflow
1. **Verify source/pacing** — confirm exact Reader chapter titles/pages, TG lessons, Big Questions, vocabulary; confirm dated calendar does not invent content.
2. **Gather resource references** — build the resource map with real master locations and honest statuses (`AVAILABLE` / `PLANNED` / `NOT REQUIRED` / `OPTIONAL/FLEX`).
3. **Build/update teacher-facing section** — front matter + chapter spreads + special sections, using the reusable chapter spread template.
4. **Apply playbook visual system** — white/light-neutral pages, dark-navy unit identity, chapter accent tabs only, clean tables, compact callouts.
5. **Render** — editable master (DOCX) → PDF → preview images (editable-first; never native-PDF-only).
6. **QA** — automated gates (page size, margins, font floors, overflow, table clipping, page breaks, header/footer, token use, grayscale, no unsupported-artifact claims, no stale INB/26-item language) + independent review.
7. **Stop on unresolved source/resource mismatch** — never invent a missing resource or pretend an artifact exists when it does not.

## Outputs
- Editable playbook master (DOCX).
- PDF (release export).
- Render previews (PNG).
- QA report.

## Must obey
`docs/standards/TEACHER_PLAYBOOK_STANDARD.md`, `docs/standards/VISUAL_DESIGN_SYSTEM.md`, `docs/standards/UNIT1_PRODUCT_STANDARD.md`.

## Stop / failure conditions
- A resource the playbook references does not exist and is not honestly marked `PLANNED`.
- Any advanced vocabulary introduced as required (kinetic/potential/mechanical/radiant/compression-wave/inertia).
- Stale INB-primary language or stale 26-item assessment language.
- Any change to frozen visual-system tokens without the full token-update → regen → QA-re-run loop.
