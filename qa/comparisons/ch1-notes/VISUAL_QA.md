# CH1 NOTE-FORMAT COMPARISON — VISUAL QA

> Part E. Both masters rendered headless to PDF (LibreOffice) → page images (`qa/temp/ch1-notes/`, 110 DPI) and measured programmatically (PIL + `pdfinfo`). Grayscale-print legibility checked via foreground darkness.

## INB (3 inserts, Letter 8.5×11 carrier pages)

| Check | Result | Note |
|---|---|---|
| Clipping / overflow | PASS | all text present in `pdftotext -layout`; no run truncated |
| Overlap | PASS | no stacked text; nested tables render in order |
| Font size | WARN | primary text 12 pt; assembly labels 10 pt (glue strip, "LIFT THE FLAP") — readable but at the low end |
| Writing space | PASS | vocab blanks, before/after box (1.08"), scavenger record lines |
| Drawing space | PASS | before/after boxes 1.08" tall; stored-energy draw box 1.4" |
| Grayscale legibility | PASS | min foreground darkness = 31 (navy on white); light tints (memory chips, flap cells) still contrast |
| Page utilization | PASS | 5.9–8.6% ink coverage; balanced whitespace |
| Visual hierarchy | PASS | title → section caps → body → labels |
| Whitespace balance | PASS | no giant empty boxes; drawing areas intentionally blank |
| Line spacing | PASS | writing lines 360 twips (≈1.15) with bottom border |
| Table readability | PASS | nested tables render cleanly |
| Trim boundaries | PASS | dashed border measured **7.00″ × 9.07″** per insert (target ≈7.0×9.0) |
| Glue zones | PASS | shaded top strip labeled "GLUE — TOP EDGE" on every insert |
| Reduced-size readability | WARN | 10 pt labels + 12 pt body hold up at 7×9, but flap/glue micro-labels are small |

## Guided Notes (3 pages, Letter portrait)

| Check | Result | Note |
|---|---|---|
| Clipping / overflow | PASS | 3 pages, no text truncated |
| Overlap | PASS | clean |
| Font size | PASS | title 22 pt · headings 16–17 pt · body 13–14 pt · floor 11 pt (only memory-cue sub-captions) |
| Writing space | PASS | full 7″-wide lines; 4 lines for synthesis reasoning |
| Drawing space | PASS | before/after boxes 1.32″; stored-energy box 1.6″ |
| Grayscale legibility | PASS | min foreground darkness = 31; mean darker than INB (more dark ink) |
| Page utilization | PASS | 3.5–5.9% ink coverage; content bbox ends ≥1.5″ from bottom (balanced, not crammed) |
| Visual hierarchy | PASS | title → heading caps → body → captions |
| Whitespace balance | PASS | generous but intentional |
| Line spacing | PASS | writing lines 26–30 pt (≈0.36–0.42″) |
| Table readability | PASS | evidence table + forms table clean |
| Trim boundaries | N/A | no trimming (full-page notes) |
| Glue zones | N/A | no gluing |
| Full-page readability | PASS | 13–14 pt body comfortable at full page |

## Overall visual verdict
- **INB: PASS** (2 WARNs: small assembly labels, 9.07″ box is +0.07″ over the 9.0″ nominal — fits a 9.75″ composition page).
- **Guided Notes: PASS** (no warnings).
- Neither format has clipping, overlap, or grayscale-contrast failures.
