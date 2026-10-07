# Grade 4 Student Prompt Standard

Student difficulty must come from the **science**, not from guessing what a
question means. A prompt that is readable but vague about what the student should
look at, name, or do is a product defect, not a difficulty feature.

This standard governs every student-facing prompt in guided notes, practice,
quizzes/tests, labs/investigations, recovery, and study guides. It is enforced by
the `STUDENT_PROMPT_CLARITY` gate (mandatory for chapter certification).

## Core rule

A required answer must be reachable from taught content or supplied evidence, and
the prompt must name the object, data, diagram, observation, table, graph, or text
the student should use.

## Rules

1. **One identifiable task at a time.** Do not fold multiple reasoning steps into
   one question.
2. **Name the referent.** Tell the student the object, data, diagram, observation,
   table, graph, or text to use.
3. **Prefer plain verbs.** Avoid unsupported task vocabulary ("infer", "evaluate",
   "analyze") when simpler language ("what changed", "which was bigger", "how do
   you know") expresses the same reasoning.
4. **No vague referents.** Do not use "that change", "these results", "what
   happened", "the relationship", "use evidence" unless the referent is explicit in
   the same prompt or the immediately preceding sentence.
5. **Teach before you ask.** A required science fact must be taught (or supplied as
   given text) before students are asked to apply it.
6. **Reachable answers.** The required answer must be reachable from taught or
   supplied evidence. A key containing the answer does not prove the prompt gave
   enough to derive it.
7. **Guided reasoning before independent transfer.** Lead students through reading
   and comparing their data before asking for an open conclusion.
8. **At most one final extension item** per artifact; it may transfer thinking but
   may not depend on untaught core content.
9. **No accidental reading test.** Academic task vocabulary must not turn a science
   question into a vocabulary puzzle.

## Prompt classification

Every prompt is classified by the gate into exactly one of:

| Class | Meaning | Requirement |
|---|---|---|
| `RECALL` | Remember a taught fact | fact must be taught |
| `IDENTIFY` | Name the object/part/feature | object must be named or visible |
| `OBSERVE` | Report what happened | observation must be supplied or performed |
| `READ_DATA` | Read a value from data/table/graph | must name the data/table/graph and the cell/axis |
| `COMPARE` | Compare two things | must name both things compared |
| `CALCULATE` | Compute (average, sum) | must name the values/column |
| `CONNECT` | Relate two taught ideas | both ideas must be taught |
| `EXPLAIN` | Explain a result/phenomenon | must identify the result/phenomenon |
| `CLAIM_EVIDENCE` | State a claim + cite evidence | must point at actual available evidence |
| `EXTEND` | Transfer thinking | at most one; no untaught core content |

## Vagueness rules (fail)

A prompt FAILS when it is vague about what to use:

- `READ_DATA` without naming the table/graph/axis/values to read.
- `COMPARE` without naming both things compared.
- `EXPLAIN` without identifying the result/phenomenon.
- `CLAIM_EVIDENCE` without pointing at actual available evidence.
- Any "infer the relationship" / "what does this show?" / "explain why." with no
  explicit referent.
- A claim prompt placed before the required science/data is taught or supplied.

## Negative fixtures (must FAIL the gate)

- "Use evidence." (no named evidence)
- "Infer the relationship." (vague referent + unsupported verb)
- "What does this show?" (ambiguous referent)
- "Explain why." (no identified claim/result)
- A claim prompt before the required science/data.
- A data question with no named table/values.

## Positive fixtures (must PASS the gate)

- A guided compare prompt naming two columns.
- A claim/evidence prompt pointing at actual averages.
- One final transfer question after guided reasoning.
