# Producer Independence Audit

F-3 requires every release-blocking producer to open and inspect the actual
artifact bytes it certifies. This matrix classifies each mandatory producer's
current independence state. Classifications:

- `INDEPENDENT` — producer opens the artifact and derives observations from bytes.
- `PARTIALLY_INDEPENDENT` — opens some real input but a PASS still depends on caller-supplied facts.
- `TAUTOLOGICAL` — observed is derived from the same object as expected.
- `CALLER_FED` — the caller supplies the observed result/booleans.
- `MISSING` — no producer or no observation path.

## Matrix

| gateId | producer | artifact(s) | files opened | derived from bytes | caller-fed | state |
|---|---|---|---|---|---|---|
| SOURCE_AUTHORITY | `source_audit.emit_source_evidence` | Reader/TG vs candidate | none (claims) | claim texts | sourceText/candidateText | CALLER_FED |
| CURRICULUM_CORRECTNESS | `source_audit.emit_source_evidence` | candidate vs source | none (claims) | derivation kind | source/candidate/approved text | CALLER_FED |
| CHAPTER_SPEC | `mandatory_producers.emit_chapter_spec` | chapter spec JSON | none | — | parsed spec dict | TAUTOLOGICAL |
| STUDENT_PROMPT_CLARITY | `student_prompt.emit_student_prompt_evidence` | notes/practice/quiz/lab/recovery | none | — | prompt text + classification | CALLER_FED |
| NOTES_STRUCTURE | `mandatory_producers.emit_notes_structure` | guided notes | none | — | observed dict == expected | TAUTOLOGICAL |
| SLIDES_STRUCTURE | `mandatory_producers.emit_slides_structure` | slides | none | — | observed dict == expected | TAUTOLOGICAL |
| NOTES_SLIDES_SYNC | `cross_artifact.emit_cross_evidence` | notes vs slides | none | — | left/right anchor dicts | TAUTOLOGICAL |
| ANSWER_LEAKAGE | `mandatory_producers.emit_answer_leakage` | notes/slides/keys | none | — | reveal sequence + prefilled bool | CALLER_FED |
| ASSESSMENT_ALIGNMENT | `cross_artifact.emit_cross_evidence` | practice/quiz/lab vs keys | none | — | left/right dicts | TAUTOLOGICAL |
| SCHEDULE_POLICY | `schedule_policy.emit_schedule_evidence` | calendar/pacing | none | — | rows (day/token/firstExposure) | CALLER_FED |
| PLAYBOOK_ALIGNMENT | `cross_artifact.emit_cross_evidence` | playbook region vs spec | none | — | left/right dicts | TAUTOLOGICAL |
| RENDER_COMPLETENESS | `render_completeness.emit_render_evidence` | render PNGs | render files (hash) | render hash/source hash | expected render list | PARTIALLY_INDEPENDENT |
| RENDERED_VISUAL_QA | `visual_qa.emit_visual_evidence` | rendered pages | render images (pixels) | ink/boxes | page spec/boxes | PARTIALLY_INDEPENDENT |
| PDF_QUALITY | `qa_pdf_quality.emit_pdf_evidence` | PDF | qpdf/pdfinfo/pdffonts/pdftotext | pages/fonts/DPI/text | expectations only | INDEPENDENT |
| FRESH_EXPORT | `mandatory_producers.emit_fresh_export` | source → fresh PDF | none | — | hashes/text/dimensions | CALLER_FED |
| RETIRED_CONTENT | `mandatory_producers.emit_retired_content` | classroom/release bytes | none | — | files text/perceptualHash | CALLER_FED |
| INVENTORY | `mandatory_producers.emit_inventory` | release/classroom set | none | — | observed list | CALLER_FED |
| RELEASE_EXACT_SET | `release_set.emit_release_evidence` | release dir | release dir (iterdir + hash) | names + hashes | expected list + manifest | INDEPENDENT |
| RELEASE_PARITY | `release_set.emit_release_evidence` | release vs production | release dir (hash) | release hashes | original_hashes | PARTIALLY_INDEPENDENT |
| STATUS_AUTHORITY | `qa_status_authority.emit_status_evidence` | status surfaces | none | — | authoritative + surfaces | CALLER_FED |
| ADVERSARIAL_QA | `mandatory_producers.emit_adversarial_qa` | runner output | none | — | summary dict (completed/counts) | CALLER_FED |
| PRIOR_FROZEN_NONREGRESSION | `mandatory_producers.emit_prior_frozen` | Ch1/Ch2 baselines | none | — | observed guard/parity dict | CALLER_FED |

## Summary

- `INDEPENDENT` (10): PDF_QUALITY, RELEASE_EXACT_SET, CHAPTER_SPEC,
  NOTES_STRUCTURE, SLIDES_STRUCTURE, INVENTORY, RETIRED_CONTENT,
  STUDENT_PROMPT_CLARITY, STATUS_AUTHORITY, SCHEDULE_POLICY, ADVERSARIAL_QA,
  PRIOR_FROZEN_NONREGRESSION.
- `PARTIALLY_INDEPENDENT` (3): RENDER_COMPLETENESS, RENDERED_VISUAL_QA,
  RELEASE_PARITY.
- `CALLER_FED` (4): SOURCE_AUTHORITY, CURRICULUM_CORRECTNESS, ANSWER_LEAKAGE,
  FRESH_EXPORT.
- `TAUTOLOGICAL` (3): NOTES_SLIDES_SYNC, ASSESSMENT_ALIGNMENT, PLAYBOOK_ALIGNMENT.

This matrix is the worklist. Repairs proceed gate-by-gate; no gate is reclassified
until its producer demonstrably opens the artifact and its negative self-test fails
through the normal entrypoint.

---

## F-3 status update

### Pass 1 (committed `163061f`)
Six producers rewired to open files: CHAPTER_SPEC, NOTES_STRUCTURE,
SLIDES_STRUCTURE, INVENTORY, RETIRED_CONTENT, STUDENT_PROMPT_CLARITY.

### Pass 2 (this pass)
Four more producers rewired to file/tool observation:

| gateId | state (before → after) | files opened / tools run | bad fixture → result |
|---|---|---|---|
| STATUS_AUTHORITY | CALLER_FED → INDEPENDENT | tracked status surfaces | premature FROZEN/RELEASED → FAIL |
| SCHEDULE_POLICY | CALLER_FED → INDEPENDENT | pacing calendar file | Friday REQUIRED / unknown token → FAIL |
| ADVERSARIAL_QA | CALLER_FED → INDEPENDENT | runner result JSON | escaped/aborted run → FAIL |
| PRIOR_FROZEN_NONREGRESSION | CALLER_FED → INDEPENDENT | Ch1 guard + Ch2 golden tools | mutated frozen byte → FAIL |

The adversary runner's status/schedule mutation cases now write actual files and
invoke the file-observing producers (no fabricated observation dicts).

### Remaining (7)
SOURCE_AUTHORITY, CURRICULUM_CORRECTNESS, NOTES_SLIDES_SYNC, ANSWER_LEAKAGE,
ASSESSMENT_ALIGNMENT, PLAYBOOK_ALIGNMENT, FRESH_EXPORT. These remain caller-fed
or tautological and are coupled to the anchor/claim data model; they need a
deeper text-extraction three-way comparison plus a full rework of the adversary's
anchor/leakage/assessment mutation cases.


