# CH1 FINAL DESIGN SYSTEM SPEC

Phase 5A. Premium design system for the Chapter 1 hybrid rebuild. Builds on the frozen Unit 1 Visual
System v1.0 tokens (`assets/visual-system/design-tokens.json`) + the Codex v5 premium treatments.

Identity: **modern museum exhibit + excellent elementary science textbook + strong classroom
presentation.**

## 1. Canvas

- 16:9, 13.333″ × 7.5″ (12192000 × 6858000 EMU) — unchanged.
- Safe margin 0.45–0.55″; no required text in extreme corners.

## 2. Palette (final — locked)

| Token | Hex | Use |
|---|---|---|
| Warm Cream (surface) | `#F5EEDC` | default slide background |
| Deep Navy (primary) | `#1F2A5A` | titles, nodes, chrome, BQ banner |
| Dark Media Navy | `#0E1428` | media shells, cinematic hero backdrops |
| Classic Gold (accent) | `#A67C16` | arrows, reveals, HUD, highlights |
| Muted Amber (neutral) | `#7A5620` | captions, secondary labels |
| Charcoal Navy | `#1B223C` | secondary nodes / deep cards |
| White | `#FFFFFF` | cards, text-on-navy |
| Card Border | `#E4DAC4` | card outlines |
| Gold Tint | `#F3E8CF` | reveal highlight fill / visual panels |
| Navy Tint | `#E3E7F2` | TEACH pill fill |

Grayscale-safe (color never the only signal); accent ≥ 3:1 vs white after desaturation.

## 3. Typography (final — verified against local fonts)

Deterministic finding: **installed** fonts = Avenir Next ✓ · Georgia ✓ · Helvetica/Helvetica Neue ✓.
**NOT installed** = Inter, Source Sans, Aptos, Merriweather. Using a non-installed family risks
LibreOffice headless substitution. Final:

| Role | Family | Size |
|---|---|---|
| Display / chapter title | **Georgia** (serif) | 48–50 pt |
| Slide title | **Georgia** | 40–46 pt |
| Body | **Avenir Next** | 28–32 pt |
| Body (dense) | Avenir Next | 28 pt |
| Vocab term | **Georgia** | 54–68 pt |
| Vocab definition | Avenir Next | 28 pt |
| Notes section heading | Avenir Next | 32 pt |
| Kicker / subtitle / Reader ref | Avenir Next | 24 pt (italic) |
| HUD / badge | Avenir Next | 24 pt (bold) |
| MCQ option | Avenir Next | 28 pt |
| Table cell | Avenir Next | 24 pt |
| Chapter tab / page ref | Avenir Next | 12–16 pt |

**Floor: 24 pt** for essential instructional text (never below). Font sizes vary by slide purpose
(hero vocab 54–68, table cells 24) — no single forced size. Fallback chain for Georgia:
Georgia → Times New Roman → serif. For Avenir Next: Avenir Next → Helvetica Neue → Helvetica → Arial.

## 4. Component specifications (19)

All instructional text is editable PPTX. Coordinates in inches (13.333 × 7.5 canvas). Reference the
canonical builder helpers (`tools/build_ch1_slides.py`: `header`, `chapter_tab`, `mode_badge`,
`hud_bubble`, `anchor_chip`, `vocab_card`, `model_strip`, `before_after`, `notes_heading`,
`write_line`, `review_question`, `review_answer`).

1. **Chapter opener** — navy full-bleed photo + gold chapter pill (top-left) + Georgia title 48–50 +
   kicker "Discovery / Evidence" + BQ line (28 italic) + `ENERGY→CHANGE→?` teaser + unit footer. No
   standard top bar.
2. **Big Question** — cream bg; navy banner (0.55,1.7 → 12.23×1.9) with BQ 34 pt white bold;
   supporting line 28; "Think" prompt 30 bold; faint `ENERGY→CHANGE→?` ghost at 6–8% opacity.
3. **Phenomenon (dark→bright)** — two-panel BEFORE/AFTER (7.4×2.6) + right conclusion card; matched
   split image behind or beside.
4. **Before/after** — `before_after` two equal paper cards, gold labels 28, hints 28.
5. **Observe (pencil)** — single big paper card with photo crop + "BEFORE" gold label + descriptive
   line; bottom "Look closely" prompt.
6. **Predict** — navy bg or paper card; sentence stem 30 + blank; "Make a prediction" line.
7. **Explain** — `ENERGY→CHANGE→?` model strip (11.8×1.0) + conclusion text 30 centered.
8. **Recite** — navy card (11.8×2.2) with recite line 38 white bold + "Say it together" 30.
9. **Vocabulary hero** — `vocab_card`: paper card, navy top band, TEACH pill, "VOCABULARY" 24 caps,
   term 54–68, definition 28, gold-tint visual panel (photo), Reader page 16. Two cards side-by-side
   on slide 10 (5.95 each).
10. **Five-form comparison** — 5 equal navy chips (2.2×1.2) for the terms + 5-panel photo strip or 5
    per-form photo cards with captions 28.
11. **Stored-energy example** — vocab card + hero photo (rubber band stretched-still).
12. **Instructional model/diagram** — `model_strip` navy nodes + gold `RIGHT_ARROW`s; sizes 24–30.
    N1 `ENERGY→CHANGE→EVIDENCE` (last box empty until reveal); N3 `STORED ENERGY→RELEASE→CHANGE`.
13. **WRITE** — `notes_heading` (anchor chip + title 32 + Reader ref 24 italic) + blanks (underline)
    + instruction 28 italic. Never reveals answer.
14. **CHECK** — identical geometry to its WRITE pair; reveal answer in gold bold; answer strip 28.
15. **Application (slide 32)** — three paper cards (10.3×1.0) listing scenarios; bottom "Pick one"
    line; no on-slide evidence rule (spoken after vote).
16. **Optional media** — dark media navy bg, centered 16:9 frame with gold border, title + prompt +
    fallback line. (Not used in the canonical Session 1/2; only if a future optional media slide is
    authorized.)
17. **Review question** — `review_question`: title 32 + question 30 bold + 4 A/B/C/D cards (11.3×0.74)
    with gold letter 28. No correct-answer signal.
18. **Review reveal** — same geometry; correct card gets gold-tint fill + gold border + bold; rationale
    strip (12.23×0.72) at bottom 28.
19. **Final BQ synthesis** — navy BQ banner + "Now I think…" + 3 ruled lines + subdued reflection
    photo at 20–30% behind; `ENERGY→CHANGE→EVIDENCE` model at bottom.

## 5. Image treatment rules

- Reuse existing approved imagery; no regeneration. Text never baked (render labels in PPTX).
- No magical glow / energy beams / invented energy. No watermarks/logos.
- Matched before/after keep object identity, geometry, scale, camera.
- Full-bleed heroes: crop-safe; scrim only for contrast.

## 6. QA expectations (per component)

16:9 · fonts present (Georgia + Avenir Next) · body ≥ 28 pt (tables/captions ≥ 24) · no clip/overflow
· no required text < projector floor · grayscale-safe · notes-mapped slides mirror Guided Notes
exactly · no answer leakage · no out-of-scope vocabulary.
