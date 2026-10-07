# Chapter Factory v1.0 Acceptance

Accepted baseline commit: `c637615afdc9dbcb157949e978dc250dad682534`

Chapter Factory v1.0 = **ACCEPTED FOR CHAPTER 3 PRODUCTION**

This acceptance does not generate Chapter 3 classroom artifacts. It records the factory that those artifacts must pass.

## Accepted capabilities

- Permanent project rules
- Common certification language
- Common evidence contract
- Immutable gate semantics
- Build and candidate identity
- Auditor independence
- Expected-versus-observed completeness
- Evidence invalidation
- Release Judge
- Release lifecycle
- Source and curriculum auditing
- Cross-artifact auditing
- Render completeness
- Rendered visual QA
- 300 DPI render standard
- 600 DPI suspicious-region evidence
- PDF quality and DPI
- OOXML forensics
- Status and version authority
- Adversarial mutation runner
- Held-out mutations
- Provenance
- Clean-room reproduction
- Release-promotion safety
- Hard Cursor hooks
- Controlled staging and commit authorization
- Mandatory producer registry
- Frozen-chapter non-regression

## State at acceptance

| Check | State |
|---|---|
| Hard Cursor enforcement | Active |
| Mandatory gates | Each has a registered producer |
| Clean rehearsal Release Judge | PASS |
| Post-commit rehearsal | PASS |
| Defective rehearsal | Judge FAIL and stop hook DENY |
| MCP tooling | NONE |
| Chapter 1 | `UNIT1_CH1_GOLD_STANDARD_VERSION` 1.1, FROZEN |
| Chapter 2 | `UNIT1_CH2_GOLD_STANDARD_VERSION` 1.0, FROZEN |

Chapter 3 may be called `INTERNALLY_CERTIFIED` only when the Release Judge returns PASS for the current build and the hooks allow that claim. Builder prose is not evidence.

Known non-blocking limits are in `docs/gold-standard/FUTURE_IMPROVEMENTS.md`. They are not part of this acceptance work.
