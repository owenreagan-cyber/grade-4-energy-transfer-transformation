# PHASE 7 — CHAPTER 2 EXTERNAL ADVERSARIAL AUDIT (stopgap)

> **Gate status: NOT SATISFIED AS EXTERNAL.** The designated external reviewer (Grok) is not reachable from this environment (no MCP namespace, no API key, no CLI, no agent definition, no `~/.cursor/mcp.json` entry). This report is an **internal adversarial audit run by the integrator as a stopgap** — it is NOT the required independent external review, and it does not by itself clear the external gate.

> Read-only. No production file was modified during this audit.

## Verdict: APPROVE WITH FIXES → all 4 findings remediated (2026-10-04); external (Grok) sign-off still pending

> The 4 blocking findings (F1–F4) were independently verified by the integrator and remediated (see "Remediation status" below). The only outstanding gate item is the **designated external (Grok) review**, which was not reachable from this environment and must still be completed for the external gate to formally pass.

## Falsification attempt results

### FAIL-level findings (blocking)

**F1 — Scored work lacks a score/percent line (AGENTS.md violation).**
- `production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx` (scored, formative) has header `Name / Date` with **no `Score: _____ / 12 = ______ %` line**.
- Also violates the locked GLOBAL PRINT HEADER STANDARD (`Name / HR 4A 4B 4C 4D`, no `Date` field).
- Systematic: Ch1 quiz/practice share the same `Name / Date` header (pre-existing Phase 5 artifact, listed in the Phase 13X normalization backlog). Still a defect in Ch2 scope.

**F2 — Teacher-facing schedule contradiction for Chapter 2.**
- Authoritative `docs/playbook/UNIT1_PACING_CALENDAR.md` + Phase 7 playbook → Chapter 2 is **Week 1** (Wed 10/14 · Thu 10/15).
- `curriculum/chapter-02/CHAPTER_MANIFEST.md`, `README.md`, `teacher/02-ch2-moving-objects-have-energy-teacher-map.md`, `teacher/02-ch2-daily-lessons.md` → all claim **Week 2**.
- Moving Marbles day differs by file: "Thursday" (`02-ch2-moving-marbles-student.docx`, `-teacher-spec.md`), "Tuesday" (`02-ch2-daily-lessons.md`, `02-ch2-friday-flex.md` "Tuesday's page"), "Friday FLEX" (playbook pacing).

**F3 — Moving Marbles status conflict.**
- `production/labs/02-ch2-moving-marbles-teacher-spec.md` tags it **CORE · Lab 2 of the 8-lab backbone · Week 1 (Thu)**.
- Phase 7 manifest + playbook reclassify it **OPTIONAL/FLEX**. The spec was not updated to match.

**F4 — Stale duplicate canonical tree with conflicting "RELEASED" claim.**
- `curriculum/chapter-02/qa/acceptance-report.md` still claims **"RELEASED"**, "22 slides legible", Week 2 — conflicting with the Phase 7 package (37 slides, Week 1). The INB-era `curriculum/chapter-02/` tree is neither archived nor marked superseded in-place.

### WARN-level findings (non-blocking, but should be reconciled)

- **W1** `production/releases/chapter-02/` holds stale exports (2-page notes PDF, 4-page key PDF, retired `…-interactive-science-notebook.pdf`) — non-canonical; candidate for archive (already documented).
- **W2** Quiz blueprint claims "NO speed/fast-slow" but Q1b ("how fast something goes") and Q2d ("evidence of speed") are speed-adjacent distractors. Correct answers are never speed-based, so distractors are defensible; the blueprint wording is imprecise.
- **W3** Old `curriculum/chapter-02/source-map.md` describes Reader p.7 motion as "position, speed, direction" — reader-faithful but a potential Ch3-leak confusion in a source map.

### PASS (falsification attempted, held)

- Big Question verbatim; vocab (`motion`, `energy of motion`) verbatim; Reader pp. 7–12.
- Notes ↔ slides sync: all BQ/V/N anchors, MOVING OBJECT→CHANGE→EVIDENCE, BEFORE/AFTER, N3 hammer/pendulum/wind table mirrored; reveal-not-frontload.
- Answer correctness: quiz 8 items, practice Parts A–E, Moving Marbles key — verified against Reader p. 7–12 + TG L3.
- Quiz key total now **12 points** (1+1+2+1+2+2+2+1); blueprint balance tally (50/37.5/12.5%) consistent.
- No banned/stale terminology in production artifacts (only guardrail/exclusion mentions).
- No Ch3 speed-energy or advanced vocab in notes/slides; grayscale/font/geometry/overflow previously PASS and re-confirmed.

## Required next steps (for the gate to actually pass)

1. Obtain the designated external reviewer (Grok) — provide access (MCP/API key) or run Grok externally and return its findings for integrator verification.
2. Fix F1 (add score line + standard header to Ch2 quiz, or scope to the documented normalization pass with explicit approval).
3. Resolve F2/F3/F4 (retire/archive or mark-superseded the old `curriculum/chapter-02/` tree; align Moving Marbles spec tag; reconcile Week 1 vs Week 2).
4. Re-run affected QA and obtain a final external or independent certification before freeze.

## Remediation status (integrator, 2026-10-04)

| # | Finding | Action | Verified |
|---|---|---|---|
| F1 | Quiz missing score line | Added `Score: ______ / 12 = ______ %` to `production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx` | DOCX opens clean; LibreOffice round-trip 2 pp ✓ |
| F2 | Schedule/day conflict | `02-ch2-moving-marbles-student.docx` → "Week 1 · Friday FLEX · OPTIONAL"; `02-ch2-friday-flex.md` "Tuesday's page" → student-file ref | ✓ |
| F3 | Moving Marbles CORE vs FLEX | Teacher-spec retagged OPTIONAL/FLEX (formerly Lab 2; RECLASSIFIED Phase 7), "Week 1 (Friday FLEX)", rationale added | ✓ |
| F4 | Stale `curriculum/chapter-02/` tree | 7 retired files marked SUPERSEDED in place (document-only per policy); KEEP files untouched | ✓ |

**Outstanding:** the designated external (Grok) review itself. The `Name/Date` header on the quiz (no `HR 4A 4B 4C 4D`) remains a cross-chapter systematic item documented in the Phase 13X normalization backlog — not fixed in this phase to avoid Ch1/Ch2 header inconsistency.
