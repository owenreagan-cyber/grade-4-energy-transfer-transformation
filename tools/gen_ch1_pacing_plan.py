"""Generate the authoritative Chapter 1 pacing plan + classroom-time simulation from tools/ch1_pacing.py.

Writes:
  docs/chapter-01/CH1_PACING_PLAN.md                      (THE one Ch1 timing system)
  qa/reports/PHASE_6_1_CH1_CLASSROOM_TIME_SIMULATION.md   (derived simulation)
Run: .venv/bin/python tools/gen_ch1_pacing_plan.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ch1_pacing as P

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def fmt(m):
    return ("%g" % m)

def session_table(sid):
    s = P.SESSIONS[sid]
    rows = ["| Slide | Task | Min | Status |", "|---|---|---|---|"]
    for sl in s["order"]:
        info = P.S[sl]
        if sl == P.REENTRY_SLIDE and sid in P.REENTRY_MIN:
            rows.append("| %d | Re-entry: re-read the Big Question; \"What evidence have we collected so far?\" | %s | REQUIRED |" % (sl, fmt(P.REENTRY_MIN[sid])))
        else:
            rows.append("| %d | %s | %s | %s |" % (sl, info["label"], fmt(info["minutes"]), "REQUIRED" if info["status"] == "REQ" else "OPTIONAL"))
    if s["quiz"]:
        rows.append("| — | **Chapter 1 quiz** (9 items · 16 pts · teacher choice open/closed note) | %s | REQUIRED |" % fmt(P.QUIZ_MIN))
    opt = [sl for sl, i in P.S.items() if i["session"] == sid and i["status"] == "OPT"]
    for sl in sorted(opt):
        rows.append("| %d | *%s* | (%s) | OPTIONAL — skip freely |" % (sl, P.S[sl]["label"], fmt(P.S[sl]["minutes"])))
    return "\n".join(rows)

def plan_md():
    L = []
    L.append("# Chapter 1 — Authoritative Pacing Plan (v1.1)\n")
    L.append("> **This is the ONE Chapter 1 timing system.** The Teacher Playbook, `UNIT1_PACING_CALENDAR.md`, `MASTER_CURRICULUM_MAP.md`, the package manifest, the slide speaker notes (TIME / PLAN lines) and QA are all derived from `tools/ch1_pacing.py` and checked against it. Do not create another. Regenerate with `.venv/bin/python tools/gen_ch1_pacing_plan.py`.\n")
    L.append("## Design rules\n")
    L.append("- **30-minute block**, ~3–5 min lost to transitions → every session plans **≤ 25 required minutes** (≥ 5 min buffer). Required minutes are shown in the tables below.")
    L.append("- **Three instructional sessions**: Mon 10/12 · Tue 10/13 · Fri 10/16. **Wed 10/14 and Thu 10/15 belong to Chapter 2** (unit calendar). Chapter 1 does not borrow them.")
    L.append("- **Friday policy (owner decision, 2026-10-04):** Friday may hold catch-up, review, completion of previously taught work, BQ reflection/synthesis, scored quizzes, makeup work and optional FLEX; it is **never the first instructional exposure** to essential new core content. All Ch1 concepts, vocabulary (V1, V2) and models (N1–N3) are taught Mon–Tue. Session 3 = recognise (N4, synthesis of content already taught), reflect (CHECK, BQ return) and the **scored quiz**. Traceability for each Friday slide is in `tools/ch1_pacing.py::FRIDAY_DEPENDS` and gated by `check_plan()`.")
    L.append("- **No session starts on a reveal/answer slide.** Session 1 opens on slide 1 (title); Sessions 2 and 3 open on slide 2 (Big Question re-entry).")
    L.append("- **Every required notes page has a named slot**: p. 1 → Session 1 · p. 2 → Session 2 · p. 3 → Session 3. **Every scored artifact has a named slot**: quiz → Session 3, minutes 12–25 (handed out no later than minute 12).")
    L.append("- " + P.PRACTICE_NOTE)
    L.append("- **Energy Detectives** (optional · ungraded): Friday FLEX or review day **after** the quiz, or enrichment. Never required.")
    L.append("- **Optional review slides 34–45** (six MCQ pairs, 1.5 min per pair): review day or FLEX only — never inside a required block.")
    L.append("- **Quiz slot:** " + P.QUIZ_SLOT + ".\n")
    L.append("## At a glance\n")
    L.append("| Session | Day | Focus | Notes page | Reader | Slides (required) | Required min | Buffer |")
    L.append("|---|---|---|---|---|---|---|---|")
    for sid, s in P.SESSIONS.items():
        req = [sl for sl in s["order"] if not (sl == P.REENTRY_SLIDE and sid > 1)]
        rng = ("2 (re-entry), " if sid > 1 else "") + ", ".join(str(x) for x in req)
        L.append("| %d | %s | %s | %s (%s) | %s | %s%s | %s | %s |" % (
            sid, s["day"], s["title"], s["notes"], s["anchors"], s["reader"], rng,
            " + quiz" if s["quiz"] else "", fmt(P.session_required_minutes(sid)), fmt(P.session_buffer(sid))))
    L.append("")
    for sid, s in P.SESSIONS.items():
        L.append("## Session %d — %s · %s\n" % (sid, s["day"], s["title"]))
        L.append("**Goal:** %s  \n**Student resources:** %s · Reader %s  \n**Required:** %s min · **Buffer:** %s min\n" % (
            s["goal"], s["notes"], s["reader"].replace("Reader ", ""), fmt(P.session_required_minutes(sid)), fmt(P.session_buffer(sid))))
        L.append(session_table(sid))
        L.append("")
        L.append("**If short on time (real cuts, in order):**")
        for c in P.IF_SHORT[sid]:
            L.append("- " + c)
        L.append("")
        if sid == 3:
            L.append("### Friday fallback — protects the quiz start (Friday is TIGHT)\n")
            L.append("Friday plans %s required minutes with a %s-minute buffer, so a normal 3–5 minute transition loss leaves no slack for the full sequence. Policy is unchanged; this ladder only decides **what yields** when time is lost. No new assignment is created — unfinished work uses the same Guided Notes page 3.\n" % (fmt(P.session_required_minutes(3)), fmt(P.session_buffer(3))))
            L.append("| Priority | Task | Slides | Rule |\n|---|---|---|---|")
            for i, (name, sls, rule) in enumerate(P.FRIDAY_PRIORITY, 1):
                L.append("| %d | %s | %s | %s |" % (i, name, ", ".join(str(x) for x in sls), rule))
            L.append("")
            for c in P.FRIDAY_FALLBACK:
                L.append("- " + c)
            n4 = sum(P.slide_minutes(sl, 3) for sl in [2] + P.FRIDAY_PRIORITY[0][1])
            L.append("")
            L.append("*Check:* re-entry + N4 = %s min; with a %s-minute loss that is minute %s, still before the minute-%s quiz deadline; quiz %s–%s, buffer %s–30.\n" % (
                fmt(n4), fmt(P.LOSS_ALLOWANCE), fmt(n4 + P.LOSS_ALLOWANCE), fmt(P.QUIZ_START_DEADLINE), fmt(P.QUIZ_START_DEADLINE), fmt(P.QUIZ_START_DEADLINE + P.QUIZ_MIN), fmt(P.QUIZ_START_DEADLINE + P.QUIZ_MIN)))
    L.append("## Optional review slides\n")
    L.append("Slides 34–45: six multiple-choice question/answer pairs. Use on a review day or FLEX. Correct letters: Q1=C · Q2=A · Q3=D · Q4=B · Q5=A · Q6=C (deliberately not patterned).\n")
    L.append("## Absence & catch-up\n")
    L.append("- Absent student → `curriculum/chapter-01/student/recovery/01-ch1-absent-student-recovery.md` (priority: complete Guided Notes pages in order; the quiz is never made up with open notes unless the teacher chose open note for the class).")
    L.append("- A class that finishes a session early starts nothing new; use the buffer for turn-and-talk or move on to the next session's re-entry.\n")
    L.append("## Unit-level note\n")
    L.append("Week 1 of the unit calendar holds Chapters 1–2 (Mon–Tue Ch1 · Wed–Thu Ch2 · Fri Ch1 Session 3 + FLEX). Under the owner Friday policy (2026-10-04) Chapter 1 uses Friday for **consolidation, BQ reflection and the scored quiz** (no new vocabulary, no new concept). Consequences: (1) the optional Friday FLEX items (Energy Detectives, Moving Marbles follow-ups) share the block only after the quiz or move to the next FLEX window or a review day; (2) if Friday is short, the Friday fallback above applies (CHECK, then BQ, yield; the quiz still starts by minute 12). Chapter 2's own pacing is outside this plan and is checked in its own phase.\n")
    return "\n".join(L)

def sim_md():
    L = ["# Phase 6.1 — Chapter 1 Classroom-Time Simulation\n",
         "Derived from `tools/ch1_pacing.py` (single source). 30-minute block; transition loss modelled at 4 min; buffer = 30 − required.\n",
         "| Session | Opening/BQ | Demo | Reader | Write | Talk | Check | Quiz | Required | Transition loss (4) | Slack |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid, s in P.SESSIONS.items():
        cm = P.category_minutes(sid)
        req = P.session_required_minutes(sid)
        g = lambda k: fmt(cm.get(k, 0))
        L.append("| %d %s | %s | %s | %s | %s | %s | %s | %s | %s | 4 | %s |" % (
            sid, s["short"], g("open"), g("demo"), g("reader"), g("write"), g("talk"), g("check"), g("quiz"), fmt(req), fmt(30 - req - 4)))
    L.append("")
    L.append("**Result:** every session retains ≥ 1 min of slack after a 4-minute transition loss, and ≥ 5 min of planned buffer before it. v1.0 planned ≈ 30 min for slides 1–12 alone and ≈ 59 min for slides 13–33 (impossible); v1.1 is feasible.\n")
    L.append("## Stress tests\n")
    L.append("| Scenario | Effect | Plan response |\n|---|---|---|")
    L.append("| Session 1 starts 3 min late (assembly) | 21.5 min available vs 24.5 planned | Cut 3 min: skip slide 13, merge 6–7 (saves 1.5); if N1 write has not started by minute 24 move slides 15–16 to Session 2 opener (buffer 5.5) |")
    L.append("| Class slow on writing (+30%) | S1 +1.8, S2 +3, S3 +2.5 min | within 5 min buffer; Session 3 sends CHECK/BQ home before cutting the quiz |")
    L.append("| Friday loses 5 min before the quiz | N4 ends at minute 11 (6 + 5) | skip slides 30–31 (CHECK → home / catch-up), BQ NOW I THINK after the quiz or at home; quiz still starts by minute 12 and ends by 25 |")
    L.append("| Friday short period (25 min) | quiz cannot share the block with N4/CHECK/BQ | N4 stays in class; CHECK and BQ become take-home / catch-up; quiz starts at minute 12 at the latest |")
    L.append("| Quiz run in a separate FLEX slot | S3 drops to 12 min | acceptable: S3 retains full instruction; the quiz slot just moves |")
    L.append("| Student absent Mon | misses notes p. 1 | recovery doc; they join Session 2 with p. 1 completed from a partner/teacher key |")
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    probs = P.check_plan()
    if probs:
        print("PLAN PROBLEMS:", probs); sys.exit(1)
    with open(os.path.join(ROOT, "docs", "chapter-01", "CH1_PACING_PLAN.md"), "w") as f:
        f.write(plan_md())
    with open(os.path.join(ROOT, "qa", "reports", "PHASE_6_1_CH1_CLASSROOM_TIME_SIMULATION.md"), "w") as f:
        f.write(sim_md())
    print("wrote pacing plan + simulation")
