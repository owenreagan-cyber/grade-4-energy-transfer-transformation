#!/usr/bin/env python3
"""Phase 6.1H — deterministic regression fixture for the fail-closed note-architecture guardrail.

Guards the whole Chapter 1 note hierarchy (Guided Notes, Science Journal, retired notebook),
not only notebook-primary sentence shapes.

BAD phrases must each be REJECTED (is_reactivation -> True) by tools/qa_ch1_note_architecture.
SAFE phrases must each be ALLOWED (is_reactivation -> False).

Run one-shot:  .venv/bin/python tools/qa_notebook_primary_fixture.py
Exit 0 = every BAD detected and every SAFE allowed.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_ch1_note_architecture as q  # noqa: E402

# All prior BAD forms (6.1D + 6.1E) plus the fresh Grok reactivation escapes.
BAD = [
    # prior (6.1D)
    "Interactive Science Notebook is primary.",
    "notebook supersedes Guided Notes.",
    "glue-in notebook supersedes Guided Notes.",
    "notebook is the primary student-note system.",
    "The glue-in notebook is the primary system and must not be retired.",
    "The legacy notebook is still the primary student-note system.",
    # prior (6.1E)
    "The primary student-note system is the notebook.",
    "The primary student note system is the Interactive Science Notebook.",
    "For Chapter 1 the primary notes are the glue-in notebook.",
    "Make the Interactive Science Notebook primary again.",
    "Chapter 1 primary notes: Interactive Science Notebook.",
    "Notebook = primary student notes.",
    # fresh Grok escapes (6.1F)
    "Students' primary notes will be the glue-in notebook.",
    "The notebook is the student's primary note system.",
    "Primary note system: glue-in notebook.",
    "Primary: Interactive Science Notebook.",
    "Guided Notes are replaced by the Interactive Science Notebook.",
    "The INB replaces Guided Notes.",
    "The Interactive Science Notebook is the main note system.",
    "Use the glue-in notebook as the main student-note system.",
    "Chapter 1 uses the Interactive Science Notebook, not Guided Notes.",
    "Guided Notes are optional; the notebook is required.",
    "Students take notes primarily in the glue-in notebook.",
    # mixed historical/current must FAIL
    "The notebook is primary and must not be retired.",
    "The legacy notebook remains the primary student-note system.",
    "The notebook remains primary despite being marked historical.",
    "The notebook was retired before, but is now the primary student-note system again.",
    # Grok silent-pass cases (6.1G) — must enter review and fail closed
    "Guided Notes yield to the notebook architecture starting Monday.",
    "The official student notes medium is the Interactive Science Notebook.",
    "Chapter 1 returns to the Interactive Science Notebook.",
    "Adopt the glue-in notebook for all student notes.",
    "Switch back to the notebook for Chapter 1 notes.",
    "Prefer the Interactive Science Notebook over Guided Notes.",
    "Guided Notes are optional.",
    "Science Journal is primary.",
    "The Science Journal becomes the required note system.",
    "Use Guided Notes only as a backup.",
    "Students take their Chapter 1 notes in the notebook.",
    "The journal replaces Guided Notes for daily notes.",
    # hierarchy gap (6.1G) — demotion / journal promotion without a notebook token
    "Guided Notes are secondary.",
    "Science Journal is required instead of Guided Notes.",
    "Student notes are kept primarily in the Science Journal.",
    "Guided Notes are no longer the main reference artifact.",
    "Switch back to the notebook.",
    "Science Journal = primary.",
    "Guided Notes = secondary.",
    # storage vs alternate note systems (6.1H)
    "The binder is now the official student note system.",
    "Students will keep their primary Chapter 1 notes in a spiral.",
    "Use the handout packet instead of Guided Notes for all Chapter 1 notes.",
    "The logbook becomes the main student reference artifact.",
    "Our new notes medium is the blue binder.",
    "Students no longer need Guided Notes; use the spiral instead.",
    "The binder replaces the current student notes system.",
    "Use a binder system for all student notes.",
    "Students keep all science notes in a spiral.",
    "The portfolio is the official note medium.",
    "Replace Guided Notes with the packet system.",
    "The logbook is the main reference artifact.",
    "Primary science notes: blue binder.",
    "The folder system becomes the main notes system.",
    "The accordion file is now the official student note system.",
    "The folder is the primary note system.",
    "Use the folder instead of Guided Notes.",
    "The folder system replaces Guided Notes.",
    "Students keep their primary notes in the folder.",
    "The folder is the official science-notes medium.",
    # same-clause retirement must not mask a live role (6.1I)
    "Although the notebook is historical, primary notes will be the spiral.",
    "Chapter 2 still uses notebooks historically, but for all chapters the binder is the primary note system.",
    "Historically we used glue-in pages, so now the accordion file is the required notes medium.",
    "The notebook is retired, but the binder is now the official notes system.",
    "Although INB is historical, students will use the spiral for all science notes.",
    "Glue-in pages are legacy, so the portfolio becomes the required notes medium.",
    "The notebook is retired, but the binder is now the primary note system.",
    "Historically we used the notebook, but students now use the spiral for all notes.",
    "Although INB is retired, the worksheet packet becomes the required note system.",
    "The Interactive Science Notebook is historical, while the digital notebook becomes the main student reference artifact.",
    # non-copular role, with and without retirement wash (6.1J)
    "Aside from the retired notebook, keep the main reference artifact in a spiral.",
    "Retired notebook workflow aside, students keep the main reference artifact in a Voice-Memo Vault.",
    "Students keep the main reference artifact in a spiral.",
    "The notebook is not current, so the binder is the official notes system.",
    "Keep the main reference artifact in a spiral.",
    "Put the primary reference artifact in the portfolio.",
    "Students maintain the official notes medium in the digital notebook.",
    "Use the accordion file for the required note system.",
    "Store all primary student notes in the composition book.",
    "Keep the main student reference in the Voice-Memo Vault.",
    "Students record all official science notes in the packet system.",
]

SAFE = [
    "The Interactive Science Notebook is retired for Chapter 1.",
    "The former glue-in notebook architecture is superseded by Guided Notes.",
    "Historical only: Guided Notes are now the primary student note/reference artifact.",
    "The Science Journal is secondary; Guided Notes are primary.",
    "The notebook was the primary system before Chapter 1.",
    "The notebook is no longer primary.",
    "The Friday quiz must not be retired.",
    # known false-positive fixes (6.1F)
    "Never restore the notebook as primary.",
    "The Science Journal is a notebook; Guided Notes are primary.",
    # retirement / historical / negation short forms
    "notebook retired",
    "notebook no longer primary",
    "Guided Notes supersede notebook",
    "The notebook was used in the past.",
    "The notebook must never replace Guided Notes.",
    "Do not make the notebook primary.",
    "The notebook is not primary.",
    "The former notebook architecture is historical.",
    "The glue-in notebook is no longer the primary note system.",
    "Guided Notes supersede the former notebook workflow.",
    "The notebook system is superseded by Guided Notes.",
    "The notebook was previously the primary system.",
    "Chapter 1 formerly used the notebook workflow.",
    # current invariant and retirement (6.1G)
    "Guided Notes are the primary structured student-note/reference artifact.",
    "Science Journal is secondary.",
    "The former notebook workflow was superseded by Guided Notes.",
    "Do not restore the notebook as the primary note system.",
    "The notebook was once used for student notes but is no longer current.",
    # student folder is storage, not a note system (6.1H)
    "Put the worksheet in your folder.",
    "Keep your notes in your folder.",
    "Place the handout in your folder.",
    "Turn in the graded worksheet.",
    "Your lab report is unfinished; place it in your folder and finish it next class.",
    "Put your worksheet in the folder.",
    "Store the handout in your folder.",
    "Keep the finished notes page in your folder.",
    "Put the unfinished lab report in your folder overnight.",
    "Collect the graded worksheet.",
    "Return the notes page to your folder after class.",
    "Store your notes in your folder.",
    "Return the lab report to your folder until tomorrow.",
    "Keep the handout in your folder.",
    "Quiz length has no forced prior-unit spiral.",
    # retirement beside the locked invariant stays safe (6.1I)
    "The notebook is historical, and Guided Notes remain primary.",
    "The notebook is retired; Guided Notes are the primary notes system.",
    "Historically students used glue-in pages, but Guided Notes are primary now.",
    "The old notebook workflow is legacy, and the Science Journal remains secondary.",
    "The former glue-in system was superseded by Guided Notes.",
]


def main():
    bad_miss = [p for p in BAD if not q.is_reactivation(p)]
    safe_hit = [p for p in SAFE if q.is_reactivation(p)]
    n_bad = len(BAD) - len(bad_miss)
    n_safe = len(SAFE) - len(safe_hit)
    print("NOTE-ARCHITECTURE FAIL-CLOSED FIXTURE (6.1J)")
    print("BAD detected: %d/%d" % (n_bad, len(BAD)))
    for p in bad_miss:
        print("  MISSED BAD: %r" % p)
    print("SAFE allowed: %d/%d" % (n_safe, len(SAFE)))
    for p in safe_hit:
        print("  FALSE-POSITIVE SAFE: %r" % p)
    ok = not bad_miss and not safe_hit
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
