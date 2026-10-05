# Visual QA (deterministic rendered checks)

Tool: `tools/qa_visual_pdf.py` · overall: **PASS**

| Artifact | Kind | Pages | PASS | WARN | FAIL | Result |
|---|---|---|---|---|---|---|
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes.pdf` | letter | 3 | 3 | 0 | 0 | **PASS** |
| `production/premium-notes/01-ch1-energy-causes-change-guided-notes-key.pdf` | letter | 3 | 3 | 0 | 0 | **PASS** |
| `production/worksheets/01-ch1-energy-causes-change-practice.pdf` | letter | 2 | 2 | 0 | 0 | **PASS** |
| `production/quizzes/01-ch1-energy-causes-change-quiz.pdf` | letter | 2 | 2 | 0 | 0 | **PASS** |
| `production/worksheets/01-ch1-energy-detectives-student.pdf` | letter | 2 | 2 | 0 | 0 | **PASS** |
| `production/slides/01-ch1-energy-causes-change-slides.pdf` | slide | 45 | 45 | 0 | 0 | **PASS** |
| `production/teacher-playbook/unit1-teacher-playbook.pdf [pp. 1-21]` | letter | 21 | 21 | 0 | 0 | **PASS** |
| `production/releases/chapter-01/01-ch1-energy-causes-change-teacher-key.pdf` | key | 6 | 6 | 0 | 0 | **PASS** |
| `production/releases/chapter-01/01-ch1-friday-flex.pdf` | letter | 4 | 4 | 0 | 0 | **PASS** |

## WARN / FAIL detail

None.
| File | Page/slide | Class | Issue |
|---|---|---|---|

## Scope notes

- **Method:** deterministic rendered checks (`pdftotext -bbox` geometry, `pdftoppm` pixel ink: blank / footer-only / edge-band clipping, minimum word-box height, page size, tight-bottom and sparse-page) **plus** rendered-image inspection of sampled pages/slides (playbook Ch1 spread, slide 14, notes). Slide chrome (slide numbers) is allowed within 5 pt of the slide edge.
- **Release copies** (`production/releases/chapter-01/*`) are byte-identical to their canonical masters (see `PHASE_6_1_CH1_RELEASE_PARITY_QA.md`), so visual results transfer; the two derived release PDFs (teacher-key bundle, Friday FLEX bank) are checked above.
- **Playbook:** pages 1–21 (front matter and the Chapter 1 sections) are in Phase 6.1 scope → **PASS**. Pages 22–33 (Chapter 2 sections, answer-key architecture, placeholders) are unchanged by Phase 6.1; they carry **3 pre-existing, informational WARN (sparse last-page-of-section)** that belong to the Chapter 2 / unit-assembly phases:

| File | Page | Class | Issue | Severity | Fix (deferred to owning phase) |
|---|---|---|---|---|---|
| `unit1-teacher-playbook.pdf` | 22 | WARN (out of scope) | Chapter 2 teacher-spread left page spills 2 table rows onto its own page (~18% filled) | Low | Tighten Ch2 spread text in the Ch2 phase |
| `unit1-teacher-playbook.pdf` | 26 | WARN (out of scope) | Chapter 2 slide-map last row + footnote spill (~16% filled) | Low | same |
| `unit1-teacher-playbook.pdf` | 30 | WARN (out of scope) | Answer-key architecture table spill (last rows) (~22% filled) | Low | Unit-assembly phase |

- **Defect found and fixed during Phase 6.1 visual QA:** the Playbook had two blank (footer-only) pages and a spilled Ch1 spread/slide-map/support index after the timing text was updated. Fix: shortened Ch1 text and replaced the page-break carrier with a 1-pt zero-spacing paragraph (`tools/build_teacher_playbook.py::_page_break`). The checker now FAILs footer-only pages.
