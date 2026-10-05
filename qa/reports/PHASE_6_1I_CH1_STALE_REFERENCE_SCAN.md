# Chapter 1 Note-Architecture FAIL-CLOSED Scan (Phase 6.1I)

Tool: `tools/qa_ch1_note_architecture.py`. Result: **PASS**

Concept gate: a clause that names a student note system and assigns a role enters review. Active architecture authorities scanned whole-file: **6**. Sensitive clauses: **43** (auto-safe **0** · allowlisted **43** · unreviewed **0**). Stale allowlist: **0**. Chapter-scoped exclusions (OUT OF SCOPE — PHASE 7.1+): **7**. Retired-standard leading-banner hits: **0**.

| Authority | Sensitive | Auto-safe | Allowlisted | Unreviewed | Exclusions |
|---|---|---|---|---|---|
| `AGENTS.md` | 2 | 0 | 2 | 0 | 0 |
| `production/PRODUCTION_MANIFEST.md` | 16 | 0 | 16 | 0 | 7 |
| `docs/planning/CURRENT_DECISIONS.md` | 14 | 0 | 14 | 0 | 0 |
| `docs/standards/GUIDED_NOTES_STANDARD.md` | 4 | 0 | 4 | 0 | 0 |
| `docs/standards/UNIT1_PRODUCT_STANDARD.md` | 3 | 0 | 3 | 0 | 0 |
| `docs/chapter-01/CH1_GOLD_STANDARD_PROPAGATION_SPEC.md` | 4 | 0 | 4 | 0 | 0 |

## Chapter-scoped exclusions

These register rows sit under a Chapter 2–7 heading. They are OUT OF SCOPE — PHASE 7.1+ and are not Chapter 1 architecture decisions. A global statement in the same file is still in scope.

- `production/PRODUCTION_MANIFEST.md` (ch2) \| P3 \| Guided Notes \| `production/student-notes/02-ch2-moving-objects-have-energy-guided-notes.docx` \| `production/releases/chapter-02/` \| RELEASED \| ADAPTED \|
- `production/PRODUCTION_MANIFEST.md` (ch2) \| P11 \| Interactive Science Notebook \| `production/student-notebook/chapter-02/02-ch2-interactive-notebook.docx` \| `production/releases/chapter-02/02-ch2-interactive-science-notebo
- `production/PRODUCTION_MANIFEST.md` (ch3) \| P3 \| Interactive Science Notebook \| `production/student-notebook/chapter-03/03-ch3-interactive-notebook.docx` \| `production/releases/chapter-03/03-ch3-interactive-science-noteboo
- `production/PRODUCTION_MANIFEST.md` (ch4) \| P4 \| Interactive Science Notebook \| `production/student-notebook/chapter-04/04-ch4-interactive-notebook.docx` \| `production/releases/chapter-04/04-ch4-interactive-science-noteboo
- `production/PRODUCTION_MANIFEST.md` (ch5) \| P4 \| Interactive Science Notebook \| `production/student-notebook/chapter-05/05-ch5-interactive-notebook.docx` \| `production/releases/chapter-05/05-ch5-interactive-science-noteboo
- `production/PRODUCTION_MANIFEST.md` (ch6) \| P4 \| Interactive Science Notebook \| `production/student-notebook/chapter-06/06-ch6-interactive-notebook.docx` \| `production/releases/chapter-06/06-ch6-interactive-notebook.pdf` \|
- `production/PRODUCTION_MANIFEST.md` (ch7) \| P4 \| Interactive Science Notebook (3 inserts) \| `production/student-notebook/chapter-07/07-ch7-interactive-notebook.docx` \| `production/releases/chapter-07/07-ch7-interactive-sci

| Retired standard | Leading banner |
|---|---|
| `docs/planning/SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md` | PASS |
| `docs/planning/INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md` | PASS |
| `docs/planning/STUDENT_NOTES_STANDARD.md` | PASS |
