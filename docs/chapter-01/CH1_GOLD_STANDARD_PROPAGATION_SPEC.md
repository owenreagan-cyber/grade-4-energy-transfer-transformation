# CHAPTER 1 — GOLD-STANDARD PROPAGATION SPEC

> What Chapters 2–7 inherit from the frozen Chapter 1 exemplar.
> This is a **specification**, not a Chapter 2 build. It defines the reusable architecture
> and the per-chapter adaptation rules so Chapters 2–7 reproduce Chapter 1's quality
> **without mechanical copying**.

Companions:
- `docs/chapter-01/CH1_GOLD_STANDARD_FREEZE.md` — what is frozen, and the rules for editing it.
- `docs/chapter-01/CH1_PACKAGE_MANIFEST.md` — the canonical Chapter 1 file inventory (the pattern each chapter manifest must follow).
- `assets/visual-system/design-tokens.json` — FROZEN Unit 1 Visual System v1.0.
- `docs/visual-system/CHAPTER_THEME_MAP.md` — the seven locked chapter palettes.

## Legend

- **INHERIT EXACTLY** — reuse the same structure/rule with no per-chapter variation.
- **ADAPT BY CHAPTER** — keep the rule, substitute the chapter's own source content (vocabulary, Reader pages, demo, palette).
- **DO NOT COPY MECHANICALLY** — a Chapter 1-specific value is not a template; derive the chapter's own equivalent.

---

## A. PROCESS

| Rule | Class |
|---|---|
| **Notes before slides.** Guided Notes are authored and finalized before the matching slideshow is built. | INHERIT EXACTLY |
| **Source review before layout.** Curriculum Source Reviewer verifies Reader/TG fidelity (title, Big Question, vocabulary, definitions, claims, page ranges, no advanced terminology, no chapter leakage) before any artifact is laid out. | INHERIT EXACTLY |
| **BQ/V/N handoff.** The locked Big Question / Vocabulary / Notes anchors are written once, then mirrored verbatim into notes → slides → playbook → quiz/key. | INHERIT EXACTLY |
| **Independent QA.** The reviewer is not the author; reviewer stays read-only unless explicitly switched to fix mode. | INHERIT EXACTLY |
| **Playbook sync.** Chapter spread, demo guide, slide map, and supporting-resource index are generated from real filenames and real slide/page numbers. | INHERIT EXACTLY |
| **Package manifest.** Each chapter publishes a `CH<n>_PACKAGE_MANIFEST.md` recording every canonical file, role, and status; no competing manifest. | INHERIT EXACTLY |
| **Authoritative pages, vocabulary, and demo.** | ADAPT BY CHAPTER |
| **N-section count, slide count, and supporting-resource set.** | DO NOT COPY MECHANICALLY |

---

## B. GUIDED NOTES

| Rule | Class |
|---|---|
| **Anchor architecture.** BQ (Big Question) → V1/V2 (vocabulary groups) → N1…Nn (note sections) → CHECK YOUR THINKING → BQ · NOW I THINK. | INHERIT EXACTLY |
| **BQ/V/N codes persist across the unit.** V1/V2/N1… codes are a shared navigation language. | INHERIT EXACTLY |
| **Layout rules.** Premium readability, generous writing space, printability, grayscale survival. | INHERIT EXACTLY |
| **Blank logic.** Blanks target the teachable concept (word or short phrase), not entire sentences; multi-word blanks get adequate width. | INHERIT EXACTLY |
| **Handwriting rules.** Clear handwriting clearance under every blank. | INHERIT EXACTLY |
| **Font floors.** No run below the 8 pt floor (headings/body larger). | INHERIT EXACTLY |
| **Key parity.** Teacher key is a page-for-page, blank-for-blank mirror of the student page (3-page student ⇄ 3-page key for Ch1). | INHERIT EXACTLY |
| **No redundant permanent-content duplication.** A fill-in never also appears as a hidden-answer on a later unrelated surface. | INHERIT EXACTLY |
| **Reader page references** printed on each section. | INHERIT EXACTLY |
| **The number of N sections** (Ch1 uses N1–N4) and the specific vocabulary/forms. | DO NOT COPY MECHANICALLY |

---

## C. SLIDES

| Rule | Class |
|---|---|
| **Anchor synchronization.** BQ/V/N slide anchors mirror the notes' BQ/V/N exactly (same wording, same grouping). | INHERIT EXACTLY |
| **HUD use.** Temporary HUD action bubbles (MODE · TIME · ASK · LISTEN FOR · REVEAL · NEXT) are visually distinct from permanent BQ/V/N navigation. | INHERIT EXACTLY |
| **Visual-density rules.** No content crowding; each slide carries one teaching job; projector-readable at the back of the room. | INHERIT EXACTLY |
| **Reader integration.** Reader cues are printed on-slide; note-writing slides are visibly anchored; non-anchor slides never hide required note answers. | INHERIT EXACTLY |
| **Review-slide architecture.** End-of-chapter review = question state → answer state, multiple choice (A/B/C/D), letters shuffled. | INHERIT EXACTLY |
| **Demo choreography.** Predict → observe → before/after → change = evidence. | INHERIT EXACTLY |
| **BQ return.** A "NOW I THINK" return-to-BQ write slide closes the chapter. | INHERIT EXACTLY |
| **No advanced unsupported vocabulary** on any slide. | INHERIT EXACTLY |
| **Chapter palette** (primary/accent/neutral/surface from `CHAPTER_THEME_MAP.md`). | ADAPT BY CHAPTER |
| **Exact slide count** (Ch1 = 45) and **exact slide numbers** for anchors/demo/review. | DO NOT COPY MECHANICALLY |

---

## D. SUPPORTING RESOURCES

| Rule | Class |
|---|---|
| **Create only if it adds a distinct instructional job.** No worksheet that merely recopies notes; the practice page must be a distinct APPLY task. | INHERIT EXACTLY |
| **Journal vs worksheet decision rule.** Journal = reflection/drawing (secondary). Worksheet = distinct apply/reasoning task. Journal prompts are not duplicated as worksheets. | INHERIT EXACTLY |
| **Absent/makeup support.** A self-contained recovery guide (Reader + notes + demo substitute) must exist per chapter. | INHERIT EXACTLY |
| **FLEX labeling.** Enrichment/optional resources are labeled OPTIONAL/FLEX, never CORE/REQUIRED. | INHERIT EXACTLY |
| **Study-guide contribution + assessment trace.** Each chapter contributes both (for later unit-level study-guide / review-game / final assembly). | INHERIT EXACTLY |
| **Teacher keys** exist wherever a student resource is scored or has a definitive answer set. | INHERIT EXACTLY |
| **Scored-resource keys mirror the student resource** (same items, same order, same point totals). | INHERIT EXACTLY |
| **Which specific resources exist** (Ch1 = practice + quiz + detectives + journal + FLEX + recovery) — later chapters may need labs/builds Ch1 did not. | DO NOT COPY MECHANICALLY |

---

## E. TEACHER PLAYBOOK

| Rule | Class |
|---|---|
| **Actual filenames.** Playbook cites real production filenames, never invented ones. | INHERIT EXACTLY |
| **Actual page/slide references.** Reader range, notes page count, slide count, and BQ/V/N/demo/review slide numbers are real. | INHERIT EXACTLY |
| **Required statuses.** Honest statuses (CORE / OPTIONAL/FLEX / REQUIRED / AVAILABLE / PLANNED / FINAL) and honest Graded column. | INHERIT EXACTLY |
| **Collect/grade status** matches the chapter's real scored items (no "no scored item" if a graded quiz exists). | INHERIT EXACTLY |
| **Timing, materials, if-short-on-time guidance** present and honest. | INHERIT EXACTLY |
| **The teacher should never need to leave the Playbook** to know what to use. | INHERIT EXACTLY |
| **Chapter-specific Reader pages, BQ, vocab, demo, and spread contents.** | ADAPT BY CHAPTER |

---

## F. QA

Required gates before any chapter is declared complete (mirrors `docs/planning/QA_GATES.md`):

| Gate | Class |
|---|---|
| Source fidelity (Curriculum Source Reviewer) | INHERIT EXACTLY |
| Guided Notes conformance (BQ/V/N, blanks, parity, printability, grayscale) | INHERIT EXACTLY |
| Slideshow conformance (anchors, HUD, density, review architecture) | INHERIT EXACTLY |
| Notes ↔ slideshow sync (automated anchor mirror) | INHERIT EXACTLY |
| Supporting-resource necessity + key completeness | INHERIT EXACTLY |
| Teacher Playbook sync | INHERIT EXACTLY |
| Package manifest vs filesystem | INHERIT EXACTLY |
| Active-reference cleanup (no stale labels/wording) | INHERIT EXACTLY |
| Reproducibility (build scripts reproduce artifacts deterministically) | INHERIT EXACTLY |
| Automated QA master run (visual-system, notes, slides, sync, playbook, package) | INHERIT EXACTLY |
| Independent final certification (read-only reviewer) | INHERIT EXACTLY |

All gates must PASS before freeze. WARN is permitted only if explicitly non-blocking and unsuitable for correction within the chapter.
