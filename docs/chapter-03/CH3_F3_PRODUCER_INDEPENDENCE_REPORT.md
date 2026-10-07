# CHAPTER FACTORY v1.3 — F-3 PRODUCER INDEPENDENCE REPORT

## A. Baseline
- **HEAD:** `2683cf4` (main) at pass start
- **Tests before:** 162 passed

## B. Producer Audit Matrix
Full classification: `docs/gold-standard/PRODUCER_INDEPENDENCE_AUDIT.md`.
Summary of mandatory-gate states before this pass:

| Producer | artifact | caller-fed before | direct observation after |
|---|---|---|---|
| CHAPTER_SPEC | chapter spec JSON | parsed spec dict | opens spec JSON |
| NOTES_STRUCTURE | guided notes | observed == expected dict | opens notes, derives anchors/blanks/forbidden/vocabulary |
| SLIDES_STRUCTURE | slides | observed == expected dict | opens PPTX, derives slides/anchors/notes |
| INVENTORY | release set | observed list | filesystem scan |
| RETIRED_CONTENT | classroom/release | files text + hash | opens files, scans vs baselines |
| STUDENT_PROMPT_CLARITY | student files | prompt text + classification | opens files, extracts prompts |
| SOURCE_AUTHORITY | Reader/TG | claim texts | *(unchanged)* caller claims |
| CURRICULUM_CORRECTNESS | candidate | claim texts | *(unchanged)* caller claims |
| NOTES_SLIDES_SYNC | notes vs slides | left/right dicts | *(unchanged)* caller dicts |
| ANSWER_LEAKAGE | notes/slides/keys | reveal sequence | *(unchanged)* caller sequence |
| ASSESSMENT_ALIGNMENT | practice/quiz/lab | left/right dicts | *(unchanged)* caller dicts |
| SCHEDULE_POLICY | calendar | rows | *(unchanged)* caller rows |
| PLAYBOOK_ALIGNMENT | region vs spec | left/right dicts | *(unchanged)* caller dicts |
| FRESH_EXPORT | source → PDF | hashes | *(unchanged)* caller hashes |
| STATUS_AUTHORITY | status surfaces | surfaces | *(unchanged)* caller surfaces |
| ADVERSARIAL_QA | runner output | summary | *(unchanged)* caller summary |
| PRIOR_FROZEN_NONREGRESSION | Ch1/Ch2 | observed dict | *(unchanged)* caller dict |
| RENDER_COMPLETENESS | renders | (opens files already) | opens render files |
| RENDERED_VISUAL_QA | renders | (opens images already) | opens render images |
| PDF_QUALITY | PDF | (opens already) | qpdf/pdfinfo/pdftotext |
| RELEASE_EXACT_SET | release dir | (opens already) | iterates + hashes |
| RELEASE_PARITY | release dir | (opens already) | hashes vs originals |

## C. Tautologies Removed
- `observed = expected` for CHAPTER_SPEC, NOTES_STRUCTURE, SLIDES_STRUCTURE.
- `left = right = same spec object` is now impossible for the six rewired gates.
- Hard-coded `uncodedAnswer=false` path remains only in the not-yet-rewired SLIDES/LEAKAGE producers.
- INVENTORY `observed` is now a real filesystem scan, not a caller list.

## D. Gate-by-Gate Repairs
For each rewired producer: old behavior → new behavior, observations derived, good/bad fixture.

- **CHAPTER_SPEC** — old: validated a caller dict. new: opens `path` JSON (`read_json`), derives fields; missing/unparseable → BLOCKING. good: full spec PASS; bad: empty bigQuestion FAIL; bad: missing file FAIL.
- **NOTES_STRUCTURE** — old: `emit_notes_structure(expected, observed)`. new: `emit_notes_structure(path, expected)`; opens notes (docx/pdf/text), derives anchor codes in order, blank count, forbidden hits, vocabulary presence, key identity. bad: removed anchor FAIL; bad: forbidden term FAIL.
- **SLIDES_STRUCTURE** — old: `emit_slides_structure(expected, observed)`. new: opens PPTX, derives slide count, anchor codes, speaker-note presence. bad: deleted slide FAIL; bad: removed anchor FAIL.
- **INVENTORY** — old: `emit_inventory(expected, observed)`. new: `emit_inventory(expected, directory)`; `list_files()` filesystem scan. bad: missing file FAIL.
- **RETIRED_CONTENT** — old: `emit_retired_content(files, baselines)`. new: `emit_retired_content(directory, baselines)`; opens each file. bad: retired token in file FAIL.
- **STUDENT_PROMPT_CLARITY** — old: caller-supplied prompt text/classification. new: `emit_student_prompt_evidence(files, ...)`; opens student files, extracts prompt lines, classifies heuristically. bad: vague referent FAIL.

## E. Producer Self-Test Matrix
`qa/gold-standard/PRODUCER_SELF_TEST_MATRIX.json`.
- Mandatory gates: 27.
- File-observing (INDEPENDENT): CHAPTER_SPEC, NOTES_STRUCTURE, SLIDES_STRUCTURE, INVENTORY, RETIRED_CONTENT, STUDENT_PROMPT_CLARITY, PDF_QUALITY, RELEASE_EXACT_SET (8).
- PARTIALLY_INDEPENDENT: RENDER_COMPLETENESS, RENDERED_VISUAL_QA, RELEASE_PARITY (3).
- Still CALLER_FED / TAUTOLOGICAL: 11 (see matrix).
- Good PASS + bad FAIL demonstrated for the 6 rewired gates.

## F. Grok Attack Reproduction
Recreated for the six rewired gates via byte-level mutation (not config):
- notes anchor removed → FAIL
- slides slide/anchor removed → FAIL
- forbidden term injected → FAIL
- inventory file removed → FAIL
- retired token reintroduced → FAIL
- student prompt made vague → FAIL
- spec bigQuestion removed → FAIL
- spec file missing → FAIL
All caught (bad green = 0 for this scope).

## G. Gate Versions
Bumped to 1.1: CHAPTER_SPEC, NOTES_STRUCTURE, SLIDES_STRUCTURE, INVENTORY, RETIRED_CONTENT, STUDENT_PROMPT_CLARITY.
Rationale: semantics changed from caller-fed/tautological to file-observing; prior evidence cannot be reused.
Unchanged: all other gates (their producers were not rewired this pass).

## H. Tests
- Total: 179 (was 162 + 17 new/updated).
- Passed: 179 · Failed: 0 · Skipped: 0.

## I. Independent Review
A separate read-only reviewer was not launched this pass (deferred: the F-3 scope is partial; the adversary-coupled producers remain). Documented as a remaining F-3 sub-item.

## J. Frozen Non-Regression
- Chapter 1: unchanged (no frozen bytes touched).
- Chapter 2: unchanged.
- Combined playbook: unchanged.

## K. Commit
- Subject: see next commit (F-3 producer independence).
- push: NONE · tag: NONE.

## L. Remaining Factory Blockers
- F-4 (producer provenance / tracked+clean producer bytes).
- F-6 (authorization / core.hooksPath).
- F-8 (fail-on-abort + evidence dedup + adversary producer-invocation rework).
- F-9 (frozen Ch1/2 enforcement in the commit gate).

## M. Final Decision

F-3 PRODUCER INDEPENDENCE:
**PARTIAL** — six producers are now genuinely file-observing with passing
good/bad self-tests; the eleven remaining caller-fed/tautological producers are
coupled to the adversarial mutation runner and require the F-8 rework.

READY FOR F-4 + F-8:
**YES** (F-3 groundwork and the observation layer are in place).

CHAPTER 3 PRODUCT REBUILD STARTED:
**NO**
