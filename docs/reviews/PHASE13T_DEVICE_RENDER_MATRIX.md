# PHASE 13T — DEVICE RENDER MATRIX (Physical iPad A16)

Device: iPad (A16) · iPad15,7 · iOS 27.0 (build 24A437) · native display 1640×2360 @2x · USB (wired)
Viewer: Safari (via `pymobiledevice3` WebInspector inspector-mode navigation) + `xcrun devicectl` screen capture
Render path: local Mac QA server (`http://192.168.4.47:8080`) serving LibreOffice-rendered slide PNGs and release PDFs

All sampled artifacts: OPENED ✓ · RENDERED ✓ · SCREENSHOT ✓ · FONT ISSUE none · LAYOUT ISSUE none · IMAGE ISSUE none · MEDIA ISSUE none.

## Presentations (slide sample — 10 decks, 40 slides)

| FILE | TYPE | ORIENTATION | SLIDES SAMPLED | STATUS |
|---|---|---|---|---|
| `01-ch1-energy-causes-change-slides` | PPTX→PNG | landscape | 1, 2, 11, 26 | CERTIFIED — PREMIUM |
| `03-ch3-energy-speed-slides` (video S17) | PPTX→PNG | landscape | 1, 2, 17, 29 | CERTIFIED — PREMIUM |
| `04-ch4-energy-transfer-slides` | PPTX→PNG | landscape | 1, 2, 21, 47 | CERTIFIED — PREMIUM |
| `06-ch6-energy-transformations-slides` | PPTX→PNG | landscape | 1, 2, 23, 45 | CERTIFIED — PREMIUM |
| `07-ch7-edison-unit-synthesis-slides` (video S13) | PPTX→PNG | landscape | 1, 2, 13, 27 | CERTIFIED — PREMIUM |
| `01-u2-ch1-renewable-nonrenewable-slides` (WATCH S4) | PPTX→PNG | landscape | 1, 2, 4, 22 | CERTIFIED — PREMIUM |
| `03-u2-ch3-slides` (video S7) | PPTX→PNG | landscape | 1, 2, 7, 20 | CERTIFIED — PREMIUM |
| `05-u2-ch5-slides` (video S6) | PPTX→PNG | landscape | 1, 2, 6, 16 | CERTIFIED — PREMIUM |
| `07-u2-ch7-slides` | PPTX→PNG | landscape | 1, 2, 9, 16 | CERTIFIED — PREMIUM |
| `09-u2-ch9-slides` | PPTX→PNG | landscape | 1, 2, 9, 17 | CERTIFIED — PREMIUM |

## Printables (PDF sample — 12 files)

| FILE | TYPE | ORIENTATION | STATUS |
|---|---|---|---|
| `01-ch1-energy-causes-change-guided-notes.pdf` | guided notes | portrait | CERTIFIED — PREMIUM |
| `unit-02-ch1-renewable-nonrenewable-guided-notes.pdf` | guided notes | portrait | CERTIFIED — PREMIUM |
| `03-ch3-ramp-it-up-student.pdf` | lab | portrait | CERTIFIED — PREMIUM |
| `05-ch5-crash-lab-student.pdf` | lab | portrait | CERTIFIED — PREMIUM |
| `water-wheel-flagship-lab-student.pdf` | lab | portrait | CERTIFIED — PREMIUM |
| `solar-device-mini-investigation.pdf` | investigation | portrait | CERTIFIED — PREMIUM |
| `unit1-study-guide.pdf` | study guide | portrait | CERTIFIED — PREMIUM |
| `unit2-written-study-review.pdf` | study guide | portrait | CERTIFIED — PREMIUM |
| `07-unit-final-assessment.pdf` | assessment | portrait | CERTIFIED — PREMIUM |
| `unit-2-written-assessment-student.pdf` | assessment | portrait | CERTIFIED — PREMIUM |
| `01-ch1-friday-flex.pdf` | Friday Flex | portrait | CERTIFIED — PREMIUM |
| `energy-detective-certificate.pdf` | certificate | portrait | CERTIFIED — PREMIUM |

## Cross-renderer notes

- **Video poster frames** confirmed intact on device (no black/blank posters): S17 (Ramp It Up), S13 (Energy recap), S7 (turbine & generator), S6 (wind power).
- **Rebuilt WATCH slides** (pending-video slots) confirmed: play-button visual + `Optional video · Week N` subtitle render cleanly on device.
- No aspect-ratio crop, no letterboxing anomaly, no missing fonts, no broken glyphs observed on the physical display.
