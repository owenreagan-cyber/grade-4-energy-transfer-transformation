# TOOLCHAIN

> Reproducibility baseline for the Grade 4 Energy unit build system. Locked in Phase 0B.1.
> Companion: root `Brewfile`, `requirements.txt`, `.python-version`, `.nvmrc`.

## Runtimes (known-good)

| Runtime | Version | Declaration |
|---|---|---|
| Python | 3.14.7 | `.python-version` = `3.14` |
| Node | 26.7.0 | `.nvmrc` = `26` |

Version declarations use **major.minor** (Python) and **major** (Node) to avoid patch-level brittleness across machines. Supported ranges: Python `>=3.14,<3.15`; Node `>=26,<27`. The pinned patch levels (3.14.7 / 26.7.0) are the currently-certified builds.

## Canonical Python workflow

```sh
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

- All production/QA scripts live in `tools/` and run against `.venv`.
- Invoke as `.venv/bin/python tools/<script>.py` (scripts import shared helpers from the same directory; add `tools/` to `sys.path` if run from elsewhere).
- Do **not** rely on the global `python3`/`pip` (global `pip` is not installed; the venv is authoritative).

## Canonical Node workflow

```sh
cd tools && npm install && npm run build:review-game
```

- Used only for the clickable review games (`pptxgenjs`). No other Node tooling.

## DOCX / PPTX master strategy

- **Editable-first**: every classroom artifact has a DOCX (notes/worksheets/keys) or PPTX (slides) editable master.
- PDF is a **release export**, never the only editable source.
- `python-docx` builds DOCX masters; `python-pptx` builds PPTX masters.
- Masters are tracked; intermediate QA renders go to `_review_renders/` (gitignored); final releases go to `production/releases/` (tracked).

## LibreOffice headless PDF export

```sh
soffice --headless --convert-to pdf --outdir <out> <file.docx|file.pptx|file.html>
```

- Canonical PDF generator (no native PDF library is used).
- `soffice` (not `libreoffice`) is the correct entry point on this machine.

## pdftoppm render QA

```sh
pdftoppm -png -r <dpi> <file.pdf> <out_prefix>   # PDF -> PNG for visual inspection
```

- Backbone of `tools/render_visual_qa.py` (DOCX/PPTX/PDF -> PDF -> PNG) and the overflow/layout gates.

## Pillow image inspection

- Used in-process for raster diagram generation (`Image`, `ImageDraw`, `ImageFont`) and pixel-level visual QA (e.g. `qa_ch1_notes_gates.py`, `qa_gn_premium.py`).

## qpdf role

- Structural PDF ops (recompress / repair / inspect) for release-PDF hardening. Present and available; not a build dependency of any generator.

## ffmpeg role

- Media decode + trim only (`ffmpeg -f null -` decode integrity checks; `-ss`/`-to` cuts). No media synthesis.

## rsvg-convert role

- SVG -> PNG rasterization for diagram assets (`build_lab_setup_guides.py`) and the Unit 1 visual system (`tools/build_visual_system.py`).
- **Certified version (Phase 1.1 freeze):** `rsvg-convert version 2.62.3` (Homebrew `librsvg`; cairo 1.18.4, pango 1.58.2, harfbuzz 14.3.1, fontconfig 2.18.3).
- **Reproducibility policy:** the root `Brewfile` declares `librsvg` (the required package). Exact Homebrew formula pinning is not used — the repo does not support a reliable pinning mechanism. Version changes are detected by `rsvg-convert --version` and **require visual re-certification** of the affected PNG renders (re-run `tools/qa_visual_system.py`, which exercises the `render_integrity` gate, and eyeball the grayscale proof) before any asset is treated as release-ready.

## ImageMagick role

- General raster image ops (resize, normalize, grayscale preview) for asset editing and visual QA. Available; not wired into any generator.

## Verify installed dependencies

```sh
brew bundle check                    # Brewfile satisfied (does not install)
command -v soffice pdftoppm pdfinfo qpdf rsvg-convert ffmpeg magick node python3.14
python3.14 --version && node --version
.venv/bin/python -c "import pptx, docx, PIL, markdown, lxml; print('py deps OK')"
```

## Reproduce on another Mac

```sh
brew bundle                            # installs the minimal Brewfile set
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd tools && npm install                # optional: review games only
```

## Certification rules

- **No upgrade during a certified build.** A rendering-certified build is pinned to the versions above.
- **Version changes require re-certification of rendering output** (re-run `render_visual_qa.py` and the typography regression audit against a known-good reference) before any artifact is treated as release-ready.

## Optional device QA (hardware-gated, not core)

- `ipad_qa_*.py` shell out to `.venv/bin/pymobiledevice3` and `xcrun devicectl` (attached iPad only). Not part of the headless pipeline; do not run unattended on the visible desktop.
