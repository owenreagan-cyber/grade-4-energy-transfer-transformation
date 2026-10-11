# SANDBOX CH12 — FINAL DIFFERENCE & RECOVERY AUDIT

> Independent, from-scratch reproduction (2026-10-10). Both repositories were re-walked **live** and every file
> SHA-256 hashed directly — the prior inventory files were treated as preliminary and not trusted for the counts below.
> No sandbox file was modified, deleted, moved, reset, merged, rebased, committed, or pushed. No content was copied.

## Release decision

**`SUPERSEDED_SANDBOX_WITH_RECOVERABLE_HISTORY`**

The sandbox is a superseded file-level copy of main, frozen at commit `5544450`. Every unique valuable item is
accounted for and recoverable — specifically, **there are none**: main is a strict superset of the sandbox at the
commit, branch, tag, reflog, and content-hash levels. The only sandbox-unique bytes are a generated Xcode
`.xcresult` test bundle (reproducible, disposable). **No deletion or archiving is authorized.** No recovery action
is required because nothing in the sandbox is missing from main.

---

## 1. Inventory-file verification

Present in `inventory/` (sizes/line counts re-verified):

| File | Exists | Notes |
|---|---|---|
| `main_repo_sha256_for_sandbox_compare.txt` | ✅ 48,973 lines | prior main hash snapshot |
| `sandbox_ch12_sha256.txt` | ✅ 21,981 lines | prior sandbox hash snapshot |
| `sandbox_ch12_git_status.txt` | ✅ | prior git-status snapshot |
| `sandbox_ch12_untracked.txt` | ✅ 34 lines | prior untracked snapshot |
| `sandbox_ch12_ignored.txt` | ✅ 20,622 lines | prior ignored snapshot |

These prior snapshots were **not** used for the decisive numbers below; the comparison was recomputed directly from
the live filesystem.

## 2. Independent recomputation (fresh full-tree hash)

Method: `os.walk` both repos, skip `.git` only, SHA-256 every file, normalize to relative paths.

| Metric | Fresh value |
|---|---|
| Sandbox files (excl. `.git`) | 22,165 |
| Main files (excl. `.git`) | 49,220 |
| Same path, same bytes | 21,533 |
| Same path, different bytes | 50 |
| **Sandbox-only paths** | **582** |
| Main-only paths | 27,637 |
| **Sandbox-only content hashes** | **548** |
| Sandbox same-hash-different-path | 34 |
| Frozen registry (both repos) | **42 / 42 match** |

## 3. The 582 sandbox-only paths — classified (requirement 3)

All 582 are under `qa/temp/ipad-artifact-qa/result.xcresult/` — a single Xcode test-result bundle. Classification
by defensible file families (extension/role), **not** assumed disposable by directory alone:

| Family | Count | Evidence |
|---|---|---|
| `Data/data.0~<opaque>` diagnostic blobs | ~343 | opaque Xcode diagnostic payloads |
| `Data/refs.0~<opaque>` empty placeholders | ~30 | hash `6e340b9c…` (empty refs placeholder) |
| `.ips` crash reports | 166 | simulator crash reports |
| `.log` / `.txt` logs | 27 | simulator/dyld logs (several empty → `e3b0c442…`) |
| `.tracev3` traces | 5 | Instruments traces |
| `.csstoredump`, `.timesync`, `.plist`, `.jsonl` | 6 | simulator runtime state |

**Disposability evidence (not assumption):** (a) `.xcresult` is machine-generated `xcodebuild test` output with
per-run random blob names — every run rewrites it; (b) the **meaningful** iPad evidence — the Xcode project +
Swift sources (`qa/ipad-artifact-qa/ScienceArtifactQA*`), `manifests/ch3-current.json`, and the per-run
`screenshots/` + `blind-review/` captures — is present in **both** repos (identical or main-newer); (c) main
additionally holds 4 *later* iPad run dirs (`ipad-qa-20261008-180046 … 180304`) plus `qa/temp/ipad_views/` that the
sandbox lacks. The sandbox's iPad record is strictly *older/less complete* than main's.

## 4. Same-path different-hash files (requirement 5) — 50 total

- **30 content** (full list + hashes in the CSV): all are Chapter-3 (curriculum, `production/releases/chapter-03`,
  `production/slides/03-ch3…`, `production/final-delivery/Energy/…` Ch3 symlinks), the 3 docs edited in main's
  working tree, `PRODUCTION_MANIFEST.md`, `RELEASE_HASH_MANIFEST.csv`, `qa/ipad-artifact-qa/manifests/ch3-current.json`,
  and 5 `tools/` + 1 `tests/` file. In **every** case the sandbox holds the **older** byte content and main the newer.
- **15 render** (`qa/work/_f3final`, `qa/work/_v13`, `qa/temp/…/current-run.json`) — QA-adversary scratch, git-ignored.
- **5 cache** (`__pycache__/*.pyc`) — bytecode, git-ignored.

## 5. Same-content / different-path (requirement 6)

- **Sandbox-only content hash: 548** (of 582) — none of these 548 hashes appears anywhere in main; all are
  `result.xcresult` bundle blobs (see §3).
- **Sandbox same-hash-different-path: 34** — the remaining 34 sandbox-only files are byte-identical to main content
  under different names: empty `refs.0~*` placeholders and empty `.log`/`.txt` files (hashes `e3b0c442…` = SHA-256 of
  empty string, and `6e340b9c…` = empty refs placeholder). Zero unique content.

## 6. Git relationship (requirement 7–9)

- `.git` = directory; `git-dir == git-common-dir == .git`; no `worktrees/`; no `objects/info/alternates`; no remote
  ⇒ **file-level copy, not a linked worktree, not a shared/independent clone.**
- HEAD: sandbox `5544450` == merge base; main `b7695bd` (3 commits ahead: `f30838d`, `177a686`, `b7695bd`).
- **Branches:** every branch tip SHA identical between repos except `refs/heads/main` (sandbox 3 behind). No unique branch.
- **Tags:** none in either repo.
- **Reflog:** all **210** unique commit SHAs across **all** sandbox reflogs (HEAD + main + every `feature/*`) resolve
  as commits in main's object store (0 missing, sentinel excluded). Orphaned amend/reset targets present in main.
- **Unique historical commit or artifact absent from main: NONE.**

## 7. Frozen & accepted resources (requirement 10)

`qa/gold-standard/frozen_registry.json` → **42/42 paths byte-identical in both repos.** The frozen Ch.1 v1.1 and
Ch.2 v1.0 classroom bytes, combined playbook, and all gate/registry JSON are unchanged in both. Accepted candidate
manifests and release manifests are likewise identical or main-newer.

## 8. Unresolved differences

None. (The prior "copy provenance mechanism" note is non-blocking and does not affect classification.) The single
non-content residue — the 582-file `.xcresult` bundle — is fully characterized as generated and reproducible.

## 9. Recovery actions required before any future archive

**None required** — every item is `ALREADY_RECOVERED` or `GENERATED_REPRODUCIBLE`. If the owner later authorizes
archiving (not authorized here), the only optional step would be preserving the historical `.xcresult` bundle
outside the curriculum repo **if** the raw iPad run-result is wanted for the record; no instructional content would
be lost either way.
