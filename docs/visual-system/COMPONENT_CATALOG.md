# COMPONENT CATALOG

> Reusable visual components for Unit 1. Each entry is a *specification* — the editable
> master lives in Figma (`Grade 4 Energy — Unit 1 Visual System`) and the canonical local
> assets live in `assets/visual-system/`. Colors/fonts/radii resolve from
> `assets/visual-system/design-tokens.json` (`UNIT1_VISUAL_SYSTEM_VERSION = 1.0`, FROZEN).
>
> Canonical component dimensions are machine-readable in `design-tokens.json` (`components`) and
> cross-checked against Figma via `assets/visual-system/figma-parity-manifest.json` in QA.

## Core reusable components

### A. Unit title slide
16:9. Unit name at **deck major 50 pt** on the chapter `primary` band or plain white, unit tagline, and the unit resource badge. No curriculum content.

### B. Chapter title slide
16:9. Chapter tab (top-left) + chapter title at **42 pt** in chapter `primary` + Big Question teaser. One idea; title + BQ only.

### C. Big Question panel
Full-width `primary` band (12 pt radius, 96 pt tall) with a single-line Big Question at **34 pt white bold**. The permanent "BQ" anchor.

### D. Guided Notes BQ anchor
Print. `primary` band (64 pt tall) with the Big Question at **19 pt white bold**, top of every notes page.

### E. Vocabulary card
Premium science card (see "Vocabulary card system" below). Canonical frame **560 × 360 pt** (full-screen on slides); compact 2-up on notes reuses the same architecture.

### F. V1/V2 section treatment
Vocabulary note sections: a `primary` section label ("KEY WORDS") + short 2 pt `primary` underline, followed by the term/definition fill-ins. Mirrors the slide's V mode.

### G. N1/N2 section treatment
Note sections: a `primary` section label (e.g. "MODEL IT" / "CHECK YOUR THINKING") + 2 pt `primary` underline, then ruled writing lines (0.75 pt) at generous spacing.

### H. HUD action bubble
Full-round pill (999 radius, 240 × 64 pt) in chapter `primary`, white **24 pt bold** action word + line icon. Temporary action guidance (see "HUD action system").

### I. Resource badge
Full-round pill (999 radius, 260 × 44 pt) in `ink`, white **15 pt bold** text. Document-level only; do not repeat per page.

### J. Diagram label
White tag (8 pt radius, 1 pt `rule` border) with **13 pt DemiBold** label. Points to diagram nodes/arrows.

### K. Before/after comparison panel
Two equal panels side by side, each with a `surface` fill + labeled "BEFORE" / "AFTER" header + the state visual. Shared 1.25 pt border; consistent labels.

### L. Data table
Shaded header row (10% `primary` tint) + bold ink header + 1.5 pt `primary` rule; 0.75 pt row rules; min row height 0.5" portrait / 1.1" landscape.

### M. Student graph
2 pt axes, 1 pt ticks, data marks in chapter accent + ink, light grid. Paired with the data table; no heavy grid.

### N. Teacher callout
Left 3 pt `primary` bar + 6% `primary` tint fill + 12 pt radius + convention tag pill (`MATERIALS`, `LISTEN-FOR`, …). Playbook-only.

### O. Assessment section header
**20 pt bold `primary`** section title + 2 pt `primary` rule across the content width. Distinct from note section headers (larger + full-width rule).

### P. Score box
10% `primary` tint fill + 1.25 pt `primary` border + 8 pt radius, showing `SCORE ___ / N` at **14 pt bold `primary`**. Always raw score + percentage.

### Q. Lab setup diagram
Clean apparatus line-art: correct apparatus, no stock clutter, arrows = model not mechanism, labeled nodes/arrows from the diagram system.

### R. Teacher Playbook chapter tab
`primary` rounded tab (10 pt radius, 320 × 52 pt) with `CHAPTER N · TITLE` at **16 pt white bold**, top of each playbook chapter.

## HUD action system

**Approved normal actions:** `RECITE · WRITE · PREDICT · VOTE · TURN & TALK · CHECK · TRACE · DRAW · WATCH`
**Optional:** `OBSERVE · EVIDENCE · DATA · ENGINEER · EXPLAIN`

- HUD is **temporary action guidance** — it signals what students *do right now*.
- HUD is **not** note navigation. Permanent student note navigation stays `BQ / V1 / V2 / N1 / N2`.
- One HUD bubble per slide; never stack multiple competing actions.

## Resource badge system

`GUIDED NOTES · PRACTICE · LAB · SCIENCE JOURNAL · REVIEW · STEM CHALLENGE`

- Document-level, compact, consistent (single `ink` pill style).
- Place once per document/page; do **not** overload pages with repeated badges.

## Vocabulary card system

One premium architecture, used everywhere:

- **Default:** 2 cards per slide (or 2-up on a notes page); 3 only for short, still-readable terms; 1 for major emphasis.
- Each card: large custom science visual (restrained frame) · huge vocabulary term · exact Reader definition · small Reader page reference · restrained 1.25 pt frame · chapter-theme accent bar.
- Avoid ornate fantasy/trading-card styling.
- `TEACH` tag distinguishes the teaching card from the `RECORD` fill-in note (fill-in from memory, card covered).

## Diagram system

Reusable science-diagram language (arrows = model, not mechanism):

- **Object/source nodes** — rounded `surface`-fill node with `primary` label.
- **Path arrows** — straight transfer arrow in chapter accent.
- **Receiver nodes** — rounded node, distinct from source.
- **Evidence labels** — `label-tag` pointing to the observed change.
- **Energy-form labels** — compact tag naming the form (Grade 4 terms only).
- **Before/after state markers** — two-panel comparison with `BEFORE`/`AFTER` headers.
- **Motion arrows** — curved arrow.
- **Transfer arrows** — straight arrow.
- **Transformation markers** — diamond marker at the arrow midpoint.
- **Cause/effect relationships** — chevron arrow.

No unsupported advanced vocabulary (kinetic, potential, mechanical, radiant, compression-wave, inertia).
