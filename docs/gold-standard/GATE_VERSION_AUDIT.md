# Gate Version Audit

Phase C.1. A version changes only when evidence accepted under the old contract could be reused incorrectly after Phases B and C. A refactor that does not change PASS/FAIL is not a bump. `evaluate()` already rejects a record whose `gateVersion` differs from the definition (`GATE_VERSION_MISMATCH`).

## Bumped to 1.1

| Gate | What changed | Why a 1.0 PASS cannot be reused |
|---|---|---|
| SOURCE_AUTHORITY | Derivation is normalized equality. Exclusion-only claims fail. Approved derivation needs a distinct `approvalId`. | A substring match or an exclusion-only note could have passed. |
| CURRICULUM_CORRECTNESS | Same source-audit contract. | Same reuse risk as source authority. |
| NOTES_SLIDES_SYNC | Required dimensions are compared. The same `contentHash` on both sides fails. | A sync record could pass while a dimension or the shared hash was unchecked. |
| ASSESSMENT_ALIGNMENT | Answer text is not punctuation-stripped into a pass. Instructional text is compared. | A punctuation-only match could have passed. |
| PLAYBOOK_ALIGNMENT | Cross-artifact comparison now fails when the compared playbook fields differ. | A presence-only pass could be reused. |
| RENDER_COMPLETENESS | The render hash must equal the candidate hash. Render files must exist and be unique. Navigation-only sheets and contact sheets fail. | An unbound or duplicate render could have passed. |
| RENDERED_VISUAL_QA | Empty boxes fail. Contrast, bottom margin, mid-word splits, and a real 600 DPI crop are checked. Contact sheets and source XML cannot pass. | A metadata-only visual pass could be reused. |
| PDF_QUALITY | Non-PDF input is refused. Tool stdout is not trusted. Font embedding and small-image checks fail closed. | A trusted tool blob could have passed. |
| RELEASE_EXACT_SET | Missing or empty `original_hashes` is a hash-launder failure. | A rewritten manifest without original hashes could have passed. |
| RELEASE_PARITY | Parity depends on that exact-set hash contract. | A parity pass that ignored original hashes could be reused. |
| STATUS_AUTHORITY | Doubled spaces and build-label wording are conflicts. | A pass that missed that wording could be reused. |

## Reviewed and left at 1.0

| Gate | Decision |
|---|---|
| SCHEDULE_POLICY | The producer matches the definition written with the gate. No earlier sealed PASS exists to reuse. |
| CHAPTER_SPEC, NOTES_STRUCTURE, SLIDES_STRUCTURE, ANSWER_LEAKAGE, FRESH_EXPORT, RETIRED_CONTENT, INVENTORY, ADVERSARIAL_QA, PRIOR_FROZEN_NONREGRESSION | Implementation of the gate contract did not change in a way that would let an old PASS survive a stricter rule. |
| POST_FREEZE_GOLDEN, OOXML_FORENSICS, SOURCE_CLOSURE, CLEAN_ROOM_REPRODUCTION, PROVENANCE_INTEGRITY | These are 1.0. The last four were added in Phase C. No prior version exists. |

## Bumped to 1.2

| Gate | What changed | Why a 1.1 PASS cannot be reused |
|---|---|---|
| RENDER_COMPLETENESS | A render hash is the PNG identity. It is not required to equal the spec candidate hash. The cited source hash and the render-file hash must match the record. | A 1.1 pass treated hash equality with the candidate as the render check and could not describe a real multi-file render. |
| RENDERED_VISUAL_QA | Margin ink is content ink. A declared background bleed may reach the edge. Export-edge fringe and PDF boxes with no rendered ink are not content violations. | A 1.1 pass could treat every non-white margin pixel, including a full-bleed background, as the same failure. |
| PDF_QUALITY | Text presence is `pdftotext`, not a raw `Tj`/`TJ` byte scan. A full-page background raster uses the decorative DPI class. | A 1.1 fail or pass could turn on whether a compressed content stream happened to contain those two bytes. |

New evidence is stamped with `gate.gateVersion` by `seal()`. A stored 1.0 or 1.1 record for a bumped gate fails closed.
