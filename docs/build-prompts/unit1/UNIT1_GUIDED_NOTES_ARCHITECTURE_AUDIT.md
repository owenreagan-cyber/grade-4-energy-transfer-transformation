# UNIT 1 — GUIDED NOTES ARCHITECTURE AUDIT

> Cross-chapter architecture audit for the Unit 1 Guided Notes family. **This is a planning/audit document, not a build prompt.** It compares the planned Ch1–7 Guided Notes architecture so the final output is **one coherent Unit 1 family** without forcing every chapter into identical content structure.

## Purpose

Prevent accidental template drift across Chapters 1–7 while allowing chapter-specific differences that are justified by content (source, vocabulary count, lab/model needs). The frozen Ch1 (v1.1) and Ch2 (v1.0) are the **exemplars**; Ch3 is built-uncertified; Ch4–7 are being rebuilt.

## Status

- **Ch1, Ch2:** FROZEN exemplars — architecture is the benchmark.
- **Ch3:** BUILT_UNCERTIFIED — audit to confirm it matches the family (no rebuild unless drift found).
- **Ch4–7:** REBUILD target — build prompts live in `01_guided-notes/`.

## Comparison matrix (must be filled in during each chapter build, then reconciled)

| Dimension | Ch1 (exemplar) | Ch2 | Ch3 | Ch4 | Ch5 | Ch6 | Ch7 | Family rule |
|---|---|---|---|---|---|---|---|---|
| Title treatment | Chapter badge + 21–24 pt serif | | | | | | | Same: badge `CHAPTER N · TITLE`, serif title |
| Name/Homeroom header | `Name: ____  Homeroom: ○4A ○4B ○4C ○4D` | | | | | | | Identical on every student page; no Date, no Score |
| Page numbering | — | | | | | | | Footer page ref (if used) consistent |
| Chapter/unit label | top-left badge | | | | | | | Same position |
| Anchor badge style | BQ / V1 / V2 / N1… / CHECK / BQ·NOW I THINK | | | | | | | Same code language |
| BQ initial treatment | BQ banner + optional 2–3 line think | | | | | | | BQ banner + ≥2 ruled lines |
| Vocab treatment | KEY WORD rows, 1.5–2.0 in blanks + Reader ref | | | | | | | Same; add WORDS YOU MAY SEE only where needed |
| N-anchor treatment | section heading + model/diagram | | | | | | | Same; N-count varies by content (justified) |
| CHECK treatment | 2–3 retrieval/application items | | | | | | | Same |
| BQ final treatment | 3–4 ruled lines ≈ 1.15–1.45 in | | | | | | | Same (locked) |
| Reader references | printed per section | | | | | | | Same |
| Table style | shaded header, min row heights | | | | | | | Same |
| Writing lines | ruled, Grade 4 spacing | | | | | | | Same (locked measurements) |
| Drawing boxes | ≥ 3.2 × 2.1 in | | | | | | | Same |
| Teacher-key answer style | gold/dark-blue bold, ANSWER/SAMPLE, no red | | | | | | | Same |
| Grayscale behavior | color never the only signal | | | | | | | Same |
| Font sizes | title 21–24 · section 15–17 · body 13.5–14 (floor 12) | | | | | | | Same |
| Margins | 0.50–0.55 in sides | | | | | | | Same |
| Page-fill target | 70–88% | | | | | | | Same |

## Flag categories

1. **Inconsistent architecture** — a chapter deviates from a family rule with no justification (must fix).
2. **Accidental template drift** — e.g., a chapter drops the Homeroom circles, changes blank spacing, or renames an anchor (must fix).
3. **Justified chapter-specific difference** — content-driven (e.g., Ch3 has a lab data table, Ch6 has a three-way verdict panel, Ch7 has a concept map) and does not break the family.
4. **Unjustified chapter-specific difference** — a stylistic change not required by content (must fix).

## Rulings (locked)

- **Do not let obsolete INB slide architecture drive new notes.** Derive structure from Reader/TG + pacing + notes architecture first.
- **Page count is a target, not frozen**, unless an accepted production decision explicitly locks it. Allow ±1 page; never compress writing to hit an arbitrary count.
- **Final `BQ · NOW I THINK` is locked at 3–4 ruled lines ≈ 1.15–1.45 in** in every chapter.
- **Teacher keys preserve student geometry exactly** (including Name/Homeroom header), plus a non-reflowing `TEACHER KEY` badge.
- **Necessary-writing audit** applies to every chapter: ~15–30% student-completed content; print facts that don't benefit from transcription.
- **Core vs supporting vocabulary** (KEY WORD vs WORDS YOU MAY SEE) applies wherever a chapter has non-test supporting terms (especially Ch7 history).

## Reconcile points (check after each chapter build)

- Does this chapter's badge, header, BQ banner, vocab row, N-section, CHECK, and BQ-final match the Ch1/Ch2 exemplar geometry?
- Are any differences justified by content (vs. drift)?
- Does the teacher key preserve geometry?
- Does the final BQ have 3–4 ruled lines?

## Next action

No build here. This audit governs the `01_guided-notes/` build prompts (already written) and will be re-checked when the Ch4–7 candidates are rendered for acceptance.
