# SOURCE PROVENANCE

> Phase 0 record of where each source came from, plus cloud-original pointers. Generated 2026-09-26.

## Discovery locations (searched, bounded)
- `~/Downloads` — chapter split PDFs, glossary, three AI-generated drafts.
- `~/Desktop` and `~/Documents` — searched; no energy-unit sources found (science folder is an empty "setup_needed" scaffold).
- `~/Projects` — searched; only unrelated "fake-staging" placeholders in `teacher-ai-workstation`.
- **Google Drive (school)** — `GoogleDrive-owen.reagan@thalesacademy.org` → "Core Knowledge Curriculum/Unit 1 - Energy Transfer and Transformation" (primary authoritative folder) and "4th Grade FPK" (materials list, unit slides) and "My Drive/00-Library/Science" (Newton sample).
- **Google Drive (personal)** — `GoogleDrive-oreagan81@gmail.com` → second Student Reader copy, ISN pages, "7 Forms of Energy" PPT.

## Cloud-original pointers (content NOT downloaded)
These `.gdoc`/`.gslides` files are Google Drive metadata placeholders (~174–184 bytes). Content is cloud-only. Retained for doc IDs.

| File | Google Doc/Slides ID | Account |
|---|---|---|
| Science 4 - Energy Transfer - Student Notebook Pages.gdoc | `16X7VLXGLSVD0s7PFzamcRWItsnsU6i5p6pOez1Pagfo` | school |
| Science 4 - Energy Transfer - Video Resources.gdoc | `14qBhFWVbuDD71HLSRkPmhOubw87Bkf_T8Ckj4SAbJlo` | school |
| Science 4 - Energy Transfer and Transformation - Presentation Slides.gslides | `1QtBku__MFLDuSMPjkYJBdK1115f88v8pPZFsJNbs4Ds` | school |
| Science 4: Energy Transfer - Pacing Guide.gdoc | `1S1Ph0XkYYZ9KqvxzeTI-D-Go9LROD_8fVedvjTsO7mU` | school |
| Science 4 - Energy Transfer - Project Slides.gslides | `11m4Hsmbr8H6Lj2MoSRfan18rjt9JLS4T5HudT86Y3zc` | school |
| Science - Unit 1 Vocabulary Quiz.gdoc | `1OM3tcoi7Fl59MDdwymRQHGC5MdXIdXE-QFJwT46NLXk` | school |
| Descriptive Paragraph Ideas and Planning.gdoc | `1_fRO6Itcboit1ykSyLFWrB1-CjHq3UhCzhpHZ1Kz8YE` | school |
| Unit 1: Energy Transfer and Transformation.gslides (FPK) | `1m9rLlOWPo6TrtnDm4KaocYAbxkGXtACicFVgRxhdlvs` | school |
| Energy Transfer ISN pages.gdoc | `1TrWIue--LI-w0MfOvoPLEZjcYHtKAxQ3DzQjv-JvwxU` | personal |

## Google Drive immutability
School-Drive source files carry the macOS `uchg` (user-immutable) flag (set by Google Drive for Desktop). Originals were read-only copied out; **no cloud original was modified, renamed, or deleted.**

## Phase 1 canonical Reader decision (2026-09-26)
- **Canonical Reader** = `assets/authoritative/student-reader/complete/Science 4 - Energy Transfer - Student Book.pdf` (PDF 1.4, GPL Ghostscript, 54 pp, ~2.95 MB). Chosen for cleaner encoding, smaller size, and residence in the primary school Drive folder.
- **Backup copy retained** = `Energy+Transfer+and+Transformation+SR.pdf` (PDF 1.6, 54 pp). Content/page order verified substantively identical (only front-matter/whitespace/case differences).
- **Chapter 4 derivative regenerated** = `assets/authoritative/student-reader/chapters/Chapter_4_Energy_Transfer.pdf` (pages 23–30, 8 pages, SHA-256 `99c077ad4c4aa7c2f1db575d00f0d41831a29988c357674aca3d53bfc6762518`). Classified AUTHORITATIVE DERIVATIVE.

## Not found locally (documented, not fabricated)
- `Chapter_4_Energy_Transfer.pdf` — **was** missing; regenerated in Phase 1 (see above).
- Chat-cited `CKSci_G4UsingNaturalResources_SR.pdf` / `CKSci_G4_U1_Energy_TG.pdf` — exact filenames absent; content preserved as "Science 4 - Energy Transfer - Student Book.pdf" / "TG .pdf".
- Chat-cited numbered activity pages `1.1.pdf`..`13.6.pdf` — not present as separate files; contained in `Science 4 - Energy Transfer - Activity Pages.pdf`.
- Chat-cited `Pasted text(20260925-202640).txt` / `(20260925-212909).txt` — not found; three unrelated `Pasted text*` files in ~/Downloads were examined and excluded (Claude dev log, Saxon 5 slide-builder code, Canvas/Thales matrix).

## Phase 13B — authoritative Unit 2 intake (2026-09-27)
- **Unit 2 = "Using Natural Resources for Energy" (CKSci G4).** Two Level-1 sources located in `~/Downloads` and copied (not moved) to `assets/authoritative/unit-02/`:
  - Teacher Guide `CKSci_G4UsingEnergyResources_TG.pdf` (178 pp) → `teacher-guide/Using Natural Resources for Energy - Teacher Guide.pdf`.
  - Student Reader `CKSci_G4UsingEnergyResources_SR.pdf` (64 pp) → `student-reader/complete/Using Natural Resources for Energy - Student Reader.pdf`.
- Chapter derivatives (9 chapters + Glossary) regenerated from the canonical Student Reader via `qpdf` page extraction (`student-reader/chapters/`). The prompt-cited `using_natural_resources_chapters 2(1).zip` was **not present** locally; derivatives were built to match (Level 2 AUTHORITATIVE DERIVATIVE). No source content altered.
- `CKSci_G4UsingEnergyResources_TG.pdf` was previously cataloged as supplemental-review entry #84 in Phase 13A; it is now formally admitted as **AUTHORITATIVE** (entry #88) — the earlier supplemental copy under `assets/supplemental/review/reference/unit-02/` remains as a working reference only.
- Source map + PBL lesson structure + terminology/content boundaries: `docs/reviews/intake/PHASE13B_UNIT2_AUTHORITATIVE_INTAKE.md`; inventory entries #88–#99.

## Phase 13A — ChatGPT workstream intake (2026-09-27)
- 22 net-new supplemental/review files copied (not moved) from `~/Downloads` into `assets/supplemental/review/` (and 3 new MP4s into `assets/supplemental/media/chapter-02/`). Originals preserved in `~/Downloads`.
- Source: ChatGPT resource-generation workstream (AI-generated review decks, Unit 2 drafts, labs, flex ideas, certificate) + one CKSci official Teacher Guide (`CKSci_G4UsingEnergyResources_TG.pdf` = "Using Natural Resources for Energy" TG, 178 pp — **Level-1 authoritative candidate** for Unit 2, formal authoritative intake pending).
- 7 additional MP4s + `Energy_Detectives.pptx` + `Energy_in_Motion.pptx` + `chapter-reading-worksheet-assessments.pdf` were already present from prior phases and were **not** re-imported.
- All 22 new copies verified byte-for-byte (SHA-256) against originals; none altered in place. Catalog + disposition + revision requirements + school content constraint: `docs/reviews/intake/PHASE13A_NEW_RESOURCE_INTAKE.md` and `SOURCE_INVENTORY.md` entries #66–#87.

## Hash verification
64 project copies verified byte-for-byte (SHA-256) against originals; 64 originals confirmed unchanged after copy. See `SOURCE_INVENTORY.md` for full hashes.
