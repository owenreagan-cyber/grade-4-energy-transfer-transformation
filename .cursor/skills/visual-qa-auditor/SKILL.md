# visual-qa-auditor

Emit `RENDER_COMPLETENESS` and `RENDERED_VISUAL_QA` evidence from rendered pages. The visual-art director does not run this skill.

## Allowed
- Read candidate DOCX, PPTX, and PDF files.
- Write renders, crops, and evidence under `qa/work/<buildId>/`.
- Run `tools/render_chapter_artifacts.py`, `tools/chapter_qa/render_completeness.py`, and `tools/chapter_qa/visual_qa.py`.

## Workflow
1. Render headless at 300 DPI into the isolated workspace. Do not write into `production/` or `curriculum/`.
2. Compare the expected page inventory with the observed renders.
3. Inspect every page. Run the deterministic detectors.
4. For a suspicious region, write a 600 DPI crop.
5. Call `emit_visual_evidence`. A contact sheet is navigation only.

## Fail closed
- Expected count differs from observed count.
- Empty render directory or a failed render command.
- No render input for a detector.
- Inspection by source XML, text extraction, or a contact sheet alone.
- A suspicious finding with no 600 DPI crop.

## Prohibited
- Assigning PASS or release certification.
- Using OOXML structure as visual proof.
- Certifying art the same agent just produced. This skill is read-only on the candidate.
