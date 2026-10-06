"""Shared fixtures for Phase B auditor tests. Nothing here is a classroom artifact."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "qa" / "work" / "_phase_b"


def build_identity():
    from chapter_qa.identity import BuildIdentity

    return BuildIdentity(
        buildId="phase-b-test",
        candidatePath="candidate/chapter-x",
        candidateFreezeId="cand-1",
        candidateHash="a" * 64,
        sourceFreezeId="src-1",
        sourceHash="b" * 64,
        inputHashes={"candidate": "c" * 64, "reader": "d" * 64},
    )


def evidence_file(name: str) -> str:
    folder = WORK / "evidence"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    path.write_text("{}\n", encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def cleanup_work() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)


def write_pdf(path: Path, pages: list[tuple[int, int, bytes]]) -> None:
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    kids = " ".join("%d 0 R" % (3 + index * 2) for index in range(len(pages)))
    objects.append(("<< /Type /Pages /Count %d /Kids [%s] >>" % (len(pages), kids)).encode())
    font_id = 3 + len(pages) * 2
    for index, (width, height, stream) in enumerate(pages):
        page_id = 3 + index * 2
        content_id = page_id + 1
        page = (
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Contents %d 0 R "
            "/Resources << /Font << /F1 %d 0 R >> >> >>"
        ) % (width, height, content_id, font_id)
        objects.append(page.encode())
        objects.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    header = b"%PDF-1.4\n"
    body = header
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(body))
        body += ("%d 0 obj\n" % number).encode() + obj + b"\nendobj\n"
    xref_at = len(body)
    xref = ["xref\n0 %d\n" % (len(objects) + 1), "0000000000 65535 f \n"]
    xref.extend("%010d 00000 n \n" % offset for offset in offsets[1:])
    trailer = "trailer << /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref_at)
    path.write_bytes(body + "".join(xref).encode() + trailer.encode())
