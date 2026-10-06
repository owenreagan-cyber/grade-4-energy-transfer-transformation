# pdf-ooxml-forensics

Emit `PDF_QUALITY` evidence from PDF tools, and structural OOXML findings from the package. OOXML findings do not satisfy `PDF_QUALITY` or rendered visual QA.

## Allowed
- Read candidate PDF, DOCX, and PPTX files.
- Write evidence under `qa/work/<buildId>/evidence/`.
- Run `tools/qa_pdf_quality.py` and `tools/qa_ooxml.py` with `qpdf`, `pdfinfo`, `pdffonts`, and `pdfimages`.

## Workflow
1. Check qpdf structure, page count, page size, fonts, and image inventory.
2. Compute effective DPI from pixel size and placed size. Use `qa/gold-standard/dpi_policy.json`.
3. Check the OOXML package for relationships, hidden slides, speaker notes, and corrupt XML.
4. Call `emit_pdf_evidence` for the PDF. Record OOXML with `inspect_package`. A clean package does not pass PDF quality.

## Fail closed
- qpdf rejects the file.
- Page count or page size does not match the expectation.
- Essential imagery below the configured fail DPI.
- Broken relationships, corrupt XML, unexpected hidden slides, or a speaker-note mismatch when notes are required.

## Prohibited
- Assigning PASS or release certification.
- Treating a successful open as a quality pass.
- Treating OOXML structure as rendered visual evidence.
- Editing the candidate.
