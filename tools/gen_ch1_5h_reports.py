#!/usr/bin/env python3
"""Phase 5H — emit video inventory, media manifest, slide-to-video map, and copy transcripts."""
import hashlib, json, os, shutil, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "qa", "reports", "ch1-phase5g")
INTAKE = os.path.join(ROOT, "source-intake", "2026-10-09-chapter-1", "media")
SUPP = os.path.join(ROOT, "assets", "supplemental", "media", "chapter-01")
TXT = "/tmp/whisper_txt"

# 19 unique videos: (label, path, verdict, reason)
VIDEOS = [
    ("Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4", os.path.join(INTAKE, "Energy_Causes_Change__The_Electric_Pencil_Sharpener.mp4"),
     "REJECTED", "narrated 'proof', 'transferred', 'electrical current', 'physical work'; interactive workbook (3:05)"),
    ("Energy_Causes_Change__The_Energy_Detective.mp4", os.path.join(INTAKE, "Energy_Causes_Change__The_Energy_Detective.mp4"),
     "REJECTED", "narrated technical terms: 'acoustic output', 'baseline inventory', 'visual geometry' (3:49)"),
    ("Energy_Causes_Change.mp4", os.path.join(INTAKE, "Energy_Causes_Change.mp4"),
     "REJECTED", "renewable energy / power grid (Unit 2); 'wind stops or the sun sets' (6:43)"),
    ("Energy_Detective.mp4", os.path.join(INTAKE, "Energy_Detective.mp4"),
     "REJECTED", "collision content 'the dent is evidence' (Ch.2/Ch.5) (5:48)"),
    ("Energy_Detectives.mp4", os.path.join(INTAKE, "Energy_Detectives.mp4"),
     "REJECTED", "wind turbines / electricity generation (Unit 2) (7:17)"),
    ("Energy_Detectives_Briefing.mp4", os.path.join(INTAKE, "Energy_Detectives_Briefing.mp4"),
     "REJECTED", "scavenger-hunt briefing; narrated 'prove/proves' (7:53)"),
    ("The_Energy_Detective-4.mp4", os.path.join(INTAKE, "The_Energy_Detective-4.mp4"),
     "REJECTED", "marble collision 'moving marble hits the target' (Ch.2/Ch.5) (5:55)"),
    ("The_Energy_Detective-3.mp4", os.path.join(INTAKE, "The_Energy_Detective-3.mp4"),
     "REJECTED", "narrated 'proof' (5:32)"),
    ("The_Energy_Detective-2.mp4", os.path.join(INTAKE, "The_Energy_Detective-2.mp4"),
     "REJECTED", "narrated 'prove/proof/proves' (6:47)"),
    ("The_Energy_Detective.mp4", os.path.join(INTAKE, "The_Energy_Detective.mp4"),
     "REJECTED", "narrated 'proof', 'transfer', 'transforms', 'collision', 'wind turbine', 'force' (6:45)"),
    ("Chapter_1_Review.mp4", os.path.join(INTAKE, "Chapter_1_Review.mp4"),
     "REJECTED", "'Electrical to light' transformation = Ch.6 scope (7:17)"),
    ("Chapter_1_Science_Notebook.mp4", os.path.join(INTAKE, "Chapter_1_Science_Notebook.mp4"),
     "REJECTED", "narrated 'transforms', 'grid', 'transfer', 'radiant', 'potential', 'mechanical' (8:26)"),
    ("The_Invisible_Boss_of_Change.mp4", os.path.join(INTAKE, "The_Invisible_Boss_of_Change.mp4"),
     "REJECTED", "cinematic Ch.2 opener (per MEDIA_ASSET_MANIFEST) (2:50)"),
    ("The_Unseen_Mover.mp4", os.path.join(INTAKE, "The_Unseen_Mover.mp4"),
     "REJECTED", "motion hook (Ch.2) (5:27)"),
    ("How_Change_Proves_Energy_Exists.mp4", os.path.join(INTAKE, "How_Change_Proves_Energy_Exists.mp4"),
     "REJECTED", "narrated 'proves', 'energy transfer', 'transforms into motion/sound/heat' (1:23)"),
    ("How_Physical_Change_Proves_Energy_Exists.mp4", os.path.join(INTAKE, "How_Physical_Change_Proves_Energy_Exists.mp4"),
     "REJECTED", "narrated 'proof', 'energy transfer', 'mechanical' (1:19)"),
    ("How_Scientists_Spot_Invisible_Energy.mp4", os.path.join(INTAKE, "How_Scientists_Spot_Invisible_Energy.mp4"),
     "REJECTED", "narrated 'prove/proof', 'zero scientific proof of energy' (contradicts N3) (1:16)"),
    ("Stored_Energy.mp4", os.path.join(INTAKE, "Stored_Energy.mp4"),
     "APPROVED_EMBEDDED", "landscape; zero banned terms; canonical V2 definition verbatim; battery/rubber/apple/position = N3 (4:37)"),
    ("Why_Still_Objects_Secretly_Have_Energy.mp4", os.path.join(SUPP, "Why_Still_Objects_Secretly_Have_Energy.mp4"),
     "APPROVED_ALTERNATE", "zero banned terms; clean; portrait 720x1280; directly answers slide-23 prediction (place after slide 25 reveal) (1:16)"),
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def ffprobe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,channels",
                        "-of", "json", p], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else {}


def main():
    os.makedirs(OUT, exist_ok=True)
    txtdir = os.path.join(OUT, "transcripts")
    os.makedirs(txtdir, exist_ok=True)
    for f in os.listdir(TXT):
        shutil.copy(os.path.join(TXT, f), os.path.join(txtdir, f))

    rows = []
    manifest = []
    for name, path, verdict, reason in VIDEOS:
        meta = ffprobe(path)
        fmt = meta.get("format", {})
        streams = meta.get("streams", [])
        v = next((s for s in streams if s["codec_type"] == "video"), {})
        a = next((s for s in streams if s["codec_type"] == "audio"), {})
        dur = float(fmt.get("duration", 0))
        h = sha256(path)
        rows.append(dict(name=name, path=path, sha256=h, duration_s=round(dur, 1),
                         res="%sx%s" % (v.get("width"), v.get("height")),
                         fps=v.get("r_frame_rate"), vcodec=v.get("codec_name"),
                         acodec=a.get("codec_name"), channels=a.get("channels"),
                         verdict=verdict, reason=reason))
        manifest.append(dict(name=name, sha256=h, bytes=int(fmt.get("size", 0)),
                             duration_s=round(dur, 1), res="%sx%s" % (v.get("width"), v.get("height")),
                             vcodec=v.get("codec_name"), acodec=a.get("codec_name"),
                             verdict=verdict))

    json.dump(manifest, open(os.path.join(OUT, "CH1_MEDIA_MANIFEST_5H.json"), "w"), indent=1)

    # inventory markdown
    lines = ["# Chapter 1 — Approved / Rejected / Unverified Video Inventory (Phase 5H)\n",
             "19 unique videos, narration-verified via faster-whisper (base.en) where on-scope; frames + OCR elsewhere.\n",
             "| # | File | Dur | Res | v/a codec | Verdict | Reason |\n|---|---|---|---|---|---|---|\n"]
    for i, r in enumerate(rows, 1):
        lines.append("| %d | %s | %.0fs | %s | %s/%s | **%s** | %s |\n" % (
            i, r["name"], r["duration_s"], r["res"], r["vcodec"], r["acodec"], r["verdict"], r["reason"]))
    lines.append("\n## Summary\n")
    from collections import Counter
    c = Counter(r["verdict"] for r in rows)
    for k, v in c.items():
        lines.append("- %s: %d\n" % (k, v))
    open(os.path.join(OUT, "CH1_VIDEO_INVENTORY_5H.md"), "w").write("".join(lines))

    # slide-to-video map
    smap = ["# Chapter 1 — Slide-to-Video Mapping (Phase 5H)\n",
            "One genuine embed. Canonical slide sequence preserved (no new slides added).\n\n",
            "| Slide | Function | Video | Placement | Fallback |\n|---|---|---|---|---|\n",
            "| 25 | Stored energy can cause a change later (STORED→RELEASE→CHANGE) | `Stored_Energy.mp4` (4:37, 16:9) | bottom-left player (0.75,5.6 → 3.95,7.4 in), click-to-play, no autoplay | skip — model + live battery/rubber/apple demos |\n",
            "| (alt, after 25) | N3 reinforcement — still objects store energy | `Why_Still_Objects_Secretly_Have_Energy.mp4` (1:16, portrait) | NOT embedded (portrait + answers the slide-23 prediction) | optional Friday FLEX |\n\n",
            "Video A (pencil) and Video B (evidence) have no clean candidate (all rejected: 'proof/transfer/transforms'). Video C (five forms) has no clean short candidate.\n"]
    open(os.path.join(OUT, "CH1_SLIDE_TO_VIDEO_MAP_5H.md"), "w").write("".join(smap))

    print("inventory rows:", len(rows), "| verdicts:", dict(c))
    print("wrote manifest, inventory, slide-to-video map; copied %d transcripts" % len(os.listdir(txtdir)))


if __name__ == "__main__":
    main()
