# UNIT 1 PLAYBOOK ARCHITECTURE

> Structure of the Unit 1 Teacher Playbook (editable master + PDF + previews).
> This documents the architecture; content lives in the editable master (`production/teacher-playbook/unit1-teacher-playbook.docx`) and this file.
> Authority: `docs/standards/TEACHER_PLAYBOOK_STANDARD.md`, `docs/standards/VISUAL_DESIGN_SYSTEM.md`, `docs/standards/UNIT1_PRODUCT_STANDARD.md`.

## Purpose

A Grade 4 teacher opens the playbook and immediately knows: what to teach, when, which Reader pages, what students have in front of them, what to project, what materials, what to demonstrate, what students complete, what is collected/graded, what to do if time is short, and what comes next.

## Section map

### FRONT MATTER

| # | Section | Status (Phase 2) | Notes |
|---|---|---|---|
| 1 | Cover | RENDERED | dark-navy unit identity + unit title + tagline |
| 2 | Unit at a Glance | RENDERED | title · 7 chapters · Big Idea · transfer/transformation · vocab · flagship lab · build · assessment · duration · resources |
| 3 | Dated Pacing Calendar | RENDERED | Weeks 1–4, day-level, honest slide/notes placeholders |
| 4 | How to Use This Unit | RENDERED | 30-min blocks · Friday FLEX · notes-first · BQ/V/N mirror |
| 5 | How Slides + Guided Notes Work | RENDERED | notes-first · exact-mirror rule · 9-step choreography · mode badges |
| 6 | Resource Map | RENDERED | full matrix (audience · status · key · reference) |
| 7 | Assessment & Grading Plan | RENDERED | 25Q/50pt locked · scoring convention · weighting note |
| 8 | Master Materials List | RENDERED | reusable · consumables · demos · labs · build · FLEX |
| 9 | Unit Vocabulary Map | RENDERED | 14 Core Vocabulary + chapter + Reader page + eligibility |
| 10 | Demo / Activity / Lab / Build Map | RENDERED | reconciled experiential taxonomy |

### CHAPTER SECTIONS

Chapters 1–7 each use the **reusable two-page teacher spread**:

- **LEFT — TEACH IT:** chapter number/title (chapter tab) · Big Question · Reader pages · approximate time · student resources · vocabulary/V-groups · N-anchor map · lesson blocks/sequence · what to project · what students do.
- **RIGHT — TEACHER SUPPORT:** demo/activity · materials · setup · teacher moves · Ask · Listen For · misconception/corrective move · do-not-overteach · if short on time · collect/grade · absent/makeup · what comes next.

Phase 2 fully populates **Chapter 1 only** (the prototype). Chapters 2–7 render as the blank template with `PLANNED` placeholders.

### SPECIAL SECTIONS

| Section | Status (Phase 2) |
|---|---|
| Ramp It Up 2.0 teacher guide | SKELETON (status `PLANNED` — ADAPT) |
| Pom-Pom Launcher teacher guide | SKELETON (status `PLANNED` — net-new) |
| Review plan | SKELETON (points to study guide + review game, both `AVAILABLE`) |
| Unit 1 assessment administration | SKELETON (points to locked 25Q/50pt + key) |
| Answer-key index | RENDERED (architecture + status table) |
| FLEX / enrichment / catch-up | SKELETON (points to Friday Flex framework) |
| Absent / makeup support | SKELETON (points to per-chapter recovery) |
| Media index | SKELETON (Ch1–2 staged · Ch3–7 scripts-only) |

## Editable-first pipeline

- **Master:** DOCX (`python-docx`), tracked.
- **PDF:** release export via LibreOffice headless (`soffice --headless --convert-to pdf`).
- **Previews:** `pdftoppm` PNG renders for visual QA.
- No native-PDF-only workflow; no Canva; no software install/upgrade.

## Visual system (consumed, not altered)

- FROZEN tokens from `assets/visual-system/design-tokens.json` (v1.0).
- White/light-neutral primary pages · dark-navy unit identity (`ink` `#1A1D26`) · chapter accent tabs only (chapter `primary`).
- Generous whitespace · clean tables (shaded header row) · compact callouts (left accent bar + convention tag) · minimal decorative framing.
- Grayscale-safe: color never the only signal.
