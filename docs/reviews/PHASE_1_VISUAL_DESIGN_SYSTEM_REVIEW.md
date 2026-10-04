# PHASE 1 — VISUAL DESIGN SYSTEM REVIEW

> Independent review of the Unit 1 reusable visual system (Phase 1).
> Scope: visual system only — no curriculum content, no Chapter 1 production artifacts.
> Artifacts under review: `assets/visual-system/design-tokens.json`, `tools/build_visual_system.py`,
> `tools/qa_visual_system.py`, `assets/visual-system/*` (SVG + rendered PNG), the four dummy sample pages,
> `docs/visual-system/*`, `docs/standards/VISUAL_DESIGN_SYSTEM.md`, and the Figma pilot
> (`Grade 4 Energy — Unit 1 Visual System`).

## 1. What Works

- **Single source of truth.** `design-tokens.json` is the only authoritative token file — no competing token
  sources were introduced. Colors, fonts, type scale, spacing, margins, line weights, and the 7 chapter palettes
  all resolve from it.
- **Seven distinct-but-familial chapter themes.** All 7 locked hex palettes are present and distinct while sharing
  the same unit neutrals (ink `#1A1D26`, ink_soft `#4A5268`, paper `#FFFFFF`, rule `#D8DCE4`).
- **Deterministic generation.** `tools/build_visual_system.py` emits 52 canonical SVG assets (icons, HUD bubbles,
  badges, vocabulary card, diagram primitives, chapter palettes + tab) and rasterizes them plus 4 dummy samples via
  `rsvg-convert`, with a PIL contact sheet. Re-runs are idempotent.
- **Headless QA is real and green.** `tools/qa_visual_system.py` passes all gates: contrast, grayscale survival,
  font floors, overflow/margins, render integrity, and component consistency.
- **Component catalog is complete.** Components A–R are specified with concrete dimensions/type; HUD (9 normal + 5
  optional) and the 6 resource badges are locked; the vocabulary card and diagram language are defined.
- **HUD is correctly scoped.** HUD actions are temporary guidance; permanent note navigation (`BQ / V1 / V2 / N1 / N2`)
  is preserved and not conflated.
- **Curriculum untouched.** No Chapter 1 notes/slides/worksheets/labs/assessments/teacher materials were rebuilt; no
  Reader/TG source altered; no commit/push; no Canva auth.

## 2. What's Missing

- **Figma → local parity verification.** Figma holds the editable masters, but there is no automated diff asserting
  Figma variables/components match `design-tokens.json`. Parity is currently by convention, not by gate.
- **Grayscale proof images.** The QA script proves grayscale survival numerically, but no B/W sample page was
  exported for a human eyeball check.
- **Rasterization dependency not pinned.** PNG generation depends on the host `rsvg-convert` binary; its absence or
  version drift is not yet surfaced as a clear, actionable error message.
- **No `TEACH`/`RECORD` second state asset.** The vocabulary-card architecture documents a `RECORD` fill-in state,
  but only the `TEACH` card is generated locally.
- **No explicit before/after panel sample.** Component K (before/after comparison) is specified but not represented
  in the dummy sample set.

## 3. Fixes — specific problems + exact fixes

| # | Problem | Exact fix |
|---|---|---|
| 1 | `TURN & TALK` HUD icon normalized to `turn__talk`, not matching the `turntalk` icon key, so it silently fell back to the checkmark | Added `hud_icon_key()` mapping `"turn & talk" → "turntalk"`; the HUD file now emits `hud/turntalk.svg` with the correct two-speech-bubble icon |
| 2 | HUD bubbles + chapter tab hardcoded Chapter-1 navy `#1F2A5A` (not theme-flexible) | `svg_doc()`/`write_svg()` now accept a `color` attribute; bubbles/tab render `fill="currentColor"` and receive the chapter `primary` via the root `color` attribute, so a single theme value re-tints them |
| 3 | `icons/check.svg` used a 3 pt stroke vs the 2 pt icon standard | Changed check path stroke width `3 → 2` |
| 4 | Sample slide dimensions/type drifted from the catalog (tab 360×56/18 pt, HUD 220×68/28 pt) | Aligned sample slide to the catalog: chapter tab 320×52 @ 16 pt, HUD bubble 240×64 @ 24 pt, resource badge 260×44 @ 15 pt |
| 5 | Playbook `TEACHER PLAYBOOK` badge at 12 pt undershot the resource-badge floor | Raised to 15 pt bold on a 190×44 pill, consistent with the resource badge height |
| 6 | Canonical `chapter-tab.svg` (320×60 @ 17 pt) disagreed with component R (320×52 @ 16 pt) | Unified the chapter tab asset to **320×52 @ 16 pt, rx 10**, matching component R; sample slide updated to match |
| 7 | Stale `hud/turn__talk.svg` persisted after the rename, breaking the HUD-count consistency gate | Added stale-file cleanup in `build_hud()` (removes `.svg` not in the expected key set); regenerated to 14 HUD files |

All fixes verified: `tools/build_visual_system.py` regenerates cleanly and `tools/qa_visual_system.py` reports
`OVERALL: PASS`.

## 4. Enhancements / Suggestions / New Ideas

- Add a **Figma ↔ tokens parity check** (export variable values from the Figma file and diff against
  `design-tokens.json`) before Phase 2 begins production.
- Emit a **grayscale proof sheet** (desaturated PNG) alongside the color contact sheet so reviewers can confirm B/W
  legibility visually, not just numerically.
- Pin/validate the **`rsvg-convert` dependency** with a clear failure message (and an optional Pillow fallback path)
  so a fresh checkout fails loudly instead of silently dropping PNGs.
- Generate the **`RECORD` vocabulary-card variant** (definition hidden, fill-in line) as a second local asset.
- Add a **before/after panel** to the dummy sample set to exercise component K end-to-end.
- Consider a tiny **component "showcase" slide** in Figma that lays out A–R against a neutral grid for quick review.

## 5. Edge Cases & Failure Modes

- **Long Big Questions / terms.** Single-line BQ panel (34 pt) and vocabulary card (64 pt term) have no wrap rules;
  a term longer than the 2-up card width could overflow. Mitigation: 1-card or 3-card layouts are already specified;
  wrap behavior should be explicit before production.
- **`currentColor` theme tinting.** If a component is placed on a non-white background or a consumer forgets the
  `color` attribute, `currentColor` falls back to black. HUD bubbles/badges assume white-on-primary contrast.
- **Grayscale-only printing.** Accent-driven signals (transfer vs transformation markers) must not rely on hue alone;
  shape/diamond vs arrow already differ, but this must be enforced at production time.
- **3-card vocabulary layout.** Only safe for short terms; the QA gate does not yet measure card text fit dynamically.
- **Missing `rsvg-convert`.** PNGs silently fail to generate on hosts without the binary; QA would still pass SVG
  checks but the sample/contact sheet would be absent.

## 6. Performance Concerns

- Generation is **fast** (single-digit seconds for 52 SVGs + 4 samples + contact sheet); no watch modes, no servers.
- QA is **one-shot and deterministic**; both scripts exit cleanly with no persistent processes.
- No network or external-service dependency in the build/QA path (Figma is out-of-band design source only).

## 7. Readability / Maintainability

- **Single token file + two scripts** keeps the system auditable; adding a chapter/component is a token edit +
  generator entry.
- The generator's `svg_doc`/`write_svg` helpers centralize XML emission; the `color`/`currentColor` change makes
  theming a one-line concern instead of hardcoded hex per component.
- Icon keys are explicit (`turntalk` vs normalized action string); `hud_icon_key()` is the single normalization
  point, and `build_hud()` now cleans stale outputs.
- Documentation is layered correctly: standard → token reference → component catalog → theme map, with the review
  file (this doc) recording decisions and fixes.
