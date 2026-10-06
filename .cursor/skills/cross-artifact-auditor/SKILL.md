# cross-artifact-auditor

Compare notes, keys, slides, speaker notes, practice, quizzes, labs, recovery, the playbook, and the chapter spec. Emit `NOTES_SLIDES_SYNC`, `PLAYBOOK_ALIGNMENT`, or `ASSESSMENT_ALIGNMENT` evidence only.

## Allowed
- Read those artifacts.
- Write evidence under `qa/work/<buildId>/evidence/`.
- Run `tools/chapter_qa/cross_artifact.py`.

## Workflow
1. Build anchor maps for the two sides.
2. Compare instructional text, anchors, vocabulary, blanks, answers, sequence, labels, meaningful punctuation, ownership, required/optional status, scoring, and source references.
3. Call `emit_cross_evidence`.

## Fail closed
- Empty anchor maps.
- Answer, vocabulary, scoring, or blank mismatches.
- A request to emit `SOURCE_AUTHORITY` or `CURRICULUM_CORRECTNESS`.

## Prohibited
- Treating cross-artifact agreement as proof of curriculum correctness.
- Assigning PASS or release certification.
- Editing the artifacts.
