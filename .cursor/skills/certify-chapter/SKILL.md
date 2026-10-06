# certify-chapter

Chapter Factory release certification is only `tools/chapter_qa/release_judge.py`. This skill writes gate evidence and a report. It does not issue `INTERNAL RELEASE CERTIFICATION` and it does not by itself move a chapter to `FROZEN`.

## When it applies
Collecting cross-artifact gate evidence before the Release Judge runs.

## Required inputs
- Complete chapter package (teacher + student + media bundles).
- All prior QA reports (source, artifact, assessment, visual).

## Workflow
1. Run the required QA gates and record each result as `PASS`, `FAIL`, or `NOT_VERIFIED`.
2. Verify slide↔notes mirror fidelity and canonical slide sequence.
3. Verify source fidelity, no answer leakage, and premium visual quality.
4. Write the gate-evidence report in `qa/reports/`.
5. Stop. Do not update release manifests and do not set a release status.

## Outputs
- A gate-evidence report for the Release Judge. No `RELEASED` status.

## Stop / failure conditions
- Any `FAIL` gate. Record it and stop.
- Independent reviewer has not confirmed no source-boundary regression.
- Reviewer edited the artifact while certifying (silent-edit violation).

## Must obey
`docs/planning/QA_GATES.md`, `UNIT1_PRODUCT_STANDARD.md`, `docs/agent-workflows/AGENT_ROLES.md`.
