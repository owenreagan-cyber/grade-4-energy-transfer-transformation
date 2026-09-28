# PHASE 13I — Video Production Specs (Optional Media Gaps)

> Hand-off document for NotebookLM / Canva / another generator / a human editor.
> Three optional scripts close the three remaining media gaps from Phase 13H.
> **No video is generated in this repo phase** — these specs are the deliverable.

---

## Shared production standard (all three videos)

| Attribute | Standard |
|---|---|
| Grade | 4 |
| Tone | clear · visual · calm · curious · scientific |
| Narration pace | ~110–135 wpm (conversational, no rush) |
| On-screen text | 3–8 words per label; never full narration paragraphs |
| Visual style | realistic imagery + simple diagrams + arrows + restrained animation; strong contrast; large labels; uncluttered frames |
| Scene density | one idea per scene |
| Ending | brief student question (turn-and-talk, no narration) |
| Voice | neutral; avoid "obviously", "simply", "everyone knows", filler |

### Visual direction — avoid
cartoon clip-art · futuristic grid graphics · political imagery · dramatic disaster footage · smokestack montage as moral framing · protest imagery · climate graphics · financial/economic charts

---

## Video 1 — Where Does Our Energy Come From?

| Field | Value |
|---|---|
| File | `01-where-does-our-energy-come-from-final-script.md` |
| Runtime target | 75–100 s |
| Scene count | 6 |
| Narration (master) | ~135 words |
| Required vocabulary | renewable · nonrenewable · resource · benefit · limitation · energy |
| Forbidden | carbon emissions · zero carbon · clean/dirty energy · climate · grid · national percentages · advocacy |
| Final question | "How are renewable and nonrenewable resources different?" |
| Placement | Week 5 Monday · SUPPORT / OPTIONAL · Unit 2 launch |

**Scene map:** Hook → Natural Resources → Nonrenewable → Renewable → Abundant≠renewable / renewable≠available → Unit question.

---

## Video 2 — Coal vs Nuclear: Different Heat Sources, Similar Power-Plant Pathway

| Field | Value |
|---|---|
| File | `04-coal-vs-nuclear-final-script.md` |
| Runtime target | 75–100 s |
| Scene count | 6 |
| Narration (master) | ~135 words |
| Required vocabulary | heat · steam · turbine · generator · electricity · pathway · source |
| Forbidden | U-235 · fission equations · atomic diagrams · radiation mechanics · kinetic/chemical/mechanical/thermal-energy labels · zero-emissions · policy comparison · "which is better?" |
| Final question | "What stays the same? What changes?" |
| Placement | Week 6 Thursday · SUPPORT / OPTIONAL · SAME/DIFFERENT model |

**Scene map:** Side-by-side hook → Coal pathway → Nuclear pathway → SAME → DIFFERENT → Think.

**Key visual device:** two identical icon chains; only the first icon (heat source) differs. This makes SAME/DIFFERENT self-evident without extra words.

---

## Video 3 — Sunlight & Earth Heat: Solar and Geothermal Energy

| Field | Value |
|---|---|
| File | `07-solar-geothermal-final-script.md` |
| Runtime target | 100–140 s |
| Scene count | 7 |
| Narration (master) | ~140 words |
| Required vocabulary | sunlight · solar cell · electricity · heat · renewable · location · available light |
| Forbidden | photons · electrons · semiconductors · electron excitation · zero emissions · zero carbon · climate · clean-energy advocacy · battery-required claims · deep steam-pressure engineering |
| Final question | "What condition matters most for each resource?" |
| Placement | Week 8 Tuesday (preferred) · SUPPORT / OPTIONAL · compare/contrast |

**Scene map:** Two sources → Solar → Solar limitation → Geothermal → Location → Compare → Think.

**Key visual device:** two-column compare card — `SOLAR: depends on available sunlight` vs `GEOTHERMAL: depends on suitable underground heat`.

---

## Hand-off checklist (before generation)

- [ ] Verify narration word counts against runtime targets (~110–135 wpm).
- [ ] Verify on-screen text ≤ 8 words per label.
- [ ] Run the guardrail scan (below) against the finalized narration transcript.
- [ ] Confirm no forbidden terms survived the voice-over.
- [ ] Confirm each video ends on a student question, not a lecture summary.
- [ ] Confirm final cut is a single contiguous piece (no stitched edits needed).

## Guardrail scan target (expected: zero unresolved hits)

Science terms: `proof` `proves` `kinetic` `potential` `mechanical energy` `chemical energy` `thermal energy` `radiant` `momentum` `impulse` `electron` `photon` `charged particle` `compression wave` `base-load` `peak demand` `grid stabilization` `fission` `U-235`

Climate/boundary terms: `climate change` `global warming` `carbon` `zero carbon` `carbon footprint` `climate crisis` `climate activism` `save the planet` `energy policy` `carbon tax` `cap and trade`

## Source alignment

- **V1** ↔ Reader Ch1 (renewable/nonrenewable definitions, "restored more quickly than it is used up", "abundant ≠ renewable"); guided notes Ch1 p.1; slides `01-u2-ch1` S1–S6.
- **V2** ↔ Reader Ch3 + Ch4 (burn → heat → steam → turbine → generator; nuclear heat source); guided notes Ch3 p.2 + Ch4 p.1; slides `03-u2-ch3` S5, `04-u2-ch4` S4–S6. Fission detail is **not** required (Reader Ch4 states "splitting of atoms" — intentionally NOT narrated here per locked language).
- **V3** ↔ Reader Ch7 + Ch8 (solar cell converts sunlight to electricity; available light; geothermal heat from Earth's interior; location); guided notes Ch7 p.1–2 + Ch8 p.1; slides `07-u2-ch7` S1–S8, `08-u2-ch8` S1–S8.
