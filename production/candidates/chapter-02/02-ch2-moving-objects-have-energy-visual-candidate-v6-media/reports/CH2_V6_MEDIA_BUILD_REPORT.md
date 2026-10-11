# Chapter 2 v6-media Build Report — Moving Objects Have Energy

## Deliverable
`production/candidates/chapter-02/02-ch2-moving-objects-have-energy-visual-candidate-v6-media/`

## What was produced
- **Editable PPTX** (`…-v6-media.pptx`, 49 slides, 16:9) — v5 visual candidate + 2 embedded videos.
- **PDF backup** (`…-v6-media.pdf`).
- **49 rendered PNG previews** (`previews/`).
- **Contact sheet** (`contact-sheet.png`).
- **Media** (`media/`): 2 embedded clips + 1 optional clip + 3 full-source fallbacks + posters.
- **Reports** (`reports/`): content QA, visual QA (deterministic + rendered-layout),
  video audit, media playback verification, classroom simulation, gold readiness,
  slide-to-notes alignment contract (md + json), slide manifest (json).
- **SHA-256 manifest** (`SHA256_MANIFEST.json`, 61 files).

## Videos (Gate B)
- VIDEO A — Marble Collision → slide 6 (embedded, poster, teacher-controlled).
- VIDEO B — Motion in Action → slide 15 (embedded, poster, teacher-controlled).
- VIDEO C — Things on the Move (pendulum/wind) → standalone fallback (documented).

## Gates
- **Gate A (source/content authority):** PASS — anchors mirror the FROZEN Guided Notes
  key exactly; deterministic content QA PASS.
- **Gate B (video selection):** DONE — metadata verified; selection recorded; content
  verification boundary documented (see `VIDEO_AUDIT_AND_SELECTION.md`).
- **Gate C (premium build):** DONE — editable deck + embedded videos + PDF + PNGs.
- **Gate D (full QA):** DONE at mechanical + deterministic level; independent visual +
  source review still required (see `GOLD_READINESS.md`).
- **Gate E (release acceptance):** NOT ISSUED — Release Judge + external audit pending.

## Governance
- No frozen bytes modified. No commit/push performed. New candidate only.
- No visible-desktop GUI used (QA-isolation rule honored).
