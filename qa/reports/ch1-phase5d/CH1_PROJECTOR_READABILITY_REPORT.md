# CH1 Projector Readability Report (Phase 5D)

## Affected set (from the independent review WARN register)

Slides 17, 19, 26, 27, 44, 45.

## Analysis

| Slide | Essential text | Rendered size | Contrast | Distance risk | Remedy applied |
|---|---|---|---|---|---|
| 17 | five-form card labels ("motion, sound, light, heat, electrical energy") | 24 pt bold white on navy | high | chip labels ~24pt — at the instructional floor | none (validation) |
| 19 | N2 table row labels + writing areas | 24 pt labels / 22 pt header | high | row text smallish from back | none (validation) |
| 26 | N3 WRITE table + blank line | 24 pt labels / 20–22 pt header | high | dense table | none (validation) |
| 27 | N3 CHECK sample answers | 28 pt **italic muted-amber** | **low-mid** | answers light at distance | **FIXED — answer ink darkened to `INK` (#1A1D26)** |
| 44 | review 6 option C (multi-line) | 28 pt | high | multi-line option small | none (validation) |
| 45 | review 6 answer C + explanation | 28 pt option / 28 pt explain | high | density | none (validation) |

## Determination

- The deck's **instructional font floor is already 24 pt** (labels) / 28–30 pt (body) — above the projector minimum in `docs/standards/SLIDESHOW_STANDARD.md` and the builder's `T_KICK = 24` floor.
- The one concrete defect the review observed — **slide 27's light, low-contrast N3 answer column** — was **fixed** by darkening the answer ink (no text change, no geometry change; parity unaffected).
- The remaining items (17, 19, 26, 44, 45) are **subjective projector-distance WARNs**, not deterministic failures. The independent review itself states it "does not establish actual back-of-room physical projector readability."

## Method limitation

A reduced-size preview was generated (110 DPI previews + contact sheet), but this is a screening aid, not a substitute for a real projector calibration. A genuine back-of-room check was not performed in this environment.

## Remedy recommendations (for the visual-review gate, not applied in v3)

If the owner's back-of-room review still finds these small:
1. Slide 17 — enlarge form-chip label region (24 → 26 pt) and re-verify `check_fit`.
2. Slide 19/26 — raise table row height and label size (24 → 26 pt) within the reserved table region.
3. Slide 44/45 — widen the review-6 option column so choice C stays on fewer lines (the `grid` layout already measures; a one-line option needs a wider box).

These are layout-only changes (font size / box size); they do not touch canonical text, so parity would remain intact. They are deferred pending a real projector read rather than applied speculatively.

## Final status

**VISUAL_REVIEW_REQUIRED** for slides 17, 19, 26, 44, 45. **FIXED** for slide 27 (contrast).
