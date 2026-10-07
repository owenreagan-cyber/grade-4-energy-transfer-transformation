# CHAPTER FACTORY v1.3 — F-3 / F-4 / F-8 REPORT

## A. Baseline
- **HEAD at start:** `163061f` (main)
- **Tests before:** 179 passed
- **Open blockers at start:** F-3 (partial), F-4, F-6, F-8, F-9

## B. Remaining F-3 Producer Audit
For the 11 producers outstanding at pass start, old vs new observation path:

| gateId | old observation | files now opened | observations derived | known-good | known-bad | result |
|---|---|---|---|---|---|---|
| STATUS_AUTHORITY | caller surface dicts | tracked status surfaces | status text from disk | FROZEN surface == FROZEN → PASS | premature FROZEN/RELEASED → FAIL | INDEPENDENT |
| SCHEDULE_POLICY | caller row dicts | pacing calendar file | dates + status tokens | Friday FLEX → PASS | Friday REQUIRED / unknown token → FAIL | INDEPENDENT |
| ADVERSARIAL_QA | caller summary dict | runner result JSON | bad-green/clean-red/completed/aborted | clean report → PASS | escaped / aborted → FAIL | INDEPENDENT |
| PRIOR_FROZEN_NONREGRESSION | caller observed dict | Ch1 guard + Ch2 golden tools | guard/unreviewed/stale/parity from tool output | unchanged frozen files → PASS | mutated frozen byte → FAIL | INDEPENDENT |
| SOURCE_AUTHORITY | caller claims | — | — | — | — | still CALLER_FED |
| CURRICULUM_CORRECTNESS | caller claims | — | — | — | — | still CALLER_FED |
| NOTES_SLIDES_SYNC | caller anchor dicts | — | — | — | — | still TAUTOLOGICAL |
| ANSWER_LEAKAGE | caller reveal sequence | — | — | — | — | still CALLER_FED |
| ASSESSMENT_ALIGNMENT | caller dicts | — | — | — | — | still TAUTOLOGICAL |
| PLAYBOOK_ALIGNMENT | caller dicts | — | — | — | — | still TAUTOLOGICAL |
| FRESH_EXPORT | caller hashes | — | — | — | — | still CALLER_FED |

## C. Final Producer Independence
- Mandatory producers: 27.
- Independent (file/tool-observing): 10 — CHAPTER_SPEC, NOTES_STRUCTURE,
  SLIDES_STRUCTURE, INVENTORY, RETIRED_CONTENT, STUDENT_PROMPT_CLARITY,
  STATUS_AUTHORITY, SCHEDULE_POLICY, ADVERSARIAL_QA, PRIOR_FROZEN_NONREGRESSION.
- PARTIALLY_INDEPENDENT: 3 — RENDER_COMPLETENESS, RENDERED_VISUAL_QA, RELEASE_PARITY.
- CALLER_FED: 4 — SOURCE_AUTHORITY, CURRICULUM_CORRECTNESS, ANSWER_LEAKAGE, FRESH_EXPORT.
- TAUTOLOGICAL: 3 — NOTES_SLIDES_SYNC, ASSESSMENT_ALIGNMENT, PLAYBOOK_ALIGNMENT.
- NON_ARTIFACT exceptions: 0.

F-3 is **not** fully closed: 7 producers remain caller-fed/tautological.

## D. Producer Provenance
- Fields added (in `toolVersions`, covered by the evidence seal):
  `producerSourcePath`, `producerSourceHash`, `gitBlobId`, `repositoryCommit`,
  `trackedSource`, `sourceClean`.
- `tools/chapter_qa/producer_provenance.py` computes tracked/clean/blob/source-hash
  from git + disk; `verify_provenance` recomputes and rejects:
  `PRODUCER_UNTRACKED`, `PRODUCER_PATH_MISMATCH`, `PRODUCER_SOURCE_CHANGED`.
- The Judge calls `verify_provenance` on every producer-sealed record.
- `sourceClean` is recorded; the tamper-evident property is enforced by the
  source-hash comparison (editing a producer after sealing changes its hash).
  Hard "clean at execution" enforcement belongs to F-6 (commit gate).

## E. ch3 Debug Script Disposition
`docs/chapter-03/CH3_DEBUG_TOOL_DISPOSITION.md`. 23 untracked scripts; all
`maySealEvidence = NO` (8 RETIRE, 15 DEBUG_ONLY).

## F. Fail-on-Abort
- Previous: no central evidence store; an aborted producer could leave an old PASS.
- New (`tools/chapter_qa/evidence_store.py`): `run_gate` invalidates the prior
  active record before running, converts any exception into a current FAIL
  record, and writes atomically (temp + rename).
- Exception, SystemExit, parser error, missing input, partial output all become
  a FAIL record; no stale PASS survives.

## G. Evidence Dedup
- Uniqueness key: `(buildId, gateId, scope)`; one active file per key by
  deterministic naming; `invalidate_prior` archives; `dedup_active` sweeps extras.

## H. Evidence Run Manifest
- `run_gate(..., manifest=…)` records gate/scope/status/aborted/finishedAt;
  `record_manifest` writes `run-manifest.json` atomically.

## I. Adversarial Runner
- Status and schedule mutation cases now write actual files and invoke the
  file-observing producers (`emit_status_evidence_from_files`,
  `emit_schedule_evidence_from_file`). No fabricated observation dicts for those
  families. Remaining anchor/leakage/assessment cases still use caller dicts
  (deferred with their producers).

## J. Gate Versions
Bumped: SCHEDULE_POLICY 1.0→1.1, ADVERSARIAL_QA 1.0→1.1,
PRIOR_FROZEN_NONREGRESSION 1.0→1.1, STATUS_AUTHORITY 1.1→1.2.
Rationale: caller-fed → file/tool-observing; old evidence cannot certify.

## K. Producer Self-Test Matrix
`qa/gold-standard/PRODUCER_SELF_TEST_MATRIX.json` updated. 10 INDEPENDENT,
3 PARTIALLY_INDEPENDENT, 7 caller-fed/tautological.

## L. External Attack Reproduction (F-3)
Status/schedule/adversarial/frozen mutations now caught through normal producers:
- premature FROZEN/RELEASED status → FAIL (caught)
- Friday REQUIRED first-exposure → FAIL (caught)
- Friday literal "Friday"/date → FAIL (caught)
- unknown schedule token → FAIL (caught)
- escaped adversarial run → FAIL (caught)
- aborted adversarial run → FAIL (caught)
- mutated frozen byte → FAIL (caught)
**bad green = 0** for these families.

## M. Provenance Attacks
- edit producer after seal → PRODUCER_SOURCE_CHANGED (caught)
- untracked producer → PRODUCER_UNTRACKED (caught)
- forged producerSourceHash → PRODUCER_SOURCE_CHANGED (caught)
**escapes = 0**

## N. Abort/Stale-PASS Attacks
- abort replaces prior PASS (caught)
- exception recorded as FAIL (caught)
- atomic write never half-written (verified)
**escapes = 0**

## O. Tests
- Total: 199 · Passed: 199 · Failed: 0 · Skipped: 0.

## P. Independent Review
A separate read-only reviewer was not launched this pass; documented as
remaining. The 7 remaining caller-fed/tautological producers are the known gap.

## Q. Frozen Non-Regression
- Chapter 1: unchanged (no frozen bytes touched).
- Chapter 2: unchanged.
- Combined playbook: unchanged.

## R. Commits
- `547f72d` — Harden producer provenance and fail-on-abort evidence (F-4 + F-8).
- (this pass) — Complete 4 more producer rewires + adversary rework + docs.
- push: NONE · tag: NONE.

## S. Remaining Factory Blockers
- F-6 (authorization / commit enforcement) — still open.
- F-9 (frozen Ch1/2 enforcement in commit gate) — still open.
- F-3 remainder (7 producers) — still open.

## T. Final Decision

F-3 PRODUCER INDEPENDENCE:
**FAIL** (10/17 mandatory release-blocking gates are file-observing; 7 remain
caller-fed/tautological).

F-4 PRODUCER PROVENANCE:
**PASS** (tracked + source-hash verified by the Judge; edit/untracked/forged
attacks caught).

F-8 FAIL-ON-ABORT + DEDUP:
**PASS** (fail-on-abort, atomic write, dedup, run manifest; stale-PASS attacks
caught).

READY FOR F-6 + F-9:
**NO** (F-3 remainder still open).

CHAPTER 3 PRODUCT REBUILD STARTED:
**NO**.
