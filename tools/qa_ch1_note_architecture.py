#!/usr/bin/env python3
"""Chapter 1 note-architecture FAIL-CLOSED guardrail (Phase 6.1H).

Concept gate, not sentence-shape regexes.

For each ACTIVE ARCHITECTURE AUTHORITY (scanned WHOLE FILE), a clause is
architecture-sensitive when it:

  - names Guided Notes, the Science Journal, or the retired notebook family, or
  - assigns any medium an instructional note-system role (primary notes, note system,
    official notes medium, replaces Guided Notes, and the same family of phrases).

The student folder is storage. Bare "folder" does not enter review. "Folder system",
"primary notes in the folder", and "folder replaces Guided Notes" do.

Role language is enough by itself. "The accordion file is now the official student
note system" fails closed even though "accordion file" is not a known medium.

A sensitive clause must then be:

  1. an exact normalized match in the reviewed allowlist
     (qa/baselines/ch1_note_architecture_allowlist.json), or
  2. a clause-local auto-safe statement (notebook retirement / negation / past-tense
     history, or a clear restatement of the locked invariant:
     Guided Notes primary, Science Journal secondary),

otherwise it FAILS CLOSED (unreviewed). A new architecture line is not approved
merely because it sounds plausible.

Chapter 2–7 register rows (markdown table rows under a Chapter 2–7 heading) are
OUT OF SCOPE — PHASE 7.1+. Exclusion is structural (heading + row), not "the line
says notebook." Prose and global statements stay in scope. Chapter 1 rows stay
in scope.

Retired notebook standards are banner-gated: only the FIRST contiguous markdown
blockquote immediately following the title satisfies the gate.

Usage:
    .venv/bin/python tools/qa_ch1_note_architecture.py [--report qa/reports/X.md] [--list]
"""
import argparse, hashlib, json, os, re, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ALLOWLIST = os.path.join(REPO, "qa/baselines/ch1_note_architecture_allowlist.json")

OUT_OF_SCOPE = "OUT OF SCOPE — PHASE 7.1+"

ARCHITECTURE_AUTHORITIES = [
    "AGENTS.md",
    "production/PRODUCTION_MANIFEST.md",
    "docs/planning/CURRENT_DECISIONS.md",
    "docs/standards/GUIDED_NOTES_STANDARD.md",
    "docs/standards/UNIT1_PRODUCT_STANDARD.md",
    "docs/chapter-01/CH1_GOLD_STANDARD_PROPAGATION_SPEC.md",
]

RETIRED_STANDARDS = [
    "docs/planning/SLIDE_TO_NOTEBOOK_MODELING_STANDARD.md",
    "docs/planning/INTERACTIVE_SCIENCE_NOTEBOOK_STANDARD.md",
    "docs/planning/STUDENT_NOTES_STANDARD.md",
]

# --------------------------------------------------------------------------- normalization

def normalize(s):
    s = s.lower()
    s = re.sub(r"[\u2018\u2019\u201B'`]", "", s)          # apostrophes/backticks -> join
    s = re.sub(r"[-–—/]", " ", s)                          # hyphens/dashes/slashes -> space
    s = re.sub(r"[^\w\s=:;]", " ", s)                      # drop punctuation except = : ;
    s = re.sub(r"\s+", " ", s).strip()
    return s


def sha256_of(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_clauses(line):
    return [c for c in re.split(r"[.;](?:\s+|$)", line) if c.strip()]


# --------------------------------------------------------------------------- entities
# Longer phrases are listed first inside each alternation. Matching is on normalized text.

NOTEBOOK = (
    r"interactive science notebook|interactive notebook|glue in notebook|glue in pages|glue in system|"
    r"notebook architecture|notebook workflow|notebook system|composition book|paste ins|"
    r"sort and glue|notebooks?|\binb\b"
)
GUIDED = r"guided notes|student guided notes|premium guided notes|structured notes"
JOURNAL = r"science journal|the journal"
GENERIC = (
    r"student notes medium|notes medium|student note system|note taking system|"
    r"student notes|notes system|note system|note taking|student artifact|"
    r"reference artifact|note format|notes workflow|student note reference artifact|"
    r"student note"
)

NB_RE = re.compile(r"\b(?:%s)\b" % NOTEBOOK)
GN_RE = re.compile(r"\b(?:%s)\b" % GUIDED)
SJ_RE = re.compile(r"\b(?:%s)\b" % JOURNAL)
GEN_RE = re.compile(r"\b(?:%s)\b" % GENERIC)

# Role / action concepts. Bare "core", "standard", "over", and "use" are intentionally
# not universal triggers: they are ubiquitous and do not by themselves assign a note-system
# role. Notebook/journal adoption verbs and notes-medium assignment are handled separately.
ROLE_RE = re.compile(
    r"\b(?:primary|primarily|secondary|main|default|official|required|optional|preferred|backup)\b"
)
ADOPT_RE = re.compile(
    r"\b(?:adopts?|adopted|adopting|switch(?:es|ed|ing)?|restores?|restored|reinstates?|"
    r"returns?|prefers?|preferred|favou?rs?|favou?red|"
    r"reverts?|reverted|revert|go back|come back|bring back|back to)\b"
)
PREFER_RE = re.compile(
    r"\b(?:yields?|priority)\b|gives way|rather than|instead of|\binstead\b"
)
# Demotion paraphrases of optional/secondary. They assign a lesser role to a note system.
DEMOTE_RE = re.compile(
    r"\b(?:supplemental|supplement|sidelined|sideline|paused|pause|demoted|demote|demoting|"
    r"discontinued|discontinue|abandoned|abandon)\b"
)
# Guided Notes removed from the routine without using the word "optional".
GN_SKIP_RE = re.compile(
    r"\b(?:skip|skips|skipped|skipping|without|dropped|omit|omits|omitted)\b[^;.]{0,60}\bguided notes\b"
    r"|"
    r"\bguided notes\b[^;.]{0,40}\b(?:only for|only if|only when)\b"
)
# The notebook or journal is the place student work lives, even with no rank word.
PLACE_RE = re.compile(
    r"\b(?:where|home|belong|belongs|live|lives|glue|glued|gluing|paste|pasted|"
    r"collect|collected|builds?|built|carry|carries|holds?|kept)\b"
    r"|stands in for|stand in for|daily home|proceeds from"
)
WORK_RE = re.compile(
    r"\b(?:vocabulary|big question|foldables?|sheets?|drawings?|responses?|writing|answers?|"
    r"new learning|energy cards?)\b"
)
REPLACE_RE = re.compile(
    r"\b(?:replac(?:e|es|ed|ing)|supersed(?:e|es|ed|ing)|displac(?:e|es|ed|ing))\b"
)
RETIRE_RE = re.compile(
    r"\b(?:retired|retires|retire|historical|historically|legacy|former|formerly|"
    r"previous|previously|no longer)\b"
)
# Taking / keeping notes in a system, or adopting a system for notes.
NOTES_MEDIUM_RE = re.compile(
    r"\b(?:take|takes|taking|kept|keep|keeping|record|records|write|writes|written)\b"
    r"[^;.]{0,50}\bnotes\b"
    r"|"
    r"\bnotes\b[^;.]{0,30}\bin\b[^;.]{0,30}\b(?:the\s+|their\s+|a\s+)?(?:glue in\s+)?"
    r"(?:interactive science\s+|interactive\s+)?notebook\b"
    r"|"
    r"\b(?:notebooks?|inb|science journal|the journal)\b[^;.]{0,40}\bfor\b[^;.]{0,40}\bnotes\b"
)
# Adoption verbs that reactivate a notebook or journal even without a rank word.
NOTEBOOK_USE_RE = re.compile(
    r"\b(?:use|uses|using|choose|chooses|chosen|selected|designated|becomes?|become|"
    r"remains?|stays?|continues?|continued)\b"
)

ROLE_WORD = r"(?:primary|primarily|main|default|official|required|preferred)"
PAST = r"(?:was|were|once|formerly|previously|used to|had been)"

# Instructional-role language. This is enough to enter review even when the medium
# is unfamiliar ("accordion file"). Bare "folder", "notes", and "spiral" (as in
# "prior-unit spiral") do not match.
# Parts stay separate so competing_live_role cannot drift from this list: a live role
# is any of these matches that is not pure retirement, pure history, or pure negation.
ARCH_ROLE_PARTS = [
    r"\b(?:primary|main|official)\s+(?:student\s+|science\s+|chapter\s+1\s+)*(?:notes?|note)\b",
    r"\b(?:primary|main|official|required)\b[^;.]{0,40}\b(?:note system|notes system|notes medium|note medium|reference artifact|student reference)\b",
    r"\b(?:note system|notes system|student note system|student notes system)\b",
    r"\b(?:notes medium|note medium|student notes medium|science notes medium)\b",
    r"\b(?:note taking system|notes workflow|required notes format)\b",
    r"\b(?:reference artifact|primary reference)\b",
    r"\b(?:all student notes|all science notes|for all notes)\b",
    r"\b(?:packet system|handout packet|folder system|binder system|notes packet|student packet)\b",
    r"\b(?:instead of|rather than)\s+guided notes\b",
    r"\b(?:replace|replaces|replaced|replacing)\b[^;.]{0,40}\bguided notes\b",
    r"\bpreferred over\b[^;.]{0,25}\bguided notes\b",
]
ARCH_ROLE_RE = re.compile("|".join(ARCH_ROLE_PARTS))
# One non-copular sentence per role alternative. Used by the drift regression.
ARCH_ROLE_EXEMPLARS = [
    "Students keep primary notes in a spiral.",
    "Students keep the main reference artifact in a spiral.",
    "Use the accordion file as the note system.",
    "Keep the notes medium in a spiral.",
    "Use a binder for the note taking system.",
    "Keep the reference artifact in a spiral.",
    "Use a binder for all student notes.",
    "Use the packet system for Chapter 1 notes.",
    "Use the spiral instead of Guided Notes.",
    "Replace Guided Notes with the packet system.",
    "The spiral is preferred over Guided Notes.",
]


def entity_flags(clause):
    c = normalize(clause)
    return {
        "notebook": bool(NB_RE.search(c)),
        "guided": bool(GN_RE.search(c)),
        "journal": bool(SJ_RE.search(c)),
        "generic": bool(GEN_RE.search(c)),
    }


def hosts_student_work(clause):
    """Notebook or journal is the place student work is kept, glued, or collected."""
    c = normalize(clause)
    if not (NB_RE.search(c) or SJ_RE.search(c)):
        return False
    if PLACE_RE.search(c) or WORK_RE.search(c):
        return True
    if re.search(r"\b(?:grade|graded|grades|rely|relies|relied)\b", c):
        return True
    if re.search(r"\bthe only\b", c) or re.search(r"\balone\b", c):
        return True
    if re.search(
        r"\bin\b[^;.]{0,25}\b(?:the\s+|their\s+|a\s+|an\s+)?(?:glue in\s+|interactive science\s+)?(?:notebooks?|inb)\b",
        c,
    ):
        return True
    return False


def _journal_is_a_notebook_only(c, e):
    """'The Science Journal is a notebook' names a physical object, not the retired system."""
    if not (e["journal"] and e["notebook"] and not e["guided"]):
        return False
    if ROLE_RE.search(c) or ADOPT_RE.search(c) or PREFER_RE.search(c) or REPLACE_RE.search(c) or RETIRE_RE.search(c):
        return False
    if hosts_student_work(c):
        return False
    return bool(re.search(r"\b(?:is|are)\s+a\s+notebook\b", c))


def has_architecture_role(clause):
    """True when the clause assigns an instructional note-system role to some medium."""
    return bool(ARCH_ROLE_RE.search(normalize(clause)))


def is_sensitive(clause):
    """True when the clause could alter Chapter 1 student-note architecture."""
    c = normalize(clause)
    # Role language is sufficient even for an unknown medium. Bare folder storage
    # ("put the worksheet in your folder") does not match.
    if has_architecture_role(c):
        return True
    e = entity_flags(c)
    if not any(e.values()):
        return False
    if _journal_is_a_notebook_only(c, e):
        return False
    # Naming Guided Notes, the Science Journal, or the retired notebook family is itself
    # architecture-sensitive. A new sentence cannot hide by avoiding the word "primary".
    if e["notebook"] or e["guided"] or e["journal"]:
        return True
    if ROLE_RE.search(c) or ADOPT_RE.search(c) or PREFER_RE.search(c) or REPLACE_RE.search(c) or RETIRE_RE.search(c) or DEMOTE_RE.search(c):
        return True
    if (e["notebook"] or e["journal"]) and NOTES_MEDIUM_RE.search(c):
        return True
    if (e["notebook"] or e["journal"]) and NOTEBOOK_USE_RE.search(c):
        return True
    if hosts_student_work(c) or (e["guided"] and GN_SKIP_RE.search(c)):
        return True
    if e["generic"] and (e["notebook"] or e["guided"] or e["journal"]):
        return True
    families = sum(1 for k in ("notebook", "guided", "journal") if e[k])
    if families >= 2:
        return True
    return False


# --------------------------------------------------------------------------- polarity
# Auto-safe is narrow: retirement/history/negation of the notebook, or a clear
# restatement of the locked invariant. Anything else sensitive fails closed.
# Live promotion/demotion is decided before any retirement word can clear the clause.

def _notebook_claim_negated(c):
    """The clause tells the reader not to give the notebook a current role."""
    if _negated_notebook_action(c):
        return True
    if re.search(r"\b(?:must not|should not|cannot)\b[^;.]{0,25}\bretired\b", c):
        return False
    if re.search(r"\b(?:is|are)\s+not\b", c) and NB_RE.search(c):
        return True
    if re.search(r"\b(?:do not|never|must not|should not)\b", c) and NB_RE.search(c):
        if re.search(r"\bnot\b[^;.]{0,15}\bretired\b", c):
            return False
        return True
    return False


def _negated_notebook_action(c):
    if re.search(
        r"\b(?:never|do not|must not|should not|cannot|dont)\b[^;.]{0,60}\b"
        r"(?:restore|make|set|use|adopt|switch|reinstate|return|prefer|promote|declare|establish|bring back|go back|revert)\b"
        r"[^;.]{0,50}\b(?:notebooks?|inb|glue in notebook|interactive science notebook)\b",
        c,
    ):
        return True
    if re.search(
        r"\b(?:notebooks?|inb|glue in notebook|interactive science notebook|notebook architecture|"
        r"notebook workflow|notebook system)\b[^;.]{0,45}\b(?:is|are|remains?|will be|should be|must be)\s+"
        r"(?:not|never|no longer)\b[^;.]{0,25}\b(?:primary|main|required|official|default|preferred)\b",
        c,
    ):
        return True
    if re.search(
        r"\b(?:notebooks?|inb|glue in notebook|interactive science notebook)\b[^;.]{0,40}\b"
        r"(?:must never|never|will not|should not|must not|does not|cannot)\b[^;.]{0,25}\b"
        r"(?:replace|replaces|supersede|supersedes|displace|displaces)\b",
        c,
    ):
        return True
    return False


def _live_notebook_role(c):
    """Present-tense assignment of a primary/main/required/official role to the notebook."""
    nb = r"(?:interactive science notebook|interactive notebook|glue in notebook|notebook architecture|notebook workflow|notebook system|notebooks?|inb)"
    if re.search(r"\b" + ROLE_WORD + r"\b[^;.]{0,60}(?:=|:)\s*(?:the\s+|a\s+|our\s+)?(?:" + nb + r")\b", c):
        return True
    if re.search(
        r"\b" + ROLE_WORD + r"\b[^;.]{0,50}\b(?:is|are|will be|shall be|becomes?|become)\b[^;.]{0,40}\b(?:" + nb + r")\b",
        c,
    ):
        return True
    if re.search(
        r"\b(?:" + nb + r")\b[^;.]{0,18}\b(?:is|are|remains?|stays?|becomes?|become|will be|shall be|should be|must be)\s+"
        r"(?:still\s+|now\s+|again\s+|currently\s+)?(?:the\s+|a\s+|our\s+|its\s+|their\s+)?(?:students?\s+)?"
        + ROLE_WORD + r"\b",
        c,
    ):
        if re.search(r"\b(?:is|are|remains?|stays?|will be|should be|must be)\s+(?:not|never|no longer)\b", c):
            return False
        return True
    if re.search(r"\b(?:" + nb + r")\b[^;.]{0,35}\bas\s+(?:the\s+|a\s+)?" + ROLE_WORD + r"\b", c):
        return True
    if re.search(r"\b(?:" + nb + r")\b\s*=\s*[^;.]{0,25}\b" + ROLE_WORD + r"\b", c):
        return True
    if re.search(
        r"\b(?:make|set|declare|establish|promote)\b[^;.]{0,40}\b(?:" + nb + r")\b[^;.]{0,25}\b" + ROLE_WORD + r"\b"
        r"|"
        r"\b(?:make|set|declare|establish|promote)\b[^;.]{0,25}\b" + ROLE_WORD + r"\b[^;.]{0,40}\b(?:" + nb + r")\b",
        c,
    ):
        return True
    return False


def _notebook_replaces_guided(c):
    if _negated_notebook_action(c):
        return False
    if re.search(
        r"\b(?:" + NOTEBOOK + r")\b[^;.]{0,40}\b(?:replace|replaces|replaced|supersede|supersedes|superseded|displace|displaces)\b(?!\s+by\b)[^;.]{0,30}\bguided notes\b",
        c,
    ):
        return True
    if re.search(
        r"\bguided notes\b[^;.]{0,50}\b(?:replaced|superseded|displaced)\b[^;.]{0,12}\bby\b[^;.]{0,40}\b(?:" + NOTEBOOK + r")\b",
        c,
    ):
        return True
    return False


def _notebook_contrast(c):
    return bool(re.search(
        r"\b(?:instead of|rather than)\s+guided notes\b|\bnot\s+guided notes\b|\bover\s+guided notes\b",
        c,
    )) and bool(NB_RE.search(c))


def notebook_promoted(clause):
    c = normalize(clause)
    if not NB_RE.search(c):
        return False
    if _notebook_claim_negated(c):
        return False
    adopt = bool(ADOPT_RE.search(c)) or bool(re.search(r"\b(?:make|set|declare|establish|promote)\b", c) and _live_notebook_role(c))
    # "make/set" without a successful role link is still promotion when the rank word is present
    if re.search(r"\b(?:make|set|declare|establish|promote)\b", c) and re.search(r"\b" + ROLE_WORD + r"\b", c):
        adopt = True
    notes = bool(NOTES_MEDIUM_RE.search(c))
    role = _live_notebook_role(c)
    contrast = _notebook_contrast(c)
    replaces = _notebook_replaces_guided(c)
    use_nb = bool(NOTEBOOK_USE_RE.search(c)) and bool(re.search(r"\b" + ROLE_WORD + r"\b|\bnotes\b", c))
    host = bool(NB_RE.search(c) and hosts_student_work(c) and not re.search(r"\b" + PAST + r"\b", c))
    if not (adopt or notes or role or contrast or replaces or use_nb or host):
        # Rank word mentioned only inside a retirement label ("notebook-primary architecture is retired").
        return False
    # Past-only history is not a live promotion ("was the primary", "was once used for notes").
    past = bool(re.search(r"\b" + PAST + r"\b", c))
    live = role or contrast or replaces or host or (adopt and not past) or (notes and not past) or (use_nb and not past)
    if past and not live:
        return False
    if RETIRE_RE.search(c) and not live:
        return False
    # "was retired, but is now primary" — live wins. "is retired" alone does not.
    if RETIRE_RE.search(c) and not (role or contrast or replaces or (adopt and not _retired_predicate_only(c)) or (notes and not past)):
        return False
    return True


def _retired_predicate_only(c):
    """Adoption/role words appear, but the clause's predicate is retirement, not a live return."""
    if re.search(r"\b(?:returns?|switch(?:es|ed)?|restore[sd]?|reinstates?|adopts?|adopted|prefers?|preferred)\b", c):
        return False
    return bool(RETIRE_RE.search(c))


def gn_demoted(clause):
    c = normalize(clause)
    if not GN_RE.search(c):
        return False
    # Historical "were optional" corrected in the same clause: "are primary, not optional".
    if re.search(r"\bnot optional\b", c) and re.search(r"\bprimary\b", c):
        return False
    if DEMOTE_RE.search(c):
        if re.search(r"\bprimary\b", c) and re.search(
            r"\bnot\b[^;.]{0,25}\b(?:a\s+)?(?:supplement|supplemental|optional|secondary|backup|paused|sidelined|demoted)\b",
            c,
        ):
            return False
        return True
    # Copula must belong to Guided Notes, not to a later subject in the same clause
    # ("Guided Notes are primary, and the Science Journal is secondary").
    if re.search(
        r"\bguided notes\b\s+(?:are|is|remain|remains|become|becomes|were|stay|stays)\s+"
        r"(?:now\s+|still\s+|the\s+|a\s+)?(?:optional|secondary|backup|supplement|supplemental|paused|sidelined|demoted)\b",
        c,
    ):
        return True
    if re.search(r"\b(?:optional|secondary|backup)\b[^;.]{0,35}\bguided notes\b", c):
        return True
    if re.search(r"\bguided notes\b[^;.]{0,40}\b(?:yield|yields|give way|gives way)\b", c):
        return True
    if re.search(r"\bno longer\b[^;.]{0,40}\b(?:primary|main|required|reference|official)\b", c):
        return True
    if re.search(r"\bonly as a (?:backup|supplement|extra)\b", c):
        return True
    if _notebook_replaces_guided(c):
        return True
    if re.search(
        r"\b(?:science journal|the journal)\b[^;.]{0,40}\b(?:replace|replaces|replaced|supersede|supersedes)\b[^;.]{0,30}\bguided notes\b"
        r"|"
        r"\bguided notes\b[^;.]{0,40}\b(?:replaced|superseded)\b[^;.]{0,12}\bby\b[^;.]{0,30}\b(?:science journal|the journal)\b",
        c,
    ):
        return True
    if re.search(r"\b(?:instead of|rather than)\s+guided notes\b", c) and (SJ_RE.search(c) or NB_RE.search(c)):
        return True
    if GN_SKIP_RE.search(c):
        if re.search(r"\b(?:do not|never|must not|should not)\b[^;.]{0,40}\b(?:skip|omit|drop)\b", c):
            return False
        return True
    return False


def _journal_is_secondary(c):
    return bool(re.search(
        r"\b(?:science journal|the journal)\b[^;.]{0,50}(?:\b(?:is|are|remains?|stays?)\b|=)\s*secondary\b",
        c,
    ))


def journal_promoted(clause):
    c = normalize(clause)
    if not SJ_RE.search(c):
        return False
    own_primary = bool(re.search(
        r"\b(?:science journal|the journal)\b[^;.]{0,45}(?:\b(?:is|are|remains?|becomes?|become)\b|=)\s*"
        r"(?:the\s+)?(?:primary|main|required|official|default|preferred)\b",
        c,
    ))
    if _journal_is_secondary(c) and not own_primary:
        return False
    if own_primary:
        if re.search(r"\b(?:is|are|remains?)\s+not\b", c):
            return False
        return True
    if re.search(
        r"\b(?:primary|main|required|official|default)\b[^;.]{0,40}\b(?:is|are|will be|becomes?)\b[^;.]{0,30}\b(?:science journal|the journal)\b",
        c,
    ):
        return True
    if re.search(
        r"\b(?:science journal|the journal)\b[^;.]{0,40}\b(?:replace|replaces|replaced|supersede|supersedes)\b[^;.]{0,30}\bguided notes\b",
        c,
    ):
        return True
    if re.search(r"\b(?:primarily|mainly)\b", c) and re.search(r"\bnotes\b", c):
        return True
    if NOTES_MEDIUM_RE.search(c) and not re.search(r"\bsecondary\b", c):
        return True
    if hosts_student_work(c) and not _journal_is_secondary(c):
        return True
    return False


def _role_match_negated(c, match):
    """Negation sits against this role phrase. "not current, so official notes" does not."""
    window = c[max(0, match.start() - 22):match.start()]
    return bool(re.search(r"\b(?:no longer|never|not)\b(?:\s+(?:the|a|an|our))?\s*$", window))


def pure_retirement_or_historical_only(clause):
    """Notebook retirement/history, with no separate live role phrase."""
    c = normalize(clause)
    if not NB_RE.search(c):
        return False
    if not (RETIRE_RE.search(c) or re.search(r"\b" + PAST + r"\b", c)):
        return False
    matches = list(ARCH_ROLE_RE.finditer(c))
    if not matches:
        return True
    return all(_role_match_negated(c, m) for m in matches)


def _role_beyond_invariant(c):
    """An architecture role remains after the locked invariant phrasing is removed."""
    stripped = re.sub(
        r"\bguided notes\b[^;.]{0,40}\b(?:are|is|remain|remains|stay|stays)\b(?:\s+(?:now|still|the|a|our|its)){0,3}\s+(?:primary|main)\b(?:(?:\s+(?:structured|student|content|note|notes)){0,4}\s+reference artifact|\s+(?:student\s+)?(?:note|notes)\s+system)?",
        " ",
        c,
    )
    stripped = re.sub(r"\bprimary\b[^;.]{0,40}\bguided notes\b", " ", stripped)
    stripped = re.sub(
        r"\b(?:science journal|the journal)\b[^;.]{0,40}(?:\b(?:is|are|remains?|stays?)\b|=)\s*secondary\b",
        " ",
        stripped,
    )
    return has_architecture_role(stripped)


def pure_negation_of_an_architecture_change(clause):
    """The clause only forbids a notebook or Guided Notes change. A later live role is not covered."""
    c = normalize(clause)
    span = re.search(
        r"\b(?:do not|never|must not|must never|should not)\b[^;.]{0,80}\b(?:restore|make|set|adopt|replace|replaces)\b[^;.]{0,50}\b(?:notebooks?|inb|glue in(?: notebook| pages| system)?|guided notes)\b(?:\s+as\s+(?:the\s+)?(?:primary|main|official)\s+(?:student\s+|science\s+)*(?:notes?|note|reference artifact)\b)?",
        c,
    )
    if not span:
        return False
    later = [m for m in ARCH_ROLE_RE.finditer(c) if m.start() >= span.end() and not _role_match_negated(c, m)]
    return not later


def competing_live_role(clause):
    """Architecture role minus invariant, pure retirement/history, and pure negation.

    Any phrase has_architecture_role() accepts is live here, with or without a copula.
    Retirement wording does not wash a role it does not itself negate.
    Guided Notes being primary does not wash a second role in the same clause.
    """
    c = normalize(clause)
    if not has_architecture_role(c):
        return False
    if pure_negation_of_an_architecture_change(c):
        return False
    if pure_retirement_or_historical_only(c):
        return False
    if invariant_safe(c) and not _role_beyond_invariant(c):
        return False
    return True


def notebook_safe(clause):
    """Retirement, past-tense history, negation, or Guided Notes replacing the notebook.

    Retirement language does not clear a competing live role in the same clause.
    """
    c = normalize(clause)
    if not NB_RE.search(c):
        return False
    if competing_live_role(c):
        return False
    if notebook_promoted(c) or gn_demoted(c) or journal_promoted(c):
        return False
    if _notebook_claim_negated(c):
        return True
    if re.search(
        r"\bguided notes\b[^;.]{0,50}\b(?:supersede|supersedes|replace|replaces)\b[^;.]{0,40}\b(?:" + NOTEBOOK + r")\b",
        c,
    ):
        return True
    if re.search(
        r"\b(?:" + NOTEBOOK + r")\b[^;.]{0,50}\b(?:superseded|replaced)\b[^;.]{0,12}\bby\b",
        c,
    ):
        return True
    if RETIRE_RE.search(c):
        return True
    if re.search(r"\b" + PAST + r"\b", c):
        return True
    # Legacy guided-notes format retired in favor of premium notes (not the notebook).
    return False


def legacy_notes_retired(clause):
    """A legacy Guided Notes format is retired/superseded, and the notebook/journal is not the replacement."""
    c = normalize(clause)
    if not re.search(r"\blegacy\b", c) or not GN_RE.search(c):
        return False
    if NB_RE.search(c) or SJ_RE.search(c):
        return False
    if notebook_promoted(c) or gn_demoted(c) or journal_promoted(c):
        return False
    return bool(RETIRE_RE.search(c) or REPLACE_RE.search(c))


def invariant_safe(clause):
    """Clear restatement of Guided Notes primary and/or Science Journal secondary."""
    c = normalize(clause)
    if notebook_promoted(c) or gn_demoted(c) or journal_promoted(c):
        return False
    gn_primary = bool(re.search(
        r"\bguided notes\b[^;.]{0,60}(?:\b(?:are|is|remain|remains|stay|stays)\b|=)[^;.]{0,40}\b(?:primary|main)\b"
        r"|"
        r"\bguided notes\b[^;.]{0,40}\bas\s+(?:the\s+)?primary\b"
        r"|"
        r"\bprimary\b[^;.]{0,40}\bguided notes\b",
        c,
    )) and bool(GN_RE.search(c))
    sj_secondary = _journal_is_secondary(c)
    if gn_primary and notebook_promoted(c):
        return False
    return gn_primary or sj_secondary


def auto_safe_reason(clause):
    """Why a sensitive clause is auto-safe, or None. Live role assignment is not auto-safe."""
    c = normalize(clause)
    if classify_clause(c) != "safe":
        return None
    if invariant_safe(c):
        return "invariant_safe"
    if re.search(r"\b(?:do not|never|must not|should not)\b[^;.]{0,40}\b(?:skip|omit|drop)\b[^;.]{0,40}\bguided notes\b", c):
        return "retirement_safe"
    if legacy_notes_retired(c):
        return "retirement_safe"
    if _notebook_claim_negated(c):
        return "retirement_safe"
    if re.search(r"\b(?:historical|historically|formerly|previously|was|were|once|in the past|before chapter 1)\b", c):
        return "historical_safe"
    if RETIRE_RE.search(c) or re.search(r"\bsuperseded\b", c):
        return "retirement_safe"
    if notebook_safe(c):
        return "notebook_safe"
    return "notebook_safe"


def classify_clause(clause):
    """'neutral' | 'safe' | 'unreviewed' (FAIL CLOSED).

    A live note-role assignment is decided before retirement/history auto-safe.
    Retirement wording does not clear a competing role in the same clause.
    """
    c = normalize(clause)
    if not is_sensitive(c):
        return "neutral"
    if notebook_promoted(c) or gn_demoted(c) or journal_promoted(c) or competing_live_role(c):
        return "unreviewed"
    if re.search(r"\b(?:do not|never|must not|should not)\b[^;.]{0,40}\b(?:skip|omit|drop)\b[^;.]{0,40}\bguided notes\b", c):
        return "safe"
    if invariant_safe(c):
        return "safe"
    if notebook_safe(c) or legacy_notes_retired(c):
        return "safe"
    return "unreviewed"


def is_reactivation(text):
    """True if a standalone sentence would FAIL the fail-closed guardrail."""
    for clause in split_clauses(text):
        if classify_clause(clause) == "unreviewed":
            return True
    return False


def is_architecture_sensitive(text):
    """True if any clause enters the architecture review path (not neutral)."""
    for clause in split_clauses(text):
        if is_sensitive(clause):
            return True
    return False


# --------------------------------------------------------------------------- chapter scope

def heading_scope(line):
    """Return (is_heading, scope). scope is None (in scope) or 'ch2'..'ch7'."""
    m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line.strip())
    if not m:
        return False, None
    title = m.group(2)
    if re.search(r"\bChapter\s+1\b", title, re.I) and not re.search(r"\bChapter\s+[2-7]\b", title, re.I):
        return True, None
    m2 = re.search(r"\bChapter\s+([2-7])\b", title, re.I)
    if m2:
        return True, "ch" + m2.group(1)
    return True, None


def is_excluded_row(line, scope):
    """Chapter 2–7 register rows only. Prose under those headings stays in scope."""
    return bool(scope) and line.strip().startswith("|")


# --------------------------------------------------------------------------- allowlist

def load_allowlist(path=None):
    path = path or ALLOWLIST
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _allowlist_lookup(entries):
    lookup = {}
    for e in entries:
        lookup[(e.get("file"), e.get("normalized"))] = e
    return lookup


# --------------------------------------------------------------------------- authority scan

def scan_lines(relpath, lines, allowlist_entries):
    """Scan already-split lines.

    Returns (sensitive, unreviewed, exclusions).
    sensitive items: (raw, normalized, verdict, allowlisted_bool)
    exclusions: (raw, normalized, scope) labeled OUT OF SCOPE — PHASE 7.1+.
    """
    lookup = _allowlist_lookup(allowlist_entries)
    sensitive, unreviewed, exclusions = [], [], []
    scope = None
    for line in lines:
        is_h, new_scope = heading_scope(line)
        # Headings are scanned in the scope that contains them, then the scope updates.
        # A Chapter 2–7 heading is not itself a register row.
        excluded = is_excluded_row(line, scope)
        if excluded and any(entity_flags(line).values()):
            exclusions.append((line.strip(), normalize(line), scope))
            if is_h:
                scope = new_scope
            continue
        if excluded:
            if is_h:
                scope = new_scope
            continue
        for clause in split_clauses(line):
            nc = normalize(clause)
            if not is_sensitive(nc):
                continue
            entry = lookup.get((relpath, nc))
            if entry is not None:
                verdict, allowlisted = "allowlisted", True
            else:
                verdict, allowlisted = classify_clause(nc), False
            sensitive.append((clause.strip(), nc, verdict, allowlisted))
            if verdict == "unreviewed":
                unreviewed.append((clause.strip(), nc))
        if is_h:
            scope = new_scope
    return sensitive, unreviewed, exclusions


def scan_authority(relpath, allowlist_entries, root=None):
    root = root or REPO
    txt = open(os.path.join(root, relpath), encoding="utf-8").read()
    return scan_lines(relpath, txt.splitlines(), allowlist_entries)


def stale_allowlist_entries(entries, seen):
    return [e for e in entries if (e.get("file"), e.get("normalized")) not in seen]


# --------------------------------------------------------------------------- retired-standard banner gate

BANNER_MARKER = re.compile(r"(?i)(?:SUPERSEDED|RETIRED)[^\n]{0,60}HISTORICAL|HISTORICAL[^\n]{0,60}(?:SUPERSEDED|RETIRED)")
BANNER_GUIDED_PRIMARY = re.compile(r"(?i)guided[- ]notes[^\n]{0,40}primary|primary[^\n]{0,40}guided[- ]notes")
BANNER_NOTEBOOK_NOT_CURRENT = re.compile(r"(?i)retired|not[^\n]{0,20}current|no longer[^\n]{0,20}current|do not (?:use|treat)|archived|superseded")


def leading_banner(lines):
    """The first contiguous markdown blockquote immediately after the title/leading heading."""
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return ""
    i += 1  # skip title/heading
    if i < len(lines) and not lines[i].strip():
        i += 1  # skip one blank line after title
    banner = []
    while i < len(lines) and lines[i].strip().startswith(">"):
        banner.append(lines[i].strip())
        i += 1
    return "\n".join(banner)


def banner_gaps(text):
    banner = leading_banner(text.splitlines())
    missing = []
    if not BANNER_MARKER.search(banner):
        missing.append("SUPERSEDED/RETIRED + HISTORICAL marker")
    if not BANNER_GUIDED_PRIMARY.search(banner):
        missing.append("states Guided Notes are PRIMARY")
    if not BANNER_NOTEBOOK_NOT_CURRENT.search(banner):
        missing.append("states notebook/glue-in architecture is not current")
    return missing


def scan_retired_standard(relpath, root=None):
    root = root or REPO
    txt = open(os.path.join(root, relpath), encoding="utf-8").read()
    missing = banner_gaps(txt)
    if not missing:
        return []
    return [(relpath, "retired standard leading banner incomplete (%s)" % "; ".join(missing))]


# --------------------------------------------------------------------------- main

def analyze(entries, root=None):
    root = root or REPO
    authority_rows = []
    for rel in ARCHITECTURE_AUTHORITIES:
        sensitive, unreviewed, exclusions = scan_authority(rel, entries, root=root)
        authority_rows.append((rel, sensitive, unreviewed, exclusions))
    retired_hits = []
    for rel in RETIRED_STANDARDS:
        retired_hits.extend(scan_retired_standard(rel, root=root))
    seen = set()
    for rel, sensitive, _un, _ex in authority_rows:
        for _raw, nc, _verdict, _al in sensitive:
            seen.add((rel, nc))
    stale = stale_allowlist_entries(entries, seen)
    return authority_rows, retired_hits, stale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=None)
    ap.add_argument("--list", action="store_true", help="dump sensitive clauses with classification")
    a = ap.parse_args()

    entries = load_allowlist()
    authority_rows, retired_hits, stale_allowlist = analyze(entries)

    if a.list:
        for rel, sensitive, _un, exclusions in authority_rows:
            for raw, nc, verdict, al in sensitive:
                reason = auto_safe_reason(raw) if verdict == "safe" else ""
                extra = (" | " + reason) if reason else ""
                print("%s | %s | %s%s" % (verdict.upper(), rel, raw[:140], extra))
            for raw, nc, scope in exclusions:
                print("%s | %s | %s | %s" % (OUT_OF_SCOPE, rel, scope, raw[:120]))
        return

    total_sensitive = sum(len(s) for _r, s, _u, _e in authority_rows)
    total_auto_safe = sum(1 for _r, s, _u, _e in authority_rows for _raw, _nc, v, _a in s if v == "safe")
    total_allowlisted = sum(1 for _r, s, _u, _e in authority_rows for _raw, _nc, v, _a in s if v == "allowlisted")
    total_unreviewed = sum(len(u) for _r, _s, u, _e in authority_rows)
    total_excl = sum(len(e) for _r, _s, _u, e in authority_rows)
    total_stale = len(stale_allowlist)

    for rel, _s, unreviewed, _e in authority_rows:
        for raw, nc in unreviewed:
            print("  UNREVIEWED %s: %s" % (rel, raw[:160]))
    for rel, msg in retired_hits:
        print("  BANNER %s: %s" % (rel, msg))
    for e in stale_allowlist:
        print("  STALE-ALLOWLIST %s: %s" % (e.get("file"), e.get("normalized", "")[:100]))

    hits = total_unreviewed + len(retired_hits) + total_stale
    print("Authority files: %d/%d · sensitive clauses: %d · auto-safe: %d · allowlisted: %d · unreviewed: %d · stale allowlist: %d · chapter-scoped exclusions: %d · retired-banner hits: %d"
          % (len(ARCHITECTURE_AUTHORITIES), len(ARCHITECTURE_AUTHORITIES),
             total_sensitive, total_auto_safe, total_allowlisted, total_unreviewed, total_stale, total_excl, len(retired_hits)))
    print("RESULT:", "PASS" if hits == 0 else "FAIL")

    if a.report:
        with open(os.path.join(REPO, a.report), "w") as f:
            f.write("# Chapter 1 Note-Architecture FAIL-CLOSED Scan (Phase 6.1J)\n\n")
            f.write("Tool: `tools/qa_ch1_note_architecture.py`. Result: **%s**\n\n" % ("PASS" if hits == 0 else "FAIL"))
            f.write("Concept gate: a clause that names a student note system and assigns a role enters review. ")
            f.write("Active architecture authorities scanned whole-file: **%d**. Sensitive clauses: **%d** (auto-safe **%d** · allowlisted **%d** · unreviewed **%d**). Stale allowlist: **%d**. Chapter-scoped exclusions (%s): **%d**. Retired-standard leading-banner hits: **%d**.\n\n"
                    % (len(ARCHITECTURE_AUTHORITIES), total_sensitive, total_auto_safe, total_allowlisted, total_unreviewed, total_stale, OUT_OF_SCOPE, total_excl, len(retired_hits)))
            f.write("| Authority | Sensitive | Auto-safe | Allowlisted | Unreviewed | Exclusions |\n|---|---|---|---|---|---|\n")
            for rel, sensitive, unreviewed, exclusions in authority_rows:
                f.write("| `%s` | %d | %d | %d | %d | %d |\n"
                        % (rel, len(sensitive),
                           sum(1 for _r, _n, v, _a in sensitive if v == "safe"),
                           sum(1 for _r, _n, v, _a in sensitive if v == "allowlisted"),
                           len(unreviewed), len(exclusions)))
            if total_auto_safe:
                f.write("\n## Auto-safe clauses\n\n")
                f.write("Retirement or the locked invariant cleared these. A live role assignment in the same clause is not auto-safe.\n\n")
                for rel, sensitive, _un, _ex in authority_rows:
                    for raw, _nc, verdict, _al in sensitive:
                        if verdict != "safe":
                            continue
                        f.write("- `%s` `%s` — %s\n" % (auto_safe_reason(raw), rel, raw[:160].replace("|", "\\|")))
            if total_excl:
                f.write("\n## Chapter-scoped exclusions\n\n")
                f.write("These register rows sit under a Chapter 2–7 heading. They are %s and are not Chapter 1 architecture decisions. A global statement in the same file is still in scope.\n\n" % OUT_OF_SCOPE)
                for rel, _s, _u, exclusions in authority_rows:
                    for raw, _nc, scope in exclusions:
                        f.write("- `%s` (%s) %s\n" % (rel, scope, raw[:180].replace("|", "\\|")))
            f.write("\n| Retired standard | Leading banner |\n|---|---|\n")
            for rel in RETIRED_STANDARDS:
                ok = not scan_retired_standard(rel)
                f.write("| `%s` | %s |\n" % (rel, "PASS" if ok else "FAIL"))

    sys.exit(0 if hits == 0 else 1)


if __name__ == "__main__":
    main()
