# COMPLETE RESOURCE READINESS CHECKLIST

> Chapter-by-chapter to-do + readiness. Status sources: `qa/gold-standard/frozen_registry.json`,
> `production/releases/chapter-0N/RELEASE_MANIFEST.json`, release-parity runs (Ch1–3 PASS), and the machine
> inventory (`inventory/CLASSROOM_ARTIFACT_INVENTORY.csv`). "Ready" = release-packaged + frozen or parity-PASS.
> "Classroom-ready" is NOT inferred from build exit codes alone.

## Legend
🟢 release-ready · 🟡 built, not release-packaged · 🔴 missing / blocker

## Unit 1

| Chapter | Notes | Slides | Assess | Lab/Eng | Release | Blockers |
|---|---|---|---|---|---|---|
| 1 | 🟢 FROZEN v1.1 | 🟢 PPTX/PDF + native Slides | 🟢 quiz 9/16 + practice | 🟢 Energy Detectives | 🟢 PASS | v2 notes promotion (owner) |
| 2 | 🟢 FROZEN v1.0 | 🟢 PPTX/PDF · 🔴 no native Slides | 🟢 quiz 12 + practice | 🟢 Moving Marbles | 🟢 PASS | native deck REQUIRES BUILD |
| 3 | 🟡 v1.3 uncertified | 🟡 PPTX/PDF | 🟡 quiz/practice | 🟡 Ramp It Up + Drop It | 🟢 parity PASS | internal certification |
| 4 | 🟡 legacy | 🟡 | 🟡 | 🟡 | 🔴 no manifest | release packaging |
| 5 | 🟡 legacy | 🟡 | 🟡 | 🟡 Crash Lab | 🔴 no manifest | release packaging |
| 6 | 🟡 legacy | 🟡 | 🟡 | 🟡 Engineering | 🔴 no manifest | release packaging |
| 7 | 🟡 legacy | 🟡 | 🟡 unit final 25/50 | — | 🔴 no manifest | release packaging |

## Unit 2 (nine Reader chapters)

| Resource | Status | Notes |
|---|---|---|
| Guided notes ch1–9 + keys | 🟡 built | `production/premium-notes/unit-02/…` |
| Slides ch1–9 | 🟡 built | `production/slides/{01..09}-u2-*` |
| Activities | 🟡 built | detective chart, sort, scenario, certificate, etc. |
| Written assessment (25/50) + key | 🟡 built | `production/quizzes/unit-02/` |
| Water Wheel flagship lab | 🟡 built | `production/labs/unit-02/` |
| Review game + scorecards | 🟡 built | `production/review/unit-02/` |
| **Per-chapter pacing plans** | 🔴 missing | AGENTS.md requires `tools/chN_pacing.py → CHN_PACING_PLAN.md` |
| **Release manifests** | 🔴 missing | none of `production/releases/unit-02/…RELEASE_MANIFEST.json` |

## Next prioritized instructional tasks
1. Build Ch2 native Google Slides (mirroring frozen notes BQ/V/N anchors exactly).
2. Promote Ch1 v2 guided notes (owner freeze-reopening) — or hold.
3. Decide Ch1 Scored Check v2 (8/10) supplement-vs-replace frozen quiz (9/16).
4. Resolve Ch2 v6-media 6 pre-existing visual FAILs before any promotion.
5. Release-package Ch4–7 (manifests + parity).
6. Build per-chapter pacing plans for Ch4–7 and Unit 2.
7. Establish media storage strategy (Git LFS or external + immutable manifest) for the 1.3 GB library.
