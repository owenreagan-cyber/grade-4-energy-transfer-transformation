# PHASE 0C — AGENT WORKFLOW VALIDATION

> Infrastructure-only validation of the specialist-agent system. No production curriculum artifacts were modified; no software installed/upgraded; no services authenticated; no commit/push.

**Summary:** repository-local subagents supported (`.cursor/agents/*.md`) · 6 specialist agents created · 6 project skills validated · Figma authenticated/available · Canva NEEDS AUTH.

---

## 1. What Works

- **Repository-local subagent format confirmed.** Cursor supports project subagents at `.cursor/agents/*.md` with YAML frontmatter (`name`, `description`, optional `model`). Project scope has higher priority than user-global (`~/.cursor/agents/`), so no global agents were needed.
- **Six specialist agents created**, each with a narrow role, tool policy, required inputs, outputs, and escalation path:
  1. `curriculum-source-reviewer`
  2. `guided-notes-specialist`
  3. `visual-art-director`
  4. `slideshow-specialist`
  5. `assessment-student-resource-specialist`
  6. `qa-certification-reviewer`
- **All six project skills validated** and mapped to owners:

| Skill | Owner agent | Verdict |
|---|---|---|
| `build-guided-notes` | Guided Notes Specialist | Sound — no defect |
| `build-slideshow` | Slideshow Specialist | Sound — no defect |
| `source-fidelity-check` | Curriculum Source Reviewer + QA Reviewer | Sound — no defect |
| `student-artifact-qa` | QA Reviewer | Sound — no defect |
| `assessment-qa` | Assessment Specialist (cross-check) + QA Reviewer | Sound — no defect |
| `certify-chapter` | QA Reviewer | Sound — no defect |

- **Non-production validation performed** (no real curriculum artifacts touched):
  - *Curriculum Source Reviewer* — stated required source files before approving any claim: authoritative Reader chapter + TG lesson page range + `VOCABULARY_PROGRESSION.md` + the artifact under review.
  - *Guided Notes Specialist* — described the notes-first workflow from an abstract dummy section: inspect Reader/TG → draft BQ → V/N anchors → blank logic → scaffold labels → model/diagram → provenance/priority tags → DOCX master.
  - *Visual Art Director* — Figma availability confirmed via `whoami` (authenticated as Owen Reagan) **without creating a file**.
  - *Slideshow Specialist* — described required anchor inputs before building: finalized BQ/V/N anchors + canonical slide sequence + accepted visual assets.
  - *Assessment Specialist* — validated a synthetic formatting example (raw score + percentage layout, separate key, matching bank with extras) unrelated to curriculum.
  - *QA Reviewer* — described the PASS/WARN/FAIL gate sequence: source fidelity → student-artifact → assessment → visual → certification; any FAIL blocks release.
- **Tool access matrix** documents per-agent tooling and correctly gates Canva (NEEDS AUTH) and grants Figma only to the Visual Art Director.

## 2. What's Missing

- A `build-teacher-playbook` skill (recommended, **not created** per instructions). The Teacher Playbook Standard exists but has no build skill yet.
- A coordinator-run smoke test that actually invokes each subagent end-to-end (deferred: safe invocation of agents is outside infrastructure-only scope and risks touching artifacts).
- Explicit per-agent `tools:` allowlists in frontmatter. The current format relies on prose tool policy rather than machine-enforced tool allowlists.

## 3. Fixes — specific problems + exact fixes

- **Problem:** `docs/agent-workflows/AGENT_ROLES.md` still described an external-AI-system role model (ChatGPT/Codex/Claude/Grok/Gemini/Qwen) that did not match the implemented architecture.
  **Fix:** Rewrote `AGENT_ROLES.md` to document the six repository-local specialist agents + the Cursor coordinator, while preserving the cross-cutting governance invariants.
- **Problem:** Canva is in `needsAuth` state but was previously listed alongside Figma as an unconditional visual tool.
  **Fix:** Gated Canva in `TOOL_ACCESS_MATRIX.md` as "Only when authenticated/approved; current state NEEDS AUTH" and mirrored this in `visual-art-director.md`.
- **Problem:** Reviewer agents produce reports (`qa/reports/`) yet are "read-only," creating ambiguity.
  **Fix:** Defined the distinction explicitly — reviewers are read-only **on the artifact under review**, and may write findings to `qa/reports/`; fixes are routed to the coordinator, never applied silently.

## 4. Enhancements / Suggestions / New Ideas

- Add a `build-teacher-playbook` skill (Phase 2 shell / Phase 12 finalization) so the playbook build has the same skill-based guardrails as notes/slides.
- Consider machine-enforced frontmatter fields (`readonly`, `tools`) once the exact Cursor subagent frontmatter schema is fully confirmed, so reviewer read-only is enforced at the harness level, not just prose.
- Optionally add a one-shot `tools/qa_agent_inventory.py` that asserts the six `.cursor/agents/*.md` files exist and each references its required standards, to make agent-inventory a repeatable QA gate.

## 5. Edge Cases & Failure Modes

- **Reviewer with fix-mode temptation:** if a reviewer silently edits, `certify-chapter` must treat it as a silent-edit violation — encoded in both `qa-certification-reviewer.md` and the `certify-chapter` skill.
- **Visual Art Director vs content:** a visual request that would change curriculum wording/answers must escalate to the coordinator, not proceed — encoded in `visual-art-director.md`.
- **Canva not authenticated:** any Canva workflow must STOP and report rather than self-authenticate — encoded in `visual-art-director.md` and the tool matrix.
- **Notes/slides divergence:** `slideshow-specialist` must STOP on BQ/V/N divergence from finalized notes.
- **Locked-decision drift:** all producers escalate rather than override frozen page counts, density (RD-6), or the locked assessment blueprint.

## 6. Performance Concerns

- None material. This phase created static Markdown definitions and documentation only; no long-lived processes, no render pipelines invoked, no servers started. The only MCP call was a read-only `whoami` for Figma availability.

## 7. Readability / Maintainability

- Each agent is a single `.md` file with consistent frontmatter (`name`, `description`, `model: inherit`) and a uniform body structure (governance → role → responsibilities → allowed tools → prohibited actions → inputs → outputs → escalation), making them easy to diff and audit.
- Agents **reference** standards rather than duplicating them, so standard changes propagate without editing six agent files.
- `AGENT_ROLES.md` and `TOOL_ACCESS_MATRIX.md` are the single sources of truth for roles and tooling; agent bodies mirror them but do not introduce divergent policy.
