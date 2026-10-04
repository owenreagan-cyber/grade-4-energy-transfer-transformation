# source-fidelity-check

## When it applies
Verifying an artifact against authoritative sources before release or after edits.

## Required inputs
- The artifact under review.
- Authoritative Reader chapter + TG lesson (exact source definitions/pages).
- `docs/planning/VOCABULARY_PROGRESSION.md`.

## Workflow
1. Check titles, concepts, vocabulary, and framing against the source.
2. Verify exact source definitions are preserved verbatim.
3. Confirm no advanced terminology as required.
4. Confirm evidence ≠ proof and transfer/transformation BOTH-allowed framing.
5. Record PASS/WARN/FAIL with owner notes.

## Outputs
- Source-fidelity report in `qa/reports/` (PASS/WARN/FAIL).

## Stop / failure conditions
- Any content contradicting the Reader/TG.
- Invented chapter titles or vocabulary.
- Unstaged media treated as a build dependency.

## Must obey
`UNIT1_PRODUCT_STANDARD.md`, `docs/planning/QA_GATES.md` (SOURCE VALIDATION gate).
