# MCP Governance

Phase C.1 defines policy only. No MCP server is configured. `.cursor/mcp.json` is not created. Certification does not call an MCP.

The checked policy functions live in `tools/hooks/mcp_policy.py`. A future `beforeMCPExecution` hook must call those functions. It must not invent a second allow list in shell.

## Classes

| Class | Meaning |
|---|---|
| READ_ONLY_SOURCE | Read an externally hosted source and record provenance. |
| READ_ONLY_REVIEW | Read metadata, such as a pull request, without writing. |
| DESIGN_WRITE | Create or edit a design file. |
| REPOSITORY_WRITE | Write to a git host: push, merge, or edit files through the host. |
| EXTERNAL_ACTION | Send mail, post a message, or take any action outside the repo. |

## Role permissions

| Role | May call | Must not |
|---|---|---|
| SOURCE_SCHOLAR | READ_ONLY_SOURCE, READ_ONLY_REVIEW, and only when the authoritative source is external and provenance is stored | Treat an MCP payload as the gate result |
| CURRICULUM_AUDITOR | READ_ONLY_SOURCE | Use a builder's expected answer as authority |
| VISUAL_ART_DIRECTOR | DESIGN_WRITE, after a later phase configures it | Certify the picture it just drew |
| VISUAL_QA_AUDITOR | READ_ONLY_REVIEW | Certify from the same design-server state that produced the asset |
| QA_ADVERSARY | READ_ONLY_REVIEW | Mutate canonical artifacts through any MCP |
| RELEASE_JUDGE | Nothing | Call a write-capable MCP, or fetch missing evidence to fill a hole |
| BUILDER, CROSS_ARTIFACT_AUDITOR, PDF_OOXML_FORENSICS | Nothing through MCP | Submit MCP output as independent evidence |

`may_satisfy_independent_gate` is false for every role and every class. MCP output can be an input to a local auditor. It cannot be the independent gate result.

`failure_cannot_pass` is true for every class. A missing server, a timeout, or an error is not PASS.

`local_verification_required` is true for every class.

## Servers

### Figma

| Field | Value |
|---|---|
| Purpose | Reusable visual assets, diagrams, components, and visual consistency. |
| Class | DESIGN_WRITE |
| Authentication | Environment variable name `FIGMA_TOKEN` only, when a later phase configures it. |
| Read | Design files and exports. |
| Write | Design files, when configured. |
| Allowed roles | VISUAL_ART_DIRECTOR |
| Prohibited roles | VISUAL_QA_AUDITOR, QA_ADVERSARY, RELEASE_JUDGE, CURRICULUM_AUDITOR |
| Independent gate | No |
| Local verification | Required. Export, then render the PPTX or PDF locally, then an independent visual audit of that render. |
| Secrets | Never commit the token. |
| Failure | Fail closed. Absence is not a visual PASS. |
| Current status | NOT CONFIGURED |

Figma is not authoritative for curriculum wording, answer truth, or release certification.

### Canva

| Field | Value |
|---|---|
| Purpose | Optional supplementary visuals. |
| Class | DESIGN_WRITE |
| Authentication | Environment variable name `CANVA_TOKEN` only, when a later phase configures it. |
| Read | Design status and export metadata. |
| Write | Supplementary designs, when configured. |
| Allowed roles | VISUAL_ART_DIRECTOR |
| Prohibited roles | VISUAL_QA_AUDITOR, QA_ADVERSARY, RELEASE_JUDGE |
| Independent gate | No |
| Local verification | Required. Provenance, a local hash, the embedded artifact, a PDF render, and the same visual QA as every other render. |
| Secrets | Never commit the token. |
| Failure | "Export succeeded" on the server is not a release PASS. |
| Current status | NOT CONFIGURED |

Canva is not the canonical instructional source, not QA evidence authority, and not a replacement for the DOCX/PPTX pipeline.

### GitHub

| Field | Value |
|---|---|
| Purpose | Possible later read of pull-request metadata. |
| Class | READ_ONLY_REVIEW if it is ever enabled. REPOSITORY_WRITE stays prohibited for certification. |
| Decision | DEFER |
| Why | The local repository is canonical for build and certification. No current workflow needs the host API. `git` in the working tree already covers status, diff, and log. |
| Independent gate | No |
| Failure | A host error cannot certify a chapter. |

### Authoritative curriculum host

Not used. The CKSci Reader and Teacher Guide in `assets/authoritative/` are the source. A READ_ONLY_SOURCE server would be allowed for SOURCE_SCHOLAR only if a future source lived off-machine and the fetch recorded provenance. That output would still be an input, not a gate result.

## Independence

Bad: a Figma design is created, the same Figma document is queried, and that query is called visual certification.

Good: the design is exported to PPTX or PDF, rendered locally with the deterministic tools, and a visual auditor inspects the render.

Bad: Canva reports that an export succeeded, and the release is marked PASS.

Good: the export is hashed locally, embedded in the artifact, rendered to PDF, and put through independent visual QA.

## Secrets

Do not store tokens in `.cursor/mcp.json`, repo files, QA evidence, or reports.

If a future MCP config format supports environment interpolation, commit the variable name only.

`tools/hooks/redact.py` replaces token-shaped values before text is written to an inventory. A bare environment-variable name such as `FIGMA_TOKEN` is kept.

The example file `docs/gold-standard/mcp.example.json` is not active configuration. It contains no secrets.

## Failure and certification

No MCP is required for certification. If a server is down, the local evidence set is unchanged. The Release Judge does not go fetch a replacement. Missing evidence stays missing, and the judgment fails closed.
