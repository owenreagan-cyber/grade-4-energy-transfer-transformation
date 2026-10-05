# External Grok Chapter 1 Adversarial Audit — Response (Phase 6.1 + Round 2 / Phase 6.1B)

Date: 2026-10-04 · Responder: Cursor (canonical integrator) · Status: `UNIT1_CH1_GOLD_STANDARD_VERSION = 1.0` / `STATUS = CORRECTIVE MAINTENANCE IN PROGRESS`.
Historical v1.0 certification is preserved unchanged (`docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`).

Each finding was independently re-checked against the repository (not accepted on assertion). Only substantiated defects were fixed. Internal read-only reviewers (curriculum source, QA certification, visual) then audited the fixes; their extra findings (R-items) are listed at the end.

| # | Orig. sev. | Disposition | Evidence (verified) | Action | Affected files | QA result | Propagation consequence |
|---|---|---|---|---|---|---|---|
| F1 | HIGH | **VERIFIED** | Two competing Ch1 schedules existed (45-min/Block language, S1–S9, S12–S23, Thu Detectives, Fri FLEX) | One authority: `tools/ch1_pacing.py` → `CH1_PACING_PLAN.md` (S1 Mon 24.5 min · S2 Tue 24.5 · S3 Fri 25, buffer ≥5 min). All schedule docs synced; stale-reference scan widened to 27 scopes | `tools/ch1_pacing.py`, `docs/chapter-01/CH1_PACING_PLAN.md`, slide speaker notes, Playbook, `UNIT1_PACING_CALENDAR`, `MASTER_*`, `ENERGY_*_PACING`, `WEEK_BY_WEEK_TEACHER_MAP`, `FRIDAY_FLEX_BANK`, quickstart | `check_plan()` + simulation PASS; `qa_ch1_stale_refs` 0 hits | Every chapter needs one generated pacing authority + a scan over all schedule docs (spec G1–G3) |
| F2 | HIGH | **VERIFIED** | Practice key used an ambiguous book-on-table row and an unsupported battery claim | Row removed; Part C uses only Reader examples (battery in flashlight, apple, rubber band); bell/ice rows labeled EXTENSION | practice builder + key | assessments QA PASS | Keys may only cite Reader-supported examples or label EXTENSION |
| F3 | HIGH | **VERIFIED** | Quiz item 9/7 key mismatch; no score line | Score line `___ / 16 ___ %`; MC letters gated against actual options; Q9 statements rewritten (flag/desk/music) so they are not reused from practice; key names each statement | quiz builder, quiz key, blueprint, `qa_ch1_assessments.py` | PASS (incl. Q9 non-duplication and key-lists-statements gates) | Key-vs-page machine check is mandatory (G5) |
| F4 | HIGH | **VERIFIED** | `production/releases/chapter-01/` held stale v1.0 files and the retired notebook | `tools/build_ch1_release.py` rebuilds from canonical masters; stale files archived to `production/archive/retired/chapter-01-release-v1.0/`; `RELEASE_MANIFEST.json` with SHA-256s; `qa_release_parity.py` negative-tested | `production/releases/chapter-01/*`, final-delivery hash CSV | parity PASS | Release parity QA is a standing gate (QA_GATES 9–13) |
| F5 | MED | **VERIFIED** | N1 had redundant blanks | N1 reduced; content blanks 5 (v1.0: 7) | guided notes | notes QA PASS | Blank budget gate |
| F6 | MED | **VERIFIED** | Writing/drawing space tight | More ruled lines (incl. N4 "What changed?" 1→2), taller practice and Detectives rows within the 2-page limit | notes, practice, Detectives | visual QA PASS (no WARN) | Space floors checked by rendered geometry |
| F7 | MED | **VERIFIED, residual closed** | Open tables were pre-answered on slides | Opening/choreography rewritten; residual pre-answers on slides 25 and 28 found by the QA reviewer and removed; gate patterns added | slides builder, `qa_ch1_slides.py` | slides QA PASS | "No hidden note answers on unrelated slides" is an automated gate |
| F8 | MED | **VERIFIED (Ch1 scope)** | Playbook had stale Ch1 language; ambiguous "electrical energy" | Ch1 Playbook sections rewritten and scoped QA added; Ch2 rows are Ch2 scope (reported, not edited) | Playbook builder/QA/docx/pdf | playbook QA PASS; pp. 1–21 visual PASS | Playbook QA must scope per chapter |
| F9 | MED | **VERIFIED** | Detectives Part C directions/points/phantom cards | Detectives is optional and ungraded; Part C directions fixed; "After:" prompt added; phantom cards removed | Detectives builder + key + spec | PASS | Optional resources carry no points |
| F10 | LOW | **VERIFIED** | Reader says "evidence, or proof" | Teach "evidence"; accept "proof" once; slide-visible text bans "proof" | notes, slides, keys | gates PASS | Evidence/proof policy in spec |
| F11 | LOW | **VERIFIED** | Title slide asked a question that is answered later | Title slide fixed | slides | PASS | — |
| F12 | LOW | **VERIFIED** | Review answer pattern guessable | Correct letters C·A·D·B·A·C; pattern gate | slides, propagation spec | PASS | Pattern gate |
| F13 | LOW | **VERIFIED** | Several Reader page references were wrong | Q3 → pp. 1–3, Q6 → p. 4, Q7 → p. 5, "Model It" naming → N1/N4; slide 13 cites p. 1 only | blueprint, quiz key, trace, study-guide contribution, slides | PASS | Page-ref table lives in the spec |
| F14 | LOW | **VERIFIED** | PPTX metadata `screen4x3`; tiny labels | 16:9, no `screen4x3`; word-box ≥ 8.4 pt gate | slides | PASS | Metadata checked in release parity |

## Additional defects found during remediation review (R-items)

| ID | Sev. | Finding | Disposition |
|---|---|---|---|
| R1 | HIGH (QA N1) | Stale competing schedules in 7 other active docs | FIXED; scan widened (27 scopes, 0 hits) |
| R2 | MED (QA N2) | Quiz item 9 duplicated practice Part B | FIXED |
| R3 | MED (QA N3) | Inventory named docs that did not exist | FIXED: the four review docs exist; `qa_phase_inventory.py` now fails on "ghost" entries |
| R4 | MED (QA N4) | Friday Session 3 vs "Friday = FLEX only" | **RESOLVED by owner decision (2026-10-04)**: Friday may hold quizzes/synthesis but never first exposure; Ch1 Session 3 is compliant and now machine-checked (`FRIDAY_DEPENDS`). Record: `docs/planning/CURRENT_DECISIONS.md` |
| R5 | LOW | Slide 23/28/4/13, quiz-key item 9 reasoning, practice-key bell/ice, slides 40–41 stem (source reviewer) | FIXED |
| R6 | LOW | Slides 25/28 pre-answered open tasks | FIXED + gate |
| R7 | LOW | Detectives Part A "Before:" without "After:" | FIXED |
| R8 | LOW | Ch2 Playbook rows still say "Model It · Draw/Label" | **DEFERRED** (Ch2 scope; Phase 7) |
| R9 | LOW | Recovery Step 4 Q3 "battery on a table" | FIXED |
| R10 | LOW | Pacing text "6 min buffer"; P11 still RELEASED; internal phase text in release PDFs; FLEX "Three tracks" | FIXED (sanitizer in release builder; neutral wording) |
| R11 | LOW | N4 cites "Reader pp. 1–6" although p. 6 is a forward preview | **ACCEPTED/OPEN-LOW** for external ruling: N4 is a chapter-wide synthesis; p. 6 is not required content |
| R12 | LOW | Visual WARNs (slide 17 prompt, review-slide explanation box, practice/Detectives row height, Playbook p. 20 title, FLEX p. 4) | FIXED; visual QA 0 WARN in scope |
| R13 | LOW | Visual reviewer: "My first thinking has one rule" | **NOT VERIFIED** — it already has 2 (gate `[2, …]`) |

## Gate status

All internal gates PASS (notes, slides, assessments, Playbook, visual, stale scan, release parity, visual system). The external gate (exact result `APPROVE PROPAGATION`) is **pending**; R4 is resolved. Gold Standard v1.1 is therefore **not frozen**.

---

# Round 2 — Phase 6.1B (final Grok verdict: APPROVE WITH FIXES · release parity WARN)

Status: `UNIT1_CH1_GOLD_STANDARD_VERSION = 1.0` / `STATUS = CORRECTIVE MAINTENANCE IN PROGRESS` — v1.1 release candidate, **not frozen**, pending external sign-off. Prior-round dispositions above are unchanged and not rewritten. Every finding below was re-checked in the repository before being fixed.

| ID | Sev. | Disposition | Verified evidence | Exact fix | Files | QA result | Status |
|---|---|---|---|---|---|---|---|
| H1 | HIGH | **VERIFIED** | `PRODUCTION_MANIFEST.md` P1 (teacher map) and P3 (`production/student-notes/01-ch1…docx`, the "WHAT WE NOTICE" file) were RELEASED; the stale scan did not read this file. Negative-tested: the scan now flags 8 hits on the HEAD version | P1 → `CH1_PACKAGE_MANIFEST.md` + Playbook Ch1 spread; P3 → `production/premium-notes/…guided-notes{,-key}.docx`; new rows P12 pacing, P13 release manifest, P14 teacher map = RETIRED/SUPERSEDED, P15 old notes = RETIRED/SUPERSEDED; status vocabulary gains RETIRED/SUPERSEDED; P4 relabelled Detectives (optional). Stale scan: explicit `PRODUCTION_MANIFEST` scope (asserted), retired-artifact rule (any line naming a retired Ch1 artifact must say RETIRED/SUPERSEDED), P3 positive check, applied to all active + shared-line files | `production/PRODUCTION_MANIFEST.md`, `tools/qa_ch1_stale_refs.py` | stale scan 0 hits, 28 scopes | **FIXED** |
| H1 follow-up | LOW | **VERIFIED** (internal reviewer) | `MASTER_RESOURCE_INDEX.md:13` listed the old teacher map as CORE; `MASTER_CURRICULUM_MAP.md:48` listed it under TEACHER — the scan could not see them | Both now point at the package manifest/Playbook; scan rule extended to those files | those two files, `qa_ch1_stale_refs.py` | 0 hits (negative-tested on HEAD) | **FIXED** |
| M1 | MED | **VERIFIED** | Student N1 printed `ENERGY → CHANGE → EVIDENCE` while asking for "evidence" | Student model's last box is empty (`ENERGY → CHANGE → ▢`); teacher key keeps the full model; slide 15 tells students to leave the box open; slide 16 shows the full model and says "write the same word in the last box"; recovery page updated | notes docx/pdf + key, `build_ch1_guided_notes.py`, slides 15–16, handoff/manifest, recovery | notes QA (N1 redundancy gate, key parity), slides QA, sync gate PASS | **FIXED** |
| M2 | MED | **VERIFIED** | Slide 23 subtitle answered its own PREDICT ("batteries store energy in chemicals") | Slide 23 is a pure prediction; the Reader p. 4 fact is read after the prediction (slide 23 note REVEAL) and shown on slide 25. Internal reviewer then found slide 20's speaker note pre-asking the battery question → rewritten to "what does *later* tell us…" | `build_ch1_slides.py`, slides 20/23/25, `qa_ch1_slides.py` (new pre-ask gate) | slides QA PASS | **FIXED** |
| M3 | MED | **VERIFIED** | Friday had no explicit fallback (TIGHT) | Single authority `tools/ch1_pacing.py`: quiz handed out ≤ minute 12; priority N4 > BQ NOW I THINK > CHECK; ladder with minute 6 / 9.5 / 12 checkpoints; N4 path 6.0 + 5.0 loss = 11 ≤ 12; `check_plan()` enforces it. Friday policy unchanged. Generated plan, Playbook, quickstart, calendar, master map/pacing, week-by-week map carry the same wording (no second timing system) | `ch1_pacing.py`, `gen_ch1_pacing_plan.py`, `CH1_PACING_PLAN.md`, Playbook, 6 schedule docs | `check_plan()` empty; Playbook QA PASS | **FIXED** |
| M4 | MED | **VERIFIED** | Recovery said "Our class looked around the room… what some classmates found" and listed a fan and a bulb that were never observed | Table now has a "Where it comes from" column: three **Reader p. 1** examples (switch/dark room, balloon pop, toy car) — checked word-for-word against the Reader PDF — plus one labelled **class pencil-sharpener demo** row. No class data invented; no second notes packet. (The brief's "fan begins moving" example is not in the Reader and was not used.) | `01-ch1-absent-student-recovery.md` | stale pattern + reviewer check PASS | **FIXED** |
| L1 | LOW | **VERIFIED** (this resolves prior R11) | N4 cited "Reader pp. 1–6" | pp. 1–5 in notes, key, slides 28/29/30, handoff, manifest, Playbook table/cue, week-by-week map, calendar, recovery. Playbook keeps "pp. 1–6 / core pp. 1–5 / p. 6 = forward preview". No p. 6 content added | see files above | notes/slides gates + stale pattern PASS | **FIXED** |
| L2 | LOW | **PARTIALLY VERIFIED** (this corrects prior R13) | The notes already had two ruled lines, but the 2nd sat 1.5 pt above the V1 heading and read as one; the key shows one sample by design | Added spacing so the two lines are visually separate (rendered gate: exactly 2 rules, pitch 28.1 pt, 19.5 pt clear of V1); nothing else compressed; still 3 pages | `build_ch1_guided_notes.py`, `qa_ch1_guided_notes.py` (new geometry gate) | PASS | **FIXED** |
| L3 | LOW | **VERIFIED** | Friday FLEX PDF printed `student/recovery/01-ch1-absent-student-recovery.md` | Text is now "Use the Chapter 1 absent-student recovery page."; release builder strips any `.md` path; new parity gate scans every release PDF for repo paths, phase labels, WHAT WE NOTICE and INB (negative-tested against the old PDF). Also fixed: bullets in FLEX/teacher-key PDFs ran together (no blank line before lists) and literal `[x]` checkboxes | `01-ch1-friday-flex.md`, `build_ch1_release.py`, `qa_release_parity.py`, release PDFs | parity PASS (13 gates) | **FIXED** |
| L4 | LOW | **VERIFIED** | Slide 32 question state carried the evidence sentence | Moved to the spoken REVEAL in the speaker note; slide face has no answer | slide 32 | slides QA PASS | **FIXED** |
| L5 | LOW | **VERIFIED** | Slide 45: "A battery stores energy; it changes when released." | "A battery stores energy. It can cause a change later." (Reader p. 4). Rubber-band "released" wording (slide 39) is source-faithful and unchanged | slide 45 | PASS | **FIXED** |
| L6 | LOW | **VERIFIED** | "17–27" ranges silently included optional slide 18 | Written "2, 17, 19–27 (18 OPTIONAL)" in the Playbook, quickstart, calendar, master docs, blueprint, handoff, manifest and speaker notes; stale pattern forbids the hyphenated form | many (see inventory) | 0 hits | **FIXED** |
| Front matter | LOW | **VERIFIED** | Playbook SCOPE callout read "Phase 7 — Chapter 2 gold-standard package complete…" | Replaced with classroom-facing text ("Chapters 1–2 are classroom-ready…; Chapters 3–7 are placeholders in this edition") | `build_teacher_playbook.py` | Playbook QA PASS | **FIXED** |
| M5 | — | **NOT VERIFIED — never defined** | The brief asks to record "H1, M1–M5, L1–L6" but defines only M1–M4 | Nothing to fix; **please supply M5 or confirm it is a typo** | — | — | **OPEN (needs auditor)** |

## Disclosures (nothing hidden)

- Prior R13 ("My first thinking already has 2 rules — NOT VERIFIED") was incomplete; see L2.
- `qa/reports/PHASE_6_1_CH1_CLASSROOM_TIME_SIMULATION.md` (untracked) was regenerated and now holds current-state content only; earlier text is not recoverable. `qa/reports/PHASE_3_CH1_GUIDED_NOTES_QA.md` and `PHASE_4_CH1_SLIDESHOW_QA.md` are rewritten by their QA tools on every run; the 6.1B copies are `PHASE_6_1B_CH1_*`.
- Internal reviewer ([QA/Certification Reviewer](17cb559a-d47f-47f1-a107-cad8fd681221)) tried to falsify the 12 requested claims: 11 PASS, 1 WARN (slide 20 pre-ask — fixed). Reported but not changed (low): Playbook labels Ch1 spreads "FINAL" although v1.1 is not frozen; Friday FLEX PDF table splits across pages; release `README.md`/`RELEASE_MANIFEST.json` contain repo paths (developer files, not classroom PDFs); slide 18 is marked OPTIONAL in speaker notes/docs, not on the slide face.
- **Known Phase 7.1 work, deliberately not touched:** Ch2 Playbook rows still say "Model It · Draw/Label"; Ch2 placeholder timing / pacing ("Block 1 / Block 2", Playbook p. ~26); Ch2 `PRODUCTION_MANIFEST` rows P1/P3 still point at the legacy `student-notes/02-ch2…docx`; sparse Ch2+ Playbook pages (visual WARN, pp. 22/26/30).

## Gate status (Round 2)

Internal gates PASS: notes, key parity, slides (incl. sync + 6.1B gates), assessments, Playbook, pacing (`check_plan()`), Friday dependency, stale scan (28 scopes, 0 hits, PRODUCTION_MANIFEST in scope), release parity (13/13), visual (0 FAIL / 0 WARN across Ch1 artifacts), inventory completeness (`PHASE_6_1B_ARTIFACT_INVENTORY.md`). External sign-off **pending**; v1.1 **not frozen**.

---

# Round 3 — Phase 6.1C (focused sign-off: APPROVE WITH FIXES · five findings)

Release parity, inventory, Friday policy and prior remediation were PASS in the sign-off. Each finding below was independently reproduced before fixing. Status: **fixed, pending one final external Grok sign-off. v1.1 is NOT frozen.**

| ID | Verdict | Verification | Fix |
|---|---|---|---|
| M-A | VERIFIED (active manifest still said the Interactive Science Notebook is primary / supersedes guided notes) | read `production/PRODUCTION_MANIFEST.md` | "Notebook System" paragraph replaced by one "Student Note Architecture (current)" statement: Guided Notes PRIMARY; Science Journal SECONDARY; notebook/glue-in RETIRED for Chapter 1. No second competing architecture statement. |
| stale checker | VERIFIED (checker did not look for notebook-primary language) | in-memory negative tests | `tools/qa_ch1_stale_refs.py`: `NOTEBOOK_PRIMARY` patterns applied to the manifest and active scopes (retired/historical wording exempt). Current tree 0 hits; 4 injected phrasings each detected in memory (no mutation left in tree). |
| L-A | VERIFIED (forms / stored-energy rows: the writing rule sat visually on the next row's label) | rendered geometry: old PDF rule 3.2 pt above the next label | Row labels bottom-anchored, zero paragraph spacing, hairline under the label joined to the writing rule, row height kept (about 38 pt pitch), no font change, 3 pages. New gate `gate_page2_row_rules` (student + key, 8/8 rows). |
| L-B | VERIFIED (FLEX p3 began with a bare Field/Value header) | `pdftotext` of v1.1-B PDF | Each FLEX activity section starts on a fresh page (`tools/build_ch1_release.py`); 4 pages, each opens with its section title. New release-parity gate fails on any page that opens with a headless table. |
| L-C | VERIFIED (slide 1 showed ENERGY → CHANGE → EVIDENCE before the N1 write/reveal) | pptx text | Slide 1 chain is now ENERGY → CHANGE → open "?" chip (Big Question unchanged). Slides 14–16 unchanged (14 "?", 15 write, 16 reveal). New gate in `gate_phase_6_1b`; fails on the v1.1-B deck. |
| L-D | VERIFIED (raw repo paths on Playbook pp. 3, 5, 8, 16, 17, 19, 20) | `pdftotext` scan of all 33 pages | Replaced with classroom names ("Chapter 1 Pacing Plan", "Chapter 1 Absent-Student Recovery", "Chapter 1 Friday FLEX", …). New Playbook gate; fails on the v1.1-B Playbook. Page count unchanged (33). |

## Disclosures (Round 3)
- Playbook pages 23–31 (Chapter 2 rows and the Ch3–7 SKELETON appendix) still print repo paths; they belong to later phases and were deliberately not edited. The Playbook was regenerated as a whole file, so Chapter 2–7 pages were re-rendered but their text is unchanged.
- Playbook page 22 is a Chapter 2 page flagged WARN (sparse) by visual QA; out of scope (Phase 7.1).
- Visual descriptions of rendered images were unreliable for L-A (they disagreed with each other); the L-A verdict rests on the deterministic gate and a pixel-level trace, not on image descriptions.

## Gate status (Round 3)
Notes, key parity, slides (incl. sync), assessments, Playbook, `check_plan()`, stale scan (28 scopes, 0 hits), release parity (14 gates) and visual QA (notes 3+3, slides 45, FLEX 4, teacher key 6, practice, quiz, Detectives, Playbook pp. 1–20) all PASS. Inventory: 0 missing.

## Internal independent review (Round 3)
[QA/Certification Reviewer](def267b3-c3bb-4ec9-8578-619b44de9d66): 9 claims PASS, 0 FAIL. Substantiated WARN fixed: the stale checker's exemption words ("never", "must not") were broad enough to hide an affirmative notebook-primary claim, and "notebook-first" / "Guided Notes secondary to the notebook" were not covered. Exemption narrowed and two patterns added; 5 evasion phrasings now each detected in memory, current tree 0 hits. Reviewer's side effect: re-running `tools/qa_ch1_slides.py` regenerated `qa/reports/PHASE_4_CH1_SLIDESHOW_QA.md` (deterministic; same tool output as 6.1C). Not changed: Friday N4 placement (owner-decided policy, documented in `FRIDAY_DEPENDS`); inventory glob looseness (tool limitation).

---

# Round 4 — Phase 6.1D (final notebook-architecture guardrails)

Focused sign-off: APPROVE WITH FIXES (classroom release correct). Two freeze holds, both fixed below. v1.1 remains **not frozen**; no commit, no push.

| ID | Verdict | Verification | Fix |
|---|---|---|---|
| M-B (checker coverage) | VERIFIED — detector missed "notebook is the primary student-note system" and equivalent phrasings; the word-level exemption ("retired"/"historical"/"legacy") could clear a live claim | `notebook_primary_hit` on injected phrasings | `NOTEBOOK_PRIMARY` rewritten as precise LIVE-claim patterns (present-tense "notebook is/remains/stays/becomes [still/now/again] [the/a/our] primary", "notebook as primary", active "notebook supersedes Guided Notes", passive "Guided Notes are superseded by the notebook", "notebook-first", adjective "primary notebook", "primary student artifact … notebook", "Guided Notes … secondary … notebook"). The whole-line word exemption is **removed**; retirement statements are excluded by construction (past tense, "superseded by Guided Notes", "is retired", "no longer primary"). |
| M-B (exemption) | VERIFIED — a line like "must not be retired" / "still the primary" / "despite historical" no longer suppresses detection | in-memory | No `retired/historical/legacy` word-skip exists. All three dodge phrasings hit. |
| M-C (retired standard) | VERIFIED — `SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md` presented itself as current for Ch1–2 | read file | Unmistakable `SUPERSEDED / HISTORICAL (Phase 6.1D)` banner at top; body retained as archival evidence. Banner is scan-validated (see below). |

## Regression fixture (saved, not terminal-only)
`tools/qa_notebook_primary_fixture.py` — run one-shot. BAD 6/6 detected, SAFE 4/4 allowed. Also carries the reviewer's adversarial set as separate in-memory checks.

## Stale-scan decision for the retired standard
`docs/planning/SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md` is **included** in the stale scan as a banner gate (`scan_retired_standard`). With the SUPERSEDED/HISTORICAL banner present → 0 hits (historical body is archival). Banner removed → 1 hit (FAIL). Live scan: **29 scopes, 0 hits**.

## Disclosures (Round 4)
- Only the checker, the fixture, the retired modeling standard, and QA reports changed. No classroom artifact was rebuilt.
- Reviewer ([QA/Certification Reviewer](219d6d0e-f1b8-4f1f-bf87-4e520cf60078)) independently attempted to falsify the logic with 5 adversarial phrasings (negation, mixed historical/current, "must not be retired", "formerly retired but primary again", "legacy notebook remains primary") — all classified correctly. Two non-blocking coverage notes were applied (indefinite/possessive determiners and adjective-form "primary notebook"); a bare "must not be retired" without any primary/supersede/first claim remains out of the documented contract and is not flagged.
- `docs/planning/INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md` and `STUDENT_NOTES_STANDARD.md` already carried RETIRED/HISTORICAL banners; no change needed there.

## Gate status (Round 4)
Notebook-architecture truth PASS (AGENTS.md, PRODUCTION_MANIFEST.md, CURRENT_DECISIONS.md, propagation spec G11, GUIDED_NOTES_STANDARD.md all agree: Guided Notes PRIMARY, Science Journal SECONDARY, notebook/glue-in RETIRED for Chapter 1). Stale checker live run PASS (0 hits). Fixture PASS (6/6 BAD, 4/4 SAFE). Adversarial review PASS. Retired standard banner CLEARLY SUPERSEDED. Release parity UNCHANGED / PASS (no classroom rebuild). Chapter 1 classroom artifacts NOT modified.

---

# Round 5 — Phase 6.1E (final notebook-guardrail hardening)

Focused sign-off: APPROVE WITH FIXES (architecture truth already PASS). Two holds fixed below. v1.1 remains **not frozen**; no commit, no push.

| ID | Verdict | Verification | Fix |
|---|---|---|---|
| H1 (semantic shapes) | VERIFIED — detector missed reversed-copula, imperative, label/colon, and equals forms | `notebook_primary_hit` on injected phrasings | `NOTEBOOK_PRIMARY` now covers: reversed copula ("primary [student-note] system/notes/artifact is/are the notebook"), imperative reactivation ("make/restore/set … notebook … [as] primary", negation-guarded), label/colon ("primary notes: notebook"), equals ("notebook = primary …" / "primary notes = notebook"), and modal/future be-copula ("shall/should/will/must/can/may … be primary", "is/are to be primary"). Word-level retirement exemption remains absent. |
| M1 (scan scope) | VERIFIED — five active architecture authorities were outside the scan; two retired standards were not banner-gated | read scan config | Added whole-file scan of `AGENTS.md`, `CURRENT_DECISIONS.md`, `GUIDED_NOTES_STANDARD.md`, `UNIT1_PRODUCT_STANDARD.md`, `CH1_GOLD_STANDARD_PROPAGATION_SPEC.md` (no Chapter-1 line filter). Banner-gated all three retired notebook standards (`SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md`, `INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md`, `STUDENT_NOTES_STANDARD.md`) on the leading blockquote only (marker + "Guided Notes PRIMARY" + "notebook not current"), so a removed banner is detected and the historical body cannot mask it. |

## Saved fixture (expanded)
`tools/qa_notebook_primary_fixture.py` — BAD 12/12 detected, SAFE 7/7 allowed.

## Adversarial QA-of-QA (read-only reviewer)
[QA/Certification Reviewer](84a92aca-e9c9-4ec7-887c-0c95981a9b75) invented 40 phrasings across reversed-copula, imperative, colon, equals, passive, possessive, indefinite, "again"/"still"/"remains", mixed historical/current, negation, retirement, supersession, and all four notebook tokens. 37/40 correct on first pass; the 3 escapes were all modal/future be-copula ("shall/should/will be primary"). Substantiated → fixed (added modal + "is/are to be" be-copula). Re-checked: all three now HIT; the negation forms ("must not be primary", "should not be primary", "is not to be primary") stay SAFE. Final: **40/40 correct** (remediation loop 1 of 2).

## Banner gates
All three retired standards: banner present → PASS (0 hits); banner removed → FAIL (hit). `STUDENT_NOTES_STANDARD.md` and `INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md` already carried complete RETIRED/HISTORICAL banners; no banner text was rewritten — they were added to the gate list only.

## Gate status (Round 5)
Live scan: **36 scopes, 0 hits** (was 29). Architecture truth PASS (AGENTS.md, PRODUCTION_MANIFEST.md, CURRENT_DECISIONS.md, UNIT1_PRODUCT_STANDARD.md, GUIDED_NOTES_STANDARD.md, CH1_GOLD_STANDARD_PROPAGATION_SPEC.md: Guided Notes PRIMARY · Science Journal SECONDARY · notebook/glue-in RETIRED for Chapter 1). Fixture PASS. Release parity UNCHANGED / PASS. No classroom artifact rebuilt (confirmed by mtime/hash). Inventory 0 missing.

---

# Round 6 — Phase 6.1F (fail-closed note-architecture guardrail)

Focused sign-off: APPROVE WITH FIXES (classroom release correct). The hold is the guardrail design itself — regex-by-sentence-shape still lets fresh realistic notebook-reactivation wording escape. Fixed by replacing the shape-regex engine with a **fail-closed authority-line model** backed by a **reviewed allowlist**. v1.1 remains **not frozen**; no commit, no push.

| ID | Verdict | Verification | Fix |
|---|---|---|---|
| F1 (regex fragility) | VERIFIED — 11 fresh realistic reactivation phrasings ("Students' primary notes will be the glue-in notebook", "Primary note system: glue-in notebook", "Guided Notes are optional; the notebook is required", etc.) were classified SAFE by shape regexes | injected phrasings | Removed `NOTEBOOK_PRIMARY` shape-regex detector. New engine `tools/qa_ch1_note_architecture.py` scans each authority **whole-file**: a clause containing a notebook token **and** an architecture-sensitive concept must be (1) a clause-local SAFE retirement/negation/historical statement, or (2) an exact match to a reviewed allowlist entry — otherwise it **fails closed** as `unreviewed`. |
| F2 (allowlist) | VERIFIED — no reviewed baseline existed, so any new architecture-affecting line had to be re-adjudicated by regex | read tree | Added `qa/baselines/ch1_note_architecture_allowlist.json` (16 reviewed clauses across the 6 authorities: file · clause · normalized · sha256 · classification · rationale). Rewritten/moved lines must match exactly or fail; stale entries are reported. |
| F3 (banner gate) | VERIFIED — retired-standard banner checker read every blockquote in the file, so a late historical blockquote could satisfy the gate | read checker | `leading_banner()` now inspects **only the first contiguous blockquote after the title**. Late-body blockquotes cannot satisfy the gate (3/3 late-body attacks rejected). |
| F4 (false positives) | VERIFIED — "Never restore the notebook as primary." and "The Science Journal is a notebook; Guided Notes are primary." mis-flagged | injected phrasings | Negation now binds to "restore … as primary"; semicolon is a clause boundary; detector no longer spans unrelated clauses. Both saved as SAFE fixtures. |

## Saved fixture (expanded)
`tools/qa_notebook_primary_fixture.py` — **BAD 27/27 detected · SAFE 22/22 allowed** (prior 12 BAD + 11 fresh Grok escapes + 4 mixed historical/current + 2 false-positive fixes + expanded SAFE).

## Structural QA-of-QA (read-only reviewer)
[QA/Certification Reviewer](b78e6e05-2403-4d1f-99b4-fc5d4f7616f9) tested the **system** (not more grammar): A. 20/20 live reactivations detected · B. 10/10 safe retirement/historical/negation allowed · C. 5/5 mutated allowlist lines rejected · D. 5/5 new unreviewed authority lines failed closed · E. 3/3 late-body banner attacks rejected. Anomalies: none. Overall **PASS** (A=20/20, B=10/10, C=5/5, D=5/5, E=3/3).

## Allowlist negative tests (T0–T5)
Modify one meaningful word → FAIL · new notebook-primary line → FAIL · new semantically-safe-but-unallowlisted retirement line → PASS (recognized by strong retirement semantics) · delete an allowlisted line → stale entry reported · move/rename authority → baseline mismatch reported. All as specified.

## Gate status (Round 6)
Live scan: **6 authorities, 16 sensitive clauses** (auto-safe 0 · allowlisted 16 · unreviewed **0** · stale allowlist **0**). Retired-standard leading-banner gates: 3/3 PASS. Architecture truth PASS (Guided Notes PRIMARY · Science Journal SECONDARY · notebook/glue-in RETIRED for Chapter 1 across all six authorities). Fixture PASS. Release parity UNCHANGED / PASS (14 gates). Inventory 0 missing. No classroom artifact rebuilt (mtime/hash/diff unchanged).

---

# Round 7 — Phase 6.1G (concept-level architecture sensitivity)

Focused sign-off: APPROVE WITH FIXES. The allowlist from 6.1F held. The remaining hole was earlier: architecture-changing sentences were classified NEUTRAL and never entered review. v1.1 remains **not frozen**; no commit, no push.

| ID | Verdict | Verification | Fix |
|---|---|---|---|
| G1 (silent neutral) | VERIFIED — 12 realistic role changes ("Guided Notes yield to the notebook architecture", "Adopt the glue-in notebook", "Guided Notes are optional", "Science Journal is primary", and the rest of the set) never entered review | injected sentences | A clause that **names** Guided Notes, the Science Journal, or the retired notebook family (INB, glue-in, notebook architecture/workflow, composition book, paste-ins, sort-and-glue) is architecture-sensitive. It then passes only if it is an exact allowlist entry, or a clause-local retirement/negation/past statement, or a clear restatement that Guided Notes are primary and/or the Science Journal is secondary. Otherwise it fails closed. |
| G2 (hierarchy) | VERIFIED — Guided Notes demotion and Science Journal promotion passed with no notebook token | injected sentences | Same gate. "Guided Notes are optional/secondary" and "Science Journal is primary" fail closed. |
| G3 (later chapters) | VERIFIED — `PRODUCTION_MANIFEST.md` still lists Chapter 2–7 notebook rows | read manifest | Markdown table rows under a Chapter 2–7 heading are OUT OF SCOPE — PHASE 7.1+. Exclusion is the heading plus the row, not the word "notebook." Prose and global statements stay in scope. Live exclusions: 7. |
| G4 (new current clauses) | VERIFIED — broadening the gate surfaced current clauses that agree with the locked hierarchy | manual read of each | 25 new allowlist entries (26 clauses; one Science Journal sentence occurs twice). Each was read and classified. None contradicts Guided Notes PRIMARY, Science Journal SECONDARY, notebook RETIRED for Chapter 1. |

## Newly allowlisted current clauses
- AGENTS.md — Guided Notes are the primary student content/reference artifact. GUIDED_NOTES_PRIMARY.
- AGENTS.md — Science Journal is secondary. JOURNAL_SECONDARY.
- PRODUCTION_MANIFEST — Phase 11 comparison of INB vs Guided Notes. HISTORICAL_REFERENCE. Comparison-only; the next sentence says the prototypes do not replace released Chapter 1 artifacts.
- PRODUCTION_MANIFEST — C1 INB comparison prototype row. HISTORICAL_REFERENCE.
- PRODUCTION_MANIFEST — C2 Guided Notes comparison prototype row. HISTORICAL_REFERENCE.
- PRODUCTION_MANIFEST — P3 released Guided Notes row. GUIDED_NOTES_PRIMARY.
- PRODUCTION_MANIFEST — P15 legacy WHAT WE NOTICE Guided Notes, RETIRED / SUPERSEDED by premium P3. HISTORICAL_REFERENCE.
- PRODUCTION_MANIFEST — "Guided Notes are the primary student artifact." GUIDED_NOTES_PRIMARY.
- PRODUCTION_MANIFEST — Guided Notes are the PRIMARY structured student-note/reference artifact. GUIDED_NOTES_PRIMARY.
- PRODUCTION_MANIFEST — Science Journal is SECONDARY. JOURNAL_SECONDARY.
- PRODUCTION_MANIFEST — "Notebook retrofit complete (Phase 4.5)" under the Chapter 2 blurb. HISTORICAL_REFERENCE. Chapter 2 status, not a Chapter 1 role.
- PRODUCTION_MANIFEST — Unit 2 premium guided notes row. HISTORICAL_REFERENCE. Outside the Chapter 1 hierarchy.
- CURRENT_DECISIONS — Phase 0A.1 reconciliation: Guided Notes are PRIMARY. GUIDED_NOTES_PRIMARY.
- CURRENT_DECISIONS — "Science Journal is SECONDARY" (both occurrences). JOURNAL_SECONDARY.
- CURRENT_DECISIONS — Phase 4.5 banner: Guided Notes are PRIMARY. GUIDED_NOTES_PRIMARY.
- CURRENT_DECISIONS — struck-through "guided notes remain OPTIONAL" corrected to PRIMARY, not OPTIONAL. GUIDED_NOTES_PRIMARY.
- CURRENT_DECISIONS — drawing/modeling retained within Guided Notes. GUIDED_NOTES_PRIMARY.
- CURRENT_DECISIONS — Chapter 4 notebook insert count. HISTORICAL_REFERENCE. Later-chapter insert count, not the Chapter 1 system.
- GUIDED_NOTES_STANDARD — leading banner "Primary student content/reference artifact." GUIDED_NOTES_PRIMARY.
- GUIDED_NOTES_STANDARD — document title. GUIDED_NOTES_PRIMARY.
- UNIT1_PRODUCT_STANDARD — Guided Notes = primary. GUIDED_NOTES_PRIMARY.
- UNIT1_PRODUCT_STANDARD — Science Journal = secondary. JOURNAL_SECONDARY.
- CH1_GOLD_STANDARD_PROPAGATION_SPEC — Notes before slides. GUIDED_NOTES_PRIMARY.
- CH1_GOLD_STANDARD_PROPAGATION_SPEC — section heading "GUIDED NOTES." GUIDED_NOTES_PRIMARY.
- CH1_GOLD_STANDARD_PROPAGATION_SPEC — Guided Notes conformance gate. GUIDED_NOTES_PRIMARY.

## Structural QA-of-QA
[QA/Certification Reviewer](bca93880-c953-44a0-843d-362bf7be03f4), read-only, two remediation loops. Round 1 found place/work paraphrases ("glue into the INB", "skip Guided Notes") classified neutral, plus three locked-invariant sentences failing closed. Fixed. Round 2 found fresh verbs ("staple", "file", "sit out", "nice-to-have") still neutral. Fixed by treating a mention of a protected system as sensitive. Re-check: 35/35 of those sentences sensitive; both safe negations allowed ("Do not glue energy cards into the INB", "The notebook is not where students keep the Big Question"). A further set that never names a protected system (spiral, binder, logbook, handout packet) is still neutral. That set is outside the token families in this phase. Remediation stopped at the cap of 2.

## Gate status (Round 7)
Live scan: **6/6 authorities, 42 sensitive clauses** (auto-safe 0 · allowlisted 42 · unreviewed **0** · stale allowlist **0** · Chapter 2–7 exclusions **7**). Fixture 46/46 BAD, 27/27 SAFE. Persistent negative suite PASS. Retired-standard leading banners 3/3; late-body attacks 3/3 rejected. Architecture truth PASS. Release parity UNCHANGED / PASS (14 gates). Classroom artifacts not modified (release masters still dated 2026-10-04). Inventory 0 missing.

---

# Round 8 — Phase 6.1H (storage vs note-system boundary)

The student folder is storage. A clause that assigns any medium an instructional note role enters review, including a medium the token list has never seen. Bare "folder" does not. v1.1 remains **not frozen**; no commit, no push.

| ID | Verdict | Fix |
|---|---|---|
| H1 (unnamed medium) | VERIFIED — spiral, binder, logbook, portfolio, packet, and "accordion file" could become the note system without naming Guided Notes, the journal, or the notebook | Instructional-role phrases (primary notes, official student note system, notes medium, main reference artifact, all student notes, folder system, instead of / replaces Guided Notes) enter review on their own. The clause then fails closed unless allowlisted or clearly a retirement/invariant statement. |
| H2 (folder storage) | VERIFIED — "keep your notes in your folder" must stay neutral, while "primary notes in the folder" must fail | Bare folder is not an entity. Role phrases are. Storage and graded-work collection stay neutral. Unfinished work placed in the folder until the next class stays neutral. |

One new current clause was reviewed and allowlisted: the Phase 11 teaching-comparison slide row, whose filename contains `note-system`. It is a comparison deck. It does not assign a Chapter 1 note system. HISTORICAL_REFERENCE.

## Structural QA-of-QA
[QA/Certification Reviewer](caba3e73-acd8-44c0-86bb-06fcceba1124), read-only. Alternate-media role changes 10/10 fail closed. Unknown-media role changes 10/10 fail closed. Folder storage 10/10 neutral. Graded-work cases 5/5 distinguished. A new medium cannot become the student note system without review.

## Gate status (Round 8)
Live scan: **6/6, 43 sensitive clauses** (allowlisted 43 · unreviewed **0** · stale **0**). Boundary A–L 12/12. Fixture 66/66 BAD, 42/42 SAFE. Release parity UNCHANGED / PASS (14 gates). Classroom artifacts not modified.

---

# Round 9 — Phase 6.1I (same-clause retirement mask)

A live note-role assignment is classified before retirement auto-safe. "Although the notebook is historical, primary notes will be the spiral" fails closed. "The notebook is no longer the primary note system" stays safe. v1.1 remains **not frozen**; no commit, no push.

| ID | Verdict | Fix |
|---|---|---|
| I1 (retirement mask) | VERIFIED — historical/retired/no-longer language cleared a later live role in the same clause | `competing_live_role` blocks `notebook_safe` when the clause also assigns primary/main/official/required notes, a notes medium, or "replaces Guided Notes" to another system. Negation applies only to the role phrase it sits against. |
| I2 (global claim) | VERIFIED — a Chapter 2 historical phrase must not shelter an all-chapters binder claim | Chapter exclusions stay limited to table rows under a Chapter 2–7 heading. The global sentence fails closed as prose. |

`--list` and the scan report name the auto-safe reason (`invariant_safe`, `historical_safe`, `retirement_safe`, `notebook_safe`) when a clause is auto-safe. The live tree has none; all 43 sensitive clauses are allowlisted.

## Structural QA-of-QA
[QA/Certification Reviewer](8e39ce5b-63c4-4bbd-b061-50c3b9aaf2f8), read-only, two loops. First scored set: mixed 12/15, pure retirement 10/10, unknown-media 10/10, storage 10/10. The three misses were "no longer" washing a later role. After that fix, one more sentence stayed safe ("not current, so official notes move to the binder") because "not" was treated as negating the later phrase. That window is now the words immediately before the role phrase. Those sentences are in the persistent suite (16/16 fail closed). A third review was not run.

## Gate status (Round 9)
Live scan unchanged: **6/6, 43 sensitive, 43 allowlisted, 0 unreviewed, 0 stale**. Allowlist file still 42 entries (one normalized Science Journal sentence matches twice). Fixture 76/76 BAD, 47/47 SAFE. Release parity UNCHANGED / PASS (14 gates). Classroom artifacts not modified. No allowlist edit.

---

# Round 10 — Phase 6.1J (role sensitivity and retirement precedence)

`competing_live_role` is no longer a second, shorter list of role forms. A live role is any match of `has_architecture_role` that is not the locked invariant, pure notebook retirement/history, or a pure negation. A role without a copula ("keep the main reference artifact") stays live when the same clause also says the notebook is retired. v1.1 remains **not frozen**; no commit, no push.

| ID | Verdict | Fix |
|---|---|---|
| J1 (list drift) | VERIFIED — "main reference artifact" entered review but was not treated as a live role without is/are/becomes, so retirement auto-safe cleared the clause | Competing role is derived from the same role pattern, minus invariant, pure retirement, and pure negation. |
| J2 (invariant wash) | VERIFIED — "Guided Notes are primary" in the same clause could erase a later "keep the main reference artifact" | Removing the invariant phrase must leave no architecture role. A later role still fails closed. |

The persistent suite checks every role alternative against `competing_live_role`, and checks that an auto-safe reason and an unapproved live role cannot both be true.

## Structural QA-of-QA
[QA/Certification Reviewer](32a29fdd-b084-4355-9042-02982c5b2bf6), read-only. Scored set: mixed non-copular 18/20, non-copular 15/15, pure retirement 10/10, invariant/negation 10/10, storage 10/10. The two misses were "never/do not replace posters" plus a later main-reference role. A follow-up found four sentences where "Guided Notes are primary" sat next to "keep the main reference artifact." Those sentences are in the persistent suite and fail closed. A third review was not run.

## Gate status (Round 10)
Live scan unchanged: **6/6, 43 sensitive, 43 allowlisted, 0 unreviewed, 0 stale, 0 auto-safe**. Allowlist file 42 entries. Fixture 87/87 BAD, 47/47 SAFE. Release parity UNCHANGED / PASS (14 gates). Classroom artifacts not modified. No allowlist edit.

---

# Round 11 — Chapter 1 v1.1 freeze approval (2026-10-05)

**EXTERNAL DECISION: APPROVE PROPAGATION.**

The external audit verified the Phase 6.1J final role-precedence / auto-safe invariant audit and authorized the Chapter 1 freeze. External result: no BLOCKER, no HIGH; role precedence PASS; architecture truth PASS; fixture 87/87 BAD and 47/47 SAFE; fresh mixed challenge 20/20; non-copular challenge 15/15; property sweep about 1,155 combinations with 0 failures; live architecture 43 sensitive / 43 allowlisted / 0 unreviewed / 0 stale / 0 auto-safe; release parity PASS (14 gates); inventory missing 0; classroom churn NONE.

| ID | Verdict | Disposition |
|---|---|---|
| Round 10 findings (J1, J2) | VERIFIED and fixed in 6.1J | Closed by the external approval. |
| Optional low-severity GN-primary fixture enhancement | NOT ADOPTED | Out of scope for the freeze (owner instruction); no fixture, guard or classroom change made. |

## Freeze action
Metadata only. Chapter 1 is `UNIT1_CH1_GOLD_STANDARD_VERSION = 1.1`, `STATUS = FROZEN` (record: `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`). Classroom artifacts rebuilt: 0. The one reviewed allowlist row that carries the P3 manifest status text was updated to the new status text (same classification, same entry count). Final certification: `qa/reports/CH1_V1_1_FREEZE_CERTIFICATION.md`.

## Playbook scope note
Playbook fixes recorded in earlier rounds (for example the Round 2 front-matter fix and the Ch1 spread/pacing rows) were verified against the combined working-tree Playbook. By owner decision (2026-10-05) the combined Playbook binary and previews are not in the Chapter 1 freeze commit because they also hold Chapter 2 pages; they ship with the Ch2 commit. The committed `tools/build_teacher_playbook.py` carries the Chapter 1 hunks only, so the committed script keeps the earlier front-matter and "Chapters 1–2" status wording until that commit. A Ch1-only build from the staged tools (isolated, outside the repo) passes all 10 Playbook QA gates (25 pp, 0 Chapter 2 pages).
