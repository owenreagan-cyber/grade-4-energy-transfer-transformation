# Tool and MCP Inventory

Recorded 2026-10-06 on this machine. Phase A does not add MCP servers.

No secrets are recorded here.

## MCP

| Check | Result |
|---|---|
| Project `.cursor/mcp.json` | Absent. |
| `~/.cursor/mcp.json` | Present. Top-level key `mcpServers`. Server count **0**. |
| `agent mcp list` | `No MCP servers configured (expected in .cursor/mcp.json or ~/.cursor/mcp.json)`. |
| Cursor CLI `agent --version` | `2026.10.01-e373342`. |

Figma MCP status: **NOT CONFIGURED**.

Canva status: **NOT CONFIGURED**.

`visual-art-director` and `docs/agent-workflows/TOOL_ACCESS_MATRIX.md` now say Figma and Canva are `NOT CONFIGURED`. An older sentence in those files had called Figma authenticated. That claim is withdrawn. Later integration is a separate phase. Do not treat either tool as available.

## Local tools (present)

| Tool | Path | Version observed |
|---|---|---|
| `soffice` | `/opt/homebrew/bin/soffice` | LibreOffice 26.2.5.2 |
| `pdftoppm` | `/opt/homebrew/bin/pdftoppm` | 26.08.0 |
| `pdfinfo` | `/opt/homebrew/bin/pdfinfo` | 26.08.0 |
| `qpdf` | `/opt/homebrew/bin/qpdf` | 12.4.1 |
| `rsvg-convert` | `/opt/homebrew/bin/rsvg-convert` | 2.62.3 |
| `ffmpeg` | `/opt/homebrew/bin/ffmpeg` | 9.0.1 |
| `magick` | `/opt/homebrew/bin/magick` | ImageMagick 7.1.2-29 |
| `python3.14` | `/opt/homebrew/bin/python3.14` | 3.14.7 |
| `node` | `/opt/homebrew/bin/node` | v26.7.0 |
| `agent` | `/Users/owen/.local/bin/agent` | 2026.10.01-e373342 |

## Repo Python (`.venv`)

| Package | Version |
|---|---|
| `python-pptx` | 1.0.2 |
| `python-docx` | 1.2.0 |
| `Pillow` | 12.3.0 |
| `markdown` | 3.11 |
| `lxml` | 6.1.3 |
| `jsonschema` | not installed |

The evidence schema is checked by `tools/chapter_qa/evidence.py`. This phase does not add the `jsonschema` package.

## Phase C.1 redaction

Inventories and reports record server names, classes, and environment-variable names. They do not record token values. `tools/hooks/redact.py` replaces assigned secrets, `github_pat_…` values, and `sk-…` values with `[REDACTED]` and leaves a bare name such as `FIGMA_TOKEN` in place.

Governance, role rules, and the inactive example config are in `docs/gold-standard/MCP_GOVERNANCE.md` and `docs/gold-standard/mcp.example.json`. No project `.cursor/mcp.json` is added.

## Repo tools already in use

Chapter certification scripts under `tools/qa_*.py`, release parity `tools/qa_release_parity.py`, and render support `tools/render_visual_qa.py`. The new shared contract is `tools/chapter_qa/`. It does not replace those chapter scripts.

## Agents

Existing: `curriculum-source-reviewer`, `guided-notes-specialist`, `slideshow-specialist`, `assessment-student-resource-specialist`, `visual-art-director`, `qa-certification-reviewer`.

Added in Phase A: `provenance-auditor`, `qa-adversary`, `release-judge`.

`VISUAL_QA_AUDITOR` and `PDF_OOXML_FORENSICS` are roles without a new agent. Headless `soffice`, `pdftoppm`, `pdfinfo`, and `qpdf` remain the deterministic tools for those roles.
