# CHAPTER FACTORY v1.3 + CHAPTER 3 EXTERNAL REMEDIATION REPORT

This report is the remediation record for the external red-team result
**DO NOT PROPAGATE YET**. It is a work-in-progress record, not release evidence.
Nothing here overrides the external result; Chapter 3 remains **NOT CERTIFIED**.

## A. Baseline
- **HEAD:** `f5f8bb6` (main)
- **Branch:** `main`
- **Initial dirty/untracked:** the accepted Chapter 3 package at `d6ef78b`,
  factory v1.2 gates at `349455c`, factory v1.0 baseline at `fffe8e5`, and 22
  untracked `tools/ch3_*.py` scripts that produced/laundered evidence.

## B. External Audit Verification
All findings classified in `docs/chapter-03/CH3_EXTERNAL_REMEDIATION_MATRIX.md`:

| Finding | Severity | Verification | Action |
|---|---|---|---|
| F-1 BuildIdentity does not cover classroom bytes | BLOCKING | VERIFIED | Fixed |
| F-2 commit clears staleness | BLOCKING | VERIFIED | Fixed |
| F-3 producers tautological/caller-fed | BLOCKING | VERIFIED | Open |
| F-4 untracked `tools/ch3_*.py` seal evidence | BLOCKING | VERIFIED | Open |
| F-5 hand-edited evidence passes | BLOCKING | VERIFIED | Fixed |
| F-6 self-grant authorization | BLOCKING | VERIFIED | Open |
| F-7 lifecycle authority untrustworthy | BLOCKING | VERIFIED | Partial |
| F-8 fail-on-abort | BLOCKING | VERIFIED | Open |
| F-9 frozen protection not in commit gate | BLOCKING | VERIFIED | Open |
| F-10 claim detection too narrow | HIGH | PARTIAL | Fixed |
| R-1 stale September release surfaces | BLOCKING | VERIFIED | Open |
| R-2 release/status self-sourced | BLOCKING | VERIFIED | Open |
| P-1 missing Reader p.15 steeper-ramp fact | HIGH | VERIFIED | Fixed (spec) |
| P-2 N2 wording + false citation | HIGH | VERIFIED | Fixed (spec) |
| P-3 BQ_NOW/RECOVER chip wrap | MEDIUM | VERIFIED | Open |
| P-4 prompt vagueness | HIGH | VERIFIED | Fixed (gate + standard) |

## C. Factory Integrity
- **Build Identity:** DONE — `BuildIdentity.candidateFiles` binds every
  classroom/release file; `recompute_mismatches` recomputes from disk.
- **Commit/Staleness:** DONE — staleness is byte-driven; a committed mutation
  still fails (`test_identity_integrity.py`).
- **Producer Independence:** OPEN — `assess_notes/slides/leakage/fresh/inventory`
  still compare caller-supplied `expected` vs `observed`.
- **Producer Provenance:** OPEN — `producerSourceHash` not yet recorded/verified.
- **Evidence Tamper Protection:** DONE — seal digest; Judge recomputes
  (`compute_evidence_seal`, `seal_valid`, `evidence_from_dict` strict).
- **Authorization:** OPEN — `qa/work/git-authorization.json` remains
  agent-writable; no `core.hooksPath` pre-commit gate yet.
- **Lifecycle:** PARTIAL — `internally_certified` now requires
  `INTERNAL_AUDIT_PENDING`; a tracked lifecycle registry is not yet built.
- **Fail-on-Abort:** OPEN — no pre-run invalidation/dedup in the sealer.
- **Frozen Protection:** PARTIAL — `PRIOR_FROZEN_NONREGRESSION` gate exists; not
  yet verified in the commit gate.
- **Claim Detection:** DONE — hyphen/punctuation normalization + pipeline terms
  (`test_claim_detection.py`).

## D. Old Untracked ch3 Tools
23 untracked `tools/ch3_*.py` files. Classification:

- **DEBUG_ONLY (cannot seal):** `ch3_*_probe.py`, `ch3_*_debug.py`,
  `ch3_*_margin.py`, `ch3_*_ink.py`, `ch3_visual_summary.py`,
  `ch3_hook_reasons.py`, `ch3_judge.py`, `ch3_slide6_pairs.py`,
  `ch3_slide_margin.py`, `ch3_text_probe.py`, `ch3_observe_sync.py`,
  `ch3_overlap_debug.py`, `ch3_n2_probe.py`, `ch3_cause_probe.py`,
  `ch3_classify_probe.py`, `ch3_find_escape.py`.
- **RETIRE (was producing evidence; must be replaced by tracked producers):**
  `ch3_emit_chapter_spec.py`, `ch3_emit_source.py`, `ch3_emit_structure.py`,
  `ch3_seal_remaining.py`, `ch3_reseal_attack.py`, `ch3_reseal_dependents.py`,
  `ch3_reseal_loop2.py`, `ch3_reseal_region.py`.

**Allowed to seal: NONE** until reimplemented as tracked, registered producers.

## E. Grade 4 Student Prompt Standard
- Rules: DONE (`docs/standards/GRADE4_STUDENT_PROMPT_STANDARD.md`).
- Gate: DONE (`STUDENT_PROMPT_CLARITY`, mandatory).
- Tests: DONE (`test_student_prompt.py` — negative + positive fixtures).

## F. Guided Lab Reasoning Standard
- DONE (`docs/standards/GUIDED_LAB_REASONING_STANDARD.md`): QUESTION→PREDICT→
  COLLECT→ORGANIZE→READ→COMPARE→NOTICE→CLAIM→EVIDENCE→REASON→EXTEND.

## G. Chapter 3 Curriculum Fixes
- Reader p.15 fact: DONE (added to `concepts` + N3 anchor).
- N2 rewrite: DONE (names ramp height cm + cup movement cm; no circular infer).
- Citations: DONE (N2 → TG Lesson 4 / AP 4.1; N3 → Reader p.15).
- No circular speed inference: DONE in spec + Playbook region.

## H. Ramp It Up 2.0
- Fair-test controls/table/average/graph/guided reasoning: **spec protocol
  present; the student-lab DOCX rebuild is NOT done.**

## I. Practice
- Prompt clarity + contexts + balance: **NOT done** (rebuild pending).

## J. Quiz
- Items/points/layout/choice labels/scoring/key PDF: **NOT done**.

## K. Recovery
- Student path + missed-lab + teacher follow-up: **NOT done**.

## L. Notes
- Pages/prompts/writing space/source refs: **spec fixed; DOCX regeneration NOT done**.

## M. Slides
- Count/visuals/sync/chips/speaker notes: **NOT done** (chip wrap + N2 sync pending).

## N. Playbook Region
- N2/N3 text fixed; full propagation-ready spread **NOT done**.

## O. Friday FLEX
- Artifact/optional status/Drop It status: **NOT done**.

## P. Release Candidate
- Exact classroom files/PDFs/internal-file exclusion/status: **NOT done**.

## Q. Provenance / Clean Room
- Closure/tracked producer paths/reproduction: **NOT done**.

## R. New Build
- buildId: **none yet**. Identity coverage/lifecycle: pending.

## S. Gates
- STUDENT_PROMPT_CLARITY added (27 gates). Full re-seal against new build: pending.

## T. Visual QA
- Pages/slides PASS/WARN/FAIL + crops: **NOT re-run**.

## U. Adversarial QA
- Generic + Ch3-aware held-out + recreated Grok classes: **NOT re-run** (bad-green=0 not yet demonstrated).

## V. Frozen Non-Regression
- Ch1/Ch2/combined playbook: **NOT re-run for this build**.

## W. Internal Reviewer
- Fresh attacks/findings/fixes: **NOT done**.

## X. Release Judge
- **NOT re-run on a new build.** Previous PASS is void.

## Y. Hook
- Claim detection done; full certification path NOT re-run.

## Z. Commits
- `afa7983` — Factory build identity + evidence integrity (F-1/F-2/F-5).
- `0128faa` — Student-prompt clarity gate + claim detection (F-10).
- `ae23c84` — Chapter 3 source fact + N2 wording.
- `f5f8bb6` — Internal certification requires audit-pending lifecycle (F-7).
- push: **NONE** · tag: **NONE**.

## AA. Remaining Findings
- **BLOCKER:** F-3 (producer independence), F-4 (provenance), F-6 (authorization),
  F-8 (fail-on-abort), F-9 (frozen commit-gate).
- **HIGH:** R-1, R-2, product rebuild (lab/practice/quiz/recovery/notes/slides/FLEX).
- **MEDIUM:** P-3 chip wrap.

## AB. Final Decision
- **FACTORY v1.3 INTEGRITY REPAIR: FAIL** (F-3/F-4/F-6/F-8/F-9 remain).
- **GRADE 4 STUDENT PROMPT STANDARD ACTIVE: YES**.
- **CHAPTER 3 INTERNALLY CERTIFIED: NO**.
- **READY FOR EXTERNAL RED-TEAM AUDIT: NO**.
- **RELEASE PROPAGATED: NO**.
- **FROZEN: NO**.
- **PUSHED: NO**.
