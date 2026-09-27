# CH1 NOTE-FORMAT COMPARISON — CONTENT EQUIVALENCE

> Part D. Controlled-comparison check: the INB and Guided Notes must teach the **same** content so the comparison isolates note format, not content quality. Method: deterministic text extraction (`tools/qa_ch1_notes.py`) from both DOCX masters (recursive paragraph + nested-table extraction).

## Concept coverage

| Concept | INB | Guided Notes |
|---|---|---|
| energy | PRESENT (definition fill-in, Insert 1) | PRESENT (definition fill-in, Page 1) |
| change | PRESENT (definition fill-in, Insert 1) | PRESENT (definition fill-in, Page 1) |
| evidence | PRESENT (definition fill-in, Insert 1) | PRESENT (definition fill-in, Page 1) |
| ENERGY → CHANGE → EVIDENCE | PRESENT (3-box model, Inserts 1 & 3) | PRESENT (3-box model, Pages 1 & 3) |
| motion | PRESENT (memory cue, Insert 1) | PRESENT (forms section, Page 1) |
| light | PRESENT (memory cue, Insert 1) | PRESENT (forms section, Page 1) |
| sound | PRESENT (memory cue, Insert 1) | PRESENT (forms section, Page 1) |
| heat | PRESENT (memory cue, Insert 1) | PRESENT (forms section, Page 1) |
| electrical | PRESENT (memory cue, Insert 1) | PRESENT (forms section, Page 1) |
| stored energy | PRESENT (Insert 2) | PRESENT (Page 2) |
| battery | PRESENT (example, Insert 2) | PRESENT (example, Page 2) |
| stretched (rubber) band | PRESENT (example, Insert 2) | PRESENT (example, Page 2) |
| raised object | PRESENT (example, Insert 2) | PRESENT (example, Page 2) |
| observation | PRESENT ("Observation = what I see", Insert 3) | PRESENT ("Observation = what I see", Page 2) |
| explanation | PRESENT ("Explanation = what it means", Insert 3) | PRESENT ("Explanation = what it means", Page 2) |

## Result

- INB missing concepts: **none**
- Guided Notes missing concepts: **none**

**Content Equivalence: PASS** — all 15 concepts present in both formats, in the same sequence (energy → change → evidence → model → forms → stored energy → observation/explanation → synthesis).

## Scope notes
- Both formats use identical fill-in stems for the three core definitions ("Energy is the ability to cause ____.", "Change means something becomes ____.", "Evidence is something we observe that helps us ____ what happened.").
- Both use identical stored-energy examples (battery, stretched rubber band, raised object) with the same "what change could happen later?" prompt.
- Both use identical forms-of-energy memory cues (motion/light/sound/heat/electrical with rolling/bright/loud/warm/powers).
- The only differences are format-level (trim/glue/fold for INB; no assembly for Guided Notes), not content-level.
