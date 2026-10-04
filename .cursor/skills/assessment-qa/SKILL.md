# assessment-qa

## When it applies
QA of quizzes, the unit final assessment, study guides, and review games.

## Required inputs
- Assessment artifact + key + blueprint.
- `docs/standards/ASSESSMENT_LAYOUT_STANDARD.md` + `docs/assessment/UNIT1_FINAL_ASSESSMENT_BLUEPRINT.md`.

## Workflow
1. Verify item counts, point values, and answer-key balance.
2. Confirm vocabulary assessed in context (not isolated matching).
3. Confirm same-object speed–energy items (no mass+speed confound).
4. Verify notes-define-boundary / Reader-verifies-science source rule.
5. Record results in `qa/reports/`.

## Outputs
- Assessment QA report (PASS/WARN/FAIL).

## Stop / failure conditions
- Advanced terminology as required.
- Answer-key sequence pattern or unbalanced distribution.
- An item not supported by both Reader + notes.

## Must obey
`ASSESSMENT_LAYOUT_STANDARD.md`, `UNIT1_FINAL_ASSESSMENT_BLUEPRINT.md`, `docs/planning/QA_GATES.md`.
