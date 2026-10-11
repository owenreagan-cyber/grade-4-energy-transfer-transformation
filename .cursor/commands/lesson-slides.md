---
description: Create instructional slide decks in Marp and compile to PDF
---

Draft an engaging, high-contrast instructional slide deck for Grade 4 Science: $ARGUMENTS

Design Rules:
1. Marp Frontmatter:
   ---
   marp: true
   theme: uncover
   class: invert
   paginate: true
   header: "Grade 4 Science: Energy Transfer & Transformation"
   footer: "Instructional Science Module"
   ---
2. Target 4th-grade readability: clear bold lead-ins, 3–4 concise bullet points per slide, large type.
3. Save to `curriculum/slides/<lesson-name>.md`.
4. Compile immediately to `_review_renders/`:
   `npx @marp-team/marp-cli curriculum/slides/<lesson-name>.md -o _review_renders/<lesson-name>-slides.pdf --allow-local-files`
5. Run the auditor: `python tools/audit_doc.py _review_renders/<lesson-name>-slides.pdf`