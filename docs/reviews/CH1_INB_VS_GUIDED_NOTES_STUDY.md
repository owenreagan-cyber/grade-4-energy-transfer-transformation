# CHAPTER 1 NOTE FORMAT STUDY

> Controlled comparison of two premium Chapter 1 note systems (same content) to determine the best student note-taking format for this 9-week Grade 4 unit.

## 1. Test Design
- Two prototypes built from the **same** released Chapter 1 content (definitions, ENERGY→CHANGE→EVIDENCE model, five forms, stored energy with battery/rubber-band/raised-object, observation-vs-explanation, synthesis).
- **INB** = 3 composition-notebook inserts (7.0″×9.0″, dashed trim, top-edge glue, one lift-flap reveal + flat option).
- **Guided Notes** = 3 US Letter pages, no assembly.
- Content equivalence enforced by deterministic extraction (15 concepts, both PASS). The only manipulated variable is **format**.
- All QA automated (headless LibreOffice render, `pdftotext`, PIL measurements, DOCX XML extraction). No human/manual gate.

## 2. Interactive Notebook Prototype
- **Inserts:** 3 (Energy Causes Change · Stored Energy — Ready for Change · Energy Detectives — Evidence).
- **Writing load:** 8 fill-in blanks · 6 free responses · 2 drawings · 3 flap reads.
- **Assembly:** 3 cuts (dashed trim) + 3 top-edge glues + 3 lift-flaps (+ a fully flat alternative).
- **Strengths:** permanent composition-book archive; tactile flap reveal; shaded model boxes.
- **Weaknesses:** 10 pt assembly labels; ~0.28″ writing lines; 2-line max responses; ~2 min/session assembly; high absent-recovery burden; poor fit for data tables.

## 3. Guided Notes Prototype
- **Pages:** 3 (Energy Causes Change · Stored Energy · Energy Detectives/Synthesis).
- **Writing load:** 10 fill-in blanks · 5 responses (incl. 4-line synthesis) · 2 drawings.
- **Assembly:** none.
- **Strengths:** 13–14 pt body, 16–17 pt headings, 22 pt title; 0.36–0.42″ writing lines; full-width tables; duplex-printable; zero assembly.
- **Weaknesses:** loose-sheet risk (needs filing); no tactile layer.

## 4. Content Equivalence
**PASS** — all 15 concepts present in both, same sequence. (See `CONTENT_EQUIVALENCE.md`.)

## 5. Readability
- INB: primary 12 pt; assembly labels 10 pt (WARN).
- Guided Notes: body 13–14 pt; floor 11 pt captions (PASS).
- **Guided Notes more readable.**

## 6. Handwriting Space
- INB: lines ≈0.28″ (under 0.30″ target); longest response 2 lines (WARN).
- Guided Notes: lines 0.36–0.42″; 4-line synthesis; larger drawing boxes (PASS).
- **Guided Notes has materially more usable writing space.**

## 7. Visual Learning
- Both have model boxes + before/after drawings (tie).
- INB adds a tactile flap; Guided Notes has clearer full-page diagrams.
- **Roughly tied; INB slight edge on tactile, Guided Notes on diagram size.**

## 8. Motor / Assembly Load
- INB: 3 cuts + 3 glues + 3 folds + supply transitions (~12–15 motor actions).
- Guided Notes: ~2–3 (write/draw only).
- **Guided Notes far lower.**

## 9. Classroom Time
- 30-min: INB WARN (assembly+transitions ≈4.5 min) · Guided Notes PASS.
- 45-min: both PASS.
- INB costs ~+54 min/unit in assembly.

## 10. Paper Use (20 students)
- INB: 3 sheets/student (60 total), single-sided only, ~15–20% trim scrap.
- Guided Notes: 3 sheets/student (60) or **duplex → 40**; no scrap.
- **Guided Notes ≤ INB paper.**

## 11. Organization
- INB: permanent bound archive (STRONG); hard to lose (LOW loose risk).
- Guided Notes: loose sheets, binder/folder required (HIGH loose risk).
- **INB stronger on organization.**

## 12. Absent Recovery
- INB: reconstruct insert out of sequence (HIGH burden).
- Guided Notes: photocopy sheet (LOW burden).
- **Guided Notes much easier.**

## 13. Accessibility
- INB: cut/glue/fold excludes fine-motor-challenged students (flat option mitigates partially).
- Guided Notes: write-only (accessible).
- **Guided Notes more accessible.**

## 14. Unit-Wide Scalability
- INB: ~21 inserts, high assembly, poor fit for Ch3–5 data + engineering W8.
- Guided Notes: ~16–21 pages, strong data/diagram fit.
- **Guided Notes scale better.**

## 15. Hybrid Analysis
Would hybrid improve the system? **Yes**, narrowly:
- **Solves INB weaknesses:** keeps daily work on full-size sheets (large writing space, no daily assembly, easy absent recovery).
- **Solves Guided Notes weaknesses:** preserves a permanent, organized anchor archive for the canonical models (the one thing INB wins).
- **Duplication check:** NO duplication if scoped — the INB anchor holds the *repeated canonical model* (which is intentionally revisited), while Guided Notes/lab sheets hold the *daily data*. They are complementary, not redundant.
- **Cost:** ~1 insert/chapter (≈7/year) vs 21 in full INB — trivial management burden.

## 16. Rubric Results
INB **48 / 75** · Guided Notes **66 / 75** (see `FORMAT_COMPARISON_RUBRIC.md`). Guided Notes lead on 10 of 15 criteria; INB leads on organization only; tied on visual learning/retention support.

## 17. Recommendation

**HYBRID MODEL**

## 18. Implementation Recommendation
- **Guided Notes become the primary daily format** (Chapters 1–7): full-size sheets for definitions, data tables, labs, and synthesis — no cutting/gluing.
- **Preserve a small INB anchor archive** — one insert per chapter for the canonical model that students must revisit:
  1. ENERGY → CHANGE → EVIDENCE
  2. MOTION → CHANGE → EVIDENCE
  3. Same-object speed model
  4. Transfer vs transformation (BOTH)
  5. Collision evidence model
  6. Engineering design cycle
  7. Unit concept map / Edison persistence
- Labs/data (Ramp It Up!, sand craters, Crash Lab A/B, sound/light/heat/electricity, capstone logs) stay on **full-size sheets**.
- This keeps the permanent archive + tactile anchors (INB's only win) at ~1 insert/chapter, while giving every lesson the large writing space, low assembly, and easy absent recovery that the evidence shows matter most in this data-heavy unit.
