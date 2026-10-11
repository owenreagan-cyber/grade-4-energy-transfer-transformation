#!/usr/bin/env python3
"""Extract per-page slide-visible text from a deck PDF (via pdftotext).

The PDF is the rendered deck: it contains only slide-visible text (speaker
notes are absent), which is exactly what the curriculum parity and answer-leak
checks need. Pages split on the form-feed separator pdftotext emits.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def pages_text(pdf_path: str) -> list[dict]:
    out = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    pages = out.split("\f")
    result = []
    for i, page in enumerate(pages, start=1):
        text = " ".join(page.split())
        if i <= len(pages) and (text or i <= len(pages)):
            result.append({"index": i, "text": text})
    # drop a trailing empty page produced by the trailing form feed
    while result and not result[-1]["text"]:
        result.pop()
    return result


def main():
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", help="write JSON to file")
    args = ap.parse_args()
    pages = pages_text(args.pdf)
    payload = json.dumps({"pages": len(pages), "slides": pages}, indent=2)
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
