# student-artifact-qa

## When it applies
QA of any student-facing artifact (notes, worksheets, labs, quizzes, tests, study guides).

## Required inputs
- The student artifact + its teacher key.
- `docs/standards/GUIDED_NOTES_STANDARD.md`, `STUDENT_HANDOUT_STANDARD.md`, `ASSESSMENT_LAYOUT_STANDARD.md`.

## Workflow
1. Check writing space, printability, grayscale quality.
2. Confirm no answer leakage on student pages.
3. Confirm raw score + percentage scoring; keys separate.
4. Confirm observation vs inference and fair-test logic.
5. Run applicable automated/headless QA; record in `qa/reports/`.

## Outputs
- QA report (PASS/WARN/FAIL) per `docs/planning/QA_GATES.md`.

## Stop / failure conditions
- Expected results revealed on a student page.
- Forced one-page layout or cramped writing space.
- Missing separate teacher key.

## Must obey
`STUDENT_HANDOUT_STANDARD.md`, `GUIDED_NOTES_STANDARD.md`, `ASSESSMENT_LAYOUT_STANDARD.md`, `docs/planning/QA_GATES.md`.
