"""Chapter 1 — SINGLE authoritative pacing data (Phase 6.1 / F1).

Every Chapter 1 timing statement (slide speaker notes, Teacher Playbook, pacing docs,
manifest, QA) is derived from or checked against this module. Do NOT create a second
timing system anywhere else.

Reality model
-------------
* 30-minute science block, 20 students, 5 groups of 4.
* 4-5 min lost to normal transitions  ->  every session must plan <= 25 min of
  required work (>= 5 min buffer) and must never depend on perfect timing.
* Friday policy (owner decision 2026-10-04): Friday may hold catch-up, review, completion of taught
  work, BQ reflection/synthesis, scored quizzes, makeup and optional FLEX; it is NEVER the first
  exposure to essential new core content. Session 3 = recognise + reflect + quiz, and every Friday
  slide is traceable to a concept first taught in Session 1 or 2 (FRIDAY_DEPENDS, gated).
"""

import re

# slide -> (session, status, minutes, category, short label)
# status: REQ = required in the session; OPT = optional (skip freely); the review slides
# 34-45 are OPT and never scheduled inside a required block.
# categories: open (opening/BQ) · demo · reader · write (note writing) · talk (discussion)
#             check (reveal/check) · quiz
S = {}

def _add(slide, session, status, minutes, cat, label):
    S[slide] = dict(session=session, status=status, minutes=minutes, cat=cat, label=label)

# ---- Session 1 · Mon 10/12 · Observe & Name · Guided Notes p. 1 (BQ, V1, N1) -----------
_add(1, 1, "REQ", 1.0, "open", "Title")
_add(2, 1, "REQ", 2.0, "open", "Big Question + turn & talk")
_add(3, 1, "REQ", 2.0, "write", "BQ - My first thinking (write)")
_add(4, 1, "OPT", 2.0, "demo", "Light-switch phenomenon (Reader p. 1)")
_add(5, 1, "OPT", 2.0, "talk", "Notice & wonder")
_add(6, 1, "REQ", 1.0, "demo", "Sharpener: observe BEFORE")
_add(7, 1, "REQ", 1.0, "demo", "Sharpener: predict")
_add(8, 1, "REQ", 3.0, "demo", "Sharpener: run + BEFORE/AFTER changes")
_add(9, 1, "REQ", 2.0, "talk", "Changes are evidence")
_add(10, 1, "REQ", 3.0, "reader", "V1 vocabulary cards (Reader p. 1)")
_add(11, 1, "REQ", 2.0, "write", "V1 notes - write")
_add(12, 1, "REQ", 0.5, "check", "V1 notes - reveal")
_add(13, 1, "REQ", 1.0, "reader", "What is energy? (Reader p. 1)")
_add(14, 1, "REQ", 3.0, "reader", "Seashore: change is evidence (Reader p. 2)")
_add(15, 1, "REQ", 2.0, "write", "N1 notes - write")
_add(16, 1, "REQ", 1.0, "check", "N1 notes - reveal + model")

# ---- Session 2 · Tue 10/13 · Forms & Stored Energy · Guided Notes p. 2 (N2, V2, N3) -----
_add(17, 2, "REQ", 3.0, "reader", "Forms of energy (Reader p. 3)")
_add(18, 2, "OPT", 2.0, "talk", "Clap check (forms)")
_add(19, 2, "REQ", 5.0, "write", "N2 notes - write 5 examples")
_add(20, 2, "REQ", 3.0, "reader", "V2 vocabulary card (Reader p. 4)")
_add(21, 2, "REQ", 1.0, "write", "V2 notes - write")
_add(22, 2, "REQ", 0.5, "check", "V2 notes - reveal")
_add(23, 2, "REQ", 2.0, "talk", "Still battery: predict")
_add(24, 2, "REQ", 2.0, "reader", "Stored energy of position (Reader p. 5)")
_add(25, 2, "REQ", 2.0, "talk", "STORED -> RELEASE -> CHANGE model")
_add(26, 2, "REQ", 4.0, "write", "N3 notes - write")
_add(27, 2, "REQ", 1.0, "check", "N3 notes - reveal + samples")

# ---- Session 3 · Fri 10/16 · Recognize, Reflect & Quiz · Guided Notes p. 3 (N4, CHECK, BQ) --
_add(28, 3, "REQ", 2.0, "reader", "Recognizing evidence (Reader pp. 1-5)")
_add(29, 3, "REQ", 3.5, "write", "N4 notes - draw BEFORE/AFTER + What changed?")
_add(30, 3, "REQ", 2.5, "write", "CHECK YOUR THINKING - write")
_add(31, 3, "REQ", 1.0, "check", "CHECK YOUR THINKING - sample")
_add(32, 3, "OPT", 2.0, "talk", "Apply: which change shows energy at work?")
_add(33, 3, "REQ", 2.5, "write", "BQ - NOW I THINK (write)")

# Optional end-of-chapter review (6 questions x question/answer): never inside a required block.
for q in range(6):
    _add(34 + 2 * q, 0, "OPT", 1.0, "check", "Review question %d" % (q + 1))
    _add(35 + 2 * q, 0, "OPT", 0.5, "check", "Review answer %d" % (q + 1))

# Re-entry: Sessions 2 and 3 do NOT open on a reveal slide. They open on slide 2 (BQ banner).
REENTRY_SLIDE = 2
REENTRY_MIN = {2: 1.0, 3: 0.5}

QUIZ_MIN = 13.0          # distribute 1 + work 11 + collect 1 (9 items / 16 pts)
BLOCK_MIN = 30.0
# Friday traceability (owner Friday policy): slide -> where its concept was FIRST taught (sessions 1-2).
FRIDAY_DEPENDS = {
    2:  "BQ introduced Session 1 (slides 2-3)",
    28: "evidence = the change we observe: Session 1 (slides 13-16, V1/N1; Reader p. 2); forms/stored energy: Session 2",
    29: "before/after observation: Session 1 demo slides 7-12 and N1; examples from Session 2 (N2/N3)",
    30: "N1-N3 content (Sessions 1-2); no new vocabulary",
    31: "sample answer to a question built from Sessions 1-2 content (N1-N3)",
    33: "BQ first thinking written Session 1 (slide 3); revisit only",
}

MIN_BUFFER = 5.0         # normal transition loss allowance (3-5 min) + 0 slack for perfect timing

SESSIONS = {
    1: dict(
        day="Mon 10/12", short="Mon", title="Observe & Name", notes="Guided Notes p. 1",
        anchors="BQ (first thinking) · V1 · N1", reader="Reader pp. 1-2",
        order=[1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        start_slide=1, end_slide=16, quiz=False,
        goal="Students observe a change, name it as evidence, and complete notes page 1.",
    ),
    2: dict(
        day="Tue 10/13", short="Tue", title="Forms & Stored Energy", notes="Guided Notes p. 2",
        anchors="N2 · V2 · N3", reader="Reader pp. 3-5",
        order=[2, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        start_slide=2, end_slide=27, quiz=False,
        goal="Students identify five forms of energy and explain stored energy; notes page 2 complete.",
    ),
    3: dict(
        day="Fri 10/16", short="Fri", title="Recognize, Reflect & Quiz", notes="Guided Notes p. 3",
        anchors="N4 · CHECK YOUR THINKING · BQ NOW I THINK", reader="Reader pp. 1-5",
        order=[2, 28, 29, 30, 31, 33], start_slide=2, end_slide=33, quiz=True,
        goal="Students synthesise evidence (no new vocabulary), answer the BQ, then take the scored Chapter 1 quiz.",
    ),
}

def slide_minutes(slide, session=None):
    if slide == REENTRY_SLIDE and session in REENTRY_MIN:
        return REENTRY_MIN[session]
    return S[slide]["minutes"]

def session_required_minutes(sid):
    s = SESSIONS[sid]
    total = sum(slide_minutes(sl, sid) for sl in s["order"])
    if s["quiz"]:
        total += QUIZ_MIN
    return total

def session_buffer(sid):
    return BLOCK_MIN - session_required_minutes(sid)

def category_minutes(sid):
    out = {}
    s = SESSIONS[sid]
    for sl in s["order"]:
        cat = S[sl]["cat"] if not (sl == REENTRY_SLIDE and sid in REENTRY_MIN) else "open"
        out[cat] = out.get(cat, 0.0) + slide_minutes(sl, sid)
    if s["quiz"]:
        out["quiz"] = out.get("quiz", 0.0) + QUIZ_MIN
    return out

# Real "if short on time" cuts (every item names a real slide/task that exists in the plan).
IF_SHORT = {
    1: [
        "Skip slides 4-5 (already optional) - saves 4 min if they were planned.",
        "Skip slide 13 (recite) and go from V1 reveal (12) straight to the Reader p. 2 read-aloud (14) - saves 1 min.",
        "Run the sharpener once (no second pencil); merge slides 6-7 into one 90-second predict-and-look - saves 0.5 min.",
        "HARD STOP: if slide 15 has not started by minute 24, move the N1 write/reveal (slides 15-16, 3 min) to the first 3 min of Session 2 (Session 2 has 5.5 min of buffer, so after the move it has 2.5 min: skip the optional clap check, slide 18, to restore it).",
    ],
    2: [
        "Skip slide 18 (clap check, already optional) - saves 2 min.",
        "Students finish at most 3 of the 5 N2 rows in class; the remaining rows are completed at the end of the block or as take-home (all 5 are required by Friday) - saves 2 min.",
        "Teach slide 24 (position) as a 90-second teacher read-aloud and skip the partner talk - saves 0.5 min.",
        "HARD STOP: if slide 26 has not started by minute 24, finish N3 as the 5-minute opener of Friday Session 3 only if Friday has a 5-min buffer; otherwise assign N3 as take-home (no new vocabulary or concept remains for it).",
    ],
    3: [
        "Skip slide 32 (already optional) and slide 31 (read the sample from the key aloud) - saves 1 min.",
        "FRIDAY FALLBACK (full ladder below): the quiz is handed out NO LATER THAN MINUTE 12 of the block, whatever is unfinished. Priority: 1 N4 draw (slides 28-29) > 2 BQ NOW I THINK (slide 33) > 3 CHECK YOUR THINKING (slides 30-31).",
        "NEVER shorten or move the quiz; unfinished CHECK / BQ work is completed at home or in catch-up (due before Monday's lesson) - no new assignment is created.",
    ],
}

PRACTICE_NOTE = ("Practice page: ungraded, NOT on any session's critical path. Assign after Session 2 as take-home or "
                 "any spare 12-minute window (or a Friday FLEX PRACTICE slot). Recommended before the Friday quiz.")

QUIZ_START_DEADLINE = 12.0   # HARD: the quiz is handed out no later than this minute of the Friday block
LOSS_ALLOWANCE = 5.0         # normal transition loss the Friday plan must survive

QUIZ_SLOT = "Fri 10/16 · Session 3 · minutes 12-25 (quiz handed out no later than minute 12) · TEACHER CHOICE: OPEN NOTE OR CLOSED NOTE"

# Friday operational fallback (Phase 6.1B / M3). Friday is TIGHT (25 min required, 5 min buffer), so the
# plan protects the quiz start instead of the page-3 close-out. Same policy, no new assignment:
# CHECK / BQ work that does not fit is finished at home or in catch-up on the SAME notes page.
FRIDAY_PRIORITY = [
    ("N4 draw BEFORE/AFTER + What changed?", [28, 29], "primary Friday note task - always done in class"),
    ("BQ NOW I THINK", [33], "required synthesis - done in class if it fits before minute 12, otherwise right after the quiz is collected or at home / in catch-up"),
    ("CHECK YOUR THINKING", [30, 31], "may be completed at home / during catch-up if needed (uses no new content)"),
]
FRIDAY_FALLBACK = [
    "HARD RULE - the quiz is handed out no later than MINUTE 12 of the block. It is never shortened and never moved.",
    "Minute 6 checkpoint: N4 (slides 28-29) should be finished. If it is not, finish N4 first, then skip slides 30-31.",
    "Skip rule: if slide 30 has not started when N4 ends (clock past minute 6), skip slides 30-31 now. CHECK YOUR THINKING goes home / catch-up (due before Monday's lesson).",
    "Minute 9.5 checkpoint: if BQ NOW I THINK (slide 33, 2.5 min) has not started, do not start it before the quiz. Students write it after handing in the quiz, or at home / in catch-up.",
    "Minute 12: hand out the quiz regardless of what is unfinished (quiz = minutes 12-25; minutes 25-30 stay as buffer).",
]

def check_plan():
    """Return a list of problems (empty list = plan is internally consistent)."""
    problems = []
    for sid, s in SESSIONS.items():
        req = session_required_minutes(sid)
        if req > BLOCK_MIN - MIN_BUFFER + 1e-9:
            problems.append("Session %d plans %.1f min (> %.1f)" % (sid, req, BLOCK_MIN - MIN_BUFFER))
        first = s["start_slide"]
        if first not in (1, REENTRY_SLIDE):
            problems.append("Session %d starts on slide %d" % (sid, first))
        for sl in s["order"]:
            if sl not in S:
                problems.append("slide %d missing" % sl)
    # Friday policy: Session 3 may reflect/synthesise/assess but never first-expose a core concept
    for sl in SESSIONS[3]["order"]:
        if S[sl]["status"] == "REQ" and sl not in FRIDAY_DEPENDS:
            problems.append("Friday slide %d has no first-taught-in-Mon/Tue traceability" % sl)
        elif S[sl]["status"] == "REQ" and not re.search(r"Session [12]|Sessions 1-2", FRIDAY_DEPENDS[sl]):
            problems.append("Friday slide %d traceability does not name Session 1 or 2" % sl)
    # Friday fallback (M3): quiz start is protected and the plan survives a LOSS_ALLOWANCE-minute loss
    pre = sum(slide_minutes(sl, 3) for sl in SESSIONS[3]["order"])
    if pre > QUIZ_START_DEADLINE + 1e-9:
        problems.append("Friday pre-quiz work %.1f min exceeds the minute-%g quiz deadline" % (pre, QUIZ_START_DEADLINE))
    if QUIZ_START_DEADLINE + QUIZ_MIN > BLOCK_MIN - MIN_BUFFER + 1e-9:
        problems.append("Friday quiz deadline %g + quiz %g leaves < %g min buffer" % (QUIZ_START_DEADLINE, QUIZ_MIN, MIN_BUFFER))
    n4 = sum(slide_minutes(sl, 3) for sl in [2] + FRIDAY_PRIORITY[0][1])
    if n4 + LOSS_ALLOWANCE > QUIZ_START_DEADLINE + 1e-9:
        problems.append("Friday N4 path %.1f + loss %.1f exceeds minute %g" % (n4, LOSS_ALLOWANCE, QUIZ_START_DEADLINE))
    # every notes slide 1..33 is scheduled (REQ or OPT) in exactly one session
    seen = {}
    for sid, s in SESSIONS.items():
        for sl in s["order"]:
            if sl != REENTRY_SLIDE:
                seen.setdefault(sl, []).append(sid)
    for sl in range(1, 34):
        if sl == REENTRY_SLIDE:
            continue
        sess = S[sl]["session"]
        if S[sl]["status"] == "REQ" and (sl not in seen or seen[sl] != [sess]):
            problems.append("required slide %d not scheduled once in session %d" % (sl, sess))
    return problems

if __name__ == "__main__":
    for sid in SESSIONS:
        print(sid, SESSIONS[sid]["day"], "required %.1f min, buffer %.1f" % (session_required_minutes(sid), session_buffer(sid)),
              category_minutes(sid))
    print("problems:", check_plan() or "none")
