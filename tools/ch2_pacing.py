"""Chapter 2 — SINGLE authoritative pacing data (Phase 7.4).

Every Chapter 2 timing statement (slide speaker notes, Teacher Playbook, pacing docs,
manifest, QA) is derived from or checked against this module. Do NOT create a second
timing system.

Reality model
-------------
* 30-minute science block. About 3–5 min is lost to transitions, so every session
  plans <= 25 required minutes (>= 5 min buffer).
* Calendar Week 1: Chapter 1 owns Mon, Tue, and Fri. Chapter 2 owns Wed 10/14 and
  Thu 10/15 only. Friday 10/16 is Chapter 1 Session 3 (quiz). Chapter 2 does not
  put essential new content, or its quiz, on that Friday.
* Friday policy (owner decision 2026-10-04): Friday is never the first exposure to
  essential new core content. All Chapter 2 vocabulary (V1, V2) and models (N1–N3)
  are taught Wednesday–Thursday. Thursday's quiz is scored work on content already
  taught that week, protected by a minute-12 handout deadline.
"""

import re

S = {}

def _add(slide, session, status, minutes, cat, label):
    S[slide] = dict(session=session, status=status, minutes=minutes, cat=cat, label=label)

# Session 1 · Wed 10/14 · Motion and cause · Notes p. 1 (BQ, V1, N1, V2)
_add(1, 1, "REQ", 1.0, "open", "Title")
_add(2, 1, "REQ", 2.0, "open", "Big Question + turn & talk")
_add(3, 1, "REQ", 2.0, "write", "BQ - My first thinking (write)")
_add(4, 1, "REQ", 1.0, "demo", "Marble Collision: observe BEFORE")
_add(5, 1, "REQ", 1.0, "demo", "Marble Collision: predict")
_add(6, 1, "REQ", 2.5, "demo", "Marble Collision: roll + name the change")
_add(7, 1, "REQ", 1.5, "talk", "Change is evidence")
_add(8, 1, "REQ", 2.5, "reader", "V1 vocabulary card (Reader p. 7)")
_add(9, 1, "REQ", 1.5, "write", "V1 notes - write")
_add(10, 1, "REQ", 0.5, "check", "V1 notes - reveal")
_add(11, 1, "REQ", 2.0, "reader", "Moving objects can cause changes (Reader p. 8)")
_add(12, 1, "REQ", 2.5, "write", "N1 notes - write")
_add(13, 1, "REQ", 0.5, "check", "N1 notes - reveal")
_add(14, 1, "REQ", 2.0, "reader", "V2 vocabulary card (Reader p. 9)")
_add(15, 1, "REQ", 1.0, "write", "V2 notes - write")
_add(16, 1, "REQ", 0.5, "check", "V2 notes - reveal")

# Session 2 · Thu 10/15 · Energy of motion, use, quiz · Notes p. 2–3
_add(17, 2, "REQ", 1.0, "reader", "N2 model: moving object, change, evidence")
_add(18, 2, "REQ", 1.0, "write", "N2 notes - write")
_add(19, 2, "REQ", 2.0, "write", "N2 draw BEFORE/AFTER + What changed?")
_add(20, 2, "REQ", 0.5, "check", "N2 notes - reveal")
_add(21, 2, "REQ", 1.0, "reader", "People use the energy of motion (Reader pp. 10-12)")
_add(22, 2, "REQ", 1.5, "write", "N3 notes - write three changes")
_add(23, 2, "REQ", 0.5, "check", "N3 notes - reveal")
_add(24, 2, "REQ", 1.5, "write", "CHECK YOUR THINKING - write")
_add(25, 2, "REQ", 0.5, "check", "CHECK YOUR THINKING - sample")
_add(26, 2, "OPT", 2.0, "talk", "Apply: which change shows the energy of motion?")
_add(27, 2, "REQ", 1.5, "write", "BQ - NOW I THINK (write)")

for q in range(5):
    _add(28 + 2 * q, 0, "OPT", 1.0, "check", "Review question %d" % (q + 1))
    _add(29 + 2 * q, 0, "OPT", 0.5, "check", "Review answer %d" % (q + 1))

REENTRY_SLIDE = 2
REENTRY_MIN = {2: 1.0}   # settle, notes out, re-read the Big Question

QUIZ_MIN = 12.0          # hand out 1 + work 10 + collect 1. All 12 minutes stay in the block.
BLOCK_MIN = 30.0
MIN_BUFFER = 5.0
QUIZ_START_DEADLINE = 12.0   # planned minute the quiz is in students' hands

SESSIONS = {
    1: dict(
        day="Wed 10/14", short="Wed", title="Motion and Cause",
        notes="Guided Notes p. 1, plus the V2 line at the top of p. 2",
        anchors="BQ (first thinking) · V1 · N1 · V2", reader="Reader pp. 7-9",
        order=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        start_slide=1, end_slide=16, quiz=False,
        goal="Students observe a marble collision, name motion, and record how a moving object causes a change.",
    ),
    2: dict(
        day="Thu 10/15", short="Thu", title="Energy of Motion, Use, and Quiz",
        notes="Guided Notes p. 2-3",
        anchors="N2 · N3 · CHECK YOUR THINKING · BQ NOW I THINK", reader="Reader pp. 9-12",
        order=[2, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27],
        start_slide=2, end_slide=27, quiz=True,
        goal="Students explain energy of motion, record three useful changes, answer the Big Question, then take the quiz.",
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

IF_SHORT = {
    1: [
        "Merge slides 4 and 5 into one 90-second observe-and-predict. Saves about 1 min.",
        "Read Reader p. 8 (slide 11) aloud in 60 seconds and go straight to the N1 write. Saves about 1 min.",
        "HARD STOP: if the V2 card (slide 14) has not started by minute 22, teach the card aloud and finish the V2 blank in the first minute of Thursday, before N2. Thursday's buffer can absorb that 1 minute.",
    ],
    2: [
        "Skip slide 26 (already optional). It is not part of the required 24 minutes.",
        "If the opening runs long, shorten the N3 read-aloud (slide 21) to 30 seconds and read the CHECK sample (slide 25) in 20 seconds. Saves about 1 minute.",
        "Do not skip N2, N3, CHECK, or the Big Question return. Keep that writing in class. Do not shorten the 12-minute quiz.",
        "A 30-second recall of yesterday's marble is inside slide 19. One reminder roll is enough. It is not a second investigation.",
    ],
}

THU_PRIORITY = [
    ("N2 model, write, draw, reveal", [17, 18, 19, 20], "required in class, including a 30-second marble recall"),
    ("N3 three useful changes", [21, 22, 23], "required in class"),
    ("CHECK YOUR THINKING", [24, 25], "required in class, before the quiz"),
    ("BQ NOW I THINK", [27], "required in class, before the quiz"),
]
THU_FALLBACK = [
    "Planned handout: minute 12, after 12 minutes of instruction. The quiz then uses minutes 12-24.",
    "The 12 quiz minutes include handing the quiz out, student work, and collection. Do not shorten them.",
    "If the opening runs long, shorten only the N3 read-aloud and the CHECK sample. N2, N3 writing, CHECK writing, and the Big Question stay in class.",
    "A full 5-minute late start is absorbed by the 6-minute buffer only if those two read-alouds are shortened. Do not move the quiz to Friday.",
]

QUIZ_SLOT = ("Thu 10/15 · Session 2 · quiz in students' hands at minute 12 "
             "· 8 items · 12 pts · the full 12 minutes are protected "
             "· TEACHER CHOICE: OPEN NOTE OR CLOSED NOTE")

PRACTICE_NOTE = ("Practice page: ungraded, NOT on any session's critical path. Assign after Session 1 "
                 "as take-home. Recommended before the Thursday quiz.")

FLEX_NOTE = ("Moving Marbles and the Chapter 2 Friday FLEX bank are optional enrichment after the quiz. "
             "They are not Week 1 Friday. That Friday is Chapter 1.")

def check_plan():
    """Return a list of problems (empty list = plan is internally consistent)."""
    problems = []
    for sid, s in SESSIONS.items():
        req = session_required_minutes(sid)
        if req > BLOCK_MIN - MIN_BUFFER + 1e-9:
            problems.append("Session %d plans %.1f min (> %.1f)" % (sid, req, BLOCK_MIN - MIN_BUFFER))
        if s["start_slide"] not in (1, REENTRY_SLIDE):
            problems.append("Session %d starts on slide %d" % (sid, s["start_slide"]))
        if re.search(r"Fri", s["day"]):
            problems.append("Session %d is on Friday" % sid)
        for sl in s["order"]:
            if sl not in S:
                problems.append("slide %d missing" % sl)
            elif S[sl]["status"] == "OPT":
                problems.append("optional slide %d is inside the required order" % sl)
    pre = sum(slide_minutes(sl, 2) for sl in SESSIONS[2]["order"])
    if abs(pre - QUIZ_START_DEADLINE) > 0.26:
        problems.append("Thursday pre-quiz work %.1f min is not the minute-%g handout" % (pre, QUIZ_START_DEADLINE))
    if pre + QUIZ_MIN > BLOCK_MIN - MIN_BUFFER + 1e-9:
        problems.append("Thursday plan %.1f min exceeds %.1f" % (pre + QUIZ_MIN, BLOCK_MIN - MIN_BUFFER))
    if re.search(r"at home|homework|goes home", " ".join(IF_SHORT[2]), re.I):
        problems.append("Thursday plan sends required notes home")
    seen = {}
    for sid, s in SESSIONS.items():
        for sl in s["order"]:
            if sl != REENTRY_SLIDE:
                seen.setdefault(sl, []).append(sid)
    for sl, info in S.items():
        if info["status"] != "REQ":
            if sl in seen:
                problems.append("optional slide %d is scheduled as required" % sl)
            continue
        if sl == REENTRY_SLIDE:
            continue
        if sl not in seen or seen[sl] != [info["session"]]:
            problems.append("required slide %d not scheduled once in session %d" % (sl, info["session"]))
    for sl, info in S.items():
        if info["session"] == 0:
            for s in SESSIONS.values():
                if sl in s["order"]:
                    problems.append("review slide %d is inside a required block" % sl)
    return problems

if __name__ == "__main__":
    for sid in SESSIONS:
        print(sid, SESSIONS[sid]["day"], "required %.1f buffer %.1f" % (
            session_required_minutes(sid), session_buffer(sid)))
    print("problems:", check_plan() or "none")
