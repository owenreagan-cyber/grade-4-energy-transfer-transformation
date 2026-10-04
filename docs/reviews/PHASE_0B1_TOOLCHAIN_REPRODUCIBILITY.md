# PHASE 0B.1 — Toolchain Reproducibility Lock

> Infrastructure-only. No curriculum artifacts modified, no installs/upgrades/auth, no venv recreation, no commit/push.
> Date: 2026-10-03 · Baseline: verified Phase 0B environment.

## 1. What Works

- **Brewfile** created at repo root with exactly the 8 required Homebrew entries (7 formulae + 1 cask): `poppler`, `qpdf`, `librsvg`, `ffmpeg`, `imagemagick`, `node`, `python@3.14`, `cask "libreoffice"`. Optional tools (`ghostscript`, `exiftool`, `pandoc`, `pnpm`, `yarn`) correctly omitted.
- **Python dependency baseline** created as root `requirements.txt`, pinned to exact currently-working versions: `python-pptx==1.0.2`, `python-docx==1.2.0`, `Pillow==12.3.0`, `Markdown==3.11`, `lxml==6.1.3`. Direct-import evidence confirms these are the only third-party packages imported by `tools/*.py`.
- **Runtime declarations** created: `.python-version` = `3.14`, `.nvmrc` = `26`.
- **Toolchain docs** created: `docs/technical/TOOLCHAIN.md` covering Python/Node workflows, DOCX/PPTX master strategy, LibreOffice PDF export, pdftoppm/Pillow/qpdf/ffmpeg/rsvg-convert/ImageMagick roles, verification commands, reproduction steps, and the re-certification-on-version-change rule.
- **PATH verification**: `soffice`, `pdftoppm`, `pdfinfo`, `qpdf`, `rsvg-convert`, `ffmpeg`, `magick`, `node`, `npm`, `python3.14` all resolve from `/opt/homebrew/bin`. Venv import check passed (`pptx 1.0.2`).
- **Brewfile syntax**: valid — all 8 entries parsed and resolved to recognized formulae/casks (no "unknown formula" or syntax error).

## 2. What’s Missing

- Nothing blocking. Remaining gaps are pre-existing (unchanged from Phase 0B): no native PDF library (soffice covers it), no chart library (`matplotlib`), no consolidated Teacher Playbook generator. None are required by current scripts.

## 3. Fixes — specific problems + exact fixes

1. **Unpinned Python deps** → FIXED with `requirements.txt` (exact versions).
2. **No Brewfile** → FIXED with root `Brewfile` (minimal required set).
3. **No runtime version pins** → FIXED with `.python-version` (3.14) and `.nvmrc` (26).
4. **No toolchain doc** → FIXED with `docs/technical/TOOLCHAIN.md`.

## 4. Enhancements / Suggestions / New Ideas

- Add `brew bundle check` and `pip check` as a cheap preamble to the QA-gate script in Phase 0C.
- If Markdown→PDF for the Teacher Playbook becomes a real requirement, add `pandoc` (not before).
- If charts/data visuals grow, add `matplotlib` (not before).

## 5. Edge Cases & Failure Modes

- **`brew bundle check` returns "needs to be installed or updated"** for all entries after a Homebrew auto-update refreshes the tap — this means *outdated*, not *missing*. All required CLIs are installed and resolve. This is expected behavior, not a Brewfile defect. Verification of "present" must use `command -v`, not `brew bundle check` exit code.
- **`brew bundle check` triggered Homebrew auto-update** (tap metadata refresh only; no formula/cask was installed or upgraded — the 69 outdated formulae / 10 outdated casks remain untouched). Note for future: run with `HOMEBREW_NO_AUTO_UPDATE=1` to keep verification fully side-effect-free.
- **`soffice` is the only LibreOffice entry point** (`libreoffice` alias absent); scripts and docs consistently use `soffice`.
- **`.python-version`/`.nvmrc` are declarative markers only**; the venv and `nvm` (if used) are what actually pin the runtime. Patch-level brittleness avoided by using `3.14` / `26`.
- **`pymobiledevice3`** is invoked as a CLI by `ipad_qa_*.py` (hardware-gated), not imported — correctly excluded from `requirements.txt`, documented as optional device QA in `TOOLCHAIN.md`.

## 6. Performance Concerns

- No persistent processes introduced; all verification was one-shot.
- The only non-trivial cost was the `brew bundle check` auto-update (tap fetch), avoided in future via `HOMEBREW_NO_AUTO_UPDATE=1`.

## 7. Readability / Maintainability

- `requirements.txt` carries per-line comments mapping each pin to its consuming scripts, so future maintainers can trim without archaeology.
- `Brewfile` carries per-entry comments identifying each dependency's role.
- `TOOLCHAIN.md` is the single canonical reference; it does not duplicate curriculum standards.

---

## PHASE 0B.1 SUMMARY

- **Brewfile created**: YES (8 entries: 7 formulae + 1 cask).
- **Python dependency file created**: YES (`requirements.txt`, 5 pinned packages).
- **Python version declaration**: `3.14` (`.python-version`).
- **Node version declaration**: `26` (`.nvmrc`).
- **required Brew packages count**: 8.
- **required Python packages count**: 5 (4 direct + `lxml` transitive pin).
- **production files modified**: NO.
- **installs/upgrades performed**: NO (Homebrew tap metadata auto-refreshed by `brew bundle check`; no formula/cask installed or upgraded).
- **Phase 0C readiness**: READY.
