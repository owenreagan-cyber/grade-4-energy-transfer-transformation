"""Chapter 2 release builder (Phase 7.6). One-shot, deterministic.

Copies canonical Chapter 2 masters into production/releases/chapter-02/, renders derived
PDFs, archives the pre-7.1 release set (including the retired notebook PDF), refreshes
Chapter 2 rows of the final-delivery hash CSV, and writes RELEASE_MANIFEST.json.

Status is FROZEN (v1.0). Usage: .venv/bin/python tools/build_ch2_release.py
"""
import csv, hashlib, json, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CANON_TOOLS = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join(REPO, "production", "releases", "chapter-02")
RETIRED = os.path.join(REPO, "production", "archive", "retired", "chapter-02-pre-7.1")
VERSION = "1.0"
STATUS = "FROZEN"
P = "production/"

COPY = [
    ("02-ch2-moving-objects-have-energy-guided-notes.pdf", P + "premium-notes/02-ch2-moving-objects-have-energy-guided-notes.pdf"),
    ("02-ch2-moving-objects-have-energy-guided-notes-key.pdf", P + "premium-notes/02-ch2-moving-objects-have-energy-guided-notes-key.pdf"),
    ("02-ch2-moving-objects-have-energy-slides.pptx", P + "slides/02-ch2-moving-objects-have-energy-slides.pptx"),
    ("02-ch2-moving-objects-have-energy-slides.pdf", P + "slides/02-ch2-moving-objects-have-energy-slides.pdf"),
]
DOCX_PDF = [
    ("02-ch2-moving-objects-have-energy-practice.pdf", P + "worksheets/02-ch2-moving-objects-have-energy-practice.docx"),
    ("02-ch2-moving-objects-have-energy-quiz.pdf", P + "quizzes/02-ch2-moving-objects-have-energy-quiz.docx"),
    ("02-ch2-moving-marbles-student.pdf", P + "worksheets/02-ch2-moving-marbles-student.docx"),
    ("02-ch2-friday-flex.pdf", P + "worksheets/02-ch2-friday-flex.docx"),
]
DERIVED_MD = [
    ("02-ch2-moving-objects-have-energy-teacher-key.pdf", "Chapter 2 Teacher Key",
     [P + "answer-keys/02-ch2-moving-objects-have-energy-quiz-key.md",
      P + "answer-keys/02-ch2-moving-objects-have-energy-practice-key.md",
      P + "answer-keys/02-ch2-moving-marbles-key.md",
      P + "answer-keys/02-ch2-friday-flex-key.md"]),
]
DOCX_PDF.append(
    ("02-ch2-absent-student-recovery.pdf", P + "worksheets/02-ch2-absent-student-recovery.docx")
)

CSS = """<style>
@page{size:8.5in 11in;margin:0.7in}
body{font-family:'Helvetica Neue',Arial,sans-serif;font-size:11pt;line-height:1.35;color:#1a1a1a}
h1{color:#0F5A5C;font-size:19pt;border-bottom:2px solid #0E8A97;padding-bottom:5px}
h2{color:#0F5A5C;font-size:14pt;margin-top:18px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:8.5pt}
th,td{border:1px solid #888;padding:3px 5px;vertical-align:top;text-align:left}
th{background:#0F5A5C;color:#fff}
</style>"""


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sanitize(txt):
    fixed = []
    for line in txt.splitlines():
        if re.match(r"\s*[-*] ", line) and fixed and fixed[-1].strip() and not re.match(r"\s*([-*] |\d+\. )", fixed[-1]):
            fixed.append("")
        fixed.append(line)
    txt = "\n".join(fixed)
    txt = re.sub(r"(?m)^(\s*)- \[[xX ]\] ", r"\1- ", txt)
    txt = re.sub(r"`[^`]*\.md`", "the matching Chapter 2 page", txt)
    txt = re.sub(r"`[^`]*\.docx`", "the matching Chapter 2 page", txt)
    return txt


def soffice_convert(src, out_pdf):
    work = tempfile.mkdtemp(prefix="ch2rel_")
    prof = tempfile.mkdtemp(prefix="lo_ch2_")
    try:
        subprocess.run(["soffice", "--headless", "--norestore", "-env:UserInstallation=file://" + prof,
                        "--convert-to", "pdf", "--outdir", work, src],
                       check=True, capture_output=True, text=True, timeout=300)
        produced = [f for f in os.listdir(work) if f.endswith(".pdf")]
        if len(produced) != 1:
            sys.exit("expected one pdf from %s, got %s" % (src, produced))
        shutil.move(os.path.join(work, produced[0]), out_pdf)
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(prof, ignore_errors=True)


def md_to_pdf(md_paths, title, out_pdf):
    import markdown
    parts = []
    if title:
        parts.append("<h1>%s</h1>" % title)
    for i, mp in enumerate(md_paths):
        txt = sanitize(open(os.path.join(REPO, mp), encoding="utf-8").read())
        body = markdown.markdown(txt, extensions=["tables", "fenced_code", "sane_lists"])
        if "friday-flex" in out_pdf:
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
    work = tempfile.mkdtemp(prefix="ch2md_")
    try:
        hp = os.path.join(work, "k.html")
        open(hp, "w", encoding="utf-8").write(html)
        soffice_convert(hp, out_pdf)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def build_into(dest):
    os.makedirs(dest, exist_ok=True)
    entries = []
    for name, src in COPY:
        s = os.path.join(REPO, src)
        if not os.path.exists(s):
            sys.exit("missing canonical source: " + src)
        shutil.copy2(s, os.path.join(dest, name))
        entries.append(dict(name=name, kind="copy", sources=[src], source_sha256=[sha(s)], sha256=sha(os.path.join(dest, name))))
    for name, src in DOCX_PDF:
        s = os.path.join(REPO, src)
        if not os.path.exists(s):
            sys.exit("missing canonical source: " + src)
        soffice_convert(s, os.path.join(dest, name))
        entries.append(dict(name=name, kind="derived", sources=[src], source_sha256=[sha(s)], sha256=sha(os.path.join(dest, name))))
    for name, title, srcs in DERIVED_MD:
        out = os.path.join(dest, name)
        md_to_pdf(srcs, title, out)
        entries.append(dict(name=name, kind="derived", sources=srcs,
                            source_sha256=[sha(os.path.join(REPO, x)) for x in srcs], sha256=sha(out)))
    man = dict(chapter=2, version=VERSION, status=STATUS, builder="tools/build_ch2_release.py", files=entries,
               retired_to="production/archive/retired/chapter-02-pre-7.1/")
    json.dump(man, open(os.path.join(dest, "RELEASE_MANIFEST.json"), "w"), indent=2)
    open(os.path.join(dest, "README.md"), "w").write(
        "# Chapter 2 release package — %s\n\n"
        "Status: **%s**. Built by `tools/build_ch2_release.py` from the canonical masters; verified by\n"
        "`tools/qa_release_parity.py --chapter 2`. Do not edit files here by hand.\n\n"
        "Timing: the Chapter 2 pacing plan (Wed · Thu). Friday of Week 1 is Chapter 1.\n"
        "Guided Notes are the primary student artifact. The interactive science notebook is not in this package.\n\n"
        "Pre-7.1 files were copied to `%s` and are not part of this package.\n"
        % (VERSION, STATUS, man["retired_to"]))
    return entries


def promote(stage):
    os.makedirs(REL, exist_ok=True)
    keep = set(os.listdir(stage))
    for name in sorted(os.listdir(REL)):
        if name not in keep:
            path = os.path.join(REL, name)
            if os.path.isfile(path):
                os.remove(path)
    for name in sorted(os.listdir(stage)):
        shutil.copy2(os.path.join(stage, name), os.path.join(REL, name))


def refresh_hashes(dest=None):
    src_csv = os.path.join(REPO, "production", "final-delivery", "RELEASE_HASH_MANIFEST.csv")
    csv_path = dest or src_csv
    if not os.path.exists(src_csv):
        return 0
    import qa_ch2_semantic as sem
    rows = list(csv.reader(open(src_csv, newline="", encoding="utf-8")))
    hdr, body = rows[0], rows[1:]
    have = {r[3] for r in body}
    for name in sem.REQUIRED_RELEASE:
        rel_path = "production/releases/chapter-02/" + name
        if rel_path not in have:
            body.append([name, "UNIT 1", "RELEASE", rel_path, "", "0", "ACTIVE"])
    n = 0
    for r in body:
        if r[0].startswith("02-ch2") and os.path.exists(os.path.join(REPO, r[3])):
            pth = os.path.join(REPO, r[3])
            r[4] = sha(pth)
            r[5] = str(os.path.getsize(pth))
            n += 1
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(hdr)
        w.writerows(body)
    return n


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    a = ap.parse_args()
    global REPO, REL, RETIRED
    if a.root:
        REPO = os.path.abspath(a.root)
        REL = os.path.join(REPO, "production", "releases", "chapter-02")
        RETIRED = os.path.join(REPO, "production", "archive", "retired", "chapter-02-pre-7.1")
    def _qa(cmd):
        proc = subprocess.run(cmd)
        if proc.returncode != 0:
            sys.exit("QA failed (%s); active release was not updated" % os.path.basename(cmd[1]))
    py = sys.executable
    _qa([py, os.path.join(CANON_TOOLS, "qa_ch2_semantic.py"), "--root", REPO, "--skip-release"])
    _qa([py, os.path.join(CANON_TOOLS, "qa_ch2_golden.py"), "--root", REPO, "--mode", "pre-freeze"])
    _qa([py, os.path.join(CANON_TOOLS, "qa_ch2_schedule.py"), "--root", REPO])
    _qa([py, os.path.join(CANON_TOOLS, "qa_ch2_slides.py"), "--root", REPO])
    _qa([py, os.path.join(CANON_TOOLS, "qa_ch2_guided_notes.py"), "--root", REPO])
    _qa([py, os.path.join(CANON_TOOLS, "qa_teacher_playbook.py"), "--root", REPO])
    os.makedirs(REL, exist_ok=True)
    os.makedirs(RETIRED, exist_ok=True)
    if not os.path.exists(os.path.join(RETIRED, "README.md")) and os.path.isdir(REL):
        for name in sorted(os.listdir(REL)):
            src = os.path.join(REL, name)
            if os.path.isfile(src) and not os.path.exists(os.path.join(RETIRED, name)):
                shutil.copy2(src, os.path.join(RETIRED, name))
        open(os.path.join(RETIRED, "README.md"), "w").write(
            "# Retired Chapter 2 release files (pre-Phase 7.1)\n\n"
            "Moved out of `production/releases/chapter-02/` in Phase 7.1. Includes the stale notes export "
            "and the retired interactive science notebook PDF. Not for classroom distribution. "
            "Guided Notes are the primary student artifact.\n")
    stage = tempfile.mkdtemp(prefix="ch2release_")
    try:
        entries = build_into(stage)
        sys.path.insert(0, CANON_TOOLS)
        import qa_ch2_semantic as sem
        post = sem.release_fails(REPO, stage)
        if post:
            for item in post:
                print("[FAIL]", item)
            sys.exit("post-build release QA failed; active release was not replaced")
        fresh = subprocess.run([sys.executable, os.path.join(CANON_TOOLS, "qa_ch2_fresh_export.py"), "--root", REPO])
        if fresh.returncode != 0:
            sys.exit("fresh export check failed; active release was not replaced")
        image = subprocess.run([sys.executable, os.path.join(CANON_TOOLS, "qa_ch2_retired_image.py"),
                                "--root", REPO, "--release-dir", stage])
        if image.returncode != 0:
            sys.exit("retired image check failed; active release was not replaced")
        preview = tempfile.mktemp(suffix="-ch2-hash.csv")
        refresh_hashes(preview)
        par = subprocess.run([sys.executable, os.path.join(CANON_TOOLS, "qa_release_parity.py"),
                              "--chapter", "2", "--root", REPO, "--release-dir", stage, "--hash-csv", preview])
        if par.returncode != 0:
            if os.path.exists(preview):
                os.remove(preview)
            sys.exit("release parity failed on the candidate; active release was not replaced")
        if os.path.exists(preview):
            os.remove(preview)
        promote(stage)
        n = refresh_hashes()
        print("final-delivery Ch2 hash rows refreshed:", n)
        print("release files:", len(entries))
    finally:
        shutil.rmtree(stage, ignore_errors=True)


if __name__ == "__main__":
    main()
