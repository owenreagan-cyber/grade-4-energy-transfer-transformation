# TEACHER PLAYBOOK STANDARD

> Teacher-facing documentation. Populated from established decisions only.
> Sources: `docs/reviews/UNIT1_INSTRUCTIONAL_RESTRUCTURING_AUDIT.md` (§B, §I, §O), `docs/planning/CHAPTER_PACKAGE_STANDARD.md`, `docs/reviews/UNIT1_CH1_PILOT_PREBUILD_AUDIT.md` (§L), and **Phase 2 Teacher Playbook Foundation** (`docs/reviews/PHASE_2_TEACHER_PLAYBOOK_FOUNDATION_REVIEW.md`).

## Principle
- The Teacher Playbook **documents the final system** — it does not drive curriculum decisions.
- Split: playbook *skeleton* (early) vs *finalization* (after all chapters) to keep it a documentation artifact.
- A teacher must be able to open it and teach tomorrow without hunting across files.
- It is a **premium teacher edition**, not a project-management document.

## Architecture (locked)
   10|
**FRONT MATTER**
1. Cover
2. Unit at a Glance
3. Dated Pacing Calendar
4. How to Use This Unit
5. How Slides + Guided Notes Work
6. Resource Map
7. Assessment & Grading Plan
8. Master Materials List
9. Unit Vocabulary Map
   20|10. Demo / Activity / Lab / Build Map

**CHAPTER SECTIONS** — Chapters 1–7 each use a reusable two-page teacher spread:
- **LEFT — TEACH IT:** chapter number/title, Big Question, Reader pages, approximate time, student resources, vocabulary/V-groups, N-anchor map, lesson blocks/sequence, what to project, what students do.
- **RIGHT — TEACHER SUPPORT:** demo/activity, materials, setup, teacher moves, Ask, Listen For, misconception/corrective move, do-not-overteach note, if short on time, collect/grade, absent/makeup, what comes next.
   30|
**SPECIAL SECTIONS**
- Ramp It Up 2.0 teacher guide · Pom-Pom Launcher teacher guide · Review plan · Unit 1 assessment administration · answer-key index · FLEX / enrichment / catch-up · absent / makeup support · media index (if applicable).

## Status vocabulary (locked)
- `AVAILABLE` — exists in the repo, current.
- `PLANNED` — scheduled, not yet built/rebuilding (do NOT fake a filename).
- `NOT REQUIRED` — intentionally absent.
- `OPTIONAL/FLEX` — exists or planned, but nonessential.
   40|

## Teacher bundle (per chapter)
- Teacher Map (objectives · sequence · Big Questions · TG lesson crosswalk).
- Daily sequence · Reader alignment · objectives · vocabulary (new/revisited/supporting/not-yet-expected).
- Misconceptions (`docs/planning/MISCONCEPTION_MAP.md`) · materials (`docs/planning/MASTER_SUPPLY_MATRIX.md`).
- Prep (setup/reset/cleanup) · Friday options (RECOVER/PRACTICE/EXTEND).
- Answer keys (separate from student pages) · absent-student recovery.

## Demonstration guide (consolidated)
- Format: **Materials / Set Up / Do This / Ask / Listen For / Connect / Do Not Overteach / If Students Ask / If Short on Time.**
- Teacher-note convention: `LIVE` / `BACKUP` / `TIME` / `ASK` / `LISTEN-FOR` / `NEXT` / `IF-SHORT-ON-TIME`.
   50|- Scripted "say this / listen for / if students ask" in one place.
- Live demo is preferred; virtual backup is `OPTIONAL` / `DEFERRED`.

## Keys
- Separate teacher key per assessment/quiz/worksheet/lab (see `docs/planning/TEACHER_KEY_STANDARD.md`).
- Keys visually mirror student pages, fill answers directly, include accepted/sample responses, preserve student-page numbering and section codes.
- For resources not yet rebuilt: `KEY STATUS = PLANNED / NOT YET GENERATED`.

## Visual (playbook)
- Premium publisher teacher edition + calm professional classroom utility.
- White/light-neutral primary pages · dark-navy unit identity (`ink` token) · chapter accent tabs only (chapter `primary`).
   60|- Generous whitespace · clean tables · compact callouts · strong hierarchy · minimal decorative framing.
- Grayscale-safe; color never the only signal. Do not make the playbook as immersive as student slides.

## Scoring & QA
- All scored work = raw score + percentage.
- Automated QA preferred; record results in `qa/reports/`.
- No "complete" claim without passing gates in `docs/planning/QA_GATES.md`.
- No unsupported-artifact claims; no stale INB-primary language; no stale 26-item assessment language (the locked final is **25 questions / 50 points**).
