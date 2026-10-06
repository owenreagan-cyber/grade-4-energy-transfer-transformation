# qa-adversary

Attack the certification path on a throwaway workspace. Do not repair the canonical repo and do not assign PASS.

## Allowed
- Read the canonical repo.
- Write under `qa/work/` and other temporary directories.
- Run `tools/run_adversarial_qa.py`.

## Workflow
1. Choose `--case`, `--family`, or `--all`.
2. The runner copies or generates a candidate, applies one mutation, and calls the existing gate.
3. Record `caseId`, seed, build id, expected gate, actual status, and `canonicalRepoTouched`.
4. A bad mutation that returns PASS is an escape. Stop.

## Fail closed
- Canonical `production/` or `curriculum/` bytes change.
- A required test module does not execute.
- Evidence is missing, truncated, or uses an unknown status.

## Prohibited
- Editing frozen artifacts, baselines, or releases.
- Declaring `INTERNAL RELEASE CERTIFICATION`.
- Treating a project-authored literal as the only attack the detector can see.
