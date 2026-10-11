# TWO-UNIT DAILY CURRICULUM & PACING MAP

> **Authoritative daily map already exists** and is the single source of truth — do not fork it:
>
> - `production/final-8.5-week/ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md` — combined Unit 1+2 day-by-day master pacing (8.5 weeks).
> - `production/final-8.5-week/MASTER_CURRICULUM_MAP.md` — one entry per day with real file paths ("authoritative whole-course navigation").
> - `production/final-8.5-week/MASTER_RESOURCE_INDEX.md` — Week→Day→Unit→Ch resource index.
> - `docs/playbook/UNIT1_PACING_CALENDAR.md` — dated Unit 1 calendar.

This file is the **reconciliation/coverage layer**: it states which per-date fields are required and where each is
populated, so gaps are visible rather than silently dropped.

## Required per-date fields and their source

| Field | Populated in | Status |
|---|---|---|
| Exact Reader chapter/pages | `MASTER_CURRICULUM_MAP.md` + `assets/authoritative/unit-02/…` | present (Unit 2 page ranges from PHASE13B intake) |
| Learning objective / approved I-can | chapter teacher maps (`curriculum/chapter-0X/teacher/`) | present for Ch1–3; **Ch4–7/Unit2 thinner** |
| Standards (from TG) | `assets/authoritative/*/teacher-guide` | present (source), not re-quoted in map |
| Concept + vocabulary | chapter vocab progression (`docs/planning/VOCABULARY_PROGRESSION.md`) | present |
| Required presentation + slide range | `MASTER_CURRICULUM_MAP.md` + slide specs | present Ch1–3; Ch4–7 slide specs exist, ranges unverified |
| Required student material | `MASTER_RESOURCE_INDEX.md` / `MASTER_RESOURCE_INVENTORY.md` | present |
| Teacher key | `production/answer-keys/`, `production/premium-notes/*-key.*` | present (frozen for Ch1/Ch2) |
| Media + live demonstration | `TWO_UNIT_MEDIA_MAP.md`, `FINAL_VIDEO_INVENTORY.md` | present |
| Lab / engineering activity | `production/labs/`, `curriculum/chapter-0X/teacher/` | present |
| Formative / summative assessment | quiz blueprints + `ASSESSMENT_BLUEPRINT.md` | present |
| Supplies + printing counts | `MASTER_SUPPLY_LIST_20_STUDENTS.md`, `PRINTING_GUIDE.md` | present |
| Instructional minutes | `MASTER_CURRICULUM_MAP.md` (30-min block) | present |
| Entry/handling/cleanup/transition minutes | `TEACHER_PREP_GUIDE.md` | present at week level; **not machine-verified per lesson** |
| Current artifact availability | `COMPLETE_RESOURCE_READINESS_CHECKLIST.md` | this layer |
| QA + approval status | `MASTER_PROJECT_STATUS_REPORT.md` | this layer |
| To-do tasks + dependencies | `COMPLETE_RESOURCE_READINESS_CHECKLIST.md` | this layer |

## Two-unit schedule (reference)

- **Unit 1** Oct 12–Nov 6 (W1–W4): 7 chapters; test Fri Nov 6.
- **Unit 2** Nov 9 start (W5–W8.5): 9 chapters; Thanksgiving Nov 23–27 excluded; test by Dec 16.

## Open reconciliation items
1. **Week 8.5 vs Week 9** label mismatch (final-delivery track vs pacing calendar).
2. **Ch4–7 + Unit 2 per-date minute/transition detail** is present only at week level, not machine-verified per lesson.
3. **Ch4–7 slide-range ↔ notes alignment** not yet independently audited (release parity only covers Ch1–3).
