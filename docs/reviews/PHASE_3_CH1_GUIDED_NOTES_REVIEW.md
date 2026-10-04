# PHASE 3 — CHAPTER 1 GUIDED NOTES REVIEW

> Independent review + source-fidelity certification of the FINAL Chapter 1 Guided Notes.
> Artifact: `production/premium-notes/01-ch1-energy-causes-change-guided-notes.{docx,pdf}` + `…-key.{docx,pdf}` (3 pp each).
> Authoritative sources: CKSci Student Reader Ch.1 (pp. 1–6) + Teacher Guide Lessons 1–2.

## Gate summary

| Gate | Result |
|---|---|
| SOURCE FIDELITY | **PASS** |
| AUTOMATED ARTIFACT QA | **PASS** (17 gates, `qa/reports/PHASE_3_CH1_GUIDED_NOTES_QA.md`) |
| INDEPENDENT QA | **PASS** (2 WARN, non-blocking) |
| TEACHER KEY PARITY | **PASS** (3/3 pages, mirrored layout, all blanks filled) |
| PLAYBOOK SYNC | **PASS** (resource map + playbook updated, playbook QA PASS) |
| SLIDESHOW HANDOFF | **PASS** (`docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md`) |

## Source-fidelity verification (Curriculum Source Reviewer)

- **Big Question:** `Where can we observe evidence of energy causing change?` — exact match to Reader p. 1 margin and TG Lesson 1. (TG Lesson 2's `What are some forms of energy?` is correctly treated as a lesson-level question, addressed by N2, not a second permanent BQ.)
- **Core Vocabulary:** `change`, `energy`, `stored energy` — the only three Chapter 1 Core Vocabulary (TG Lesson 1 Word Work). Exact definitions verified: change = "to become different"; energy = "the ability to cause change"; stored energy = "energy that has the ability to cause change at a later time."
- **Reader page refs:** V1 → p. 1 · V2 → p. 4 · N1 → pp. 1–2 · N2 → p. 3 · N3 → pp. 4–5 · N4 → pp. 1–6. All verified.
- **Forms list:** motion · sound · light · heat · electrical energy — exact match to Reader p. 3 headings (TG Lesson 2 objective).
- **Stored-energy examples:** battery (flashlight), stretched rubber band, raised object (apple) — sourced from Reader pp. 4–5.
- **No later-chapter leakage:** no transfer/transformation (Ch4–6), no kinetic/potential/mechanical/radiant/momentum/inertia/compression wave/gravitational potential. Reader p. 6 "Energy Can Move and Change" is forward-preview only.
- **Terminology nuance (documented):** `evidence` and `position` are TG Language of Instruction (no Reader page #). They appear as concept blanks in N1/N3 (not V-groups) — consistent with the locked project decision to treat `evidence` as preferred student-facing language. Source classification preserved.

---

## 1. What Works

- Notes-first architecture is clean: `BQ → V1 → N1 → N2 → V2 → N3 → N4 → BQ·NOW I THINK`. No slide-mode badges (D/R/C/W) exposed.
- Exact 3-page pagination on both student and teacher key; teacher key visually mirrors student pages 1:1.
- Source-faithful BQ wording, vocabulary, definitions, page refs, forms list, and stored-energy examples.
- Multi-word blank separation honored: `cause` + `change` are two independent blanks (0.9" + 1.4"), never one long underline.
- Generous handwriting clearance: fill lines reserve 26 pt line height; 5-form and 3-example tables give ~0.47–0.50" rows.
- Two model chains (ENERGY→CHANGE→EVIDENCE; STORED ENERGY→RELEASE→CHANGE) + BEFORE/AFTER draw boxes satisfy the "one model/diagram per page" rule.
- Grayscale-safe: chapter primary/accent/neutral all pass ≥3:1 contrast vs white.
- Teacher key distinguishes exact answers (bold neutral-brown) from sample/acceptable responses (italic gray) via a compact one-line legend.

## 2. What's Missing

- Nothing at the acceptance-gate level. Notes intentionally omit: transfer/transformation language, kinetic/potential family, and p. 6 forward-preview content — per scope lock.
- `energy of motion` is not labeled as a term on the notes (Reader p. 3 uses "energy of motion" inside the Motion form). It is deferred to Chapter 2 where it becomes Core Vocabulary. This is correct scoping, not an omission.

## 3. Fixes — specific problems + exact fixes

- *Problem (build-time):* paragraph `after` spacing originally set in twips via raw OXML caused 6-page PDF spillover. *Fix:* switched to `python-docx` `space_before/space_after` in points + `WD_LINE_SPACING.EXACTLY`; tightened section spacing (4–6 pt).
- *Problem:* page 2 content (N2+V2+N3) overflowed by the final `position` fill line. *Fix:* shortened the N2 caption to one line, removed the redundant N3 table caption, reduced table rows 720→680 dxa, and tightened section-head cell margins (20/30→12/18 dxa). Removed the now-unneeded explicit page break before N4.
- *Problem:* teacher key was 5 pages (legend panel + subtitle pushed N1's last line to page 2). *Fix:* collapsed the legend to a single 12 pt line and tightened the subtitle spacing → key now 3 pages matching the student.
- *Problem (QA gate, false positive):* font-floor check flagged 2 pt spacer runs; BQ/V/N order check assumed `V1<V2<N1`. *Fix:* QA now ignores empty spacer runs and asserts the true architecture order `BQ→V1→N1→N2→V2→N3→N4`.

## 4. Enhancements / Suggestions / New Ideas

- (Later, not now) A printed rule-tone for the 5-form table's answer column could improve hand-drawing legibility, but current light border is adequate.
- Phase 4 may optionally add a full-screen vocab card visual per term (TEACH mode), mirroring V1/V2 exactly.
- Consider a single reusable `NOTES_THEME` helper if Chapter 2–7 builders are refactored; not required for Ch1.

## 5. Edge Cases & Failure Modes

- Font substitution: `Avenir Next` is embedded in the PDFs; a small set of glyphs (`→`, `○`, `·`, `—`) substitute via LucidaGrande on this machine. Rendering remains correct; verify on a Windows device before classroom print if exact glyph metrics matter.
- LibreOffice vs Word: pagination is verified in headless LibreOffice; a final open-in-Word sanity check is recommended for the editable master (no content change expected).
- If a teacher prints in grayscale, gold accent (#A67C16) desaturates to ~3.8:1 gray — still readable but lighter than navy; hierarchy relies on weight+size, which holds.

## 6. Performance Concerns

- Build is fast (<2 s for DOCX; PDF export <3 s per file). No long-running processes.
- No network, no Canva, no software installs. All deterministic and reproducible from `tools/build_ch1_guided_notes.py`.

## 7. Readability / Maintainability

- Single builder script produces both student and key from shared section functions (`header`, `big_question`, `vocab_v1/v2`, `note_n1..n4`, `bq_return`), so student/key parity is structural, not copy-pasted.
- FROZEN tokens are hardcoded at the top of the script (mirroring `design-tokens.json`); the tokens file itself is untouched.
- `qa_ch1_guided_notes.py` is self-contained and prints a PASS/WARN/FAIL report to `qa/reports/PHASE_3_CH1_GUIDED_NOTES_QA.md`.

---

## Verdict

All six acceptance gates PASS. Phase 4 slideshow construction may proceed against `docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md`.
