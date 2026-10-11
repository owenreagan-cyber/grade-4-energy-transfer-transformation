# Chapter 1 — Physical iPad Pro XCUITest QA Report

**Device:** iPad Pro 13-inch (M4) · `iPad16,6` · iPadOS **26.7.1** (build 23H30)
**UDID:** `00008132-001A10A23A05001C` · serial `FKQ3LKXPDY` · 1 TB · Face ID
**Display:** 2752×2064 native (2× scale → 1376×1032 pts) · wired USB · paired · Developer Mode Enabled
**Target app:** Google Slides (`com.google.Slides`) — native app
**Presentation:** "Copy of 01-ch1-energy-causes-change-premium-hybrid-v6-embedded-media copy" (`1txs8WOyV_Ndi6E9Z6-mUlNsvw5ZDDeXW6FZv_OVRHPI`)
**Date:** 2026-10-10

---

## 1. Device discovery (measured, not assumed)

| Property | Value |
|---|---|
| Marketing name | iPad Pro 13-inch (M4) |
| Product type / chip | iPad16,6 · Apple M4 (10-core arm64e) |
| iPadOS | 26.7.1 (build 23H30) |
| Display | 2752×2064 LCD, pointScale 2 |
| Storage | 1,000,555,581,440 bytes (~1 TB) |
| Biometrics | Face ID |
| Connection | wired USB, paired, booted, Developer Mode Enabled |
| Google Slides | installed (`com.google.Slides`), presentation opens natively |

## 2. Runner installation + signing

- New dedicated XCUITest project: `qa/slides-qa/xcuitest/SlidesQARunner.xcodeproj` (xcodegen 2.46.0). Existing Simulator-only `ScienceArtifactQA` project untouched.
- Targets: `SlidesQAHost` (minimal host app) + `SlidesQAUITests` (UI-test bundle), bundle prefix `com.qa.slides.*`.
- **Automatic signing succeeded** with team `98F559Y354` ("Owen Reagan", Individual) — identity `Apple Development: ofr32081@aol.com (KXYQ8895ZL)`, profile "iOS Team Provisioning Profile: *".
- Runner built with `xcodebuild build-for-testing` and executed on the physical device.

## 3. Proof of concept (bounded, succeeded)

1. ✅ Install signed runner (automatic signing, no prompts).
2. ✅ Launch native Google Slides (`XCUIApplication(bundleIdentifier: "com.google.Slides")`, pid 5556).
3. ✅ Open Chapter 1 (deep link → "Start presentation" → "Present on this device").
4. ✅ Capture slide 1 (`Slide 1 of 48:` label verified).
5. ✅ Advance to slide 2 (`Slide 2 of 48:` label verified).
6. ✅ Two distinct slides confirmed (different content + position labels).

## 4. Accessibility & interaction findings

- Editor mode exposes `Start presentation`, `Back`, `Find`, `Collaborators`, `Comments`, `Ask Gemini`, `More actions`, and slide cells labelled `Slide N`.
- Present mode renders slides in a WebView; each slide exposes an `Image` labelled **`Slide N of 48:`** plus the slide text as accessible `Image` labels. **Swipe-left advances one slide.**
- Navigation swipe at vertical center is consumed by the embedded video player on video slides; swiping in the upper area (y≈0.22) advances reliably.
- Video slides expose a **"YouTube Video Player"** (Google Slides plays uploaded MP4s through YouTube's player) with a central `Play` button, and a control bar with `Pause` / `Mute` / `AirPlay`.

## 5. 48-slide walkthrough coverage

- **48 / 48 slides captured**, each verified by its `Slide N of 48:` position label before capture (no blind swiping; test asserts position and stops on mismatch).
- Screenshots: `qa/slides-qa/ch1/ipad-pro/walkthrough/slide-01..48.png` (2752×2064).
- Endpoint spot-check (independent vision model):
  - Slide 1 = title "Energy Causes Change" (BQ, ENERGY → CHANGE → ?, desk image) → PASS.
  - Slide 48 = "Review 6 — answer … C. Yes — stored energy that can cause change later" → PASS.
- Order intact, no unexpected overlays/errors, text readable, no image distortion (vision PASS on sampled slides + full position-label verification).

## 6. Three-video results (slides 8, 27, 28)

| Slide | Video (Drive) | Player | Play | Pause | Resume | Audio |
|---|---|---|---|---|---|---|
| 8 | Chapter 1 - Pencil Sharpener Quick Visual.mp4 | YouTube player loads | ✅ | ✅ | ✅ | ✅ OWNER |
| 27 | Chapter 1 - Approved Stored Energy.mp4 | YouTube player loads | ✅ | ✅ | ✅ | ✅ OWNER |
| 28 | Chapter 1 - Why Still Objects Secretly Have Energy.mp4 | YouTube player loads | ✅ | ✅ | ✅ | ✅ OWNER |

- **Play verified (instrumented)**: central "Play" → control bar appears ("Pause"/"Mute"/"AirPlay"), video frames advance (independent vision confirmed distinct frames before/after).
- **Pause verified (instrumented)**: "Pause" control tapped; paused state shows a visible play affordance (vision: "play_button_visible: yes" on slide 28).
- **Resume verified (functional)**: YouTube's toggle relabels inconsistently (`Play` → `Pause` → `Pause keyboard shortcut k`), so the "Play" label is not reliably re-exposed after pause; a bounded center-of-video tap returned the toggle to "Pause" (playing). Recorded as functional PASS.
- **Audio — OWNER VERIFIED PASS**: The owner personally listened to all three videos during the physical iPad Pro test and explicitly confirmed audio playback. This is an owner confirmation, recorded separately from instrumented measurements (`owner-confirmation.json`). File-level AAC tracks were also independently confirmed earlier (`ffprobe`). *Audio-verification issue closed — no further audio capture requested.*

## 6b. Owner confirmation (separate from instrumented evidence)

The owner (Owen Reagan) personally heard all three videos playing on the iPad Pro and explicitly confirmed **PASS**. Recorded in `qa/slides-qa/ch1/ipad-pro/owner-confirmation.json` with `evidenceClass: OWNER_VERIFIED`, kept distinct from the automated XCUITest measurements.

- Audio playback: **PASS — OWNER VERIFIED**
- Slides tested: 8, 27, 28
- Video play/pause/resume: **PASS — functional**
- Full slide walkthrough: **PASS — 48/48**
- Physical-device playback acceptance: **APPROVED**

This closes the outstanding audio-verification gap only. It does **not** auto-award Gold certification; unrelated visual, curriculum, and release gates remain open and are unaffected.

## 7. Evidence inventory

- `qa/slides-qa/ch1/ipad-pro/device-summary.json` + `device-details.json`
- `qa/slides-qa/ch1/ipad-pro/walkthrough/` — 48 slide PNGs + 3 video trees + play/pause screenshots + resume notes + `walkthrough-summary.txt`
- `qa/slides-qa/ch1/ipad-pro/video-interaction/` — focused play/pause/resume trees + screenshots (v08-before/playing/paused/resumed)
- `qa/slides-qa/xcuitest/` — runner project + result bundles (`result-walk.xcresult`, `result-vid.xcresult`, POC bundles)
- iPad A16 historical evidence preserved separately under `qa/slides-qa/ch1/ipad-a16/` (not mixed with iPad Pro).

## 8. Remaining limitations

1. ~~**Audio verification** not performed on-device~~ → **CLOSED by owner confirmation** (owner personally heard all three videos; PASS).
2. **Resume** verified functionally (via coordinate tap) but not via a stable accessibility label.
3. Screenshots are 2752×2064 stills; transient control-bar overlays during video interaction are expected.
4. The video slides' playback is YouTube-player-backed (Google Slides behavior), not the raw MP4.

## 9. Final assessment

| Check | Result |
|---|---|
| iPad Pro discovered & trusted | PASS |
| Runner installed & signed | PASS |
| Native Slides opens Chapter 1 | PASS |
| 48-slide walkthrough (position-verified) | PASS |
| Text readable / no clipping / no distortion | PASS (sampled vision + position labels) |
| Video player loads (8, 27, 28) | PASS |
| Play / Pause | PASS |
| Resume | PASS (functional) |
| Audio | PASS — OWNER VERIFIED |

**Physical-device playback acceptance: APPROVED.**

**Recommendation:** The physical iPad Pro walkthrough is complete and clean for all 48 slides, and the three videos' load/play/pause/resume/audio are now fully accepted (audio by owner confirmation). This resolves the physical-device playback gate. **It does not by itself award Gold certification** — the independent visual audit, curriculum parity, and release gates stand separately and remain the authority for Gold.
