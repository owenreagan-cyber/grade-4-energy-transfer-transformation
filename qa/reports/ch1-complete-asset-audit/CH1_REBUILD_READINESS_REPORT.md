# CH1 REBUILD READINESS REPORT

Phase 4 — Chapter 1 Complete Visual Asset Audit. Verdict: **ready to specify the hybrid, but not
ready to build** — three owner decisions are blocking; otherwise assets are sufficient.

## 1. What was found (headline)

- The **canonical frozen deck (v1.1)** has **zero raster artwork**; it is the text/sequence/model
  authority. 45 slides, 16:9, Avenir Next.
- **Codex candidate v5** supplies a complete, consistent premium raster set (11 unique text-free
  images, 29 embedded via strip-cropping), but its **45-slide sequence diverges from canonical** in
  five places (media shell @8; split V1; folded RECITE; collapsed N3 teaching; media shell replacing
  the application slide @32).
- **Gemini** delivers five image-only, non-editable decks (1376×768, no text layer) — usable only as
  photograph reference.
- **Standalone intake images** (19 unique) are generally higher resolution than the Codex set and
  are the best substitute pool.
- **18 videos** are all H.264+AAC; one already rejected (`How_Scientists_Spot_Invisible_Energy.mp4`);
  three are portrait "Proves" shorts (drift risk). No video may become core-required.

## 2. Blocking decisions (owner must resolve before build)

1. **Sequence authority:** build the hybrid on the **canonical frozen 45-slide sequence** (recommended)
   or adopt the blueprint/v5 re-sequencing? Every downstream step depends on this.
2. **N3 teaching:** restore canonical slides 23 (battery PREDICT) + 24 (position) + 25
   (STORED→RELEASE→CHANGE), or accept v5's single "Objects can store energy" card slide? Restoring
   is recommended (preserves predict-first pedagogy and explicit "position" teaching).
3. **Slide 32:** keep the canonical "Which change shows energy at work?" application slide, or adopt
   v5's optional-review media shell? (Friday synthesis; canonical content is preferable.)

Secondary decisions: keep Georgia titles vs normalize to Avenir Next; keep-vs-fold the canonical
"EXPLAIN" (slide 9) and "RECITE" (slide 13) slides; which (if any) Gemini/standalone image replaces a
Codex image (visual-art director call).

## 3. What is sufficient today (no new generation required)

- Opener, dark/bright, pencil before/after, seashore, five-forms strip, rubber-band, 3-panel stored,
  3-panel evidence, BQ reflection, chapter-close — **all present** in the Codex set.
- All WRITE/CHECK, model-chain, table, and review slides are **deterministic** (shapes/text) — no
  raster needed.
- Standalone intake pool covers every missing *alternate* (higher-res openers, per-form images,
  per-vocab cards, battery, raised apple).

## 4. Gaps / corrections

| Gap | Fix |
|---|---|
| N3 predict/position teaching (if restored) | crop `slide-25` battery/apple or use `ch1-stored-battery-01.jpg` / `ch1-stored-raised-apple-01.jpg` |
| `science-chapter-opener.jpg` baked title | reject as-is; use the other two openers |
| Portrait "Proves" videos | exclude unless re-cut landscape + re-worded |
| Gemini decks non-editable | never use as slide masters |
| v2 empty media | nothing to recover (superseded by v3/v4/v5) |
| `[VISUAL]` subjective grading | visual-art director must grade Gemini vs Codex vs standalone image A/B before freeze |

## 5. Risks

- **Highest:** rebuilding on v5's sequence would silently change the frozen instructional sequence
  (governance rule 80 — frozen Chapter 1 must not change without owner-authorized reopening).
- **Medium:** v5's collapse of N3 teaching under-teaches "position" before the write slide.
- **Medium:** adopting any "Proves"-titled video re-introduces proof language the chapter rejects.
- **Low:** Georgia title font is a minor deviation from the frozen Avenir Next-only deck.

## 6. Recommended next steps (after this audit)

1. Owner resolves the three blocking decisions (above).
2. Visual-art director grades the A/B image candidates (Codex vs standalone vs Gemini).
3. Specify the hybrid on the **canonical** sequence (map in `CH1_45_SLIDE_SELECTION_MATRIX.md`).
4. Build a new candidate (editable PPTX) — do **not** touch the frozen deck or Guided Notes.
5. Run deterministic QA (notes-to-slide exact match, answer-leakage, 16:9/overflow, vocab guardrails),
   then visual QA + contact sheet, then external Grok adversarial audit, then freeze — per the phase
   pipeline. No promotion without explicit owner approval.

## 7. Scope accounting (this phase)

Read-only. No frozen deck, Guided Notes, or canonical source was modified. No rebuild, no commit, no
push, no promotion. New artifacts produced in `qa/reports/ch1-complete-asset-audit/` (6 reports +
`CH1_ASSET_MANIFEST.json` + `_contact_sheets/` + `_scripts/`).
