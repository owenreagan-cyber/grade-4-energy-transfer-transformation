# SLIDE RE-SYNC PROMPT — Chapter 4 Guided Notes ↔ Slideshow

> Standalone future-work prompt. **Do NOT execute now.** This instructs a future Cursor session to re-sync the Chapter 4 slide deck to the accepted Guided Notes candidate.
>
> **State:** `RESYNC_PENDING_GUIDED_NOTES_APPROVAL`. The Chapter 4 Guided Notes must be **built, rendered, and accepted** before this re-sync executes.
>
> **Guiding principle (locked):** the **new Guided Notes architecture drives the slide re-sync.** Do NOT force the notes to mimic obsolete INB-era slide structure.

---

## 1. Inputs

- **Accepted Guided Notes candidate:** `production/premium-notes/04-ch4-energy-transfer-guided-notes.docx` + `…-key.docx` (must already be accepted).
- **Existing deck:** `production/slides/04-ch4-energy-transfer-slides.pptx` (46 slides).
- **Chapter anchors (locked):** BQ "What evidence shows that energy transfers from place to place?" · V1 (energy transfer · sound) · N1 Energy Transfer · N2 Sound and Light Can Transfer Energy · N3 Heat and Electric Current Can Transfer Energy · N4 Finding Evidence of Energy Transfer · CHECK YOUR THINKING · BQ · NOW I THINK.
- **Chapter boundary:** Chapter 4 is ENERGY TRANSFER only. Do **not** introduce formal transfer/transformation/BOTH classification (that is Chapter 6).

## 2. Tasks (in order)

1. **Inspect the accepted Guided Notes candidate** — record its exact BQ/V/N anchor set, wording, blank structure, table/diagram structure, and page order.
2. **Inspect the existing deck** — map every slide's current anchor and note-writing direction.
3. **Identify obsolete INB references** — any slide that says "cut/paste/glue into your notebook", "foldable", "interactive notebook", or uses INB-only insert directions.
4. **Derive slide writing anchors from the accepted Guided Notes** — not the reverse.
5. **Preserve accepted curriculum wording** — the slide WRITE/CHECK text must mirror the notes' BQ/V/N wording exactly.
6. **Update the WRITE/CHECK mapping** — produce the table `| Note anchor | Notes section | Slide WRITE | Slide CHECK/REVEAL |`; no WRITE slide may show its answer.
7. **Remove obsolete INB directions** from affected slides.
8. **Preserve slide sequence where possible** — do not reorder unrelated slides; only re-anchor the note-writing moments.
9. **Do not change unrelated chapter content** — no new science, no re-sequencing of non-note slides, no palette changes.
10. **Render the whole deck** — export PDF + PNG previews for visual QA.
11. **Audit notes ↔ slides** for: anchor match · wording match · blank structure · order · diagram/table structure · answer leakage (no WRITE slide reveals an answer).
12. **Produce a re-sync report** — list changed slides, removed INB references, and the final WRITE/CHECK mapping.
13. **Do not overwrite the canonical deck until the candidate passes** — stage as a candidate (e.g., `04-ch4-energy-transfer-slides-resync-candidate.pptx`), run visual QA, and only promote on acceptance.

## 3. Output

- Re-synced deck candidate + rendered PDF + previews.
- `docs/build-prompts/unit1/10_slide-resync/CH04_RESYNC_REPORT.md` (or `qa/reports/` equivalent) recording the audit and the WRITE/CHECK mapping.

## 4. Acceptance gate

Every note anchor has a matching WRITE slide and a separate CHECK/REVEAL slide; wording matches verbatim; no answer leakage; no obsolete INB directions remain; unrelated content unchanged; rendered deck passes visual QA. **Do not freeze, commit, or push** (commit only when the user asks).
