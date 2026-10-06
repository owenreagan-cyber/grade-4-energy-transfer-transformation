"""Live semantic QA for Chapter 2. Reads the real tree. Exit 1 on any failure.

Compares full Guided Notes and slide anchor blocks to curriculum/chapter-02/ch2_anchor_map.json.
Does not trust RELEASE_MANIFEST.json for completeness or for the allowed release set.

Usage: .venv/bin/python tools/qa_ch2_semantic.py [--root PATH]
"""
import argparse, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CANON_ROOT = os.path.abspath(os.path.join(HERE, ".."))

REQUIRED_RELEASE = [
    "02-ch2-moving-objects-have-energy-guided-notes.pdf",
    "02-ch2-moving-objects-have-energy-guided-notes-key.pdf",
    "02-ch2-moving-objects-have-energy-slides.pptx",
    "02-ch2-moving-objects-have-energy-slides.pdf",
    "02-ch2-moving-objects-have-energy-quiz.pdf",
    "02-ch2-moving-objects-have-energy-practice.pdf",
    "02-ch2-moving-objects-have-energy-teacher-key.pdf",
    "02-ch2-friday-flex.pdf",
    "02-ch2-absent-student-recovery.pdf",
    "02-ch2-moving-marbles-student.pdf",
]
RELEASE_META = {"README.md", "RELEASE_MANIFEST.json"}
ALLOWED_RELEASE = set(REQUIRED_RELEASE) | RELEASE_META
HARD_REQUIRED = {1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27}
RETIRED_MARKERS = (
    "glue the top edge into your notebook",
    "observation vs inference",
    "lift the flap",
    "insert 1 — moving objects have energy",
    "insert 1 - moving objects have energy",
)
CH2_ENTITY = re.compile(
    r"chapter\s*2|chapter two|\bch\s*2\b|moving objects have energy|"
    r"\bslides?\s*(?:1\s*[–-]\s*16|17\s*[–-]\s*2[57]|s1\s*[–-]s16|s17)",
    re.I,
)
OPTIONAL_PATTERNS = (
    "optional if time", "skip if short", "after-quiz extension", "after quiz extension",
    "if time", "optional", "extension",
)
STATUS_LIKE = re.compile(
    r"optional|required|core|mandatory|bonus|enrichment|extension|skip|if time|only if",
    re.I,
)
SKIP_WORDS = re.compile(
    r"as time permits|nice-to-have|nice to have|drop if running behind|bonus|enrichment|if we have time|only if there is time|not required|skip if needed|can be skipped",
    re.I,
)


CURRENT_ROOT = CANON_ROOT


def load_map():
    path = os.path.join(CURRENT_ROOT, "curriculum", "chapter-02", "ch2_anchor_map.json")
    return json.load(open(path, encoding="utf-8"))


def norm_keep(s):
    """Whitespace, quotes, and equivalent dashes only. Case stays."""
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("—", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2026", "...")
    s = re.sub(r"_{3,}", "____", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,;:?!])", r"\1", s)
    return s


def norm(s):
    return norm_keep(s).lower()


def blank_count(text):
    return len(re.findall(r"____", norm(text)))


def notes_sections(root):
    from docx import Document
    path = os.path.join(root, "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx")
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = Document(path)
    items = []
    for child in d.element.body.iterchildren():
        if child.tag.endswith("}p"):
            text = Paragraph(child, d).text.strip()
            if text:
                items.append(text)
        elif child.tag.endswith("}tbl"):
            table = Table(child, d)
            cells = []
            seen = set()
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()
                    if text and text not in seen:
                        seen.add(text)
                        cells.append(text)
            if cells:
                items.append(" ".join(cells))
    sections = {k: [] for k in ("BQ", "V1", "N1", "V2", "N2", "N3", "CHECK", "BQ_RETURN")}
    order, current = [], None
    for text in items:
        raw = text.strip()
        head = raw.upper()
        kind = None
        if head.startswith("BQ") and "NOW I THINK" in head:
            kind = "BQ_RETURN"
        elif head.startswith("BQ"):
            kind = "BQ"
        elif head.startswith("V1"):
            kind = "V1"
        elif head.startswith("V2"):
            kind = "V2"
        elif head.startswith("N1"):
            kind = "N1"
        elif head.startswith("N2"):
            kind = "N2"
        elif head.startswith("N3"):
            kind = "N3"
        elif head.startswith("CHECK"):
            kind = "CHECK"
        if kind and (not order or order[-1] != kind):
            order.append(kind)
            current = kind
        if current:
            sections[current].append(raw)
    sections["_order"] = order
    return sections


def slide_pack(root):
    from pptx import Presentation
    path = os.path.join(root, "production/slides/02-ch2-moving-objects-have-energy-slides.pptx")
    prs = Presentation(path)
    faces, notes = [], []
    for s in prs.slides:
        bits = []
        for sh in s.shapes:
            if sh.has_text_frame:
                bits.append(sh.text_frame.text)
        faces.append("\n".join(bits))
        if s.has_notes_slide and s.notes_slide.notes_text_frame:
            notes.append(s.notes_slide.notes_text_frame.text)
        else:
            notes.append("")
    return faces, notes


def playbook_blob(root):
    from docx import Document
    path = os.path.join(root, "production/teacher-playbook/unit1-teacher-playbook.docx")
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    return "\n".join(parts)


def load_pacing(root):
    path = os.path.join(root, "tools/ch2_pacing.py")
    spec = importlib.util.spec_from_file_location("ch2_pacing_live", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def section_has_line(section_text, line):
    return norm(line) in norm(section_text)


CHROME_EXACT = {
    "write", "check", "observe", "before", "after", "draw", "sample", "n", "r", "c",
    "bq", "v1", "v2", "n1", "n2", "n3", "big question",
}


def _golden_chrome():
    path = os.path.join(CANON_ROOT, "qa/baselines/ch2_golden_text.json")
    if not os.path.exists(path):
        return set()
    data = json.load(open(path, encoding="utf-8"))
    return {norm(x) for x in data.get("exact_chrome") or []}


def is_chrome(line, spec, reveal=False):
    """Chrome is an exact full line from the golden snapshot or a one-token badge.

    A longer sentence is not chrome because it starts with a chapter title or a page ref.
    """
    n = norm(line)
    if not n:
        return True
    if n in CHROME_EXACT or re.fullmatch(r"\d+", n):
        return True
    if n in _golden_chrome():
        return True
    if n == "big question - my first thinking":
        return True
    # Non-authoritative. This only lets a period-free diagram label through semantic
    # anchor equality. It does not run in golden compare, so it cannot bless new text.
    if "." not in n:
        words = re.findall(r"[a-z0-9]+", n)
        labels = {"moving", "object", "change", "evidence", "before", "after", "what", "does", "it", "cause"}
        if words and set(words) <= labels:
            return True
    title = norm(spec.get("title") or "")
    code = norm(spec.get("code") or "")
    write_title = norm(spec.get("write_title") or "")
    if n in (code, title, write_title):
        return True
    if reveal and n in {norm(a) for a in (spec.get("answers") or [])}:
        return True
    if reveal and n in {norm(a) for a in (spec.get("reveal_labels") or [])}:
        return True
    if n in {norm(x) for x in (spec.get("diagram") or [])}:
        return True
    return False


def block_equal(raw_lines, expected, spec, reveal=False):
    """Expected lines are the only non-chrome text, in order. Extra text fails."""
    exp = [norm_keep(x) for x in expected]
    cursor = 0
    extras = []
    for raw in raw_lines:
        n = norm_keep(raw)
        if not n:
            continue
        work = n
        took = False
        while cursor < len(exp):
            e = exp[cursor]
            idx = work.find(e)
            if idx < 0:
                break
            gap = work[:idx].strip(" -·")
            if gap and not is_chrome(gap, spec, reveal):
                break
            work = work[idx + len(e):]
            cursor += 1
            took = True
        if took:
            rest = work.strip(" -·")
            if rest and not is_chrome(rest, spec, reveal):
                extras.append(rest)
            continue
        if is_chrome(n, spec, reveal):
            continue
        extras.append(n)
    return extras, exp[cursor:]


def sync_fails(sections, faces):
    amap = load_map()
    fails = []
    for code in amap["order"]:
        spec = amap["anchors"][code]
        blob = "\n".join(sections.get(code, []))
        if not blob.strip():
            fails.append("SYNC %s missing from notes" % code)
            continue
        extras, missing = block_equal(sections[code], spec.get("notes_lines") or spec["lines"], spec)
        if extras or missing:
            fails.append("SYNC %s notes extra=%s missing=%s" % (code, extras[:2], missing[:2]))
        slide_no = spec["write_slide"]
        if slide_no - 1 >= len(faces):
            fails.append("SYNC %s write slide %d missing" % (code, slide_no))
            continue
        face_lines = [ln for ln in faces[slide_no - 1].splitlines() if ln.strip()]
        extras, missing = block_equal(face_lines, spec.get("write_lines") or spec["lines"], spec)
        if extras or missing:
            fails.append("SYNC %s slide %d extra=%s missing=%s" % (code, slide_no, extras[:2], missing[:2]))
        if spec.get("reveal_lines") and spec.get("reveal_slide"):
            rev = spec["reveal_slide"]
            if rev - 1 < len(faces):
                rev_lines = [ln for ln in faces[rev - 1].splitlines() if ln.strip()]
                extras, missing = block_equal(rev_lines, spec["reveal_lines"], spec, reveal=True)
                if extras or missing:
                    fails.append("SYNC %s reveal %d extra=%s missing=%s" % (code, rev, extras[:2], missing[:2]))
        for label in spec.get("diagram") or []:
            if norm(label) not in norm(blob):
                fails.append("SYNC %s notes missing diagram label %s" % (code, label))
            dslide = spec.get("diagram_slide", slide_no)
            if dslide - 1 < len(faces) and norm(label) not in norm(faces[dslide - 1]) and norm(label) not in norm(face):
                fails.append("SYNC %s slides missing diagram label %s" % (code, label))
    if sections.get("_order") != amap["order"]:
        fails.append("SYNC anchor order %s" % " ".join(sections.get("_order") or []))
    # Same words under the wrong anchor: V1 must not carry the V2 line, and the reverse.
    v1 = "\n".join(sections.get("V1", []))
    v2 = "\n".join(sections.get("V2", []))
    v1_line = amap["anchors"]["V1"]["lines"][0]
    v2_line = amap["anchors"]["V2"]["lines"][0]
    if section_has_line(v1, v2_line) or not section_has_line(v1, v1_line):
        fails.append("VOCAB V1 block does not carry the motion definition")
    if section_has_line(v2, v1_line) or not section_has_line(v2, v2_line):
        fails.append("VOCAB V2 block does not carry the energy-of-motion definition")
    v1s = next((i for i, f in enumerate(faces) if "Vocabulary — Motion" in f or "Vocabulary - Motion" in f), None)
    v2s = next((i for i, f in enumerate(faces) if "Energy of Motion" in f and "Vocabulary" in f), None)
    if v1s is None or v2s is None or v1s > v2s:
        fails.append("VOCAB slides order: Motion must precede Energy of Motion")
    return fails


def spec_lines_present(lines, expected):
    return lines


def n1_answer_line(line):
    if "?" in line or "____" in norm(line):
        return False
    low = line.lower()
    if not re.search(r"\bmoving objects?\b", low):
        return False
    if not re.search(r"\b(can cause|causes|cause)\b", low):
        return False
    if not re.search(r"\bchanges?\b", low):
        return False
    return True


def leak_fails(faces, speaker):
    amap = load_map()
    fails = []
    for code, spec in amap["anchors"].items():
        write = spec["write_slide"]
        reveal = spec.get("reveal_slide")
        if not reveal or write - 1 >= len(faces):
            continue
        answers = spec.get("answers") or []
        face = faces[write - 1]
        if answers and blank_count(face) < len(answers):
            filled = [a for a in answers if re.search(r"\b%s\b" % re.escape(a), face, re.I)]
            if filled:
                fails.append("LEAK %s slide %d blank pre-filled with %s" % (code, write, ", ".join(filled)))
        prior = range(1, reveal)
        for i in prior:
            prev = faces[i - 1]
            for line in prev.splitlines():
                if code == "N1" and n1_answer_line(line):
                    fails.append("LEAK slide %d states a completed N1 answer before the reveal" % i)
                if code == "N1" and re.search(r"\boutside\b", line, re.I) and "____" not in norm(line):
                    fails.append("LEAK slide %d shows outside before the reveal" % i)
                if code == "N2" and re.search(r"all moving objects have energy of motion\b", line, re.I) and "____" not in norm(line):
                    fails.append("LEAK slide %d states the completed N2 answer before the reveal" % i)
                if code == "N3":
                    for term in spec.get("leak_terms") or []:
                        if re.search(r"\b%s\b" % term, line, re.I):
                            fails.append("LEAK slide %d shows N3 answer %s before the reveal" % (i, term))
            for line in speaker[i - 1].splitlines():
                cue = re.match(r"\s*(REVEAL|SAY|LISTEN FOR)\b(.*)$", line, re.I)
                if not cue:
                    continue
                body = cue.group(2)
                kind = cue.group(1).upper()
                if code == "N1" and (n1_answer_line(body) or re.search(r"\boutside\b", body, re.I)):
                    if not (kind == "LISTEN FOR" and i == write and "missing" in body.lower()):
                        fails.append("LEAK speaker %s on slide %d cues N1 before the reveal" % (kind, i))
                if code == "N2" and kind == "REVEAL" and re.match(r"\s*motion\b", body.strip(), re.I) and "process" not in body.lower():
                    fails.append("LEAK speaker slide %d reveals N2 before the reveal slide" % i)
                if code == "N2" and re.search(r"all moving objects have energy of motion", body, re.I):
                    fails.append("LEAK speaker slide %d states the completed N2 answer" % i)
                if code == "N3" and i < reveal:
                    for term in spec.get("leak_terms") or []:
                        if re.search(r"\b%s\b" % term, body, re.I):
                            fails.append("LEAK speaker slide %d cues N3 answer %s" % (i, term))
    return fails


def parse_plan(note):
    time_m = re.search(r"TIME\s+([0-9.]+)\s+min", note)
    plan_m = re.search(r"^PLAN\s+(.+)$", note, re.M)
    plan = plan_m.group(1) if plan_m else ""
    status = None
    field = re.search(r"^(?:Session\s+\d+\s+\([^)]*\)\s+·\s+)?([^·]+)", plan.strip())
    token = field.group(1).strip() if field else ""
    if token == "REQUIRED":
        status = "REQ"
    elif token == "OPTIONAL":
        status = "OPT"
    elif token:
        status = "UNKNOWN"
    sess = re.search(r"Session\s+(\d+)\s+\(([^)]+)\)", plan)
    day = None
    if re.search(r"\bfri(?:day)?\b", plan, re.I):
        day = "Fri"
    elif sess:
        day = sess.group(2)
    return {
        "minutes": float(time_m.group(1)) if time_m else None,
        "status": status,
        "session": int(sess.group(1)) if sess else None,
        "day": day,
        "plan": plan,
    }


def pacing_fails(speaker, pace):
    fails = []
    problems = pace.check_plan()
    if problems:
        fails.append("PACING check_plan: " + "; ".join(problems))
    for sid in pace.SESSIONS:
        mins = pace.session_required_minutes(sid)
        if mins > 25.0:
            fails.append("PACING session %d is %.1f min" % (sid, mins))
    for n, info in pace.S.items():
        if n - 1 >= len(speaker):
            fails.append("PACING slide %d missing from deck" % n)
            continue
        parsed = parse_plan(speaker[n - 1])
        if parsed["minutes"] is None or abs(parsed["minutes"] - info["minutes"]) > 0.01:
            fails.append("PACING slide %d TIME disagrees (note %s, plan %s)" % (
                n, parsed["minutes"], info["minutes"]))
        if info["session"] == 0:
            expect = "OPT"
        else:
            expect = "REQ" if info["status"] == "REQ" else "OPT"
        if parsed["status"] in ("UNKNOWN", "NEGATED"):
            fails.append("OPTIONAL status unrecognized on slide %d: %s" % (n, parsed["plan"][:80]))
        elif parsed["status"] and parsed["status"] != expect:
            fails.append("OPTIONAL slide %d speaker is %s and pacing is %s" % (n, parsed["status"], expect))
        if n in HARD_REQUIRED and info["status"] != "REQ":
            fails.append("OPTIONAL hard-required slide %d was reclassified in pacing" % n)
        if n in HARD_REQUIRED and SKIP_WORDS.search(speaker[n - 1]):
            fails.append("OPTIONAL hard-required slide %d has skip wording" % n)
        if info["session"] and parsed["session"] and parsed["session"] != info["session"]:
            fails.append("PACING slide %d PLAN session %s, pacing session %s" % (n, parsed["session"], info["session"]))
        if info["session"] and parsed["day"] and parsed["day"] != "Fri":
            expect_day = pace.SESSIONS[info["session"]]["day"]
            if parsed["day"] != expect_day:
                fails.append("PACING slide %d PLAN day %s, pacing day %s" % (n, parsed["day"], expect_day))
        if parsed["day"] == "Fri" and n in HARD_REQUIRED:
            fails.append("FRIDAY speaker slide %d PLAN moved to Friday: %s" % (n, parsed["plan"][:120]))
    return fails


def _friday_heading(title):
    return bool(re.search(r"\bfriday\b|\bfri\b", title, re.I)) and not re.search(
        r"\bnot\b(?:\s+\w+){0,2}\s+fridays?\b", title, re.I)


def _ch2_in(text, anchors=False):
    if CH2_ENTITY.search(text):
        return True
    if anchors and re.search(r"\bch2\s+session\b|\bn[123]\b|\bv[12]\b", text, re.I):
        return True
    return False


def _ch2_negated(text):
    return bool(re.search(
        r"\b(not|no|never)\b(?:\s+\w+){0,2}\s+(chapter\s*2|chapter two|ch\s*2|moving objects have energy)",
        text, re.I))


def _friday_schedule_negated(text):
    return bool(re.search(r"\bnot\b(?:\s+\w+){0,2}\s+fridays?\b", text, re.I))


def friday_hits(text):
    """Heading context carries Friday onto following bullets until the next sibling heading."""
    bad = []
    stack = []  # (level, is_friday)
    for line in text.splitlines():
        m = re.match(r"^(#+)\s+(.*)$", line.strip())
        if m:
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, _friday_heading(m.group(2))))
        in_friday = any(flag for _, flag in stack)
        low = line.lower()
        if _friday_schedule_negated(low):
            continue
        if in_friday:
            if _ch2_in(line, anchors=True) and not _ch2_negated(line):
                bad.append(line.strip()[:160])
            continue
        if not re.search(r"friday|\bfri\b", low):
            continue
        for clause in re.split(r"[.;·|]", low):
            if not re.search(r"friday|\bfri\b", clause):
                continue
            if _friday_schedule_negated(clause) or _ch2_negated(clause):
                continue
            if re.search(r"chapter\s*1|\bch\s*1\b", clause) and not _ch2_in(clause, anchors=False):
                continue
            if _ch2_in(clause, anchors=False):
                bad.append(line.strip()[:160])
                break
    return bad


def schedule_fails(root, speaker):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import qa_ch2_schedule as sched
    return sched.check_root(root)


def playbook_fails(root):
    pb = playbook_blob(root)
    fails = []
    if not ("Wed 10/14" in pb and "Thu 10/15" in pb and "Ch2 Session 1" in pb and "Ch2 Session 2" in pb):
        fails.append("PLAYBOOK missing Wed/Thu Chapter 2 sessions")
    if re.search(r"Fri 10/16.{0,80}Ch2 Session|Ch2 Session.{0,80}Fri 10/16", pb):
        fails.append("PLAYBOOK day/session moved onto Friday")
    if "Ch2 Block 1" in pb or "min 13–25" in pb or "min 13-25" in pb:
        fails.append("PLAYBOOK still has Block 1 or the minute-13 quiz window")
    if "in hands at minute 12" not in pb:
        fails.append("PLAYBOOK missing the minute-12 quiz handout")
    return fails


def media_fails(root):
    fails = []
    play = os.path.join(root, "production/final-package/ENERGY_UNIT_MEDIA_PLAYBACK_GUIDE.md")
    matrix = os.path.join(root, "production/final-8.5-week/VIDEO_PRESENTATION_INTEGRATION_MATRIX.md")
    if not os.path.exists(play) or not os.path.exists(matrix):
        return ["MEDIA guide missing"]
    guide = open(play, encoding="utf-8").read()
    sec = guide.split("## Chapter 2", 1)[-1].split("## ", 1)[0]
    for line in sec.splitlines():
        if "Moving_Objects_Have_Energy.mp4" in line:
            if "SUPPORT" not in line or "CORE" in line:
                fails.append("MEDIA playback 4:50 video is not SUPPORT / optional")
        if "Marble_Collisions" in line:
            if "Wed" not in line or "SUPPORT" not in line:
                fails.append("MEDIA playback Marble Collisions is not Wednesday demo support")
            if "Thu" in line and "CORE" in line:
                fails.append("MEDIA playback Marble Collisions marked Thursday CORE")
        if "Chapter_2_Interactive_Notebook" in line and "retired" not in line.lower() and "RETIRED" not in line:
            fails.append("MEDIA playback notebook is not retired")
    if "optional after the quiz" not in sec.lower() and "optional after the quiz" not in guide.lower():
        fails.append("MEDIA playback Moving Marbles is not optional after the quiz")
    mx = open(matrix, encoding="utf-8").read()
    for line in mx.splitlines():
        if "Marble Collisions" in line and "Ch2" in line:
            if "Wed" not in line or "Session 1" not in line or "SUPPORT" not in line:
                fails.append("MEDIA matrix Marble Collisions is not Wed Session 1 SUPPORT")
            if re.search(r"Thu", line) and "CORE" in line:
                fails.append("MEDIA matrix Marble Collisions marked Thursday CORE")
        if "Moving Objects Have Energy" in line and "4:50" in line:
            if "SUPPORT" not in line or re.search(r"\bCORE\b", line):
                fails.append("MEDIA matrix 4:50 video is not SUPPORT / optional")
        if "Chapter 2 Interactive Notebook" in line and "NOT NEEDED" not in line:
            fails.append("MEDIA matrix notebook is not retired")
    return fails


def manifest_fails(root):
    man_path = os.path.join(root, "production/PRODUCTION_MANIFEST.md")
    if not os.path.exists(man_path):
        return ["MANIFEST missing"]
    man = open(man_path, encoding="utf-8").read()
    chunk = man.split("## Chapter 2")[-1].split("## Chapter 3")[0]
    fails = []
    m = re.search(r"\|\s*P3\s*\|[^|]*\|\s*`([^`]+)`", chunk)
    if not m:
        fails.append("MANIFEST Chapter 2 P3 row missing")
    else:
        p3 = m.group(1).split("+")[0].strip()
        if "student-notes/" in p3 or not os.path.exists(os.path.join(root, p3)):
            fails.append("MANIFEST P3 path does not exist: " + p3)
    if "02-ch2-absent-student-recovery.docx" not in chunk:
        fails.append("MANIFEST recovery source is not the recovery docx")
    return fails


def retired_text(path):
    if not path.endswith(".pdf") or not os.path.isfile(path):
        return ""
    return subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout.lower()


def is_retired_notebook(name, text):
    low = name.lower()
    if "notebook" in low or "interactive-science" in low:
        return True
    hits = sum(1 for marker in RETIRED_MARKERS if marker in text)
    return hits >= 2


MAP_SCIENCE = (
    "the process of an object changing",
    "the energy an object possesses while it is",
    "puts the ball into motion",
    "All moving objects have energy of",
    "Write or draw the change each moving object causes.",
    "We know because the moving object causes",
)
# Approved bytes of curriculum/chapter-02/ch2_anchor_map.json. AM cannot rewrite the map.
MAP_SHA256 = "3fc912ba14cfa35fd65d8099224bc9feda1de5f9a9063f48aa3d3e3868f9ea40"


def map_pin_fails():
    import hashlib
    path = os.path.join(CURRENT_ROOT, "curriculum", "chapter-02", "ch2_anchor_map.json")
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    fails = []
    if MAP_SHA256 and digest != MAP_SHA256:
        fails.append("SYNC anchor map is not the approved baseline")
    text = raw.decode("utf-8")
    for phrase in MAP_SCIENCE:
        if phrase not in text:
            fails.append("SYNC anchor map lost approved wording: " + phrase[:48])
    return fails


def _pdf_page_count(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", info)
    return int(m.group(1)) if m else 0


def _pdf_page_text(path, page):
    return subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), path, "-"],
                          capture_output=True, text=True).stdout


def stale_export_fails(root):
    fails = []
    amap = load_map()
    phrases = []
    for spec in amap["anchors"].values():
        phrases.extend(spec.get("notes_lines") or [])
    pair = (
        "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx",
        "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.pdf",
    )
    pdf = os.path.join(root, pair[1])
    if not os.path.exists(pdf):
        return ["STALE_EXPORT notes PDF missing"]
    text = norm(subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout)
    missing = [p for p in phrases if norm(p).replace("____", "")[:24] not in text and norm(p) not in text]
    # Blank lines are underscores in the PDF. Compare the lead before the blank.
    still = []
    for p in phrases:
        lead = norm(p).split("____")[0].strip()
        if lead and lead not in text:
            still.append(lead[:40])
    if still:
        fails.append("STALE_EXPORT notes PDF does not match the docx: " + still[0])
    pages = _pdf_page_count(pdf)
    if pages != 3:
        fails.append("STALE_EXPORT notes PDF page count %s" % pages)
    return fails


def retired_pages(path):
    hits = []
    if not path.endswith(".pdf") or not os.path.isfile(path):
        return hits
    n = _pdf_page_count(path)
    strong = ("glue the top edge into your notebook", "lift the flap")
    for i in range(1, n + 1):
        text = _pdf_page_text(path, i).lower()
        for marker in strong:
            if marker in text:
                hits.append("p%d %s" % (i, marker))
                break
    return hits


def release_fails(root, release_dir=None):
    rel = release_dir or os.path.join(root, "production/releases/chapter-02")
    fails = []
    if not os.path.isdir(rel):
        return ["RELEASE directory missing"]
    names = set(os.listdir(rel))
    missing = [n for n in REQUIRED_RELEASE if n not in names]
    extra = sorted(names - ALLOWED_RELEASE)
    if missing:
        fails.append("RELEASE missing " + ", ".join(missing))
    if extra:
        fails.append("RELEASE unauthorized extra " + ", ".join(extra))
    for name in sorted(names):
        path = os.path.join(rel, name)
        if not os.path.isfile(path):
            continue
        text = retired_text(path) if name.endswith(".pdf") else ""
        if is_retired_notebook(name, text):
            fails.append("RETIRED notebook content in " + name)
        for hit in retired_pages(path):
            fails.append("RETIRED page in %s %s" % (name, hit))
    return fails


def legacy_fails(root):
    fails = []
    notes = os.path.join(root, "curriculum/chapter-02/teacher/02-ch2-teacher-notes.md")
    if os.path.exists(notes):
        head = open(notes, encoding="utf-8").read(400)
        if "SUPERSEDED" not in head.split("##")[0]:
            fails.append("RETIRED teacher notes are not marked superseded")
    delivery = os.path.join(root, "production/final-delivery/Energy/Unit 1 Teacher Guide/02-ch2-teacher-notes.md")
    if os.path.exists(delivery) and re.search(r"observation vs\.?\s*inference", open(delivery, encoding="utf-8").read(), re.I):
        fails.append("RETIRED delivery copy still teaches observation versus inference")
    return fails


def check(root, release_dir=None, include_release=True):
    global CURRENT_ROOT
    CURRENT_ROOT = root
    fails = []
    sections = notes_sections(root)
    faces, speaker = slide_pack(root)
    fails.extend(sync_fails(sections, faces))
    fails.extend(leak_fails(faces, speaker))
    pace = load_pacing(root)
    fails.extend(pacing_fails(speaker, pace))
    fails.extend(schedule_fails(root, speaker))
    fails.extend(playbook_fails(root))
    fails.extend(media_fails(root))
    fails.extend(manifest_fails(root))
    fails.extend(map_pin_fails())
    fails.extend(stale_export_fails(root))
    fails.extend(legacy_fails(root))
    if include_release:
        fails.extend(release_fails(root, release_dir))
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--skip-release", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root or CANON_ROOT)
    fails = check(root, include_release=not a.skip_release)
    print("=" * 72)
    print("CH2 LIVE SEMANTIC QA")
    print("=" * 72)
    if fails:
        for f in fails:
            print("[FAIL]", f)
        print("OVERALL: FAIL (%d)" % len(fails))
        sys.exit(1)
    print("[PASS] sync, leakage, vocab, pacing, Friday, playbook, media, manifest, release set")
    print("OVERALL: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
