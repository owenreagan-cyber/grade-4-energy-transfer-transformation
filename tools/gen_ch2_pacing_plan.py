"""Generate the authoritative Chapter 2 pacing plan from tools/ch2_pacing.py.

Writes:
  docs/chapter-02/CH2_PACING_PLAN.md
  qa/reports/PHASE_7_1_CH2_CLASSROOM_TIME_SIMULATION.md
Run: .venv/bin/python tools/gen_ch2_pacing_plan.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ch2_pacing as P

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def fmt(m):
    return "%g" % m

def session_table(sid):
    s = P.SESSIONS[sid]
    rows = ["| Slide | Task | Min | Status |", "|---|---|---|---|"]
    for sl in s["order"]:
        info = P.S[sl]
        if sl == P.REENTRY_SLIDE and sid in P.REENTRY_MIN:
            rows.append("| %d | Re-entry: re-read the Big Question; \"What evidence have we collected so far?\" | %s | REQUIRED |" % (
                sl, fmt(P.REENTRY_MIN[sid])))
        else:
            rows.append("| %d | %s | %s | REQUIRED |" % (sl, info["label"], fmt(info["minutes"])))
    if s["quiz"]:
        rows.append("| — | **Chapter 2 quiz** (8 items · 12 pts · teacher choice open/closed note) | %s | REQUIRED |" % fmt(P.QUIZ_MIN))
    opt = [sl for sl, i in P.S.items() if i["session"] == sid and i["status"] == "OPT"]
    for sl in sorted(opt):
        rows.append("| %d | *%s* | (%s) | OPTIONAL — skip freely |" % (sl, P.S[sl]["label"], fmt(P.S[sl]["minutes"])))
    return "\n".join(rows)

def plan_md():
    s1, s2 = P.session_required_minutes(1), P.session_required_minutes(2)
    L = []
    L.append("# Chapter 2 — Authoritative Pacing Plan\n")
    L.append("> **This is the ONE Chapter 2 timing system.** The Teacher Playbook, the Week 1 calendar rows, the curriculum map, slide speaker notes (TIME / PLAN lines), and QA are checked against `tools/ch2_pacing.py`. Do not create another. Regenerate with `.venv/bin/python tools/gen_ch2_pacing_plan.py`.\n")
    L.append("Status: `UNIT1_CH2_GOLD_STANDARD_VERSION = 1.0`. **FROZEN** (2026-10-06).\n")
    L.append("## Design rules\n")
    L.append("- **30-minute block.** Every session plans **≤ 25 required minutes** so about 5 minutes remain for transitions, materials, questions, and cleanup.")
    L.append("- **Two sessions only:** Wed 10/14 · Thu 10/15. Monday, Tuesday, and Friday of Week 1 belong to Chapter 1. Chapter 2 does not borrow Friday.")
    L.append("- **Friday policy:** Friday may hold catch-up, review, synthesis, a quiz, makeup, or optional enrichment. It is never the first exposure to essential new core content. Chapter 2 vocabulary and models are taught Wednesday and Thursday. Friday 10/16 is the Chapter 1 quiz, not a Chapter 2 lesson.")
    L.append("- **No session starts on a reveal slide.** Session 1 opens on slide 1. Session 2 opens on slide 2 (Big Question re-entry).")
    L.append("- **Notes pages:** p. 1 (BQ, V1, N1) and the V2 line at the top of p. 2 → Session 1. The rest of p. 2 (N2) and p. 3 (N3, CHECK, BQ return) → Session 2.")
    L.append("- **Quiz slot:** %s." % P.QUIZ_SLOT)
    L.append("- %s" % P.PRACTICE_NOTE)
    L.append("- %s" % P.FLEX_NOTE)
    L.append("- **Optional review slides 28–37** stay outside both required blocks.\n")
    L.append("## At a glance\n")
    L.append("| Session | Day | Focus | Notes | Reader | Slides (required) | Required min | Buffer |")
    L.append("|---|---|---|---|---|---|---|---|")
    L.append("| 1 | Wed 10/14 | Motion and Cause | p. 1: BQ · V1 · N1, then V2 at the top of p. 2 | pp. 7–9 | 1–16 | %s | %s |" % (fmt(s1), fmt(P.session_buffer(1))))
    L.append("| 2 | Thu 10/15 | Energy of Motion, Use, and Quiz | p. 2–3: N2 · N3 · CHECK · BQ now | pp. 9–12 | 2, 17–25, 27 + quiz (26 OPTIONAL) | %s | %s |\n" % (fmt(s2), fmt(P.session_buffer(2))))
    L.append("## Session 1 — Wed 10/14 · Motion and Cause\n")
    L.append("**Goal:** %s" % P.SESSIONS[1]["goal"])
    L.append("**Student resources:** Guided Notes p. 1 · Reader pp. 7–9")
    L.append("**Required:** %s min · **Buffer:** %s min\n" % (fmt(s1), fmt(P.session_buffer(1))))
    L.append(session_table(1))
    L.append("\n**If short on time:**\n")
    for line in P.IF_SHORT[1]:
        L.append("- " + line)
    L.append("\n## Session 2 — Thu 10/15 · Energy of Motion, Use, and Quiz\n")
    L.append("**Goal:** %s" % P.SESSIONS[2]["goal"])
    L.append("**Student resources:** Guided Notes pp. 2–3 · Reader pp. 9–12")
    L.append("**Required:** %s min · **Buffer:** %s min\n" % (fmt(s2), fmt(P.session_buffer(2))))
    L.append(session_table(2))
    L.append("\n**If short on time:**\n")
    for line in P.IF_SHORT[2]:
        L.append("- " + line)
    L.append("\n### Thursday fallback — protects the quiz start\n")
    L.append("Thursday plans %s required minutes. A normal transition loss leaves the quiz start protected by yielding synthesis, not new content.\n" % fmt(s2))
    L.append("| Priority | Task | Slides | Rule |")
    L.append("|---|---|---|---|")
    for name, slides, rule in P.THU_PRIORITY:
        L.append("| %s | %s | %s | %s |" % (P.THU_PRIORITY.index((name, slides, rule)) + 1, name, ", ".join(str(x) for x in slides), rule))
    L.append("")
    for line in P.THU_FALLBACK:
        L.append("- " + line)
    L.append("\n## What is not in either block\n")
    L.append("- Review slides 28–37 (five question/answer pairs): enrichment only, after the quiz.")
    L.append("- Slide 26 (which change shows the energy of motion): optional. Skip it when the quiz needs the time.")
    L.append("- Moving Marbles: optional enrichment after the quiz. It is not Thursday's lesson and not Week 1 Friday.")
    L.append("- The Marble Collision on Wednesday is a mini demonstration. It is not a second investigation and it does not measure speed.\n")
    probs = P.check_plan()
    L.append("## Internal check\n")
    L.append("`check_plan()` problems: %s\n" % (probs or "none"))
    return "\n".join(L) + "\n"

def sim_md():
    L = ["# Chapter 2 classroom-time simulation (Phase 7.1)\n",
         "Derived from `tools/ch2_pacing.py`. Not a second timing system.\n",
         "| Session | Day | Required min | Buffer | Quiz |",
         "|---|---|---|---|---|"]
    for sid, s in P.SESSIONS.items():
        L.append("| %d | %s | %s | %s | %s |" % (
            sid, s["day"], fmt(P.session_required_minutes(sid)), fmt(P.session_buffer(sid)),
            "yes, by minute %g" % P.QUIZ_START_DEADLINE if s["quiz"] else "no"))
    pre = sum(P.slide_minutes(sl, 2) for sl in P.SESSIONS[2]["order"])
    L.append("\nThursday instruction before the quiz = %s min. The quiz is in students' hands at minute %g and uses the next %s minutes (hand out, work, collect)." % (
        fmt(pre), P.QUIZ_START_DEADLINE, fmt(P.QUIZ_MIN)))
    L.append("\n`check_plan()`: %s\n" % (P.check_plan() or "none"))
    return "\n".join(L) + "\n"

def main():
    probs = P.check_plan()
    if probs:
        sys.exit("pacing inconsistent: " + "; ".join(probs))
    plan = os.path.join(ROOT, "docs", "chapter-02", "CH2_PACING_PLAN.md")
    sim = os.path.join(ROOT, "qa", "reports", "PHASE_7_1_CH2_CLASSROOM_TIME_SIMULATION.md")
    open(plan, "w").write(plan_md())
    open(sim, "w").write(sim_md())
    print("wrote", plan)
    print("wrote", sim)

if __name__ == "__main__":
    main()
