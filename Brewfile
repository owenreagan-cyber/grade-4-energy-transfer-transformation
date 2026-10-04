# Phase 0B.1 — minimal reproducible Homebrew set (verified against Phase 0B).
# Only packages actually required by repository workflows. Do not add optional tools.

# PDF rendering + inspection (pdftoppm, pdfinfo) — render QA + release-PDF open checks
brew "poppler"

# PDF structural ops (recompress / repair / inspect) — release PDF hardening
brew "qpdf"

# SVG -> PNG rasterizer (rsvg-convert) — diagram asset generation
brew "librsvg"

# Media decode + trim — Phase 10 media staging and media QA
brew "ffmpeg"

# Raster image ops — asset editing + visual QA
brew "imagemagick"

# Node runtime — pptxgenjs review-game builds (tools/package.json)
brew "node"

# Python 3.14 runtime — the project virtualenv interpreter (.venv)
brew "python@3.14"

# LibreOffice headless (soffice) — DOCX / PPTX / Markdown -> PDF export
cask "libreoffice"
