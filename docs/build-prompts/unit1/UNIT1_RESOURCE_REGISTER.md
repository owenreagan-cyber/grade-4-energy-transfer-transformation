# UNIT 1 — RESOURCE REGISTER

> Complete per-chapter + unit-wide register of Unit 1 PDF resources, with recommendations, build order, and dependencies. **Planning register only — does not build, overwrite, freeze, commit, or push anything.**
> Corrected by the **Correction Pass (2026-10-09)** — see "Correction Pass additions" and "Remaining conflicts" at the bottom.

## Recommendation vocabulary

`KEEP` · `POLISH` · `REBUILD` · `CREATE` · `ARCHIVE` · `RETIRE`

## Status (two axes — Correction Pass §9)

- **Content Status:** `CURRENT` · `STALE` · `MISSING` · `HISTORICAL` · `RETIRED`
- **Printable PDF Status:** `PDF_CURRENT` · `PDF_NEEDS_POLISH` · `PDF_NEEDS_REBUILD` · `PDF_MISSING` · `NOT_APPLICABLE`

> A resource is **not** classroom-ready merely because Markdown/source exists. Printable-PDF status is a separate judgment.

---

## Chapter 1 — Energy Causes Change (Reader pp. 1–6 · TG L1–L2)

**Lifecycle: FROZEN v1.1 — no rebuild.**

| Resource | Content | PDF | S/T | Req/Opt | Rec |
|---|---|---|---|---|---|
| Guided Notes + Key | CURRENT | PDF_CURRENT | S/T | REQ | KEEP |
| Practice + Key | CURRENT | PDF_CURRENT (key via combined) | S/T | REQ (ungraded) | KEEP |
| Chapter Quiz (9·16) + Key + Blueprint | CURRENT | PDF_CURRENT | S/T | REQ (graded) | KEEP |
| Energy Detectives + Key + Spec | CURRENT | PDF_CURRENT (student) · MD (key/spec) | S/T | OPT (ungraded) | KEEP |
| Absent Recovery | CURRENT | **PDF_MISSING (MD-only)** | S/T | REQ (support) | POLISH (optional PDF-ify) |
| Friday FLEX | CURRENT | PDF_CURRENT | S/T | OPT | KEEP |

> Ch1 is complete and frozen. No prompt issued. Do not alter.

---

## Chapter 2 — Moving Objects Have Energy (Reader pp. 7–12 · TG L3)

**Lifecycle: FROZEN v1.0 — no rebuild.**

| Resource | Content | PDF | S/T | Req/Opt | Rec |
|---|---|---|---|---|---|
| Guided Notes + Key | CURRENT (FROZEN) | PDF_CURRENT | S/T | REQ | KEEP |
| Practice + Key | CURRENT | PDF_CURRENT | S/T | REQ (ungraded) | KEEP |
| Chapter Quiz (8·12) + Key + Blueprint | CURRENT | PDF_CURRENT | S/T | REQ (graded) | KEEP |
| Moving Marbles + Key + Spec | CURRENT | PDF_CURRENT (student) · MD (key/spec) | S/T | OPT | KEEP |
| Absent Recovery | CURRENT | PDF_CURRENT | S | REQ (support) | KEEP |
| Friday FLEX | CURRENT | PDF_CURRENT | S/T | OPT | KEEP |

> Ch2 is complete and frozen. No prompt issued.

---

## Chapter 3 — Energy and Speed Are Related (Reader pp. 13–16 · TG L4–L5)

**Lifecycle: BUILT_UNCERTIFIED — all artifacts exist; needs certification, not rebuild.**

| Resource | Content | PDF | S/T | Req/Opt | Rec |
|---|---|---|---|---|---|
| Guided Notes + Key | CURRENT (built 8-Oct) | PDF_CURRENT | S/T | REQ | KEEP (certify) |
| Ramp It Up 2.0 + Key + Spec | CURRENT | PDF_CURRENT (student) · MD (key/spec) | S/T | REQ (formative) | KEEP (certify) |
| Drop It + Key + Spec | CURRENT | PDF_CURRENT (student) · MD (key/spec) | S/T | OPT | KEEP |
| Practice + Key | CURRENT | PDF_CURRENT | S/T | REQ (ungraded) | KEEP (certify) |
| Chapter Quiz (12pt) + Key + Blueprint | CURRENT | PDF_CURRENT | S/T | REQ (graded) | KEEP (certify) |
| Absent Recovery | CURRENT | PDF_CURRENT | S | REQ (support) | KEEP |
| Friday FLEX | CURRENT | PDF_CURRENT | S/T | OPT | KEEP |

> Ch3 does **not** need build prompts. It needs the certification pipeline.

---

## Chapter 4 — Energy Transfer (Reader pp. 17–24 · TG L6–L9)

**Lifecycle: RELEASED under retired INB architecture → Guided Notes REBUILD required. Chapter 4 = ENERGY TRANSFER only (no transformation/BOTH).**

| Resource | Content | PDF | S/T | Req/Opt | Prompt | Priority | Rec |
|---|---|---|---|---|---|---|---|
| **Guided Notes (student)** | STALE | PDF_NEEDS_REBUILD | S | REQ | `01_guided-notes/CH04_GUIDED_NOTES_STUDENT_BUILD_PROMPT.md` | P0 | REBUILD |
| **Guided Notes Key** | MISSING | PDF_MISSING | T | REQ | `01_guided-notes/CH04_GUIDED_NOTES_KEY_BUILD_PROMPT.md` | P0 | CREATE |
| Sound/Light/Heat/Electricity investigations + keys | CURRENT | PDF_CURRENT (student) · MD (key/spec) | S/T | REQ (formative) | — | P2 | POLISH (header/badge) |
| Practice + Key | CURRENT | PDF_NEEDS_POLISH | S/T | REQ (ungraded) | — | P2 | POLISH |
| Chapter Quiz (11 item) + Key + Blueprint | CURRENT | PDF_CURRENT | S/T | REQ (graded) | — | — | KEEP |
| Absent Recovery | CURRENT | **PDF_MISSING (MD-only)** | S | REQ (support) | — | P2 | POLISH (optional PDF-ify) |
| Friday FLEX | CURRENT | PDF_CURRENT | S/T | OPT | — | — | KEEP |
| Interactive Science Notebook | RETIRED | NOT_APPLICABLE | S | RETIRED | — (never rebuild) | — | RETIRE |
| **Slide re-sync (future)** | — | NOT_APPLICABLE | T | REQ (after notes) | `10_slide-resync/CH04_GUIDED_NOTES_SLIDE_RESYNC_PROMPT.md` | P1 | `RESYNC_PENDING_GUIDED_NOTES_APPROVAL` |

**Dependency (locked):** Ch4 Guided Notes must be **accepted** before the Ch4 slide re-sync executes. The new Guided Notes architecture drives the re-sync; obsolete INB slide structure must not drive the notes.

---

## Chapter 5 — Collisions Transfer Energy (Reader pp. 25–30 · TG L10–L11)

**Lifecycle: RELEASED under retired INB architecture → Guided Notes REBUILD required. Collision-focused; NO required mass/weight comparison.**

| Resource | Content | PDF | S/T | Req/Opt | Prompt | Priority | Rec |
|---|---|---|---|---|---|---|---|
| **Guided Notes (student)** | STALE | PDF_NEEDS_REBUILD | S | REQ | `01_guided-notes/CH05_GUIDED_NOTES_STUDENT_BUILD_PROMPT.md` | P0 | REBUILD |
| **Guided Notes Key** | MISSING | PDF_MISSING | T | REQ | `01_guided-notes/CH05_GUIDED_NOTES_KEY_BUILD_PROMPT.md` | P0 | CREATE |
| Crash Lab + Key + Spec | CURRENT | PDF_CURRENT (student) · MD (key/spec) | S/T | REQ (formative) | — | P2 | POLISH (header/badge) + **flag Part B mass/weight** |
| Practice + Key | CURRENT | PDF_NEEDS_POLISH | S/T | REQ (ungraded) | — | P2 | POLISH |
| Chapter Quiz (10 item) + Key | CURRENT | PDF_CURRENT | S/T | REQ (graded) | — | — | KEEP |
| Absent Recovery | CURRENT | **PDF_MISSING (MD-only)** | S | REQ (support) | — | P2 | POLISH (optional PDF-ify) |
| Friday FLEX | CURRENT | PDF_CURRENT | S/T | OPT | — | — | KEEP |
| Interactive Science Notebook | RETIRED | NOT_APPLICABLE | S | RETIRED | — (never rebuild) | — | RETIRE |
| **Slide re-sync (future)** | — | NOT_APPLICABLE | T | REQ (after notes) | `10_slide-resync/CH05_GUIDED_NOTES_SLIDE_RESYNC_PROMPT.md` | P1 | `RESYNC_PENDING_GUIDED_NOTES_APPROVAL` |

**Dependency (locked):** Ch5 Guided Notes must be accepted before the Ch5 slide re-sync executes.

---

## Chapter 6 — Energy Transformations + Engineering (Reader pp. 31–36 · TG L12–L13)

**Lifecycle: RELEASED under retired INB architecture → Guided Notes REBUILD required. Chapter 6 is the formal home of transfer/transformation/BOTH (preserved, not removed).**

| Resource | Content | PDF | S/T | Req/Opt | Prompt | Priority | Rec |
|---|---|---|---|---|---|---|---|
| **Guided Notes (student)** | STALE | PDF_NEEDS_REBUILD | S | REQ | `01_guided-notes/CH06_GUIDED_NOTES_STUDENT_BUILD_PROMPT.md` | P0 | REBUILD |
| **Guided Notes Key** | MISSING | PDF_MISSING | T | REQ | `01_guided-notes/CH06_GUIDED_NOTES_KEY_BUILD_PROMPT.md` | P0 | CREATE |
| Engineering Capstone (7pp) + Rubric + Keys + Exemplar | CURRENT | PDF_CURRENT | S/T | REQ (performance) | — | P2 | POLISH (header/badge) |
| Practice + Key | CURRENT | PDF_NEEDS_POLISH | S/T | REQ (ungraded) | — | P2 | POLISH |
| Concept Checkpoint (10 item) + Key | CURRENT | PDF_CURRENT | S/T | REQ (graded) | — | — | KEEP |
| Absent Recovery | CURRENT | **PDF_MISSING (MD-only)** | S | REQ (support) | — | P2 | POLISH (optional PDF-ify) |
| Friday FLEX | CURRENT | PDF_CURRENT | S/T | OPT | — | — | KEEP |
| Interactive Science Notebook | RETIRED | NOT_APPLICABLE | S | RETIRED | — (never rebuild) | — | RETIRE |
| **Slide re-sync (future)** | — | NOT_APPLICABLE | T | REQ (after notes) | `10_slide-resync/CH06_GUIDED_NOTES_SLIDE_RESYNC_PROMPT.md` | P1 | `RESYNC_PENDING_GUIDED_NOTES_APPROVAL` |

**Dependency (locked):** Ch6 Guided Notes must be accepted before the Ch6 slide re-sync executes.

---

## Chapter 7 — Edison + Unit Synthesis (Reader pp. 37–42 · TG Unit Review pp. 94–98)

**Lifecycle: RELEASED under retired INB architecture → Guided Notes REBUILD required. History must be source-derived only.**

| Resource | Content | PDF | S/T | Req/Opt | Prompt | Priority | Rec |
|---|---|---|---|---|---|---|---|
| **Guided Notes (student)** | STALE | PDF_NEEDS_REBUILD | S | REQ | `01_guided-notes/CH07_GUIDED_NOTES_STUDENT_BUILD_PROMPT.md` | P0 | REBUILD |
| **Guided Notes Key** | MISSING | PDF_MISSING | T | REQ | `01_guided-notes/CH07_GUIDED_NOTES_KEY_BUILD_PROMPT.md` | P0 | CREATE |
| Unit Synthesis Review + Key | CURRENT | PDF_CURRENT | S/T | REQ (ungraded) | — | — | KEEP |
| Energy's Big Questions + Key | CURRENT | PDF_CURRENT | S/T | REQ (ungraded) | — | — | KEEP |
| Unit Final (25Q/50pt) + Key + Scoring Guide | CURRENT | PDF_CURRENT | S/T | REQ (graded) | — | — | KEEP |
| Absent + Corrections Recovery | CURRENT | corrections PDF_CURRENT · absent **PDF_MISSING (MD-only)** | S | REQ (support) | — | P2 | POLISH (optional PDF-ify) |
| Friday FLEX (unit close) | CURRENT | PDF_CURRENT | S/T | OPT | — | — | KEEP |
| Interactive Science Notebook | RETIRED | NOT_APPLICABLE | S | RETIRED | — (never rebuild) | — | RETIRE |
| **Slide re-sync (future)** | — | NOT_APPLICABLE | T | REQ (after notes) | `10_slide-resync/CH07_GUIDED_NOTES_SLIDE_RESYNC_PROMPT.md` | P1 | `RESYNC_PENDING_GUIDED_NOTES_APPROVAL` |

**Dependency (locked):** Ch7 Guided Notes must be accepted before the Ch7 slide re-sync executes. The Ch7 chapter manifest's "26 items" final-assessment note is **stale** — the locked standard is **25 Q / 50 pt**; ignore the stale count.

---

## Unit-wide

| Resource | Content | PDF | S/T | Req/Opt | Prompt | Priority | Rec |
|---|---|---|---|---|---|---|---|
| Unit 1 Study Guide + Key | CURRENT | PDF_CURRENT | S/T | REQ (ungraded) | — | — | KEEP |
| Review Game + Scorecards + Guide | CURRENT | PDF_CURRENT (scorecards) · PPTX+MD | S/T | OPT | — | — | KEEP |
| Assessment Blueprint / Trace | CURRENT | NOT_APPLICABLE (MD) | T | REQ (traceability) | — | — | KEEP |
| Assessment Administration Note | CURRENT | NOT_APPLICABLE (MD) | T | REQ | — | — | KEEP |
| **Pom-Pom Launcher (student sheet)** | MISSING | PDF_MISSING | S | REQ (formative) | `05_labs-engineering/UNIT1_POM_POM_LAUNCHER_STUDENT_BUILD_PROMPT.md` | P0 | CREATE |
| **Pom-Pom Launcher (teacher guide)** | MISSING | PDF_MISSING | T | REQ | `05_labs-engineering/UNIT1_POM_POM_LAUNCHER_TEACHER_BUILD_PROMPT.md` | P0 | CREATE |
| Infographics ×6 | CURRENT | PDF_CURRENT (PNG) | T | OPT | — | — | KEEP |
| Teacher Prep Guide / Master Index / Printing | CURRENT | NOT_APPLICABLE (MD) | T | REQ | — | — | KEEP |
| **Guided Notes Architecture Audit** | — | NOT_APPLICABLE | T | — | `UNIT1_GUIDED_NOTES_ARCHITECTURE_AUDIT.md` | — | governing doc |

---

## Redundancy audit — resources that should NOT be rebuilt

| Candidate | Verdict | Reason |
|---|---|---|
| Ch4 "source→path→receiver activity" as separate PDF | REDUNDANT | Served by the 4 investigation worksheets + practice + N2/N4 guided-notes panels. |
| Ch5 "before/after model activity" as separate PDF | REDUNDANT | Served by Crash Lab (before/after) + N2 guided-notes panel. |
| Ch6 "Transfer/Transformation/BOTH sort" as separate PDF | DEFERRED | Served inline by Ch6 practice + N1 three-way panel; a card-sort printable is P2 only. |
| Ch1/Ch2 Guided Notes "rebuild" | NOT REBUILT | FROZEN (rule 80). |
| Interactive Science Notebook (Ch1–7) | RETIRE | Retired architecture; excluded from release. |
| Ch4–7 practice/quiz/lab rebuilds | NOT REBUILT | Source-faithful and standalone; only header/badge polish (P2). |
| Second "notes packet" / recovery-as-full-notes | REDUNDANT | Recovery is 1–2 pages pointing to Guided Notes, never a second notes packet. |
| Ch4 transformation/BOTH content | REMOVED | Belongs to Ch6 (Correction Pass §3). |
| Ch5 mass/weight comparison sublesson | REMOVED from required notes | Deferred to oral/demo enrichment (Correction Pass §4). |

---

## Build order (recommended — Correction Pass §22)

1. **Chapter 4 Guided Notes (student + key)** — P0, candidate pair.
2. **Render + audit Chapter 4 against the architecture audit** — approve the family before proceeding.
3. **Chapter 4 slide re-sync** — execute `CH04_GUIDED_NOTES_SLIDE_RESYNC_PROMPT.md` **only after** the Ch4 notes are accepted.
4. **Then repeat for Ch5, Ch6, Ch7** (notes → approve → slide re-sync), one chapter at a time.
5. **Pom-Pom Launcher (student + teacher guide)** — P0 (independent of notes; can run in parallel).

> **Do NOT proceed to Chapter 5 automatically.** Finish Chapter 4 end-to-end (notes candidate → render → audit → approve architecture → slide re-sync) before starting Chapter 5.

---

## Correction Pass additions (2026-10-09)

1. **Ch4:** removed transformation/BOTH from required content; N-structure now BQ · V1 (energy transfer · sound) · N1 Energy Transfer · N2 Sound+Light · N3 Heat+Electric Current · N4 Finding Evidence of Energy Transfer · CHECK · BQ·NOW I THINK.
2. **Ch5:** removed mass/weight comparison from required content; N-structure now BQ · V1 (collide · collision · sound) · N1 Collisions Cause Changes · N2 Collisions Can Transfer Energy · N3 What Happened to the Energy? · fair-test (same object(s), change speed only) · CHECK · BQ·NOW I THINK.
3. **Teacher keys:** geometry parity preserved (Name/Homeroom kept), non-reflowing `TEACHER KEY` badge, commentary limit with appendix fallback.
4. **Final BQ:** 3–4 ruled lines ≈ 1.15–1.45 in (locked) across Ch4–7.
5. **Ch7 history:** source-derived only; anchored to Reader pp. 38/39/41 (Reader *does* state "did not invent first bulb" and Latimer — preserved accurately, not external correction).
6. **Pom-Pom:** controlled testing-lane framing; allergy-aware balloon note (not "latex-free by default").
7. **PDF status:** content vs printable-PDF axes separated (see index + register tables).
8. **Slide re-sync:** 4 future prompts created; decks marked `RESYNC_PENDING_GUIDED_NOTES_APPROVAL`.
9. **Architecture audit:** `UNIT1_GUIDED_NOTES_ARCHITECTURE_AUDIT.md` created.

---

## Remaining conflicts (unresolved — must be decided before build)

1. **Ch5 mass/weight scope vs. Reader/TG.** Reader p.30 ("Weight Affects the Changes Caused by Collisions") and TG L10's weight demo *do* teach mass/weight. The corrected Ch5 notes defer it (oral/demo enrichment only), but the existing **Crash Lab has Part B (mass/weight)** as a required investigation. This is a real tension: either (a) keep Crash Lab Part B as an *optional/demo* extension (aligning with the corrected notes), or (b) flag Crash Lab for assessment/spec review. **Decision needed.**
2. **Ch4 final-assessment Q20 ("Both transfer and transformation").** This unit-final item references transformation (Ch6). It is fine at unit level (Ch6 taught before the final), but it confirms Ch4 notes must not pre-teach transformation. No Ch4 notes change required; no blueprint change required — but flag for the record.
3. **Slide decks Ch4–7 still anchor to the retired INB.** Resolved by the re-sync prompts (pending notes approval) — not a source conflict, but a sequencing dependency.
4. **Page counts.** The old "frozen page count" guidance (Ch4=4pp etc.) is now a **target**, not locked. No production decision locks these counts today; flag for the owner if a hard count is desired.
5. **Stale "26 items" in the Ch7 chapter manifest.** The locked standard is 25 Q / 50 pt; the Ch7 manifest is stale and should be corrected in a later phase (not in this prompt-library pass).

---

## Boundary (enforced)

- **DO NOT build PDFs/DOCX** in this pass.
- **DO NOT overwrite canonical artifacts** (especially frozen Ch1/Ch2).
- **DO NOT alter frozen Ch1/Ch2 artifacts, certify Ch3, or change assessment files.**
- **DO NOT commit or push.**
