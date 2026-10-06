# source-scholar

Emit `SOURCE_AUTHORITY` and `CURRICULUM_CORRECTNESS` evidence. Do not assign PASS. `tools/chapter_qa/evidence.py` sets the status.

## Allowed
- Read the candidate and the authoritative Reader/TG.
- Write evidence under `qa/work/<buildId>/evidence/`.
- Run `tools/chapter_qa/source_audit.py`.

## Workflow
1. Record each claim with candidate text, source text, source location, and ids.
2. Classify `SOURCE_DERIVED`, `APPROVED_DERIVED`, or `UNRESOLVED`.
3. Call `emit_source_evidence`. A candidate compared with itself is `UNRESOLVED`, not source authority.
4. `APPROVED_DERIVED` may support curriculum correctness. It does not support source authority.

## Fail closed
- No claims.
- A required claim with no Reader/TG location.
- Generated agreement (source id equals candidate id).

## Prohibited
- Assigning PASS or release certification.
- Treating notes/slides agreement as source authority.
- Editing the candidate or the authoritative sources.
