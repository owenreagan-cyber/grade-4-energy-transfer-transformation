# Chapter 1 — Google Slides Instructional QA Report

**Target:** https://docs.google.com/presentation/d/1txs8WOyV_Ndi6E9Z6-mUlNsvw5ZDDeXW6FZv_OVRHPI/edit
**Deck:** "Copy of 01-ch1-energy-causes-change-premium-hybrid-v6-embedded-media copy" (owner `oreagan81@gmail.com`)
**Date:** 2026-10-10 · **Method:** independent vision model (`ollama qwen3-vl:30b`) + deterministic text parity + `xcrun devicectl` physical-device capture

---

## 1. Repository and source discovery

- Canonical Chapter 1 deck: **45 slides** — `production/slides/01-ch1-energy-causes-change-slides.{pptx,pdf}` (FROZEN v1.1 contract).
- Canonical contract docs: `docs/chapter-01/CH1_SLIDESHOW_HANDOFF.md` + `CH1_SLIDESHOW_MANIFEST.md` (BQ/V/N anchors, slide map, review answers, pacing).
- Media library: `docs/planning/MEDIA_ASSET_MANIFEST.md` (8 Ch.1 videos, SHA-256 + resolution recorded; videos are *SUPPLEMENTAL/GENERATED*, not authoritative CKSci).
- The live deck is a **16.6 MB** Google Slides file (videos embedded) derived from the `ch1-premium-hybrid-v6-embedded-media` candidate. It **exceeds Google's 10 MB export cap**, so `pptx` export fails (`exportSizeLimitExceeded`); PDF + text exports succeeded.

## 2. 48-slide structural audit

| Check | Expected | Actual | Status |
|---|---|---|---|
| Total slides | 48 | **48** (PDF = 48 pages) | **PASS** |
| Instructional slides | 45 | **45** | **PASS** |
| Video slides | 3 | **3** (positions **8, 27, 28**) | **PASS** |
| Canonical content parity | 45/45 | **45/45 match, 0 content mismatches** (after ligature/order normalization) | **PASS** |

- Video slide placement matches the expected baseline exactly:
  - **Slide 8** — "WATCH & OBSERVE — Pencil Sharpening" (after slide-7 prediction, before "What changed?").
  - **Slide 27** — "WATCH & THINK — Stored Energy" (after STORED→RELEASE→CHANGE model).
  - **Slide 28** — "WATCH & THINK — Still Objects Can Have Energy" (after stored-energy explanation, before N3 writing).
- The prediction (slide 7) precedes the sharpening demonstration/video; no premature answer reveal.

## 3. 48-slide independent visual audit (blind vision model)

Raw verdicts: **31 PASS / 14 WARN / 3 FAIL**. After sequence-aware triage:

| Disposition | Count |
|---|---|
| Real defects | **0** |
| Low observations | 13 |
| False positives | 19 |

- **No** text clipping, overflow, element overlap, image distortion, or incorrect science was found on any slide.
- The WARN/FAIL verdicts are explained by the blind model's lack of instructional-sequence context (documented limitation):
  - **answer_leak (17)** on reveal/teach/demo/answer slides — these slides *intentionally* show answers.
  - **label_badge "D"** — the section-code badge system (D=Demo) is intentional.
  - **science_error** on `ENERGY → CHANGE → EVIDENCE` — that is the canonical, required N1 model.
- Low observations (non-blocking): small **chrome** text (section codes, prompts, page refs, sample text) at the documented `≥12 pt` floor (12 slides), and a minor title-vs-body alignment note on slide 28.
- Full per-slide table: `slide-table.md`.

## 4. Curriculum + Guided Notes parity

**21/21 PASS** (deterministic, against slide-visible text):

- Big Question exact wording present.
- Vocabulary: `energy` / `change` / `stored energy` with exact definitions; blanks `change`, `different`, `later`, `evidence`, `position` all present.
- Model chains `ENERGY → CHANGE → EVIDENCE` and `STORED ENERGY → RELEASE → CHANGE` present.
- Five forms (motion · sound · light · heat · electrical energy) present.
- Review answer letters correct: **C · A · D · B · A · C** (each answer slide states the correct response).
- **Zero** banned vocabulary (kinetic/potential/mechanical/radiant/compression-wave/inertia); **zero** occurrences of "proof" in slide-visible text.
- Battery wording on Review 6 = "A battery stores energy. It can cause a change later." (no "released") — matches L5.

## 5. Three-video content and playback audit

| Slide | Video (Drive) | Drive ID | Duration | Resolution | Audio | Verdict |
|---|---|---|---|---|---|---|
| 8 | Chapter 1 - Pencil Sharpener Quick Visual.mp4 | `1nYbGi3UHCi6m6L1s-8TrU4w8lUEx9fcI` | 8 s | 1280×720 (landscape) | AAC | on-topic, PASS |
| 27 | Chapter 1 - Approved Stored Energy.mp4 | `1SspboYGYU93hPahlKkNXz2lHYLeMGzNU` | 4:37 | 1280×720 (landscape) | AAC | on-topic, PASS |
| 28 | Chapter 1 - Why Still Objects Secretly Have Energy.mp4 | `1Jnud-4trYJPfetpEcsQz3SgmNSb0hAt2` | 1:16 | 720×1280 (**portrait**) | AAC | on-topic, PASS |

- **Identity verified**: `Stored_Energy.mp4` and `Why_Still_Objects_Secretly_Have_Energy.mp4` match the manifest's recorded SHA-256 **exactly** (local copies `38381321…` / `915d7389…`). The pencil-sharpener video is **new** (not in `MEDIA_ASSET_MANIFEST.md`).
- **Content verified** (frame inspection): pencil sharpener on a desk; "Can objects have energy when completely still?"; stretched rubber band — all on-topic, age-appropriate, Grade 4 scope. ("Gemini Notebook" watermark confirms generated/supplemental media.)
- **Aspect ratio**: landscape videos presented landscape; the portrait video (slide 28) presented portrait — no stretching.
- **No media overlap** with instructional text; **no premature answer reveal**.
- **Playback (pause/resume) NOT VERIFIED** — no physical-device touch injection is available (see §6/§9).

## 6. Physical iPad A16 execution evidence

Device: **iPad (A16)** · `iPad15,7` · UDID `00008120-001E54313E380032` · iPadOS **27.0.1** · Developer Mode **Enabled** · serial `LKX3PKVG3R`.

| Status | Result | Evidence |
|---|---|---|
| DEVICE CONNECTED | **PASS** | `devicectl device info details` (physical, paired, wired) |
| PRESENTATION OPENED | **PASS** | `process openURL …/present` → slide 1 "Energy Causes Change" rendered; vision PASS (readable, unclipped, no distortion) |
| SCREENSHOT CAPTURED | **PASS** | 6 PNGs @ 1640×2360 (`qa/slides-qa/ch1/ipad/`) |
| PLAYBACK VERIFIED | **NOT VERIFIED** | no touch injection; video slides not reachable via `devicectl` |

- Route used: **Safari** (no Google Slides/Drive app installed on the device; fallback route, per directive). The deck is shared `anyoneWithLink` (writer), so the school account (`owen.reagan@thalesacademy.org`) can open the link.
- Only **slide 1** was rendered on-device (no navigation tooling); full-slide device walkthrough and video playback are not automatable with `devicectl` (no HID tap/scroll subcommand) and `idb`/`tidevice` are not installed.

## 7. Screenshots and defect register

- iPad screenshots: `qa/slides-qa/ch1/ipad/{00,01,02,03,04,05,06}-*.png`.
- Rendered slides: `qa/slides-qa/ch1/renders/slide-01..48.png` (150 DPI).
- Vision per-slide JSON: `qa/slides-qa/ch1/run-live/vision/vision-*.json`.
- Defect register: `qa/slides-qa/ch1/run-live/defect-register.json` (raw) + `qa/slides-qa/ch1/triaged_defects.json` (triaged).

**Triaged result: 0 real defects, 13 low observations, 19 false positives.**

## 8. Repairs and regression results

**No candidate repair presentation is required.** There are no source-grounded blocking defects. The only documentation gap (new pencil-sharpener video not recorded in `MEDIA_ASSET_MANIFEST.md`) is a manifest update, not a slide edit, and is logged as a low-priority follow-up. Per the directive ("preserve all original instructional content unless a source-grounded defect requires a documented correction"), no changes were made to the accepted baseline.

## 9. Remaining limitations

1. ~~**Video playback (pause/resume/audio) not verified**~~ → **RESOLVED** by the iPad Pro XCUITest run + owner audio confirmation (see `ipad-pro/IPAD_PRO_QA_REPORT.md` and `ipad-pro/owner-confirmation.json`).
2. ~~**Physical-device slide-through not performed**~~ → **RESOLVED** (48/48 position-verified walkthrough on the iPad Pro).
3. **PDF render shows video slides as placeholders** (Google PDF export does not embed video thumbnails); video slides were verified via source files + frame extraction instead.
4. **Google Slides internal object IDs** unavailable (no Slides API access); slide identity uses position + content.
5. **Vision model is `qwen3-vl:30b`** (local), not Gemini; it is a suitable independent vision model but is not the named model.
6. `pptx` export blocked by Google's 10 MB export cap (deck is 16.6 MB).
7. **Resume** verified functionally (coordinate tap) but not via a stable accessibility label (YouTube player label quirk).

## 10. Final assessment

| Dimension | Result |
|---|---|
| Structure (48 / 45 + 3) | **PASS** |
| Curriculum + Guided Notes parity | **PASS** (21/21) |
| Canonical content parity | **PASS** (45/45) |
| Independent visual audit | **PASS** (0 real defects) |
| Video identity + content + aspect | **PASS** |
| Video playback (device) | **PASS** — play/pause/resume functional |
| Video audio (device) | **PASS — OWNER VERIFIED** |
| Physical-device full slide-through | **PASS** (48/48) |
| Physical-device playback acceptance | **APPROVED** |

**Overall: PASS for content, structure, visual, curriculum, and physical-device playback.** The two prior NOT-VERIFIED gaps (video playback and full device slide-through) are now closed — playback by the iPad Pro XCUITest run, and audio by owner confirmation.

**Readiness recommendation:** The deck is instructionally sound, visually clean, and now physically validated on the iPad Pro (48/48 slides + three videos, audio owner-confirmed). This resolves the physical-device evidence gaps. **Gold certification is still not auto-awarded** — it remains subject to the full release gate set (independent visual audit, curriculum parity, release parity), which stand separately.
