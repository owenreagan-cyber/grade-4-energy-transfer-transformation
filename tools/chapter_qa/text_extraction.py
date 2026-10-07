"""Shared text/structure extraction for producer independence.

Deterministic extraction of student/teacher-visible content from DOCX, PPTX,
PDF, Markdown, and JSON. Producers use this to derive observations from real
bytes; they must not trust caller-supplied text.

Extraction preserves distinctions that matter for certification:
- blank vs filled answer (``____`` vs a word)
- WRITE vs REVEAL surface
- student vs key file
- anchor codes
- question numbering
- score lines
- units
- negation
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve(path, root: Path | None = None) -> Path:
    p = Path(str(path))
    base = root or REPO_ROOT
    return p if p.is_absolute() else base / p


def normalize(text: str) -> str:
    """Whitespace-and-case fold; preserves word order and punctuation as spaces."""
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def read_bytes(path, root: Path | None = None) -> bytes:
    p = _resolve(path, root)
    if not p.is_file():
        return b""
    return p.read_bytes()


def _strip_xml(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    text = re.sub(r"</w:p>|</a:p>", "\n", text)
    text = re.sub(r"<w:tab/>|<a:tab/>", "\t", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def docx_paragraphs(path, root: Path | None = None) -> list[str]:
    """Paragraph-level text from a DOCX document body."""
    p = _resolve(path, root)
    if not p.is_file():
        return []
    try:
        with zipfile.ZipFile(p) as archive:
            raw = archive.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError, OSError):
        return []
    text = _strip_xml(raw)
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def docx_tables(path, root: Path | None = None) -> list[list[str]]:
    """Table cells as a list of row-lists, preserving blank cells."""
    p = _resolve(path, root)
    if not p.is_file():
        return []
    try:
        with zipfile.ZipFile(p) as archive:
            raw = archive.read("word/document.xml")
    except (zipfile.BadZipFile, KeyError, OSError):
        return []
    text = raw.decode("utf-8", errors="replace")
    tables = []
    for table in re.findall(r"<w:tbl>.*?</w:tbl>", text, re.S):
        rows = []
        for row in re.findall(r"<w:tr>.*?</w:tr>", table, re.S):
            cells = []
            for cell in re.findall(r"<w:tc>.*?</w:tc>", row, re.S):
                cell_text = _strip_xml(cell.encode("utf-8"))
                cells.append(normalize(cell_text))
            rows.append(cells)
        tables.append(rows)
    return tables


def pptx_slides(path, root: Path | None = None) -> list[dict]:
    """Per-slide visible text and speaker notes, with hidden status and order."""
    p = _resolve(path, root)
    if not p.is_file():
        return []
    try:
        with zipfile.ZipFile(p) as archive:
            slide_names = sorted(
                (n for n in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                key=lambda n: int(re.search(r"(\d+)", n).group(1)),
            )
            notes_names = {
                int(re.search(r"(\d+)", n).group(1)): n
                for n in archive.namelist()
                if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)
            }
            slides = []
            for index, name in enumerate(slide_names, 1):
                raw = archive.read(name)
                txt = raw.decode("utf-8", errors="replace")
                hidden = 'show="0"' in txt
                slides.append({
                    "slide": index,
                    "text": _strip_xml(raw),
                    "hidden": hidden,
                    "notes": _strip_xml(archive.read(notes_names[index])) if index in notes_names else "",
                })
            return slides
    except (zipfile.BadZipFile, KeyError, OSError):
        return []


SLIDE_MARK = re.compile(r"\bSLIDE\s+(\d+)\b", re.I)
NOTES_MARK = re.compile(r"\bNOTES\s+(\d+)\b", re.I)


def slide_blocks(path, root: Path | None = None) -> list[dict]:
    """Per-slide blocks with text and speaker notes.

    For PPTX uses the zip reader; for text fixtures (Markdown/plain), splits on
    ``SLIDE n`` / ``NOTES n`` markers so producers work on both real decks and
    text fixtures. Returns ``[{"slide": int, "text": str, "notes": str}]``.
    """
    p = _resolve(path, root)
    if not p.is_file():
        return []
    if p.suffix.lower() == ".pptx":
        return pptx_slides(p, root)
    text = p.read_text(encoding="utf-8", errors="replace")
    slides = {}
    notes = {}
    current = None
    current_notes = None
    for line in text.splitlines():
        sm = SLIDE_MARK.search(line)
        nm = NOTES_MARK.search(line)
        if sm:
            current = int(sm.group(1))
            current_notes = None
            slides.setdefault(current, [])
        elif nm:
            current_notes = int(nm.group(1))
            notes.setdefault(current_notes, [])
            current = None
        elif current is not None:
            slides[current].append(line)
        elif current_notes is not None:
            notes[current_notes].append(line)
    result = []
    for index in sorted(slides):
        result.append({
            "slide": index,
            "text": "\n".join(slides[index]).strip(),
            "notes": "\n".join(notes.get(index, [])).strip(),
            "hidden": False,
        })
    return result


def pdf_text(path, root: Path | None = None) -> str:
    import subprocess

    p = _resolve(path, root)
    if not p.is_file():
        return ""
    completed = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    return completed.stdout or ""


def pdf_pages(path, root: Path | None = None) -> list[str]:
    import subprocess

    p = _resolve(path, root)
    if not p.is_file():
        return []
    completed = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True)
    pages = (completed.stdout or "").split("\f")
    return [page for page in pages if page.strip()]


def extract_text(path, root: Path | None = None) -> str:
    """Unified text extraction across DOCX/PPTX/PDF/MD/JSON."""
    p = _resolve(path, root)
    if not p.is_file():
        return ""
    suffix = p.suffix.lower()
    if suffix == ".docx":
        return "\n".join(docx_paragraphs(p, root))
    if suffix == ".pptx":
        return "\n".join(s["text"] + "\n" + s["notes"] for s in pptx_slides(p, root))
    if suffix == ".pdf":
        return pdf_text(p, root)
    if suffix == ".json":
        try:
            return json.dumps(json.loads(p.read_text(encoding="utf-8")), ensure_ascii=False)
        except (OSError, ValueError):
            return ""
    return p.read_text(encoding="utf-8", errors="replace")


# --- anchor / structure extraction ---

ANCHOR_CODE = re.compile(r"\b(BQ(?:_NOW|_NO)?|V\d|N\d|DEMO|LAB|GRAPH|CHECK|DROP|RECOVER)\b")


def anchor_codes_in_order(text: str, expected_codes) -> list[str]:
    """Anchor codes present in text, in first-occurrence order, limited to expected."""
    lowered = normalize(text)
    found = []
    positions = {}
    for code in expected_codes:
        token = normalize(str(code))
        match = re.search(r"\b" + re.escape(token) + r"\b", lowered)
        if match:
            positions[str(code)] = match.start()
    for code in sorted(positions, key=lambda c: positions[c]):
        found.append(code)
    return found


BLANK = re.compile(r"_{2,}")


def blank_count(text: str) -> int:
    return len(BLANK.findall(text))


def units_present(text: str, units=("cm", "centimeter", "centimeters")) -> bool:
    lowered = normalize(text)
    return any(unit in lowered for unit in units)


def negation_present(text: str) -> bool:
    return bool(re.search(r"\b(not|never|do not|does not|don't|doesn't)\b", text, re.I))


# --- boundary / forbidden families (generic; expanded by producer config) ---

SPEED_QUANTITY = re.compile(
    r"\b\d+\s*(m/s|meters?\s+per\s+second|metres?\s+per\s+second|km/h|mph|kph)\b", re.I,
)
RAMP_IS_SPEED = re.compile(
    r"\b(ramp\s+height|height)\b[^.]{0,40}\b(is|equals|tells|shows|measures|means)\b[^.]{0,40}\b(speed)\b",
    re.I,
)
ADVANCED_VOCAB = re.compile(r"\b(kinetic|potential|mechanical|inertia|radiant|compression\s*wave)\b", re.I)
MASS_COMPARISON = re.compile(
    r"\b(heavier|lighter|more\s+massive|less\s+massive|different\s+(ball|object|mass))\b[^.]{0,60}\b(more|greater|energy)\b",
    re.I,
)


def family_hits(text: str) -> dict[str, list[str]]:
    """Return matched spans per boundary family. Used by CURRICULUM_CORRECTNESS."""
    hits = {}
    for name, pattern in (
        ("speed_quantity", SPEED_QUANTITY),
        ("ramp_is_speed", RAMP_IS_SPEED),
        ("advanced_vocab", ADVANCED_VOCAB),
        ("mass_comparison", MASS_COMPARISON),
    ):
        matches = [m.group(0) for m in pattern.finditer(text)]
        if matches:
            hits[name] = matches
    return hits
