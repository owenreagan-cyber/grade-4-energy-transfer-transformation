"""Chapter 1 release builder (Phase 6.1 / F4). One-shot, deterministic.

Copies the canonical Chapter 1 masters into production/releases/chapter-01/, renders the
derived PDFs (teacher key bundle, Friday FLEX bank) with an isolated LibreOffice profile,
retires stale pre-canonical release files, refreshes Ch1 rows of the final-delivery hash
CSV, and writes RELEASE_MANIFEST.json (read by tools/qa_release_parity.py).

Usage: .venv/bin/python tools/build_ch1_release.py
"""
import csv, hashlib, json, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REL = os.path.join(REPO, "production", "releases", "chapter-01")
RETIRED = os.path.join(REPO, "production", "archive", "retired", "chapter-01-release-v1.0")
VERSION = "1.1"
STATUS = "FROZEN"

P = "production/"
# (release file name, kind, [canonical sources])
COPY = [
    ("01-ch1-energy-causes-change-guided-notes.pdf", P + "premium-notes/01-ch1-energy-causes-change-guided-notes.pdf"),
    ("01-ch1-energy-causes-change-guided-notes-key.pdf", P + "premium-notes/01-ch1-energy-causes-change-guided-notes-key.pdf"),
    ("01-ch1-energy-causes-change-slides.pptx", P + "slides/01-ch1-energy-causes-change-slides.pptx"),
    ("01-ch1-energy-causes-change-slides.pdf", P + "slides/01-ch1-energy-causes-change-slides.pdf"),
    ("01-ch1-energy-causes-change-practice.pdf", P + "worksheets/01-ch1-energy-causes-change-practice.pdf"),
    ("01-ch1-energy-causes-change-quiz.pdf", P + "quizzes/01-ch1-energy-causes-change-quiz.pdf"),
    ("01-ch1-energy-detectives-student.pdf", P + "worksheets/01-ch1-energy-detectives-student.pdf"),
]
DERIVED = [
    ("01-ch1-energy-causes-change-teacher-key.pdf", "Chapter 1 Teacher Key — Combined",
     [P + "answer-keys/01-ch1-energy-causes-change-quiz-key.md",
      P + "answer-keys/01-ch1-energy-causes-change-practice-key.md",
      P + "answer-keys/01-ch1-energy-detectives-key.md"]),
    ("01-ch1-friday-flex.pdf", None, ["curriculum/chapter-01/student/01-ch1-friday-flex.md"]),
]
RETIRE_FROM_RELEASE = ["01-ch1-interactive-science-notebook.pdf"]   # retired INB architecture

CSS = """<style>
@page{size:8.5in 11in;margin:0.7in}
body{font-family:'Helvetica Neue',Arial,sans-serif;font-size:11pt;line-height:1.35;color:#1a1a1a}
h1{color:#1F2A5A;font-size:19pt;border-bottom:2px solid #A67C16;padding-bottom:5px}
h2{color:#1F2A5A;font-size:14pt;margin-top:18px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:8.5pt}
th,td{border:1px solid #888;padding:3px 5px;vertical-align:top;text-align:left}
th{background:#1F2A5A;color:#fff}
code{background:#eee;padding:0 2px}
blockquote{color:#444;border-left:4px solid #A67C16;margin:6px 0;padding-left:10px}
</style>"""


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sanitize(txt):
    """Release PDFs are classroom-facing: drop repo paths, artifact lines, phase labels and calendar dates."""
    out = []
    for line in txt.splitlines():
        if line.lstrip("- ").startswith("**Artifact:**") or "Phase 6.1" in line and line.startswith(">"):
            continue
        out.append(line)
    # python-markdown needs a blank line before a list that follows a paragraph (else bullets run together)
    fixed = []
    for line in out:
        if re.match(r"\s*[-*] ", line) and fixed and fixed[-1].strip() and not re.match(r"\s*([-*] |\d+\. )", fixed[-1]):
            fixed.append("")
        fixed.append(line)
    txt = "\n".join(fixed)
    txt = re.sub(r"(?m)^(\s*)- \[[xX ]\] ", r"\1- ", txt)   # no literal markdown checkboxes in classroom PDFs
    txt = re.sub(r"\(?see `docs/chapter-01/CH1_PACING_PLAN\.md`\)?", "(see the Chapter 1 pacing plan)", txt)
    txt = re.sub(r"`docs/chapter-01/CH1_PACING_PLAN\.md`", "the Chapter 1 pacing plan", txt)
    # L3 safety net: no repo-relative .md paths may survive into a classroom PDF
    txt = re.sub(r"\(?see `[^`]*\.md`\)?", "(see your teacher)", txt)
    txt = re.sub(r"`[A-Za-z0-9_./-]+\.md`", "the matching Chapter 1 page", txt)
    txt = re.sub(r"\b(Mon|Tue|Fri) \d{1,2}/\d{1,2}\b", lambda m: {"Mon": "Monday", "Tue": "Tuesday", "Fri": "Friday"}[m.group(1)], txt)
    return txt


def md_to_pdf(md_paths, title, out_pdf):
    import markdown
    parts = []
    if title:
        parts.append("<h1>%s</h1>" % title)
    for i, mp in enumerate(md_paths):
        txt = sanitize(open(os.path.join(REPO, mp), encoding="utf-8").read())
        body = markdown.markdown(txt, extensions=["tables", "fenced_code", "sane_lists"])
        if "friday-flex" in out_pdf:
            # 6.1C / L-B: each activity section starts on a fresh page so no table continues
            # onto a page without its section title (first section and "Rule check" stay inline).
            def _brk(m, _n=[0]):
                _n[0] += 1
                if _n[0] == 1 or m.group(1).startswith("Rule check"):
                    return m.group(0)
                return '<h2 style="page-break-before:always">%s</h2>' % m.group(1)
            body = re.sub(r"<h2>(.*?)</h2>", _brk, body)
        parts.append(body)
        if i < len(md_paths) - 1:
            parts.append('<div style="page-break-after:always"></div>')
    html = "<!doctype html><html><head><meta charset='utf-8'>%s</head><body>%s</body></html>" % (CSS, "".join(parts))
    work = tempfile.mkdtemp(prefix="ch1rel_")
    prof = tempfile.mkdtemp(prefix="lo_prof_")
    try:
        hp = os.path.join(work, "k.html")
        open(hp, "w", encoding="utf-8").write(html)
        subprocess.run(["soffice", "--headless", "--norestore", "-env:UserInstallation=file://" + prof,
                        "--convert-to", "pdf:writer_web_pdf_Export", "--outdir", work, hp],
                       check=True, capture_output=True, text=True, timeout=300)
        shutil.move(os.path.join(work, "k.pdf"), out_pdf)
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(prof, ignore_errors=True)


def main():
    os.makedirs(REL, exist_ok=True)
    os.makedirs(RETIRED, exist_ok=True)
    # 1. retire stale files (anything in the release dir not part of the new package)
    keep = {n for n, _ in COPY} | {n for n, _, _ in DERIVED} | {"RELEASE_MANIFEST.json", "README.md"}
    for name in sorted(os.listdir(REL)):
        if name not in keep or name in RETIRE_FROM_RELEASE:
            shutil.move(os.path.join(REL, name), os.path.join(RETIRED, name))
    # derived files are always rebuilt, so retire their old copies too (v1.0 content)
    # (only on the first run; later runs just overwrite — the v1.0 copies in RETIRED are never replaced)
    for name, _, _ in DERIVED:
        old = os.path.join(REL, name)
        arch = os.path.join(RETIRED, "v1.0-" + name)
        if os.path.exists(old) and not os.path.exists(arch):
            shutil.move(old, arch)
    # 2. copy canonical masters
    entries = []
    for name, src in COPY:
        s = os.path.join(REPO, src)
        if not os.path.exists(s):
            sys.exit("missing canonical source: " + src)
        shutil.copy2(s, os.path.join(REL, name))
        entries.append(dict(name=name, kind="copy", sources=[src], source_sha256=[sha(s)], sha256=sha(os.path.join(REL, name))))
    # 3. derived PDFs
    for name, title, srcs in DERIVED:
        out = os.path.join(REL, name)
        md_to_pdf(srcs, title, out)
        entries.append(dict(name=name, kind="derived", sources=srcs,
                            source_sha256=[sha(os.path.join(REPO, x)) for x in srcs], sha256=sha(out)))
    man = dict(chapter=1, version=VERSION, status=STATUS, builder="tools/build_ch1_release.py", files=entries,
               retired_to="production/archive/retired/chapter-01-release-v1.0/")
    json.dump(man, open(os.path.join(REL, "RELEASE_MANIFEST.json"), "w"), indent=2)
    open(os.path.join(REL, "README.md"), "w").write(
        "# Chapter 1 release package — %s\n\n"
        "Status: **%s**. Built by `tools/build_ch1_release.py` from the canonical masters; verified by\n"
        "`tools/qa_release_parity.py --chapter 1`. Do not edit files here by hand.\n\n"
        "Timing: `docs/chapter-01/CH1_PACING_PLAN.md` (Mon · Tue · Fri). Teacher keys: bundled PDF\n"
        "`01-ch1-energy-causes-change-teacher-key.pdf` + `…-guided-notes-key.pdf`.\n\n"
        "Retired v1.0 files (stale / retired architecture) were moved to `%s` and are NOT part of this package.\n"
        % (VERSION, STATUS, man["retired_to"]))
    open(os.path.join(RETIRED, "README.md"), "w").write(
        "# Retired Chapter 1 release files (v1.0 package)\n\n"
        "Moved out of `production/releases/chapter-01/` in Phase 6.1 (F4). Kept for provenance only; they predate the\n"
        "canonical Guided Notes architecture (Interactive Science Notebook, old combined key, old Friday FLEX) and must not be\n"
        "distributed.\n")
    # 4. refresh Ch1 rows of final-delivery hash CSV (Ch1 rows only; other chapters untouched)
    csv_path = os.path.join(REPO, "production", "final-delivery", "RELEASE_HASH_MANIFEST.csv")
    if os.path.exists(csv_path):
        rows = list(csv.reader(open(csv_path, newline="", encoding="utf-8")))
        hdr, body, n = rows[0], rows[1:], 0
        for r in body:
            if r[0].startswith("01-ch1") and os.path.exists(os.path.join(REPO, r[3])):
                p = os.path.join(REPO, r[3]); r[4] = sha(p); r[5] = str(os.path.getsize(p)); n += 1
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(hdr); w.writerows(body)
        print("final-delivery Ch1 hash rows refreshed:", n)
    print("release files:", len(entries), "→", REL)


if __name__ == "__main__":
    main()
