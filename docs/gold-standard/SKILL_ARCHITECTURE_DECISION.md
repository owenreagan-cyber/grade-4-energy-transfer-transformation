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

## Phase B

Evidence producers now exist, so four thin skills were added under `.cursor/skills/`. Each one calls a script and forbids assigning PASS. No second skill tree was created. No visual-QA agent was added: `qa-certification-reviewer` emits render, visual, PDF, and OOXML evidence in read-only mode. `visual-art-director` stays the producer and does not certify visual QA.

| Skill | Decision | Why |
|---|---|---|
| `source-scholar` | IMPLEMENT | Emits source and curriculum evidence. `source-fidelity-check` remains the older prose workflow. |
| `cross-artifact-auditor` | IMPLEMENT | Compares artifact classes and refuses source-authority claims. |
| `visual-qa-auditor` | IMPLEMENT | Runs render completeness and rendered inspection. |
| `pdf-ooxml-forensics` | IMPLEMENT | Runs PDF tools and OOXML structure. |
| Adversary skill | DEFER | Full mutation architecture is Phase C. |
| Provenance skill | DEFER | Clean-room rebuild is still later. |
| Release-judge skill | UNNEEDED | The judge remains a tested function. |
| Parallel `.agents/skills` copies | UNNEEDED | Skills stay in `.cursor/skills/`. |

## Rule

Add a skill only when it contributes a reusable workflow or a deterministic tool beyond the current agent prompt. Do not add a skill that repeats a rule file.
