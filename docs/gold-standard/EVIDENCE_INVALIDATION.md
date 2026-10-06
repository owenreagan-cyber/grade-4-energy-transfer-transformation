# Evidence Invalidation

An evidence record that carries an applicable invalidation reason cannot certify a new candidate.

Implementation: `tools/chapter_qa/invalidation.py`.

## Reasons

| Reason | When it applies |
|---|---|
| `SOURCE_CHANGED` | Authoritative Reader/TG bytes changed. |
| `CANDIDATE_CHANGED` | The candidate artifact named by the gate changed. |
| `FREEZE_CHANGED` | The freeze identity changed. |
| `EXPECTED_INVENTORY_CHANGED` | A chapter config changed an expected count. |
| `AUDITOR_VERSION_CHANGED` | The auditor contract that produced the record changed. |
| `GATE_VERSION_CHANGED` | `gateVersion` on the definition changed. |
| `TOOL_VERSION_CHANGED` | A recorded tool version differs from the current tool version. |
| `DEPENDENCY_CHANGED` | An upstream gate this gate depends on was invalidated. |

## Propagation

Direct gates receive the caller's reason. Gates that depend on those gates, directly or further downstream, receive `DEPENDENCY_CHANGED`. Gates that are not downstream stay valid.

Artifact classes and the gates that read them:

| Artifact | Direct gates |
|---|---|
| `authoritative-source` | `SOURCE_AUTHORITY` |
| `notes` | `NOTES_STRUCTURE` |
| `slides` | `SLIDES_STRUCTURE` |
| `assessment` | `ASSESSMENT_ALIGNMENT` |
| `schedule` | `SCHEDULE_POLICY` |
| `playbook` | `PLAYBOOK_ALIGNMENT` |
| `release` | `FRESH_EXPORT`, `RELEASE_EXACT_SET`, `RELEASE_PARITY` |
| `inventory` | `INVENTORY` |
| `freeze` | `PRIOR_FROZEN_NONREGRESSION`, `POST_FREEZE_GOLDEN` |

### Notes example

A notes source change marks `NOTES_STRUCTURE` with the caller's reason.

Downstream, the dependency graph then marks:

- `NOTES_SLIDES_SYNC`
- `ANSWER_LEAKAGE`
- `RENDER_COMPLETENESS`
- `RENDERED_VISUAL_QA`
- `PDF_QUALITY`
- `FRESH_EXPORT`
- `RELEASE_PARITY`

Those downstream records get `DEPENDENCY_CHANGED`.

The same notes change does not mark `SOURCE_AUTHORITY`, `SLIDES_STRUCTURE`, `SCHEDULE_POLICY`, or `PLAYBOOK_ALIGNMENT`.

After a rebuild, the new candidate has a new association hash (`buildId`, path, freeze ids, and content hashes). Evidence still bound to the previous hash cannot certify the new build. That is candidate identity, not a second copy of the notes rule.

## What does not happen

A change to notes does not invalidate an unrelated gate. A stale record is rejected. It is not accepted as current-build evidence.

`judge(..., affected=propagate(...))` applies that map itself. Evidence for a listed gate is stale even when the record's `invalidationReasons` is empty. Omitting `affected` does not scan the worktree. The caller is declaring that no change map applies. The planned hook must pass the map.
