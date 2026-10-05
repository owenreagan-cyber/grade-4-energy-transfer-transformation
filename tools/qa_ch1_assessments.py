"""Phase 6.1 — Chapter 1 assessment/resource QA (practice · quiz · Energy Detectives + keys).

Deterministic gates: layout (US Letter, pages), headers, score line, point arithmetic, key parity,
ruled-line counts on explain prompts, scope language, retired-content absence, optional-status honesty.

Run: .venv/bin/python tools/qa_ch1_assessments.py [--report qa/reports/NAME.md]
"""
import os, re, subprocess, sys
from docx import Document
from docx.oxml.ns import qn

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
P = lambda *a: os.path.join(ROOT, *a)
PRACTICE = P("production", "worksheets", "01-ch1-energy-causes-change-practice")
QUIZ = P("production", "quizzes", "01-ch1-energy-causes-change-quiz")
DET = P("production", "worksheets", "01-ch1-energy-detectives-student")
KEYS = {
    "practice": P("production", "answer-keys", "01-ch1-energy-causes-change-practice-key.md"),
    "quiz": P("production", "answer-keys", "01-ch1-energy-causes-change-quiz-key.md"),
    "det": P("production", "answer-keys", "01-ch1-energy-detectives-key.md"),
    "blueprint": P("production", "quizzes", "01-ch1-energy-causes-change-quiz-blueprint.md"),
}
BANNED = ["kinetic", "potential", "mechanical", "radiant", "momentum", "inertia", "compression wave",
          "gravitational", "26 items", "INB", "lying flat", "book lying"]

def ordered_text(doc):
    out = []
    for el in doc.element.body.iterchildren():
        out.append("".join(x.text or "" for x in el.iter(qn("w:t"))))
    return "\n".join(out)

def pdf_pages(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", info)
    return int(m.group(1)) if m else -1

def ruled_groups(doc):
    g = []
    for t in doc.tables:
        if len(t.columns) != 1:
            continue
        ok = True
        for row in t.rows:
            c = row.cells[0]
            tcPr = c._tc.find(qn("w:tcPr"))
            bd = tcPr.find(qn("w:tcBorders")) if tcPr is not None else None
            if c.text.strip() or bd is None or bd.find(qn("w:bottom")) is None:
                ok = False; break
        if ok:
            g.append(len(t.rows))
    return g

def read(path):
    return open(path, encoding="utf-8").read()

def main():
    results = []
    def add(n, s, note): results.append((n, s, note))

    qd, pd_, dd = Document(QUIZ + ".docx"), Document(PRACTICE + ".docx"), Document(DET + ".docx")
    qt, pt, dt = ordered_text(qd), ordered_text(pd_), ordered_text(dd)

    for name, d in (("quiz", qd), ("practice", pd_), ("detectives", dd)):
        sec = d.sections[0]
        w, h = sec.page_width / 914400, sec.page_height / 914400
        add(f"{name}: US Letter", "PASS" if abs(w - 8.5) < .01 and abs(h - 11) < .01 else "FAIL", f"{w:.2f}x{h:.2f}")
    for name, base, exp in (("quiz", QUIZ, 2), ("practice", PRACTICE, 2), ("detectives", DET, 2)):
        n = pdf_pages(base + ".pdf")
        add(f"{name}: PDF pages = {exp}", "PASS" if n == exp else "FAIL", f"pages {n}")
        txt = {"quiz": qt, "practice": pt, "detectives": dt}[name]
        ok = "Name:" in txt and "Homeroom" in txt and "Date" not in txt
        add(f"{name}: Name + Homeroom header, no Date", "PASS" if ok else "FAIL", "header fields")

    # ---- quiz arithmetic
    pts = [int(x) for x in re.findall(r"\((\d) pts?\)", qt)]
    add("quiz: 9 items with point labels", "PASS" if len(pts) == 9 else "FAIL", f"labels {pts}")
    add("quiz: points sum 16", "PASS" if sum(pts) == 16 else "FAIL", f"sum {sum(pts)}")
    add("quiz: standard score line (raw / 16 + %)", "PASS" if re.search(r"SCORE:.*/ 16.*%", qt) else "FAIL", "SCORE: ___ / 16  ___ %")
    add("quiz: note policy line (teacher choice)", "PASS" if "OPEN NOTE" in qt and "CLOSED NOTE" in qt else "FAIL", "open/closed circle line")
    g = ruled_groups(qd)
    add("quiz: explain items have >= 2 ruled lines", "PASS" if g.count(3) >= 2 else "FAIL", f"ruled groups {g}")
    ky = read(KEYS["quiz"])
    key_pts = [int(x) for x in re.findall(r"^\| (\d) \| (\d) \|", ky, re.M) and [m[1] for m in re.findall(r"^\| (\d) \| (\d) \|", ky, re.M)]]
    add("quiz key: per-item points match student page", "PASS" if key_pts == pts else "FAIL", f"key {key_pts} vs page {pts}")
    # MC key letters vs actual options
    opts = {}
    cur = None
    for line in qt.split("\n"):
        m = re.match(r"^(\d)\.\s", line)
        if m: cur = int(m.group(1))
        m2 = re.match(r"^([abcd])\)\s+(.*)$", line)
        if m2 and cur: opts.setdefault(cur, {})[m2.group(1)] = m2.group(2)
    expect = {1: ("c", "cause change"), 2: ("b", "evidence"), 4: ("d", "motion, sound, light, heat, electrical energy"), 7: ("a", "has stored energy")}
    bad = []
    for q, (L, text) in expect.items():
        if opts.get(q, {}).get(L) != text or f"**{L})** {text}" not in ky:
            bad.append(q)
    add("quiz key: MC letters = actual correct options (items 1,2,4,7)", "PASS" if not bad else "FAIL", f"mismatch items {bad or 'none'}")
    letters = "".join(expect[q][0] for q in (1, 2, 4, 7))
    add("quiz: MC answer letters not patterned", "PASS" if letters not in ("abcd", "dcba") and len(set(letters)) >= 3 else "FAIL", f"letters {letters}")
    q9 = re.findall(r"[abc]\)\s+(The [^\n]*?\.)(?=YES)", qt)
    dup = [x for x in q9 if x.rstrip(".").lower() in pt.lower()]
    add("quiz Q9 statements not reused in practice", "PASS" if len(q9) == 3 and not dup else "FAIL", f"q9 {q9} dup {dup or 'none'}")
    add("quiz key: Q9 statements listed", "PASS" if all(x.rstrip(".") in ky for x in q9) and len(q9) == 3 else "FAIL", "key names the 3 statements")
    add("quiz key: Q9 YES/NO/YES", "PASS" if "a) **YES** · b) **NO** · c) **YES**" in ky else "FAIL", "explicit")
    add("quiz key: score + percent instruction", "PASS" if "raw score + percentage" in ky and "TEACHER CHOICE" in ky else "FAIL", "scoring + note policy")
    add("quiz key: item 5 blanks match page (2 blanks, 2 pts)", "PASS" if "ENERGY → **change** → **evidence**" in ky and "1 pt per blank" in ky else "FAIL", "q5")
    bp = read(KEYS["blueprint"])
    add("blueprint: points + note policy", "PASS" if "= **16**" in bp and "TEACHER CHOICE" in bp else "FAIL", "blueprint synced")

    # ---- practice
    add("practice: ungraded (no score line)", "PASS" if "NOT GRADED" in pt and "SCORE" not in pt else "FAIL", "ungraded")
    pg = ruled_groups(pd_)
    add("practice: Explain prompt >= 2 ruled lines", "PASS" if pg and max(pg) >= 2 else "FAIL", f"ruled groups {pg}")
    pk = read(KEYS["practice"])
    add("practice: no ambiguous book-on-table row", "PASS" if "lying flat" not in pt and "lying flat" not in pk.split("Rationale")[0] else "FAIL", "retired row absent")
    add("practice key: Reader-supported stored-energy rows", "PASS" if "flashlight that is switched off" in pk and "toy car rolling" in pk else "FAIL", "Part C rows")

    # ---- detectives
    add("detectives: optional + ungraded on page", "PASS" if "OPTIONAL" in dt and "NOT GRADED" in dt else "FAIL", "tag")
    dk = read(KEYS["det"])
    scored = re.findall(r"\b\d+\s*(?:pts?|points?)\b", dk)
    add("detectives key: no point values", "PASS" if not scored and "UNGRADED" in dk else "FAIL", f"scored tokens {scored or 'none'}")
    add("detectives: ruled lines present", "PASS" if len(ruled_groups(dd)) >= 6 else "FAIL", f"groups {ruled_groups(dd)}")

    # ---- scope
    def scrub(t):
        t = t.split("## Out-of-scope")[0]
        return "\n".join(l for l in t.split("\n") if not l.startswith("*Rationale"))
    blob = (qt + pt + dt + scrub(ky) + scrub(pk) + scrub(dk)).lower()
    hits = [b for b in BANNED if b.lower() in blob]
    add("scope: no advanced/retired language", "PASS" if not hits else "FAIL", f"{hits or 'none'}")

    overall = "PASS" if all(s == "PASS" for _, s, _ in results) else "FAIL"
    print("=" * 76); print("CH1 ASSESSMENTS & RESOURCES — QA (Phase 6.1)"); print("=" * 76)
    for n, s, note in results:
        print(f"[{s:4}] {n:58} {note}")
    print("=" * 76); print("OVERALL:", overall)
    out = P("qa", "reports", "PHASE_6_1_CH1_ASSESSMENT_QA.md")
    if "--report" in sys.argv:
        out = P(sys.argv[sys.argv.index("--report") + 1])
    with open(out, "w") as f:
        f.write("# Chapter 1 Assessments & Resources QA (Phase 6.1)\n\nGenerated by tools/qa_ch1_assessments.py.\n\n")
        f.write(f"Overall: **{overall}**\n\n")
        for n, s, note in results:
            f.write(f"- [{s}] {n} — {note}\n")
    print("report:", out)
    return 0 if overall == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
