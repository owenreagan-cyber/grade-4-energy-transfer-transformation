# CH1 Pencil Image Root Cause and Replacement (Phase 5D)

## 1. Original defect (confirmed by independent review + project records)

The `BEFORE` pencil photograph reads as **already sharpened/pointed**, while the canonical wording describes a **dull/flat tip** ("A dull pencil — tip is flat, and it is quiet", slide 6; "dull tip · quiet", slide 8).

## 2. Exact source, identity, SHA-256, referencing slides

| Field | Value |
|---|---|
| Source file | `assets/ch1/candidate-v2/slide-09-pencil-before-after.png` |
| Asset ID | R03 (`CH1_PREMIUM_VISUAL_SELECTIONS.md`) |
| SHA-256 (short) | `920594e1…` (full: `920594e1` prefix, per Phase 5A manifest) |
| Dimensions | 1942 × 809 |
| `pen_before` crop | left half `(0, 0, 971, 809)` |
| `pen_after` crop | right half `(971, 0, 1942, 809)` |
| Referencing slides | 6, 8, 10 (change card BEFORE|AFTER), 36, 37 (review 2) |

## 3. Root cause

- The generation prompt requested "before pencil is dull and longer, after pencil is shorter and sharply pointed" (`IMAGE_GENERATION_MANIFEST.md`).
- The rendered composite's **before half does not visibly deliver a flat/blunt tip** — it reads as a formed point.
- The Phase 5C record already flagged this as **D3 — NEW_ASSET_RECOMMENDED: "the approved BEFORE pencil (R03) does not visibly show a flat tip… No image was generated."** (`CH1_REMAINING_ISSUES.md`).

## 4. Replacement option assessment

| Option | Candidate | Verdict |
|---|---|---|
| Option 1 — reuse existing | `slide-06-pencil-before.png` (1536×1024) | **REJECTED** — single close-up, no matched before/after pair (Phase 5A explicitly disqualified it). |
| Option 1 — reuse existing | `ch1-pencil-evidence-01.jpg` (1920×1234) | **REJECTED** — evidence/shavings scene, not a matched dull-before state. |
| Option 1 — reuse existing | `slide-25-stored-examples.png` / others | Not a pencil before/after pair. |
| Option 2 — reconstruct/edit | n/a | **FORBIDDEN** — cannot deceptively edit a pointed pencil to look dull (produces a scientifically misleading object). |
| Option 3 — new source image | — | **REQUIRED** (owner approval) — see spec below. |

## 5. Replacement-image specification (Option 3 — for owner approval)

A matched BEFORE/AFTER pair (single photographic scene, same pencil, same electric sharpener, same camera/scale/lighting/background):

- **BEFORE:** the same yellow pencil with an **unmistakably flat/blunt tip** (tip visibly squared/rounded, graphite core flush, no point), positioned beside or just outside the electric sharpener; longer than the AFTER state.
- **AFTER:** the same pencil **shorter and sharply pointed**, ordinary shavings visible.
- No embedded text, no watermark, no logo, no visible "energy", no glow.
- Premium editorial science-textbook lighting and focus; text-free; crop-safe.
- Minimum resolution sufficient for a 6.2×3.75 in (slide 6) and 4.0×2.6 in (slide 8) panel at ≥ 120 effective DPI.
- The pair must keep the same object identity and perspective so "same pencil" is self-evident.

## 6. Required checks (before resolving)

- Full source-image visual inspection (both states).
- Final-crop visual inspection.
- Full-slide render of slides 6, 8, 10, 36, 37.
- Comparison against canonical caption meaning ("dull tip").
- Answer-leakage re-check (review 2 options must not be answered by the photo).
- Regression across every slide using the source.

## 7. Final status

**BLOCKED.** The rendered BEFORE image does not visibly agree with the canonical "dull/flat tip" wording, and no suitable matched replacement exists in the approved library. Resolution requires the owner-approved replacement pair above (or explicit authorization to generate one). Until then, slides 6, 8, 10, 36, 37 remain flagged; the v3 candidate keeps the current (defective) R03 image unchanged and unmodified.
