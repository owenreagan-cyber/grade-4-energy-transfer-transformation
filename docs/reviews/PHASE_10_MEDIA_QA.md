# PHASE 10 — FINAL MEDIA QA

> Validates every reviewed video against staging and the MAJOR-FAIL policy. Ch.3–7 = scripts only (no files to QA).

## Chapter 1 (8 videos)

| Video | Playable? | Correct chapter? | Correct role? | Major fail? | Staging sensible? | Duplicates a CORE? | Runtime OK? | Overload risk? |
|---|---|---|---|---|---|---|---|---|
| Invisible Boss of Change | PASS | Yes | Yes | No | Yes (CORE Mon) | No | 2:50 ✓ | low |
| The Energy Detective | PASS | Yes | Yes | No | Yes (CORE Mon) | Overlaps #1 theme | 6:45 ✓ | Mon w/ #1 = WARN |
| Stored Energy | PASS | Yes | Yes | No | Yes (CORE Wed) | No | 4:37 ✓ | low |
| Energy Detectives Briefing | PASS | Yes | Yes | No | Yes (SUPPORT Tue) | No | 7:53 ✓ | low (optional) |
| Chapter 1 Science Notebook | PASS | Yes | Yes | No | Yes (SUPPORT) | No | 8:26 ✓ | low (optional) |
| How Scientists Spot Invisible Energy | PASS | Yes | Yes | No | Yes (FLEX) | No | 1:16 ✓ | none |
| Why Still Objects Secretly Have Energy | PASS | Yes | Yes | No | Yes (FLEX) | No | 1:16 ✓ | none |
| Chapter 1 Review | PASS | Yes | Yes | No | Yes (SUPPORT/FLEX) | No | 7:17 ✓ | low (optional) |

## Chapter 2 (4 videos)

| Video | Playable? | Correct chapter? | Correct role? | Major fail? | Staging sensible? | Duplicates a CORE? | Runtime OK? | Overload risk? |
|---|---|---|---|---|---|---|---|---|
| Things on the Move | PASS | Yes (Ch.2, NOT Ch.1) | Yes (hook) | No | Yes (SUPPORT) | Overlaps #2 | 7:21 ✓ | low (optional) |
| Moving Objects Have Energy | PASS | Yes | Yes (core explainer) | No | Yes (CORE) | Overlaps #1 | 4:50 ✓ | low |
| Marble Collisions: Investigating Motion Energy | PASS | Yes | Yes (lab preview) | No | Yes (CORE Tue) | No | 5:59 ✓ | low |
| Chapter 2 Interactive Notebook | PASS | Yes (Ch.2, NOT Ch.3) | Yes (notebook) | No | Yes (SUPPORT) | No | 6:42 ✓ | low (optional) |

## Policy adherence
- No MAJOR FAIL. All videos already accepted under the MAJOR-FAIL policy (minor wording ≠ regenerate).
- `ch-3.mp4` correctly reclassified → `Chapter_2_Interactive_Notebook.mp4` (Chapter 2, not 3). SHA-256 byte-verified.
- Ch.1/Ch.2 remain UNSTAGED in the manifest but are now concretely mapped (day/tier) in `WHOLE_UNIT_MEDIA_STAGING.md`.

## Verdict
- **PASS.** 12/12 videos playable, correctly chaptered/rolled, no major fails, sensible staging, one flagged overlap pair each chapter (resolved: SUPPORT is optional). Ch.3–7 correctly marked PENDING GENERATION (not fake-RELEASED).
