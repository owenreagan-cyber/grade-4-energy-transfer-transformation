"""Reusable deterministic canonical <-> release parity QA (Phase 6.1 / F4).

Reads production/releases/chapter-0N/RELEASE_MANIFEST.json (written by the chapter's release builder) and checks:
  1. every manifest file exists in the release dir and its SHA-256 matches the manifest
  2. kind=copy   -> release hash == LIVE canonical source hash (no drift)
     kind=derived -> recorded source hashes == LIVE source hashes (derived PDF is not stale)
  3. no unexpected files in the release dir (only manifest files + README.md + RELEASE_MANIFEST.json)
  4. no retired architecture files (interactive science notebook, v1.0 names, INB) in the release dir
  5. release PDFs: stale-language scan (pdftotext) against the chapter's stale tokens; US Letter size for text PDFs
  6. release PPTX: 16:9 dimensions and no screen4x3 presentation type metadata
  7. final-delivery hash CSV rows for this chapter match live canonical hashes (if the CSV lists them)
  8. retired directory exists and holds the retired files
  9. (6.1B) no repo paths, phase labels, WHAT WE NOTICE or INB text in any release PDF; quiz shows raw /16 + %

Usage: .venv/bin/python tools/qa_release_parity.py --chapter 1 [--report qa/reports/X.md]
Exit code 0 = PASS, 1 = FAIL.
"""
import argparse, csv, hashlib, json, os, re, subprocess, sys, zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

RETIRED_PATTERNS = [r"interactive-science-notebook", r"-inb[-.]", r"-v1\.0\.", r"notebook"]
STALE_TOKENS = {
    1: ["Model It", "Draw/Label", "Block 1", "Block 2", "cup/balloon/salt", "Interactive Science Notebook",
        "kinetic", "potential energy", "mechanical energy", "radiant", "inertia", "compression wave"],
}
# Phase 6.1B / L3: classroom-facing PDFs must not leak repo paths, internal phase labels or retired note architecture
LEAK_PATTERNS = [
    (r"\b[\w./-]+\.md\b", "markdown repo path"),
    (r"\b(?:docs|curriculum|production|tools|qa|assets)/[\w.-]+/", "repo directory path"),
    (r"\bstudent/recovery", "repo path student/recovery"),
    (r"\bPhase\s+\d", "internal phase label"),
    (r"WHAT WE NOTICE", "retired WHAT WE NOTICE notes architecture"),
    (r"Interactive Science Notebook|\bINB\b", "retired notebook architecture"),
]
# text PDFs that are legitimately not Letter portrait (slides are 16:9)
LANDSCAPE_OK = ("slides.pdf",)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    n = a.chapter
    rel = os.path.join(REPO, "production", "releases", "chapter-%02d" % n)
    mp = os.path.join(rel, "RELEASE_MANIFEST.json")
    gates = []

    def gate(name, ok, note):
        gates.append((name, "PASS" if ok else "FAIL", note))

    if not os.path.exists(mp):
        gate("manifest present", False, "missing " + os.path.relpath(mp, REPO))
        return finish(gates, a)
    man = json.load(open(mp))
    files = man["files"]
    gate("manifest present", True, "version %s · %d files · status: %s" % (man["version"], len(files), man["status"]))

    missing = [f["name"] for f in files if not os.path.exists(os.path.join(rel, f["name"]))]
    gate("all manifest files exist", not missing, "missing: %s" % (missing or "none"))
    present = [f for f in files if f["name"] not in missing]

    bad = [f["name"] for f in present if sha(os.path.join(rel, f["name"])) != f["sha256"]]
    gate("release hashes match manifest", not bad, "mismatch: %s" % (bad or "none"))

    drift = []
    for f in present:
        live = []
        for s in f["sources"]:
            sp = os.path.join(REPO, s)
            live.append(sha(sp) if os.path.exists(sp) else "MISSING")
        if f["kind"] == "copy":
            if live[0] != f["sha256"]:
                drift.append(f["name"])
        elif live != f["source_sha256"]:
            drift.append(f["name"] + " (derived source changed)")
    gate("canonical == release (no drift)", not drift, "drifted: %s" % (drift or "none"))

    allowed = {f["name"] for f in files} | {"RELEASE_MANIFEST.json", "README.md"}
    extra = sorted(set(os.listdir(rel)) - allowed)
    gate("no unexpected files", not extra, "extra: %s" % (extra or "none"))

    retired = [x for x in os.listdir(rel) if any(re.search(p, x, re.I) for p in RETIRED_PATTERNS)]
    gate("no retired-architecture files", not retired, "retired-pattern files: %s" % (retired or "none"))

    stale = {}
    badsize = []
    for f in present:
        p = os.path.join(rel, f["name"])
        if f["name"].endswith(".pdf"):
            t = pdf_text(p)
            if "key" in f["name"]:   # teacher keys may restate the out-of-scope list as a prohibition
                t = "\n".join(l for l in t.splitlines() if not re.search(r"out-of-scope|\bno kinetic|do not (use|introduce|teach)", l, re.I))
            hits = [s for s in STALE_TOKENS.get(n, []) if s.lower() in t.lower()]
            if hits:
                stale[f["name"]] = hits
            info = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout
            sz = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
            if sz and not f["name"].endswith(LANDSCAPE_OK):
                w, h = float(sz.group(1)), float(sz.group(2))
                if not (abs(w - 612) < 2 and abs(h - 792) < 2):
                    badsize.append("%s %.0fx%.0f" % (f["name"], w, h))
    gate("release PDFs: stale/banned language", not stale, "hits: %s" % (stale or "none"))
    leaks = {}
    for f in present:
        if f["name"].endswith(".pdf"):
            t = pdf_text(os.path.join(rel, f["name"]))
            t = re.sub(r"-\n", "-", t)
            for rx, why in LEAK_PATTERNS:
                m = re.search(rx, t)
                if m:
                    leaks.setdefault(f["name"], []).append("%s: %r" % (why, m.group(0)))
    gate("release PDFs: no repo paths / phase labels / retired architecture", not leaks, "leaks: %s" % (leaks or "none"))
    q = [f for f in present if "quiz" in f["name"] and f["name"].endswith(".pdf") and "key" not in f["name"]]
    qbad = []
    for f in q:
        t = pdf_text(os.path.join(rel, f["name"]))
        if not (re.search(r"/\s*16\b", t) and "%" in t):
            qbad.append(f["name"])
    gate("quiz PDF: current score layout (raw /16 + %)", not qbad, "missing score layout: %s" % (qbad or "none"))
    # 6.1C / L-B: FLEX continuation pages must not open with a headless table
    fx = [f for f in present if "friday-flex" in f["name"] and f["name"].endswith(".pdf")]
    fxbad = []
    for f in fx:
        for i, pg in enumerate(pdf_text(os.path.join(rel, f["name"])).split("\f")):
            first = next((l.strip() for l in pg.splitlines() if l.strip()), "")
            if pg.strip() and re.match(r"Field\b", first):
                fxbad.append("%s p%d" % (f["name"], i + 1))
    gate("FLEX PDF: no page opens with a table header lacking its section title (L-B)", not fxbad,
         "headless continuation pages: %s" % (fxbad or "none"))
    gate("release PDFs: US Letter (non-slides)", not badsize, "off-size: %s" % (badsize or "none"))

    pp = []
    for f in present:
        if f["name"].endswith(".pptx"):
            z = zipfile.ZipFile(os.path.join(rel, f["name"]))
            pres = z.read("ppt/presentation.xml").decode("utf8")
            cx = int(re.search(r'<p:sldSz[^>]*cx="(\d+)"', pres).group(1))
            cy = int(re.search(r'<p:sldSz[^>]*cy="(\d+)"', pres).group(1))
            typ = re.search(r'<p:sldSz[^>]*type="(\w+)"', pres)
            ok = abs(cx / cy - 16 / 9) < 0.01 and not (typ and typ.group(1) == "screen4x3")
            pp.append("%s %sx%s type=%s %s" % (f["name"], cx, cy, typ.group(1) if typ else "none", "OK" if ok else "BAD"))
            if not ok:
                gate("PPTX widescreen metadata", False, pp[-1])
    if not any(g[0] == "PPTX widescreen metadata" for g in gates):
        gate("PPTX widescreen metadata", True, "; ".join(pp) or "no pptx")

    # final-delivery CSV
    csvp = os.path.join(REPO, "production", "final-delivery", "RELEASE_HASH_MANIFEST.csv")
    mism = []
    if os.path.exists(csvp):
        prefix = "%02d-ch%d" % (n, n)
        for r in list(csv.reader(open(csvp, newline="", encoding="utf-8")))[1:]:
            if r[0].startswith(prefix) and os.path.exists(os.path.join(REPO, r[3])):
                if sha(os.path.join(REPO, r[3])) != r[4]:
                    mism.append(r[0])
    gate("final-delivery hash CSV current (this chapter)", not mism, "stale rows: %s" % (mism or "none"))

    rd = man.get("retired_to")
    gate("retired v1.0 files archived", bool(rd) and os.path.isdir(os.path.join(REPO, rd)) and
         len([x for x in os.listdir(os.path.join(REPO, rd)) if x.endswith(".pdf")]) >= 1, rd or "no retired_to")
    return finish(gates, a)


def finish(gates, a):
    overall = "PASS" if all(g[1] == "PASS" for g in gates) else "FAIL"
    print("=" * 72)
    print("RELEASE PARITY QA — chapter %d" % a.chapter)
    print("=" * 72)
    for name, st, note in gates:
        print("[%-4s] %-46s %s" % (st, name, note))
    print("=" * 72)
    print("OVERALL:", overall)
    if a.report:
        os.makedirs(os.path.dirname(os.path.join(REPO, a.report)), exist_ok=True)
        with open(os.path.join(REPO, a.report), "w") as f:
            f.write("# Release Parity QA — Chapter %d\n\nTool: `tools/qa_release_parity.py` (reusable). Overall: **%s**\n\n" % (a.chapter, overall))
            for name, st, note in gates:
                f.write("- [%s] %s — %s\n" % (st, name, note))
        print("report:", a.report)
    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()
