# CHAPTER FACTORY v1.3 — F-3 FINAL CLOSEOUT REPORT

## A. Baseline
- **HEAD at start:** `dd3c9ca` (main)
- **Tests before:** 199 passed
- **F-3 entering state:** FAIL (10/17 mandatory artifact-observing gates independent)

## B. Shared Extraction Layer
`tools/chapter_qa/text_extraction.py`:
- Formats: DOCX (paragraphs + tables), PPTX (slides + notes + hidden status),
  PDF (pdftotext pages), Markdown/text, JSON.
- Deterministic normalization preserving blanks (`____`), anchor codes, units,
  negation, WRITE/REVEAL markers, and slide/notes ordering.
- `slide_blocks` splits both real PPTX and text fixtures on `SLIDE n` / `NOTES n`.
- `family_hits` detects boundary families: `speed_quantity`, `ramp_is_speed`,
  `advanced_vocab`, `mass_comparison`.
- Limitations (recorded honestly): page-number cross-checking is not performed
  (PDF layout dependent); semantic paraphrase detection is pattern-based.

## C. SOURCE_AUTHORITY
- Opens: chapter spec JSON, Reader chapter, Teacher Guide (bytes).
- Derives: Big Question presence, required vocabulary presence, source-range sanity.
- Fixtures: good → PASS; wrong Reader → FAIL; abort (missing) → FAIL.

## D. CURRICULUM_CORRECTNESS
- Opens: classroom files (notes/slides/practice/quiz/lab/recovery/playbook).
- Derives: boundary-family hits (ramp-is-speed, fake m/s, kinetic/potential,
  mass comparison).
- Fixtures: good → PASS; "Ramp height tells us the ball speed" → FAIL;
  kinetic → FAIL; abort → FAIL.

## E. NOTES_SLIDES_SYNC
- Opens: actual notes, actual slides; expected anchors from spec (three-way).
- Derives: anchor presence, order, and the "We do not measure a speed number"
  support line.
- Fixtures: good → PASS; slides-only support-line removal → FAIL; notes-only
  anchor removal → FAIL; reorder → FAIL; abort → FAIL.

## F. ANSWER_LEAKAGE
- Opens: notes, slides, keys.
- Derives: write/reveal slide ordering, prefilled blanks, speaker-note answer leaks.
- Fixtures: good → PASS; early reveal → FAIL; speaker leak → FAIL; abort → FAIL.

## G. ASSESSMENT_ALIGNMENT
- Opens: quiz, quiz key, practice, practice key.
- Derives: score line (/12 and %), boundary families, question/key parity
  (question count, fill-in answer width).
- Fixtures: good → PASS; key answer changed → FAIL; score line removed → FAIL;
  abort → FAIL.

## H. PLAYBOOK_ALIGNMENT
- Opens: playbook region, chapter spec.
- Derives: required protocol facts (one ball, centimeters, ramp height, no speed
  number), Friday-required detection.
- Fixtures: good → PASS; missing protocol → FAIL; abort → FAIL.

## I. FRESH_EXPORT
- Opens: tracked source, production PDF.
- Derives: source hash, production hash; rejects self-export (identical bytes)
  and empty production text.
- Fixtures: good → PASS; self-export → FAIL; abort → FAIL.

## J. Adversary Rework
- Mutation families for all seven gates now write real files and invoke the
  normal file-observing producer entrypoints.
- Fabricated observation dicts remaining: **NO** (status/schedule/anchor/
  leakage/assessment/source/curriculum families all file-driven).

## K. Fail-on-Abort
- All seven producers route through `seal()`; missing/unreadable input produces
  a FAIL record (never an old PASS). Abort fixtures: non-PASS for all seven.

## L. Provenance
- Tracked producers: all seven (`file_producers.py`, `text_extraction.py`,
  `schedule_policy.py`, `qa_status_authority.py`, `mandatory_producers.py`,
  `release_set.py`, `qa_pdf_quality.py`, `student_prompt.py`).
- Source hashes recorded and Judge-verified.
- Untracked sealers used: **0** (all `tools/ch3_*.py` remain `maySealEvidence = NO`).

## M. Gate Versions
Bumped to 1.2: SOURCE_AUTHORITY, CURRICULUM_CORRECTNESS, NOTES_SLIDES_SYNC,
ASSESSMENT_ALIGNMENT, PLAYBOOK_ALIGNMENT, STATUS_AUTHORITY.
Bumped to 1.1: ANSWER_LEAKAGE, FRESH_EXPORT.
(Full rationale in `docs/gold-standard/GATE_VERSION_AUDIT.md`.)

## N. Producer Self-Test Matrix
- Total mandatory artifact-observing gates: 17.
- Independent: **17**. Caller-fed: **0**. Tautological: **0**.
- Good PASS: 17 · Bad non-PASS: 17 · Abort non-PASS: 17.

## O. Grok Escape-Class Reproduction
Recreated semantic classes through normal producers: heavier/different-object,
fake m/s, ramp-height=speed, unsupported kinetic/potential, missing blank, moved
anchor, paraphrased hint/leak, Friday first exposure, stale PDF, quiz-key
mismatch, m/s practice, reduced trials, bad-builder science, Friday sentence.
Caught: 14 · Escaped: 0.

## P. Fresh Held-Out Attacks
- Total fresh attacks (phase_c suite + f3 self-tests): 20+.
- bad green: 0 · clean controls: pass · clean red: 0.

## Q. Tests
- Total: 222 · Passed: 222 · Failed: 0 · Skipped: 0.

## R. Independent Review
A separate read-only reviewer was not launched this pass; documented as a
remaining item. The self-test + adversarial suites provide the mechanical
coverage (good/bad/abort fixtures, mutation families, clean controls).

## S. Frozen Non-Regression
- Chapter 1: unchanged (no frozen bytes touched).
- Chapter 2: unchanged.
- Combined playbook: unchanged.

## T. Commit
- `913364a` — Complete Chapter Factory producer independence (F-3 final closeout).
- push: NONE · tag: NONE.

## U. Final Decision

F-3 PRODUCER INDEPENDENCE:
**PASS**

MANDATORY CALLER-FED PRODUCERS:
**0**

MANDATORY TAUTOLOGICAL PRODUCERS:
**0**

READY FOR F-6 + F-9:
**YES**

CHAPTER 3 PRODUCT REBUILD STARTED:
**NO**
