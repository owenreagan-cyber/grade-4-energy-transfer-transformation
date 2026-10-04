# PHASE 1.1 — VISUAL SYSTEM RECONCILIATION AND FREEZE

> Cleanup/freeze pass on the Phase 1 visual system. Scope: visual system only — no curriculum
> content, no Chapter 1 production artifacts, no Canva, no installs, no commit/push.
> Canonical source: `assets/visual-system/design-tokens.json` (`UNIT1_VISUAL_SYSTEM_VERSION = 1.0`, FROZEN).

## 1. What Works

- **Figma ↔ local dimensions reconciled.** Chapter Tab corrected 320×60 → **320×52** (radius 12 → 10); Vocabulary Card corrected 560×170 → **560×360** (with visual region + 64pt term + TEACH tag). Verified live via Figma `get_metadata`/`use_figma`.
- **Chapter palette parity confirmed.** All 7 Figma palettes (`ch1–ch7` primary/accent/neutral/surface) + 5 unit neutrals match the canonical hex exactly (verified via `get_variable_defs`/`getLocalVariablesAsync`).
- **Canonical dimensions promoted into the token file.** `design-tokens.json` now carries a `components` block (chapter tab, vocabulary card, BQ panel, HUD bubble, resource badge); the generator consumes it, so there is one dimension source.
- **Parity gate implemented.** `tools/qa_visual_system.py` gate 8 validates the Figma parity manifest against tokens *and* against generated local SVGs.
- **Grayscale proof generated.** `tools/build_visual_system.py` emits `qa/temp/phase1_visual/grayscale_proof.png` (B/W contact sheet of notes/assessment/slide + vocabulary card + 7 palettes), with a matching QA gate.
- **Design-system freeze.** `design_system_version = 1.0`, `status: FROZEN`, version identifier `UNIT1_VISUAL_SYSTEM_VERSION = 1.0` stored in the token file only.
- **Automated QA:** 9/9 gates PASS (contrast, grayscale, font floors, overflow, render integrity, component consistency, token validation, figma parity, grayscale proof).

## 2. What's Missing

- **No live Figma API in headless QA.** Parity is enforced via the versioned manifest snapshot, not by live extraction. Figma re-verification remains a manual/MCP step (procedure documented in the manifest).
- **No automated Avenir Next↔Inter visual-diff.** The Figma pilot substitutes Inter (Avenir Next not bundled in Figma); the substitution is documented, not pixel-verified.
- **No grayscale *regression baseline*.** The proof proves "readable in B/W" structurally; there is no stored golden image to diff against on future regens.

## 3. Fixes — specific problems + exact fixes

| # | Problem | Exact fix |
|---|---|---|
| 1 | Figma Chapter Tab 320×60 vs canonical 320×52 | Resized Figma component `2:13` to 320×52 and radius 12→10 (canonical rx 10) |
| 2 | Figma Vocabulary Card 560×170 vs canonical 560×360 | Resized Figma component `2:5` to 560×360, added the accent-tinted visual region + 64pt term + right-aligned TEACH tag |
| 3 | Component dimensions not machine-readable (competing source risk) | Added `components` block to `design-tokens.json`; generator reads it; QA cross-checks it |
| 4 | No parity validation between Figma snapshot and canonical tokens | Added `assets/visual-system/figma-parity-manifest.json` + QA gate 8 (colors + dims vs tokens + local SVGs) |
| 5 | No B/W proof of the sample set | Added `grayscale_proof()` to the generator + QA gate 9 (present, non-blank, all-gray pixels) |
| 6 | `rsvg-convert` version not recorded | Recorded certified version 2.62.3 + reproducibility policy in `docs/technical/TOOLCHAIN.md` |
| 7 | Initial parity gate compared manifest chapters to token chapters (which carry `name`/`keywords`) | Fixed comparison to per-slot (`primary/accent/neutral/surface`) check |

## 4. Enhancements / Suggestions / New Ideas

- Store a **grayscale golden baseline** (or content hash) so future regenerations can diff against a known-good B/W proof.
- Add a **Figma export step** to dump variable values + component dims to JSON in one `use_figma` call, so the manifest can be regenerated deterministically rather than hand-edited.
- Consider a **font-substitution assertion** (local renders use Avenir Next; Figma uses Inter) as a documented checklist item rather than an automated gate.
- Extend the `components` block to cover diagram node/arrow/label so all diagram primitives are token-governed too.

## 5. Edge Cases & Failure Modes

- **Token edit without Figma/manifest update.** QA gate 8 catches token↔manifest drift, but Figma itself can still silently diverge until the next manual re-verification.
- **`rsvg-convert` version change.** Detected only by `--version`; requires re-certification (policy recorded). No automated pin guard.
- **Font fallback.** Avenir Next is unavailable in Figma and absent on non-macOS CI renders; local SVGs carry a full fallback chain, but a missing-font machine would rasterize with Helvetica/Arial (acceptable, but not pixel-identical).
- **Grayscale proof blank check.** A near-all-white proof (e.g. if a source PNG failed silently) is caught by the mean-brightness gate, but a subtly-broken proof is not.
- **`bq_panel` width.** Canonical BQ panel is full-width (96pt tall); the manifest records `width_mode: full`, so QA checks height only — width is intentionally context-dependent.

## 6. Performance Concerns

- Generator + QA are both **one-shot and fast** (single-digit seconds); no watch modes, no servers, no persistent processes.
- Grayscale proof uses PIL in-process; no external rasterizer beyond the already-required `rsvg-convert`.
- Parity gate is a **pure in-memory JSON/dict comparison** — negligible cost.

## 7. Readability / Maintainability

- One token file + one parity manifest + two scripts; the manifest is clearly marked "not a source of truth".
- `components` block keeps dimensions adjacent to the other tokens; the generator and QA both read it, eliminating hand-synced literals.
- The parity comparison is per-slot, so adding a chapter only extends the existing loop.
- Documentation is layered: standard → token reference → component catalog → theme map → parity manifest → this freeze review.
