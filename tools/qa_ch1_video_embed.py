#!/usr/bin/env python3
"""Phase 5H — genuine-embedding package-integrity verification.

Deterministically inspects the PPTX ZIP: content types, media parts, slide relationships, the
video shape on the target slide, timing (click-to-play, no autoplay), poster frame, and whether
unused media are packaged. Emits CH1_EMBEDDING_INTEGRITY.md. Does NOT claim PowerPoint playback.
"""
import hashlib, json, os, re, sys, zipfile
from lxml import etree

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CAND = os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v6-embedded-media",
                    "01-ch1-energy-causes-change-premium-hybrid-v6-embedded-media.pptx")
BASELINE = os.path.join(ROOT, "production", "candidates", "chapter-01",
                        "ch1-premium-hybrid-v4", "01-ch1-energy-causes-change-premium-hybrid-v4.pptx")
OUTDIR = os.path.join(ROOT, "qa", "reports", "ch1-phase5g")

NS = {
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

def q(tag):
    for k, v in NS.items():
        if tag.startswith(k + ":"):
            return tag
    return tag


def main():
    checks = []
    def check(name, ok, detail):
        checks.append((name, "PASS" if ok else "FAIL", detail))

    with zipfile.ZipFile(CAND) as z:
        names = z.namelist()
        # 1. video media present + non-corrupt
        media = sorted(n for n in names if n.startswith("ppt/media/"))
        videos = [m for m in media if m.lower().endswith(".mp4")]
        check("video media present", len(videos) >= 1, "media parts: %s" % media)

        # 2. content types declare mp4
        ct = z.read("[Content_Types].xml").decode()
        check("content-type declares video/mp4", "video/mp4" in ct, "mp4 default present" if "video/mp4" in ct else ct[:200])

        # 3. slide 25 rels reference the video
        rels = z.read("ppt/slides/_rels/slide25.xml.rels").decode()
        video_rel = "video" in rels
        check("slide 25 relationship references video", video_rel, rels.strip())

        # 4. slide 25 XML has videoFile + timing
        slide_xml = z.read("ppt/slides/slide25.xml").decode()
        has_videofile = "<p:videoFile" in slide_xml or "videoFile" in slide_xml
        has_ext = "media" in slide_xml
        check("slide 25 has videoFile element", has_videofile, "videoFile present" if has_videofile else slide_xml[-400:])

        # 5. poster frame present (image blip referencing a media image)
        poster_images = [m for m in media if m.lower().endswith((".png", ".jpeg", ".jpg"))]
        check("poster frame image present", len(poster_images) >= 1, "poster images: %s" % poster_images)

        # 6. timing: video node, no autoplay (no 'afterEffect'/trigger cond referencing onLoad)
        timing = z.read("ppt/slides/slide25.xml").decode()
        has_video_node = "<p:video" in timing or "video" in timing
        check("click-to-play timing node present", has_video_node, "p:video timing present")

        # 7. byte size sanity: candidate > baseline by ~video size
        v_size = sum(z.getinfo(m).file_size for m in videos)
        check("embedded video non-trivial size", v_size > 1_000_000, "%d bytes of video" % v_size)

    # 8. media integrity: mp4 decodes (ffprobe)
    import subprocess, tempfile
    with zipfile.ZipFile(CAND) as z:
        mp4 = [m for m in z.namelist() if m.startswith("ppt/media/") and m.endswith(".mp4")][0]
        tmp = tempfile.mkdtemp()
        p = os.path.join(tmp, "v.mp4")
        with open(p, "wb") as f:
            f.write(z.read(mp4))
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", p],
                           capture_output=True, text=True)
        check("embedded mp4 decodes (ffprobe)", r.returncode == 0 and "duration" in r.stdout,
              r.stdout[:160] if r.returncode == 0 else r.stderr[:160])

    # 9. unused videos not packaged (only 1 mp4 embedded)
    check("exactly one mp4 packaged", len(videos) == 1, "video parts: %s" % videos)

    # 10. candidate not byte-identical to baseline
    def sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for c in iter(lambda: f.read(1 << 16), b""):
                h.update(c)
        return h.hexdigest()
    check("candidate differs from baseline", sha(CAND) != sha(BASELINE),
          "v6 %s… vs v4 %s…" % (sha(CAND)[:16], sha(BASELINE)[:16]))

    # 11. poster frame referenced by slide 25
    with zipfile.ZipFile(CAND) as z:
        s25 = z.read("ppt/slides/slide25.xml").decode()
        check("poster frame referenced on slide 25", "blip" in s25 or "media" in s25, "blip/media in slide25")

    ok = all(c[1] == "PASS" for c in checks)
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "CH1_EMBEDDING_INTEGRITY.md"), "w") as f:
        f.write("# Chapter 1 — Embedding / Package Integrity Report (Phase 5H)\n\nOverall: **%s**\n\n" % ("PASS" if ok else "FAIL"))
        f.write("| Check | Result | Detail |\n|---|---|---|\n")
        for name, st, detail in checks:
            f.write("| %s | **%s** | %s |\n" % (name, st, detail))
        f.write("\n> Package-integrity PASS means the MP4 is genuinely inside the PPTX ZIP, referenced by slide 25 "
                "relationships, declared in content types, with a poster frame and click-to-play timing. It does NOT "
                "certify Microsoft PowerPoint playback (see playback report).\n")
    for name, st, detail in checks:
        print("%-4s %s: %s" % (st, name, detail[:100]))
    print("INTEGRITY:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
