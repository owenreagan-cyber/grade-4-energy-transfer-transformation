# Chapter 1 — Phase 5C Asset Selections

Every photo is a Phase 5A selection (R-id) or a Phase 5A-listed alternative for that R-id
(`qa/reports/ch1-phase5a/CH1_PREMIUM_VISUAL_SELECTIONS.md`). No image was generated, edited, or newly introduced.
Exact placements, crop boxes, focus points, staged crops and SHA-256 hashes (source and staged) are in
`production/candidates/chapter-01/ch1-premium-hybrid-v2/CANDIDATE_ASSET_MANIFEST.json` (27 placements).
5A treated choosing an alternative after vision review as the intended process ("replaced if vision review picks an
alternative"); the owner should still confirm.

| Key | Source | 5A status | Used on | Why |
|---|---|---|---|---|
| opener | `assets/ch1/candidate-v2/slide-01-opener.png` | R01 default | 1 | text-free lamp-lit desk; fills the right region |
| dark / bright | `…/slide-04-dark-bright.png` halves | R02 default | 4, 33 | true matched pair (same desk, light off/on) |
| pen_before / pen_after | `…/slide-09-pencil-before-after.png` halves | R03 default | 6, 8, 10, 33, 36, 37 | matched pair; shavings visible after |
| energy | `…/slide-10-energy.png` | R04 default | 10 | a push sets a toy car moving |
| seashore | `…/slide-14-seashore.png` | R06 default | 14, 33 | waves breaking on sand |
| f_motion, f_sound, f_light, f_heat, f_elec | `source-intake/…/ch1-forms-motion-03, sound-02, light-01, heat-01, electrical-01.jpg` | R07 **alternates** | 17 | one consistent studio series, 1440–1536px (strip crops would be 434px wide); motion-blurred ball conveys movement |
| stored_hero | `…/slide-22-stored-energy.png` | R08 default | 20 | stretched band held still |
| rubber | `…/ch1-voc-stored-energy-01.jpg` | R08 **alternate** | 25, 33 | 1920px; band clearly stretched |
| battery | `…/ch1-stored-battery-01.jpg` | R09 **alternate** | 23 | batteries visible inside the flashlight; nothing glowing |
| apple | `…/ch1-stored-raised-apple-01.jpg` | R09 **alternate** | 24 | apple held high with the table far below; position unambiguous |
| ev_light / ev_pencil | `…/slide-28-evidence.png` panels 1–2 | R10 default | 28 | changes already observed in Session 1 |

Not used: R11 `slide-33-reflection.png` and R12 `slide-45-close.png` (the evidence wall replaced R11 on 33; 45 is a review
reveal). The `science-chapter-opener.jpg` (baked text) and `slide-06-pencil-before.png` (5A-disqualified) remain unused.
Slide 14: an approved seashore asset exists, so **NEW_ASSET_RECOMMENDED is not raised**.

## Unresolved visual / instructional decisions (owner)
| ID | Slide | Question | Default chosen |
|---|---|---|---|
| D1 | 20 | The teacher note says "Save examples for slide 23", but the prompt asks for a stored-energy photo. Keep the stretched-band photo, or revert to card-only? | photo kept (5A R08 assigned to slide 20) |
| D2 | 28 | The lamp and shavings photos resemble the slide 31 sample answer ("…a light turning on"). They are Session 1 phenomena, so this is recall rather than new answers. Accept, or use one photo / none? | accept, unlabeled |
| D3 | 6, 8 | In the approved R03 "BEFORE" photo the pencil tip looks fairly pointed, but the canonical text says "tip is flat". | **NEW_ASSET_RECOMMENDED** (owner decision; not generated) |
| D4 | 4, 8, 13, 14, 17, 23–25, 28 | Canonical text stores line breaks as literal LF inside `<a:t>`. LibreOffice renders them unevenly when centred; PowerPoint behaviour unverified. Converting to `<a:br/>` needs the parity tool to normalise whitespace. | unchanged (canonical encoding) |
| D5 | 17, 23, 24, 25, 33 | Confirm the promotion of the 5A-listed alternates above. | promoted |
| D6 | 33 | The 4-photo evidence wall recalls the phenomena. Confirm it does not over-cue the student's reflection. | kept, no captions |
| D7 | 44/45 | Review 6 is in the grid family; the photo variant was rejected (P-7). | grid |
