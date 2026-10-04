# PHASE 2 — TEACHER PLAYBOOK FOUNDATION REVIEW

> Phase: build + automated QA + independent review. No student curriculum artifact was modified. No commit/push.
> Artifact under review: Unit 1 Teacher Playbook (`production/teacher-playbook/unit1-teacher-playbook.docx` → `.pdf` → `previews/*.png`).
> Reviewers: Cursor Coordinator (integrator) · Curriculum Source Reviewer (independent) · QA/Certification Reviewer (independent).

---

## 1. What Works

- **Skill created.** `.cursor/skills/build-teacher-playbook/SKILL.md` defines WHEN / INPUTS / WORKFLOW / OUTPUTS / MUST-OBEY / STOP conditions for building or updating the playbook.
- **Editable-first pipeline reproduced.** `tools/build_teacher_playbook.py` (python-docx) → LibreOffice headless PDF → `pdftoppm` PNG previews. No native-PDF-only workflow, no Canva, no install/upgrade.
- **Playbook architecture implemented** per `TEACHER_PLAYBOOK_STANDARD.md`: full front matter (Cover → At a Glance → Pacing → How to Use This Unit → How Slides+Notes Work → Resource Map → Assessment & Grading → Materials → Vocabulary Map → Demo Map), reusable chapter spread template, Chapter 1 prototype spread + demo guide, answer-key architecture/index, and skeleton special sections + Ch2–7 placeholders.
- **Sample scope fully rendered** (23 pages): Cover, Unit at a Glance, Pacing Calendar, How to Use This Unit, How Slides+Notes Work, Resource/Grading Map, Master Materials, Chapter 1 spread (2-page), Chapter 1 demo guide, answer-key architecture/index. Chapters 2–7 render as placeholders, as scoped.
- **Locked content is faithful.** Exact 7 Reader titles · Big Questions verbatim · all 14 Core Vocabulary terms with correct Reader pages/chapter placement · 25Q/50pt assessment (matching Q1–8 · MC Q9–25 · no short answer/CER/fill-in) · no advanced vocabulary · no stale INB-primary or 26-item language. Confirmed by the Curriculum Source Reviewer (PASS).
- **Visual system consumed, not altered.** Frozen tokens (`design-tokens.json` v1.0) applied: `ink #1A1D26` dark-navy identity, chapter `primary` as accent tabs only, light-neutral pages, shaded-header tables, tagged callouts. `design-tokens.json` unchanged.
- **Independent reviews both PASS.** Curriculum Source Reviewer: PASS (2 WARNs, both fixed). QA/Certification Reviewer: PASS (3 WARNs, all fixed) with acceptance verdict **TEACHER GUIDANCE COMPLETE / STUDENT ARTIFACT DEPENDENCY PENDING**.

## 2. What's Missing

| Item | Status | Note |
|---|---|---|
| Chapters 2–7 teacher spreads | PLANNED | Template + placeholders rendered; populate in later phases (notes-first). |
| Ramp It Up 2.0 teacher guide (final) | PLANNED — ADAPT | Skeleton only; calibration/roles/actual-height/Design-Your-Ramp pending. |
| Pom-Pom Launcher teacher guide | PLANNED — net-new | Skeleton only; ADAPT from colleague + latex-safe note. |
| Chapter 1 guided-notes key / rebuilt notes | PLANNED | Rebuild is Phase 3/4; key not yet generated (honestly marked). |
| Consolidated per-chapter demo guides (Ch2–7) | PLANNED | Ch1 sharpener guide is the prototype; others pending. |
| Media index (populated) | PARTIAL | Ch1–2 staged · Ch3–7 scripts-only (does not block). |

None of these block the Phase 2 acceptance; all are honestly labeled `PLANNED`/`PARTIAL`, not presented as existing.

## 3. Fixes — specific problems + exact fixes

| # | Problem (found by) | Exact fix (applied) |
|---|---|---|
| 1 | Ch4 "battery circuit" listed as a co-equal core DEMO (Curriculum Source Reviewer, RD-2 conflict) | Reclassified Ch4 demo to "Balloon Drum / salt (sound transfer)"; Block-2 demo changed to "Source→Path→Receiver organizer (ACTIVITY)". Circuit = teacher enrichment only. |
| 2 | T/T/BOTH sort double-listed (Week 3 FLEX + Ch6 ACTIVITY) | Removed from Fri 10/30 FLEX; kept as the canonical Ch6 ACTIVITY. |
| 3 | "How to Use This Unit" front-matter section missing but marked RENDERED (QA Reviewer) | Added `how_to_use_this_unit()` section to the builder (30-min blocks · notes-first · BQ/V/N mirror · status vocabulary · Friday FLEX). |
| 4 | Footer text + page field at 8.5pt (below 9pt floor) | Bumped footer to 9pt. |
| 5 | Pacing table had 5 widths for 6 columns (sum 8.17" → horizontal overflow) | Corrected to 6 columns summing to 7.0" (verified: 0 tables exceed usable width). |
| 6 | QA script false-positives (page-size gate hardcoded; font floor excluded footer; naive non-linearized luminance) | Wired real `pdfinfo`/section size; font floor now includes footer; grayscale uses linearized sRGB WCAG luminance. |
| 7 | Chapter 1 Reader range "1–5" vs repo "1–6" discrepancy | Used authoritative **1–6** with p. 6 labeled as the "Energy Can Move and Change" forward preview. |

## 4. Enhancements / Suggestions / New Ideas

- **Repeat-header tables** already applied (`w:tblHeader`) so multi-page tables (vocabulary map, pacing) keep their header row on split pages — recommend keeping this for all future playbook tables.
- **Higher-DPI previews** — previews re-rendered at 110 DPI; consider 150 DPI for final visual certification in Phase 9.
- **Answer-key "mirror" generator** — the key architecture is defined; a later phase could script mirror-image keys from the student DOCX masters (same page/geometry, answers filled).
- **Pacing "split-buffer" marker** — consider a per-day "⚠ may split" tag for the assessment and Pom-Pom blocks when the 30-min timing check lands in the pilot.
- **Frozen-token lint in CI** — reuse `check_token_use()` so any future playbook edit that introduces an off-token color is caught automatically.

## 5. Edge Cases & Failure Modes

| # | Edge case / failure mode | Mitigation |
|---|---|---|
| 1 | Week 4 density (Ch6×2 + Ch7 + Pom-Pom + review + assessment in 5 days) | Reported, not compressed: PACING FLAG callout + 4 flags; RD-4 compact-cycle condition; assessment split buffer. |
| 2 | Assessment on Friday conflicts with "no new core content on Friday" | Assessed as scored summative (not new core); documented ~30–45 min with Thu/Fri split option. |
| 3 | A teacher mistakes a `PLANNED` entry for a filename | Status vocabulary + "do NOT treat as a filename" note on every placeholder. |
| 4 | Ch4/Ch5 demotion loses measured practice | Coverage trace (§N) confirms no assessment hole; organizer + practice retained. |
| 5 | Virtual sharpener video (previously failed) reused as a dependency | Explicitly marked `OPTIONAL / DEFERRED`; "must NOT be reused as a dependency." |
| 6 | 30-min feasibility unknown until pilot | Flagged as pilot item; not asserted as resolved. |
| 7 | Ch7 manifest still carries stale "26 items" language (docs only) | Playbook does not propagate it; flagged for a later doc cleanup (not a Phase 2 artifact). |

## 6. Performance Concerns

- **Render pipeline** — DOCX build ~0.4s, PDF convert ~2s, PNG previews ~1s, QA ~0.2s. All one-shot, no persistent processes, no watch mode. Compliant with resource-safety rules.
- **Table density** — vocabulary map (14×7) and pacing tables are the densest; they split cleanly with repeated headers. No clipping (verified: 0 tables > 7.0").
- **Font floors** — minimum 9pt everywhere (including footer); body 11pt; headers 12–22pt. Within premium-but-utilitarian bounds.
- **No media/network dependency** — playbook is fully local; no video, no Canva, no external fetch.

## 7. Readability / Maintainability

- **Single source of truth** — the DOCX builder is the canonical generator; the three `docs/playbook/*.md` files mirror the human-readable content. Rebuild is one command.
- **Status vocabulary is consistent** (`AVAILABLE` / `PLANNED` / `NOT REQUIRED` / `OPTIONAL/FLEX`) across the DOCX and all three markdown docs.
- **Honest dependency split** — `TEACHER GUIDANCE COMPLETE` (Ch1) vs `STUDENT ARTIFACT DEPENDENCY PENDING` (notes/slides rebuild) is stated explicitly, so the playbook is not prematurely failed.
- **Reusable chapter spread** — the blank template + the populated Ch1 spread are the two artifacts future phases copy; no per-chapter re-derivation.
- **QA is re-runnable** — `tools/qa_teacher_playbook.py` writes `qa/reports/PHASE_2_PLAYBOOK_QA.md` and gates all 8 checks.

---

### Acceptance summary

- Automated QA: **PASS** (8/8 gates).
- Curriculum Source Reviewer: **PASS** (2 WARNs fixed).
- QA/Certification Reviewer: **PASS** (3 WARNs fixed); acceptance = **TEACHER GUIDANCE COMPLETE / STUDENT ARTIFACT DEPENDENCY PENDING**.
- Teacher-usability acceptance: **PASS** — a Grade 4 teacher can teach Chapter 1 tomorrow using the playbook + Reader + planned notes/slides references, without guessing.

*Phase 3/4 readiness: READY WITH CONDITIONS — the Ch1 notes/slides rebuild (Phase 3/4) and Ramp It Up 2.0 / Pom-Pom finalization are the remaining student-artifact dependencies; the teacher-guidance foundation is complete.*
