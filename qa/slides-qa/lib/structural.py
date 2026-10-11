#!/usr/bin/env python3
"""Structural audit of a Google Slides deck from its exports.

Inputs (produced by the Google Drive MCP retrieval layer):
  - a plain-text export (Slides -> text, one slide per block)
  - an optional PPTX export (for video-shape / media detection)

Outputs per-slide text, a slide count, and a stable slide identity (position +
content hash). NOTE: Google Slides' internal object IDs are only available via
the Slides API (not the Drive export path), so the stable key used here is
`position` plus a SHA-1 of normalized slide text.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def stable_id(slide_index: int, text: str) -> str:
    h = hashlib.sha1(_norm(text).encode("utf-8")).hexdigest()[:10]
    return f"s{slide_index:02d}-{h}"


def load_pptx(path: str) -> list[dict]:
    """Extract per-slide text + video detection from a PPTX export."""
    out = []
    with zipfile.ZipFile(path) as z:
        slide_names = sorted(
            n for n in z.namelist()
            if re.match(r"ppt/slides/slide\d+\.xml$", n)
        )
        media = [n for n in z.namelist() if n.startswith("ppt/media/")]
        for name in slide_names:
            idx = int(re.search(r"slide(\d+)\.xml$", name).group(1))
            xml = z.read(name).decode("utf-8", "ignore")
            texts = re.findall(r"<a:t>(.*?)</a:t>", xml, flags=re.S)
            text = _norm(" ".join(texts))
            has_video = "<p:videoFile" in xml or "videoFile" in xml
            # gather relationship targets for video detection
            rels_name = f"ppt/slides/_rels/slide{idx}.xml.rels"
            rel_targets = []
            if rels_name in z.namelist():
                rels = z.read(rels_name).decode("utf-8", "ignore")
                rel_targets = re.findall(r'Target="([^"]+)"', rels)
            video_hint = has_video or any(
                (".mp4" in t or "video" in t.lower()) for t in rel_targets
            )
            out.append({
                "index": idx,
                "text": text,
                "has_video_shape": has_video,
                "video_hint": video_hint,
                "rel_targets": rel_targets,
            })
    out.sort(key=lambda s: s["index"])
    for s in out:
        s["stable_id"] = stable_id(s["index"], s["text"])
    return out


def load_txt(path: str) -> list[dict]:
    """Parse a plain-text Slides export into per-slide blocks.

    Google's plain-text Slides export separates slides with a line of
    backticks or a blank line + index. This parser is deliberately tolerant.
    """
    raw = Path(path).read_text(encoding="utf-8", errors="ignore")
    # Split on lines that look like slide separators
    parts = re.split(r"\n\s*`{3,}\s*\n|\n={3,}\n|\n(?=Slide\s+\d+)", raw)
    slides = []
    for i, part in enumerate(parts, start=1):
        text = _norm(part)
        if not text and i > 1:
            continue
        slides.append({"index": i, "text": text})
    for s in slides:
        s["stable_id"] = stable_id(s["index"], s["text"])
    return slides


def summary(slides: list[dict]) -> dict:
    return {
        "slideCount": len(slides),
        "videoSlides": [
            s["index"] for s in slides
            if s.get("has_video_shape") or s.get("video_hint")
        ],
        "slides": [{"index": s["index"], "stable_id": s["stable_id"],
                    "text": s["text"][:400]} for s in slides],
    }


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pptx", help="PPTX export path")
    ap.add_argument("--txt", help="plain-text export path")
    args = ap.parse_args()
    if args.pptx:
        slides = load_pptx(args.pptx)
    elif args.txt:
        slides = load_txt(args.txt)
    else:
        raise SystemExit("provide --pptx or --txt")
    print(json.dumps(summary(slides), indent=2))


if __name__ == "__main__":
    main()
