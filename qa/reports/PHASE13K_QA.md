# PHASE 13K — HIGH-VALUE GAP CLOSURE QA

> Automated + content QA for the Phase 13K gap-closure artifacts (four high-value non-media gaps + two nice-to-haves).

## 1. Visual QA (render + inspect)

All new DOCX masters were exported to PDF (LibreOffice headless) and rendered to images for inspection.

| Artifact | Pages | Blank pages | Clipping/overflow | Font floor | Table fit | Handwriting space | Grayscale |
|---|---|---|---|---|---|---|---|
| `unit2-written-study-review.docx` (student) | 3 | none | none | 12 pt (verified) | OK | generous | yes |
| `unit2-written-study-review-key.docx` | 1 | none | none | 13 pt | OK | — | yes |
| `ramp-it-up-setup-guide.docx` | 1 | none | none | 12 pt | OK | — | yes |
| `crash-lab-setup-guide.docx` | 1 | none | none | 12 pt | OK | — | yes |
| `water-wheel-setup-guide.docx` | 1 | none | none | 12 pt | OK | — | yes |
| `solar-device-setup-guide.docx` | 1 | none | none | 12 pt | OK | — | yes |

- Review sheet body is 13 pt; absolute floor 12 pt (verified programmatically: min run size = 12.0 pt).
- Diagrams use black/white/light-gray fills + thick outlines → grayscale-printable and readable from a prep table.
- Teacher/student labels: student sheet + key are clearly labeled; guides are marked "TEACHER ONLY".

## 2. Scientific / vocabulary QA

Word-boundary scan of every new file for: proof/proves, kinetic, potential, mechanical energy, chemical energy, thermal energy, radiant, momentum, impulse, electron, compression wave, base-load, peak demand, grid stabilization, fission.

**Result: zero inappropriate hits.** All matches are teacher-facing guardrails:
- "use evidence, never proof" / "not 'proves'" (corrective instruction).
- "No advanced terms (kinetic, potential, mechanical, radiant, momentum, impulse)" (disclaimer list).

The only student-facing new file (`unit2-written-study-review.docx`) is clean. "geothermal energy" (a legitimate Reader term) contains the substring "thermal energy" but is not the banned term.

The solar guide avoids "efficiency" (uses "observable device output"); the water-wheel guide uses "final locked primary response" as specified.

## 3. Climate / controversial content QA

Scan of every new file for: climate change, global warming, carbon, zero carbon, carbon footprint, climate crisis, climate activism, save the planet, energy policy, carbon tax, cap and trade.

**Result: zero hits** across all new student- and teacher-facing files.

## 4. Path integrity QA

- 148 concrete paths across the master map/index/inventory/printing/prep/quickstarts resolve to real files.
- All 19 new files verified present (DOCX + PDF + Markdown + build scripts).
- Remaining non-resolving references are pre-existing range/wildcard shorthands (e.g., `0X-chX-*`, `chapter-0X/*`) plus the documented future archive target `archive/retired/` (convention only — no directory created by policy alone).

## 5. Scope guard

No pacing, guided notes, slide sequencing, assessment content, lab science, Friday Flex, video integration, or course architecture was reopened. No new videos/quizzes/homework/labs/games/assessments/maps were created.
