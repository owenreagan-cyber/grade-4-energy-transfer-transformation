# PHASE 13G — Week 7–8.5 Classroom-Use Review (Final Unit 2 Hardening)

> Final classroom-use pass over Week 7 (Wind · Hydro · Water Wheel), Week 8 (Solar · Geothermal ·
> Innovations · Solar investigation · Scenario Challenge), and Week 8.5 (synthesis · assessment ·
> corrections/reflection/certificate). Targeted edits only; no rebuild.

## Scope & method
- Simulated each 30-min block against the 20-student / 5-groups-of-4 model.
- Re-verified slide ↔ guided-note ↔ reader ↔ lab ↔ Friday-Flex ↔ assessment alignment.
- Ran guardrail (science) + controversial (climate/carbon) scans on every student-facing file.
- Re-rendered every edited DOCX → PDF via LibreOffice headless and checked page counts + content.

## Findings & fixes

| # | Finding | Fix | File(s) |
|---|---|---|---|
| 1 | Wind+Hydro delivered video (9:09) contained climate/carbon/"zero combustion"/Unit-1 review | Produced contiguous 1:35 wind excerpt (156–251 s), verified clean | `assets/supplemental/media/unit-02/chapter-05/wind-hydro-power-classroom-cut.mp4` |
| 2 | Week 7–8 pacing slide ranges under-specified (e.g., "S1–S3" stopped at the hook) | Corrected to full content ranges (S1–S7 / S1–S8 / S1–S6; solar Thu → S8) | `ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md` |
| 3 | Water Wheel teacher timing table had wheel-build (10 min) on Thursday, contradicting Wed-build pacing | Realigned to Thu = launch 4 / test 16 / cleanup+exit 10; added Wed build note | `water-wheel-flagship-lab-teacher.docx` |
| 4 | Unit 2 assessment scored parts summed to 24 vs declared 22 | Marked "Check Your Thinking" as **+2 bonus**; base total stays 22 | `unit-2-written-assessment-student.docx`, `unit-2-written-assessment-key.docx` |
| 5 | Assessment had a duplicate Name/Date header line on page 1 | Removed duplicate | `unit-2-written-assessment-student.docx` |
| 6 | Geothermal notes benefit cell read "little pollution (clean)" (advocacy-adjacent gloss) | Changed to "little pollution" (matches slide S7) | `unit-02-ch8-geothermal-energy-guided-notes.docx` |
| 7 | Solar mini-investigation lacked an explicit fair-test statement | Added "Fair Test: same device, same way of observing, change ONLY the light" | `solar-device-mini-investigation.docx` |
| 8 | Week 8 Friday-Flex categorization (RECOVER/EXTEND) + Week 8.5 PRACTICE/EXTEND diverged from spec | Aligned: RECOVER = Detective completion, EXTEND = innovation design; 8.5 PRACTICE = whole-unit review, EXTEND = reflection+certificate | `FRIDAY_FLEX_BANK.md`, pacing |
| 9 | Week 8 Mon still referenced "Video 7 (SUPPORT)" (not yet generated) | Marked PENDING GENERATION; added trimmed-clip note to header | pacing |
| 10 | Solar indoor-backup contingency not stated in teacher prep | Added PRIMARY window/outdoor + BACKUP indoor lamp (test the day before) | `TEACHER_PREP_GUIDE.md`, `MASTER_SUPPLY_LIST_20_STUDENTS.md` |

## Classroom acceptance gates

| Gate | Result |
|---|---|
| 1. Source Alignment | PASS — Ch5–9 tracked to Reader pp.25–49; no invented titles |
| 2. Scientific Accuracy | PASS — pathways correct; "energy of motion"/"transfer" used |
| 3. 30-Minute Fit | PASS — every block ≤30 min; Water Wheel simulated 4/16/10 |
| 4. Guided Notes Alignment | PASS — notes match slides + reader; 12–23 pt fonts (≥12 floor) |
| 5. Slide Readability | PASS — titles 38 pt, body 26–32 pt (11 pt "NOTE"/"THINK" = teacher hint labels only) |
| 6. Student Workload | PASS — one lab sheet + one mini-investigation; no overload |
| 7. Teacher Prep | PASS — 35 min (Wk 7) / 20 min (Wk 8); substitutions listed |
| 8. Lab Practicality | PASS — water containment, cleanup, reset, substitutions specified |
| 9. Friday Flex Integrity | PASS — no new core content; RECOVER/PRACTICE/EXTEND aligned |
| 10. Absent Recovery | PASS — partner data + self-contained sheets |
| 11. Media Fit | PASS — trimmed wind clip placed Wk 7 Mon only |
| 12. Assessment Fit | PASS — 22 pts (+2 bonus), ≤30 min, no base-load/scrubber/fission/climate |

## Guardrail scans (student-facing)

- **Science:** zero hits for proof/proves/kinetic/potential/mechanical energy/radiant/momentum/impulse/
  electron/compression wave/base-load/peak demand/grid stabilization/fission.
- **Climate/controversial:** zero hits for climate change/global warming/carbon footprint/carbon/zero
  carbon/carbon tax/cap and trade/climate crisis/activism/save the planet/energy policy.
- The one "mechanical energy" string lives in the **teacher** guide as an explicit "do NOT use this term"
  instruction — justified.

## Certificate & reflection
- Certificate wording confirmed: "Using fair tests to investigate speed and energy of motion" and
  "Tracing energy pathways through power systems." No Mechanical Motion / Mass & Collision Impact /
  community energy plan / climate references.
- Reflection prompts confirmed (changed thinking / strongest evidence / most interesting resource) — no
  policy advocacy.

## Outcome
**Week 7–8.5 is RELEASE-ready.** No FAIL gates. Remaining WARN items are cosmetic only (11 pt teacher
hint labels; "gears spin a smaller generator shaft" gloss in the video).

## Hygiene note (retired legacy INB PDFs — documented, not moved)
Retired legacy interactive-science-notebook PDFs still sit co-located with current releases under
`production/releases/` (note: path is `production/releases/`, not `releases/`). There is **no archive
convention** in this repo, so per policy these are **documented, not moved/deleted**:

- `production/releases/chapter-05/05-ch5-interactive-science-notebook.pdf`
- `production/releases/chapter-06/06-ch6-interactive-notebook.pdf`
- `production/releases/chapter-07/07-ch7-interactive-science-notebook.pdf`

These predate the Guided-Notes-primary system (no traditional INB). Future hygiene: archive under a
dedicated `production/releases/_retired/` (or equivalent) once a convention is agreed.
