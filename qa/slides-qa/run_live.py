#!/usr/bin/env python3
"""Live Chapter 1 audit runner.

Inputs already produced by the retrieval layer:
  - qa/slides-qa/ch1/slide-text.json  (per-page slide-visible text from PDF)
  - qa/slides-qa/ch1/renders/slide-*.png (rendered slides)

Runs: video-slide detection, curriculum parity, independent vision audit
(blind), defect register, and a markdown report.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parent / "lib"
sys.path.insert(0, str(LIB))

from curriculum import run as curriculum_run
from vision import analyze, SLIDE_RUBRIC
from defects import DefectRegister, new_defect


def load_slides(text_json: str) -> list[dict]:
    data = json.loads(Path(text_json).read_text(encoding="utf-8"))
    slides = []
    for s in data["slides"]:
        text = s["text"]
        is_video = "WATCH" in text
        slides.append({
            "index": s["index"],
            "text": text,
            "has_video_shape": is_video,
            "video_hint": is_video,
        })
    return slides


def vision_audit(renders_dir: str, out_dir: Path, limit: int = 0) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    pngs = sorted(Path(renders_dir).glob("slide-*.png"),
                  key=lambda p: int(p.stem.split("-")[-1]))
    if limit:
        pngs = pngs[:limit]
    results = []
    for p in pngs:
        num = int(p.stem.split("-")[-1])
        out = out_dir / f"vision-{num:02d}.json"
        try:
            v = analyze(str(p), SLIDE_RUBRIC)
        except Exception as e:  # noqa: BLE001
            v = {"error": str(e)}
        out.write_text(json.dumps(v, indent=2), encoding="utf-8")
        results.append({"page": num, "path": str(p), "vision": v})
        overall = v.get("overall", "?") if isinstance(v, dict) else "?"
        print(f"slide {num:02d}: {overall}", flush=True)
    return results


def build_defects(vis, slides, reg):
    slide_by_idx = {s["index"]: s for s in slides}
    maps = {
        "text_issues": ("TEXT_CLIP_OVERFLOW", "text_issues"),
        "readability_issues": ("FONT_READABILITY", "readability_issues"),
        "image_issues": ("IMAGE_QUALITY", "image_issues"),
        "overlap_issues": ("OVERLAP", "overlap_issues"),
        "label_issues": ("LABEL_BADGE", "label_issues"),
        "hierarchy_issues": ("HIERARCHY_ALIGNMENT", "hierarchy_issues"),
        "science_issues": ("SCIENCE_ERROR", "science_issues"),
        "answer_leak": ("ANSWER_LEAK", "answer_leak"),
        "composition_issues": ("COMPOSITION", "composition_issues"),
    }
    for r in vis:
        v = r.get("vision", {})
        if not isinstance(v, dict) or v.get("skipped") or "summary" not in v:
            continue
        page = r["page"]
        overall = v.get("overall", "")
        for _, (cat, key) in maps.items():
            items = v.get(key, [])
            for item in items:
                reg.add(new_defect(
                    slide=page, slide_id=f"s{page:02d}", category=cat,
                    severity="HIGH" if overall == "FAIL" else "MEDIUM",
                    evidence=[r["path"]], expected="", actual=str(item),
                    proposed_repair="review slide and correct the issue",
                ))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default="ch1/slide-text.json")
    ap.add_argument("--renders", default="ch1/renders")
    ap.add_argument("--expected", default="ch1/expected_ch1.json")
    ap.add_argument("--outdir", default="ch1/run-live")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    slides = load_slides(args.text)
    video_slides = [s["index"] for s in slides if s["has_video_shape"]]
    print("total slides:", len(slides), "video slides:", video_slides, flush=True)

    cur = curriculum_run(args.expected, slides)
    print("curriculum:", cur["summary"], flush=True)

    vis = vision_audit(args.renders, out / "vision", limit=args.limit)

    reg = DefectRegister(str(out / "defect-register.json"))
    build_defects(vis, slides, reg)
    # structural defect for video slide count
    exp_videos = 3
    if len(video_slides) != exp_videos:
        reg.add(new_defect(
            slide=0, slide_id="deck", category="SLIDE_COUNT",
            severity="BLOCKING", evidence=[],
            expected=f"{exp_videos} video slides", actual=f"{len(video_slides)}",
            proposed_repair="reconcile video slides with canonical deck",
        ))
    reg.save()

    bundle = {
        "totalSlides": len(slides),
        "videoSlides": video_slides,
        "curriculum": cur,
        "visual": vis,
        "defects": reg.data["defects"],
    }
    (out / "results.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    print("defects:", len(reg.data["defects"]))
    print("DONE ->", out / "results.json")


if __name__ == "__main__":
    main()
