# CH1 45-SLIDE REBUILD SPEC

Phase 5A. Implementation-ready reconstruction spec, keyed to the **canonical frozen 45-slide
sequence** (Decision A). Machine-readable twin: `CH1_45_SLIDE_SPEC.json`. All text is editable PPTX.
Raster assets = provisional defaults (see `CH1_PREMIUM_VISUAL_SELECTIONS.md`); subjective picks are
`VISUAL_REVIEW_REQUIRED`.

Legend — Sess/Status: S1/S2/S3 = session, REQ/OPT. Constructor = canonical builder helper(s).
Asset IDs reference `CH1_PREMIUM_VISUAL_SELECTIONS.md`.

| # | Sess/Status | Title / purpose | Anchor | Constructor | Asset (provisional) | Student behavior | Reveal / media | Risk → check |
|---|---|---|---|---|---|---|---|---|
| 1 | S1 REQ | Energy Causes Change (opener) | — | `title` | R01-opener full-bleed | orient | — | baked title → none; 16:9 render |
| 2 | S1 REQ | Big Question | BQ | `header`+BQ banner | — (deterministic) | turn & talk | do not answer BQ | exact BQ text |
| 3 | S1 REQ | Big Question — My first thinking | BQ·WRITE | `notes_heading`+`write_line` | — | write 1–2 ideas | no answer | no leak |
| 4 | S1 OPT | What changed? (dark→bright) | — | `header`+`before_after` | R02-darkbright | observe | — | matched pair |
| 5 | S1 OPT | I notice… I wonder… | — | two cards | R02 halves | share notice/wonder | — | same crops |
| 6 | S1 REQ | Electric Pencil Sharpener (BEFORE) | — | `header`+card | R03 before-half | observe pencil | — | matched object |
| 7 | S1 REQ | Predict: what will change? | — | `header`+stem | — | predict aloud | — | no cue |
| 8 | S1 REQ | What changed? (evidence) | — | `header`+`before_after`+CHANGES | R03 full pair | name changes | record 3 changes | no media shell |
| 9 | S1 REQ | How do we know energy was involved? | — | `header`+`model_strip` | — | explain | keep `?` open | model + conclusion |
| 10 | S1 REQ | Vocabulary — Energy & Change | V1 | 2×`vocab_card` | R04-energy + R05-change | recite | full defs shown | both terms+defs |
| 11 | S1 REQ | Vocabulary — Energy & Change (write) | V1·WRITE | `notes_heading`+blanks | — | fill `change`/`different` | after write | no leak |
| 12 | S1 REQ | Vocabulary — Energy & Change (check) | V1·CHECK | same as 11 | — | check | reveal gold | geometry parity |
| 13 | S1 REQ | What is energy? (RECITE) | — | `header`+recite card | — | recite together | — | exact line |
| 14 | S1 REQ | Look at the seashore | — | `header`+`model_strip` | R06-seashore | read + discuss | `?` stays open | model overlay |
| 15 | S1 REQ | Energy Causes Change (write) | N1·WRITE | `notes_heading`+blank+model | — | fill `evidence`; last box empty | after write | no leak |
| 16 | S1 REQ | Energy Causes Change (check) | N1·CHECK | same + full model | — | copy into last box | reveal `EVIDENCE` | full model |
| 17 | S2 REQ | Energy has different forms | N2 | 5 chips + strip | R07-forms-strip | name forms | motion modeled only | forms text |
| 18 | S2 OPT | Clap three times | — | `header`+card | — | clap + observe | students name forms | optional |
| 19 | S2 REQ | Energy Occurs in Different Forms (write) | N2·WRITE | `notes_heading`+5-row table | — | write one example each | no answer slide | no pre-fill |
| 20 | S2 REQ | Vocabulary — Stored Energy | V2 | `vocab_card` | R08-stored | recite | full def | term+def |
| 21 | S2 REQ | Vocabulary — Stored Energy (write) | V2·WRITE | `notes_heading`+blank | — | fill `later` | after write | no leak |
| 22 | S2 REQ | Vocabulary — Stored Energy (check) | V2·CHECK | same as 21 | — | check | reveal `later` | geometry parity |
| 23 | S2 REQ | Does a still battery have energy? | N3 | `header`+predict card | R09 battery crop | predict yes/no | read battery fact after | predict-first |
| 24 | S2 REQ | The stored energy of position | N3 | `header`+gold card | R09 apple crop | discuss position | — | "position" taught |
| 25 | S2 REQ | Stored energy can cause a change later | N3 | `header`+`model_strip` | R09 rubber crop | trace model | battery fact | model shapes |
| 26 | S2 REQ | Objects Can Store Energy (write) | N3·WRITE | `notes_heading`+model+table+blank | — | fill `position` | after write | no leak |
| 27 | S2 REQ | Objects Can Store Energy (check) | N3·CHECK | same as 26 | — | check | reveal `position`+samples | geometry parity |
| 28 | S3 REQ | Recognizing evidence | N4 | `header`+navy card | R10-evidence | name clues | no CHECK answer yet | no mechanism art |
| 29 | S3 REQ | Recognizing Evidence (draw) | N4·DRAW | `notes_heading`+`before_after` | — | draw before/after | — | no "ENERGY ACTS" |
| 30 | S3 REQ | Check Your Thinking (write) | CHECK·WRITE | `notes_heading`+starter+lines | — | complete starter | after write | no leak |
| 31 | S3 REQ | We know because we see a change | CHECK·REVEAL | sample card | — | — | reveal sample | geometry parity |
| 32 | S3 OPT | Which change shows energy at work? | — | 3 scenario cards | — | pick + partner | spoken rule after vote | 3 scenarios |
| 33 | S3 REQ | BQ · Now I Think | BQ·NOW I THINK | `notes_heading`+BQ banner+lines | R11-reflection subdued | write answer | — | BQ text |
| 34 | OPT | Review 1 — concept | — | `review_question` | — | vote | — | verbatim |
| 35 | OPT | Review 1 — answer | — | `review_answer` | — | — | reveal C | highlight C |
| 36 | OPT | Review 2 — visual | — | `review_question`+photo | R03 pencil | vote | — | verbatim |
| 37 | OPT | Review 2 — answer | — | `review_answer` | same as 36 | — | reveal A | highlight A |
| 38 | OPT | Review 3 — scenario | — | `review_question`+photo | R08 rubber | vote | — | verbatim |
| 39 | OPT | Review 3 — answer | — | `review_answer` | same as 38 | — | reveal D | highlight D |
| 40 | OPT | Review 4 — comparison | — | `review_question` | — | vote | — | verbatim |
| 41 | OPT | Review 4 — answer | — | `review_answer` | — | — | reveal B | highlight B |
| 42 | OPT | Review 5 — concept | — | `review_question` | — | vote | — | verbatim |
| 43 | OPT | Review 5 — answer | — | `review_answer` | — | — | reveal A | highlight A |
| 44 | OPT | Review 6 — scenario | — | `review_question`+photo | R09 battery | vote | — | verbatim |
| 45 | OPT | Review 6 — answer + close | — | `review_answer`+close | R12-close | — | reveal C + close model | highlight C + `ENERGY→CHANGE→EVIDENCE` |

## Per-anchor write/reveal parity (explicit)

- 11↔12 (V1), 15↔16 (N1), 21↔22 (V2), 26↔27 (N3), 30↔31 (CHECK) share identical geometry; reveal
  only the answer in gold.
- 3, 19, 29, 33 are open writes (no canonical reveal slide). 19 (N2) has no answer slide per
  `tools/build_ch1_slides.py` note.

## Review verbatim (locked; from canonical deck)

Q1=C · Q2=A · Q3=D · Q4=B · Q5=A · Q6=C. Exact question/option/rationale text is in
`tools/build_ch1_slides.py` `REVIEW` list and is not paraphrased.

## Acceptance checks (every slide)

render OK · 16:9 · no clip/overflow · body ≥ 28 pt (tables ≥ 24) · Georgia+Avenir Next present · no
answer leakage on WRITE · reveal follows write · no out-of-scope vocab (kinetic/potential/mechanical/
radiant/gravitational/inertia/momentum/compression-wave) · notes-mapped slides mirror Guided Notes ·
grayscale-safe.
