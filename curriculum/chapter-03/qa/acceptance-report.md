# Final Acceptance Report — Chapter 3

> 10-gate QA (Phase 5 adds Data Quality and Physical Notebook Usability). Any FAIL blocks release.

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | Source Validation | **PASS** | `qa/source-validation.md` — no UNSUPPORTED statements; exact titles/AP/vocab; PE 4-PS3-1 at L5 only; measured-vs-inferred preserved; 2 deviations documented as ADAPTED |
| 2 | Content Priority | **PASS** | Chapter 3 boundary honored; no mass-as-central, no collisions/transfer/transformation/engineering, no kinetic/potential |
| 3 | Cross-Artifact Alignment | **PASS** | `qa/cross-artifact-alignment.md` — same model/vocab/Big Question/sequence; no answers leaked; graph never "Speed vs. Energy" |
| 4 | Educational Suitability | **PASS** | `qa/educational-suitability.md` — Grade 4 level, balanced demand, observation-before-definition, same-object rule |
| 5 | Data Quality | **PASS** | `qa/data-quality.md` — trials feasible; units consistent (cm/books); graph matches table; averages correct; no fake precision; no invented speed/energy numbers |
| 6 | Visual / Layout QA | **PASS** | All DOCX/PPTX rendered to PDF and inspected: ramp = 3 clean pages (graph title + grid together, no near-empty page); notebook 3 inserts within 7"×9" frame; 28 slides legible; grayscale-safe |
| 7 | Technical QA | **PASS** | PPTX/DOCX open cleanly (LibreOffice round-trip); PDFs match masters; no blank/duplicate pages; Arial; no temp files tracked |
| 8 | Physical Notebook Usability | **PASS** | 7.0"×9.0" dashed trim frames; top-edge glue instruction; fold direction ("fold down, then lift") consistent; flap answer clear; no-cut flat fill-in alternative provided |
| 9 | Classroom Simulation | **PASS** | `qa/classroom-simulation.md` — Mon–Thu fit at 45 min; 30-min Wednesday graphing split documented; averaging moved to Wednesday |
| 10 | Final Acceptance | **PASS** | all gates green; WARN items below are non-blocking |

## WARN (non-blocking)
1. External media links are **candidates**, not verified (extension videos). Media plan marks "NOT VERIFIED."
2. Class/group count unresolved → supply quantities use `GROUP_COUNT × amount`.
3. Quiz scoring denominator left to school grading policy (item points given).
4. Ramp It Up! 2.0 and Drop It are **ADAPTED** from AP 4.1/4.2 (measurement/graphing upgrade; fixed heights). Documented in `source-map.md` and `qa/source-validation.md` — deliberate, science-preserving, NOT silent overrides.

## Release status
**RELEASED** — editable masters in `production/` + release candidates in `production/releases/chapter-03/`.
