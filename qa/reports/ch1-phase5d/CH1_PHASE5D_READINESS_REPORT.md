# CH1 Phase 5D Readiness Report

## Candidate

| Field | Value |
|---|---|
| Build ID | `ch1-premium-hybrid-v3` |
| Candidate dir | `production/candidates/chapter-01/ch1-premium-hybrid-v3/` |
| PPTX | `01-ch1-energy-causes-change-premium-hybrid-v3.pptx` |
| PDF | `01-ch1-energy-causes-change-premium-hybrid-v3.pdf` |
| Previews | `previews/slide-01..45.png` |
| Contact sheet | `contact-sheet.png` |
| Slide count | **45** |
| PPTX SHA-256 | `b39bb19a1f94a35690beac7a21f53eb0891739cf101aacadeb4613fd2011132a` |
| PDF SHA-256 | `080391450ef529ad60c044156db40da4c71974352055a9f75bb556975ae4bc62` |

## Phase 5D corrections summary

| Item | Disposition |
|---|---|
| Pencil BEFORE (slides 6, 8, 10, 36, 37) | **BLOCKED** — no matched dull-before asset; owner-approved replacement pair required (spec in pencil report). |
| Slide 20 early stored-energy example | **FIXED** — pre-teaching photo removed; concept-first card. |
| Slide 24 raised-apple height | **FIXED** — crop focus lowered to keep hand + table. |
| Slide 27 N3 answer contrast | **FIXED** — answer ink darkened. |
| Projector readability (17, 19, 26, 44, 45) | **VISUAL_REVIEW_REQUIRED** — subjective distance WARNs; remedies proposed, not speculatively applied. |

## QA evidence

| Gate | Result |
|---|---|
| Instructional parity (45/45 text + notes) | PASS |
| Structural QA (28 gates) | PASS |
| Rendered-layout visual QA v2 | 44 PASS / 1 WARN / 0 FAIL (WARN = pre-existing slide-2 chip) |
| Regression vs Phase 5C | none |

## Release status

**BLOCKED.**

Reason: the single highest-priority defect — the pencil `BEFORE` photograph contradicting the canonical "dull/flat tip" wording — cannot be resolved without either (a) an owner-approved replacement-image pair, or (b) explicit authorization to generate one. Per the Phase 5D directive, no deceptive edit was made and no AI imagery was generated. Additionally, a genuine independent whole-slide visual review (a builder's own inspection does not qualify) has not yet been performed.

The candidate is **not** Gold/Production Certified and **not** classroom-ready. It is a separately versioned `BUILT_UNCERTIFIED` candidate carrying three verified visual fixes plus an explicit blocker.

## Unresolved-decision register

| ID | Decision needed | Owner |
|---|---|---|
| D3 (pencil asset) | Approve a new matched dull-before/pointed-after pencil pair, or authorize generation | Owner |
| D1-remnant (readability) | Approve optional font/row enlargement on 17/19/26/44/45, or accept current 24pt+ floor | Owner |
| Independent visual gate | Schedule an independent rendered-slide review of v3 (45 slides) | Owner / reviewer |

## Repository protection (verified)

- Frozen canonical deck unchanged (`production/slides/01-ch1-*.pptx/pdf` untouched).
- Phase 5B candidate (`ch1-premium-hybrid-v1`) unchanged.
- Phase 5C candidate (`ch1-premium-hybrid-v2`) unchanged.
- Guided Notes / teacher key / accepted releases unchanged.
- Nothing staged, committed, pushed, or promoted.
- No visible-desktop automation (headless `soffice` + `pdftoppm` only).

## Next recommended action

1. Owner decision on the pencil replacement image (spec in `CH1_PENCIL_IMAGE_ROOT_CAUSE_AND_REPLACEMENT.md`).
2. Independent rendered-slide review of v3.
3. Only after both: re-render, re-run parity/structural/visual QA, then consider promotion. **Do not promote, commit, or push now.**
