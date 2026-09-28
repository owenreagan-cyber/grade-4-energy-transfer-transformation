# PHASE 13G — Week 7 Media Review (Wind + Hydro)

> Final decision on the delivered `Wind___Hydro_Power.mp4` (9:09) for classroom use.
> Companion to `PHASE13F_UNIT2_MEDIA_REVIEW.md` (which rejected the file "as-is").

## Decision

**TRIM → USE.** A clean, fully **contiguous** classroom excerpt was produced and shipped. It covers the
wind-turbine pathway only and contains **zero** forbidden content.

- **File:** `assets/supplemental/media/unit-02/chapter-05/wind-hydro-power-classroom-cut.mp4`
- **Placement:** Week 7 **Monday** (Wind Energy), OPTIONAL / SUPPORT — do NOT also use it Tuesday.

## Source vs output

| | Value |
|---|---|
| Source file | `Wind___Hydro_Power.mp4` |
| Source path | `assets/supplemental/media/unit-02/chapter-05/` |
| Source SHA-256 | `db03356e8b3aea0b4d2e70efee05e60e7a59e3d3aa0467c03378c72f86835ea5` |
| Source runtime | 548.7 s (9:09) |
| Output file | `wind-hydro-power-classroom-cut.mp4` |
| Output SHA-256 | `0d4ec2bd866c531574333291c5c09fea54c78d76920c42ac2195b0a321864dbd` |
| Output runtime | 95.0 s (1:35) |
| Output size | 3,742,861 bytes |
| Codec / resolution | h264 · 24 fps · 1280×720 |
| Audio | aac · 44.1 kHz · mono |
| Cut command | `ffmpeg -ss 156 -to 251 -c:v libx264 -crf 18 -preset veryfast -c:a aac -b:a 128k` |

## Included time range

- **156 s → 251 s** (contiguous, single segment — no stitch, no audio-transition risk).

Content (OCR-verified):

1. *"Energy of Motion in Action — Wind Turbines"* — "Moving air transfers energy to cause blades to rotate."
2. *Push → Spin → Accelerate → Generate* — "Moving air pushes the turbine blades … blades spin a large shaft
   inside … gears spin a smaller generator shaft … generator transforms motion to electricity."
3. *"Wind farms group multiple turbines to generate electricity."*

## Excluded issue ranges (all cut)

| Time | Issue | Disposition |
|---|---|---|
| 0:00–2:36 (0–156 s) | Title + "The Big Rule" + "Synthesizing our Evidence" hammer/pendulum Unit 1 review | excluded |
| 4:12–4:45 (252–285 s) | "Offshore wind … faces severe constraints" (off-topic) | excluded |
| ~6:40–7:50 (400–470 s) | "Zero Combustion" section + coal/wind/hydro carbon comparison table | excluded |
| 8:20–8:30 (500–510 s) | "Renewable resources offer long-term, cost-effective power" (advocacy-leaning) | excluded |
| 8:40–9:09 (520–549 s) | "How will climate change affect renewable power?" | excluded |

## Science review

- Uses the course-approved **"energy of motion"** and **"transfer"** vocabulary.
- Correct wind pathway: **moving air → blades → shaft → generator → electricity.**
- One mild over-technical phrase remains ("gears spin a smaller generator shaft") — harmless, but a teacher
  may gloss it as "the shaft spins faster inside the generator."

## Classroom placement

- **Week 7 Monday — Wind Energy**, after the slide-deck pathway reveal (`05-u2-ch5` S5), as a 1:35
  reinforcement. Do **not** place it on Tuesday (hydro is covered by `06-u2-ch6` deck + Water Wheel lab).

## Verification

- Full decode: clean (`ffmpeg -f null -`).
- Audio present and in sync (aac 44.1 kHz mono).
- First/mid/last frames OCR'd — no black frames, no abrupt content.
- 16-frame dense OCR scan of the output: **zero** hits for climate, carbon, zero-combustion, clean, kinetic,
  potential, mechanical/thermal/chemical energy, fission, electron, base-load, grid.

## Files updated

- `docs/planning/TWO_UNIT_MEDIA_MAP.md` — registry row added + script #6 status changed to "trimmed classroom cut shipped."
- `production/final-8.5-week/ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md` — Wk 7 Mon video reference set to the trimmed cut.
