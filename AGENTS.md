# AGENTS.md

> Governance for Cursor/Codex/Claude/GPT agents working in this repo. Read before acting. Detailed numeric standards live in `docs/standards/`; workflows in `docs/agent-workflows/`.

## Canonical source of truth
- This repository is the **canonical source of truth** for the Grade 4 **Energy Transfer and Transformation** unit (CKSci-aligned).
- **Authoritative curriculum sources:** CKSci Student Reader and Teacher Guide (`assets/authoritative/…`). Nothing overrides them; never alter them in place.
- **Audience:** Grade 4. **Schedule:** 30-minute science blocks, M–Th core + Friday.

## Primary artifacts
- **Guided Notes** are the primary student content/reference artifact, designed **before** the matching slideshow.
- **Science Journal** is secondary: reflection, drawing, evidence, and extension.
- Slides' **Big Question / Vocabulary / Notes (BQ/V/N) anchors must mirror student notes exactly**.
- No hidden required note answers may appear on unrelated slides.
- Slides may be visually richer than notes but must remain extremely easy to follow.

## Non-negotiables
- **Premium visual quality** required; student **readability, printability, generous writing space, and grayscale quality** are mandatory.
- **Conservative-school content constraints** always apply (see `docs/standards/`).
- **Friday policy (owner decision, 2026-10-04):** Friday is not reserved for FLEX only. Friday may be used for catch-up, review, completion of previously taught work, BQ reflection/synthesis, scored quizzes/tests, makeup work, and optional FLEX/enrichment. Friday must **NOT** be the first instructional exposure to essential new core content: required chapter science concepts are taught by Thursday, and Friday may finish reflection/synthesis that depends on content already taught.
- **All scored work = raw score + percentage.**
- **Automated QA is preferred**; no "complete" claim without required validation.
- Transfer (moves) vs transformation (changes form) — allow **BOTH**; don't conflate them.
- Compare the **same object** at different speeds for the speed–energy relationship.
- Never introduce advanced vocabulary as required (kinetic, potential, gravitational potential, mechanical, radiant, compression wave, inertia).
- Never invent chapter titles (7 exact Reader titles).

## Roles
- **Cursor = canonical production integrator.**
- Reviewer agents **do not silently modify** the artifact they are reviewing.

## Source discipline
- Inspect authoritative sources before authoring. Label provenance: `SOURCE` / `ADAPTED` / `CUSTOM` / `EXTENSION`.
- Use editable-first production (PPTX/DOCX/Markdown masters; PDF = release export).

## Phase pipeline (mandatory)
`BUILD → deterministic QA → internal specialist review → visual QA → phase artifact inventory → external Grok adversarial audit → verified remediation → final QA → freeze → commit` (commit only when the user asks). Details: `docs/agent-workflows/PHASE_PIPELINE.md`.
- **No phase is considered complete until every created/modified/affected artifact is accounted for by the external audit.**
- Grok is READ-ONLY; independently verify every external finding (VERIFIED / PARTIALLY VERIFIED / NOT VERIFIED) and fix only substantiated defects.
- One authoritative pacing plan per chapter (`tools/chN_pacing.py` → `docs/chapter-0N/CHN_PACING_PLAN.md`); no competing timing systems.

## Process
- **No commit or push unless explicitly requested.** No Git remote.
- Never start watch-mode runners or duplicate servers; prefer one-shot commands.
