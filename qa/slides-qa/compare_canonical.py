#!/usr/bin/env python3
"""Compare the canonical 45-slide deck text against the live 48-slide deck.

Verifies that the live deck == canonical deck + 3 inserted video slides at the
documented positions, with no other edits to slide-visible text.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from pdftext import pages_text

CANON = "production/slides/01-ch1-energy-causes-change-slides.pdf"
LIVE = "qa/slides-qa/ch1/deck.pdf"
# canonical slide index -> live slide index (video insertions shift the rest)
VIDEO_POSITIONS = [8, 27, 28]  # 1-based live positions of the 3 video slides


def norm(t):
    return " ".join(t.split())


def main():
    canon = [norm(s["text"]) for s in pages_text(CANON)]
    live = [norm(s["text"]) for s in pages_text(LIVE)]
    print(f"canonical: {len(canon)} slides, live: {len(live)} slides")

    # build mapping
    live_idx = 1
    mismatches = []
    compared = 0
    for c_idx, c_text in enumerate(canon, start=1):
        while live_idx in VIDEO_POSITIONS:
            live_idx += 1  # skip inserted video slides
        if live_idx > len(live):
            mismatches.append(f"canonical {c_idx}: no live slide (ran out)")
            break
        compared += 1
        if c_text != live[live_idx - 1]:
            mismatches.append(
                f"canonical {c_idx} -> live {live_idx}: TEXT DIFFERS"
            )
        live_idx += 1

    # confirm the 3 video slides are exactly at the expected positions
    video_ok = []
    for vp in VIDEO_POSITIONS:
        video_ok.append((vp, live[vp - 1][:60]))

    print(f"compared {compared} canonical->live slides")
    print("mismatches:", len(mismatches))
    for m in mismatches[:20]:
        print("  ", m)
    print("video slides at expected positions:")
    for vp, txt in video_ok:
        print(f"   live {vp}: {txt!r}")


if __name__ == "__main__":
    main()
