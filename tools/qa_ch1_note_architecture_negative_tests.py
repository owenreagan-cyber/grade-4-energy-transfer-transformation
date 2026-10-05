#!/usr/bin/env python3
"""Phase 6.1G — persistent system tests for the fail-closed note-architecture guard.

Repeatable from the repo. Does not modify canonical files.

    .venv/bin/python tools/qa_ch1_note_architecture_negative_tests.py

Exit 0 only when every category passes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_ch1_note_architecture as q  # noqa: E402

# A. New notebook adoption / reactivation. Each must be sensitive AND fail closed.
NOTEBOOK_REACTIVATION = [
    "Guided Notes yield to the notebook architecture starting Monday.",
    "The official student notes medium is the Interactive Science Notebook.",
    "Chapter 1 returns to the Interactive Science Notebook.",
    "Adopt the glue-in notebook for all student notes.",
    "Switch back to the notebook.",
    "Prefer the Interactive Science Notebook over Guided Notes.",
    "Students take their Chapter 1 notes in the notebook.",
    "Use the glue-in notebook as the main student-note system.",
    "Chapter 1 uses the Interactive Science Notebook, not Guided Notes.",
    "The INB replaces Guided Notes.",
    "Primary: Interactive Science Notebook.",
    "Bring back the glue-in notebook.",
    "Go back to the Interactive Science Notebook.",
]

# B. Guided Notes demotion, including cases with no notebook token.
GUIDED_DEMOTION = [
    "Guided Notes are optional.",
    "Guided Notes are secondary.",
    "Use Guided Notes only as a backup.",
    "Guided Notes are no longer the main reference artifact.",
    "Guided Notes are replaced by the Interactive Science Notebook.",
    "Guided Notes = secondary.",
    "Guided Notes are a supplement.",
    "Sideline Guided Notes.",
]

# C. Science Journal promoted above Guided Notes.
JOURNAL_PROMOTION = [
    "Science Journal is primary.",
    "The Science Journal becomes the required note system.",
    "The journal replaces Guided Notes for daily notes.",
    "Science Journal is required instead of Guided Notes.",
    "Student notes are kept primarily in the Science Journal.",
    "Science Journal = primary.",
]

# D. Generic note-system role assigned away from Guided Notes.
GENERIC_ROLE = [
    "The official student notes medium is the Interactive Science Notebook.",
    "Primary note system: glue-in notebook.",
    "The note system for Chapter 1 is the glue-in notebook.",
    "Our notes workflow now uses the Interactive Science Notebook.",
    "The student artifact for daily notes is the notebook.",
    "Student notes are kept primarily in the Science Journal.",
]

# E. Retirement, history, negation, and the locked invariant. Must NOT fail.
SAFE_HISTORY = [
    "The Interactive Science Notebook is retired for Chapter 1.",
    "The former notebook workflow was superseded by Guided Notes.",
    "The notebook was once used for student notes but is no longer current.",
    "Do not restore the notebook as the primary note system.",
    "Never restore the notebook as primary.",
    "The notebook must never replace Guided Notes.",
    "The notebook is not primary.",
    "Guided Notes supersede the former notebook workflow.",
    "The notebook was previously the primary system.",
    "Chapter 1 formerly used the notebook workflow.",
    "Guided Notes are the primary structured student-note/reference artifact.",
    "Science Journal is secondary.",
]

# Section 12. Truly unrelated. Not architecture-sensitive and not a failure.
NEUTRAL = [
    "The Friday quiz begins at minute 12.",
    "Reader pages 1–5 contain the Chapter 1 core.",
    "Use pencils for the quiz.",
    "The slideshow has 45 slides.",
    "Students work with a partner.",
]

# Reviewer round-1 bypass attempts (2026-10-05). Architecture changes must not stay neutral.
REVIEWER_BYPASS = [
    "Students glue today's energy sheet into the Interactive Science Notebook.",
    "Paste the vocabulary strip on the next page of the INB.",
    "The glue-in notebook is where students keep the Big Question.",
    "Each student builds an INB for the energy unit.",
    "The notebook architecture for Chapter 1 is glue-in pages with student writing beside them.",
    "Chapter 1 student responses live in the Interactive Science Notebook.",
    "The INB carries the Big Question, the vocabulary, and the daily evidence.",
    "Input pages in the glue-in notebook show the teacher example for energy.",
    "Students create a table of contents in the Interactive Science Notebook.",
    "Foldables belong in the notebook after the vocabulary talk.",
    "The left side of the glue-in notebook is for new learning about energy.",
    "Fourth graders cut, arrange, and glue energy cards in the Interactive Science Notebook.",
    "We collect a completed INB at the end of Chapter 1.",
    "Open the notebook and add the marble drawing from today's investigation.",
    "Glue-in pages are the Chapter 1 place for vocabulary and evidence.",
    "Students may skip Guided Notes when the block runs long.",
    "Teachers can finish the energy lesson without Guided Notes.",
    "We dropped Guided Notes from the daily science routine.",
    "Print Guided Notes only for students who ask.",
    "The Science Journal is the daily home for Chapter 1 answers.",
    "Students answer every Big Question in the Science Journal.",
    "All Chapter 1 writing belongs in the Science Journal.",
    "The journal stands in for the class reference during this chapter.",
    "Teachers grade the Science Journal as the Chapter 1 product students turn in.",
    "The Science Journal carries the vocabulary and the Big Question for the week.",
    "Students rely on the Science Journal for the chapter definitions and examples.",
    "The only written lesson record for Chapter 1 is the Science Journal.",
    "For Chapter 1, class proceeds from the Science Journal alone.",
]
REVIEWER_SAFE = [
    "Guided Notes are primary, and the Science Journal is secondary.",
    "The Science Journal remains secondary.",
    "Guided Notes remain the primary reference for students.",
    "Do not skip Guided Notes.",
    "The notebook was where students kept vocabulary before Chapter 1.",
    "Do not glue energy cards into the INB.",
    "The notebook is not where students keep the Big Question.",
]
# Reviewer round-2 paraphrases. Naming a note system is enough to enter review.
REVIEWER_BYPASS_2 = [
    "Students mount today's energy organizer onto the Interactive Science Notebook.",
    "The INB receives the speed table after the marble trial.",
    "Teachers staple the lesson organizer into each Interactive Science Notebook.",
    "The notebook architecture stores Monday's evidence log.",
    "Students file the quiz reflection under the INB tab labeled Energy.",
    "Interactive Science Notebook setup happens before the first science block.",
    "The class notebook workflow houses observation logs from the ramp.",
    "Tape the diagram strip across the Interactive Science Notebook.",
    "The INB pocket chart tracks fast versus slow motion.",
    "Students assemble a flip book as their Interactive Science Notebook.",
    "Each child maintains an INB section called Causes of Change.",
    "Output pages inside the Interactive Science Notebook show student explanations of motion.",
    "A composition book captures the full Chapter 1 record for each student.",
    "Paste-ins are how Chapter 1 vocabulary and evidence get into student hands.",
    "Sort-and-glue pieces for the energy lesson go on a composition book page.",
    "Guided Notes can sit out on days when the block is short.",
    "Teachers may set Guided Notes aside after the read-aloud.",
    "Guided Notes are a nice-to-have after the investigation.",
    "Fast finishers may pick up Guided Notes if they want more practice.",
    "The daily lesson does not depend on Guided Notes.",
    "Guided Notes are enrichment for students who finish early.",
    "We pulled Guided Notes off the Monday materials list.",
    "Guided Notes are extra copies in the back cabinet.",
    "Guided Notes are not part of the Monday through Thursday routine.",
    "A half-sheet handout now covers what Guided Notes used to cover.",
    "The Science Journal is the lesson anchor students study before the quiz.",
    "Definitions for the chapter sit in the Science Journal.",
    "The journal is the chapter packet students bring to class.",
    "Teachers check the Science Journal for the chapter's worked examples.",
    "Class discussion follows the Science Journal page by page.",
    "The Science Journal is the piece students take to the quiz.",
    "Every definition the class needs is copied onto the Science Journal.",
    "The journal functions as the class reference packet this week.",
    "Students consult the Science Journal when a definition slips their mind.",
    "For the energy chapter, the Science Journal is the student book.",
]

# Phase 6.1H — alternate media and unknown media assigned an instructional role.
BOUNDARY_BAD = [
    "The binder is now the official student note system.",
    "Students will keep their primary Chapter 1 notes in a spiral.",
    "Use the handout packet instead of Guided Notes for all Chapter 1 notes.",
    "The logbook becomes the main student reference artifact.",
    "Our new notes medium is the blue binder.",
    "Students no longer need Guided Notes; use the spiral instead.",
    "The binder replaces the current student notes system.",
]
BOUNDARY_SAFE = [
    "Put the worksheet in your folder.",
    "Keep your notes in your folder.",
    "Place the handout in your folder.",
    "Turn in the graded worksheet.",
    "Your lab report is unfinished; place it in your folder and finish it next class.",
]
COUSIN_BAD = [
    "Use a binder system for all student notes.",
    "Students keep all science notes in a spiral.",
    "The portfolio is the official note medium.",
    "Replace Guided Notes with the packet system.",
    "The logbook is the main reference artifact.",
    "Primary science notes: blue binder.",
    "The folder system becomes the main notes system.",
    "The folder is the primary note system.",
    "Use the folder instead of Guided Notes.",
    "The folder system replaces Guided Notes.",
    "Students keep their primary notes in the folder.",
    "The folder is the official science-notes medium.",
    "The accordion file is now the official student note system.",
    "The manila envelope is the main reference artifact.",
]
FOLDER_SAFE = [
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
]
# Phase 6.1J — non-copular role language is a live role, with or without retirement.
NON_COPULAR = [
    "Students keep the main reference artifact in a spiral.",
    "Keep the main reference artifact in a spiral.",
    "Put the primary reference artifact in the portfolio.",
    "Students maintain the official notes medium in the digital notebook.",
    "Use the accordion file for the required note system.",
    "Store all primary student notes in the composition book.",
    "Keep the main student reference in the Voice-Memo Vault.",
    "Students record all official science notes in the packet system.",
    "Use the accordion file as the note system.",
    "Keep the notes medium in a spiral.",
    "Use a binder for the note taking system.",
    "The spiral is preferred over Guided Notes.",
]
RETIREMENT_PLUS_ROLE = [
    "Aside from the retired notebook, keep the main reference artifact in a spiral.",
    "Retired notebook workflow aside, students keep the main reference artifact in a Voice-Memo Vault.",
    "Although the notebook is historical, keep the main reference artifact in a spiral.",
    "The notebook is legacy, but students keep the main reference artifact in a spiral.",
    "Historically we used glue-in pages, so keep the main reference artifact in a spiral.",
    "The notebook is no longer current; however students keep the main reference artifact in a spiral.",
    "Despite retiring INB, students keep the main reference artifact in a spiral.",
    "The notebook is not current, so the binder is the official notes system.",
    "The notebook is retired, but put the primary reference artifact in the portfolio.",
    "Although the notebook is historical, use the accordion file for the required note system.",
    "The notebook is no longer the primary note system, while primary notes will be the binder.",
    "The glue-in notebook is historical, not current, so official notes move to the binder.",
    "Never replace posters, the retired notebook sits aside, and students keep the main reference artifact on the cart.",
    "Do not replace posters, the notebook was common in the building, and students keep the main reference artifact on the cart.",
    "Guided Notes remain primary while the notebook is retired and students keep the main reference artifact.",
    "Guided Notes are primary and the notebook was home to vocabulary sheets and students keep the main reference artifact.",
    "Guided Notes are primary keep the main reference artifact.",
    "Guided Notes are primary so keep the main reference artifact.",
    "Guided Notes are primary so store the main reference artifact.",
    "Guided Notes remain primary and keep the main reference artifact.",
]
CURRENT_INVARIANT = [
    "Guided Notes are primary.",
    "Guided Notes are the primary structured student-note/reference artifact.",
    "Science Journal is secondary.",
    "The Science Journal remains secondary.",
    "The notebook is historical, and Guided Notes remain primary.",
    "Do not make the notebook primary.",
    "Never replace Guided Notes with the notebook.",
    "The notebook must never replace Guided Notes.",
    "Do not restore the notebook as the primary note system.",
]

# Phase 6.1I — retirement language must not wash a live role in the same clause.
SAME_CLAUSE_MASK = [
    "Although the notebook is historical, primary notes will be the spiral.",
    "The notebook is retired, but the binder is now the required note system.",
    "The glue-in system is legacy, so the portfolio is now the official notes medium.",
    "The notebook was superseded, but the binder is the main notes system.",
    "The notebook is no longer current, so the spiral replaces Guided Notes.",
    "Chapter 2 still uses notebooks historically, but for all chapters the binder is the primary note system.",
    "Although the notebook is retired, the accordion file is the required notes medium.",
    "Glue-in pages are retired, so the folder system becomes the main notes system.",
    "The notebook is historical, while the digital notebook becomes the main student reference artifact.",
    "INB is legacy, so the portfolio is the official notes medium.",
    "The notebook is no longer the primary note system, and the binder is the primary note system.",
    "Glue-in pages are no longer current, so the portfolio is the official note system.",
    "The notebook is no longer used, and the spiral is the main note system.",
    "The notebook is no longer the primary note system, while primary notes will be the binder.",
    "The glue-in system is no longer primary, so main notes shift into the spiral.",
    "The glue-in notebook is historical, not current, so official notes move to the binder.",
]
PURE_RETIREMENT = [
    "The notebook is historical.",
    "The Interactive Science Notebook is retired for Chapter 1.",
    "The former glue-in system was superseded by Guided Notes.",
    "The notebook is no longer the primary note system.",
    "Historically, students used the notebook workflow.",
    "The legacy notebook architecture is not current.",
    "The notebook is historical, and Guided Notes remain primary.",
    "The notebook is retired; Guided Notes are the primary notes system.",
    "Historically students used glue-in pages, but Guided Notes are primary now.",
    "The old notebook workflow is legacy, and the Science Journal remains secondary.",
]

GRADED_SAFE = [
    "Turn in the graded worksheet.",
    "Collect the graded worksheet.",
    "Your lab report is unfinished; place it in your folder and finish it next class.",
    "Put the unfinished lab report in your folder and finish it next class.",
    "Return the graded lab report to the student after class.",
]

# Section 11. Injected as sentences; every one must be sensitive and fail closed.
CRITICAL = [
    "Guided Notes yield to the notebook architecture starting Monday.",
    "The official student notes medium is the Interactive Science Notebook.",
    "Adopt the glue-in notebook for all student notes.",
    "Switch back to the notebook.",
    "Prefer the Interactive Science Notebook over Guided Notes.",
    "Guided Notes are optional.",
    "Science Journal is primary.",
]


def _read(rel):
    with open(os.path.join(q.REPO, rel), encoding="utf-8") as f:
        return f.read()


def _scan_overrides(overrides, entries=None):
    entries = entries if entries is not None else q.load_allowlist()
    rows = []
    for rel in q.ARCHITECTURE_AUTHORITIES:
        text = overrides.get(rel, _read(rel))
        sensitive, unreviewed, exclusions = q.scan_lines(rel, text.splitlines(), entries)
        rows.append((rel, sensitive, unreviewed, exclusions))
    seen = set()
    for rel, sensitive, _un, _ex in rows:
        for _raw, nc, _verdict, _al in sensitive:
            seen.add((rel, nc))
    stale = q.stale_allowlist_entries(entries, seen)
    unreviewed = [item for _rel, _s, un, _e in rows for item in un]
    return unreviewed, stale, rows


def _expect_fail(sentences):
    bad = []
    for s in sentences:
        if not q.is_architecture_sensitive(s) or not q.is_reactivation(s):
            bad.append(s)
    return bad


def _expect_allowed(sentences):
    bad = []
    for s in sentences:
        if q.is_reactivation(s):
            bad.append(s)
    return bad


def _strip_leading_banner(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        i += 1
    if i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines) and lines[i].strip().startswith(">"):
        del lines[i]
    return "\n".join(lines) + "\n"


def test_banners():
    present = late = 0
    for rel in q.RETIRED_STANDARDS:
        original = _read(rel)
        if q.banner_gaps(original):
            continue
        present += 1
        stripped = _strip_leading_banner(original)
        attacked = stripped + (
            "\n## Historical notes\n\nThe body below is archival.\n\n"
            "> **SUPERSEDED / HISTORICAL.** Guided Notes are PRIMARY. "
            "The notebook architecture is retired and not current.\n"
        )
        if q.banner_gaps(stripped) and q.banner_gaps(attacked):
            late += 1
    return present, late


def test_mutations():
    """Change one architecture word in a real authority. The changed line must fail."""
    cases = [
        ("AGENTS.md",
         "**Guided Notes** are the primary student content/reference artifact",
         "**notebook** is the primary student content/reference artifact"),
        ("docs/planning/CURRENT_DECISIONS.md",
         "the Interactive Science Notebook-primary architecture is **RETIRED**",
         "the Interactive Science Notebook-primary architecture is **PRIMARY**"),
        ("docs/standards/UNIT1_PRODUCT_STANDARD.md",
         "**Science Journal** = secondary",
         "**Science Journal** = primary"),
        ("docs/planning/CURRENT_DECISIONS.md",
         "**Guided Notes are PRIMARY** (current standard:",
         "**Guided Notes are OPTIONAL** (current standard:"),
        ("docs/standards/GUIDED_NOTES_STANDARD.md",
         "> Primary student content/reference artifact.",
         "> The notebook is the primary student content/reference artifact."),
    ]
    ok = 0
    for rel, old, new in cases:
        text = _read(rel)
        if old not in text:
            print("  MUTATION ANCHOR MISSING %s: %r" % (rel, old[:80]))
            continue
        unreviewed, _stale, _rows = _scan_overrides({rel: text.replace(old, new, 1)})
        if unreviewed:
            ok += 1
        else:
            print("  MUTATION DID NOT FAIL %s" % rel)
    return ok, len(cases)


def test_stale():
    """Delete, move, and rewrite allowlist identity. Each must report a stale entry."""
    entries = q.load_allowlist()
    ok = 0

    # 1. Delete an allowlisted line from the file.
    rel = "docs/planning/CURRENT_DECISIONS.md"
    needle = "- Notebook system validated (historical"
    text = _read(rel)
    if needle not in text:
        print("  STALE ANCHOR MISSING", needle)
    else:
        deleted = "\n".join(line for line in text.splitlines() if needle not in line)
        _un, stale, _rows = _scan_overrides({rel: deleted}, entries)
        if any(needle.split("(")[0].strip("*- ")[:24].lower() in (e.get("normalized") or "") or "notebook system validated" in (e.get("normalized") or "") for e in stale):
            ok += 1
        else:
            print("  DELETE did not stale the notebook-system entry", [e.get("normalized", "")[:60] for e in stale])

    # 2. Move an authority path on an otherwise exact entry.
    moved = []
    changed = False
    for e in entries:
        e2 = dict(e)
        if not changed and e.get("file") == "AGENTS.md":
            e2["file"] = "docs/MOVED_AGENTS.md"
            changed = True
        moved.append(e2)
    _un, stale, _rows = _scan_overrides({}, moved)
    if any(e.get("file") == "docs/MOVED_AGENTS.md" for e in stale):
        ok += 1
    else:
        print("  MOVE did not report a path mismatch")

    # 3. Rewrite the normalized text of one entry.
    rewritten = []
    changed = False
    for e in entries:
        e2 = dict(e)
        if not changed and e.get("file") == "docs/chapter-01/CH1_GOLD_STANDARD_PROPAGATION_SPEC.md":
            e2["normalized"] = (e.get("normalized") or "") + " rewritten"
            e2["sha256"] = q.sha256_of(e2["normalized"])
            changed = True
        rewritten.append(e2)
    _un, stale, _rows = _scan_overrides({}, rewritten)
    if any((e.get("normalized") or "").endswith(" rewritten") for e in stale):
        ok += 1
    else:
        print("  REWRITE did not report a stale normalized entry")
    return ok, 3


def test_scope():
    """Chapter 2–7 table rows are excluded. Chapter 1 rows and prose are not."""
    sample = "\n".join([
        "# PRODUCTION MANIFEST",
        "",
        "## Chapter 1 — Energy Causes Change",
        "| P11 | The notebook is the primary note system |",
        "",
        "## Chapter 2 — Moving Objects Have Energy",
        "| P11 | The notebook is the primary note system |",
        "",
        "## Chapter 5 — Collisions Transfer Energy",
        "| P4 | Adopt the glue-in notebook for all student notes |",
        "",
        "## Chapter 7 — Solving Problems",
        "| P4 | Science Journal is primary |",
        "",
        "## Student Note Architecture (current)",
        "Guided Notes yield to the notebook architecture starting Monday.",
        "",
        "## Chapter 3 — Energy and Speed Are Related",
        "> Guided Notes are optional for the whole unit.",
        "",
    ])
    # Scan only this synthetic manifest; other authorities stay canonical so the
    # real allowlist does not go stale for this structural check. We inspect the
    # manifest result directly.
    _sensitive, unreviewed, exclusions = q.scan_lines(
        "production/PRODUCTION_MANIFEST.md", sample.splitlines(), []
    )
    excl_scopes = [scope for _raw, _nc, scope in exclusions]
    unrev_text = " ".join(raw for raw, _nc in unreviewed)
    ok = 0
    # three later-chapter rows excluded
    if excl_scopes.count("ch2") == 1 and excl_scopes.count("ch5") == 1 and excl_scopes.count("ch7") == 1:
        ok += 3
    else:
        print("  SCOPE exclusions", excl_scopes)
    # Chapter 1 row, the global yield sentence, and the Chapter 3 prose quote still fail.
    ch1_failed = "primary note system" in unrev_text and "chapter 1" not in unrev_text.lower()
    # The ch1 row text is "The notebook is the primary note system" and must be unreviewed.
    # The same words inside the ch2 row must not be unreviewed twice. Count occurrences.
    ch1_hits = [raw for raw, _nc in unreviewed if "primary note system" in raw.lower()]
    yield_hits = [raw for raw, _nc in unreviewed if "yield" in raw.lower()]
    prose_hits = [raw for raw, _nc in unreviewed if "optional" in raw.lower()]
    if len(ch1_hits) == 1:
        ok += 1
    else:
        print("  CH1 ROW hits", ch1_hits)
    if len(yield_hits) == 1:
        ok += 1
    else:
        print("  GLOBAL hits", yield_hits)
    if len(prose_hits) == 1:
        ok += 1
    else:
        print("  PROSE hits", prose_hits)
    if ch1_failed:
        pass
    return ok, 6


def main():
    checks = []

    def add(name, got, total):
        checks.append((name, got, total))
        print("%s: %d/%d" % (name, got, total))

    add("A notebook reactivation", len(NOTEBOOK_REACTIVATION) - len(_expect_fail(NOTEBOOK_REACTIVATION)), len(NOTEBOOK_REACTIVATION))
    for s in _expect_fail(NOTEBOOK_REACTIVATION):
        print("  MISSED A:", s)
    add("B guided-notes demotion", len(GUIDED_DEMOTION) - len(_expect_fail(GUIDED_DEMOTION)), len(GUIDED_DEMOTION))
    for s in _expect_fail(GUIDED_DEMOTION):
        print("  MISSED B:", s)
    add("C science-journal promotion", len(JOURNAL_PROMOTION) - len(_expect_fail(JOURNAL_PROMOTION)), len(JOURNAL_PROMOTION))
    for s in _expect_fail(JOURNAL_PROMOTION):
        print("  MISSED C:", s)
    add("D generic note-system role", len(GENERIC_ROLE) - len(_expect_fail(GENERIC_ROLE)), len(GENERIC_ROLE))
    for s in _expect_fail(GENERIC_ROLE):
        print("  MISSED D:", s)
    add("E historical/retirement/invariant", len(SAFE_HISTORY) - len(_expect_allowed(SAFE_HISTORY)), len(SAFE_HISTORY))
    for s in _expect_allowed(SAFE_HISTORY):
        print("  FALSE E:", s)
    neutral_bad = [s for s in NEUTRAL if q.is_architecture_sensitive(s) or q.is_reactivation(s)]
    add("neutral unrelated", len(NEUTRAL) - len(neutral_bad), len(NEUTRAL))
    for s in neutral_bad:
        print("  FALSE NEUTRAL:", s)
    add("reviewer bypass sentences", len(REVIEWER_BYPASS) - len(_expect_fail(REVIEWER_BYPASS)), len(REVIEWER_BYPASS))
    for s in _expect_fail(REVIEWER_BYPASS):
        print("  MISSED REVIEWER:", s)
    add("reviewer round-2 paraphrases", len(REVIEWER_BYPASS_2) - len(_expect_fail(REVIEWER_BYPASS_2)), len(REVIEWER_BYPASS_2))
    for s in _expect_fail(REVIEWER_BYPASS_2):
        print("  MISSED REVIEWER 2:", s)
    add("reviewer safe sentences", len(REVIEWER_SAFE) - len(_expect_allowed(REVIEWER_SAFE)), len(REVIEWER_SAFE))
    for s in _expect_allowed(REVIEWER_SAFE):
        print("  FALSE REVIEWER SAFE:", s)
    add("non-copular live role", len(NON_COPULAR) - len(_expect_fail(NON_COPULAR)), len(NON_COPULAR))
    for s in _expect_fail(NON_COPULAR):
        print("  MISSED NON-COPULAR:", s)
    add("retirement plus non-copular role", len(RETIREMENT_PLUS_ROLE) - len(_expect_fail(RETIREMENT_PLUS_ROLE)), len(RETIREMENT_PLUS_ROLE))
    for s in _expect_fail(RETIREMENT_PLUS_ROLE):
        print("  MISSED RETIREMENT+ROLE:", s)
    add("current invariant/negation", len(CURRENT_INVARIANT) - len(_expect_allowed(CURRENT_INVARIANT)), len(CURRENT_INVARIANT))
    for s in _expect_allowed(CURRENT_INVARIANT):
        print("  FALSE INVARIANT:", s)

    # Every sensitivity alternative must also be a competing live role.
    drift = []
    for i, part in enumerate(q.ARCH_ROLE_PARTS):
        covered = False
        for sample in q.ARCH_ROLE_EXEMPLARS:
            c = q.normalize(sample)
            if not q.re.search(part, c):
                continue
            covered = True
            if not (q.has_architecture_role(c) and q.competing_live_role(c) and q.classify_clause(c) == "unreviewed"):
                drift.append((i, sample))
        if not covered:
            drift.append((i, "NO EXEMPLAR"))
    add("role-alternative consistency", 0 if drift else 1, 1)
    for item in drift:
        print("  DRIFT:", item)

    # Auto-safe and an unapproved live role cannot both be true.
    corpus = []
    corpus += NON_COPULAR + RETIREMENT_PLUS_ROLE + PURE_RETIREMENT + CURRENT_INVARIANT
    corpus += FOLDER_SAFE + GRADED_SAFE + SAME_CLAUSE_MASK + BOUNDARY_BAD + BOUNDARY_SAFE
    corpus += q.ARCH_ROLE_EXEMPLARS
    washed = []
    for sample in corpus:
        for clause in q.split_clauses(sample):
            reason = q.auto_safe_reason(clause)
            if reason and q.competing_live_role(clause):
                washed.append((reason, clause))
    add("auto-safe excludes live role", 0 if washed else 1, 1)
    for item in washed:
        print("  WASHED:", item)

    add("same-clause retirement mask", len(SAME_CLAUSE_MASK) - len(_expect_fail(SAME_CLAUSE_MASK)), len(SAME_CLAUSE_MASK))
    for s in _expect_fail(SAME_CLAUSE_MASK):
        print("  MISSED MASK:", s)
    add("pure retirement safe", len(PURE_RETIREMENT) - len(_expect_allowed(PURE_RETIREMENT)), len(PURE_RETIREMENT))
    for s in _expect_allowed(PURE_RETIREMENT):
        print("  FALSE RETIREMENT:", s)
    # A global claim under a Chapter 2 heading is prose, not a register row.
    sample = "\n".join([
        "## Chapter 2 — Moving Objects Have Energy",
        "Chapter 2 still uses notebooks historically, but for all chapters the binder is the primary note system.",
        "| P11 | Interactive Science Notebook | chapter-02 | RELEASED |",
        "",
    ])
    _s, unreviewed, exclusions = q.scan_lines("production/PRODUCTION_MANIFEST.md", sample.splitlines(), [])
    global_hit = any("binder" in raw.lower() for raw, _nc in unreviewed)
    row_excluded = any(scope == "ch2" for _raw, _nc, scope in exclusions)
    add("global claim not excluded by chapter heading", 1 if global_hit and row_excluded else 0, 1)
    if not global_hit or not row_excluded:
        print("  SCOPE global", global_hit, "row", row_excluded, unreviewed, exclusions)
    add("boundary A-G fail closed", len(BOUNDARY_BAD) - len(_expect_fail(BOUNDARY_BAD)), len(BOUNDARY_BAD))
    for s in _expect_fail(BOUNDARY_BAD):
        print("  MISSED BOUNDARY:", s)
    boundary_safe_bad = [s for s in BOUNDARY_SAFE if q.is_architecture_sensitive(s) or q.is_reactivation(s)]
    add("boundary H-L folder storage", len(BOUNDARY_SAFE) - len(boundary_safe_bad), len(BOUNDARY_SAFE))
    for s in boundary_safe_bad:
        print("  FALSE BOUNDARY SAFE:", s)
    add("cousin alternate-media", len(COUSIN_BAD) - len(_expect_fail(COUSIN_BAD)), len(COUSIN_BAD))
    for s in _expect_fail(COUSIN_BAD):
        print("  MISSED COUSIN:", s)
    folder_bad = [s for s in FOLDER_SAFE if q.is_architecture_sensitive(s) or q.is_reactivation(s)]
    add("safe folder storage", len(FOLDER_SAFE) - len(folder_bad), len(FOLDER_SAFE))
    for s in folder_bad:
        print("  FALSE FOLDER:", s)
    graded_bad = [s for s in GRADED_SAFE if q.is_architecture_sensitive(s) or q.is_reactivation(s)]
    add("graded-work workflow", len(GRADED_SAFE) - len(graded_bad), len(GRADED_SAFE))
    for s in graded_bad:
        print("  FALSE GRADED:", s)
    add("critical injections", len(CRITICAL) - len(_expect_fail(CRITICAL)), len(CRITICAL))
    for s in _expect_fail(CRITICAL):
        print("  MISSED CRITICAL:", s)

    present, late = test_banners()
    add("retired leading banners", present, len(q.RETIRED_STANDARDS))
    add("late-body banner attacks rejected", late, len(q.RETIRED_STANDARDS))

    m_ok, m_n = test_mutations()
    add("allowlist mutations fail", m_ok, m_n)
    s_ok, s_n = test_stale()
    add("stale/move/delete allowlist", s_ok, s_n)
    h_ok, h_n = test_scope()
    add("chapter-scoped row handling", h_ok, h_n)

    _rows, _retired, stale = q.analyze(q.load_allowlist())
    unreviewed = sum(len(u) for _r, _s, u, _e in _rows)
    live_ok = unreviewed == 0 and not stale and not _retired
    add("live tree unreviewed+stale+banners", 1 if live_ok else 0, 1)
    if not live_ok:
        print("  live unreviewed", unreviewed, "stale", len(stale), "banner", len(_retired))

    failed = [c for c in checks if c[1] != c[2]]
    print("RESULT:", "PASS" if not failed else "FAIL")
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
