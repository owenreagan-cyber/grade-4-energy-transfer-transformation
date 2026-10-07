# Chapter 3 External Red-Team Remediation Matrix

Authoritative input: external red-team result **DO NOT PROPAGATE YET** for build
`ch3-factory-2026-10-06`. Previous Judge PASS 21/21 + hook ALLOW is **void**.

This matrix classifies every BLOCKING / HIGH finding, records verification, root
cause, factory fix, product fix, affected files/gates, and status. It is the
remediation worklist; it is **not** release evidence.

## Verification key

- `VERIFIED` — reproduced against the current tree; the defect is real.
- `PARTIAL` — reproduced in part; the claim overstates the defect or the mechanism differs.
- `NOT VERIFIED` — could not reproduce; recorded and closed with reasoning.

---

## Factory integrity blockers (Phase A)

### F-1 · BuildIdentity does not cover classroom bytes — VERIFIED

- **Category:** identity
- **Severity:** BLOCKING
- **Root cause:** `BuildIdentity.inputHashes` carries only `calendar`,
  `chapterSpec`, `productionPrompt`, `readerChapter`, `teacherGuide`. The actual
  classroom bytes (`production/premium-notes/*.docx`, `*.pdf`, `production/slides/*.pptx`,
  keys, quizzes, labs, recovery, release files) are never hashed into identity.
  `candidateHash` is the chapter-spec hash, not any classroom file.
- **Factory fix:** extend `BuildIdentity` with `candidateFiles: {relpath: sha256}`
  covering every certification-relevant inventory file; the set comes from the
  candidate inventory, not hard-coded Chapter 3 filenames. The Judge and stop hook
  recompute SHA-256 from disk and reject on any mismatch.
- **Product fix:** none directly; Chapter 3 must reseal against the new identity.
- **Affected files:** `tools/chapter_qa/identity.py`, `release_judge.py`,
  `hooks/final_release_gate.py`, `hooks/validate_evidence.py`.
- **Affected gates:** all.
- **Status:** in progress.

### F-2 · A git commit clears staleness — VERIFIED

- **Category:** staleness
- **Severity:** BLOCKING
- **Root cause:** staleness is derived from `hooks/edited_paths.git_changed_paths`
  (`git diff --name-only HEAD` + untracked). After a commit, the diff is empty, so
  the invalidation map is empty and evidence is treated fresh even though the
  classroom bytes changed relative to the sealed identity.
- **Factory fix:** evidence freshness must depend on recorded input hashes vs
  current disk bytes (via F-1 recompute), never on `git status`. A committed
  mutation must still FAIL.
- **Product fix:** none.
- **Affected files:** `release_judge.py`, `hooks/final_release_gate.py`,
  `hooks/invalidate_evidence.py`.
- **Affected gates:** all.
- **Status:** in progress (coupled to F-1).

### F-3 · Producers are tautological / caller-fed — VERIFIED

- **Category:** producer independence
- **Severity:** BLOCKING
- **Root cause:** `mandatory_producers.assess_notes/slides`, `assess_leakage`,
  `assess_fresh`, `assess_inventory`, `cross_artifact.emit_cross_evidence`, and
  `source_audit.emit_source_evidence` compare caller-supplied `expected` vs
  `observed`. `observed = expected` passes. No producer opens the classroom file
  and derives its own observations. `assess_fresh` can pass when the caller copies
  the target over the fresh export before comparison.
- **Factory fix:** each producer must open the real file(s) and derive its own
  observation; prohibit `observed = expected` and the same spec-derived object on
  both sides. Remove `hard-coded completed=true` and self-checked manifests.
- **Product fix:** reseal through the corrected producers.
- **Affected files:** `mandatory_producers.py`, `cross_artifact.py`,
  `source_audit.py`, `schedule_policy.py`, `release_set.py`, `render_completeness.py`.
- **Affected gates:** CHAPTER_SPEC, NOTES_STRUCTURE, SLIDES_STRUCTURE,
  NOTES_SLIDES_SYNC, ANSWER_LEAKAGE, ASSESSMENT_ALIGNMENT, SCHEDULE_POLICY,
  PLAYBOOK_ALIGNMENT, RENDER_COMPLETENESS, FRESH_EXPORT, RETIRED_CONTENT,
  RELEASE_EXACT_SET, RELEASE_PARITY, STATUS_AUTHORITY, INVENTORY, ADVERSARIAL_QA,
  PRIOR_FROZEN_NONREGRESSION.
- **Status:** in progress.

### F-4 · Producer provenance / untracked `tools/ch3_*.py` — VERIFIED

- **Category:** provenance
- **Severity:** BLOCKING
- **Root cause:** the Chapter 3 evidence was sealed by untracked `tools/ch3_*.py`
  scripts. Untracked code has no recorded blob/hash and cannot be trusted to produce
  release-certifying evidence.
- **Factory fix:** evidence must record `producerSourceHash` (and caller source
  hash where applicable); untracked code may never seal release evidence.
- **Product fix:** classify every `tools/ch3_*.py` (see §D) and re-seal only from
  tracked, clean producers.
- **Affected files:** `tools/chapter_qa/emit.py`, `registry.py`, `evidence.py`.
- **Affected gates:** all.
- **Status:** in progress.

### F-5 · Evidence is not tamper-evident — VERIFIED

- **Category:** evidence integrity
- **Severity:** BLOCKING
- **Root cause:** `evidence_from_dict` validates structure only; a hand edit to
  `findings=[]`, `execution.succeeded=true`, `execution.stale=false`, or
  `inputHashes` passes. No seal digest binds the payload.
- **Factory fix:** add a `seal` digest over the canonical evidence payload; the
  Judge recomputes and rejects on `SEAL_MISMATCH`. Maintain a tracked evidence
  ledger.
- **Product fix:** none.
- **Affected files:** `evidence.py`, `emit.py`, `release_judge.py`.
- **Affected gates:** all.
- **Status:** in progress.

### F-6 · Agent can self-grant authorization — VERIFIED

- **Category:** authorization
- **Severity:** BLOCKING
- **Root cause:** `protect_git.py` reads `qa/work/git-authorization.json` — a
  gitignored, agent-writable boolean file. Commit/freeze/external-approval booleans
  are self-grantable.
- **Factory fix:** authorization must come from a source outside ordinary model
  write scope; install a real pre-commit protection (`core.hooksPath`) so a
  subprocess commit cannot bypass `beforeShell` classification.
- **Product fix:** none.
- **Affected files:** `hooks/protect_git.py`, repo git config.
- **Affected gates:** none (cross-cutting).
- **Status:** in progress.

### F-7 · Lifecycle authority is not trustworthy — VERIFIED

- **Category:** lifecycle
- **Severity:** BLOCKING
- **Root cause:** lifecycle lives in gitignored `qa/work/` (`seal-summary.json`
  still says `BUILD_IN_PROGRESS`); no tracked record is bound to `buildId` and
  candidate identity. Internal certification is possible while lifecycle is
  `BUILD_IN_PROGRESS`.
- **Factory fix:** one tracked, integrity-protected lifecycle record per build,
  bound to `buildId` + candidate identity; enforce legal transitions and forbid
  internal certification from `BUILD_IN_PROGRESS`.
- **Product fix:** none.
- **Affected files:** `chapter_qa/lifecycle.py`, `hooks/final_release_gate.py`.
- **Affected gates:** none (cross-cutting).
- **Status:** in progress.

### F-8 · Fail-on-abort — VERIFIED

- **Category:** evidence lifecycle
- **Severity:** BLOCKING
- **Root cause:** no mechanism invalidates/removes a prior active PASS before a
  gate reruns; an aborted checker can leave the old PASS active.
- **Factory fix:** before a gate runs, invalidate/remove its previous active
  evidence; on abort/timeout/parser error/blocking defect, write a current FAIL;
  deduplicate evidence ids (one active record per build+gate+sub-scope).
- **Product fix:** none.
- **Affected files:** sealing orchestration, `emit.py`.
- **Affected gates:** all.
- **Status:** in progress.

### F-9 · Frozen Chapter 1/2 protection — VERIFIED

- **Category:** frozen non-regression
- **Severity:** BLOCKING
- **Root cause:** the commit gate does not verify Ch1/Ch2 against immutable
  baselines; protection relies on a later sealer, not the commit path.
- **Factory fix:** hook and commit gate verify frozen Ch1/Ch2 hashes/guard/golden
  and the combined playbook bytes directly.
- **Product fix:** none.
- **Affected files:** `hooks/protect_git.py`, `chapter_qa/lifecycle.py`.
- **Affected gates:** PRIOR_FROZEN_NONREGRESSION.
- **Status:** in progress.

### F-10 · Claim detection is too narrow — PARTIAL

- **Category:** claim detection
- **Severity:** HIGH
- **Root cause:** `final_release_gate._PHRASES` is an exact phrase list; it
  normalizes whitespace only, and terms like "ready"/"ship"/"approved" alone are
  not caught in some forms. The "why did certification fail?" negative control is
  handled by `_negated`, but the normalization is incomplete.
- **Factory fix:** normalize spaces/hyphens/case/punctuation; treat a
  chapter/build-context statement as sensitive when it combines context with
  certif*/release/ready/ship/propagat*/freez*/approv*/sign-off/final/gold/complete;
  keep positive and negative controls.
- **Product fix:** none.
- **Affected files:** `hooks/final_release_gate.py`.
- **Affected gates:** none (cross-cutting).
- **Status:** in progress.

---

## Release / status (Phase E)

### R-1 · Stale September release surfaces — VERIFIED

- **Category:** release
- **Severity:** BLOCKING
- **Root cause:** `production/final-delivery/` still carries legacy Chapter 3
  surfaces (heavy/light practice, interactive-notebook, invented class data, stale
  28-slide deck references, `03-ch3-drop-it-*` and legacy teacher maps).
- **Fix:** one reviewed propagation change after recertification; build
  `production/releases/chapter-03/` with only the certified set + `RELEASE_MANIFEST.json`.
- **Status:** not started (blocked on recertification).

### R-2 · STATUS_AUTHORITY / RELEASE parity self-sourced — VERIFIED

- **Category:** release/status
- **Severity:** BLOCKING
- **Root cause:** `RELEASE_EXACT_SET`/`RELEASE_PARITY`/`STATUS_AUTHORITY` can
  inspect a temporary folder generated from the same source hashes, and status
  surfaces are not scanned exhaustively.
- **Fix:** inspect the actual tracked release folder; scan every tracked status surface.
- **Status:** not started.

---

## Product defects (Phase D)

### P-1 · Missing Reader p.15 steeper-ramp fact — VERIFIED

- **Category:** curriculum completeness
- **Severity:** HIGH
- **Root cause:** Reader p.15 ("objects rolling down a steeper ramp pick up more
  speed") and TG Lesson 5 "Know the Science" are not explicitly taught; N2 uses
  circular inference ("infer the speed relationship from that change") and cites a
  false source (Reader pp. 13–14 instead of TG Lesson 4 / AP 4.1).
- **Fix:** teach the source fact; rewrite N2 (§19); correct citations; add to notes,
  key, slides, Playbook region.
- **Status:** not started.

### P-2 · N2 wording + citation — VERIFIED

- **Category:** notes/slides sync + citation
- **Severity:** HIGH
- **Fix:** rewrite N2 to name ramp height (cm) and cup movement (cm), what is
  measured vs not measured, keep "We do not measure a speed number", cite TG Lesson
  4 / Ramp It Up AP 4.1.
- **Status:** not started.

### P-3 · BQ_NOW / RECOVER chip wrap — VERIFIED

- **Category:** visual
- **Severity:** MEDIUM
- **Root cause:** the anchor chip is too narrow; `BQ_NOW` renders as `BQ_NO`/`W`,
  `RECOVER` as `RECOVE`/`R`. The v1.2 mid-word-split detector keeps a split only
  when a hyphen is present, so this was not flagged.
- **Fix:** widen chips / use student-friendly labels (`BQ NOW`, `RECOVER`).
- **Status:** not started.

### P-4 · Prompt vagueness ("infer", "that change") — VERIFIED

- **Category:** student prompt clarity
- **Severity:** HIGH
- **Fix:** new `STUDENT_PROMPT_CLARITY` gate + `GRADE4_STUDENT_PROMPT_STANDARD.md`;
  rewrite practice/quiz/lab prompts.
- **Status:** not started.

---

## Notes

- "24 of 26 fresh Chapter 3 mutations finished green" — the exact 26 M01–M26
  semantic classes are recreated independently in §36/§35; a mutation finishing
  green is an escape. `bad green = 0` is the acceptance bar, not "most caught".
- Nothing in this matrix overrides the acceptance authority of the external
  red-team result. The Chapter 3 internal certification claim remains **VOID**
  until the factory is repaired and the product is rebuilt and recertified.
