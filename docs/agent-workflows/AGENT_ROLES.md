# AGENT ROLES

> Division of labor across production agents. Governance only — no curriculum decisions.

## Cursor
- **Canonical production integrator.** Merges production work, owns release packaging, and records QA/manifest state.

## ChatGPT
- Planning, synthesis, curriculum/product direction, prompt design, and review.

## Codex
- Deterministic repo/build/QA specialist (headless scripts, renders, validation).

## Claude Code
- Independent architecture/content/review specialist.

## Grok
- Optional red-team or isolated specialist (adversarial/edge-case review).

## Gemini / NotebookLM
- Source-grounded research or alternate review (grounded in authoritative Reader/TG).

## Canva / Figma / image generation
- Visual production specialists (slides, diagrams, media, badges).

## Qwen (local)
- Low-cost batch classification/summarization/repetitive analysis.

## Cross-cutting rules
- Only **Cursor** merges production work.
- Reviewer agents **do not silently modify** the artifact they are reviewing (switch to fix mode explicitly).
- All agents respect root `AGENTS.md` and `docs/standards/`.
