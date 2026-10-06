# Cursor Hook Plan

Status: **not enabled**. Phase A does not create hook files, `hooks.json`, or a blocking git hook.

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

Phase B adds evidence producers a later hook can call. Hooks stay disabled until those producers and the Phase C adversary both pass.

| Later hook | Calls | Stop condition |
|---|---|---|
| Render completeness | `tools/chapter_qa/render_completeness.py` | Expected and observed render counts differ, or the render command failed. |
| PDF and OOXML | `tools/qa_pdf_quality.py`, `tools/qa_ooxml.py` | Corrupt PDF, broken package, or essential imagery below the configured DPI. |
| Status authority | `tools/qa_status_authority.py` | Current human-facing text contradicts the authoritative lifecycle status. |

No hook in this phase can block a commit. Frozen-chapter protection remains the non-regression run plus the rule, not a live hook.
