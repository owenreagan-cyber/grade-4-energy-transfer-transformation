# Phase 6.1 — Chapter 1 Classroom-Time Simulation

Derived from `tools/ch1_pacing.py` (single source). 30-minute block; transition loss modelled at 4 min; buffer = 30 − required.

| Session | Opening/BQ | Demo | Reader | Write | Talk | Check | Quiz | Required | Transition loss (4) | Slack |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Mon | 3 | 5 | 7 | 6 | 2 | 1.5 | 0 | 24.5 | 4 | 1.5 |
| 2 Tue | 1 | 0 | 8 | 10 | 4 | 1.5 | 0 | 24.5 | 4 | 1.5 |
| 3 Fri | 0.5 | 0 | 2 | 8.5 | 0 | 1 | 13 | 25 | 4 | 1 |

**Result:** every session retains ≥ 1 min of slack after a 4-minute transition loss, and ≥ 5 min of planned buffer before it. v1.0 planned ≈ 30 min for slides 1–12 alone and ≈ 59 min for slides 13–33 (impossible); v1.1 is feasible.

## Stress tests

| Scenario | Effect | Plan response |
|---|---|---|
| Session 1 starts 3 min late (assembly) | 21.5 min available vs 24.5 planned | Cut 3 min: skip slide 13, merge 6–7 (saves 1.5); if N1 write has not started by minute 24 move slides 15–16 to Session 2 opener (buffer 5.5) |
| Class slow on writing (+30%) | S1 +1.8, S2 +3, S3 +2.5 min | within 5 min buffer; Session 3 sends CHECK/BQ home before cutting the quiz |
| Friday loses 5 min before the quiz | N4 ends at minute 11 (6 + 5) | skip slides 30–31 (CHECK → home / catch-up), BQ NOW I THINK after the quiz or at home; quiz still starts by minute 12 and ends by 25 |
| Friday short period (25 min) | quiz cannot share the block with N4/CHECK/BQ | N4 stays in class; CHECK and BQ become take-home / catch-up; quiz starts at minute 12 at the latest |
| Quiz run in a separate FLEX slot | S3 drops to 12 min | acceptable: S3 retains full instruction; the quiz slot just moves |
| Student absent Mon | misses notes p. 1 | recovery doc; they join Session 2 with p. 1 completed from a partner/teacher key |
