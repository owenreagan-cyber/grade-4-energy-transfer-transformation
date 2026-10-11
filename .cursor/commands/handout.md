---
description: Create clean, printable student lab sheets or study guides as PDFs
---

Draft a printable student handout/worksheet for: $ARGUMENTS

Design Rules:
1. Produce a standalone HTML file with clean print CSS (@page { margin: 18mm; }, sans-serif fonts, structured tables with page-break-inside: avoid;).
2. Include student name/date headers, explicit directions, diagram boxes, and lined response areas.
3. Save HTML to `curriculum/handouts/<name>.html`.
4. Compile to PDF:
   `node tools/render-pdf.js curriculum/handouts/<name>.html _review_renders/<name>.pdf`
5. Run the auditor: `python tools/audit_doc.py _review_renders/<name>.pdf`