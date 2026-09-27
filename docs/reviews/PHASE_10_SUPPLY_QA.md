# PHASE 10 — FINAL SUPPLY QA

> Verifies the master supply order against the released lab/capstone requirements.

## Checks

| Check | Result |
|---|---|
| Every released lab supply appears in `ENERGY_UNIT_MASTER_SUPPLY_ORDER.md` | PASS |
| No obsolete/unsafe supply remains | PASS |
| No contradictory quantities | PASS |
| Reusable vs consumable correctly labeled | PASS |
| Low-voltage electricity only (no wall outlet) | PASS |
| Latex concern noted (rubber bands) | PASS |
| Marble/car containment noted | PASS |
| Warm-water safety noted (≤40°C, teacher-controlled) | PASS |
| Engineering cleanup/storage practical | PASS |

## Obsolete / unsafe supplies REMOVED (confirmed absent from order)
- hot plate
- wall-outlet experiment
- surge-protector experiment
- phone-charger experiment
- chalk-dust requirement
- steel-shooter marble requirement
- solar-oven default materials
- heavy real-door pendulum hardware
- glass/steel multi-variable collision trial

## Group-count handling
- Class size unresolved → all quantities are `GROUP_COUNT × amount` (per group of 4). **No invented total.** Unresolved = class size only; resolved on the teacher's side at ordering time.

## Verdict
- **PASS.** Supply order is complete, safe, and consistent with released chapters. Only unresolved quantity is the class-size variable (intentionally deferred to teacher).
