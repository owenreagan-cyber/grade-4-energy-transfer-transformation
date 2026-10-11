#!/usr/bin/env python3
"""Render a deck PDF to per-slide high-resolution PNGs (pdftoppm).

Deterministic and dependency-light. Used for the independent visual audit and
as the projector-fidelity reference.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def render_pdf(pdf_path: str, out_dir: str, dpi: int = 150,
               prefix: str = "slide") -> list[dict]:
    """Render every page of `pdf_path` to PNG at `dpi`. Returns records."""
    pdf = Path(pdf_path)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = out / prefix
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(stem)],
        check=True, capture_output=True, text=True,
    )
    pngs = sorted(out.glob(f"{prefix}-*.png"))
    records = []
    for p in pngs:
        # pdftoppm names pages as <prefix>-01.png, <prefix>-02.png, ...
        try:
            num = int(p.stem.split("-")[-1])
        except ValueError:
            num = 0
        records.append({"page": num, "path": str(p)})
    records.sort(key=lambda r: r["page"])
    return records


def pdf_page_count(pdf_path: str) -> int:
    out = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True,
                         check=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--prefix", default="slide")
    args = ap.parse_args()
    recs = render_pdf(args.pdf, args.out, args.dpi, args.prefix)
    print(json.dumps({"pages": len(recs), "records": recs}, indent=2))


if __name__ == "__main__":
    main()
