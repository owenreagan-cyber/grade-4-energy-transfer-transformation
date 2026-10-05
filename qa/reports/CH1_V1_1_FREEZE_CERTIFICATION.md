# CHAPTER 1 v1.1 — FINAL FREEZE CERTIFICATION

> Date: 2026-10-05. Scope: freeze + scoped commit of Chapter 1 only. Metadata-only freeze; **classroom artifacts rebuilt: 0**.
> External decision (verbatim): **APPROVE PROPAGATION** (Phase 6.1J final role-precedence / auto-safe invariant audit).
> Declared state: `UNIT1_CH1_GOLD_STANDARD_VERSION = 1.1` · `STATUS = FROZEN` (record: `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`).

## 1. Final no-change certification (run twice: before staging and again on the staged state; identical)

| # | Gate | Result |
|---|---|---|
| A | Architecture guard (`tools/qa_ch1_note_architecture.py`) | PASS · 6/6 authorities · 43 sensitive · 43 allowlisted occurrences · 42 unique entries · 0 unreviewed · 0 stale · 0 auto-safe |
| B | Fixture (`tools/qa_notebook_primary_fixture.py`) | PASS · 87/87 BAD · 47/47 SAFE |
| C | Negative / property suite (`tools/qa_ch1_note_architecture_negative_tests.py`) | PASS (29 categories, every one at full score; role-alternative consistency and auto-safe-excludes-live-role included) |
| D | Stale / content scan (`tools/qa_ch1_stale_refs.py`) | PASS · 28 active scopes · 0 hits |
| E | Guided Notes QA (`tools/qa_ch1_guided_notes.py`) | PASS · 28 PASS / 0 WARN / 0 FAIL |
| F | Slideshow QA (`tools/qa_ch1_slides.py`) | PASS · 28 PASS / 0 WARN / 0 FAIL |
| G | Notes ↔ slides sync (BQ/V/N anchors + order · BQ exact wording · note wording mirror · no front-loaded answers; part of F) | PASS |
| H | Assessments / keys / scoring (`tools/qa_ch1_assessments.py`) | PASS · 31 PASS / 0 WARN / 0 FAIL |
| I | Friday / pacing (`tools/ch1_pacing.py::check_plan`; `CH1_PACING_PLAN.md` and the simulation report equal the generator output) | PASS · problems: none · sessions 24.5 / 24.5 / 25.0 min · Friday slides 2, 28–31, 33 each traced to Mon–Tue content |
| J | Teacher Playbook Chapter 1 gate (`tools/qa_teacher_playbook.py`) | PASS · 10/10 on the working-tree Playbook (see §4 for the binary exception) |
| K | Release parity (`tools/qa_release_parity.py --chapter 1`) | PASS · 14 gates · manifest version 1.1 · status FROZEN · 9 files · hashes match · canonical == release |
| L | Artifact inventory (`tools/qa_phase_inventory.py qa/reports/CH1_V1_1_FREEZE_INVENTORY.md`) | PASS · in scope 244 (the retired-Notebook delete + add pair as one rename once staged) · excluded (Ch2 / Phase 7) 75 · missing 0 |

External result carried into the record (not re-run here): no BLOCKER · no HIGH · fresh mixed challenge 20/20 · non-copular challenge 15/15 · property sweep ≈1,155 combinations / 0 failures.

## 2. Classroom artifact churn

- Pre-freeze snapshot of 102 Chapter 1 classroom/release files (SHA-256) compared after all freeze edits: **0 differences**.
- Only `production/releases/chapter-01/README.md` and `RELEASE_MANIFEST.json` changed in the release directory (status text only). `tools/build_ch1_release.py` was **not run**; its VERSION / STATUS constants were edited by hand, and the hand-edited README was checked byte-for-byte against the builder's template.
- Staged binaries equal the working-tree files (no unstaged Ch1 binary diffs).

## 3. Freeze consistency

Current authoritative sources now read version 1.1 / FROZEN / APPROVE PROPAGATION: `CH1_GOLD_STANDARD_FREEZE.md`, `CH1_PACKAGE_MANIFEST.md`, `PRODUCTION_MANIFEST.md` (P1, P3, P13, lifecycle note), `ENERGY_UNIT_MASTER_INDEX.md`, `RELEASE_MANIFEST.json`, release `README.md`, `tools/build_ch1_release.py`. The reviewed allowlist row for manifest row P3 was updated to the new status text (same classification; 42 entries). Historical reports (`PHASE_6_1*`, v1.0 freeze text, audit rounds 1–10) were not rewritten; the freeze record's superseded sections are labelled historical.

## 4. Staging scope and the Playbook exception

- Staged by explicit path list only (no `git add .`, no `git add -A`): 208 entries (89 A · 118 M · 1 rename: the retired Notebook PDF moved to `production/archive/retired/chapter-01-release-v1.0/`).
- Staged paths in Chapter 2 / Phase 7 sets: **0** (75 paths excluded by the inventory regexes, all left unstaged).
- Owner decision (2026-10-05): the Teacher Playbook binaries (`production/teacher-playbook/unit1-teacher-playbook.{docx,pdf}`, `previews/playbook-*.png`) and `qa/reports/PHASE_2_PLAYBOOK_QA.md` are **not** committed; they mix Chapter 1 with Chapter 2 pages (PDF pp. 21–28) and ship with the Ch2 commit.
- `tools/qa_teacher_playbook.py` is staged whole (its diff is Chapter 1 only). `tools/build_teacher_playbook.py` is staged hunk-wise: Chapter 1 hunks 1, 3–6, 10–22 and the Energy Detectives row of hunk 9; the Chapter 2 Phase 7 hunks (cover callout, status callout, Ch1–2 resource rows, Ch2 absent-support row, placeholder range, the four Chapter 2 builders and their calls) remain unstaged.
- Evidence the staged playbook tools are sound: exported to an isolated directory outside the repo, they build a Chapter 1-only Playbook that passes all 10 Playbook QA gates (25 pp, 0 Chapter 2 Phase 7 pages). That build was not copied into the repo.

## 5. Staged-diff review

- `git diff --cached`: 208 files · +9,478 / −477 · 81 binary entries, all Chapter 1 release / notes / slides / quiz / worksheets / previews / visual-QA / retired-archive files.
- Secret-pattern scan over staged text files: no hits. No cache, temp or log files. The only deletion is the retired Notebook PDF (a pure rename into the retired archive).
- Chapter 2 Phase 7 content markers in added lines: none in instructional content. Benign mentions only: (a) tool-generated "excluded paths" lists in the `*_INVENTORY_COMPLETENESS.md` reports, (b) a legacy Chapter 2 register-row quote in the Phase 6.1G–J scan reports (the guard's "OUT OF SCOPE — PHASE 7.1+" exclusion), (c) an audit-history row that quotes the earlier Playbook front-matter finding.
- Shared governance / production / planning files (AGENTS.md, `.cursor/rules`, `docs/planning/*`, `docs/playbook/*`, `production/PRODUCTION_MANIFEST.md`, `production/final-8.5-week/*`, `production/final-package/*`, FLEX bank, hash CSV): every diff inspected; Chapter 1 only.

## 6. Residual risks

1. The committed Playbook binary is the v1.0 build until the Ch2 commit; Chapter 1 timing there is superseded by `CH1_PACING_PLAN.md`. Recorded in the freeze record, package manifest and production manifest (P1).
2. The committed `tools/build_teacher_playbook.py` keeps the earlier front-matter / status wording that the combined working-tree build replaced; it passes all Playbook gates as committed.
3. No tag was created (no documented tagging convention). No push (no remote).
