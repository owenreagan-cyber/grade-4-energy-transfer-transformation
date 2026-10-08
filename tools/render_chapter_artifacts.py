"""Headless chapter render. Writes only under an isolated QA directory.

Default page render is 300 DPI. Suspicious crops are 600 DPI.
A contact sheet is a navigation aid, not exhaustive visual evidence.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chapter_qa.workspace import assert_output_allowed

DEFAULT_DPI = 300
CROP_DPI = 600


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stem(path: str) -> str:
    # Include the source extension so a DOCX and a PDF with the same basename
    # cannot collide in a shared output directory (no basename-only identity).
    name = os.path.basename(path).lower()
    cleaned = re.sub(r"[^a-z0-9.]+", "-", name).replace(".", "-").strip("-")
    return cleaned or "artifact"


def planned_png_name(source: str, page_index: int, dpi: int = DEFAULT_DPI) -> str:
    return "%s-p%03d-%ddpi.png" % (_stem(source), page_index, dpi)


def guard_output_directory(out_dir: str, repo_root: str) -> None:
    assert_output_allowed(os.path.abspath(out_dir), repo_root)


def headless_render(source: str, out_dir: str, *, dpi: int = DEFAULT_DPI, repo_root: str) -> dict:
    """Convert DOCX/PPTX/PDF to a PDF and then to PNG pages. No visible desktop."""
    guard_output_directory(out_dir, repo_root)
    os.makedirs(out_dir, exist_ok=True)
    source_hash = _sha256(source)
    pdf_path = os.path.join(out_dir, _stem(source) + ".pdf")
    if source.lower().endswith(".pdf"):
        pdf_path = source
    else:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", out_dir, source],
            check=True,
            capture_output=True,
        )
        produced = os.path.join(out_dir, os.path.splitext(os.path.basename(source))[0] + ".pdf")
        if produced != pdf_path and os.path.exists(produced):
            os.replace(produced, pdf_path)
    info = subprocess.run(["pdfinfo", pdf_path], check=True, capture_output=True, text=True)
    pages = 0
    for line in info.stdout.splitlines():
        if line.startswith("Pages:"):
            pages = int(line.split(":", 1)[1].strip())
    prefix = os.path.join(out_dir, _stem(source))
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), pdf_path, prefix], check=True, capture_output=True)
    renders = []
    width = max(1, len(str(pages)))
    for index in range(1, pages + 1):
        produced = "%s-%d.png" % (prefix, index)
        padded = "%s-%0*d.png" % (prefix, width, index)
        target = os.path.join(out_dir, planned_png_name(source, index, dpi))
        if os.path.exists(produced):
            os.replace(produced, target)
        elif os.path.exists(padded):
            os.replace(padded, target)
        if not os.path.exists(target):
            raise RuntimeError("missing render page %s" % index)
        renders.append({
            "artifactId": _stem(source),
            "artifactPath": source,
            "artifactHash": source_hash,
            "renderPath": target,
            "renderHash": _sha256(target),
            "pageOrSlide": index,
            "dpi": dpi,
            "navigation": False,
            "renderedAt": _utc(),
        })
    return {
        "source": source,
        "sourceHash": source_hash,
        "pdfPath": pdf_path,
        "pageCount": pages,
        "dpi": dpi,
        "renders": renders,
        "renderedAt": _utc(),
        "toolVersions": _tool_versions(),
    }


def mark_contact_sheet(path: str) -> dict:
    return {"path": path, "role": "navigation", "exhaustive": False, "dpi": None}


def _tool_versions() -> dict:
    versions = {}
    for command, args in (
        ("soffice", ["soffice", "--version"]),
        ("pdftoppm", ["pdftoppm", "-v"]),
        ("pdfinfo", ["pdfinfo", "-v"]),
    ):
        completed = subprocess.run(args, capture_output=True, text=True, check=False)
        versions[command] = (completed.stdout or completed.stderr).splitlines()[0] if (completed.stdout or completed.stderr) else "unknown"
    return versions
