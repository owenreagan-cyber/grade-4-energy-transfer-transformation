# Phase 5 — Chapter 1 Supporting-Resource Ecosystem — QA / Certification Report

> Independent package certification for the completed Chapter 1 "Energy Causes Change" supporting-resource ecosystem.
> Phase 5 scope: complete supporting resources around the FINAL Guided Notes (Phase 3) + Slideshow (Phase 4). No notes/slides rebuild.

## Gate summary

| Gate | Result |
|---|---|
| RESOURCE-NEED AUDIT | **PASS** |
| SOURCE FIDELITY | **PASS** (1 WARN corrected) |
| STUDENT ARTIFACT QA | **NOT APPLICABLE** (no new student handout created) |
| ANSWER-KEY PARITY | **PASS** (4/4 keys present + mirrored) |
| PLAYBOOK SYNC | **PASS** (regenerated DOCX + PDF + 29 previews; automated QA PASS) |
| PACKAGE COMPLETENESS QA | **PASS** (21/21 required files exist; consistency checks clean) |
| INDEPENDENT QA | **PASS** (10/10 dimensions; no FAIL) |

---

## 1. Resource-need audit (Section 3–9)

Decision per candidate resource:

| Candidate | Decision | Rationale |
|---|---|---|
| Chapter practice / application | **KEEP** (already exists) | Distinct APPLY job — evidence judgment + stored energy + explain; not note recopy (§K of restructuring audit) |
| Science Journal prompt | **ALREADY COVERED** | 2 daily prompts in `MASTER_CURRICULUM_MAP.md` ("draw one change" · "one stored-energy example"); secondary role served; no new prompt |
| Absent / makeup support | **KEEP + REFINE** | Existing recovery guide retained; added exact BQ + V1/V2/N1–N4 anchor map |
| Teacher demo support | **ALREADY COVERED** | Playbook "Ch1 Demo Guide — Electric Pencil Sharpener" already does the job; no extra card |
| FLEX / Energy Detectives | **RECLASSIFY → OPTIONAL/FLEX** | Restructuring audit §E/§J/§U; retagged in spec + resource map + playbook |
| Study-guide contribution | **CREATE** | `CH1_STUDY_GUIDE_CONTRIBUTION.md` |
| Assessment trace | **CREATE** | `CH1_ASSESSMENT_TRACE.md` |
| Package manifest | **CREATE** | `CH1_PACKAGE_MANIFEST.md` (canonical) |

No separate practice page was created (one already exists and is justified). No new scored resource → no new teacher key.

## 2. Package completeness checks (Section 18)

- ✅ Required files exist — 21/21 verified on disk (notes+key, slides+pdf+previews, practice+key, quiz+key+blueprint, detectives+key+spec, recovery, friday-flex, playbook docx+pdf, manifest, study-guide contribution, assessment trace).
- ✅ No duplicate competing canonical artifacts — historical `curriculum/chapter-01/CHAPTER_MANIFEST.md` now carries a SUPERSEDED banner pointing to `CH1_PACKAGE_MANIFEST.md`.
- ✅ Notes/slides/playbook agree — exact BQ, V1/V2 (energy·change / stored energy), N1–N4 anchors mirror across handoff contract, playbook slide map, and recovery guide.
- ✅ Reader range pp. 1–6 consistent.
- ✅ Exact BQ "Where can we observe evidence of energy causing change?" consistent (drift "find"→"observe" corrected in 4 files).
- ✅ V1/V2 · N1–N4 consistent.
- ✅ No stale INB-primary language in active resources.
- ✅ No stale 26-item language in active resources (locked final = 25 Q / 50 pts).
- ✅ All scored resources have matching keys (guided-notes key, practice key, quiz key, detectives key).
- ✅ All required resources referenced in the playbook (new "Chapter 1 — Supporting Resource Index" section).
- ✅ Optional resources labeled OPTIONAL/FLEX.
- ✅ Absent/makeup path exists.
- ✅ Study-guide contribution exists.
- ✅ Assessment trace exists (6 items / 12 pts, direct coverage).

## 3. Source fidelity (Curriculum Source Reviewer)

- Verdict: **PASS** (initial WARN corrected).
- WARN found: Energy Detectives teacher spec BQ "find" → fixed to "observe" (plus same drift fixed in `01-ch1-daily-lessons.md`, `01-ch1-explainer-script.md`, and a `01-ch1-energy-causes-change-teacher-map.md` learning target).
- Verified clean: exact BQ; exact definitions (energy/change/stored energy); evidence+position correctly Language-of-Instruction; no forbidden terminology; no later-chapter leakage; 6-item assessment trace maps to Reader pp.1–6 with correct anchors.

## 4. Answer-key parity (Section 12)

| Scored artifact | Key required | Key exists | Mirrors student | Accepted/sample answers |
|---|---|---|---|---|
| Guided Notes | YES | YES (`-key.docx/pdf`) | YES | YES |
| Practice | YES | YES (`-practice-key.md`) | YES | YES |
| Quiz | YES | YES (`-quiz-key.md`) | YES | YES |
| Energy Detectives (FLEX) | YES | YES (`-detectives-key.md`) | YES | YES |

**PASS.** No new Phase 5 scored resource → no new key required.

## 5. Playbook synchronization (Section 16)

- `tools/build_teacher_playbook.py` updated: cover scope, resource-map table (added Chapter quiz + Energy Detectives FLEX rows), answer-key index (added Ch1 Energy Detectives key), special-sections absent/makeup (Ch1 AVAILABLE), and a new **"Chapter 1 — Supporting Resource Index (Phase 5)"** section.
- Regenerated: `unit1-teacher-playbook.docx` + `.pdf` (29 pages) + 29 PNG previews.
- Automated QA (`tools/qa_teacher_playbook.py`): **PASS** (8/8 gates — page size, font floors, table width, token use, grayscale, banned language, assessment terms, PDF render).

## 6. Independent QA (QA / Certification Reviewer, read-only)

- Verdict: **PASS** — 10/10 dimensions (instructional completeness, redundancy, teacher usability, student workload, absent-student recovery, visual consistency, answer-key completeness, source fidelity, file organization, playbook usability).
- 3 low-severity WARNs, all corrected in this phase: (1) Detectives BQ "find" → "observe"; (2) Friday-FLEX stale "Tuesday's AP 1.1" label → "Friday FLEX page"; (3) quiz-key "~16 points" → "16 points" (clean sum).
- `design-tokens.json` verified unmodified (FROZEN v1.0).

## Verdict

**Phase 5 Chapter 1 supporting-resource ecosystem: COMPLETE.** All required gates PASS.
