# certify-chapter

## When it applies
Final certification of a chapter before it propagates to later chapters or is released.

## Required inputs
- Complete chapter package (teacher + student + media bundles).
- All prior QA reports (source, artifact, assessment, visual).

## Workflow
1. Confirm all required QA gates pass (no FAIL).
2. Verify slide↔notes mirror fidelity and canonical slide sequence.
3. Verify source fidelity + no answer leakage + premium visual quality.
4. Record FINAL ACCEPTANCE REPORT in `qa/reports/`.
5. Update manifests/status (`production/PRODUCTION_MANIFEST.md`, chapter manifest).

## Outputs
- Certification report + RELEASED status (or explicit hold).

## Stop / failure conditions
- Any FAIL gate (block release).
- Independent reviewer has not confirmed no source-boundary regression.
- Reviewer edited the artifact while certifying (silent-edit violation).

## Must obey
`docs/planning/QA_GATES.md`, `UNIT1_PRODUCT_STANDARD.md`, `docs/agent-workflows/AGENT_ROLES.md`.
