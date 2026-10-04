# UNIT 1 · CHAPTER 1 PILOT — PRE-BUILD READINESS AUDIT

> **Phase — AUDIT / PLANNING ONLY. No production artifact was modified, regenerated, extracted permanently, or committed.**
> Planning inputs: `docs/reviews/UNIT1_INSTRUCTIONAL_RESTRUCTURING_AUDIT.md` (authoritative), plus live inspection of the Ch1 deck/spec/outline, premium notes, worksheets, quiz, infographic, source Reader Ch1, and colleague Ch1 intake.
> Authoritative sources: `assets/authoritative/teacher-guide/Science 4 - Energy Transfer - TG .pdf` · `assets/authoritative/student-reader/complete/Science 4 - Energy Transfer - Student Book.pdf` (Ch1 = Reader pp.1–6).

---

## 1. What Works

### A. Executive Readiness Verdict

**READY WITH CONDITIONS.** Chapter 1 is the most mature chapter in the unit — it already has a teaching deck, a slide spec, premium notes, a practice worksheet, an application worksheet, a quiz + blueprint, an infographic, per-chapter teacher docs, source-map, and full QA. The target choreography is ~80% present.

The conditions that must be resolved before production begins are **documentation/asset unification issues, not content defects**:

1. **Three competing Ch1 slide artifacts** exist with three different slide counts (outline = 28, spec = 25, deck = 26). Production must pick ONE canonical sequence (§H, §M).
2. **No vocabulary-card artifact exists** (content is ready in `VOCABULARY_PROGRESSION.md`, but the card design/template is not).
3. **No demonstration guide or virtual-demo backup exists** for Ch1 (demo *content* lives in `01-ch1-teacher-notes.md`).
4. **No consolidated design-token/icon document exists** — palette/typography live in outline headers only.

None of these blocks *content* authoring, but each will stall production mid-build if not fixed first. Two are **BLOCKERs**, the rest **NON-BLOCKING** (§M).

### B. Chapter 1 Current Artifact Inventory

| Layer | Artifact | Path | State |
|---|---|---|---|
| Deck | Teaching deck | `production/slides/01-ch1-energy-causes-change-slides.pptx` | RELEASED (26 slides actual) |
| Deck spec | `01-ch1-energy-causes-change-slide-spec.md` | RELEASED (25 slides: 22 + 3 cues) |
| Deck outline | `production/slides/outlines/01-ch1-slideshow-outline.md` | RELEASED (28 slides, NotebookLM source) |
| Notes | Premium guided notes | `production/premium-notes/01-ch1-energy-causes-change-guided-notes.docx|pdf` | RELEASED (3 pp) |
| Notes (legacy) | `production/student-notes/01-ch1-energy-causes-change-guided-notes.docx` | STALE (pre-rebuild) |
| Practice | `01-ch1-energy-causes-change-practice.docx` | RELEASED |
| Application | `01-ch1-energy-detectives-student.docx` (scavenger hunt) | RELEASED |
| Quiz | `01-ch1-energy-causes-change-quiz.docx` + `-quiz-blueprint.md` | RELEASED (9 items) |
| Infographic | `unit1-energy-detective-anchor.png` (2752×1536) | RELEASED |
| Media | `Stored_Energy.mp4`, `The_Energy_Detective.mp4`, `Energy_Detectives_Briefing.mp4`, `How_Scientists_Spot_Invisible_Energy.mp4` | UNSTAGED (supplemental) |
| Retired INB | `production/student-notebook/chapter-01/01-ch1-interactive-notebook.docx` + release PDF | RETIRED |
| Teacher | `01-ch1-daily-lessons.md` · `01-ch1-teacher-map.md` · `01-ch1-teacher-notes.md` · `01-ch1-supply-prep-guide.md` | RELEASED |
| Source | `01-ch1-source-map.md` | RELEASED |
| QA | acceptance · classroom-simulation · cross-artifact-alignment · educational-suitability · source-validation | RELEASED |
| Recovery | `01-ch1-absent-student-recovery.md` | RELEASED |
| Vocabulary | `docs/planning/VOCABULARY_PROGRESSION.md` (3 Ch1 core terms + exact defs) | RELEASED |

---

## 2. What's Missing

| Gap | Evidence | Class |
|---|---|---|
| Vocabulary-card artifact (teach) | No card template/doc exists; defs ready in `VOCABULARY_PROGRESSION.md` | BLOCKER (for the vocab-card feature) |
| Canonical Ch1 slide sequence | outline=28 · spec=25 · deck=26 (three documents disagree) | BLOCKER (for notes-sync) |
| Demonstration guide (Ch1) | Demo content in `01-ch1-teacher-notes.md`; no unified guide | NON-BLOCKING |
| Virtual-demo backup (sharpener) | No clip exists; only unstaged supplemental mp4s | OPTIONAL |
| Design-token / icon document | Palette/typography only in outline headers; no icon system file | NON-BLOCKING |
| Per-section Reader page refs in notes | Notes have chapter-level range only | NON-BLOCKING (build-scope item) |

---

## 3. Fixes — specific problems + exact fixes

### C. Colleague vs Ours — Chapter 1 Only

| Component | Colleague (Ch1) | Ours (Ch1) | Classification |
|---|---|---|---|
| Title / BQ | Title + Big Question on one slide | Title (S1) + Big Question (S4), separated by hook | KEEP ours (hook-before-BQ is better) |
| Demo | Sharpener, "watch and listen, what changes?" + 3 questions | Sharpener S8, "predict first — then watch" + before/after | KEEP ours (adds prediction) |
| Vocabulary | 3 fill-ins on slide, then answer-reveal slide | Fill-in Key Words in notes; definition slide | ADAPT (add full-screen card = teach, keep fill-in = record) |
| Reader choreography | "Listen & fill in — follow along" with Reader section headings + page refs | Reader slides with page refs, but notes don't mirror headings | ADAPT (borrow page-ref + section-heading mirror) |
| Note structure | One page: vocab → listen&fill (5 sections) → explain it (2 Qs) | 3 pp: KEY WORDS → MODEL IT → DRAW/LABEL → FORMS → STORED → OBSERVATION-VS-EXPLANATION → EVIDENCE TABLE → CHECK YOUR THINKING | KEEP ours (scaffolds are stronger; not re-opening RD-6) |
| Explain It / application | 2 complete-sentence prompts with sentence starters | Check Your Thinking + practice worksheet + Detectives | KEEP ours (richer application) |
| Visuals | Text-only; one "label the five forms" blank | Diagrams/arrows/models + infographic | KEEP ours |
| Slide density | Low (text-only) | Low (one idea/slide) | KEEP ours (parity + richer visuals) |
| Teacher guidance | Demo scripted "say this / listen for / if students ask" | Scattered across teacher-notes + daily-lessons | BORROW (consolidate into demo guide) |
| Assessment prep | "Test Q" tags on notes | Blueprint + study guide + quiz | KEEP ours |
| Pacing | 1 day (35-min routine) | 2 blocks (30-min) | KEEP ours (30-min reality) |
| Student writing load | Light (fill-ins + 2 sentences) | Moderate (fill-ins + draw + evidence table + check) | KEEP ours (justified depth) |

**WHAT COLLEAGUE DOES BETTER:** (1) demo guidance is scripted in one place; (2) Reader section headings + page refs explicitly mirrored in notes; (3) sentence starters on every "Explain It."
**WHAT OURS DOES BETTER:** (1) prediction-before-reveal demo; (2) scaffolded note architecture (MODEL IT / DRAW-LABEL / evidence table / observation-vs-explanation); (3) custom practice + application; (4) richer visuals; (5) assessment alignment is explicit.
**BEST HYBRID:** our deck + our notes + our practice, **plus** (a) full-screen vocab cards, (b) per-section Reader page refs, (c) a consolidated scripted demo guide, (d) sentence starters added to the "Check Your Thinking" prompts.

### D. Keep / Borrow / Adapt / Add / Remove Matrix (Ch1)

| Item | Decision | Detail |
|---|---|---|
| Ch1 deck (concept sequence) | KEEP | hook→BQ→model→demo→forms→stored→exit is sound |
| Ch1 slide spec | ADAPT | reconcile to one canonical slide count + add vocab-card slots + page refs |
| Ch1 premium notes | ADAPT (light) | add page refs + badge; keep scaffold density (RD-6) |
| Practice worksheet | KEEP | already application-focused |
| Energy Detectives sheet | ADAPT → FLEX | keep as Friday FLEX / application, not lesson driver |
| Quiz + blueprint | KEEP | aligned to 25Q final |
| Infographic | KEEP | anchor is premium |
| Demo guidance | BORROW/ADAPT | consolidate into scripted demo guide |
| Virtual demo | ADD (optional) | one sharpener clip, correct apparatus |
| Sentence starters | ADD | to Check-Your-Thinking prompts |
| Reader page refs | ADD | per-section, in notes + slides |
| Vocab cards | ADD | full-screen teach cards |
| Legacy `student-notes/01` | REMOVE (archive) | stale pre-rebuild |
| Retired INB ch1 | REMOVE (archive) | superseded by premium notes |

---

## 4. Enhancements / Suggestions / New Ideas

### E. Visual Asset Reuse Matrix

Legend: **EXTRACT / REUSE** · **REFERENCE / RECREATE** · **DO NOT USE**.

| Source | Slide/Page | Visual | Classification | Intended use | Concerns |
|---|---|---|---|---|---|
| Current deck S8 | sharpener | BEFORE/AFTER dull→sharp + noise icon | EXTRACT / REUSE | demo slide | icon set must be consistent (see §L) |
| Current deck S10–15 | forms | 5 icons (motion/sound/light/heat/electrical) | EXTRACT / REUSE | forms section | consolidate icon style |
| Current deck S7 | model | ENERGY→CHANGE→EVIDENCE arrows | EXTRACT / REUSE | model slide + notes MODEL IT | already correct |
| Current deck S17–19 | stored | battery→flashlight→light sequence | EXTRACT / REUSE | stored-energy section | correct, non-misleading |
| Infographic | — | `unit1-energy-detective-anchor.png` | EXTRACT / REUSE | slide anchor / application hook | premium, 2752×1536 |
| Colleague Ch1 | vocab/forms | "label the five forms at the carousel" (blank lines) | REFERENCE / RECREATE | vocab card for "forms" | flat text; recreate as icon+label card |
| Reader p.1 | photo | water balloon POP + splash | REFERENCE / RECREATE | hook/change example | photo; recreate or license-clear |
| Reader p.2 | photo | crashing seashore (sound/sand/sun) | REFERENCE / RECREATE | evidence examples | multi-change scene; recreate as annotated diagram |
| Reader p.3 | photo | carousel (5 forms in one scene) | REFERENCE / RECREATE | forms synthesis | strong anchor; recreate as clean labeled diagram |
| Reader p.4 | photo | battery + flashlight / stretched rubber band SNAP | REFERENCE / RECREATE | stored energy | recreate cleanly |
| Reader p.5 | photo | apple held high (stored energy of position) | REFERENCE / RECREATE | position/stored | recreate; key concept |
| Reader p.6 | photo | napping cat in sunlight | REFERENCE / RECREATE | "energy can move/change" (NOT Ch1 core; forward-pointer) | only as optional extension |
| `Stored_Energy.mp4` | — | supplemental | DO NOT USE (unstaged; no classroom-cut) | — | no accepted classroom cut |
| `The_Energy_Detective.mp4` etc. | — | supplemental | DO NOT USE (unstaged) | — | not accepted |

**Summary: 6 EXTRACT/REUSE · 6 REFERENCE/RECREATE · 3 DO NOT USE** (see §RECONCILIATION summary below).

### F. Premium Visual Opportunity Map (Ch1 concepts)

| Concept | Preferred treatment | Why |
|---|---|---|
| Energy = ability to cause change | DIAGRAM (definition card + arrow to change) | abstract; needs a labeled model, not a photo |
| Change as evidence | DIAGRAM (ENERGY→CHANGE→EVIDENCE chain) | the unit's core model; must be visual |
| Observable before/after | BEFORE / AFTER (dark→light, still→moving) | comparison is the point |
| Motion | CUSTOM ILLUSTRATION (rolling ball → moved block) | simple, controllable, no stock clutter |
| Sound | CUSTOM ILLUSTRATION (bell → waves → ear) | "model, not mechanism" — no compression-wave detail |
| Light | DIAGRAM (bulb → bright wall) | clean cause→effect |
| Heat | CUSTOM ILLUSTRATION (warm cup → melting) | teacher-controlled; no hot-plate imagery |
| Electrical energy | CUSTOM ILLUSTRATION (cord → carousel lights) | source-appropriate only; no electron detail |
| Stored energy (battery) | SEQUENCE (battery → flashlight → light) | shows "energy stored → released → change" |
| Stretched rubber band | CUSTOM ILLUSTRATION (loose vs stretched → SNAP) | before/after of the release |
| Raised apple / position | CUSTOM ILLUSTRATION (apple held high → falls) | position concept; clean, no photo ambiguity |
| Carousel (five forms) | READER VISUAL → recreate as labeled DIAGRAM | one scene, five forms; powerful anchor |

**No decorative visuals.** Every item above maps to a comprehension/comparison/memory/modeling/navigation function.

### G. Guided Notes Readiness

| Note section | Classification | Note |
|---|---|---|
| BIG QUESTION | KEEP | correct (Reader p.1) |
| KEY WORDS (energy/change/evidence) | TEXT ALIGNMENT FIX | `evidence` is Language of Instruction (no Reader page) — keep as project-preferred term; add page refs for energy (1), change (1) |
| MODEL IT | KEEP | ENERGY→CHANGE→EVIDENCE is the core model |
| DRAW / LABEL (before/after) | KEEP | premium; supports comparison |
| FORMS OF ENERGY (5-form table) | LIGHT CLEANUP | add icons per form (visual enhancement) |
| STORED ENERGY (3 examples) | KEEP | correct |
| DRAW ONE STORED-ENERGY EXAMPLE | KEEP | premium writing space |
| OBSERVATION VS EXPLANATION | KEEP | supports evidence reasoning |
| EVIDENCE TABLE | KEEP | premium |
| CHECK YOUR THINKING | TEXT ALIGNMENT FIX (add sentence starter) | borrow colleague's "start with:" convention |
| REMEMBER (ENERGY→CHANGE→EVIDENCE) | KEEP | cumulative retrieval |
| CONNECT | KEEP | chapter link |

**No content added for density.** Only page-ref labels + a sentence starter + icons. RD-6 (keep density) is **not** reopened.

### H. Slide / Notes / Reader Synchronization Readiness

**Critical finding:** Ch1 has **three slide documents with three different slide counts**:
- `outlines/01-ch1-slideshow-outline.md` → **28 slides** (NotebookLM source, has talking points + cue legend)
- `01-ch1-energy-causes-change-slide-spec.md` → **25 slides** (22 instructional + 3 notes cues)
- `01-ch1-energy-causes-change-slides.pptx` → **26 slides** (actual)

The reconciliation audit flagged Ch5 for *lacking* a spec; Ch1 has the inverse problem — **too many, disagreeing** slide documents. The `ENERGY_GUIDED_NOTES_SLIDE_ALIGNMENT.md` matrix references the 28-slide outline, while the spec references 25. Production must declare the **actual deck (26) as canonical**, regenerate the spec to match it, and retire/align the outline + matrix.

**Notes-cue count (RD-6 confirmed):** 3 notes-cue slides map to the *definition, model, and stored-energy* sections only. The notes' other sections (forms table, evidence table, check-your-thinking) are completed via discussion/practice, not a dedicated NOTES slide — this is acceptable and does **not** violate the mirror rule, because those sections are *not* projected as NOTES-mode slides. The mirror rule ("every NOTES slide matches the paper exactly") is satisfied for the 3 cues; it does **not** require every notes blank to have a cue slide.

**Reader section mirroring:** notes use scaffold labels, not Reader section headings. Add per-section page refs as *labels* (§F of restructuring audit), do **not** replace scaffolds.

### I. Demo / Virtual Demo Readiness

- **Live demo content:** READY. `01-ch1-teacher-notes.md` already carries the sharpener demo with "say this" phrasing, misconception notes (don't claim unobserved heat), and safety. Consolidate into the scripted guide.
- **Virtual demo:** NOT READY (does not exist). Requirements trace:
  - correct apparatus (electric sharpener, not hand) → must be specified in the generation brief
  - visible shape change (pencil dull→sharp, shavings secondary) → must be the PRIMARY evidence, not loose shavings
  - authentic audible sound → required
  - no "mechanical energy" / advanced terms → already enforced by media policy
- **Classification:** live demo = BLOCKER-adjacent (content exists, needs consolidation); virtual = OPTIONAL (P3).

### J. Energy Detectives Salvage Plan

- The **deck** `Energy_Detective.pptx` is **not in the repo** (only in `~/Downloads`) — do not treat it as a build dependency; it is a colleague/prior-iteration source, not ours.
- **Salvage the following from the worksheet + infographic:**
  - `01-ch1-energy-detectives-student.docx` (scavenger hunt: Part A demo evidence, Part B 3-classroom-changes, Part C stored-energy battery) → **KEEP as Friday FLEX / application (P)**, not a lesson driver.
  - `unit1-energy-detective-anchor.png` → **EXTRACT/REUSE** as the chapter anchor / application hook.
- **Too dense / do not reuse:** the Detectives briefing's case-file framing (multiple "cases") — collapses into the simpler 3-part scavenger hunt.
- **Verdict:** keep the worksheet as FLEX; use the anchor infographic; do **not** let the Detectives deck shape lesson structure.

### K. 30-Minute Pacing Analysis

Target elements: opening/BQ · demo · discuss · vocab · read · checks · notes · application · BQ return.

**Recommendation: TWO 30-minute blocks.** Forcing into one block harms instruction.

**Block 1 — "Observe & Name" (~30 min)**
| Min | Segment | Mode |
|---|---|---|
| 0–2 | Title + Big Question | BQ |
| 2–7 | Live demo: sharpener (predict → observe) | D |
| 7–10 | Observe/discuss: what changed? (before/after) | T |
| 10–16 | Vocabulary cards (energy, change) + vocab notes fill-in | V + N |
| 16–26 | Read Reader pp.1–3 (chunk 1: change is evidence) | R + C |
| 26–29 | Notes: MODEL IT + DRAW/LABEL | N |
| 29–30 | Exit / BQ touchback | C |

**Block 2 — "Forms & Stored" (~30 min)**
| Min | Segment | Mode |
|---|---|---|
| 0–3 | Warm-up: recall energy = cause change | C |
| 3–8 | Read Reader p.3 (five forms) | R |
| 8–13 | Vocabulary card: stored energy | V |
| 13–20 | Read Reader pp.4–5 (rubber band, apple position) | R + C |
| 20–26 | Notes: FORMS table + STORED examples + evidence table | N |
| 26–29 | Application: one "Energy Detective" example (P) or journal (J) | P/J |
| 29–30 | Return to Big Question | BQ |

The break occurs **after Block 1's "change is evidence"** (a clean conceptual seam: "what is energy / change" → "forms / stored energy"). This preserves the observe-first sequence and keeps the notes mirror intact. The Energy Detectives full scavenger hunt moves to Friday FLEX.

### L. Visual System / Art Direction (Ch1, propagatable)

| Element | Treatment |
|---|---|
| Title hierarchy | deck major 50 pt · slide 42 pt · body 32 pt · labels 28 pt (existing outline tokens) |
| Chapter badge | `CHAPTER 1 · ENERGY CAUSES CHANGE` top-left |
| Mode badge | pill: BQ / D / V / R / C / N / W / T / P / J (mode-shift, not re-theme) |
| Big Question | navy band, single line, large type |
| Vocabulary card | large word + icon/illustration + exact source def + Reader page + "TEACH" tag |
| Notes slide | exact mirror of paper (same section label, bullets, blanks, order, diagram) + "NOTES" mode badge |
| Reading slide | Reader page number + section heading + permitted crop |
| Check slide | A/B/C/D or signal (thumbs), one check per idea |
| Demo slide | BEFORE/AFTER + "predict first — then watch" |
| Visual comparison | two-panel BEFORE/AFTER, consistent labels |
| Diagram style | navy/coral/gold/light palette, grayscale-safe, arrows = "model, not mechanism" |
| Photo treatment | only where realism matters; clean frame, no stock clutter |
| Worksheet/activity header | shared "UNIT 1 · CH1 · PRACTICE/ACTIVITY" badge |
| Teacher note convention | LIVE/BACKUP/TIME/ASK/LISTEN-FOR/NEXT/IF-SHORT-ON-TIME |

**Palette (from existing outline):** navy `#2F3C7E` · coral `#C03D3D` · gold `#E8C54A` · light `#F4F4F8`. **No icon-system file exists** — this is a missing dependency (§M). Goal: family resemblance + clear mode shifts, **not** one identical template.

---

## 5. Edge Cases & Failure Modes

| # | Edge case / failure mode | Mitigation |
|---|---|---|
| 1 | Vocab card before hook reverses observe-first | card after demo, before reading (§K Block 1) |
| 2 | Vocab card spoils fill-in recall | TEACH (card) vs RECORD (fill-in from memory, card covered) |
| 3 | Sharpener demo unavailable / broken | virtual backup (correct apparatus); fall back to "flip the light switch" as a backup change |
| 4 | Loose shavings over-emphasized as evidence | brief: primary evidence = pencil shape change + sound; shavings secondary |
| 5 | "Proof" language leakage | keep "evidence" not "proof" (Reader says "evidence, or proof" — our policy: evidence only) |
| 6 | Unobserved heat claim (sharpener tip warm) | teacher-notes already flag "treat as optional, teacher-observed" |
| 7 | 3-document slide drift recurs | declare deck canonical; single spec; retire outline/matrix drift |
| 8 | 30-min overflow | two-block split (§K); Friday FLEX buffer |

---

## 6. Performance Concerns

### M. Missing Dependencies / Blockers

| Dependency | Status | Class |
|---|---|---|
| Exact source definitions (energy/change/stored energy) | PRESENT (`VOCABULARY_PROGRESSION.md` + Reader pp.1,1,4) | — |
| Colleague intake (Ch1 slides/notes) | PRESENT (`~/Downloads/Slides ET&T .pdf`, `Student Pages…`) | — |
| Source page images (Reader Ch1 pp.1–6) | PRESENT (chapter split PDF; photos identified) | — |
| Editable visual (icons/illustrations) | PARTIAL (infographic + deck icons exist; no icon library) | NON-BLOCKING |
| Video / virtual demo | MISSING (no sharpener clip) | OPTIONAL |
| Font/style tokens | PARTIAL (palette + pt sizes in outline; no token file) | NON-BLOCKING |
| Icon system | MISSING (no icon set document) | BLOCKER (for consistency across cards/forms) |
| Slide-spec rule (canonical sequence) | CONFLICT (28 vs 25 vs 26) | BLOCKER (for notes-sync) |
| Asset folder convention | PRESENT (`production/infographics/`, `media/`) | — |

**Blocker count: 2** (icon system; canonical slide sequence). Everything else is non-blocking or optional.

### N. Exact Chapter 1 Build Scope (future phase — NOT executed)

| # | Deliverable | Change |
|---|---|---|
| 1 | Ch1 slide deck | reconcile to canonical 26-slide sequence; add vocab-card slots; add mode badges; add page refs |
| 2 | Ch1 slide spec | regenerate to match canonical deck |
| 3 | Vocabulary cards (NEW) | energy / change / stored energy (exact defs + Reader pp.1,1,4) |
| 4 | Notes-slide sync | keep 3 cues; verify mirror fidelity; add "NOTES" badge |
| 5 | Demo slide | sharpen BEFORE/AFTER + "predict first" |
| 6 | Virtual demo (optional) | one sharpener clip (correct apparatus, audio, no mech. energy) |
| 7 | Reader choreography slides | page numbers + section headings + permitted crops |
| 8 | Quick checks | retain exit/retrieval; add one A/B/C/D |
| 9 | Application activity | keep Detectives scavenger hunt as Friday FLEX |
| 10 | Teacher speaker notes | LIVE/BACKUP/TIME/ASK/LISTEN-FOR/NEXT/IF-SHORT-ON-TIME |
| 11 | Visual assets | icon set + recreate Reader carousel/apple/rubber-band visuals |
| 12 | Worksheet updates | sentence starters on Check-Your-Thinking; page refs on notes |
| 13 | Retire stale artifacts | archive `student-notes/01` + retired INB ch1 |

### O. Acceptance Criteria (measurable gates)

**SOURCE FIDELITY** — all content Reader/TG-supported; exact source definitions preserved; no "proof" (evidence only); no kinetic/potential/mechanical/radiant/compression-wave/inertia.

**INSTRUCTIONAL COHERENCE** — sequence clear; modes labeled; no unnecessary duplication (vocab card ≠ vocab note).

**NOTES SYNC** — every NOTES slide matches the paper exactly (section label, wording, bullets, blanks, order, diagram).

**VISUAL QUALITY** — premium; projector-readable (≥28 pt labels); no decorative clutter; every visual teaches.

**MEDIA QUALITY** — correct apparatus; realistic physics; meaningful audio when scientifically relevant.

**PACING** — fits two 30-min blocks (§K) with Friday FLEX buffer.

**ASSESSMENT ALIGNMENT** — Ch1 assessed concepts (Q1, Q2, Q8, Q9, Q11, Q16, Q18) remain supported by notes + slides.

**STUDENT LOAD** — note copying reasonable (3 cues); reading/check/notes rhythm manageable.

**TEACHER USABILITY** — another teacher can teach from deck + playbook without guessing.

---

## 7. Readability / Maintainability

**Structural debt to clear in the build phase:** (1) collapse the 3 slide documents to 1 canonical spec that matches the deck; (2) retire the legacy `student-notes/` + INB duplicates; (3) establish a single design-token/icon file so Ch2–7 don't re-derive the visual system; (4) keep `ENERGY_GUIDED_NOTES_SLIDE_ALIGNMENT.md` regenerated against the canonical deck after any change.

**Maintainability recommendation:** the Ch1 pilot should **also** produce the reusable templates (vocab card, mode badges, icon set, demo-guide format) so Chapters 2–7 inherit rather than re-invent them.

---

*End of Chapter 1 pre-build readiness audit. No production artifact was modified in this phase.*
