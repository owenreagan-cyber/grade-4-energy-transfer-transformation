# Chapter 2 Visual Candidate V3 — Artifact Inventory

Status: candidate package complete for classroom-readiness review; external Grok audit and release freeze are pending.

## Final candidate deliverables

| Artifact | Path / scope | Count / hash | QA disposition |
|---|---|---|---|
| Editable PPTX with integrated speaker notes | `production/candidates/chapter-02/02-ch2-moving-objects-have-energy-visual-candidate-v3.pptx` | 49 slides; SHA-256 `21c5c39e2a79dd0bd33cc62a605f588579ca6fd963cd89277626dff66a564ab7` | PASS |
| Rendered PDF | `production/candidates/chapter-02/02-ch2-moving-objects-have-energy-visual-candidate-v3.pdf` | 49 pages; SHA-256 `51fe1a6cacaf95f515a4f98be08decad2a664bf9eb05bfc0f9507c00d0fafbb0` | PASS |
| 300-DPI slide PNGs | `previews/ch2-visual-candidate-v3/ch2-slides-300dpi/slide-01.png` through `slide-49.png` | 49 files | PASS |
| Contact sheet | `work/ch2-visual-candidate-v3/contact-sheets/CH2_VISUAL_CANDIDATE_V3_CONTACT_SHEET.png` | SHA-256 `dcec2ec1172e71a3d59159efe28c8c947962e4ee2fc51ee59e30f72301ef3b1f` | PASS |
| Artifact Tool renders | `work/ch2-visual-candidate-v3/artifact-tool-renders-v3/` | 49 PNGs + montage | Structural build evidence |

## Contracts and manifests

| Artifact | Path | Hash / status |
|---|---|---|
| Content contract | `work/ch2-visual-candidate-v1/CH2_CONTENT_CONTRACT.json` | `011f11098cd9a321a3019b7e09313aeecc7e65edd62a941a7e8776be4faed329` |
| Content contract, readable | `work/ch2-visual-candidate-v1/CH2_CONTENT_CONTRACT.md` | `5b555a613c0481d4a8047c204593e2041d62e74b663bee94ab133a20ee8f28bc` |
| Instructional Alignment Contract | `work/ch2-visual-candidate-v3/CH2_INSTRUCTIONAL_ALIGNMENT_CONTRACT.json` | 49 records; `b8393083d3289d48110c6480c69369bd090b94d12b51b5e49323f2032c1b6d27` |
| Slide manifest | `work/ch2-visual-candidate-v3/CH2_SLIDE_MANIFEST.json` | 49 records; `0d87d82fb85d6c94c321029bc7c28161eb47c85b6f5d52ea320aedeb097b99b7` |
| Image asset manifest | `assets/ch2/candidate-v1/IMAGE_ASSET_MANIFEST.json` and `.md` | 10 generated assets; science-reviewed |
| Notes mapping | `work/ch2-visual-candidate-v3/CH2_NOTES_TO_SLIDES_MAPPING.md` | PASS |
| Source traceability | `work/ch2-visual-candidate-v3/CH2_SOURCE_TRACEABILITY.md` | PASS |
| Frozen-pacing crosswalk | `work/ch2-visual-candidate-v3/CH2_REQUIRED_OPTIONAL_TIMING.md` | PASS |
| Remaining issues | `work/ch2-visual-candidate-v3/CH2_REMAINING_ISSUES.md` | 0 classroom blockers; 4 production WARN items |

## QA and reproducibility

| Artifact | Path | Result |
|---|---|---|
| Candidate builder | `work/ch2-visual-candidate-v1/build-ch2-visual-candidate.mjs` | Reproduces V3; source assets embedded as bytes |
| Candidate content QA tool | `tools/qa_ch2_visual_candidate.py` | PASS on V3 |
| Content / notes / leakage report | `qa/reports/CH2_VISUAL_CANDIDATE_V3_CONTENT_QA.md` | 49 PASS, 0 FAIL |
| Deterministic rendered visual report | `qa/reports/CH2_VISUAL_CANDIDATE_V3_DETERMINISTIC_VISUAL_QA.md` | 49 PASS, 0 WARN, 0 FAIL |
| Classroom readiness report | `qa/reports/CH2_VISUAL_CANDIDATE_V3_CLASSROOM_READINESS_QA.md` | CLASSROOM READY PASS |
| Finalizer receipt | `.codex-build/ch2-visual-candidate-v3/candidate.validation.json` | Package integrity, layout, fonts, first-party import, native tables PASS |

## Generated image set

Directory: `assets/ch2/candidate-v1/`  
Count: 10 selected source PNGs plus two manifests.  
The JSON manifest records dimensions, SHA-256 hashes, generation prompts, crops, provenance class, slide usage, and science review for each asset.

## Superseded candidate history retained

- V1 PPTX/PDF, 49 300-DPI PNGs, renders, and QA reports: first complete build; superseded because slides 42–49 had an extension badge/title collision.
- V2 PPTX/PDF, 49 300-DPI PNGs, renders, review sheets, and QA reports: badge issue fixed; superseded because slide 10 punctuation wrapped alone.
- V3: both issues fixed and all final checks pass.

These files are retained for provenance and are not canonical releases.

## Unchanged / not touched

- `production/slides/02-ch2-moving-objects-have-energy-slides.pptx`
- `production/slides/02-ch2-moving-objects-have-energy-slides.pdf`
- Authoritative Reader and Teacher Guide files
- Frozen Guided Notes, key, quiz, and pacing plan

No commit, push, freeze, or release promotion was performed.
