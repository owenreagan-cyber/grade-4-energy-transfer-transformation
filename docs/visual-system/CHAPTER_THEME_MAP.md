# CHAPTER THEME MAP

> Unit 1 `Energy Transfer & Transformation` — seven locked chapter themes.
> Authoritative values live in `assets/visual-system/design-tokens.json` (`colors.chapters`). This document is the human-readable reference.

## Semantic roles

Every chapter exposes four color roles used consistently across slides, notes, worksheets, labs, and the teacher playbook:

| Role | Purpose | Contrast floor |
|---|---|---|
| `primary` | deep dominant — chapter tab, BQ band, headings, section rules | 4.5:1 vs white (text + white-on-band) |
| `accent` | bright action — diagram arrows, HUD fills, highlights, data marks | 3:1 vs white (non-text/graphic) |
| `neutral` | muted secondary — secondary text, borders on light surfaces | 4.5:1 vs `surface` |
| `surface` | light background — panels, card backs, tinted regions | — |

Unit-wide neutrals (shared by all seven chapters):

| Token | Hex | Use |
|---|---|---|
| `ink` | `#1A1D26` | primary body text |
| `ink_soft` | `#4A5268` | secondary text, captions |
| `paper` | `#FFFFFF` | default page/slide background |
| `mist` | `#F6F7F9` | alternate panel background |
| `rule` | `#D8DCE4` | hairlines, table row rules |

## The seven themes

### Chapter 1 — Discovery / Evidence
`deep navy · warm gold · cream · muted amber`

| Role | Hex |
|---|---|
| primary | `#1F2A5A` |
| accent | `#A67C16` |
| neutral | `#7A5620` |
| surface | `#F5EEDC` |

### Chapter 2 — Motion
`deep teal · aqua · slate · white`

| Role | Hex |
|---|---|
| primary | `#0F5A5C` |
| accent | `#0E8A97` |
| neutral | `#5B6770` |
| surface | `#FFFFFF` |

### Chapter 3 — Measurement / Data
`cobalt · chartreuse · charcoal · light gray`

| Role | Hex |
|---|---|
| primary | `#1B4FC2` |
| accent | `#5E8A18` |
| neutral | `#2B2F36` |
| surface | `#E9EBEF` |

### Chapter 4 — Pathways / Connections
`violet · cyan · dark indigo · light neutral`

| Role | Hex |
|---|---|
| primary | `#6A3FB5` |
| accent | `#0E93A6` |
| neutral | `#2A2350` |
| surface | `#EFEDF6` |

### Chapter 5 — Impact / Before-After
`deep red · orange · charcoal · cream`

| Role | Hex |
|---|---|
| primary | `#A62626` |
| accent | `#C25A1E` |
| neutral | `#2E2E30` |
| surface | `#F7EFE2` |

### Chapter 6 — Engineering / Transformation
`dark green · brass/gold · blue-gray · off-white`

| Role | Hex |
|---|---|
| primary | `#1F5C3D` |
| accent | `#8F6D24` |
| neutral | `#5A6B7A` |
| surface | `#F4F5F3` |

### Chapter 7 — Innovation / Historical Engineering
`warm sepia · deep brown · tungsten amber · dark slate`

| Role | Hex |
|---|---|
| primary | `#3E2C1F` |
| accent | `#A06E16` |
| neutral | `#2E3238` |
| surface | `#EFE3CE` |

## Family resemblance

The seven themes share one structure — a **deep primary** (headings/bands), a **warm or saturated accent** (action/graphic), a **muted neutral** (secondary), and a **light surface** (background) — so they read as one Unit 1 family while staying clearly distinct chapter-to-chapter. All values pass the unit contrast and grayscale floors (verified by `tools/qa_visual_system.py`).

## Grayscale note

Every primary desaturates **darker** than its accent, so chapter headings and bands survive black-and-white printing. Color is never the only signal — diagrams and labels always carry text + shape + position.
