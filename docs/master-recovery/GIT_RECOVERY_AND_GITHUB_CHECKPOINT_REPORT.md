# GIT RECOVERY & GITHUB CHECKPOINT REPORT

> Read-only checkpoint. No remote configured, no commit/push performed. Full sandbox audit:
> `inventory/SANDBOX_CH12_AUDIT.md`, `inventory/SANDBOX_CH12_COMMIT_DIFF.md`, `inventory/SANDBOX_CH12_UNIQUE_FILES.csv`.

## Current Git state (verified 2026-10-10)

| Item | Value |
|---|---|
| Root | `/Users/owen/Projects/grade-4-energy-transfer-transformation` |
| Branch | `main` @ `b7695bd364f3a56daa96604ef2c9b785a29f9492` |
| Commits | 211 |
| Remote | **none** |
| Tracked files | 1,517 |
| Working tree | 5 modified + 95 untracked (nothing staged) |
| Tags | none |
| Frozen registry | 42/42 byte-identical |
| Object store | 3,641 objects, 0 missing |
| git-lfs | **not installed** |

## Sandbox relationship (definitive)
`…-sandbox-ch12` is a **file-level copy** of main frozen at `5544450` (main is 3 commits ahead). Classification:
**SUPERSEDED_SANDBOX_WITH_RECOVERABLE_HISTORY** — zero unique commits, branches, tags, reflog commits, or content
hashes. **Do not delete**; no wholesale merge needed; nothing requires recovery.

## Historical refs preserved (branch inventory)
All 29 `feature/*` packed refs + `main` + 12 loose heads are present and identical between main and sandbox
(except `main`, 3 commits behind in sandbox). Examples of the historical branch surface: `feature/chapter-01-prototype`
… `feature/chapter-07-unit-final`, `feature/final-classroom-package`, `feature/media-supplemental-intake`,
`feature/interactive-notebook-alignment`, `feature/premium-guided-notes-slide-outlines`, `feature/phase13a`…`phase13z`,
`phase13aa`…`phase13ac`, `phase13s`…`phase13x3`. **Backup must include all of these**, not just `main`.

## Media strategy (required before media enters Git)
1.3 GB git-excluded library in `assets/supplemental/media/` (48 videos). Options:
- **Git LFS** (install + `git lfs track 'assets/supplemental/media/**'`, plus a frozen SHA-256 sidecar manifest), or
- **External object storage** (immutable bucket) with `assets/supplemental/media/MEDIA_MANIFEST.sha256` committed as the
  source of truth; Drive/S3 URLs referenced in the repo.
Either requires owner authorization. **No media should be committed to GitHub directly.**

## Intended destination
- No remote configured. `gh` CLI authenticated as **`owenreagan-cyber`** (scopes `repo`, `workflow`, `gist`).
- Owner must name the **PRIVATE** repository. Note account mismatch risk: the Drive target account is
  `owen.reagan@thalesacademy.org`; the GitHub CLI is signed in as a different identity — confirm before push.

## Proposed commit plan (STOP — not executed, awaiting owner authorization)
Review branch `recovery/reconcile-2026-10-10` (do **not** overwrite `main`):

1. **Stage A — docs/standards/QA evidence:** the 5 modified tracked files
   (`CH1_PACKAGE_MANIFEST.md`, `MEDIA_VIDEO_WORKFLOW.md`, `DIAGRAM_AND_MEDIA_STANDARD.md`, `tools/hooks/mcp_policy.py`,
   `tools/hooks/protect_git.py`) + 3 untracked standards/recovery docs + `docs/master-recovery/*` + `qa/reports/*` +
   `inventory/SANDBOX_CH12_*`.
2. **Stage B — generators/scripts:** the ~57 `tools/*.py` + `tools/render-pdf.js` + `package*.json` + `.cursor/commands/`.
3. **Stage C — source intake/registries:** `source-intake/`, `docs/build-prompts/`, `docs/chapter-02/CH2_MEDIA_SHORTLIST…`.
4. **Deferred (owner decision):** large binaries (`assets/ch1|ch2/`, storyboard PNG, `production/candidates/`,
   `production/classroom-ready/`, `previews/`, `.codex-build/`), `qa/ipad-artifact-qa/` Xcode project, and **all 1.3 GB media**.

No merge into `main`, no remote config, no push until destination + exact scope are owner-approved.

## Secret & privacy
Clean: no `.env`, credentials, service-account, client-secret, private keys, or API-key material in tracked or
content files.
