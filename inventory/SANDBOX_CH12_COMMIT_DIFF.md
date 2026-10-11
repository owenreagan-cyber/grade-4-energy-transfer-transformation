# SANDBOX CH12 — COMMIT DIFF

> Distinguishes HEAD-ancestry from unique branches, tags, and reflog-only history. Read-only; no mutations.

## 1. HEAD ancestry

| Ref | SHA |
|---|---|
| Main `HEAD` (`refs/heads/main`, loose) | `b7695bd364f3a56daa96604ef2c9b785a29f9492` |
| Sandbox `HEAD` (`refs/heads/main`, loose) | `5544450647525d3ddc065b045268b1af40270130` |
| Merge base | `5544450647525d3ddc065b045268b1af40270130` |

Sandbox `HEAD` == merge base ⇒ the sandbox commit graph is a strict prefix of main's.

- **Commits in main not sandbox (3):**
  ```
  b7695bd  Align Chapter 3 iPad certification inventory
  177a686  Add tracked Chapter 3 release builder
  f30838d  Establish Chapter 3 release authority
  ```
- **Commits in sandbox not main: 0.**

## 2. Branch tips (all, not only main)

Ref maps built from `packed-refs` + all loose `refs/` files in both repos, compared SHA-for-SHA:

- Identical set of 29 `feature/*` refs + 12 loose heads, **every tip SHA equal** between repos.
- Sole divergence: `refs/heads/main` — sandbox `5544450` vs main `b7695bd` (3 commits behind).
- **No sandbox-unique branch.**

## 3. Tags

None in either repository. **No sandbox-unique tag.**

## 4. Reflog-only history (all branches, not only main)

Sandbox reflogs (`logs/HEAD` + `logs/refs/heads/main` + every `logs/refs/heads/feature/*`) were fully collected:

- Unique commit SHAs present in sandbox reflogs: **210**.
- SHAs resolvable as commits in **main's** object store: **210 / 210** (the `000000…` sentinel excluded; zero missing).
- Orphaned pre-amend / reset-target commits (`571281dec…`, `e4d2fd8b…`, `9ea5d432…`) all present in main.

**No reflog-only history is unique to the sandbox.**

## 5. Summary

| Aspect | Sandbox-unique? |
|---|---|
| HEAD ancestry | No (strict prefix of main) |
| Branch tips | No (all identical except `main`, which is 3 commits behind) |
| Tags | No (none in either) |
| Reflog-only commits | No (all 210 resolve in main) |
| Unique historical commit absent from main | **None** |
