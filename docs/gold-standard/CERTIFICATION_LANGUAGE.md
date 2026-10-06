# Certification Language

Chapter Factory gate status is exactly `PASS`, `FAIL`, or `NOT_VERIFIED`.

Finding severity is exactly `BLOCKING`, `HIGH`, `MEDIUM`, `LOW`, or `INFO`.

A warning is a finding. It is not a gate status. Do not emit `PASS_WITH_WARNINGS`, `MOSTLY_PASS`, `PARTIAL`, `CLEAN`, `READY`, or `OK`.

Legacy artifact reports may still say `WARN` under `.cursor/rules/30-qa-and-release.mdc`. When that report enters a Chapter Factory gate, the warning is stored as a finding. The gate status stays one of the three words above.

Release Judge status is exactly `PASS` or `FAIL`. A lifecycle state is not a gate status.

The evaluator in `tools/chapter_qa/evidence.py` computes status. The `status` field on a record is a claim. A claim cannot upgrade the result.

## Words

| Word | Meaning |
|---|---|
| performed | The gate actually executed. |
| inspected | A declared evidence item was examined with the declared method. |
| rendered | A source artifact was converted into the declared visual evidence. |
| observed | Required evidence existed and was read. |
| flagged | A finding was emitted. |
| finding | A flagged issue with one severity. |
| verified | The claim has accepted supporting evidence. |
| PASS | The gate contract is fully satisfied. |
| FAIL | The gate contract is not satisfied. |
| NOT_VERIFIED | The gate definition permits unavailable evidence, and the record cites that reason. |
| certified | Release Judge `PASS` for one exact build. |
| approved | An authorized lifecycle decision. |
| frozen | The immutable approved state tied to a freeze identity. |

## PASS

`PASS` is allowed only when all of these hold:

- `performed` is true
- execution succeeded
- every required input exists
- the expected inventory is complete
- the observed inventory matches the expected inventory
- the evidence belongs to the requested build
- required hashes match
- the evidence is not stale
- independence requirements are satisfied
- no `BLOCKING` finding exists
- no gate-specific failure exists

`performed: false` cannot be `PASS`.

An empty input set is not a clean pass. Zero findings are not a pass unless execution and completeness are valid.

## FAIL

Use `FAIL` for a missing required input, a missing render, a missing slide, a parser crash, a detector exception, or a failed tool execution.

`NOT_VERIFIED` is not a substitute for those defects.

## NOT_VERIFIED

`NOT_VERIFIED` is allowed only when the gate definition sets `allowedNotVerified` and the record sets `execution.unavailableEvidence` with a `notVerifiedReason`.

## Roles

| Role | Who |
|---|---|
| `SOURCE_SCHOLAR` | Function of `curriculum-source-reviewer`. Evidence cites Reader/TG bytes. |
| `CURRICULUM_AUDITOR` | Function of `curriculum-source-reviewer`. Does not issue release certification. |
| `BUILDER` | `guided-notes-specialist`, `slideshow-specialist`, `assessment-student-resource-specialist`, `visual-art-director`. |
| `CROSS_ARTIFACT_AUDITOR` | `qa-certification-reviewer`. Gate evidence only. |
| `VISUAL_QA_AUDITOR` | No agent yet. Not the visual-art director. |
| `PDF_OOXML_FORENSICS` | No agent yet. Headless PDF/OOXML checks will write this evidence. |
| `PROVENANCE_AUDITOR` | `provenance-auditor`. |
| `QA_ADVERSARY` | `qa-adversary`. |
| `RELEASE_JUDGE` | `release-judge`. Only this role issues internal release certification. |

`visual-art-director` produces design. It is not the visual QA certifier.

One agent is not both the cross-artifact reviewer and the release judge.

## Build identity

`buildId`, `candidatePath`, `candidateFreezeId`, `candidateHash`, `sourceFreezeId`, `sourceHash`, and `inputHashes` associate evidence with one build. The association hash is SHA-256 of the canonical JSON of those fields. Evidence from build A cannot certify build B.

## Independence

`thingBeingCertified` and `independentEvidenceSource` must be materially distinct when the gate requires independent evidence. The same source model, the same ledger, the same mutable working-tree golden, or the same newly generated freeze on both sides is self-evidence and is rejected. Renaming one side (`working-tree-golden` versus `mutable-golden`, or `source model` versus `source-model`) does not make it distinct. A hash typed into the label does not make it distinct.

Builder-only evidence cannot satisfy a gate that requires independent evidence.
