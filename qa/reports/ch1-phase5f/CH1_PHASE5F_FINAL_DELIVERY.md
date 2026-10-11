# Chapter 1 — Final Production Delivery & Readiness (Phase 5F)

> Candidate `ch1-premium-hybrid-v4` (final production priority correction, owner directive 2026-10-10).
> Deadline context: Monday, Oct 12, 2026.

## 1. Final candidate

| Field | Value |
|---|---|
| Build ID | `ch1-premium-hybrid-v4` |
| Candidate dir | `production/candidates/chapter-01/ch1-premium-hybrid-v4/` |
| Editable PPTX | `01-ch1-energy-causes-change-premium-hybrid-v4.pptx` (45 slides, 16.7 MB) |
| PDF backup | `01-ch1-energy-causes-change-premium-hybrid-v4.pdf` (45 pages) |
| Previews | `previews/slide-01..45.png` |
| Contact sheet | `contact-sheet.png` |
| Builder | `tools/build_ch1_premium_v4.py` |
| PPTX SHA-256 | `1f85244f69ba8cb5df1a2fff935b1a9f7da6d635745485c7fc13f7184ae730b0` |
| PDF SHA-256 | `6c54d7d2d7c2f12c8dfe11367a488d0b64989bf877d15119a400f62b4636f399` |

## 2. Pencil decision — resolved (bounded correction)

Per the owner directive, no further cycles were spent chasing a perfect pencil photograph. The contradictory `pen_before` photograph (a pointed "before" contradicting the canonical "dull/flat tip" wording) was **removed from all five slides (6, 8, 10, 36, 37)** and reverted to the **canonical editable diagram**:

- Slide 6 → drawn `BEFORE` panel ("A dull pencil — tip is flat, and it is quiet.").
- Slide 8 → drawn two-panel `BEFORE / AFTER` + CHANGES card (dull tip · quiet → shorter · sharper · humming).
- Slide 10 (change card) → drawn `BEFORE → AFTER` mini-model (no photo).
- Slides 36–37 (review 2) → canonical single-column text MCQ (answer comes from the taught change, not an image).
- Slide 33 keeps only the **sharpened** `pen_after` thumbnail in the evidence wall (scientifically correct).

The live **dull-vs-sharpened pencil demonstration** is the intended classroom fallback (already in the canonical speaker notes: "live demo"). Exact canonical wording preserved throughout (parity PASS).

## 3. Instructional integrity (verified)

| Check | Result |
|---|---|
| 45 canonical slides | PASS |
| 45/45 text parity vs frozen canonical | PASS |
| 45/45 speaker-notes parity | PASS |
| Answer reveal letters | `C · A · D · B · A · C` |
| BQ/V/N anchors + order | PASS |
| Guided Notes + teacher-key alignment | PASS (BQ/V/N mirror; reveal = key) |
| 28-gate structural QA | OVERALL PASS |
| No transfer/transformation leakage | PASS |
| No answer leakage | PASS |

## 4. Visual / technical (verified)

| Check | Result |
|---|---|
| Rendered-layout QA v2 | 44 PASS / 1 WARN / 0 FAIL (WARN = pre-existing slide-2 "BQ" chip) |
| Rendered geometry | 0 out-of-bounds / 0 overlap / 0 empty pages |
| Fonts | Avenir Next + Georgia embedded (font-faithful isolated render) |
| 16:9 widescreen metadata | PASS |
| No external links / valid PPTX | PASS |
| Original Phase 5C critical fixes (1, 4, 8) | still fixed (no recurrence) |

## 5. Phase 5D fixes retained (carried into v4)

- Slide 20 — pre-teaching stored-energy photo removed (concept-first). ✓
- Slide 24 — apple crop keeps hand + table (height cue). ✓
- Slide 27 — N3 sample answers darkened. ✓

## 6. Remaining issues (honest)

1. **Projector-distance WARNs** (slides 17, 19, 26, 44, 45) — subjective back-of-room readability. Instructional floor is already 24 pt; the independent review itself did not establish physical projector readability. **Not a science/instruction defect.**
2. **Two cosmetic WARNs** — slide 2 "BQ" chip inside the 0.30″ edge band; the `→` glyph uses a LibreOffice fallback font (renders correctly; not in Avenir Next/Georgia). Both pre-existing and non-blocking.
3. **Independent human visual audit** — a builder inspecting its own renders is not a fully independent audit; this remains outstanding for the Gold gate.

## 7. Classroom Ready assessment

**CLASSROOM READY (pending independent visual sign-off).** The complete, source-verified, notes-aligned, correctly-sequenced 45-slide package exists; pacing is practical (Mon 24.5 · Tue 24.5 · Fri 25.0 min); all reveals match the key; no contradictory imagery remains; editable PPTX + PDF backup + previews + contact sheet are produced. The only item requiring a human before classroom use is a back-of-room readability spot-check of five dense slides.

## 8. Gold certification status

**NOT GOLD CERTIFIED.** Gold requires independent multimodal review, external adversarial audit, reproducible-build attestation, and release acceptance — which a builder agent cannot self-issue (rules 30/40/50/60). This phase delivers the candidate and QA evidence; Gold is a separate certification process.

## 9. Final deliverable checklist

| Deliverable | Status |
|---|---|
| Editable 45-slide PPTX | ✓ `…-hybrid-v4.pptx` |
| PDF backup | ✓ `…-hybrid-v4.pdf` |
| Guided Notes student packet | ✓ frozen `production/premium-notes/01-ch1-…-guided-notes.{docx,pdf}` |
| Teacher key | ✓ frozen `…-guided-notes-key.{docx,pdf}` |
| Teacher notes + pacing guide | ✓ `docs/chapter-01/CH1_PACING_PLAN.md` + `production/teacher-playbook/…` + per-slide speaker notes |
| Approved supporting media | ✓ Ch1 media staged (scripts; videos optional, non-essential) |
| Classroom materials checklist | see §10 |
| Monday/Tuesday/Friday routes | ✓ single pacing plan (`tools/ch1_pacing.py`) |
| QA evidence | ✓ `qa/reports/ch1-phase5c/`, `…/ch1-phase5d/`, `…/ch1-phase5f/` |
| Classroom Ready assessment | ✓ (above) |
| Gold status | NOT GOLD (honest) |
| Remaining issues | ✓ (above) |

## 10. Classroom materials checklist

- Projected deck: `…-hybrid-v4.pptx` (or PDF backup).
- Guided Notes: one per student (`01-ch1-…-guided-notes.pdf`).
- Teacher key: `01-ch1-…-guided-notes-key.pdf`.
- Pacing: `CH1_PACING_PLAN.md` (Mon/Tue/Fri, incl. Friday quiz-by-minute-12 clock).
- Demos: electric pencil sharpener + dull/sharpened pencil (live); light switch; flashlight/battery; stretched rubber band (optional); raised apple (optional).
- Quiz (Fri): `production/quizzes/01-ch1-…-quiz.pdf` + key.

## 11. Repository protection (verified)

Frozen canonical deck, Guided Notes, teacher key, Phase 5B (v1) / 5C (v2) / 5D (v3) candidates, and accepted releases are all unchanged. Nothing staged/committed/pushed/promoted. Headless rendering only; no visible-desktop automation. (Pre-existing `soffice` PID 4624 predates this session.)

## 12. Next recommended action

1. Independent rendered-slide visual review of v4 (45 slides) — sign off Classroom Ready.
2. Then proceed to the full Gold certification process (external audit, reproducible-build attestation, release acceptance) if Gold is required before the Oct 12 deadline.
3. **Do not promote, commit, or push without explicit owner approval.**
