# Release Lifecycle

The machine table is `tools/chapter_qa/lifecycle.py`. A lifecycle state is not a gate status.

## States

`BUILD_IN_PROGRESS`
`BUILT_UNCERTIFIED`
`INTERNAL_AUDIT_PENDING`
`INTERNAL_AUDIT_FAILED`
`INTERNALLY_CERTIFIED`
`EXTERNAL_AUDIT_PENDING`
`EXTERNAL_AUDIT_REJECTED`
`APPROVED_FOR_FREEZE`
`FROZEN`

## Legal transitions

| From | To |
|---|---|
| `BUILD_IN_PROGRESS` | `BUILT_UNCERTIFIED` |
| `BUILT_UNCERTIFIED` | `INTERNAL_AUDIT_PENDING`, `BUILD_IN_PROGRESS` |
| `INTERNAL_AUDIT_PENDING` | `INTERNALLY_CERTIFIED`, `INTERNAL_AUDIT_FAILED` |
| `INTERNAL_AUDIT_FAILED` | `BUILD_IN_PROGRESS` |
| `INTERNALLY_CERTIFIED` | `EXTERNAL_AUDIT_PENDING` |
| `EXTERNAL_AUDIT_PENDING` | `APPROVED_FOR_FREEZE`, `EXTERNAL_AUDIT_REJECTED` |
| `EXTERNAL_AUDIT_REJECTED` | `BUILD_IN_PROGRESS` |
| `APPROVED_FOR_FREEZE` | `FROZEN` |

`FROZEN` has no outbound transition in this factory. Reopening a frozen chapter is an owner decision under `.cursor/rules/80-frozen-chapter-protection.mdc`, not a normal edge.

`compare_frozen_bytes` reports a hash that changed. The owner-authorization flag does not look at bytes. A future hook must call the byte compare. This phase does not enable that hook.

## Forbidden

`BUILT_UNCERTIFIED` must not go to `FROZEN`.

No state other than `APPROVED_FOR_FREEZE` may enter `FROZEN`.

`PASS` is not a lifecycle state. Internal certification is a Release Judge result. It is recorded while the lifecycle is in an audit state. It does not itself move the chapter to `FROZEN`.
