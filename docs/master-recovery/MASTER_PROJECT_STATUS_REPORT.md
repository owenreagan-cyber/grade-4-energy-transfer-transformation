# MASTER PROJECT STATUS REPORT

> Consolidated status layer. Authoritative daily maps: `production/final-8.5-week/` (see
> `MASTER_CURRICULUM_MAP.md`, `ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md`, `FINAL_RELEASE_MANIFEST.md`).
> This file reconciles chapter-by-chapter status and blockers; it does not replace those maps.
> Generated 2026-10-10 by recovery audit. No commits/pushes/uploads performed.

## Scope

Two-unit Grade 4 science course (CKSci-aligned), 30-minute inclusive blocks.

- **Unit 1 — Energy Transfer & Transformation** · Oct 12 – Nov 6, 2026 · 7 chapters · Unit test Fri Nov 6.
- **Unit 2 — Using Natural Resources for Energy** · starts Nov 9, 2026 · 9 Reader chapters · no instruction
  Thanksgiving week (Nov 23–27) · Unit test no later than Dec 16.

## Chapter status matrix

| Chapter | Classroom bytes | Release | Google Slides | Notes |
|---|---|---|---|---|
| U1-1 Energy Causes Change | **FROZEN v1.1** (42/42 registry match) | PASS (parity) | native deck `1txs8WOy…` (48 slides, iPad 48/48) | v2 guided notes OWNER-APPROVED but registered-only |
| U1-2 Moving Objects Have Energy | **FROZEN v1.0** | PASS (parity) | **MISSING / REQUIRES BUILD** | v6-media 49-slide candidate NOT promoted |
| U1-3 Energy and Speed Are Related | BUILT_UNCERTIFIED (v1.3) | PASS (parity) | not registered | release parity + iPad QA present |
| U1-4 Energy Transfer | legacy build | no release manifest | not registered | needs release packaging |
| U1-5 Collisions Transfer Energy | legacy build | no release manifest | not registered | needs release packaging |
| U1-6 Energy Transformations + Engineering | legacy build | no release manifest | not registered | needs release packaging |
| U1-7 Edison + Unit Review | legacy build | no release manifest | not registered | unit final 25Q/50pt |
| U2-1..9 (nine Reader chapters) | built (notes/slides/activities/labs/assess) | no release manifest | not registered | no per-chapter pacing plans |

## Integrity baseline (verified this run)

- Git: `main` @ `b7695bd`, 211 commits, **no remote**, 1,517 tracked files; 5 modified + 95 untracked working-tree entries.
- Frozen registry: **42/42 byte-identical** in main and in the sandbox copy.
- Object store: **3,641 objects, 0 missing** (2,214 blobs / 211 commits / 1,216 trees).
- Release parity: chapters 1–3 **PASS** (canonical↔release drift, hashes, banned language, widescreen, US Letter, retired-arch archiving).
- Secrets: none (no `.env`/credentials/service-account/private keys; no key-material scan hits).
- Sandbox `…-sandbox-ch12`: superseded copy @ `5544450`; zero unique content/history (see `inventory/SANDBOX_CH12_AUDIT.md`).

## Inventory summary (machine)

`inventory/MASTER_FILE_INVENTORY.csv` (9,222 content files, SHA-256 + tracking status) ·
`inventory/CLASSROOM_ARTIFACT_INVENTORY.csv` (1,437 classroom artifacts) ·
`inventory/FILE_FAMILY_COUNTS.txt` (family counts).

Key families (production/curriculum/assets-authoritative): guided notes 93 · slides 155 · assessments 69 ·
practice/worksheets 49 · answer keys 45 · labs/engineering 54 · media 65 · review/study 403 · teacher playbook 32.

## Release-critical blockers (do NOT claim "complete")

1. Ch2 has **no native Google Slides** teaching deck (canonical is a 37-slide PPTX; 49-slide v6-media candidate unpromoted).
2. Ch4–7 and all of Unit 2 have **no release manifests** and **no per-chapter pacing plans**.
3. **1.3 GB** supplemental video library is git-excluded with **no Git LFS / external-storage strategy**.
4. Google Drive connector times out (mirror not verified this run).
5. No GitHub remote/destination configured (owner decision pending).
