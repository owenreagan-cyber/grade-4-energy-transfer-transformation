# Cursor Hook Plan

Status: **not enabled**. Adapters exist and are dry-run only. `.cursor/hooks.json` is not created.

Future hooks must call the tested functions below. They must not reimplement certification rules in shell.

| Future hook | Calls | Stop condition |
|---|---|---|
| Dangerous git protection | `tools/chapter_qa/lifecycle.py` frozen registry | A command would reset, clean, or rewrite frozen chapter bytes without owner authorization. |
| Evidence invalidation | `tools/chapter_qa/invalidation.py` `propagate`, then `release_judge.judge(..., affected=that map)` | An edit touches an artifact class and existing evidence has no matching invalidation reason. |
| Candidate / source drift | `tools/chapter_qa/identity.py` `association_hash` | Working-tree hashes differ from the evidence `inputHashes` or freeze hashes. |
| Required evidence completeness | `tools/chapter_qa/completeness.py` `assess_completeness` | Expected inputs or inventory counts are missing or unequal. |
| Release Judge stop | `tools/chapter_qa/release_judge.py` `judge` | The judgment status is `FAIL`, or a mandatory gate has no accepted `PASS` evidence. |

## Constraints

- Hooks run the Python contract. Shell only locates the repo and invokes it.
- A hook must not issue `INTERNAL RELEASE CERTIFICATION` itself.
- A hook must not freeze a chapter or promote a release.
- A hook must not treat an empty input set as a pass.
- Enable a hook only after the function it calls already has a failing test for the case the hook is meant to catch.

Phase B adds evidence producers a later hook can call. Phase C exercises those producers with mutations, provenance closure, and Release Judge attacks. Hooks stay disabled. Enabling them is a later step, after this logic has stayed green.

| Later hook | Calls | Stop condition |
|---|---|---|
| Render completeness | `tools/chapter_qa/render_completeness.py` | Expected and observed render counts differ, or the render command failed. |
| PDF and OOXML | `tools/qa_pdf_quality.py`, `tools/qa_ooxml.py` | Corrupt PDF, broken package, or essential imagery below the configured DPI. |
| Status authority | `tools/qa_status_authority.py` | Current human-facing text contradicts the authoritative lifecycle status. |

No hook in Phase A, B, or C can block a commit. Frozen-chapter protection remains the non-regression run plus the rule, not a live hook.

## Phase C.1 dry-run adapters

Cursor can host project hooks in `.cursor/hooks.json` (schema version 1). Relevant events, still unused:

| Event | Future use |
|---|---|
| `beforeShellExecution` | Git protection |
| `afterFileEdit` | Evidence invalidation |
| `stop` | Certification claim on the final response |
| `beforeMCPExecution` | Role policy, after a server exists |

The adapters below are the functions those events would call. `--apply` is refused. Shell must not reimplement judge, identity, or invalidation rules.

| Adapter | Calls | Decision |
|---|---|---|
| `tools/hooks/protect_git.py` | Command classification only. Does not run git. | DENY `reset`, `clean`, `stash`, `restore`, `checkout`, and the other write verbs. DENY `commit` unless `workflowAuthorizesCommit` is boolean true. DENY `push` unless `ownerAuthorizesPush` is boolean true. ALLOW `status`, `diff`, `log`, `rev-parse`, and commands that are not git. |
| `tools/hooks/invalidate_evidence.py` | `invalidation.propagate` and `dependents` | ALLOW the edit. Return the stale gate map. An unrelated `docs/` path returns an empty map. A crash WARNs and marks every gate stale so a release cannot stay fresh. |
| `tools/hooks/validate_evidence.py` | `evidence_from_dict` and `evaluate` | A caller-supplied PASS is ignored. |
| `tools/hooks/final_release_gate.py` | `release_judge.judge`, `lifecycle.legal_transition`, `default_release_gates` | `show_failures` and `build_draft` ALLOW with no judge. `chapter_ready` requires judge PASS. Evidence is read from JSON files in the evidence directory; an inline list is ignored. `freeze_chapter` also requires `ownerAuthorizedFreeze`, a lifecycle file whose state is `APPROVED_FOR_FREEZE`, and `externalAuditAccepted`. Timeout, a missing judge, a crash, malformed input, stale evidence, the wrong build, or `failClosed` DENY the certification claim. |

Failure policy for a certification claim: DENY when the dependency is missing, the input is malformed, the judge raises, the evidence directory is absent, the evidence is stale or from another build, or the hook times out. Ordinary draft actions stay ALLOW when the action is already known, including when the judge is missing or the hook timed out.

These adapters do not edit frozen chapter files in order to enforce the policy.
