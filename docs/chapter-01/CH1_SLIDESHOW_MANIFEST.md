# CHAPTER 1 — SLIDESHOW MANIFEST (Phase 4, FINAL · updated Phase 6.1)

> Canonical instructional slideshow for Chapter 1 "Energy Causes Change".
> Built notes-first from the finalized Guided Notes (Phase 3). Supersedes all legacy Chapter 1 slide artifacts.

## Canonical files

| Artifact | Path |
|---|---|
| Editable master (PPTX) | `production/slides/01-ch1-energy-causes-change-slides.pptx` |
| Rendered PDF | `production/slides/01-ch1-energy-causes-change-slides.pdf` |
| PNG previews (45) | `production/slides/previews/ch1-slides-*.png` |
| Builder (canonical pipeline) | `tools/build_ch1_slides.py` |
| Automated QA | `tools/qa_ch1_slides.py` → `qa/reports/PHASE_6_1_CH1_SLIDESHOW_QA.md` (historical: `PHASE_4_CH1_SLIDESHOW_QA.md`) |

- **Slide count:** 45 (16:9, 13.333" × 7.5").
- **Theme:** DISCOVERY / EVIDENCE — primary `#1F2A5A` · accent `#A67C16` · surface `#F5EEDC` · neutral `#7A5620`.
- **Font:** Avenir Next. Chrome ≥ 12 pt · body ≥ 28 pt · vocab term ≥ 48 pt.

## Slide map (Phase 6.1 — matches `tools/ch1_pacing.py`)

Timing authority: `docs/chapter-01/CH1_PACING_PLAN.md`. Sessions: **S1 Mon** slides 1–3, 6–16 (24.5 min) · **S2 Tue** slide 2 re-entry, then 17, 19–27 (24.5 min; **slide 18 OPTIONAL**) · **S3 Fri** slide 2 re-entry, then 28–31, 33 + quiz (25 min). Optional: 4, 5, 18, 32, 34–45. No session opens on a reveal slide. **Friday fallback:** quiz handed out no later than minute 12; priority N4 > BQ NOW I THINK > CHECK (see the pacing plan).

| Slide(s) | Session | Anchor / purpose | Detail |
|---|---|---|---|
| 1 | S1 | Title | Chapter 1 · Energy Causes Change (neutral subtitle; exact BQ lives on slide 2) |
| 2 | S1 (re-entry S2, S3) | **BQ** | Big Question banner + TURN & TALK |
| 3 | S1 | **BQ** · My first thinking | notes write |
| 4–5 | S1 (optional) | Phenomenon · Notice & Wonder | light-switch change (Reader p. 1) · I notice / I wonder |
| 6–9 | S1 | Demo | sharpener — observe (6) · predict (7) · run + BEFORE/AFTER (8) · changes are clues, "?" box open (9) |
| 10 | S1 | **V1** cards | energy + change |
| 11–12 | S1 | **V1** notes | write (11) · reveal (12) — change · different |
| 13–14 | S1 | **N1** concept | what is energy (13) · Reader p. 2 seashore + ENERGY → CHANGE → ? (14) |
| 15–16 | S1 | **N1** notes | write (15, one blank; model's last box stays empty) · reveal evidence + full model, students copy the word into the last box (16) |
| 17 | S2 | **N2** | five forms (only motion modeled) |
| 18 | S2 (optional) | clap check | forms |
| 19 | S2 | **N2** notes | write 5 examples (no pre-filled answers) |
| 20 | S2 | **V2** card | stored energy |
| 21–22 | S2 | **V2** notes | write (21) · reveal (22) — later |
| 23–25 | S2 | **N3** concept | still battery predict — a real prediction, no answer on screen (23) · position (24) · STORED → RELEASE → CHANGE + Reader p. 4 battery fact (25) |
| 26–27 | S2 | **N3** notes | write (26) · reveal position + samples (27) |
| 28 | S3 | **N4** concept | recognizing evidence (clues) |
| 29 | S3 | **N4** notes | BEFORE / AFTER draw + "What changed?" |
| 30–31 | S3 | CHECK YOUR THINKING | write (30) · sample reveal (31) |
| 32 | S3 (optional) | Application | which change shows energy at work? |
| 33 | S3 | **BQ** · NOW I THINK | return, notes write |
| 34–45 | optional | End-of-chapter review | 6 × multiple-choice (A/B/C/D), question (even) + answer (odd) |

## BQ / V / N anchor slide numbers

| Anchor | Slide(s) |
|---|---|
| BQ | 2 · 3 · 33 |
| V1 (energy · change) | 10 · 11 · 12 |
| V2 (stored energy) | 20 · 21 · 22 |
| N1 Energy Causes Change | 13 · 14 · 15 · 16 |
| N2 Energy Occurs in Different Forms | 17 · 18 · 19 |
| N3 Objects Can Store Energy | 23 · 24 · 25 · 26 · 27 |
| N4 Recognizing Evidence | 28 · 29 · 30 · 31 |

## Demo slide numbers

- 4 (light switch, optional) · 6 (observe) · 7 (predict) · 8 (run + what changed) · 9 (changes are clues).

## Review slides

- **Range:** 34–45 (6 question slides + 6 answer slides). Optional — review day / FLEX only.
- **Correct letters:** Q1=C · Q2=A · Q3=D · Q4=B · Q5=A · Q6=C (not patterned; gate-checked).

## Reader page ranges

| Anchor | Reader |
|---|---|
| BQ | p. 1 |
| V1 | p. 1 |
| N1 | pp. 1–2 |
| N2 | p. 3 |
| V2 | p. 4 |
| N3 | pp. 4–5 |
| N4 | pp. 1–5 (core; p. 6 is a teacher-facing forward preview only and is not cited) |

## Visual assets

All visuals are programmatically generated (no external raster assets): model chains (ENERGY → CHANGE → EVIDENCE; STORED → RELEASE → CHANGE), BEFORE/AFTER boxes, full-screen vocabulary cards, five-form cards, and the N2/N3 tables.

- Custom diagrams created: 2 model chains + BEFORE/AFTER component + vocabulary-card component + 5-form card row.

## Optional / FLEX slides

- Slides 4–5, 18, 32 and 34–45 are optional (see slide map); the other slides are required. The virtual sharpener video is **OPTIONAL / DEFERRED** and is **not** a dependency.
