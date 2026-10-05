# PHASE PIPELINE (mandatory for every chapter/phase from Phase 6.1 on)

> Every future phase inherits this pipeline. Skipping a step means the phase is **not complete**.

```
BUILD
  → deterministic QA            (tools/qa_*.py — notes, slides, assessments, playbook, visual system)
  → internal specialist review  (curriculum-source-reviewer, qa-certification-reviewer; read-only)
  → visual QA                   (tools/qa_visual_pdf.py + rendered inspection of EVERY affected student/teacher/projected artifact; PASS/WARN/FAIL)
  → phase artifact inventory    (qa/reports/PHASE_<n>_ARTIFACT_INVENTORY.md; tools/qa_phase_inventory.py must PASS)
  → external Grok adversarial audit   (Grok is READ-ONLY; result must be exactly "APPROVE PROPAGATION")
  → verified remediation        (independently verify each finding: VERIFIED / PARTIALLY VERIFIED / NOT VERIFIED; fix only substantiated defects)
  → final QA                    (full deterministic re-run + release parity + stale-reference scan)
  → freeze                      (version bump; preserve prior freeze history)
  → commit                      (ONLY when the user explicitly asks)
```

## Completion rule

**No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
The phase inventory is the audit's checklist; the packet sent to the external auditor must list every inventory row.

## Roles
- Cursor Coordinator = integrator and the only role that edits artifacts in fix mode.
- Reviewer agents (curriculum-source-reviewer, qa-certification-reviewer, visual-art-director) are read-only on the artifact they certify; to fix, switch to fix mode explicitly and re-run the review.
- Grok = external adversarial auditor, READ-ONLY. Gemini = source-fidelity tie-breaker only.

## Status vocabulary during remediation
`UNIT1_CHn_GOLD_STANDARD_VERSION = <current frozen version>` and `STATUS = CORRECTIVE MAINTENANCE IN PROGRESS` until the external audit returns "APPROVE PROPAGATION" and final QA passes. Then bump the version and set `STATUS = FROZEN`. Never delete or rewrite the previous certification.

## Reusable tools
| Purpose | Tool |
|---|---|
| Chapter pacing single source / simulation | `tools/ch1_pacing.py` (pattern: one module per chapter) |
| Rendered geometry, blank/clipped/overlap/small-text | `tools/qa_visual_pdf.py`, `tools/qa_render_geometry.py` |
| Canonical ↔ release parity | `tools/qa_release_parity.py --chapter N` |
| Stale-reference scan (target 0) | `tools/qa_ch1_stale_refs.py` (copy per chapter) |
| Phase inventory completeness | `tools/qa_phase_inventory.py` |
| PDF/preview export (isolated LibreOffice profile) | `tools/export_pdf_previews.py` |
