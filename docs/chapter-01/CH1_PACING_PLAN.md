# Chapter 1 — Authoritative Pacing Plan (v1.1)

> **This is the ONE Chapter 1 timing system.** The Teacher Playbook, `UNIT1_PACING_CALENDAR.md`, `MASTER_CURRICULUM_MAP.md`, the package manifest, the slide speaker notes (TIME / PLAN lines) and QA are all derived from `tools/ch1_pacing.py` and checked against it. Do not create another. Regenerate with `.venv/bin/python tools/gen_ch1_pacing_plan.py`.

## Design rules

- **30-minute block**, ~3–5 min lost to transitions → every session plans **≤ 25 required minutes** (≥ 5 min buffer). Required minutes are shown in the tables below.
- **Three instructional sessions**: Mon 10/12 · Tue 10/13 · Fri 10/16. **Wed 10/14 and Thu 10/15 belong to Chapter 2** (unit calendar). Chapter 1 does not borrow them.
- **Friday policy (owner decision, 2026-10-04):** Friday may hold catch-up, review, completion of previously taught work, BQ reflection/synthesis, scored quizzes, makeup work and optional FLEX; it is **never the first instructional exposure** to essential new core content. All Ch1 concepts, vocabulary (V1, V2) and models (N1–N3) are taught Mon–Tue. Session 3 = recognise (N4, synthesis of content already taught), reflect (CHECK, BQ return) and the **scored quiz**. Traceability for each Friday slide is in `tools/ch1_pacing.py::FRIDAY_DEPENDS` and gated by `check_plan()`.
- **No session starts on a reveal/answer slide.** Session 1 opens on slide 1 (title); Sessions 2 and 3 open on slide 2 (Big Question re-entry).
- **Every required notes page has a named slot**: p. 1 → Session 1 · p. 2 → Session 2 · p. 3 → Session 3. **Every scored artifact has a named slot**: quiz → Session 3, minutes 12–25 (handed out no later than minute 12).
- Practice page: ungraded, NOT on any session's critical path. Assign after Session 2 as take-home or any spare 12-minute window (or a Friday FLEX PRACTICE slot). Recommended before the Friday quiz.
- **Energy Detectives** (optional · ungraded): Friday FLEX or review day **after** the quiz, or enrichment. Never required.
- **Optional review slides 34–45** (six MCQ pairs, 1.5 min per pair): review day or FLEX only — never inside a required block.
- **Quiz slot:** Fri 10/16 · Session 3 · minutes 12-25 (quiz handed out no later than minute 12) · TEACHER CHOICE: OPEN NOTE OR CLOSED NOTE.

## At a glance

| Session | Day | Focus | Notes page | Reader | Slides (required) | Required min | Buffer |
|---|---|---|---|---|---|---|---|
| 1 | Mon 10/12 | Observe & Name | Guided Notes p. 1 (BQ (first thinking) · V1 · N1) | Reader pp. 1-2 | 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 | 24.5 | 5.5 |
| 2 | Tue 10/13 | Forms & Stored Energy | Guided Notes p. 2 (N2 · V2 · N3) | Reader pp. 3-5 | 2 (re-entry), 17, 19, 20, 21, 22, 23, 24, 25, 26, 27 | 24.5 | 5.5 |
| 3 | Fri 10/16 | Recognize, Reflect & Quiz | Guided Notes p. 3 (N4 · CHECK YOUR THINKING · BQ NOW I THINK) | Reader pp. 1-5 | 2 (re-entry), 28, 29, 30, 31, 33 + quiz | 25 | 5 |

## Session 1 — Mon 10/12 · Observe & Name

**Goal:** Students observe a change, name it as evidence, and complete notes page 1.  
**Student resources:** Guided Notes p. 1 · Reader pp. 1-2  
**Required:** 24.5 min · **Buffer:** 5.5 min

| Slide | Task | Min | Status |
|---|---|---|---|
| 1 | Title | 1 | REQUIRED |
| 2 | Big Question + turn & talk | 2 | REQUIRED |
| 3 | BQ - My first thinking (write) | 2 | REQUIRED |
| 6 | Sharpener: observe BEFORE | 1 | REQUIRED |
| 7 | Sharpener: predict | 1 | REQUIRED |
| 8 | Sharpener: run + BEFORE/AFTER changes | 3 | REQUIRED |
| 9 | Changes are evidence | 2 | REQUIRED |
| 10 | V1 vocabulary cards (Reader p. 1) | 3 | REQUIRED |
| 11 | V1 notes - write | 2 | REQUIRED |
| 12 | V1 notes - reveal | 0.5 | REQUIRED |
| 13 | What is energy? (Reader p. 1) | 1 | REQUIRED |
| 14 | Seashore: change is evidence (Reader p. 2) | 3 | REQUIRED |
| 15 | N1 notes - write | 2 | REQUIRED |
| 16 | N1 notes - reveal + model | 1 | REQUIRED |
| 4 | *Light-switch phenomenon (Reader p. 1)* | (2) | OPTIONAL — skip freely |
| 5 | *Notice & wonder* | (2) | OPTIONAL — skip freely |

**If short on time (real cuts, in order):**
- Skip slides 4-5 (already optional) - saves 4 min if they were planned.
- Skip slide 13 (recite) and go from V1 reveal (12) straight to the Reader p. 2 read-aloud (14) - saves 1 min.
- Run the sharpener once (no second pencil); merge slides 6-7 into one 90-second predict-and-look - saves 0.5 min.
- HARD STOP: if slide 15 has not started by minute 24, move the N1 write/reveal (slides 15-16, 3 min) to the first 3 min of Session 2 (Session 2 has 5.5 min of buffer, so after the move it has 2.5 min: skip the optional clap check, slide 18, to restore it).

## Session 2 — Tue 10/13 · Forms & Stored Energy

**Goal:** Students identify five forms of energy and explain stored energy; notes page 2 complete.  
**Student resources:** Guided Notes p. 2 · Reader pp. 3-5  
**Required:** 24.5 min · **Buffer:** 5.5 min

| Slide | Task | Min | Status |
|---|---|---|---|
| 2 | Re-entry: re-read the Big Question; "What evidence have we collected so far?" | 1 | REQUIRED |
| 17 | Forms of energy (Reader p. 3) | 3 | REQUIRED |
| 19 | N2 notes - write 5 examples | 5 | REQUIRED |
| 20 | V2 vocabulary card (Reader p. 4) | 3 | REQUIRED |
| 21 | V2 notes - write | 1 | REQUIRED |
| 22 | V2 notes - reveal | 0.5 | REQUIRED |
| 23 | Still battery: predict | 2 | REQUIRED |
| 24 | Stored energy of position (Reader p. 5) | 2 | REQUIRED |
| 25 | STORED -> RELEASE -> CHANGE model | 2 | REQUIRED |
| 26 | N3 notes - write | 4 | REQUIRED |
| 27 | N3 notes - reveal + samples | 1 | REQUIRED |
| 18 | *Clap check (forms)* | (2) | OPTIONAL — skip freely |

**If short on time (real cuts, in order):**
- Skip slide 18 (clap check, already optional) - saves 2 min.
- Students finish at most 3 of the 5 N2 rows in class; the remaining rows are completed at the end of the block or as take-home (all 5 are required by Friday) - saves 2 min.
- Teach slide 24 (position) as a 90-second teacher read-aloud and skip the partner talk - saves 0.5 min.
- HARD STOP: if slide 26 has not started by minute 24, finish N3 as the 5-minute opener of Friday Session 3 only if Friday has a 5-min buffer; otherwise assign N3 as take-home (no new vocabulary or concept remains for it).

## Session 3 — Fri 10/16 · Recognize, Reflect & Quiz

**Goal:** Students synthesise evidence (no new vocabulary), answer the BQ, then take the scored Chapter 1 quiz.  
**Student resources:** Guided Notes p. 3 · Reader pp. 1-5  
**Required:** 25 min · **Buffer:** 5 min

| Slide | Task | Min | Status |
|---|---|---|---|
| 2 | Re-entry: re-read the Big Question; "What evidence have we collected so far?" | 0.5 | REQUIRED |
| 28 | Recognizing evidence (Reader pp. 1-5) | 2 | REQUIRED |
| 29 | N4 notes - draw BEFORE/AFTER + What changed? | 3.5 | REQUIRED |
| 30 | CHECK YOUR THINKING - write | 2.5 | REQUIRED |
| 31 | CHECK YOUR THINKING - sample | 1 | REQUIRED |
| 33 | BQ - NOW I THINK (write) | 2.5 | REQUIRED |
| — | **Chapter 1 quiz** (9 items · 16 pts · teacher choice open/closed note) | 13 | REQUIRED |
| 32 | *Apply: which change shows energy at work?* | (2) | OPTIONAL — skip freely |

**If short on time (real cuts, in order):**
- Skip slide 32 (already optional) and slide 31 (read the sample from the key aloud) - saves 1 min.
- FRIDAY FALLBACK (full ladder below): the quiz is handed out NO LATER THAN MINUTE 12 of the block, whatever is unfinished. Priority: 1 N4 draw (slides 28-29) > 2 BQ NOW I THINK (slide 33) > 3 CHECK YOUR THINKING (slides 30-31).
- NEVER shorten or move the quiz; unfinished CHECK / BQ work is completed at home or in catch-up (due before Monday's lesson) - no new assignment is created.

### Friday fallback — protects the quiz start (Friday is TIGHT)

Friday plans 25 required minutes with a 5-minute buffer, so a normal 3–5 minute transition loss leaves no slack for the full sequence. Policy is unchanged; this ladder only decides **what yields** when time is lost. No new assignment is created — unfinished work uses the same Guided Notes page 3.

| Priority | Task | Slides | Rule |
|---|---|---|---|
| 1 | N4 draw BEFORE/AFTER + What changed? | 28, 29 | primary Friday note task - always done in class |
| 2 | BQ NOW I THINK | 33 | required synthesis - done in class if it fits before minute 12, otherwise right after the quiz is collected or at home / in catch-up |
| 3 | CHECK YOUR THINKING | 30, 31 | may be completed at home / during catch-up if needed (uses no new content) |

- HARD RULE - the quiz is handed out no later than MINUTE 12 of the block. It is never shortened and never moved.
- Minute 6 checkpoint: N4 (slides 28-29) should be finished. If it is not, finish N4 first, then skip slides 30-31.
- Skip rule: if slide 30 has not started when N4 ends (clock past minute 6), skip slides 30-31 now. CHECK YOUR THINKING goes home / catch-up (due before Monday's lesson).
- Minute 9.5 checkpoint: if BQ NOW I THINK (slide 33, 2.5 min) has not started, do not start it before the quiz. Students write it after handing in the quiz, or at home / in catch-up.
- Minute 12: hand out the quiz regardless of what is unfinished (quiz = minutes 12-25; minutes 25-30 stay as buffer).

*Check:* re-entry + N4 = 6 min; with a 5-minute loss that is minute 11, still before the minute-12 quiz deadline; quiz 12–25, buffer 25–30.

## Optional review slides

Slides 34–45: six multiple-choice question/answer pairs. Use on a review day or FLEX. Correct letters: Q1=C · Q2=A · Q3=D · Q4=B · Q5=A · Q6=C (deliberately not patterned).

## Absence & catch-up

- Absent student → `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md` (priority: complete Guided Notes pages in order; the quiz is never made up with open notes unless the teacher chose open note for the class).
- A class that finishes a session early starts nothing new; use the buffer for turn-and-talk or move on to the next session's re-entry.

## Unit-level note

Week 1 of the unit calendar holds Chapters 1–2 (Mon–Tue Ch1 · Wed–Thu Ch2 · Fri Ch1 Session 3 + FLEX). Under the owner Friday policy (2026-10-04) Chapter 1 uses Friday for **consolidation, BQ reflection and the scored quiz** (no new vocabulary, no new concept). Consequences: (1) the optional Friday FLEX items (Energy Detectives, Moving Marbles follow-ups) share the block only after the quiz or move to the next FLEX window or a review day; (2) if Friday is short, the Friday fallback above applies (CHECK, then BQ, yield; the quiz still starts by minute 12). Chapter 2's own pacing is outside this plan and is checked in its own phase.
