# Chapter 1 — 45-Slide Refinement Matrix (Phase 5C)

**KEEP 16 · MINOR FIX 8 · MAJOR REBUILD 21 · BLOCKED 0** (total 45).
One global change applies to every slide with a 40pt title: titles render in Georgia per the Phase 5A spec (F08). On KEEP
slides this is the only change (pixel diff 0–2%, `CH1_VISUAL_QA_V2_FULL.json`).
Text, run order and speaker notes are identical to the canonical deck on all 45 slides.

| # | Role | Class | Phase 5C treatment | Photo(s) |
|---|---|---|---|---|
| 1 | Opener | MAJOR | F01 fix: measured text column + full-bleed photo region with a gold seam; full BQ visible | R01 opener |
| 2 | BQ intro | KEEP | — | — |
| 3 | BQ write | KEEP | writing slide stays minimal | — |
| 4 | Dark → bright | MAJOR | F02 fix: `before_after_compare`, matched 3.6×2.7in photos, reserved captions | R02 halves |
| 5 | Notice/wonder | KEEP | discussion slide; no photo needed | — |
| 6 | Pencil (before) | MAJOR | phenomenon-first: photo 6.2×3.75in (v1 4.4×3.3, letterboxed) | R03 before |
| 7 | Predict | KEEP | — | — |
| 8 | What changed | MAJOR | F03 fix: same constructor; 2-line AFTER caption reserved; wider CHANGES | R03 pair |
| 9 | Evidence model | KEEP | — | — |
| 10 | V1 vocab | MAJOR | photos restored **with** both mini-models (photo column beside term + definition) | R04 energy; R03 pair (change) |
| 11/12 | V1 write/check | KEEP | — | — |
| 13 | Recite | KEEP | — | — |
| 14 | Seashore | MAJOR | large seashore still + Reader text + full-width open model | R06 |
| 15 | N1 write | MINOR | geometry locked to 16; instruction frame sized (F04, F07) | — |
| 16 | N1 check | KEEP | — | — |
| 17 | Five forms | MAJOR | five matched photo cards with editable label chips below the photos | R07 alts ×5 |
| 18 | Clap | KEEP | — | — |
| 19 | N2 table | MINOR | table 12.03in wide (was 11.0), rows 0.70in (was 0.62); no CHECK slide added | — |
| 20 | V2 vocab | MAJOR | split: stretched-band photo + unchanged card and STILL → LATER → CHANGE | R08 |
| 21/22 | V2 write/check | KEEP | — | — |
| 23 | Battery predict | MAJOR | 6.3×4.6in photo (batteries inside the tube; nothing glows) | R09 alt (battery) |
| 24 | Position | MAJOR | portrait crop: whole apple held high + table far below; F05 | R09 alt (apple) |
| 25 | Stored model | MAJOR | full-width editable model; stretched band under STORED ENERGY; F06 | R08 alt (rubber) |
| 26/27 | N3 write/check | KEEP | dense table already fills the slide | — |
| 28 | Evidence | MAJOR | question card + two **unlabeled** evidence photos (lamp, shavings) | R10 panels 1–2 |
| 29 | N4 draw | MINOR | BEFORE/AFTER draw boxes widened to 11.0in | — |
| 30 | N4 write | KEEP | — | — |
| 31 | N4 sample | MINOR | SAMPLE card aligned to slide 30's card (x 1.5, w 11.0) | — |
| 32 | Application | KEEP | — | — |
| 33 | BQ return | MAJOR | synthesis: BQ card + writing lines + 4-photo "evidence wall" of the chapter's phenomena | R02, R03, R06, R08 alt |
| 34/35 | Review 1 | MINOR | list family (reflowed by the unified constructor) | — |
| 36/37 | Review 2 | MAJOR | photo family: scenario photo (before state only) + options | R03 before |
| 38/39 | Review 3 | MAJOR | grid family: navy question banner + 2×2 options | — |
| 40/41 | Review 4 | MAJOR | grid family | — |
| 42/43 | Review 5 | MINOR | list family | — |
| 44/45 | Review 6 | MAJOR | grid family (photo variant piloted, rejected: decision P-7) | — |

Constructors changed or added: `before_after_compare` (replaces `before_after_photo`), `vocab_card` (measured;
`side` photo column), `model_strip` (measured chips), `photo` / `photo_band` (cover-crop), `review_slide`
(three families; question and reveal share geometry), `text` / `rich` / `tb` (fit guard, no auto-grow, Georgia titles).
