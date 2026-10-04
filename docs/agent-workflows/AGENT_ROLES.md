# AGENT ROLES

> Division of labor across the unit's specialist agents. Governance only — no curriculum decisions.

## Implemented architecture

Specialist agents are repository-local Cursor subagents defined in `.cursor/agents/*.md`. Each inherits root `AGENTS.md`, obeys `.cursor/rules/`, references `docs/standards/` (never duplicates them), and has a narrow role, tool policy, required inputs, outputs, and escalation path.

Tool access is governed by `docs/agent-workflows/TOOL_ACCESS_MATRIX.md`.

| Agent (`.cursor/agents/`) | Role | Default mode | Primary skills |
|---|---|---|---|
| `curriculum-source-reviewer` | Verify fidelity against authoritative CKSci Reader + TG | READ-ONLY | `source-fidelity-check` |
| `guided-notes-specialist` | Build premium guided notes (primary student artifact) | Produce | `build-guided-notes` |
| `visual-art-director` | Own visual-system execution + visual assets | Produce | — (Figma MCP + image tooling) |
| `slideshow-specialist` | Build premium slides around finalized notes | Produce | `build-slideshow` |
| `assessment-student-resource-specialist` | Own worksheets, labs, practice, tests, keys, scoring | Produce | `assessment-qa` (as QA cross-check) |
| `qa-certification-reviewer` | Independent final reviewer (PASS/WARN/FAIL) | READ-ONLY (fix mode explicit) | `source-fidelity-check`, `student-artifact-qa`, `assessment-qa`, `certify-chapter` |

## Coordinator
- **Cursor = canonical production integrator.** Only Cursor merges production work, owns release packaging, and records QA/manifest state.
- Coordinator dispatches specialist agents, receives escalation, and applies fixes the reviewers only report.

## Cross-cutting rules
- Reviewer agents (`curriculum-source-reviewer`, `qa-certification-reviewer`) **do not silently modify** the artifact they are reviewing; they switch to fix mode explicitly or route fixes to the coordinator.
- Only **Cursor** merges production work to `main`.
- All agents respect root `AGENTS.md`, `.cursor/rules/`, and `docs/standards/`.
- No commit or push unless explicitly requested. No Git remote.

## Escalation
- Any agent that hits a STOP/failure condition reports to the coordinator instead of improvising a fix outside its role.
- Conflicts with locked decisions (`docs/planning/CURRENT_DECISIONS.md`, `docs/planning/QA_GATES.md`, `docs/assessment/UNIT1_FINAL_ASSESSMENT_BLUEPRINT.md`) are escalated, never overridden silently.
