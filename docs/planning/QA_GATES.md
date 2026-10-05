# QA GATES

> No resource may be called **FINAL / READY / COMPLETE / RELEASED** unless it passes all 8 gates. Each gate returns **PASS / WARN / FAIL**. Any FAIL blocks release; WARN requires a recorded note + owner.

## The 8 gates
1. **SOURCE VALIDATION** — matches authoritative source (titles, concepts, vocabulary, standards, framing).
2. **CONTENT PRIORITY** — CORE content present and correct; no drift into non-core.
3. **CROSS-ARTIFACT ALIGNMENT** — Big Question/vocabulary/model consistent across notes, slides, quiz, final.
4. **EDUCATIONAL SUITABILITY** — Grade 4 language; observation vs inference; fair-test logic; misconception handling.
5. **VISUAL / LAYOUT QA** — projection & print quality; no cutoff.
6. **TECHNICAL QA** — files open, render, export correctly; hashes stable.
7. **CLASSROOM SIMULATION** — walk-through as teacher + student; timing & prep realistic.
8. **FINAL ACCEPTANCE REPORT** — explicit sign-off recording all PASS/WARN/FAIL results.

## Phase-level gates (added Phase 6.1; apply to every phase)
9. **VISUAL QA (deterministic + rendered)** — `tools/qa_visual_pdf.py` on every affected student/teacher/projected artifact; each artifact PASS/WARN/FAIL; every WARN/FAIL lists file, page/slide, issue, severity, fix. Required result: PASS.
10. **RELEASE PARITY** — `tools/qa_release_parity.py`: release == canonical (hash), no stale/retired files, widescreen metadata.
11. **STALE-REFERENCE SCAN** — zero stale hits in active files.
12. **PHASE ARTIFACT INVENTORY** — `qa/reports/PHASE_<n>_ARTIFACT_INVENTORY.md`; `tools/qa_phase_inventory.py` PASS.
13. **EXTERNAL ADVERSARIAL AUDIT** — Grok read-only; result must be exactly "APPROVE PROPAGATION". No phase is complete until every created/modified/affected artifact is accounted for by the external audit.

## Presentation-specific checks
- one core idea per slide
- readable projection size
- no crowded paragraphs
- visual clarity
- no off-screen / cutoff content

## Student-page-specific checks
- generous writing space
- readable tables
- **no answer leakage**
- age-appropriate language
- printability

## Status vocabulary
- Use **PASS / WARN / FAIL** only.
- Draft artifacts stay labeled **DRAFT** until they pass all gates.
