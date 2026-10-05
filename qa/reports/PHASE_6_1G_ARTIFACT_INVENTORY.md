# PHASE 6.1G — ARTIFACT INVENTORY (concept-level note-architecture gate)

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: `tools/qa_phase_inventory.py` on this file.
> Status key: PASS · n/a · PENDING-GROK (included in the external audit; Grok is read-only; v1.1 is **not frozen**).
> Type: **M** modified · **C** created · **A** affected-by-reference.
> Section 1 = artifacts changed in 6.1G. Section 2 = carry-forward of the Phase 6.1F inventory.

## 1. Phase 6.1G changes

| Finding | Artifact | Type | Content QA | External audit |
|---|---|---|---|---|
| Concept-level sensitivity gate | `tools/qa_ch1_note_architecture.py` (a clause that names Guided Notes, the Science Journal, or the retired notebook family enters review; fail-closed unless allowlisted or clearly retirement/negation/invariant) | M | PASS (fixture 46/46 BAD, 27/27 SAFE; live 6 authorities, 42 sensitive clauses, 0 unreviewed, 0 stale; 7 Chapter 2–7 row exclusions) | PENDING-GROK |
| Reviewed allowlist | `qa/baselines/ch1_note_architecture_allowlist.json` (41 entries covering 42 current clauses; 25 new entries reviewed in 6.1G) | M | PASS (mutate → FAIL; delete/move/rewrite → stale) | PENDING-GROK |
| Persistent negative suite | `tools/qa_ch1_note_architecture_negative_tests.py` (reactivation, demotion, journal promotion, generic role, safe/neutral, mutations, stale allowlist, chapter-scoped rows, banners, reviewer sentences) | C | PASS | PENDING-GROK |
| Fixture | `tools/qa_notebook_primary_fixture.py` (46 BAD / 27 SAFE, including the 12 Grok silent-pass sentences and the hierarchy cases) | M | PASS | PENDING-GROK |
| QA reports | `qa/reports/PHASE_6_1G_CH1_STALE_REFERENCE_SCAN.md` · `qa/reports/PHASE_6_1G_CH1_CONTENT_STALE_SCAN.md` | C | PASS (architecture scan 0 unreviewed; content-stale scan 0 hits) | PENDING-GROK |
| audit response | `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | M | n/a (Round 7 section) | PENDING-GROK |
| inventory | `qa/reports/PHASE_6_1G_ARTIFACT_INVENTORY.md` · `qa/reports/PHASE_6_1G_INVENTORY_COMPLETENESS.md` | C | n/a | PENDING-GROK |

> No authority prose was edited. No classroom artifact was rebuilt. Chapter 2–7 register rows are excluded structurally (heading + table row), labeled OUT OF SCOPE — PHASE 7.1+.

## 2. Carry-forward (Phase 6.1F inventory)

# PHASE 6.1F — ARTIFACT INVENTORY (fail-closed note-architecture guardrail)

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: `tools/qa_phase_inventory.py` on this file.
> Status key: PASS · n/a · PENDING-GROK (included in the external audit; Grok is read-only; v1.1 is **not frozen**).
> Type: **M** modified · **C** created · **A** affected-by-reference.
> Section 1 = artifacts changed in 6.1F. Section 2 = carry-forward: the full Phase 6.1E inventory (unchanged in 6.1F, already accounted for).

## 1. Phase 6.1F changes

| Finding | Artifact | Type | Content QA | External audit |
|---|---|---|---|---|
| Fail-closed authority guard | `tools/qa_ch1_note_architecture.py` (new: notebook/reactivation token families, clause splitter, SAFE/ELEVATED semantic classifiers, whole-file scan of 6 authorities, leading-banner gate for 3 retired standards, allowlist loader + stale detection) | C | PASS (fixture 27/27 BAD, 22/22 SAFE; live 6 authorities 16 sensitive clauses, 0 unreviewed; allowlist negative tests T0–T5; structural QA-of-QA 20/20·10/10·5/5·5/5·3/3) | PENDING-GROK |
| Reviewed allowlist baseline | `qa/baselines/ch1_note_architecture_allowlist.json` (16 reviewed architecture-sensitive clauses; file, clause, normalized, sha256, classification, rationale) | C | PASS (16/16 allowlisted live; mutate→FAIL; delete→stale; move→mismatch) | PENDING-GROK |
| Retired-standard banner gate fix | `tools/qa_ch1_note_architecture.py` `leading_banner()` (first contiguous blockquote after title only) — banner checker no longer reads late-body blockquotes | C | PASS (3/3 live banners PASS; removed→FAIL; removed+late-blockquote→FAIL) | PENDING-GROK |
| Legacy checker cleanup | `tools/qa_ch1_stale_refs.py` (removed NOTEBOOK_PRIMARY regex-shape detector, `scan_notebook_primary`, retired-standard banner logic; note-architecture delegated to the new module; content-stale + retired-artifact checks retained) | M | PASS (28 scopes, 0 hits) | PENDING-GROK |
| Fixture expansion | `tools/qa_notebook_primary_fixture.py` (27 BAD / 22 SAFE: prior 12 BAD + 11 fresh Grok + 4 mixed historical/current + 2 false-positive fixes + expanded SAFE) | M | PASS (27/27, 22/22) | PENDING-GROK |
| QA reports | `qa/reports/PHASE_6_1F_CH1_STALE_REFERENCE_SCAN.md` · `qa/reports/PHASE_6_1F_CH1_CONTENT_STALE_SCAN.md` | C | PASS (note-architecture scan 0 hits; content-stale scan 0 hits) | PENDING-GROK |
| audit response | `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | M | n/a (Round 6 section) | PENDING-GROK |
| inventory | `qa/reports/PHASE_6_1F_ARTIFACT_INVENTORY.md` · `qa/reports/PHASE_6_1F_INVENTORY_COMPLETENESS.md` | C | n/a | PENDING-GROK |

> Note: no authority file text, no retired-standard banner text, and no classroom artifact was changed in 6.1F. Only the guardrail (checker, fixture, allowlist) and its evidence (QA reports, inventory, audit response) changed.

## 2. Carry-forward (Phase 6.1E inventory, verbatim)

# PHASE 6.1E — ARTIFACT INVENTORY (final notebook-guardrail hardening)

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: tools/qa_phase_inventory.py on this file.
> Status key: PASS · n/a · PENDING-GROK (included in the external audit; Grok is read-only; v1.1 is **not frozen**).
> Type: **M** modified · **C** created · **A** affected-by-reference.
> Section 1 = artifacts changed in 6.1E. Section 2 = carry-forward: the full Phase 6.1D inventory (unchanged in 6.1E, already accounted for).

## 1. Phase 6.1E changes

| Finding | Artifact | Type | Content QA | External audit |
|---|---|---|---|---|
| H1 semantic-shape coverage | `tools/qa_ch1_stale_refs.py` (NOTEBOOK_PRIMARY + reversed-copula/imperative/colon/equals/modal-be patterns) | M | PASS (fixture 12/12 BAD, 7/7 SAFE; modal/future be-copula negative-tested) | PENDING-GROK |
| H1 fixture expansion | `tools/qa_notebook_primary_fixture.py` (12 BAD / 7 SAFE) | M | PASS (12/12, 7/7) | PENDING-GROK |
| M1 active authorities + banner gates | `tools/qa_ch1_stale_refs.py` (ARCHITECTURE_AUTHORITIES + RETIRED_STANDARDS banner gate) · `qa/reports/PHASE_6_1E_CH1_STALE_REFERENCE_SCAN.md` | M/C | PASS (36 scopes, 0 hits; 5 whole-file authorities; 3 retired standards banner-gated) | PENDING-GROK |
| audit response | `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | M | n/a (Round 5 section) | PENDING-GROK |
| inventory | `qa/reports/PHASE_6_1E_ARTIFACT_INVENTORY.md` · `qa/reports/PHASE_6_1E_INVENTORY_COMPLETENESS.md` | C | n/a | PENDING-GROK |

> Note: no retired-standard banner text changed in 6.1E — `docs/planning/INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md` and `docs/planning/STUDENT_NOTES_STANDARD.md` already carried complete RETIRED/HISTORICAL banners stating Guided Notes PRIMARY and the notebook architecture retired; they were added to the banner-gate list (scan scope) only. No classroom artifact was rebuilt.

## 2. Carry-forward (Phase 6.1D inventory, verbatim)

# PHASE 6.1D — ARTIFACT INVENTORY (final notebook-architecture guardrails)

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: tools/qa_phase_inventory.py on this file.
> Status key: PASS · n/a · PENDING-GROK (included in the external audit; Grok is read-only; v1.1 is **not frozen**).
> Type: **M** modified · **C** created · **A** affected-by-reference.
> Section 1 = artifacts changed in 6.1D. Section 2 = carry-forward: the full Phase 6.1C inventory (unchanged in 6.1D, already accounted for).

## 1. Phase 6.1D changes

| Finding | Artifact | Type | Content QA | External audit |
|---|---|---|---|---|
| M-B checker + fixture | `tools/qa_ch1_stale_refs.py` · `tools/qa_notebook_primary_fixture.py` · `qa/reports/PHASE_6_1D_CH1_STALE_REFERENCE_SCAN.md` | M/C | PASS (fixture 6/6 BAD, 4/4 SAFE; live 29 scopes 0 hits; reconstructed bad manifest + no-banner standard caught; in-memory negative tests) | PENDING-GROK |
| M-C retired standard | `docs/planning/SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md` | M | PASS (SUPERSEDED/HISTORICAL banner; scan banner-gate) | PENDING-GROK |
| audit response | `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | M | n/a (Round 4 section) | PENDING-GROK |
| inventory | `qa/reports/PHASE_6_1D_ARTIFACT_INVENTORY.md` · `qa/reports/PHASE_6_1D_INVENTORY_COMPLETENESS.md` | C | n/a | PENDING-GROK |

## 2. Carry-forward (Phase 6.1C inventory, verbatim)

# PHASE 6.1C — ARTIFACT INVENTORY (final Chapter 1 freeze-blocker cleanup)

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: tools/qa_phase_inventory.py on this file.
> Status key: PASS · n/a · PENDING-GROK (included in the external audit; Grok is read-only; v1.1 is **not frozen**).
> Type: **M** modified · **C** created · **A** affected-by-reference.
> Section 1 = artifacts changed or regenerated in 6.1C. Section 2 = carry-forward: the full Phase 6.1B inventory (unchanged in 6.1C or already accounted for there).

## 1. Phase 6.1C changes

| Finding | Artifact | Type | Content QA | Visual QA | Release parity | External audit |
|---|---|---|---|---|---|---|
| M-A + stale checker | `production/PRODUCTION_MANIFEST.md` · `tools/qa_ch1_stale_refs.py` · `qa/reports/PHASE_6_1C_CH1_STALE_REFERENCE_SCAN.md` | M/C | PASS (0 hits; 4 in-memory negative tests each detected; nothing left in tree) | n/a | n/a | PENDING-GROK |
| L-A | `production/premium-notes/01-ch1-energy-causes-change-guided-notes.{docx,pdf}` · `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.{docx,pdf}` · `production/premium-notes/previews/ch1-notes-*.png` · `tools/build_ch1_guided_notes.py` · `tools/qa_ch1_guided_notes.py` · `qa/reports/PHASE_6_1C_CH1_GUIDED_NOTES_QA.md` | M/C | PASS (new row-rule gate student + key 8/8; 3 pp) | PASS (3+3 pp) | PASS | PENDING-GROK |
| L-B | `production/releases/chapter-01/01-ch1-friday-flex.pdf` · `tools/build_ch1_release.py` · `tools/qa_release_parity.py` | M | PASS (new headless-continuation gate; fails on v1.1-B PDF) | PASS (4 pp, every page opens with its title) | PASS | PENDING-GROK |
| L-C | `production/slides/01-ch1-energy-causes-change-slides.{pptx,pdf}` · `production/slides/previews/ch1-slides-*.png` · `tools/build_ch1_slides.py` · `tools/qa_ch1_slides.py` · `qa/reports/PHASE_6_1C_CH1_SLIDESHOW_QA.md` | M/C | PASS (slide 1 gate; fails on v1.1-B deck) | PASS (45/45) | PASS | PENDING-GROK |
| L-D | `production/teacher-playbook/unit1-teacher-playbook.{docx,pdf}` · `production/teacher-playbook/previews/playbook-*.png` · `tools/build_teacher_playbook.py` · `tools/qa_teacher_playbook.py` · `qa/reports/PHASE_2_PLAYBOOK_QA.md` · `qa/reports/PHASE_6_1C_PLAYBOOK_QA.md` | M/C | PASS (new repo-path gate; fails on v1.1-B Playbook) | PASS (pp. 1-20) | n/a | PENDING-GROK |
| all | `production/releases/chapter-01/*` · `production/final-delivery/RELEASE_HASH_MANIFEST.csv` · `qa/reports/PHASE_6_1C_CH1_RELEASE_PARITY.md` | M/C | PASS | PASS | PASS | PENDING-GROK |
| all | `qa/reports/PHASE_6_1C_CH1_VISUAL_QA.md` · `qa/reports/PHASE_6_1C_ARTIFACT_INVENTORY.md` · `qa/reports/PHASE_6_1C_INVENTORY_COMPLETENESS.md` · `qa/reports/PHASE_3_CH1_GUIDED_NOTES_QA.md` · `qa/reports/PHASE_4_CH1_SLIDESHOW_QA.md` · `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | M/C | n/a | n/a | n/a | PENDING-GROK |
| carry | `qa/reports/PHASE_6_1B_*` (prior-phase reports, retained unchanged) | A | PASS | n/a | n/a | PENDING-GROK |

## 2. Carry-forward (Phase 6.1B inventory, verbatim)

# PHASE 6.1 — ARTIFACT INVENTORY (Chapter 1 external-audit remediation)

> Governance rule: **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
> Machine check: `tools/qa_phase_inventory.py` (every changed Ch1-scope path must be covered by a row below).
> Status key — **Content QA / Visual QA / Key parity / Release parity**: PASS · n/a · PENDING. **External audit**: `PENDING-GROK` = included in `docs/reviews/GROK_CH1_V1_1_AUDIT_PACKET.md`; Grok is read-only and has not yet returned a verdict (see §Status).
> Type: **C** created · **M** modified · **A** affected-by-reference (content unchanged, references checked/updated in text only where listed).
> Paths with `*` are glob groups.

## 1. Student-facing artifacts

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes.docx` | M | Student | PASS (`PHASE_6_1_CH1_GUIDED_NOTES_QA`) | PASS (3 pp) | PASS (key matches blanks) | n/a (PDF released) | PENDING-GROK |
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes.pdf` | M | Student | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |
| `production/premium-notes/previews/ch1-notes-student-*.png` | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `production/worksheets/01-ch1-energy-causes-change-practice.docx` | M | Student | PASS (`PHASE_6_1_CH1_ASSESSMENT_QA`) | PASS (2 pp) | PASS | n/a | PENDING-GROK |
| `production/worksheets/01-ch1-energy-causes-change-practice.pdf` | C | Student | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |
| `production/quizzes/01-ch1-energy-causes-change-quiz.docx` | M | Student | PASS | PASS (2 pp) | PASS (9 items / 16 pts) | n/a | PENDING-GROK |
| `production/quizzes/01-ch1-energy-causes-change-quiz.pdf` | C | Student | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |
| `production/worksheets/01-ch1-energy-detectives-student.docx` | M | Student (optional) | PASS | PASS (2 pp) | PASS | n/a | PENDING-GROK |
| `production/worksheets/01-ch1-energy-detectives-student.pdf` | C | Student (optional) | PASS | PASS | n/a | PASS (identical copy) | PENDING-GROK |

## 2. Projected artifacts

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/slides/01-ch1-energy-causes-change-slides.pptx` | M | Projected | PASS (`PHASE_6_1_CH1_SLIDESHOW_QA`, 28 gates) | PASS (geometry, tiers, 45 slides) | PASS (reveal answers = key) | PASS (identical copy) | PENDING-GROK |
| `production/slides/01-ch1-energy-causes-change-slides.pdf` | M | Projected | PASS | PASS (45/45) | n/a | PASS (identical copy) | PENDING-GROK |
| `production/slides/previews/ch1-slides-*.png` (45) | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `tools/build_ch1_slides.py` (speaker notes TIME/PLAN lines from `tools/ch1_pacing.py`) | M | Builder | PASS | n/a | n/a | n/a | PENDING-GROK |

## 3. Teacher-facing artifacts

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.docx`, `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.pdf` | M | Teacher | PASS | PASS (3 pp) | PASS (all 5 blanks + samples) | PASS (PDF identical copy) | PENDING-GROK |
| `production/premium-notes/previews/ch1-notes-key-*.png` | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `production/answer-keys/01-ch1-energy-causes-change-quiz-key.md` | M | Teacher | PASS (explicit YES/NO/YES; exact MC options; refs corrected) | n/a | PASS | PASS (derived into bundle PDF) | PENDING-GROK |
| `production/answer-keys/01-ch1-energy-causes-change-practice-key.md` | M | Teacher | PASS (book-on-table science corrected; no unsupported battery) | n/a | PASS | PASS (derived) | PENDING-GROK |
| `production/answer-keys/01-ch1-energy-detectives-key.md` | M | Teacher | PASS (ungraded look-fors) | n/a | PASS | PASS (derived) | PENDING-GROK |
| `production/quizzes/01-ch1-energy-causes-change-quiz-blueprint.md` | M | Teacher | PASS (points, note policy, refs) | n/a | PASS | n/a | PENDING-GROK |
| `production/labs/01-ch1-energy-detectives-teacher-spec.md` | M | Teacher | PASS | n/a | n/a | n/a | PENDING-GROK |
| `production/teacher-playbook/unit1-teacher-playbook.docx`, `production/teacher-playbook/unit1-teacher-playbook.pdf` | M | Teacher | PASS (`PHASE_6_1_PLAYBOOK_QA`, Ch1 sync gate) | PASS pp. 1–21 (Ch1 scope); 3 pre-existing out-of-scope WARN (pp. 22–33) | n/a | n/a | PENDING-GROK |
| `production/teacher-playbook/previews/playbook-*.png` | M | QA | n/a | PASS | n/a | n/a | PENDING-GROK |
| `tools/build_teacher_playbook.py`, `tools/qa_teacher_playbook.py` | M | Builder | PASS | n/a | n/a | n/a | PENDING-GROK |
| `qa/reports/PHASE_2_PLAYBOOK_QA.md` | A | Record | historical (was already modified before Phase 6.1; superseded by `PHASE_6_1_PLAYBOOK_QA.md`) | n/a | n/a | n/a | PENDING-GROK |

## 4. Release package

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `production/releases/chapter-01/*` (9 files + `RELEASE_MANIFEST.json` + `README.md`) | M/C | Teacher/Student | PASS (stale-language scan) | PASS (derived PDFs) | PASS | **PASS** (`PHASE_6_1_CH1_RELEASE_PARITY_QA`) | PENDING-GROK |
| `production/archive/retired/chapter-01-release-v1.0/*` | C | Archive | n/a | n/a | n/a | PASS (retired files excluded from release) | PENDING-GROK |
| `production/final-delivery/RELEASE_HASH_MANIFEST.csv` (Ch1 rows only) | M | Delivery index | n/a | n/a | n/a | PASS (rows == live hashes) | PENDING-GROK |
| `production/final-package/ENERGY_UNIT_MASTER_INDEX.md`, `production/PRODUCTION_MANIFEST.md` | M | Index | PASS (`PHASE_6_1_CH1_STALE_REFERENCE_SCAN`) | n/a | n/a | n/a | PENDING-GROK |

## 5. Pacing, manifests, traces (docs)

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `docs/chapter-01/CH1_PACING_PLAN.md` | C | Teacher/agents | PASS (`check_plan()`; simulation) | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_PACKAGE_MANIFEST.md` | M | Agents | PASS (stale scan) | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_SLIDESHOW_MANIFEST.md`, `docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md` | M | Agents | PASS | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_ASSESSMENT_TRACE.md`, `docs/chapter-01/CH1_STUDY_GUIDE_CONTRIBUTION.md` | M | Agents | PASS (F13 refs) | n/a | n/a | n/a | PENDING-GROK |
| `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md`, `docs/chapter-01/CH1_GOLD_STANDARD_PROPAGATION_SPEC.md` | M | Agents | PASS | n/a | n/a | n/a | PENDING-GROK |
| `docs/playbook/UNIT1_PACING_CALENDAR.md`, `docs/playbook/UNIT1_RESOURCE_MAP.md` | M | Teacher/agents | PASS | n/a | n/a | n/a | PENDING-GROK |
| `production/final-8.5-week/MASTER_CURRICULUM_MAP.md`, `production/final-8.5-week/WEEK1_2_TEACHER_QUICKSTART.md` | M | Teacher | PASS | n/a | n/a | n/a | PENDING-GROK |
| `production/final-8.5-week/MASTER_RESOURCE_INDEX.md`, `production/final-8.5-week/ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md`, `production/final-8.5-week/MASTER_RESOURCE_INVENTORY.md`, `production/final-8.5-week/VIDEO_PRESENTATION_INTEGRATION_MATRIX.md`, `production/final-package/ENERGY_UNIT_WEEK_BY_WEEK_TEACHER_MAP.md`, `production/friday-flex/FRIDAY_FLEX_BANK.md` | M | Teacher (Ch1 schedule sync, N1) | PASS (stale scan) | n/a | n/a | n/a | PENDING-GROK |
| `docs/planning/CURRENT_DECISIONS.md`, `docs/planning/FRIDAY_FLEX_FRAMEWORK.md` | M | Governance (owner Friday policy 2026-10-04, DECIDED) | n/a | n/a | n/a | n/a | PENDING-GROK |
| `qa/reports/PHASE_6_1_CH1_CLASSROOM_TIME_SIMULATION.md` | C | Record | PASS | n/a | n/a | n/a | PENDING-GROK |
| `qa/reports/PHASE_6_1_INVENTORY_COMPLETENESS.md` | C | Record (output of `qa_phase_inventory.py`) | PASS | n/a | n/a | n/a | PENDING-GROK |

## 6. Legacy / support content

| Artifact | Type | Audience | Content QA | Visual QA | Key parity | Release parity | External audit |
|---|---|---|---|---|---|---|---|
| `curriculum/chapter-01/student/01-ch1-friday-flex.md` | M | Teacher/student | PASS (cards listed inline; Detectives optional) | PASS (derived release PDF) | n/a | PASS (derived) | PENDING-GROK |
| `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md` | M | Student (absent) | PASS (5 blanks; no re-copy of printed text) | n/a | n/a | n/a | PENDING-GROK |
| `curriculum/chapter-01/README.md`, `curriculum/chapter-01/qa/*.md`, `curriculum/chapter-01/teacher/01-ch1-daily-lessons.md`, `curriculum/chapter-01/teacher/01-ch1-energy-causes-change-teacher-map.md`, `curriculum/chapter-01/teacher/01-ch1-supply-prep-guide.md` | M (SUPERSEDED banner only) | Archive | n/a (body untouched) | n/a | n/a | n/a | PENDING-GROK |
| `curriculum/chapter-01/CHAPTER_MANIFEST.md`, `curriculum/chapter-01/source-map.md`, `curriculum/chapter-01/teacher/01-ch1-teacher-notes.md`, `curriculum/chapter-01/media/*` | A | Archive | unchanged (already SUPERSEDED / source record) | n/a | n/a | n/a | PENDING-GROK |
| `production/final-delivery/Energy/Unit 1 *` (symlinks to canonical) | A | Delivery | resolve to current masters; legacy Teacher Guide copies are SUPERSEDED-bannered | n/a | n/a | PASS (CSV) | PENDING-GROK |

## 7. Tools and QA reports (created/modified)

| Artifact | Type | Notes | External audit |
|---|---|---|---|
| `tools/ch1_pacing.py` | C | single pacing data source | PENDING-GROK |
| `tools/gen_ch1_pacing_plan.py` | C | writes the pacing plan + simulation | PENDING-GROK |
| `tools/build_ch1_guided_notes.py`, `tools/qa_ch1_guided_notes.py` | M | notes fixes + new gates | PENDING-GROK |
| `tools/qa_ch1_slides.py` | M | new gates | PENDING-GROK |
| `tools/build_ch1_assessments.py`, `tools/qa_ch1_assessments.py` | C | practice/quiz/Detectives builder + QA | PENDING-GROK |
| `tools/build_ch1_release.py`, `tools/qa_release_parity.py` | C | reusable release build + parity QA | PENDING-GROK |
| `tools/qa_ch1_stale_refs.py`, `tools/qa_phase_inventory.py` | C | stale-reference scan; inventory completeness | PENDING-GROK |
| `tools/qa_visual_pdf.py`, `tools/qa_render_geometry.py`, `tools/pdf_page_ink.py`, `tools/export_pdf_previews.py` | C | reusable visual QA + export helpers | PENDING-GROK |
| `qa/reports/PHASE_6_1_*` (notes, slides, assessments, playbook, release parity, stale scan, visual, simulation, inventory) | C | evidence | PENDING-GROK |
| `qa/visual/phase6_1/*` | C | rendered review PNGs | PENDING-GROK |

## 8. Governance and review docs (created/modified)

| Artifact | Type | External audit |
|---|---|---|
| `docs/reviews/EXTERNAL_GROK_CH1_ADVERSARIAL_AUDIT_RESPONSE.md` | C | PENDING-GROK |
| `docs/reviews/PHASE_6_1_CH1_EXTERNAL_AUDIT_REMEDIATION.md` | C | PENDING-GROK |
| `docs/reviews/GROK_CH1_V1_1_AUDIT_PACKET.md`, `docs/reviews/GROK_CH1_V1_1_AUDIT_PROMPT.md` | C | n/a (the audit input) |
| `AGENTS.md`, `.cursor/rules/30-qa-and-release.mdc`, `.cursor/rules/00-project-governance.mdc`, `docs/planning/QA_GATES.md`, `docs/agent-workflows/PHASE_PIPELINE.md` | M/C | PENDING-GROK |

## 9. Not touched (explicit)

Chapters 3–7 artifacts; Unit 1 Visual System v1.0 (`qa_visual_system.py` PASS, tokens unchanged); locked Unit 1 final assessment; authoritative CKSci sources. Chapter 2 files that appear modified in the working tree belong to the separate Phase 7 work and were **not** edited by Phase 6.1 (the Playbook's shared `_page_break` helper change affects Ch2 page layout only by removing blank-page risk; Ch2 text unchanged).

## 10. Status

- Internal gates: see `docs/reviews/PHASE_6_1_CH1_EXTERNAL_AUDIT_REMEDIATION.md`.
- External audit: **not yet returned**. Every row above is `PENDING-GROK`; the freeze to v1.1 is therefore **not** performed.
