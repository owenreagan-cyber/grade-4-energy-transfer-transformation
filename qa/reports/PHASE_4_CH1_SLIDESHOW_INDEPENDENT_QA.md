# Phase 4 — Chapter 1 Slideshow · Independent Certification Review (RE-VERIFICATION)

- **Reviewer:** QA / Certification Reviewer (READ-ONLY)
- **Date:** 2026-10-04 (re-verification of rebuilt deck)
- **Artifact under review:** `production/slides/01-ch1-energy-causes-change-slides.pptx` (+ rendered PDF + 45 PNG previews) — regenerated after fixes
- **Anchors:** Guided Notes (`production/premium-notes/01-ch1-energy-causes-change-guided-notes.{pdf,key}`), `docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md`
- **Standards:** `SLIDESHOW_STANDARD.md`, `SLIDESHOW_LOGIC_LOCKDOWN.md`, `VISUAL_DESIGN_SYSTEM.md`, `assets/visual-system/design-tokens.json`
- **Prior QA:** `qa/reports/PHASE_4_CH1_SLIDESHOW_QA.md` (20 gates, all PASS)
- **Mode:** READ-ONLY. No production artifact or repo file was modified during this review.

## Verification counts

| Check | Expected | Actual | Verdict |
|---|---|---|---|
| Slide count (PPTX) | 45 | 45 | PASS |
| Rendered PDF pages | 45 | 45 | PASS |
| PNG previews | 45 | 45 | PASS |
| Review slides range | 34–45 (6 Q + 6 A) | 34–45, 6 question + 6 answer | PASS |
| Slide dimensions | 16:9 | 13.333 × 7.5 in (960 × 540 pt) | PASS |
| Guided Notes pages | 3 (student + key) | 3 + 3 | PASS |

## Re-verification of the three prior warnings

1. **N3 notes slides 26–27 (fill-in overlap) — RESOLVED.** Table geometry compressed (model strip y=2.15 h=0.55; header y=2.85 h=0.5; 3 rows h=0.55 → table bottom ≈ 5.0 in) and fill-in moved to y=5.2. Rendered PNG analysis confirms the last row bottom border ends at ≈5.01 in and the fill-in text "Objects also have stored energy because of their ________" renders at 5.28–5.67 in — a clean ≈0.27 in gap, no overlap.

2. **Review slides 34–45 (all-A answers) — RESOLVED.** Correct letters now shuffled: Q1=A, Q2=B, Q3=C, Q4=D, Q5=B, Q6=C, confirmed in both build script (`correct` = 0/1/2/3/1/2) and rendered PDF (answer slides highlight "B … shorter and sharper", "C … stretched rubber band", "D … motion and sound", etc.).

3. **Chrome/contrast (small gold caps labels) — RESOLVED.** `VOCABULARY` (18 pt), `CHANGES` (20 pt), `CHECK YOUR THINKING` (22 pt), and `SAMPLE` (18 pt) now use NEUTRAL `#7A5620` instead of gold — contrast 5.4–6.6:1 (passes AA 4.5:1 on white/cream/gold-tint). `BIG QUESTION` bumped to 18 pt (bold gold-on-navy 3.59:1, meets WCAG large-text 3:1). Gold `#A67C16` is now reserved for the mandated iconic uses (anchor chips, model arrows, BEFORE/AFTER labels, answer highlights), each rendered bold ≥18 pt on gold (≈3.8:1, large-text compliant — by-design frozen token). Remaining chrome sizes (chapter tab 12 pt, page refs 16 pt, HUD 18 pt, kickers 20 pt) are by-design chrome below the 28 pt body floor, consistent with the prior QA gate "font floor ≥ 12 pt (chrome)" = PASS.

## OVERALL: PASS

All three previously flagged warnings are resolved; no FAIL or remaining WARN gates.

## Dimension verdicts

1. **Teacher usability — PASS.** Speaker-note block on every slide (`MODE / TIME / STUDENT RESOURCE / ASK / LISTEN FOR / REVEAL / MISCONCEPTION / NEXT`); mode badges and HUD actions make pacing legible at a glance.

2. **Projector readability — PASS.** Core text large and high-contrast (titles 40–48 pt, body 28–30 pt, vocab terms 54 pt, review options 28 pt; navy/ink on cream ≥ 11:1). Small gold labels fixed to neutral 5.4–6.6:1; gold retained only on bold ≥18 pt large-text elements (≥3:1). Chrome/caption text (12–20 pt) is by-design per frozen type scale.

3. **Visual hierarchy — PASS.** Consistent chapter tab + mode badge + HUD + anchor chip + slide title + kicker; clear model chains, cards, panels, and tables; one idea per slide.

4. **Conceptual sequencing — PASS.** Follows the canonical 9-step grammar: BQ intro → phenomenon (dark→light + pencil-sharpener observe→predict→observe→evidence) → vocab cards → vocab notes → Reader concept/model → checks → concept notes → application → return to BQ, then 12-slide end-of-chapter review. No second BQ banner (correctly routed to N2).

5. **Notes synchronization — PASS.** BQ exact wording, V1 (energy/change), V2 (stored energy), N1 (`cause · change · evidence` + ENERGY→CHANGE→EVIDENCE), N2 (5 forms), N3 (`position` + STORED ENERGY→RELEASE→CHANGE + 3 examples), N4 (BEFORE/AFTER + "What changed?" + CHECK YOUR THINKING), BQ return ("Now I Think") all mirror the Guided Notes exactly. Reveal-not-front-load; no hidden required answers on unrelated slides.

6. **Action-cue (HUD) clarity — PASS.** HUD bubbles consistent and correctly scoped (OBSERVE, PREDICT, WRITE, CHECK, EVIDENCE, TRACE, DRAW, RECITE, TURN & TALK); never used as note-navigation; BQ/V/N anchor chips remain separate and permanent.

7. **Visual quality — PASS.** Premium, spacious, non-clip-art, non-dense; palette restrained and grayscale-safe. N3 fill-in crowding resolved (clean gap).

8. **Source fidelity — PASS.** No banned advanced terms (kinetic/potential/mechanical/radiant/compression wave/inertia); "evidence" used, never "proof/prove"; no transfer vs. transformation teaching outside unit title; no invented chapter titles; Reader page refs match handoff contract (pp. 1, 1–2, 3, 4, 4–5, 1–6).

9. **Chapter-theme consistency — PASS.** Discovery/Evidence palette applied correctly: navy `#1F2A5A`, gold `#A67C16`, cream `#F5EEDC`, neutral `#7A5620`; gold now reserved for section-code chips, model arrows, BEFORE/AFTER labels, and answer highlights per frozen tokens.

10. **Review-question quality — PASS.** 6 MCQ, A/B/C/D, question-state then answer-state (34→35 … 44→45), plausible distractors, no all/none-of-the-above, no rote-only; correct letters shuffled (A/B/C/D/B/C) to remove pattern-matching.

## Blocking issues

None.

## Residual notes (non-blocking)

- Chrome/caption text (chapter tab 12 pt, page refs 16 pt, HUD 18 pt, kickers 20 pt) remains below the 28 pt slide-body floor by design (frozen type scale; prior QA "chrome ≥ 12 pt" gate = PASS). No action required.
