# SOURCE HIERARCHY (DRAFT)

> Proposed hierarchy of trust for curriculum content. **Not final curriculum decisions** — this is a provenance model to be refined in Phase 1.

## LEVEL 1 — AUTHORITATIVE
- CKSci **Student Reader** (complete): `assets/authoritative/student-reader/complete/`
- CKSci **Teacher Guide**: `assets/authoritative/teacher-guide/`
- Confirmed official **Unit 1 activity pages** (Activity Pages, Worksheets, Answer Key, Vocabulary Study Guide): `assets/authoritative/official-activity-pages/`

## LEVEL 2 — AUTHORITATIVE DERIVATIVES
- Chapter splits (1–3, 5–7) + Glossary: `assets/authoritative/student-reader/chapters/` and `.../glossary/`
- (Chapter 4 split is missing as a standalone file; its content lives in the complete Reader.)

## LEVEL 3 — SUPPLEMENTAL
- External/third-party worksheets and activities (Forms of Energy, Newton, heat, kinetic/potential): `assets/supplemental/`
- Presentations (7 Forms of Energy PPT, Energy Supplemental Unit lesson slides): `assets/supplemental/presentations/`
- ISN / notebook / study-guide / teacher-created materials: `assets/supplemental/notes/`
- Teacher-created tests, Quizlet/Kahoot exports, online-resource lists, materials/equipment list: `assets/supplemental/external-reference/`
- Cloud-only pointers (.gdoc/.gslides metadata): `assets/supplemental/external-reference/` (content not local)

## LEVEL 4 — OUR DRAFTS
- Custom labs (`assets/drafts/labs/`), custom student workbook (`assets/drafts/student-workbooks/`), custom unit test (`assets/drafts/assessments/`), and future planning outputs.

## Conflict rule
When sources conflict, **do not silently reconcile them**. Flag the conflict in `OPEN_QUESTIONS.md` and surface it in Phase 1 planning.
