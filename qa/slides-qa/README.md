# Google Slides Instructional QA Tool (reusable)

A deterministic, independent QA system for CKSci Chapter slideshows delivered
as Google Slides. It combines:

1. **Retrieval** — Google Drive MCP (`plugin-google-drive-google-drive`):
   search/read the deck, export `pdf` (render fidelity), `pptx` (video-shape +
   media detection), and `txt` (plain slide text).
2. **Structural audit** — `lib/structural.py`: slide count, per-slide text,
   video-slide detection, stable slide identity (position + content hash).
3. **Render** — `lib/render.py`: PDF → per-slide high-res PNG via `pdftoppm`.
4. **Independent visual audit** — `lib/vision.py`: `ollama qwen3-vl:30b`
   inspects each rendered slide **blind** (no builder metadata, no prior QA)
   and returns structured JSON.
5. **Curriculum parity** — `lib/curriculum.py`: deck text vs. the accepted
   baseline (`ch1/expected_ch1.json`).
6. **Physical iPad capture** — `lib/ipad_capture.py`: `xcrun devicectl device
   capture screenshot` + optional vision inspection.
7. **Defect register** — `lib/defects.py`: per-slide, categorized, with
   evidence, expected/actual, proposed repair, retest result.

## Retrieval procedure (Drive MCP, performed manually via the agent)

The Drive MCP tools are invoked by the agent (not by these scripts). Steps:

1. `get_file_metadata` on the presentation id → confirm identity/name/mime.
2. `read_file` (or `search` with `includeContent`) → plain slide text.
3. `export_file` format `pdf` → base64 → decode to `deck.pdf`.
4. `export_file` format `pptx` → base64 → decode to `deck.pptx`.
5. `export_file` format `txt` → base64 → decode to `deck.txt` (optional).

Decode base64 to disk with:
`python3 -m base64 -d < in.b64 > out.ext` (or `base64 -d`).

## Run (local analysis)

```bash
cd qa/slides-qa
python3 run.py --pptx deck.pptx --pdf deck.pdf \
    --expected ch1/expected_ch1.json --outdir ch1/run-001
```

Outputs: `results.json`, `REPORT.md`, `defect-register.json`,
`renders/slide-*.png`, `vision/vision-*.json`.

Use `--limit N` to bound the (slow) vision pass during development, and
`--skip-vision` for structure/render/curriculum-only runs.

## iPad capture

```bash
python3 lib/ipad_capture.py --device <UDID> --out shot.png --vision
```

Device UDID from `xcrun devicectl list devices` (look for the physical
`iPad (A16)` row with `Reality: physical`).

## Limitations (recorded, not hidden)

- Google Slides **internal object IDs** require the Slides API and are not
  available via the Drive export path; the stable key is `position` +
  SHA-1(content). Recorded as a limitation in reports.
- A rendered screenshot is **not** proof of video playback; a screenshot is
  **not** proof a presentation is open on the device. Statuses are reported
  separately (`DEVICE CONNECTED`, `PRESENTATION OPENED`, `SCREENSHOT
  CAPTURED`, `PLAYBACK VERIFIED`).
- The vision model is `qwen3-vl:30b` (local, independent of the builder);
  it is not Gemini, but is a suitable independent vision model per the
  directive.
