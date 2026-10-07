# CHAPTER FACTORY v1.3 — F-6 / F-9 REPORT

## A. Baseline
- **HEAD at start:** `ef328cf` (main)
- **Tests before:** 222 passed
- **Open blockers at start:** F-6, F-9

## B. Authorization Trust Model
`docs/gold-standard/AUTHORIZATION_TRUST_MODEL.md`.
- **Trusted:** `.git/hooks/pre-commit` (host-installed, pins gate+registry hashes);
  `frozen_registry.json` (hash-pinned); freeze-commit baselines; the Release
  Judge (recomputed from disk); host-injected owner authorization.
- **Untrusted:** any agent-writable repo file; `qa/work/**`; caller-supplied
  "current" values; `--no-verify`/`--amend`/broad staging.
- The previous `qa/work/git-authorization.json` self-grant mechanism is retired:
  `protect_git._authorization_file()` now returns `{}`.

## C. Commit Enforcement
- Hook: `.git/hooks/pre-commit` (real git enforcement; runs for direct,
  subprocess, and wrapper commits).
- Direct commit: ALLOW → hook enforces frozen bytes.
- Subprocess (python/node) commit: hooks fire (canary-verified).
- Wrappers: hooks fire (git-native).
- `--no-verify` / `--amend` / `git add .` / `-A` / `--all`: DENIED by the shell
  gate; never reach the hook.
- Result: commit authority is no longer a self-grantable boolean.

## D. Freeze Enforcement
Prerequisites (unchanged + strengthened): Judge PASS, legal lifecycle, current
evidence, producer provenance, frozen non-regression, release parity, external
audit acceptance (build-bound + candidate-bound), owner authorization
(host-injected). `_read_lifecycle` now also binds `candidateHash`.

## E. Frozen Baseline Registry
`qa/gold-standard/frozen_registry.json` (42 files): Unit 1 Ch1 + Ch2 classroom
bytes + combined playbook. Trust anchor = pinned `REGISTRY_SHA` in `frozen_gate.py`
+ pinned `GATE_SHA` in the hook.

## F. Frozen Byte Enforcement
- Chapter 1: covered (all `01-ch1-*` bytes).
- Chapter 2: covered (all `02-ch2-*` bytes).
- Combined playbook: covered (`.docx` + `.pdf`).

## G. Same-Run Canaries
All machine-readable via `tests/chapter_qa/test_f6_f9_canaries.py`:
- frozen bytes unchanged → ALLOW (caught as allow)
- registry tamper (remove a chapter) → DENY (caught)
- mutated frozen file → DENY (caught)
- subprocess commit with failing hook → DENY (caught)
- python `-c` subprocess commit with failing hook → DENY (caught)
- `--no-verify` / `--amend` → DENY (caught)
- wrapped destructive command → DENY (caught)
- repo file self-grant → DENY (caught)

## H. Bypass Attacks
11 canary + adversarial bypass cases. **Caught: 11 · Escaped: 0.**

## I. Clean Controls
- clean commit → ALLOW (caught as allow)
- clean add → ALLOW (caught as allow)
- passing hook commit → ALLOW (caught as allow)
**False DENY: 0.**

## J. Independent Forensic Review
A separate read-only forensic reviewer was not launched this pass; the canary
suite provides the mechanical same-run coverage. Documented as remaining.

## K. Tests
- Total: 233 · Passed: 233 · Failed: 0 · Skipped: 0.

## L. Gate / Factory Versioning
F-6/F-9 are enforcement-layer (hooks), not gate-semantics changes; no
evidence-gate version bump. Recorded in
`docs/gold-standard/AUTHORIZATION_TRUST_MODEL.md` and
`qa/gold-standard/frozen_registry.json` (`schemaVersion 1.0`).

## M. Commit
- `859aba1` — Harden Chapter Factory authorization and frozen protections (F-6 + F-9).
- (post-commit) lifecycle candidateHash binding.
- push: NONE · tag: NONE.

## N. Post-Commit Verification
- Frozen canaries: PASS (unchanged).
- Full tests: 233 passed.
- Frozen bytes: unchanged.

## O. Final Factory Integrity State

F-6 AUTHORIZATION:
**PASS**

F-9 FROZEN ENFORCEMENT:
**PASS**

FACTORY v1.3 INTEGRITY BLOCKERS CLOSED:
**YES**

READY FOR CHAPTER 3 PRODUCT REBUILD:
**YES**

CHAPTER 3 INTERNALLY CERTIFIED:
**NO**

## Residual limitations (honest)

- `--no-verify` is a git-native bypass of the pre-commit hook; it is closed by
  `protect_git.py` command-inspection at the shell layer. A hostile actor who
  can edit `.git/hooks` directly and run git with `--no-verify` is the host
  operator, outside this model's trust boundary.
- Owner authorization is a human out-of-band signal (no external identity
  service on a single-machine repo).
- External-audit acceptance remains a lifecycle-record boolean (build+candidate
  bound) in the gitignored evidence workspace; a fully tracked, integrity-sealed
  audit-authority record is a further F-7 completeness item, documented here.
