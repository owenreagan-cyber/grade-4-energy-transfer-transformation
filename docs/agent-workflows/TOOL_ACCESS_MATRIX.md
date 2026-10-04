# TOOL ACCESS MATRIX

> Which tools each agent may use. Authoritative for Phase 0C onward. Agents must not expand their own tool access; changes go through the coordinator.

| Agent | Repo reading | DOCX/PPTX tooling | PDF/headless QA | Figma MCP | Image/vector tooling | Canva | Write reports (`qa/reports/`) | Edit production artifacts |
|---|---|---|---|---|---|---|---|---|
| **Cursor (coordinator)** | Full | Full | Full | On request | On request | On request | Yes | Yes — full repo integration authority |
| **Curriculum Source Reviewer** | Full | No | Read-only | No | No | No | Yes | No |
| **Guided Notes Specialist** | Full | DOCX (`python-docx`) | Render QA only | No | No | No | Yes | Yes — notes only |
| **Visual Art Director** | Full | No | Render QA only | Yes | Yes (`Pillow`, `rsvg-convert`, `ImageMagick`) | Only when authenticated/approved | Yes | Yes — visual assets only |
| **Slideshow Specialist** | Full | PPTX (`python-pptx`) | Render QA only | No | No | No | Yes | Yes — slides only |
| **Assessment & Student Resource Specialist** | Full | DOCX (`python-docx`) | Render QA only | No | No | No | Yes | Yes — assessments/keys only |
| **QA / Certification Reviewer** | Full | No | Full (headless: `soffice`, `pdftoppm`, `qpdf`, `pdfinfo`, `.venv/bin/python` scripts) | No | No | No | Yes | No — read-only unless switched to fix mode |

## Notes
- **Canonical tooling**: DOCX via `.venv/bin/python` + `python-docx`; PPTX via `.venv/bin/python` + `python-pptx`; PDF via `soffice --headless` (release export only); render QA via `pdftoppm` (see `docs/technical/TOOLCHAIN.md`).
- **Visual-design MCP** is required only for the Visual Art Director. Reviewers and content producers have no Figma/Canva requirement.
- **Canva** is gated: the Visual Art Director may use it only after authentication is established by the coordinator and the task is explicitly approved. Current state: NEEDS AUTH.
- **Figma** is authenticated and available to the Visual Art Director.
- Reviewers write findings to `qa/reports/` but never edit the artifact under review.
