# CH1 GUIDED NOTES ALIGNMENT REPORT

Phase 5A. Verifies the slide→anchor mapping against the **live accepted Guided Notes student packet
and teacher key** (`production/premium-notes/01-ch1-energy-causes-change-guided-notes{,-key}.pdf`),
extracted deterministically via `pdftotext`.

## ⚠️ Critical finding — the task's provided mapping is the BLUEPRINT numbering, not the canonical

The anchor table supplied in the Phase 5A brief uses the **Codex v5 / blueprint** slide numbers. The
canonical frozen deck uses **different numbers** for V1, N2, and V2. This is a genuine conflict that
must be resolved to the canonical sequence (Decision A). It is recorded here rather than silently
chosen.

| Anchor | Brief's (blueprint) slide | **Canonical slide (authority)** | Status |
|---|---|---|---|
| BQ | 2 | 2 | ✓ agrees |
| BQ · WRITE | 3 | 3 | ✓ agrees |
| V1 · WRITE | 12 | **11** | ✗ shifted |
| V1 · CHECK | 13 | **12** | ✗ shifted |
| N1 · WRITE | 15 | 15 | ✓ agrees |
| N1 · CHECK | 16 | 16 | ✓ agrees |
| N2 · WRITE | 20 | **19** | ✗ shifted |
| N2 · CHECK | 21 | **none exists canonically** | ✗ added by blueprint |
| V2 · WRITE | 23 | **21** | ✗ shifted |
| V2 · CHECK | 24 | **22** | ✗ shifted |
| N3 · WRITE | 26 | 26 | ✓ agrees |
| N3 · CHECK | 27 | 27 | ✓ agrees |
| N4 · WRITE/DRAW | 29 | 29 | ✓ agrees |
| CHECK · WRITE | 30 | 30 | ✓ agrees |
| CHECK · REVEAL | 31 | 31 | ✓ agrees |
| BQ · NOW I THINK | 33 | 33 | ✓ agrees |

### Why the shift exists

The blueprint (implemented by Codex v5) **split V1 into two vocab cards** (canonical 10 → blueprint
10+11), **added a "five-forms recap" teaching slide** (blueprint 19), and **added an N2 sample-answers
slide** (blueprint 21). These insertions pushed V1→+1, N2→+1, V2→+2 relative to canonical. Decision A
rejects those insertions, so Phase 5B uses the canonical numbers in the right-hand column.

### The N2 "CHECK" question

The canonical deck has **no N2 CHECK slide**. The builder note on slide 19 is explicit:
*"REVEAL There is no answer slide for N2. Circulate; use student examples as the check."*
The Guided Notes handoff (`CH1_SLIDESHOW_HANDOFF.md`) says N2/N4 are "open writing tasks — never
pre-answered on a slide before the write slide." The blueprint's "N2 CHECK / SAMPLE ANSWERS" slide is
therefore **not part of the canonical 45-slide sequence** and is not rebuilt in Phase 5B. (This is
also listed in the unresolved-decision register as a possible future value-add, but it changes slide
count and is out of scope for Decision A.)

## Verified canonical anchor map (authoritative)

| Slide | Anchor | Write/reveal pair |
|---|---|---|
| 2 | BQ | — |
| 3 | BQ · WRITE | (open) |
| 10 | V1 (cards, both terms) | — |
| 11 | V1 · WRITE | 11↔12 |
| 12 | V1 · CHECK | 11↔12 |
| 15 | N1 · WRITE | 15↔16 |
| 16 | N1 · CHECK | 15↔16 |
| 19 | N2 · WRITE | (open, no check slide) |
| 20 | V2 (card) | — |
| 21 | V2 · WRITE | 21↔22 |
| 22 | V2 · CHECK | 21↔22 |
| 26 | N3 · WRITE | 26↔27 |
| 27 | N3 · CHECK | 26↔27 |
| 29 | N4 · WRITE/DRAW | (open; N4 sample on 31) |
| 30 | CHECK · WRITE | 30↔31 |
| 31 | CHECK · REVEAL | 30↔31 |
| 33 | BQ · NOW I THINK | (open) |

## Exact fill answers (from key; must mirror)

| Anchor | Blank(s) |
|---|---|
| V1 | `change` · `different` |
| V2 | `later` |
| N1 | `evidence` |
| N3 | `position` |
| BQ initial | (any observed change; sample "A pencil gets shorter and sharper.") |
| N4 CHECK | (any change-as-evidence; sample "We know because we see a change, like a ball starting to move or a light turning on.") |
| BQ return | (any change named; sample "…things move, make sound, light up, heat up, or change shape.") |

## Write/reveal geometry contract (enforced in Phase 5B)

- WRITE and CHECK slides for a given anchor use **identical geometry** (same heading position, same
  blank line placement, same table/model layout). CHECK reveals only the answer word(s) in **gold
  accent**, without moving the question.
- N1: student page prints `ENERGY → CHANGE → ▢` (last box empty). Slide 15 (write) asks for the
  sentence blank only; slide 16 (reveal) shows `ENERGY → CHANGE → EVIDENCE` and instructs students to
  copy the word into the last box.
- N3: student page prints `STORED ENERGY → RELEASE → CHANGE`. Slide 26 blank = `position`; slide 27
  reveals `position` plus sample table answers.
- No WRITE slide may leak an answer; no reveal may appear before its write slide.

## Verification status

- ✓ Student packet and teacher key both present and final; anchors V1/V2/N1/N3/N4/BQ match the
  canonical deck and builder.
- ✓ Live materials confirm the canonical numbering above (not the blueprint numbering).
- ⚠ The only open item is the N2 "no check slide" decision — recorded, not forced.
