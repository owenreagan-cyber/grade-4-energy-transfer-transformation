# CH1 Raised-Object Visual Validation (Phase 5D)

## Concern (Phase 5C slide 24 WARN)

The raised-apple photograph (`ch1-stored-raised-apple-01.jpg`, 1440×1920 portrait) did not establish the apple's **height above the ground** strongly enough.

## Root cause

The v2 crop used `focus=(0.5, 0.0)` — a **top-aligned** cover-crop. Because the source is portrait (0.75 aspect) and the slide region is 4.0×4.6 in (0.87 aspect), `cover()` cropped height and, top-aligned, **discarded the lower portion of the image** — the hand and the table/surface that carry the "held up" height cue.

## Remedy (FIXED in v3)

Changed the crop focus to `(0.5, 0.55)` so the cover-crop keeps the **apple + holding hand + table/surface below it** in frame. The apple's elevation is now established by visible reference to the surface beneath it, not by the apple alone.

## Constraints honored

- No scientifically misleading glow, beam, or decorative energy effect added.
- The canonical stored-energy model is unchanged.
- No caption/wording change; parity unaffected.

## Verification

- Slide 24 rendered preview shows the apple with the surface/table context visible below it.
- Structural QA `N3 three examples` and `transfer/transform scope` PASS.

## Final status

**FIXED** (crop improvement). This is a bounded crop/asset-composition fix, not a content change. A final subjective check under a genuine human visual review is still recommended at the whole-slide gate (see `CH1_PHASE5D_READINESS_REPORT.md`).
