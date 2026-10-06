# Phase 7.1 baseline inventory (before remediation edits)

Taken at HEAD `279a9deca5fa30fd1217d5c8c6264dc856bd982e` ("Freeze Chapter 1 v1.1 gold standard"), before Chapter 2 edits in this phase. Chapter 1 classroom files were not in the dirty tree.

## Dirty-tree classification

**A. Preserved Chapter 2 Phase 7 work** (uncommitted): `curriculum/chapter-02/` edits, `docs/chapter-02/`, `docs/reviews/PHASE_7_CH2_GOLD_STANDARD_PROPAGATION.md`, premium notes + key + previews, slides pptx/pdf + previews, quiz docx, quiz key, Moving Marbles spec and student docx, labs spec, chapter QA reports, `tools/build_ch2_*.py`, `tools/qa_ch2_*.py`.

**B. Playbook deferred from the Chapter 1 commit:** `production/teacher-playbook/unit1-teacher-playbook.docx` + `.pdf`, previews `playbook-01` through `playbook-33`, `qa/reports/PHASE_2_PLAYBOOK_QA.md`, `tools/build_teacher_playbook.py`.

**C. Unrelated / pre-existing:** none in the dirty tree at start. Chapters 3–7 files were clean.

**D. Unexpected:** `docs/chapter-02/CH2_GOLD_STANDARD_FREEZE.md` claimed `STATUS = FROZEN` even though the external Grok review never ran. Treated as a false status, not as a freeze.

## Earlier findings, classified against the tree at start

| Finding | Class | Evidence |
|---|---|---|
| Schedule disagreement | VERIFIED | Calendar and Playbook still said Block 1 / Model It / Draw/Label / PLANNED Phase 4. Week-by-week map put Chapter 2 on a 45-minute Week 2. Slide 1 said WEEK 2. Thursday curriculum map assigned Moving Marbles and "transfers energy." |
| Timing | VERIFIED | Speaker-note times for slides 1–13 summed to 31 min and slides 14–27 to 37 min. No `ch2_pacing.py`. Placeholder "two 30-min blocks." |
| Stale release | VERIFIED | `production/releases/chapter-02/` held a pre-canonical notes PDF, an old deck, a teacher-key PDF, and `02-ch2-interactive-science-notebook.pdf`. No `RELEASE_MANIFEST.json`. |
| Model It / Draw/Label | VERIFIED in schedule rows; NOT in the notes | Notes use BQ / V1 / V2 / N1 / N2 / N3. The BEFORE/AFTER draw is the real observation task. Its row was 1200 twips (~0.83 in), under the 2 in drawing minimum. |
| Placeholder timing | VERIFIED | Same as Timing. |
| Legacy manifest P1/P3 | VERIFIED | `PRODUCTION_MANIFEST.md` P1 pointed at the superseded teacher map. P3 pointed at `production/student-notes/02-ch2…docx` (file absent). P11 listed the notebook as RELEASED. |
| Sparse pages | PARTIAL | Notes pp. 1–2 left a large empty region because V2 started page 2 and the draw boxes were short. Playbook sparse WARN was not re-measured until the rebuild. |
| Release parity | VERIFIED fail | No manifest, retired notebook still in the release directory. |

## Chapter 1 excluded from editing

Frozen classroom masters under `production/premium-notes/01-ch1*`, `production/slides/01-ch1*`, `production/releases/chapter-01/`, `tools/ch1_pacing.py`, `tools/build_ch1_release.py`, and `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`. The combined Playbook generator still emits the Chapter 1 spread from unchanged functions.
