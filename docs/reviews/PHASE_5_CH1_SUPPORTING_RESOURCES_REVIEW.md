# PHASE 5 — CHAPTER 1 SUPPORTING RESOURCES REVIEW

> Independent review + certification of the completed Chapter 1 supporting-resource ecosystem.
> Guided Notes (Phase 3) + Slideshow (Phase 4) are FINAL and were not rebuilt. No Chapters 2–7 changes. No frozen-token changes.
> Reviewers: Curriculum Source Reviewer (fidelity) · QA / Certification Reviewer (independent, read-only).

## 1. What Works

- **Lean ecosystem achieved.** The Chapter 1 package is complete without redundant artifacts: Guided Notes (primary) → Slideshow → practice/application (apply) → chapter quiz (assess) → Science Journal (2 prompts, secondary) → absent-recovery → FLEX Energy Detectives → study-guide contribution + assessment trace (future unit assembly).
- **No note recopy.** The retained practice page is a genuine APPLY task (evidence judgment, stored-energy classification, explanation), not a re-fill of the notes blanks — verified by the independent reviewer.
- **Single canonical manifest.** `docs/chapter-01/CH1_PACKAGE_MANIFEST.md` now governs; the historical INB-era `curriculum/chapter-01/CHAPTER_MANIFEST.md` is banner-marked SUPERSEDED, eliminating the two-source-of-truth risk.
- **Deterministic assessment trace.** Chapter 1 → locked 25Q/50pt final mapped precisely (6 items / 12 pts: Q2, Q8, Q9, Q11, Q16, Q18), every item direct-coverage with no untested-content dependency.
- **Deterministic study-guide contribution.** `CH1_STUDY_GUIDE_CONTRIBUTION.md` records the exact Ch1 source block for later unit assembly.
- **Playbook sync is now exact.** New "Chapter 1 — Supporting Resource Index (Phase 5)" lists every resource with filename/status/graded/when-used/key/absent role. Automated playbook QA PASS (8/8 gates, 29 pages).

## 2. What's Missing

- **Nothing at the acceptance-gate level.** No required student resource, teacher key, or documentation record is absent.
- Chapter 2–7 supporting ecosystems remain future phases (out of scope, correctly untouched).
- The virtual sharpener backup remains OPTIONAL / DEFERRED (per contract); live demo preferred — no AI-generated video dependency introduced.

## 3. Fixes — specific problems + exact fixes

1. **BQ drift "find" → "observe".** *Problem:* four active Ch1 files used "find evidence" instead of the locked verbatim "observe evidence". *Fix:* corrected `production/labs/01-ch1-energy-detectives-teacher-spec.md`, `curriculum/chapter-01/teacher/01-ch1-daily-lessons.md`, `curriculum/chapter-01/media/01-ch1-explainer-script.md`, and the `01-ch1-energy-causes-change-teacher-map.md` learning target.
2. **Energy Detectives stale CORE tag.** *Problem:* spec header said "Tag: CORE" (pre-dated the restructuring reclassification). *Fix:* retagged OPTIONAL/FLEX, re-labeled "Friday FLEX", and removed "Lab 1 of the 8-lab backbone".
3. **Friday-FLEX stale day label.** *Problem:* RECOVER track called Detectives "Tuesday's AP 1.1 page" after the reclassification. *Fix:* → "Friday FLEX page".
4. **Quiz-key point total.** *Problem:* "~16 points … adjust per policy" was softer than the strict raw+% convention. *Fix:* → "16 points … raw score + percentage" (items sum cleanly to 16).
5. **Assessment-trace page range.** *Problem:* Q18 stored-energy source cited "pp. 4–6" (p. 6 is forward-preview only). *Fix:* tightened to "pp. 4–5".
6. **Absent-recovery anchor gap.** *Problem:* recovery guide stated the big idea but not the exact BQ or V/N anchor map. *Fix:* added exact BQ + a "What to complete in your Guided Notes" map (BQ/V1/V2/N1–N4 with exact fills).

## 4. Enhancements / Suggestions / New Ideas

- **Legacy-name cleanup (future).** `production/student-notes/01-ch1-…-guided-notes.docx` and `production/student-notebook/chapter-01/01-ch1-interactive-notebook.docx` share near-identical names with the canonical `premium-notes` version. Already marked RETIRED in the resource map; a future archive/rename would further de-risk.
- **VOTE HUD (already noted in Phase 4).** Formalize the A/B/C/D signal on review slides (currently speaker-note-only).
- **Study-guide over-coverage note.** The existing study guide adds `evidence`/`constraints`/`refine` beyond the assessment's 8 matching terms — acceptable per "slight over-coverage is not a flaw"; the contribution spec records this.

## 5. Edge Cases & Failure Modes

- **Cloud-only authoritative sources.** Unit 1 Reader/TG PDFs are not in the repo; fidelity review necessarily relies on `source-map.md` + `source-validation.md`. A future re-download-and-hash would harden this.
- **Q18 blueprint range.** The locked `UNIT1_FINAL_ASSESSMENT_BLUEPRINT.md` itself cites "p. 4–6"; the trace tightened to "pp. 4–5" for precision. If the blueprint is ever re-edited, re-align the trace.
- **FLEX reclassification drift.** Energy Detectives now appears in three places (spec, resource map, playbook); future edits must update all three to prevent a "CORE vs FLEX" mismatch recurring.

## 6. Performance Concerns

- Playbook build (<0.5 s), LibreOffice PDF export (~2 s), preview render (~1.5 s). All one-shot; no persistent processes, no watch-mode, no network, no Canva, no software installs.
- No new build dependencies. `design-tokens.json` untouched (FROZEN v1.0).

## 7. Readability / Maintainability

- All new docs (manifest, study-guide contribution, assessment trace) are plain Markdown with explicit source/status/provenance fields, consistent with the repo's other `docs/chapter-01/` records.
- The playbook builder (`tools/build_teacher_playbook.py`) gained one composable function (`chapter1_support_index`) in the established pattern; the existing QA script (`qa_teacher_playbook.py`) covers the new table width/overflow automatically.
- Deterministic file-existence + consistency checks are reproducible via `rg`/`pdftotext`/`pdfinfo` (documented in `qa/reports/PHASE_5_CH1_PACKAGE_QA.md`).

---

## Verdict

**Phase 5 Chapter 1 supporting-resource ecosystem: COMPLETE.** All acceptance gates PASS (resource-need audit, source fidelity, answer-key parity, playbook sync, package completeness, independent QA). Phase 6 readiness: **READY WITH CONDITIONS** — the only conditions are unit-level (Chapters 2–7 propagation), not Chapter 1 defects.
