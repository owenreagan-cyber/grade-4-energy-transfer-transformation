# BRANCH & WORKTREE POLICY

> Isolation rules for parallel production agents. Governance only.

## Canonical integration
- **Only one canonical integrator (Cursor) merges production work.** No other agent merges to `main`.

## Parallel work
- Parallel agents work in **isolated branches** (`feature/<scope>`) or isolated worktrees.
- No Git remote; do not push.

## Reviewer isolation
- **Reviewer agents do not edit the branch they are certifying** unless explicitly switched into fix mode.
- Fixes on a certified branch go through the integrator, not the reviewer.

## Process
- Prefer one-shot commands; no watch-mode runners; no duplicate servers.
- No commit or push unless explicitly requested.
- See `docs/planning/GIT_STRATEGY.md` and `docs/technical/REPOSITORY_POLICY.md` for tracked/excluded paths.
