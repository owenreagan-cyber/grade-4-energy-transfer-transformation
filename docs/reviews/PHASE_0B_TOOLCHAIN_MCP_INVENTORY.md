# PHASE 0B — Toolchain / MCP / Dependency Inventory

> Discovery + capability verification only. No production artifacts modified, no installs, no auth, no commits.
> Date: 2026-10-03 · Scope: Unit 1 production system.

---

## 1. What Works

### A. Repository Toolchain Inventory

**Package managers**
- `npm` 11.19.0 — the only package manager with a lockfile. Used exclusively in `tools/`.
- `pip` (venv-only) — Python deps are installed into `.venv/` but **not pinned** (no `requirements.txt`, `pyproject.toml`, `Pipfile`, or lockfile).
- `pnpm` — NOT installed. `yarn` — NOT installed.

**Runtimes / versions**
- Node `v26.7.0` (Homebrew).
- Python `3.14.7` (`.venv`, symlinked to Homebrew `python@3.14`; a `python@3.12` formula is also present).
- No `.nvmrc`, `.node-version`, `.python-version`, or `.tool-versions` pin files anywhere.

**Relevant manifests**
- `tools/package.json` + `tools/package-lock.json` (lockfileVersion 3) — name `energy-unit-review-tools` v1.1.0; sole runtime dep `pptxgenjs ^4.0.1` (transitive: `jszip`, `image-size`, `@types/node`, `https`). This is for the **clickable review games only** (Unit 1 Phase 13Z / Unit 2 Phase 13AA), not the core curriculum pipeline.
- No `pyproject.toml` / `requirements*.txt` / `setup.py` / `Pipfile` / `environment.yml`.

**Key Python libraries in `.venv/` (project-relevant)**
- `python-pptx 1.0.2` — all slide generation.
- `python-docx 1.2.0` — guided notes, worksheets, labs, quizzes, assessments, keys, certificates.
- `Pillow 12.3.0` — raster diagram generation + visual QA.
- `lxml`, `Markdown`, `rich`, `typer`, `click`, `python-dotenv`, `requests`.
- `playwright 1.63.0` — installed but **not imported by any repo script** (latent/unused).
- `pymobiledevice3 11.19.4` — iPad/device QA capture (`ipad_qa_*.py`).
- `xlsxwriter 3.2.9` — installed; not observed in script imports (latent/unused).

**Slide-generation scripts (CURRENT)**
- `python-pptx`: `build_ch4_slides.py`, `build_ch5_slides.py`, `build_ch6_slides.py`, `build_ch7_slides.py`, `build_u2_slides.py`, `build_ch1_note_comparison_slides.py`, `embed_infographics.py`.
- `pptxgenjs` (JS): `build_u1_review_game.js`, `build_u2_review_game.js` (+ `review_game_lib.js`).

**PDF generation — NO native PDF library.** `reportlab`, `weasyprint`, `pymupdf/fitz` are all **absent**. PDF is produced by `soffice --headless --convert-to pdf` from DOCX/HTML/Markdown masters (`md_to_pdf.py`, `render_visual_qa.py`, and `__main__` blocks in the build scripts).

**Image-processing**
- `Pillow` (in-process), `rsvg-convert 2.62.3` (SVG→PNG, used by `build_lab_setup_guides.py`), plus CLI `imagemagick`/`magick` and `webp` available (not wired into scripts).

**Rendering / screenshot / preview**
- `render_visual_qa.py`: `soffice → PDF → pdftoppm → PNG` for DOCX/PPTX/PDF.
- `playwright` (unused), `ipad_qa_capture.py` / `ipad_qa_studyguides.py` / `ipad_qa_u2_capture.py` (device capture via `pymobiledevice3` + `xcrun devicectl`).

**Media-processing**
- `ffmpeg 9.0.1` (decode/trim — used in Phase 13 media reviews, not in a build script), `imagemagick`, `webp`, `rsvg-convert`.

**Existing QA scripts**
- PDF: `pdfinfo` via `qa_phase10.py`, `qa_ch1_notes_gates.py`, `qa_gn_premium.py`, `qa_gn_u2.py`.
- PPTX: `python-pptx` re-open checks (`qa_phase10.py`, `qa_ch1_notes_gates.py`).
- Visual layout / overflow: `render_visual_qa.py` (raster compare), `Pillow` pixel checks (`qa_ch1_notes_gates.py`, `qa_gn_premium.py`).
- Font sizes / floor: `audit_typography_regression.py`, `fix_font_floor.py`.
- Asset manifests: `build_final_delivery.py` (SHA-256 + CSV), `qa_phase10.py` (release PDF hash/open verification).
- Source alignment: `source-fidelity-check` skill (manual/AI review; no automated source diff tool).
- Assessment checks: `assessment-qa` skill + `qa_review_game.py` / `qa_u1_review_game.py` (JS game zip QA).

**CURRENT vs historical/obsolete**
- CURRENT: `python-pptx`, `python-docx`, `Pillow`, `soffice`+`poppler` render chain, `rsvg-convert`, `ffmpeg`, the `qa_*` and `build_gn_*` scripts, `gn_design.py` / `ch1_notes_common.py` / `ch4_common.py`.
- HISTORICAL / RETIRED: Interactive Science Notebook generators (`build_ch*_notebook.py`, `build_ch*_inb_comparison.py`, `build_ch1_note_comparison_slides.py`) — the INB-primary architecture is retired (Phase 0A.1); these scripts are vestigial. `build_u2_*` scripts are Unit 2 (adjacent unit), not Unit 1.
- UNUSED but installed: `playwright`, `xlsxwriter`, `pymobiledevice3` (device QA only, needs hardware).

### B. Homebrew / CLI Inventory

| Tool | Status | Version |
|---|---|---|
| Homebrew | present | 7.0.6 |
| ffmpeg | present | 9.0.1 |
| imagemagick | present | 7.1.2-29 |
| poppler (`pdftoppm`,`pdfinfo`) | present | 26.08.0 |
| qpdf | present | 12.4.1 |
| ghostscript (`gs`) | **missing** | — |
| exiftool | **missing** | — |
| jq | present | 1.8.2 |
| ripgrep | present | 15.2.0 |
| fd | present | 10.4.2 |
| pandoc | **missing** | — |
| libreoffice (`soffice`) | present (as `soffice`; `libreoffice` alias **missing**) | 26.2.5.2 |
| node / npm | present | 26.7.0 / 11.19.0 |
| pnpm / yarn | **missing** | — |
| python3 / pip | python3 present; global `pip` **missing** (venv `pip` 26.2.1) | 3.14.7 |
| rsvg-convert (librsvg) | present | 2.62.3 |
| webp / cairo / harfbuzz / librsvg | present | — |

**Brewfile** — none exists.

**Repo scripts that shell out to CLIs**: `soffice`, `pdftoppm`, `pdfinfo`, `rsvg-convert`, `xcrun devicectl`, `pymobiledevice3`. **All required CLIs are present.** No repo script depends on `gs`, `exiftool`, `pandoc`, `pnpm`, or `yarn`.

**Recommended smallest reproducible Brewfile** (do NOT create yet):
```ruby
# Phase 0B recommendation — smallest reproducible set actually used by repo scripts
brew "poppler"       # pdftoppm + pdfinfo (render + PDF QA)
brew "qpdf"          # PDF structural ops (available; harden/inspect)
brew "librsvg"       # rsvg-convert (SVG -> PNG diagrams)
brew "ffmpeg"        # media decode/trim (Phase 10 media staging)
brew "imagemagick"   # raster ops
brew "node"          # pptxgenjs review games
brew "python@3.14"   # venv runtime
cask "libreoffice"   # soffice headless -> PDF
# optional, not currently required: ghostscript, exiftool, pandoc, jq, ripgrep, fd
```

### C. Cursor MCP / Plugin Inventory

| Service | Connected | Relevance |
|---|---|---|
| **Canva** (`plugin-canva-canva`) | **NO** (`needsAuth`) | design creation/editing if authenticated |
| **Figma** (`plugin-figma-figma`) | **YES** (`ready`) | full design/diagram/component toolset |
| **GitHub** | **NO git-host MCP** | only `cursor-subscriptions` (`subscribe_github_ci/pr` event hooks); no repo ops |
| **Google Drive** | **NO** | not present as an MCP namespace |
| `cursor-origin` | Origin host (not GitHub) | irrelevant — repo has no remote |

No PDF-generation, image-generation, slide-generation, document-creation, file-conversion, or asset-management MCP is present beyond **Figma** (and **Canva** once authenticated).

### D. Canva Capability

- Connected: **NO** (`namespaceStatus: needsAuth`; only `mcp_auth` tool exposed).
- Create/edit/feedback/implement/bulk-create/export/brand-kit: **unverifiable until authenticated**.
- Not recommended as a dependency for Unit 1 production while unauthenticated; even if authenticated, Canva export is raster/PDF-oriented and would not supersede the editable DOCX/PPTX master pipeline.

### E. Figma Capability

- Connected: **YES** (`namespaceStatus: ready`).
- Tools confirmed: `create_new_file`, `use_figma`, `generate_figma_design`, `generate_diagram`, `get_design_context`, `get_screenshot`, `get_metadata`, `upload_assets`, `download_assets`, `get_libraries`, `search_design_system`, `get_code_connect_map`/`add_code_connect_map`, `create_shader`/`update_shader`, `create_generative_plugin`/`update_generative_plugin`, `export_video`, `get_figjam`, plus `weave_*` toolchain helpers.
- Can create a new file: YES. Can create reusable components/library: YES (`use_figma` + design-system search). Can generate diagrams: YES (`generate_diagram`). Can write editable vectors/components: YES (`use_figma`). Can work with slides: YES (Figma Slides via `use_figma`/slides URL handling). Can export assets: YES (`get_screenshot`, `download_assets`, `export_video`).
- **Limitation for PPTX/PDF production**: Figma exports PNG/SVG/PDF/Figma Slides, not editable PPTX/DOCX. It is best as a **visual-asset / diagram source**, not a replacement for `python-pptx`/`python-docx`. Figma Slides ≠ PowerPoint master.

### F. Existing PDF Pipeline

`EDITABLE MASTER (DOCX/HTML/MD) → soffice --headless --convert-to pdf → PDF → pdftoppm → PNG`
- No native PDF library (no reportlab/weasyprint/pymupdf).
- QA renders → `_review_renders/` (gitignored); releases → `production/releases/` (tracked).
- Classification: **KEEP EXISTING**.

### G. Existing PPTX Pipeline

`python-pptx build script → editable PPTX master → (render QA) soffice → PDF → pdftoppm`
- `pptxgenjs` used only for JS review games.
- Classification: **KEEP EXISTING**.

### H. Existing Media Pipeline

- `ffmpeg` (decode/trim) + `imagemagick` + `webp` + `rsvg-convert` (SVG diagrams) + `Pillow` (raster).
- Media binaries are git-ignored (`assets/supplemental/`, `production/videos/`); inventory tracked in Markdown (`SOURCE_INVENTORY.md`, `MEDIA_ASSET_MANIFEST.md`).
- Classification: **KEEP EXISTING** (staging is Phase 10, still PENDING/UNSTAGED for Unit 1).

### I. Existing QA Pipeline

- `qa_*.py` + `render_visual_qa.py` + `pdfinfo` + `pdftoppm` + `Pillow` + `audit_typography_regression.py` / `fix_font_floor.py`.
- Headless (soffice/poppler) — no visible-desktop QA. Device QA via `pymobiledevice3`/`devicectl` (hardware-gated).
- Classification: **KEEP EXISTING**.

### J. Canonical Production Path Recommendation

| Production path | Current system | Classification |
|---|---|---|
| Guided Notes source | `python-docx` (`gn_design.py` + `build_gn_*.py`) → DOCX | KEEP EXISTING |
| Guided Notes PDF | `soffice` headless | KEEP EXISTING |
| Worksheets / labs / study guides | `python-docx` (`ch4_common.py`, `build_*_worksheets.py`, `build_lab_setup_guides.py`) | KEEP EXISTING |
| Teacher Playbook | Markdown teacher maps + teacher notes per chapter; consolidated playbook = standard doc only | EXTEND EXISTING |
| PPTX generation | `python-pptx` (`build_*_slides.py`) | KEEP EXISTING |
| PPTX rendering / preview | `render_visual_qa.py` (soffice→PDF→pdftoppm) | KEEP EXISTING |
| Image assets | `Pillow` + `rsvg-convert` + (imagemagick available) | KEEP EXISTING |
| Diagrams | `Pillow ImageDraw` + SVG via `rsvg-convert` | KEEP EXISTING / EXTEND (Figma) |
| Video / media | `ffmpeg` staging (git-ignored) | KEEP EXISTING |
| Assessment generation | `python-docx` (`build_ch7_assessment.py`, `build_final_assessments.py`) | KEEP EXISTING |
| Answer keys | `python-docx` (same scripts) | KEEP EXISTING |
| Final packaging | `build_final_delivery.py` + `production/final-package/` + `final-delivery/` | KEEP EXISTING |

### K. Missing Dependencies

1. **Python deps are unpinned** — no `requirements.txt`/`pyproject.toml`/lockfile. A fresh `.venv` cannot be reproduced deterministically.
2. **No native PDF library** — acceptable today (soffice covers it), but means no programmatic PDF text/layout assertion (only `pdfinfo` + raster).
3. **`ghostscript` missing** — no PDF flatten/font-subset/render fallback beyond poppler (not currently required).
4. **`pandoc` missing** — Markdown→DOCX/PDF path not available (not currently required).
5. **`exiftool` missing** — no EXIF/metadata assertion on media (not currently required).
6. **No Brewfile** — CLI set is not reproducible.
7. **No runtime version pins** (`.nvmrc`/`.node-version`/`.python-version`/`.tool-versions`).
8. **No chart library** (`matplotlib` absent) — data/chart visuals are hand-built (PIL) today.

### L. Recommended Specialist Tool Map

| Task | Recommended tool | Rationale |
|---|---|---|
| Curriculum / source fidelity | `source-fidelity-check` skill + reader/TG inspection | authoritative-source manual/AI review; no automated source diff exists |
| Guided notes layout | `python-docx` (`gn_design.py`) | already reliable, editable-first |
| Worksheet / test layout | `python-docx` (`ch4_common.py`) | already reliable |
| Slide assembly | `python-pptx` | editable PPTX master, mirror-rule capable |
| Custom diagrams | `rsvg-convert` (SVG) + `Pillow`; **optional** Figma `generate_diagram` | SVG→PNG already wired; Figma for richer vectors |
| Premium vocabulary-card visuals | `python-pptx` shapes / `Pillow` | current system; no new tool needed |
| Chapter hero visuals | `Pillow` / `python-pptx`; **optional** Figma | current system sufficient |
| Charts / data visuals | `Pillow` (today); add `matplotlib` only if charts proliferate | avoid new dep unless needed |
| PDF generation | `soffice --headless` (LibreOffice) | canonical, reliable |
| PPTX generation | `python-pptx` (+ `pptxgenjs` for games) | canonical |
| PDF/PPTX rendering QA | `render_visual_qa.py` (soffice+pdftoppm) + `Pillow` | headless, invisible QA |
| Image editing | ImageMagick / Pillow | present and sufficient |
| Video processing | `ffmpeg` | decode/trim only; no synthesis |
| Automated QA | `qa_*.py` + `pdfinfo` + `pdftoppm` | present and sufficient |
| Independent review | reviewer subagents per `AGENT_ROLES.md` | process, not a new tool |

No new tool is recommended merely because it exists; the only *optional* additions are Figma (already connected) for richer diagrams/visuals and, later, `matplotlib` if charting grows.

### M. Phase 0C Readiness

**READY WITH CONDITIONS.** Toolchain is sufficient and consistent; the only structural gap is reproducibility (unpinned Python deps, no Brewfile, no version pins). Canva is unauthenticated (not blocking). Fixes in §3.

---

## 2. What’s Missing

- Python dependency pinning (no lockfile/manifest).
- A Brewfile (CLI reproducibility).
- Runtime version pins (`.nvmrc`/`.python-version`/`.tool-versions`).
- `ghostscript`, `pandoc`, `exiftool` (none currently required by scripts).
- Native PDF generation library (not required — soffice covers it).
- Chart/data library (`matplotlib`) — only needed if charts grow.
- A consolidated Teacher Playbook generator (standard exists; only per-chapter Markdown maps exist).
- Canva authentication (design MCP unavailable until authed).
- Any Git remote (intentional — no commit/push policy).

## 3. Fixes — specific problems + exact fixes

1. **Unpinned Python deps** → create `tools/requirements.txt` (or `pyproject.toml`) pinning `python-pptx==1.0.2`, `python-docx==1.2.0`, `Pillow==12.3.0`, `lxml`, `Markdown`, plus a `pip freeze` snapshot. *(Phase 0C — do not create now.)*
2. **No Brewfile** → create `Brewfile` with the minimal set in §1B. *(Phase 0C.)*
3. **No version pins** → add `.nvmrc` (`26`), `.python-version` (`3.14`). *(Phase 0C.)*
4. **Vestigial INB scripts** (`build_ch*_notebook.py`, `build_ch*_inb_comparison.py`, `build_ch1_note_comparison_slides.py`) → retire/move to `tools/` historical area or `docs/architecture/RETIRED_CURRICULUM_ARTIFACT_POLICY.md` disposition. *(Do not modify now.)*
5. **Unused installed deps** (`playwright`, `xlsxwriter`) → remove from the venv once `requirements.txt` is authoritative, to avoid drift. *(Phase 0C.)*

## 4. Enhancements / Suggestions / New Ideas

- Use **Figma** (already connected) as a diagram/hero-visual source for future premium visuals, exporting PNG/SVG into `assets/`, while keeping DOCX/PPTX as the editable masters.
- Consider `pandoc` (or extend `md_to_pdf.py`) only if Markdown-authored Teacher Playbook → PDF becomes a real requirement.
- Consider `matplotlib` only if data/chart visuals proliferate (currently hand-built with PIL).
- Add a `brew bundle check` and `pip check` step to the QA gate preamble for reproducibility assertions.

## 5. Edge Cases & Failure Modes

- `soffice` is the **only** LibreOffice entry point (`libreoffice` alias missing) — scripts correctly use `soffice`; do not introduce `libreoffice` calls.
- `pdftoppm`/`pdfinfo` assume poppler is on PATH; if a fresh machine lacks it, all render QA silently fails (currently caught by `render_visual_qa.py` tool check).
- `rsvg-convert` is required by `build_lab_setup_guides.py` but lives outside the venv (Homebrew `librsvg`); a Brewfile-less clone breaks lab-guide generation.
- `pymobiledevice3`/`xcrun devicectl` QA requires attached hardware + iOS device; not headless, must not run unattended on the visible desktop (QA-isolation rule).
- `ffmpeg`/media binaries are git-ignored; media staging must not be treated as a build dependency (documented policy).
- Canva in `needsAuth` state exposes only `mcp_auth` — invoking design tools will fail until authenticated; do not preemptively authenticate.

## 6. Performance Concerns

- `soffice --headless` PDF conversion + `pdftoppm` raster is CPU-heavy but one-shot per artifact; `render_visual_qa.py` already batches to `_review_renders/` (gitignored). No persistent processes.
- `pptxgenjs`/`python-pptx` builds are fast and deterministic.
- Media decode (`ffmpeg -f null`) is one-shot; no watch loops.
- No daemon/watch-mode tooling exists; keep it that way.

## 7. Readability / Maintainability

- The `tools/` directory mixes Unit 1, Unit 2, retired-INB, QA, and device scripts with no subfolder separation or `requirements.txt`; a `tools/` README + manifest would reduce ambiguity.
- `gn_design.py` / `ch1_notes_common.py` / `ch4_common.py` are the shared design-layer libraries (good); the per-chapter `build_*` scripts are thin wrappers (good).
- Common build idiom: DOCX/PPTX master → `soffice` PDF export in `__main__` — consistent.
- Version pinning + Brewfile + `requirements.txt` are the highest-leverage maintainability fixes.

---

## PHASE 0B SUMMARY

- **repo build toolchain status**: Python 3.14.7 (venv) + Node 26.7.0; `python-pptx`/`python-docx`/`Pillow` current; `pptxgenjs` for games; no native PDF lib; Python deps UNPINNED.
- **Homebrew status**: 7.0.6 installed; required CLIs (soffice, poppler, qpdf, rsvg-convert, ffmpeg, imagemagick, node, python) all present; no Brewfile.
- **missing required CLIs count**: 0 (ghostscript/exiftool/pandoc/pnpm/yarn absent but NOT required by any repo script).
- **Canva connected**: NO (`needsAuth`).
- **Figma connected**: YES (`ready`).
- **write-capability verification status**: NOT VERIFIED — verifying Figma/Canva write would require creating a throwaway artifact; STOPPED per stop conditions.
- **current PDF pipeline classification**: KEEP EXISTING (soffice→PDF→pdftoppm).
- **current PPTX pipeline classification**: KEEP EXISTING (python-pptx→PPTX→soffice render QA).
- **current QA pipeline classification**: KEEP EXISTING (qa_*.py + pdfinfo + pdftoppm + Pillow, headless).
- **recommended missing tools count**: 3 optional only (ghostscript, pandoc, exiftool — none required); 0 mandatory.
- **Phase 0C readiness**: READY WITH CONDITIONS (reproducibility pinning deferred).
- **files modified**: `docs/reviews/PHASE_0B_TOOLCHAIN_MCP_INVENTORY.md` (new).
- **git status --short**: see below.
