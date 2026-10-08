# iPad Artifact QA Harness — Architecture

> Phase 1. QA infrastructure only. Does not modify Chapter 1/2/3 classroom content.

## Purpose

Inspect the **actual generated PDFs** in a native iPad viewing environment (PDFKit),
so visual QA is based on what students and teachers really see — not only DOCX/PPTX
geometry metadata.

Permanent rule:

> NATIVE VIEWER SCREENSHOT > generator geometry prediction

## Baseline (captured at build time)

- HEAD: `649a908a1c3ce8daa5284aff39fded15bde11b0e`
- Branch: `main`
- Frozen gate: `FROZEN_BYTES ALLOW` (42 files, 0 mismatches)
- Toolchain: Xcode 27.0 (27A266a), Swift 6.4, iOS 26.5 + 27.0 runtimes
- Render toolchain: LibreOffice 26.8.0.3 (`soffice`), `pdfinfo` 26.10.0
- Project generator: XcodeGen 2.46.0

## Existing reusable components (found in repo)

| Component | Path | Reuse |
|-----------|------|-------|
| Headless DOCX/PPTX→PDF renderer | `tools/render_chapter_artifacts.py` | Reused for **fresh PDF export only** (`soffice --headless`). NOT used for the primary view. |
| Output-directory guard | `tools/chapter_qa/workspace.py` (`assert_output_allowed`) | Reused to keep QA output out of `production/`, `curriculum/`, `assets/authoritative/`. |
| Frozen gate | `tools/chapter_qa/frozen_gate.py` | Re-run to prove 42 frozen bytes unchanged. |
| Chapter 3 spec | `docs/chapter-03/CH3_CHAPTER_SPEC.json` | Source of truth for expected pages (notes 3, slides 41), anchors, artifact inventory. |

**No existing Xcode project, iPad/macOS QA harness, PDFKit viewer, QuickLook
harness, XCUITest utility, or Simulator screenshot tool exists in the repo.**
This harness is new infrastructure.

## New files required

```
qa/ipad-artifact-qa/
├── project.yml                          # XcodeGen spec
├── ScienceArtifactQA/                   # iOS app target (PDFKit viewer)
│   ├── ScienceArtifactQAApp.swift
│   ├── LaunchConfig.swift
│   ├── PDFViewer.swift                  # UIViewRepresentable over PDFView
│   └── ContentView.swift
├── ScienceArtifactQAUITests/            # XCUITest target (the walk)
│   ├── ArtifactWalkTests.swift
│   └── RegressionTests.swift
└── manifests/
    └── ch3-current.json                 # Chapter 3 pilot manifest

tools/ipad_qa_driver.py                  # orchestrates render → manifest → test → postprocess
docs/qa/IPAD_ARTIFACT_QA_ARCHITECTURE.md # this file
```

Output (all under isolated `qa/temp/ipad-artifact-qa/`):

```
qa/temp/ipad-artifact-qa/
├── ch3/                                 # TEMP_FRESH_RENDER PDFs (never overwrites production)
└── <runId>/
    ├── screenshots/<name>.png           # deterministic filenames
    ├── manifest.json                    # merged per-screenshot metadata
    └── blind-review/                    # clean review bundle
```

## Simulator target

Primary: **iPad (A16)** — exact simulator match to the user's physical classroom device.

- iPad (A16), iOS 27.0 runtime (UDID `9D00E3DB-8157-4E43-8749-EE63EF18BD43`)
- Fallback: iPad (A16) 26.5 (UDID `50D5132F-BAF2-461A-BDC3-78BCB89FFB4C`)
- Viewport (logical @2x): 820 × 1180 pt → 1640 × 2360 px portrait; 1180 × 820 pt landscape

Profiles (Phase 1, deliberately small matrix):

1. **PRIMARY** — portrait, `FIT_PAGE` (worksheets / notes / labs / quizzes / keys)
2. **SECONDARY** — landscape, `FIT_PAGE` (slide PDFs)
3. Optional later: smaller iPad viewport stress test — deferred.

## Supported artifact formats

Phase 1 primary path: **PPTX/DOCX → fresh PDF export → PDFKit → iPad screenshots**.

`artifactType` vocabulary (manifest schema):

`GUIDED_NOTES`, `GUIDED_NOTES_KEY`, `WORKSHEET`, `LAB`, `PRACTICE`, `QUIZ`,
`QUIZ_KEY`, `RECOVERY`, `FLEX`, `SLIDE_PDF`.

## Screenshot output path

`qa/temp/ipad-artifact-qa/<runId>/screenshots/<slug>__<device>__<orientation>__<viewmode>__<p|s><nnn>.png`

## Metadata schema (per screenshot)

```json
{
  "artifactId": "ch3-guided-notes",
  "artifactSHA256": "…",
  "pdfPage": 1,
  "deviceModel": "iPad (A16)",
  "osVersion": "27.0",
  "viewportPixels": {"width": 1640, "height": 2360},
  "orientation": "portrait",
  "viewMode": "fit-page",
  "zoomScale": 0.0,
  "screenshotSHA256": "…",
  "screenshotPath": "…",
  "runId": "…",
  "buildId": "…"
}
```

## Future PPTX strategy (Phase 2, do not block Phase 1)

Phase 1 certifies slides as `PPTX → PDF → PDFKit → screenshots`.

Phase 2 (deferred) investigates **Quick Look preview of the actual PPTX**:
- whether Simulator supports useful PPTX Quick Look
- whether rendering is deterministic
- whether it differs materially from the PDF export

If reliable → add as a secondary path. PowerPoint/Keynote automation is out of scope.

## Physical iPad A16 (secondary)

Same app/test targets the USB-connected iPad A16 via `-destination
platform=iOS,name=<device>`. Documented in `PHYSICAL_IPAD.md`. Not auto-run.

## Phase 1.1 — Performance modes + incremental capture

QA infrastructure only; no classroom content changed. Adds three capture modes
over the Phase 1 driver (`tools/ipad_qa_driver.py`):

| Mode | Command | Behavior | Evidence class |
|------|---------|----------|----------------|
| preview | `--mode preview --artifact <id> [--pages 1,2] [--slides 12,28]` | capture the selected artifact/page(s) only; default first page | `preview` |
| changed-only | `--mode changed-only` | reuse unchanged artifacts from the run-independent cache; capture only changed artifacts | `changed-only` |
| full | `--mode full` | every artifact / page / slide; no caching | `certification` |

### Capture efficiency
- The walk launches the app **once per artifact** and navigates pages through the
  app's own Prev/Next buttons, gating every capture on the exact `Page N of M`
  indicator (determinism preserved; a missed tap can never silently capture the
  wrong page). Phase 1 launched once per page.
- `launchCount`, `artifactLoads`, `captureCount` are recorded to
  `<runId>/harness-stats.json` and surfaced in `capture-summary.json`.

### Screenshot cache
- Run-independent cache: `qa/temp/ipad-artifact-qa/cache.json` (+ `cache-shots/`).
- Key = `SHA-256(artifactId, artifactSHA256, deviceSlug, osVersion, orientation, viewMode, pageCount)`.
- A changed artifact hash, device, OS, orientation, or view mode invalidates only
  that artifact's entry. Partial (preview) captures are never cached.
- `seed-cache --from <prior manifest.json>` bootstraps the cache from a prior run.

### Differential reporting
- `<runId>/capture-summary.json` records `cached` / `captured` / `failed` per run.

### Blind review integrity
- Blind review bundles are generated **only** for evidence class `certification`
  (`--mode full`). `preview` and `changed-only` captures are a distinct evidence
  class and are never packaged as blind-review evidence.
