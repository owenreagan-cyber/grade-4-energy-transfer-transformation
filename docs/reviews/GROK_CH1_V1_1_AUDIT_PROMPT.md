# Prompt for the External Grok Re-Audit (Chapter 1 v1.1 candidate)

You are an independent, adversarial, **READ-ONLY** auditor. Do not edit, create, or delete any file. Do not run builds.

Audit the repository `grade-4-energy-transfer-transformation` using `docs/reviews/GROK_CH1_V1_1_AUDIT_PACKET.md` as the entry point.

Tasks:
1. For each of your findings F1–F14, open the cited files and decide RESOLVED / PARTIALLY RESOLVED / NOT RESOLVED. Do not accept the response document on trust.
2. Walk every row of `qa/reports/PHASE_6_1_ARTIFACT_INVENTORY.md`; confirm each created/modified/affected artifact exists and is consistent with the single pacing plan (`docs/chapter-01/CH1_PACING_PLAN.md`).
3. Check, against the authoritative CKSci sources, the Reader page references, vocabulary wording, and that no advanced vocabulary is required.
4. Rule on the open items R4, R8, R11 (see the packet).
5. Look for anything the internal reviewers missed (stale schedules, pre-answered notes on slides, key/page mismatches, space/readability, release parity).

Output format (exactly):
- A table: finding → verdict → evidence (file:line) → required fix (if any).
- A list of NEW findings with severity (HIGH/MEDIUM/LOW).
- Final line, **exactly one** of:
  - `APPROVE PROPAGATION`
  - `REJECT — <number> blocking findings` followed by the blocking list.

Any wording other than the exact line `APPROVE PROPAGATION` counts as a rejection.
