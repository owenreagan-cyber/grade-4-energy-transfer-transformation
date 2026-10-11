# CHAPTER 2 — MEDIA SHORTLIST & INTEGRATION PLAN

> External-video discovery + Chapter 2 slide audit. Date: 2026-10-10.
> **No teaching presentation was modified and no approved media was replaced.** This is a shortlist + plan only; changes await owner authorization.

## 1. Audit — what is embedded today

### Canonical deck (repo source of truth)
`production/slides/02-ch2-moving-objects-have-energy-slides.pptx` — **no videos embedded** (empty `ppt/media/`).

### v6-media candidate (NOT yet promoted)
`production/candidates/chapter-02/02-ch2-moving-objects-have-energy-visual-candidate-v6-media/…-v6-media.pptx` (49 slides) — 2 embedded clips, teacher-controlled (`p14:media`, no autoplay):

| Video | Project name | Slide | Embedded | Clip |
|---|---|---|---|---|
| VIDEO A | Marble Collision | 6 (`CH2-S06-MEDIA`, media-shell) | ✅ EMBEDDED | `video1.mp4` 40 s |
| VIDEO B | Motion in Action | 15 (`CH2-S15-BASKETBALL`) | ✅ EMBEDDED | `video2.mp4` 40 s |
| VIDEO C | Things on the Move | — (no shell) | ❌ NOT EMBEDDED | `ch2-videoC-things-on-the-move.mp4` 40 s standalone fallback |

> **Answer to the audit question:** Marble Collision = embedded (slide 6) · Motion in Action = embedded (slide 15) · Things on the Move = **not** embedded (standalone fallback only). Embedding exists only in the v6-media **candidate**; the canonical deck has none.

### Google Slides (native teaching format)
Owner Google Drive pointers exist (`assets/supplemental/external-reference/*.gslides`), e.g. "Presentation Slides" `doc_id=1QtBku__MFLDuSMPjkYJBdK1115f88v8pPZFsJNbs4Ds`. **Live verification of the Google Slides deck could not be performed** — the Google Drive connector (`plugin-google-drive-google-drive`) times out on connection. This plan is therefore grounded in the repository (canonical) plus web search; Google Slides embedding must be re-checked by the owner or once the connector is reachable.

## 2. External discovery (web search, 2026-10-10)

Discovery method: web search (no YouTube Data API key; captions/transcripts and live playback not independently verified this run). Candidates evaluated against CKSci Reader Ch.2 (pp. 7–12) + TG L3 and the locked anchors (motion · energy of motion · moving object → change → evidence · hammer/pendulum/wind).

| Publisher | Title | URL / ID | Dur | Fit for Ch.2? | Verdict |
|---|---|---|---|---|---|
| Generation Genius | Energy Transfer (3–5) | generationgenius.com/videolessons/energy-transfer-video-for-kids | ~12 min | ⚠️ "chemical/electrical/motion energy", generator, transfer → Ch.4 scope | **REJECT for Ch.2** (candidate Ch.4) |
| Generation Genius | Collisions Energy Transfer (3–5) | generationgenius.com/videolessons/collisions-video-for-kids | ~12 min | ⚠️ "collision/transfer", "faster/heavier = more energy" → Ch.3/Ch.5 scope | **REJECT for Ch.2** (candidate Ch.5) |
| PBS LearningMedia (WGBH) | Energy in Moving Objects | lsintspl3.wgbh.org/en-us/lesson/midlit11-sci-splenergy/2 | short | ❌ "mechanical energy" — forbidden vocabulary | **REJECT** |
| PBS LearningMedia | Roller Coaster Design | pbslearningmedia.org/resource/midlit11.sci.phys.maf.energy/roller-coaster-design | — | ❌ "potential/kinetic" — forbidden | **REJECT** |
| Smithsonian SSEC | Motion Energy Video (module) | ssec.si.edu/collisions | — | ✅ "moving objects = energy"; but module access + "motion energy" vs "energy of motion" | **CANDIDATE** (needs access + timestamp) |
| Mystery Science | How can marbles save the world? | mysteryscience.com/energy/mystery-3/collisions-energy-transfer/963 | full lesson | ⚠️ collision/transfer + speed → Ch.5; not a standalone embeddable clip | **REJECT for Ch.2** (Ch.5 EXTENSION reference) |
| NASA Johnson | STEMonstrations Kinetic & Potential Energy | youtube.com/watch?v=OpxGp2P48kI | 2:49 | ❌ "kinetic/potential/gravitational" — forbidden | **REJECT** |

**Headline finding:** no external candidate matches the project's own Chapter 2 clips on vocabulary fidelity. External "energy" videos consistently use `kinetic/potential/mechanical` (forbidden) or drift into Ch.3 (speed) / Ch.4 (transfer) / Ch.5 (collision) scope. This supports the rule: **do not replace approved project clips merely because an external option is newer.**

## 3. Recommended media selections (Ch.2)

| # | Slot | Source | Selection | Duration | Status |
|---|---|---|---|---|---|
| 1 | Slide 6 — Marble Collision (phenomenon) | Project-authored | `Marble_Collisions__Investigating_Motion_Energy.mp4` → 40 s clip (VIDEO A) | 40 s | **KEEP (embedded)** |
| 2 | Slide 15 — Motion in Action (application) | Project-authored | `Ch_2__Motion_Energy_in_Action.mp4` → 40 s clip (VIDEO B) | 40 s | **KEEP (embedded)** |
| 3 | N3 — hammer/pendulum/wind (useful motion) | Project-authored | `Things_on_the_Move.mp4` 40 s clip (VIDEO C) | 40 s | **OPTIONAL fallback** (not embedded; no clean shell on slide 23) |
| 4 | Extension/FLEX (optional) | Project-authored | `How_Motion_Proves_Energy_Exists.mp4` (1:12) / `How_We_See_Invisible_Energy_of_Motion.mp4` (1:03) | ≤1:12 | **FLEX** |

External additions recommended: **none for Ch.2 core** at this time. Smithsonian "Motion Energy Video" is the only external CANDIDATE worth a follow-up (for a real-world "moving objects = energy" montage), pending module access + a vocabulary/timestamp check.

## 4. Integration plan (Google Slides media-slide spec)

Each selected video gets a dedicated media slide, inserted **after** its teaching anchor without reordering existing slides. Template:

- **Introduction** (1–2 lines): set context.
- **Find Out / Follow Along question**: one observable-focus question read before playback.
- **Embed** (or verified playback link) at correct 16:9 aspect, poster frame, no autoplay (teacher-clicked).
- **Teacher note** (speaker note): follow-up discussion question + fallback.

Ch.2 concrete slots:
- **Slide 6 media** — intro: "A moving marble meets a still marble." · Find Out: "What changed for the still marble?" · note: "What is the evidence the moving marble had energy?"
- **Slide 15 media** — intro: "A basketball in motion reaches the net." · Follow Along: "What change does the moving ball cause?" · note: "Name the change; connect to energy of motion."
- **Slide 23 (N3) optional** — Things on the Move: pendulum/wind. Follow Along: "Which object is moving? What change could it cause?" · note: maps hammer/pendulum/wind to their useful change.

## 5. Fallback & reliability (mandatory)

- Never make external/embedded playback the only route to a required concept. Fallback for every slot = **live demo / still image / oral re-teach** (marble collision = classroom marble demo; N3 = three still images already on slide 23).
- Total Ch.2 video budget ≤ ~2–3 min (two 40 s clips + optional 40 s), well within the 30-min period after recess-return, Reader handling, discussion, cleanup.
- Recheck links + embeddability before each classroom use; verify native playback on the iPad Pro before first use (isolated/Simulator or owner-approved bounded live test — not performed this run).

## 6. Authorization gate

No deck edit, no media replacement, no promotion of the v6-media candidate until the owner reviews this shortlist and authorizes changes. Canonical deck and frozen Ch.2 notes (`CH2_GOLD_STANDARD_FREEZE.md`, v1.0) remain untouched.
