# MEDIA RECOVERY — UNIT 1 (Energy Transfer & Transformation)

> One-shot discovery + reconciliation. Date: 2026-10-10. Read-only on all sources; originals untouched.
> Companion machine artifacts (this run): `qa/work/media-recovery/inventory.json` (88 unique files / 208 raw hits), `inventory.md`, `duplicates.json`, `staging_log.json`.
> This record does **not** grant approval. It classifies and stages. Approval lives only in the existing manifests and review reports cited below.

## 1. Scope & method

Swept: `~/Downloads`, `~/Desktop`, `~/Documents`, `~/Movies`, `~/Projects`, and the mounted iCloud Drive (`~/Library/Mobile Documents/com~apple~CloudDocs/School/Science`). Extension filter: `.mp4 .mov .m4v .mkv .avi .webm`. Every hit got a SHA-256, `ffprobe` metadata (duration, width×height, video/audio codec), size, and mtime.

Google Drive: the authorized connector (`plugin-google-drive-google-drive`) **timed out** on connection during this run, so Drive discovery is recorded **not performed** (see §7).

## 2. Classification legend (provisional)

- **APPROVED** — cited KEEP/USE in `docs/planning/MEDIA_ASSET_MANIFEST.md` or `docs/planning/TWO_UNIT_MEDIA_MAP.md`.
- **APPROVED WITH CONDITIONS** — cited KEEP WITH NOTES, or a TRIM→USE source whose accepted classroom cut ships.
- **CANDIDATE — NEEDS AUDIT** — on disk, not yet through the review pipeline.
- **FUTURE CHAPTER** — Ch.3–7 generated media, unreviewed.
- **UNIT 2 POTENTIAL** — Unit 2 generated media, unreviewed.
- **TEACHER ONLY** — teacher-recorded demo footage (classroom decision = live demo; file is a backup).
- **SUPERSEDED** — superseded by a reclassified/renamed canonical copy.
- **REJECTED** — cited DO NOT USE.
- **UNKNOWN — RETAIN FOR REVIEW** — ambiguous mapping.

## 3. Classified inventory (energy-relevant, unique by SHA-256)

### 3.1 Chapter 1 — Energy Causes Change

| Filename | Runtime | Res | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|---|---|
| The_Invisible_Boss_of_Change.mp4 | 2:50 | 1280×720 | `9636469cbd32fcf1` | APPROVED WITH CONDITIONS | MANIFEST "KEEP WITH NOTES" |
| The_Energy_Detective.mp4 | 6:45 | 1280×720 | `4396afabfe42127b` | APPROVED | MANIFEST "KEEP" |
| Stored_Energy.mp4 | 4:37 | 1280×720 | `38381321a79e16ae` | APPROVED WITH CONDITIONS | MANIFEST "KEEP WITH NOTES" |
| Energy_Detectives_Briefing.mp4 | 7:53 | 1280×720 | `a018652d4262fd37` | APPROVED | MANIFEST "KEEP" |
| Chapter_1_Science_Notebook.mp4 | 8:26 | 1280×720 | `90266f21fc1ab475` | APPROVED | MANIFEST "KEEP" |
| How_Scientists_Spot_Invisible_Energy.mp4 | 1:16 | 720×1280 | `3b47afea3aaee36a` | APPROVED | MANIFEST "KEEP" |
| Why_Still_Objects_Secretly_Have_Energy.mp4 | 1:16 | 720×1280 | `915d7389526bc619` | APPROVED | MANIFEST "KEEP" |
| Chapter_1_Review.mp4 | 7:17 | 1280×720 | `501b8e7e3450e9d6` | APPROVED | MANIFEST "KEEP" |
| Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4 | 3:05 | 1280×720 | `ec61b59dd1aa844b` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| Energy_Causes_Change__The_Energy_Detective.mp4 | 3:49 | 1280×720 | `21a290001b8b2a71` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| Energy_Detective.mp4 | 5:48 | 1280×720 | `45fb876643b64267` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| The_Energy_Detective-2.mp4 | 6:47 | 1280×720 | `647f10389edcfcfc` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| The_Energy_Detective-3.mp4 | 5:32 | 1280×720 | `2bc2e5f21c9552ab` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| The_Energy_Detective-4.mp4 | 5:55 | 1280×720 | `1f0ab58a9b27f4e9` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| How_Change_Proves_Energy_Exists.mp4 | 1:23 | 720×1280 | `8d0880d707660f6a` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| How_Physical_Change_Proves_Energy_Exists.mp4 | 1:19 | 720×1280 | `0d00e203ffa21846` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| The_Unseen_Mover.mp4 | 5:27 | 1280×720 | `8e6a056b66600c46` | CANDIDATE — NEEDS AUDIT | source-intake 2026-10-09 |
| Energy_Causes_Change.mp4 | 6:43 | 1280×720 | `514b434431ee3418` | REJECTED (Unit 2 misfile) | TWO_UNIT_MEDIA_MAP "DO NOT USE" |
| Teacher_sharpening_pencil_20261003180428.mp4 | 0:08 | 1280×720 | `1882a1b44acc5fc6` | TEACHER ONLY | teacher-recorded demo (2nd take) |
| pencil-sharpener.mp4 (= `…_150908.mp4`) | 0:08 | 1280×720 | `4eee9bd034f11f6a` | TEACHER ONLY | teacher-recorded demo (1st take), already in `qa/slides-qa/ch1/` |

> **Ch.1 media decision (approved):** live pencil-sharpener demonstration; no required video. `build_ch1_classroom_ready.py` records that the uploaded micro-video was reviewed and NOT recommended (unsupported wording: "zero state", "null result", "verified proof"). The teacher-recorded demo files above are backups only.

### 3.2 Chapter 2 — Moving Objects Have Energy

| Filename | Runtime | Res | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|---|---|
| Moving_Objects_Have_Energy.mp4 | 4:50 | 1280×720 | `2885858bf5ac83e2` | APPROVED | MANIFEST "KEEP"; v6 VIDEO A/B/C selection |
| Marble_Collisions__Investigating_Motion_Energy.mp4 | 5:59 | 1280×720 | `b3f7d670c89b2e2c` | APPROVED | MANIFEST "KEEP"; v6 VIDEO A source |
| Things_on_the_Move.mp4 | 7:21 | 1280×720 | `708483c50ad0c940` | APPROVED | MANIFEST "KEEP"; v6 VIDEO C source |
| Chapter_2_Interactive_Notebook.mp4 (= `ch-3.mp4`) | 6:42 | 1280×720 | `80ae44210d193f33` | APPROVED | MANIFEST "KEEP" (reclassified from ch-3) |
| Ch_2__Motion_Energy_in_Action.mp4 | 6:21 | 1280×720 | `352531cf0f018eb6` | APPROVED | v6 VIDEO B source |
| How_Motion_Proves_Energy_Exists.mp4 | 1:12 | 720×1280 | `b18c26dc6b20c482` | APPROVED | v6 audit inventory |
| How_We_See_Invisible_Energy_of_Motion.mp4 | 1:03 | 720×1280 | `1fb4b8cf8a566ff1` | APPROVED | v6 audit inventory |
| ch-3.mp4 | 6:42 | 1280×720 | `80ae44210d193f33` | SUPERSEDED | duplicate of Chapter_2_Interactive_Notebook.mp4 |

### 3.3 Chapter 3 — Energy and Speed

| Filename | Runtime | Res | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|---|---|
| Energy___Speed_Are_Related.mp4 | 7:17 | 1280×720 | `a5c83c50703839fb` | APPROVED WITH CONDITIONS | TRIM→USE source; cut ships |
| speed-and-energy-ramp-it-up-classroom-cut.mp4 | 2:29 | 1280×720 | `e37776710249f75c` | APPROVED | TWO_UNIT_MEDIA_MAP "USE (Wk 2 Wed)" |
| Energy__Ramp_It_Up!.mp4 | 6:05 | 1280×720 | `f0a9531129d6ee91` | FUTURE CHAPTER | NEW (staged this run) |
| How_Speed_Changes_Energy_of_Motion.mp4 | 1:02 | 720×1280 | `0c6ac9cf5c5311e7` | FUTURE CHAPTER | NEW (staged this run) |

### 3.4 Chapter 4 — Energy Transfer

| Filename | Runtime | Res | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|---|---|
| How_Sound_Transfers_Energy.mp4 | 1:18 | 720×1280 | `2db67ae1e1cbeac6` | FUTURE CHAPTER | NEW (staged this run) |
| The_Dancing_Salt_Mystery.mp4 | 7:17 | 1280×720 | `214f207fe840e0c0` | FUTURE CHAPTER | NEW (staged this run) |
| Transfer_vs.mp4 | 7:21 | 1280×720 | `589b0a1f899213a5` | FUTURE CHAPTER | NEW (staged this run; may also serve Ch.6) |
| Energy_Transfer___Transformation_Masterclass.mp4 | 6:52 | 1280×720 | `d5c98f3e25c1e530` | FUTURE CHAPTER | NEW (staged this run; may also serve Ch.6) |

### 3.5 Chapter 5 — Collisions Transfer Energy

| Filename | Runtime | Res | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|---|---|
| Collision_Dynamics___Mass_Effect.mp4 | 4:27 | 1280×720 | `9771a967429d279b` | FUTURE CHAPTER | NEW (staged this run) |
| How_Collisions_Transfer_Energy.mp4 | 1:11 | 720×1280 | `b6b751558ca4bb16` | FUTURE CHAPTER | NEW (staged this run) |
| What_Happens_in_a_Collision_.mp4 | 7:15 | 1280×720 | `d5bc601253e97227` | FUTURE CHAPTER | NEW (staged this run) |
| Investigating_Craters.mp4 | 9:32 | 1280×720 | `01cceb96744ca859` | FUTURE CHAPTER | NEW (staged this run) |

### 3.6 Chapter 6 — Energy Transformations

| Filename | Runtime | Res | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|---|---|
| Energy_Transformations.mp4 | 8:20 | 1280×720 | `3cc7953be12d9a9f` | FUTURE CHAPTER | NEW (staged this run) |
| Engineering_a_Door_Alert.mp4 | 7:48 | 1280×720 | `92a64327d9435e1b` | FUTURE CHAPTER | NEW (staged this run) |
| Observing_Energy_Transformations_in_a_Timer.mp4 | 0:57 | 720×1280 | `98697c44a177465a` | FUTURE CHAPTER | NEW (staged this run) |
| How_a_Flashlight_Transforms_Energy.mp4 | 1:10 | 720×1280 | `118947e7bc8d9b85` | FUTURE CHAPTER | NEW (staged this run) |

### 3.7 Chapter 7 — Edison & Unit Review

| Filename | Runtime | Res | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|---|---|
| The_Journey_of_Energy.mp4 | 8:03 | 1280×720 | `ed3f5005f8143f58` | APPROVED WITH CONDITIONS | TRIM→USE source; cut ships |
| journey-of-energy-unit1-recap-classroom-cut.mp4 | 2:49 | 1280×720 | `8dc946665f0db32e` | APPROVED | TWO_UNIT_MEDIA_MAP "USE (Wk 4)" |
| Edison_s_Light_Bulb.mp4 | 9:36 | 1280×720 | `291062c5acbbbc3e` | FUTURE CHAPTER | NEW (staged this run) |

### 3.8 Unit 2 (energy sources)

| Filename | SHA-256 (first 16) | Category | Evidence |
|---|---|---|---|
| fossil-fuel-formation-classroom-cut.mp4 | `1f255f6e0c0fda25` | APPROVED | TWO_UNIT_MEDIA_MAP "USE (Wk 5 Wed)" |
| turbine-generator-classroom-cut.mp4 | `649fbc83e7d9ad50` | APPROVED | "USE (Wk 6 Tue)" |
| wind-hydro-power-classroom-cut.mp4 | `0d4ec2bd866c5315` | APPROVED | "USE (Wk 7 Mon)" |
| Fossil_Fuel_Formation.mp4 | `08d59d655194e10b` | APPROVED WITH CONDITIONS | TRIM→USE source |
| Energy_Detectives.mp4 | `e341dec3242ed232` | APPROVED WITH CONDITIONS | TRIM→USE source (turbine/generator) |
| Where_Does_Energy_Come_From_.mp4 | `f49baa4eae364f03` | REJECTED | DO NOT USE |
| Power_Plant_Energy_Transformations__Tracing_the_Grid.mp4 | `ce8f4052b50c5520` | REJECTED | DO NOT USE |
| Wind___Hydro_Power.mp4 | `db03356e8b3aea0b` | REJECTED (as-is) | DO NOT USE as-is |
| Solar___Geothermal_Energy.mp4 | `d1a173f325bbf942` | REJECTED | DO NOT USE |
| The_Timescale_Tradeoff__Physics,_Economics,_and_the_Energy_Grid.mp4 | `e773c74ce51f5a07` | REJECTED | DO NOT USE |
| Energy_Causes_Change.mp4 | `514b434431ee3418` | REJECTED | DO NOT USE (misfiled grid-storage) |
| Energy_Innovations.mp4 | `43500449da73e621` | REJECTED | DO NOT USE |
| Unit_2_Synthesis__Energy_Detective_Masterclass.mp4 | `8882d42e94c39d76` | REJECTED | DO NOT USE |

## 4. Duplicate groups (byte-identical by SHA-256)

`qa/work/media-recovery/duplicates.json` lists 46 groups. Notable multi-copy groups (source → mirrors):
- The 8 Ch.1 + 4 Ch.2 approved videos exist in 4–6 identical copies (`~/Downloads`, `assets/supplemental/media/`, `grade-4-lovable-sync`, `source-intake`).
- `ch-3.mp4` ≡ `Chapter_2_Interactive_Notebook.mp4` (4 copies) — SUPERSEDED duplicate.
- `Teacher_sharpening_pencil_…_150908.mp4` ≡ `qa/slides-qa/ch1/pencil-sharpener.mp4` (2 copies) — TEACHER ONLY.
- `Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4` ≡ `source-intake/2026-10-09-chapter-1/media/` copy.

## 5. Staging actions (this run)

Copied 16 new science videos into `assets/supplemental/media/` under chapter folders; every copy SHA-256 verified equal to source. Log: `qa/work/media-recovery/staging_log.json`. Originals in `~/Downloads` remain untouched. One non-science file (`Parent Canvas Account Creation.mov`, 78 MB) was deliberately **not** staged.

## 6. Deletion / move proposal (NOT executed)

Destructive cleanup requires owner approval. Proposed, non-executed:
1. **Downloads dedup:** the 46 duplicate groups mean `~/Downloads` holds redundant copies already mirrored in `assets/supplemental/media/`; propose moving (not deleting) Downloads copies of APPROVED/REJECTED videos to a `~/Downloads/_energy-media-superseded` folder. ~1.2 GB.
2. **`grade-4-lovable-sync` mirror:** propose retiring this entire stale mirror if it is no longer the sync source (owner confirmation).
3. **`grade-4-energy-transfer-transformation-sandbox-ch12`:** propose archiving this sandbox copy once its purpose is confirmed complete.
4. **`Parent Canvas Account Creation.mov`** in `~/Downloads` is unrelated; propose moving to a non-science location (owner's call — not science media).

## 7. Missing / inaccessible

- **Google Drive:** connector timed out (`plugin-google-drive-google-drive`); Drive discovery not performed this run.
- `~/Movies` empty; `~/Desktop`, `~/Documents` have no video assets at top level.
- Ch.3–7 and Unit 2 #2/#4/#7 generation slots remain **PENDING GENERATION** (scripts only) — unchanged.

## 8. Out-of-scope videos observed (other subjects — retained where found, not staged here)

Life science (`~/Library/Mobile Documents/…/School/Science/Videos /` and `Celery /`): A_Plant's Playbook, A_Plant's Secret Senses, Animal Senses, Animal Survival Playbook, Beyond Sight and Sound, How We See the World, Structures and Functions, Building Blocks of Life, From Celery to Cells. Earth science (`Processes that shape earth /Videos/`): 4th Grade Earth Science Labs Earthquakes & Volcanoes, Ch1–Ch7.mp4. Other projects: `explorer-academy-grade4` (cartography), `4th Grade Writing` (writing). These are **not** Energy-unit media.
