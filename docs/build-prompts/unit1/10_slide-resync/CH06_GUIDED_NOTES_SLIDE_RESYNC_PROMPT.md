# SLIDE RE-SYNC PROMPT — Chapter 6 Guided Notes ↔ Slideshow

> Standalone future-work prompt. **Do NOT execute now.** This instructs a future Cursor session to re-sync the Chapter 6 slide deck to the accepted Guided Notes candidate.
>
> **State:** `RESYNC_PENDING_GUIDED_NOTES_APPROVAL`. The Chapter 6 Guided Notes must be **built, rendered, and accepted** before this re-sync executes.
>
> **Guiding principle (locked):** the **new Guided Notes architecture drives the slide re-sync.** Do NOT force the notes to mimic obsolete INB-era slide structure.

---

## 1. Inputs

- **Accepted Guided Notes candidate:** `production/premium-notes/06-ch6-energy-transformations-guided-notes.docx` + `…-key.docx`.
- **Existing deck:** `production/slides/06-ch6-energy-transformations-slides.pptx` (44 slides).
- **Chapter anchors (locked):** BQ "How do energy transformations help people?" (supporting "How can I design a device that transforms energy to solve a problem?") · V1 (convert · conversion · energy transformation) · V2 (engineering design) · N1 Energy Can Change Form (transfer / transformation / BOTH) · N2 Systems Do Transfer AND Transformation · N3 Engineering Design (criteria/constraints, DESIGN → BUILD → TEST → REFINE) · CHECK YOUR THINKING · BQ · NOW I THINK.
- **Chapter boundary:** Chapter 6 is the formal home of transfer/transformation/BOTH. No kinetic/potential/mechanical/radiant/chemical required; no "proves" language; no solar-oven default.

## 2. Tasks (in order)

1. **Inspect the accepted Guided Notes candidate** — record its exact BQ/V/N anchor set, wording, blank structure, table/diagram structure, and page order.
2. **Inspect the existing deck** — map every slide's current anchor and note-writing direction.
3. **Identify obsolete INB references** — any slide that says "cut/paste/glue into your notebook", "foldable", "interactive notebook", or uses INB-only insert directions.
4. **Derive slide writing anchors from the accepted Guided Notes** — not the reverse.
5. **Preserve accepted curriculum wording** — slide WRITE/CHECK text mirrors the notes' BQ/V/N wording exactly (including the transfer / transformation / BOTH definitions).
6. **Update the WRITE/CHECK mapping** — produce `| Note anchor | Notes section | Slide WRITE | Slide CHECK/REVEAL |`; no WRITE slide may show its answer.
7. **Remove obsolete INB directions** from affected slides.
8. **Preserve slide sequence where possible** — re-anchor only the note-writing moments; do not reorder unrelated slides.
9. **Do not change unrelated chapter content** — no new science, no palette changes.
10. **Render the whole deck** — export PDF + PNG previews.
11. **Audit notes ↔ slides** for: anchor match · wording match · blank structure · order · diagram/table structure · answer leakage.
12. **Produce a re-sync report** — changed slides, removed INB references, final WRITE/CHECK mapping.
13. **Do not overwrite the canonical deck until the candidate passes** — stage `06-ch6-energy-transformations-slides-resync-candidate.pptx`, run visual QA, promote only on acceptance.

## 3. Output

- Re-synced deck candidate + rendered PDF + previews.
- `CH06_RESYNC_REPORT.md` (or `qa/reports/` equivalent) recording the audit and WRITE/CHECK mapping.

## 4. Acceptance gate

Every note anchor has a matching WRITE slide and a separate CHECK/REVEAL slide; wording matches verbatim; the transfer/transformation/BOTH distinction is preserved; no answer leakage; no obsolete INB directions; unrelated content unchanged; rendered deck passes visual QA. **Do not freeze, commit, or push.**
