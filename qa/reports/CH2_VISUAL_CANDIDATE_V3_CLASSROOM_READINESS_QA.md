# Chapter 2 Visual Candidate V3 — Classroom Readiness QA

Artifact: `production/candidates/chapter-02/02-ch2-moving-objects-have-energy-visual-candidate-v3.pptx`  
Rendered artifact: `production/candidates/chapter-02/02-ch2-moving-objects-have-energy-visual-candidate-v3.pdf`

## Decision

**CLASSROOM READY: PASS**  
**GOLD / PRODUCTION CERTIFIED: NOT YET — external Grok adversarial audit, owner acceptance, and freeze/promotion remain pending.**

## Evidence summary

| Gate | Result | Evidence |
|---|---|---|
| Source and science | PASS | Reader pp. 7–12 and Teacher Guide Lesson 3 inspected; source-to-slide table covers every core concept. |
| Guided Notes parity | PASS | Exact BQ/V1/N1/V2/N2/N3/CHECK mapping; all WRITE answers hidden until CHECK slides. |
| Structure and editability | PASS | 49 slides, 16:9, integrated notes on all slides, native editable tables on slides 24–25. |
| Speaker notes | PASS | Every slide has MODE, TIME, SESSION, PLAN, STUDENT RESOURCE, READER PAGE, SAY/ASK, DO, LISTEN FOR, REVEAL, MISCONCEPTION, NEXT, IF SHORT, and MATERIALS. |
| Assessment | PASS | Quiz direction slide preserves 8 questions / 12 points / about 12 minutes; review key pattern B, B, C, D, A is exact. |
| Scope guardrails | PASS | No advanced required vocabulary, no speed–energy teaching, no Chapter 2 transfer/transformation teaching, and evidence is not framed as proof. |
| Required vs. optional | PASS | Core science is required by Thursday; optional application/review/extension content is clearly separated. Slides 42–49 visibly say OPTIONAL / NOT GRADED. |
| Technical package | PASS | First-party import, package integrity, heading-fit geometry, approved fonts, and required native-table checks passed in `.codex-build/ch2-visual-candidate-v3/candidate.validation.json`. |
| Deterministic content QA | PASS | `qa/reports/CH2_VISUAL_CANDIDATE_V3_CONTENT_QA.md`: 49 PASS, 0 FAIL. |
| Deterministic rendered QA | PASS | `qa/reports/CH2_VISUAL_CANDIDATE_V3_DETERMINISTIC_VISUAL_QA.md`: 49 PASS, 0 WARN, 0 FAIL. |

## Independent rendered-slide review

The rendered slides were reviewed from the pixels rather than trusted from builder metadata. Review sheets covered slides 1–7, 8–14, 15–21, 22–28, 29–35, 36–42, and 43–49. The review checked hierarchy, legibility, crop meaning, answer visibility, visual/source fit, classroom operation, and ambiguity.

Findings and remediation:

1. V1 slides 42–49: the optional badge touched the title. Classified FAIL and corrected in V2.
2. V2 slide 10: the punctuation after the response blank wrapped onto its own line. Classified WARN and corrected in V3.
3. V3 regression: slide 10 was inspected at full rendered size and passes. Slides 1–9 and 11–49 are byte-identical to the already reviewed V2 300-DPI PNGs; a complete `cmp` sweep showed slide 10 as the only changed render. Slides 42–43 were also spot-checked at full rendered size after the final build.

Final visual result: **49/49 PASS; no blocking ambiguity, clipping, overflow, unreadable essential text, or misleading key photograph.**

## Classroom simulation

### Wednesday

- 24 required minutes plus 6-minute buffer.
- The live marble roll occurs on required slide 7; only two marbles and a clear lane are required.
- Optional slide 6 is a replay shell, not a dependency. Optional slide 15 can be skipped.
- Students record BQ, V1, N1, and V2 before the session ends.

Result: **PASS**. Likely confusion is controlled through explicit own/outside-motion language and the repeated MOVING OBJECT → CHANGE → EVIDENCE model.

### Thursday

- 12 required instructional minutes followed by the protected 12-minute quiz, within a 24-minute required route and 6-minute buffer.
- Students complete N2, N3, CHECK, and BQ return before the quiz.
- Slides 28–29, 32–41, and 42–49 are outside the critical path.
- One reminder roll is available if students do not remember the marble change.

Result: **PASS**. The shortened-session path preserves student writing and the full quiz time.

## Artifact hashes

- PPTX: `21c5c39e2a79dd0bd33cc62a605f588579ca6fd963cd89277626dff66a564ab7`
- PDF: `51fe1a6cacaf95f515a4f98be08decad2a664bf9eb05bfc0f9507c00d0fafbb0`

No commit, push, freeze, or canonical promotion was performed.
