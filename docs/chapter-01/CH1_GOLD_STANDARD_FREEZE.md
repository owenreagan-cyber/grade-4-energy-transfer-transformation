# CHAPTER 1 — GOLD-STANDARD FREEZE

> Authoritative freeze record for Chapter 1 (`Energy Causes Change`, Reader pp. 1–6 · TG L1–L2).
> This is the single source of truth for the frozen Chapter 1 version. Do not create a competing version source.

## Declaration (current)

```
UNIT1_CH1_GOLD_STANDARD_VERSION = 1.1
STATUS                         = FROZEN
EXTERNAL APPROVAL              = APPROVE PROPAGATION
FREEZE DATE                    = 2026-10-05
```

## v1.1 freeze record

- **External decision (verbatim): APPROVE PROPAGATION.** Issued by the external adversarial audit after verifying the Phase 6.1J final role-precedence / auto-safe invariant audit.
- **External result:** no BLOCKER · no HIGH · role precedence PASS · architecture truth PASS · fixture 87/87 BAD and 47/47 SAFE · fresh mixed challenge 20/20 · non-copular challenge 15/15 · property sweep ≈1,155 combinations / 0 failures · live architecture 43 sensitive / 43 allowlisted / 0 unreviewed / 0 stale / 0 auto-safe · release parity PASS (14 gates) · inventory missing 0 · classroom churn NONE.
- **Freeze action:** metadata only. Classroom artifacts rebuilt for the freeze: **0**. Updated: this record, `CH1_PACKAGE_MANIFEST.md`, `production/PRODUCTION_MANIFEST.md`, `production/final-package/ENERGY_UNIT_MASTER_INDEX.md`, `production/releases/chapter-01/RELEASE_MANIFEST.json` + `README.md` (status text; no release file touched), `tools/build_ch1_release.py` (version/status constants), and the reviewed allowlist row for manifest row P3 (status text only).
- **Final certification and inventory:** `qa/reports/CH1_V1_1_FREEZE_CERTIFICATION.md` · `qa/reports/CH1_V1_1_FREEZE_INVENTORY.md`. External audit history: `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` (Round 11 = freeze approval).
- **Playbook exception (owner decision, 2026-10-05):** the Chapter 1 spread in the Teacher Playbook was rebuilt in Phase 6.1 and passed the Playbook Chapter 1 gate on the working tree. `production/teacher-playbook/unit1-teacher-playbook.{docx,pdf}` and `previews/` are one combined binary that also contains Chapter 2 Phase 7 pages, so they are **not** part of the Chapter 1 freeze commit; they ship with the Chapter 2 commit. Until then the committed Playbook binary is the v1.0 build (29 pp, Block 1 / Block 2 pacing), and Chapter 1 timing is governed by `CH1_PACING_PLAN.md`. The committed `tools/build_teacher_playbook.py` / `tools/qa_teacher_playbook.py` carry the Chapter 1 v1.1 changes only.
- **Tag:** none (the repository has no documented chapter-freeze tagging convention).

## History (superseded by the current declaration above; preserved)

> **Phase 6.1 (2026-10-04):** v1.0 passed internal certification and was frozen. An external adversarial audit (14 findings) triggered corrective maintenance. v1.0 is **not** retracted; the v1.0 declaration below (`STATUS = FROZEN`, freeze basis, QA table) is preserved as history. Chapter 1 returned to `FROZEN` as **v1.1** after every internal gate passed **and** the external audit returned exactly "APPROVE PROPAGATION" (condition met 2026-10-05). See "Phase 6.1 corrective maintenance" at the end of this file.

### v1.0 declaration (historical, preserved)

```
UNIT1_CH1_GOLD_STANDARD_VERSION = 1.0
STATUS                         = FROZEN   (as of 2026-10-04, before Phase 6.1)
```

- **Freeze date:** 2026-10-04
- **Freeze basis:** Phase 6 final independent certification — all required acceptance gates PASS (see `docs/reviews/PHASE_6_CH1_GOLD_STANDARD_CERTIFICATION.md`).

## Canonical artifacts

The complete, canonical Chapter 1 file inventory is **`docs/chapter-01/CH1_PACKAGE_MANIFEST.md`** (21 canonical files, all verified on disk). It is the single authoritative list; this freeze record does not duplicate it. Key groups:

| Group | Canonical location |
|---|---|
| Guided Notes (student + key) | `production/premium-notes/01-ch1-energy-causes-change-guided-notes{-key}.{docx,pdf}` (3 pp each) |
| Slideshow | `production/slides/01-ch1-energy-causes-change-slides.{pptx,pdf}` + `previews/ch1-slides-*.png` (45 slides) |
| Teacher Playbook (Ch1 section) | `production/teacher-playbook/unit1-teacher-playbook.{docx,pdf}` (committed binary = v1.0 build, 29 pp; the v1.1 Ch1 spread ships with the Ch2 commit — see the Playbook exception) |
| Practice + key | `production/worksheets/01-ch1-energy-causes-change-practice.docx` · `production/answer-keys/01-ch1-energy-causes-change-practice-key.md` |
| Quiz + key + blueprint | `production/quizzes/01-ch1-energy-causes-change-quiz.{docx}` · `…-quiz-key.md` · `…-quiz-blueprint.md` (9-item · 16 pts) |
| Absent recovery | `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md` |
| Energy Detectives + key + spec | `production/worksheets/01-ch1-energy-detectives-student.docx` · `production/answer-keys/01-ch1-energy-detectives-key.md` · `production/labs/01-ch1-energy-detectives-teacher-spec.md` (OPTIONAL/FLEX) |
| Friday FLEX | `curriculum/chapter-01/student/01-ch1-friday-flex.md` |
| Study-guide contribution | `docs/chapter-01/CH1_STUDY_GUIDE_CONTRIBUTION.md` |
| Assessment trace | `docs/chapter-01/CH1_ASSESSMENT_TRACE.md` |

## Locked anchors (all resources agree)

- **BQ:** "Where can we observe evidence of energy causing change?"
- **V1:** energy · change (Reader p. 1) — **V2:** stored energy (Reader p. 4)
- **N1** Energy Causes Change (ENERGY → CHANGE → EVIDENCE) · **N2** Energy Occurs in Different Forms (motion · sound · light · heat · electrical energy) · **N3** Objects Can Store Energy (STORED → RELEASE → CHANGE) · **N4** Recognizing Evidence (BEFORE/AFTER)

## QA reports (all PASS)

| Report | Result |
|---|---|
| `qa/reports/PHASE_3_CH1_GUIDED_NOTES_QA.md` | PASS |
| `qa/reports/PHASE_4_CH1_SLIDESHOW_QA.md` + `…_INDEPENDENT_QA.md` + `…_SOURCE_FIDELITY.md` | PASS |
| `qa/reports/PHASE_5_CH1_PACKAGE_QA.md` | PASS |
| `qa/reports/PHASE_2_PLAYBOOK_QA.md` | PASS (re-run after Phase 6 collect/grade fix) |
| Visual-system QA (`tools/qa_visual_system.py`, FROZEN v1.0) | PASS (unchanged) |

## Known non-blocking warnings

- **None.** Every WARN surfaced during Phases 3–6 was corrected before freeze (worksheet header/BQ alignment, quiz-key point sum, absent-recovery Q4 reference, Energy Detectives BQ "find" → "observe", Friday-FLEX stale label, and the Phase 6 Playbook "No scored chapter item" → "Scored chapter item" fix).

## Rules for future edits (after freeze)

Any change to frozen Chapter 1 requires:

1. An **explicit, substantiated reason** (not preference-only redesign).
2. Rebuild of the **affected artifact(s)** from their editable master.
3. **Re-run of the affected QA gate(s)** (and the automated QA master run if any anchor/layout changes).
4. **Playbook resync** if the change touches filenames, page/slide counts, anchors, or statuses.
5. **Manifest update** if the file inventory changes.

Frozen and must NOT be altered in place:
- Unit 1 Visual System v1.0 (`assets/visual-system/design-tokens.json`).
- Authoritative CKSci Student Reader / Teacher Guide.

---

## Phase 6.1 corrective maintenance (appended; v1.0 text above is unchanged history)

- **Trigger:** independent external Grok audit of v1.0, 14 findings (F1–F14). Each independently verified; dispositions in `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md`.
- **Summary report:** `docs/reviews/PHASE_6_1_CH1_EXTERNAL_AUDIT_REMEDIATION.md`. Inventory: `qa/reports/PHASE_6_1_ARTIFACT_INVENTORY.md`.
- **Superseded facts (v1.0 → v1.1):** Playbook 29 pp → 33 pp on the working tree (combined with Chapter 2 pages; see the Playbook exception above); quiz release copy and all release PDFs rebuilt from canonical masters; Interactive Science Notebook PDF retired from the release; Ch1 timing = three sessions (Mon · Tue · Fri) per `CH1_PACING_PLAN.md`; notes content blanks 5; Energy Detectives optional/ungraded.
- **Freeze condition for v1.1:** all internal gates PASS **and** external audit result exactly "APPROVE PROPAGATION". *(Historical; condition met 2026-10-05 — see the v1.1 freeze record at the top.)*


### Phase 6.1 round 2 (post-review) — historical (superseded by the v1.1 freeze)
*As of that round (before the external approval):* internal reviewer findings were fixed (schedule docs synced, quiz item 9 rewritten, slides 4/13/23/25/28 and review Q4 reworded, Detectives "After:" added, release PDFs sanitized). The Friday Session 3 owner decision is now made (2026-10-04 Friday policy; Ch1 compliant). At that point the external audit (`docs/reviews/GROK_CH1_V1_1_AUDIT_PACKET.md`) had not yet returned, and the declaration then in force read `VERSION = 1.0` / `STATUS = CORRECTIVE MAINTENANCE IN PROGRESS`; both were superseded on 2026-10-05.
