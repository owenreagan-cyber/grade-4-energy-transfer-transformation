# Phase 4 — Chapter 1 Slideshow · Source-Fidelity Review

**Reviewer role:** Curriculum Source Reviewer (READ-ONLY — no artifact modified)
**Artifact:** `production/slides/01-ch1-energy-causes-change-slides.pptx` (45 slides) + `-slides.pdf`
**Authoritative inputs:**
- CKSci Student Reader Ch.1 "Energy Causes Change" (Reader pp. 1–6) — `assets/authoritative/student-reader/chapters/Chapter_1_Energy_Causes_Change.pdf`
- CKSci Teacher Guide Lessons 1–2 (TG pp. 18–25) — `assets/authoritative/teacher-guide/Science 4 - Energy Transfer - TG .pdf`
- Guided Notes (authoritative for BQ/V/N): `production/premium-notes/01-ch1-energy-causes-change-guided-notes.{pdf,-key.pdf}`
- Contract: `docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md`
- Vocabulary standard: `docs/planning/VOCABULARY_PROGRESSION.md`

**Method:** Extracted all 45 slides' on-slide text + speaker notes via python-pptx; extracted rendered PDF via `pdftotext`; cross-checked against Reader Ch.1 text, TG Lesson 1/2, the Guided Notes student/key, and the contract.

---

## OVERALL: PASS

All nine fidelity items PASS. No content contradicts the Reader or Teacher Guide; no advanced/unsupported required terminology; no transfer/transformation language taught as Chapter 1 content; BQ/V/N anchors mirror the finalized notes exactly.

## Per-item results

| # | Item | Verdict |
|---|---|---|
| 1 | Big Question EXACT wording | PASS |
| 2 | V1/V2 terms + exact definitions | PASS |
| 3 | N1–N4 titles + fill-in answers mirror notes | PASS |
| 4 | Reader page citations (pp. 1–6, correct per contract) | PASS |
| 5 | No advanced unsupported required terminology | PASS |
| 6 | No transfer/transformation as Ch.1 required content | PASS |
| 7 | "evidence", never "proof/proves/prove" | PASS |
| 8 | No invented chapter title | PASS |
| 9 | No later-chapter concept leakage into required anchors | PASS |

## Evidence by item

### 1. Big Question — PASS
Verbatim **"Where can we observe evidence of energy causing change?"** appears on slides 2 (BQ intro), 3 (My first thinking), and 33 (BQ · Now I Think). Matches Reader p.1 sidebar and TG Lesson 1 Big Question (TG p.18). The TG Lesson 2 question ("What are some forms of energy?") is correctly **not** surfaced as a second BQ banner — it maps to N2, per contract §1.

### 2. Vocabulary — PASS
Exact, source-faithful definitions (verbatim vs Reader p.1/p.4 and TG Lesson 1 Word Work p.22):
- **energy** — "the ability to cause change" (slides 10, 13) ✓
- **change** — "to become different" (slide 10) ✓
- **stored energy** — "energy that has the ability to cause change at a later time" (slide 20) ✓
Groupings V1 (energy + change, Reader p.1) and V2 (stored energy, Reader p.4) match the notes and contract §2. No other terms added to the V-group card decks.

### 3. Note sections N1–N4 — PASS
All titles, prompts, model chains, tables, and fill-in answers mirror the Guided Notes exactly:
- **N1 "Energy Causes Change"** — fills `cause · change · evidence`; model ENERGY → CHANGE → EVIDENCE (slides 15–16) ✓
- **N2 "Energy Occurs in Different Forms"** — 5 rows motion · sound · light · heat · electrical energy (slide 19) ✓
- **N3 "Objects Can Store Energy"** — fill `position`; 3 rows battery (in a flashlight) · stretched rubber band · raised object (apple); model STORED ENERGY → RELEASE → CHANGE (slides 26–27) ✓
- **N4 "Recognizing Evidence"** — BEFORE/AFTER boxes + "What changed?" + CHECK YOUR THINKING sub-section with starter "We know because we see …" (slides 29–30) ✓
Answers are revealed only on CHECK slides (12, 16, 22, 27); not front-loaded. Confirmed against the notes key.

### 4. Reader page citations — PASS
All on-slide Reader citations fall within pp. 1–6 and match the contract §6 page map:
BQ→p.1 · V1→p.1 (slides 10–12) · N1→pp.1–2 (slides 13–16) · N2→p.3 (slides 17, 19) · V2→p.4 (slides 20–22) · N3→pp.4–5 (slides 23–27) · N4→pp.1–6 (slides 28–30). No out-of-range or fabricated page numbers.

### 5. No advanced unsupported required terminology — PASS
Grep across PPTX body + notes and rendered PDF found **zero** occurrences of: kinetic, potential, gravitational, mechanical, radiant, compression wave, inertia, momentum. "stored energy" and "position" are the Reader's own Grade-4 wording (Reader pp.4–5), not the banned substitutes.

### 6. No transfer/transformation as Chapter 1 required content — PASS
The only "transfer/transformation" occurrence is the Slide 1 **unit banner** ("Unit 1 · Energy Transfer & Transformation"), which is the unit title, not Chapter 1 taught content (allowed; contract §7 + QA gate). No slide teaches transfer/transformation; Reader p.6 ("Energy Can Move and Change") is not taught — it is only reflected in the N4 synthesis page range (pp.1–6), consistent with the contract §6 note "forward preview only." Note: TG Lesson 1 does list `transfer`/`transform` as *Language of Instruction* (teacher-modeled), but the project contract §7 and `VOCABULARY_PROGRESSION.md` deliberately scope these out of Chapter 1 — and the slides honor that.

### 7. "evidence", never "proof/proves/prove" — PASS
No on-slide "proof/proves/prove." Speaker notes on slides 14 and 28 contain the meta-instruction strings *"using 'evidence' not 'proof'"* and *"Evidence, not proof"* — these instruct the teacher to avoid "proof" (correct pedagogy), not claims of proof. No violation.

### 8. Chapter title — PASS
Chapter title is **"Energy Causes Change"** (slide 1 title; chrome "CHAPTER 1 · ENERGY CAUSES CHANGE"), matching the Reader chapter title and the 7 exact Reader titles. No invented title.

### 9. No later-chapter concept leakage — PASS
Grep found **no** leakage into required notes/anchors: no "energy transfer", "energy transformation", "energy of motion", "speed", "collide/collision", "convert/conversion", "chemical energy". The five forms taught in N2 (motion, sound, light, heat, electrical energy) are Reader p.3's own Chapter-1 forms, not later-chapter vocabulary. "release" (N3 model) is the Reader's p.4 wording, not transfer language.

## Required fixes
None.

## Reviewer notes
- Read-only review; no artifact or source file was modified.
- Cross-checked the rendered PDF: 45 pages == 45 slides; banned-term grep on the PDF returned only the unit-title occurrence (Slide 1).
- Automated QA (`qa/reports/PHASE_4_CH1_SLIDESHOW_QA.md`) independently reports PASS with "banned language: none" and "transfer/transform outside unit title: none" — consistent with this review.
