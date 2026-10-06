# Skill Architecture Decision

Phase A does not create a parallel `.agents/skills` tree.

Existing reusable workflows already live in `.cursor/skills/`. They are Markdown workflow skills. They are not Python detectors.

## What exists

| Skill | What it is | Decision |
|---|---|---|
| `source-fidelity-check` | Workflow for Reader/TG fidelity. Referenced by `curriculum-source-reviewer`. | REUSE |
| `student-artifact-qa` | Workflow for student-artifact QA. Referenced by `qa-certification-reviewer`. | REUSE |
| `assessment-qa` | Workflow for assessment QA. Referenced by the assessment specialist and the certification reviewer. | REUSE |
| `certify-chapter` | Prose checklist. It collects gate evidence and does not set `RELEASED` or issue release certification. Binding it to `judge()` stays deferred. | DEFER |
| `build-guided-notes` | Builder workflow for notes. | REUSE |
| `build-slideshow` | Builder workflow for slides. | REUSE |
| `build-teacher-playbook` | Builder workflow for the playbook. | REUSE |

`certify-chapter` collects gate evidence and stops before manifests or a release status. Chapter Factory release certification is `tools/chapter_qa/release_judge.py`. Binding that skill to the judge stays deferred so this phase does not create a second certification procedure.

## Not added

| Candidate | Decision | Why |
|---|---|---|
| Visual-detector skill | DEFER | The detector suite is out of scope. A skill with no detector would only restate `VISUAL_QA_AUDITOR`. |
| Provenance skill | DEFER | `provenance-auditor` plus `identity.py` is enough until a clean-room rebuild engine exists. |
| Adversary skill | DEFER | `qa-adversary` is the workflow. A mutation runner is out of scope. |
| Release-judge skill | UNNEEDED | The judge is a tested Python function. An agent prompt already points at it. |
| Parallel `.agents/skills` copies | UNNEEDED | They would duplicate `.cursor/skills/` and `.cursor/agents/`. |

## Rule

Add a skill only when it contributes a reusable workflow or a deterministic tool beyond the current agent prompt. Do not add a skill that repeats a rule file.
