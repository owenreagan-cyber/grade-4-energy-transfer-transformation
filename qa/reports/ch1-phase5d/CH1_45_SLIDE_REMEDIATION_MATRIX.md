# CH1 45-Slide Remediation Matrix (Phase 5D)

> One record per canonical slide. 5C status from the independent review; Phase 5D disposition + remedy.

| Slide | 5C | Issue | Root cause | Selected remedy | Final status | Evidence |
|---|---|---|---|---|---|---|
| 1 | PASS | — | — | KEEP | KEEP | — |
| 2 | PASS | corner tag cosmetic | — | KEEP | KEEP | — |
| 3 | PASS | — | — | KEEP | KEEP | — |
| 4 | PASS | — | — | KEEP | KEEP | — |
| 5 | PASS | — | — | KEEP | KEEP | — |
| 6 | FAIL | BEFORE pencil pointed | R03 before-half reads sharp | BLOCKED — new asset proposal | BLOCKED | pencil report |
| 7 | PASS | — | — | KEEP | KEEP | — |
| 8 | FAIL | BEFORE contradicts 'dull' | same R03 | BLOCKED | BLOCKED | pencil report |
| 9 | PASS | — | — | KEEP | KEEP | — |
| 10 | WARN | BEFORE/AFTER misleading | same R03 | BLOCKED | BLOCKED | pencil report |
| 11 | PASS | — | — | KEEP | KEEP | — |
| 12 | PASS | — | — | KEEP | KEEP | — |
| 13 | PASS | — | — | KEEP | KEEP | — |
| 14 | PASS | — | — | KEEP | KEEP | — |
| 15 | PASS | — | — | KEEP | KEEP | — |
| 16 | PASS | — | — | KEEP | KEEP | — |
| 17 | WARN | category tags small | 24pt chip labels | projector validation | VISUAL_REVIEW_REQUIRED | projector report |
| 18 | PASS | — | — | KEEP | KEEP | — |
| 19 | WARN | N2 rows small | 24pt/22pt table | projector validation | VISUAL_REVIEW_REQUIRED | projector report |
| 20 | WARN | photo preteaches example | stored_hero photo | remove photo; concept-first card | FIXED | stored-energy report |
| 21 | PASS | — | — | KEEP | KEEP | — |
| 22 | PASS | — | — | KEEP | KEEP | — |
| 23 | PASS | — | — | KEEP | KEEP | — |
| 24 | WARN | apple height unclear | top-aligned crop dropped table | lower crop focus (0.5,0.55) | FIXED | raised-object report |
| 25 | PASS | — | — | KEEP | KEEP | — |
| 26 | WARN | N3 WRITE dense | 24pt/20pt table | projector validation | VISUAL_REVIEW_REQUIRED | projector report |
| 27 | WARN | N3 answers light | NEUTRAL ink low contrast | darken answer ink to INK | FIXED | projector report |
| 28 | PASS | — | — | KEEP | KEEP | — |
| 29 | PASS | — | — | KEEP | KEEP | — |
| 30 | PASS | — | — | KEEP | KEEP | — |
| 31 | PASS | — | — | KEEP | KEEP | — |
| 32 | PASS | — | — | KEEP | KEEP | — |
| 33 | PASS | — | — | KEEP | KEEP | — |
| 34 | PASS | — | — | KEEP | KEEP | — |
| 35 | PASS | — | — | KEEP | KEEP | — |
| 36 | WARN | review 2 BEFORE 'dull' | same R03 | BLOCKED | BLOCKED | pencil report |
| 37 | WARN | review 2 answer repeats | same R03 | BLOCKED | BLOCKED | pencil report |
| 38 | PASS | — | — | KEEP | KEEP | — |
| 39 | PASS | — | — | KEEP | KEEP | — |
| 40 | PASS | — | — | KEEP | KEEP | — |
| 41 | PASS | — | — | KEEP | KEEP | — |
| 42 | PASS | — | — | KEEP | KEEP | — |
| 43 | PASS | — | — | KEEP | KEEP | — |
| 44 | WARN | review 6 choice C small | 28pt option, multi-line | projector validation | VISUAL_REVIEW_REQUIRED | projector report |
| 45 | WARN | review 6 answer C density | same | projector validation | VISUAL_REVIEW_REQUIRED | projector report |

## Machine-readable register

A JSON mirror is written at `qa/reports/ch1-phase5d/CH1_45_SLIDE_REMEDIATION_REGISTER.json`.

## Constructor/asset touch summary

- `build_ch1_premium_v3.py` slide 20: removed `photo("stored_hero", …)`, vocab card full-width (12.23").
- `build_ch1_premium_v3.py` slide 24: apple crop focus `(0.5, 0.0)` → `(0.5, 0.55)`.
- `build_ch1_premium_v3.py` slide 27: N3 answer ink `NEUTRAL` → `INK`.
- Pencil slides (6, 8, 10, 36, 37): unchanged; blocked pending owner asset decision.
