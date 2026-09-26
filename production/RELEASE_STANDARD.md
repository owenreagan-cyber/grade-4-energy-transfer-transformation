# RELEASE STANDARD

> Governs how an artifact moves from editable master to a releasable classroom output.

## Flow
```
EDITABLE MASTER → QA RENDER → FINAL RELEASE (PDF/PPTX)
```
- Never overwrite the master during rendering.
- QA renders go to `_review_renders/` (gitignored, regenerable).
- Final releases go to `production/releases/` (tracked).

## Status vocabulary
| Status | Meaning |
|---|---|
| **DRAFT** | in-progress, not QA'd |
| **QA** | passed through applicable gates, pending acceptance |
| **ACCEPTED** | accepted after QA, ready to release |
| **RELEASED** | final classroom output published |

- No artifact may be called FINAL/READY/COMPLETE/RELEASED without passing the gates in `docs/planning/QA_GATES.md`.
- Any FAIL gate blocks progression past QA.

## Versioning
- Working drafts: use the status tag; **no** semantic-version noise.
- Final releases: `NN-chN-<name>-vX.Y.pdf`, e.g. `01-ch1-energy-causes-change-notes-v1.0.pdf`.
- Bump minor `Y` for typo/layout fixes; major `X` for content changes.

## Release checklist (before marking RELEASED)
- [ ] passed `SOURCE_VALIDATION`
- [ ] passed `CROSS_ARTIFACT_ALIGNMENT`
- [ ] passed `EDUCATIONAL_SUITABILITY`
- [ ] passed `VISUAL_LAYOUT`
- [ ] passed `TECHNICAL_QA`
- [ ] passed `CLASSROOM_SIMULATION`
- [ ] `FINAL_ACCEPTANCE_REPORT` recorded in `qa/reports/`
