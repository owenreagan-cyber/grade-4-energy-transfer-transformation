# Phase 6.1 — Chapter 1 External-Audit Remediation

## 1. What Works
- One generated pacing authority (`tools/ch1_pacing.py`) drives speaker notes, `CH1_PACING_PLAN.md`, and QA; three sessions (24.5 / 24.5 / 25 min) each keep ≥ 5 min buffer.
- Release package is rebuilt from canonical masters with a SHA-256 manifest; `qa_release_parity.py` (negative-tested) passes.
- Deterministic visual QA (`qa_visual_pdf.py`) passes for notes, key, practice, quiz, Detectives, 45 slides, Playbook pp. 1–21, and both derived release PDFs: 0 FAIL, 0 WARN in scope.
- Stale-reference scan covers 27 active scopes with 0 hits.
- Unit 1 Visual System v1.0, the locked Unit 1 final assessment, and Chapters 3–7 are untouched; the v1.0 certification is preserved.

## 2. What's Missing
- External Grok audit result (`APPROVE PROPAGATION`) — not obtainable autonomously; packet and prompt are ready (`GROK_CH1_V1_1_AUDIT_PACKET.md`, `GROK_CH1_V1_1_AUDIT_PROMPT.md`).
- (Resolved) Friday placement: owner policy of 2026-10-04 allows Friday synthesis and the graded quiz, never first exposure; Ch1 is compliant and gated.
- Chapter 2 Playbook rows still use "Model It · Draw/Label" (Ch2 scope; Phase 7).
- Real-classroom timing is simulated, not observed.

## 3. Fixes — specific problems + exact fixes
- **F1/R1 schedules:** replace S1–S9 / S12–S23 / Thu Detectives / Fri FLEX in `MASTER_CURRICULUM_MAP`, `MASTER_RESOURCE_INDEX`, `ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING`, `MASTER_RESOURCE_INVENTORY`, `FRIDAY_FLEX_BANK`, `ENERGY_UNIT_WEEK_BY_WEEK_TEACHER_MAP`, video matrix with the three-session plan; add 7 stale patterns to `qa_ch1_stale_refs.py`.
- **F2/F3/R2 assessments:** quiz Q9 statements → flag waved / desk is brown / music got louder (YES/NO/YES), listed in the key; new gates for Q9 non-reuse and key listing; practice key labels bell/ice as EXTENSION.
- **F7/R6 slides:** slide 25 and 28 prompts rewritten as questions; slide 23 kicker, slide 4 caption, slide 13 citation, review Q4 stem, slide 17 prompt, review answer box width; gate patterns added.
- **F6/R12 space:** N4 "What changed?" has 2 rules (notes, slide 29); practice rows 660/680; Detectives Part B on page 2 with 640-twip rows; Detectives "After:" added (page count held at 2).
- **F4/R10 release:** release builder sanitizes derived PDFs (no repo paths, phase labels, or calendar dates); FLEX source note reworded; P11 marked RETIRED.
- **R3 inventory:** four review docs created; `qa_phase_inventory.py` fails on ghost entries.
- **R4:** owner Friday policy recorded; `AGENTS.md`, rule 00, FRIDAY_FLEX_FRAMEWORK, spec G16 updated; `check_plan()` now fails if a required Friday slide lacks Session 1/2 traceability.

## 4. Enhancements / Suggestions / New Ideas
- Generalize `build_ch1_release.py` / `qa_release_parity.py` to `--chapter N` for propagation.
- Add a per-chapter "schedule-doc registry" so the stale scan reads its file list from one place.
- Add a Q9-style duplication gate for every chapter's quiz vs practice.
- Observe one real session to calibrate the simulation's minute costs.

## 5. Edge Cases & Failure Modes
- If slide 15 has not started by minute 24 of Session 1, N1 write/reveal moves to Session 2, which then has 2.5 min buffer (skip slide 18 to recover).
- Absent on quiz day → make up at the next FLEX window (quiz key policy: teacher-chosen open/closed note).
- Table rows that grow can silently push a Detectives/practice page to 3 pages; the page-count and footer-only-page gates catch it.
- Playbook `_page_break` change also affects Ch2 pages (layout only); Ch2 QA must be re-run in Phase 7.
- A derived release PDF built on a machine without LibreOffice fails loudly (no partial release).

## 6. Performance Concerns
- Full rebuild (notes, slides, 3 assessments, Playbook, release) with PDF export and previews takes ~1 min; every export uses a throw-away LibreOffice profile and exits.
- No watchers or servers are used; all QA is one-shot and headless.

## 7. Readability / Maintainability
- Builders and QA tools take `--report` so reruns do not overwrite another phase's report (a rerun that did overwrite `PHASE_4_CH1_SLIDESHOW_QA.md` was restored from git).
- Gate expectations live next to the builders (`EXPECTED_RULED_LINE_GROUPS`, `QUIZ_POINTS`); the key's ruled-line expectation is documented (sample answer replaces one rule).
- Governance: `docs/agent-workflows/PHASE_PIPELINE.md`, `docs/planning/QA_GATES.md` gates 9–13, and propagation spec section G capture the lessons.
