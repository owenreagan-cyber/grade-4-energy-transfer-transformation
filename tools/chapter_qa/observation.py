"""Generic artifact observation: open real files and derive text/facts.

Release-blocking producers must observe actual bytes. This module provides
the readers they use so that a producer never treats caller-supplied text as
the observed artifact.

Readers return structured facts derived from bytes. They do not assign PASS
and they do not trust a caller's "clean" observation.
"""

from __future__ import annotations

import json
import re
import subprocess
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

_TEXT_SUFFIXES = {".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml"}


def _resolve(path, root: Path | None = None) -> Path:
    p = Path(str(path))
    base = root or REPO_ROOT
    if p.is_absolute():
        return p
    return base / p


def read_text(path, root: Path | None = None) -> str:
    return _resolve(path, root).read_text(encoding="utf-8", errors="replace")


def read_json(path, root: Path | None = None):
    with open(_resolve(path, root), encoding="utf-8") as handle:
        return json.load(handle)


def _zip_xml_text(path: Path, parts: tuple[str, ...]) -> str:
    if not path.is_file():
        return ""
    try:
        with zipfile.ZipFile(path) as archive:
            names = [n for n in archive.namelist() if n.endswith(".xml")]
            chunks = []
            for name in names:
                base = name.rstrip("0123456789") if False else name
                if not any(name.startswith(prefix) for prefix in parts):
                    continue
                raw = archive.read(name)
                text = _strip_xml(raw)
                if text:
                    chunks.append(text)
            return "\n".join(chunks)
    except (zipfile.BadZipFile, KeyError, OSError):
        return ""
    return ""


def _strip_xml(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    # paragraph / line breaks become spaces or newlines; tags become separators.
    text = re.sub(r"</w:p>|</a:p>", "\n", text)
    text = re.sub(r"<w:tab/>|<a:tab/>", "\t", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def read_docx_text(path, root: Path | None = None) -> str:
    return _zip_xml_text(_resolve(path, root), ("word/document.xml",))


def read_pptx_text(path, root: Path | None = None) -> str:
    """Slide text plus speaker notes. Hidden slides are included and marked."""
    p = _resolve(path, root)
    if not p.is_file():
        return ""
    try:
        with zipfile.ZipFile(p) as archive:
            slides = sorted(
                (n for n in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                key=lambda n: int(re.search(r"(\d+)", n).group(1)),
            )
            notes = sorted(
                (n for n in archive.namelist() if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)),
                key=lambda n: int(re.search(r"(\d+)", n).group(1)),
            )
            chunks = []
            for idx, name in enumerate(slides, 1):
                chunks.append("SLIDE %d\n%s" % (idx, _strip_xml(archive.read(name))))
            for idx, name in enumerate(notes, 1):
                chunks.append("NOTES %d\n%s" % (idx, _strip_xml(archive.read(name))))
            return "\n".join(chunks)
    except (zipfile.BadZipFile, KeyError, OSError):
        return ""
    return ""


def read_pdf_text(path, root: Path | None = None) -> str:
    p = _resolve(path, root)
    if not p.is_file():
        return ""
    completed = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    return completed.stdout or ""


def read_any_text(path, root: Path | None = None) -> str:
    """Dispatch to the right reader by suffix."""
    p = _resolve(path, root)
    suffix = p.suffix.lower()
    if suffix == ".docx":
        return read_docx_text(p)
    if suffix == ".pptx":
        return read_pptx_text(p)
    if suffix == ".pdf":
        return read_pdf_text(p)
    return read_text(p)


def normalized(text: str) -> str:
    """Whitespace-and-case fold for comparison, preserving word order."""
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def list_files(directory, root: Path | None = None, *, recurse: bool = False) -> list[str]:
    """Filesystem scan: actual observed file set, sorted by relative path."""
    base = _resolve(directory, root)
    if not base.is_dir():
        return []
    pattern = "**/*" if recurse else "*"
    return sorted(str(p.relative_to(base)) for p in base.glob(pattern) if p.is_file())
