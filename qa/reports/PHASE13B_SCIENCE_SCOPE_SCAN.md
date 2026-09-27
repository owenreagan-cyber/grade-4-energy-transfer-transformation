# PHASE 13B — SCIENCE SCOPE SCAN (Forbidden Vocabulary)

> Automated sweep of all final student + teacher text for advanced/out-of-scope terms.
> Scope: every Markdown source (production tree) + 59 DOCX masters + 78 release PDFs.
> Rule (AGENTS.md / slide locks): required Grade 4 terms only — `stored energy`, `energy of motion`, `heat`, `light`, `sound`, `electric current`, `transfer`, `transformation`, `evidence`. Never require the advanced list below.

## Forbidden terms scanned
`proof` · `proves` · `kinetic` · `potential` · `mechanical energy` · `radiant` · `momentum` · `impulse` · `electron` · `compression wave` (+ `mechanical` standalone)

## Result: PASS (after 2 corrections)

### Genuine content hits — REMOVED
| File | Before | After | Class |
|---|---|---|---|
| `production/slides/01-ch1-energy-causes-change-slide-spec.md` (row 7, purpose) | "change **proves** energy" | "change **is evidence of** energy" | teacher-facing slide spec |
| `production/answer-keys/01-ch1-energy-detectives-key.md` (Part C) | "change **proves** stored energy" | "change **is evidence of** stored energy" | teacher-facing answer key |

Both were corrected to the "evidence / supports" framing; the student-facing text in the same files was already correct ("Change is evidence of energy").

### Guardrail hits — JUSTIFIED (NOT removed)
All remaining hits are **negative guardrails** instructing students/teachers NOT to use the advanced term, or teacher-facing "Do NOT teach" boundaries. Examples:

- `production/quizzes/04-ch4-energy-transfer-quiz-blueprint.md:39` — "kinetic/potential/mechanical/radiant vocabulary" (exclusion list)
- `production/labs/05-ch5-crash-lab-teacher-spec.md:35` — "Do NOT teach momentum, impulse, force calculations… 'Energy of motion' is the ceiling"
- `production/labs/04-ch4-electricity-transfer-teacher-spec.md:34` — "Do NOT teach electron flow…"
- `production/quizzes/07-unit-final-assessment.docx` — "Use 'supports,' not 'proves.'"
- `production/rubrics/06-ch6-engineering-rubric.docx` — "uses observed evidence (not 'proves')"
- `production/labs/unit-02/water-wheel-flagship-lab-teacher.docx` — "Students use 'energy of motion' and 'transfer' (not 'mechanical energy')"

These are boundary statements that *reinforce* the Grade 4 ceiling rather than violate it. No student-facing instructional content teaches or requires any forbidden term.

## WARN item
`production/releases/chapter-01/01-ch1-energy-causes-change-teacher-key.pdf` still carries the pre-fix wording ("change **proves** stored energy"). This is a **Phase 13A release export** of the answer key whose Markdown source is now corrected. Action: regenerate the release PDF from the corrected source on the next release pass, or treat the corrected Markdown (`production/answer-keys/01-ch1-energy-detectives-key.md`) as the source of truth. Student-facing material is unaffected.

**OVERALL: PASS** (2 genuine hits fixed; remaining hits are guardrail text only; 1 stale-export WARN documented).
