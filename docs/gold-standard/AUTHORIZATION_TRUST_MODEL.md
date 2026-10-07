# Authorization Trust Model

F-6. This document defines what is and is not a trust source for the Chapter
Factory's authority transitions. Enforcement code must match this model; a
discrepancy is a factory defect.

## Authorities (separate)

| Authority | Meaning | Trust source | Grantable by repo write? |
|---|---|---|---|
| COMMIT AUTHORITY | Permission to create a commit | git `pre-commit` hook (frozen-byte enforcement); explicit-`git add`; no `--no-verify`/`--amend` | No — the hook is in `.git/hooks`, outside the tracked tree |
| FREEZE AUTHORITY | Permission to transition a chapter to `FROZEN` | Release Judge PASS + legal lifecycle + current evidence + external audit acceptance + owner authorization | No |
| EXTERNAL AUDIT ACCEPTANCE | The external red-team's `APPROVE PROPAGATION` for the current build | A build-bound audit-authority record, integrity-protected and matched to the exact `buildId`/candidate identity | No — old-build replay is rejected |
| OWNER AUTHORIZATION | The human owner's out-of-band approval (freeze/push) | Host-injected context (e.g. the Cursor approval card), NOT a repo file | No |
| AUTOMATED JUDGE RESULT | `INTERNAL RELEASE CERTIFICATION: PASS` | `release_judge.judge()` recomputed from disk (identity, seals, provenance) | No — evidence-only |

## Hard rule

An ordinary agent-writable repo file is **not** sufficient to create owner
authorization, external approval, or freeze authority.

Specifically, a JSON boolean such as `ownerAuthorizedFreeze=true`,
`externalAuditAccepted=true`, or `workflowAuthorizesCommit=true` is **not**
independently trustworthy merely because it exists in the repo. The previous
`qa/work/git-authorization.json` mechanism is retired: `protect_git.py` no longer
reads any agent-writable authorization file, and `_authorization_file()` returns
an empty map.

## Trust anchors

1. **`.git/hooks/pre-commit`** (installed in the host `.git` directory, not a
   tracked working-tree file). It pins the SHA-256 of `frozen_gate.py` and
   `frozen_registry.json`, then runs the frozen-byte check.
2. **`qa/gold-standard/frozen_registry.json`** — the frozen-artifact hash map,
   whose own hash is pinned in the hook.
3. **Freeze-commit baselines** — the bytes the registry hashes were computed
   from (Chapter 1 freeze, Chapter 2 freeze, combined playbook).

## What is untrusted

- `qa/work/**` (gitignored, agent-writable) — no authority.
- Any repo file containing an authorization boolean — no authority.
- Caller-supplied "current" hashes/status — recomputed by the Judge.
- `--no-verify` / `--amend` / `git add .` / `-A` / `--all` — rejected by
  `protect_git.py` (the shell gate) and never reach the hook.

## Commit enforcement model

- `git commit` (explicit message, no `--no-verify`/`--amend`) → ALLOWED by the
  shell gate; the pre-commit hook then enforces frozen bytes.
- `git add <explicit paths>` → ALLOWED; broad staging/wildcards/traversal → DENIED.
- `git push` → requires host-injected `ownerAuthorizesPush` (never a file).
- `git reset/clean/stash/restore/checkout --` → DENIED (destructive).

## Freeze prerequisites (all required)

1. Current internally-certified build (Judge PASS, recomputed).
2. Legal lifecycle state (`APPROVED_FOR_FREEZE` → `FROZEN`).
3. Current evidence hashes match disk.
4. Producer provenance valid (tracked, source-hash verified).
5. External audit acceptance for THIS build (`APPROVE PROPAGATION`).
6. Owner authorization (out-of-band, host-injected).
7. Frozen non-regression clean.
8. Release parity clean.

No single agent-authored file may satisfy (5) or (6).

## Residual limitations (honest)

- `--no-verify` is a git-native bypass of the pre-commit hook. It is closed by
  `protect_git.py` (command-inspection) at the shell layer; a hostile actor who
  can run git directly against `.git` with `--no-verify` and edit `.git/hooks`
  is outside this model's trust boundary (that is the host operator).
- Owner authorization is ultimately a human out-of-band signal; on a
  single-machine repo there is no external identity service to anchor it beyond
  the host operator.
