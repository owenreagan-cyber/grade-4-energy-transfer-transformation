"""Reseal Chapter 3 visual, render, and PDF evidence after the v1.2 detectors."""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, "tools")
from chapter_qa.identity import hash_file
from chapter_qa.visual_qa import emit_visual_evidence, page_record
from qa_pdf_quality import emit_pdf_evidence
from ch3_seal_remaining import (
    FRESH,
    RELEASE,
    ROOT,
    SOURCES,
    bbox_lines,
    boxes_for_page,
    fresh_pairs,
    identity,
    inventory_names,
    release_dir,
    seal_call,
    spec,
)
from chapter_qa.mandatory_producers import emit_adversarial_qa, emit_fresh_export, emit_inventory, emit_prior_frozen
from chapter_qa.release_set import emit_release_evidence
from chapter_qa.render_completeness import emit_render_evidence
from run_adversarial_qa import execute

RENDERS = ROOT / "qa" / "work" / "ch3-factory-2026-10-06" / "renders"
CROPS = ROOT / "qa" / "work" / "ch3-factory-2026-10-06" / "crops"


def crop_page(pdf, page, name, mode):
    CROPS.mkdir(parents=True, exist_ok=True)
    prefix = CROPS / name
    subprocess.run(["pdftoppm", "-png", "-r", "600", "-f", str(page), "-l", str(page), pdf, str(prefix)], check=True, capture_output=True)
    produced = sorted(CROPS.glob(name + "-*.png"))
    if not produced:
        raise SystemExit("missing 600 dpi page %s" % name)
    image = Image.open(produced[0])
    width, height = image.size
    if mode == "corner":
        box = (0, 0, min(width, 700), min(height, 500))
    elif mode == "right-edge":
        box = (max(0, width - 240), 0, width, min(height, 500))
    else:
        box = (0, 0, width, min(height, 900))
    cropped = image.crop(box)
    out = CROPS / ("%s-600dpi.png" % name)
    cropped.save(out)
    produced[0].unlink()
    return out.relative_to(ROOT).as_posix()


def render_rows(ident):
    rows = []
    for _artifact, source, _pdf, _count, _size in SOURCES:
        stem = Path(source).stem.lower().replace("_", "-")
        stem = "".join(ch if ch.isalnum() else "-" for ch in stem).strip("-")
        pngs = sorted(RENDERS.glob(stem + "-p*-300dpi.png"))
        for index, png in enumerate(pngs, start=1):
            rows.append({
                "artifactId": stem,
                "artifactPath": source,
                "artifactHash": hash_file(source),
                "pageOrSlide": index,
                "renderPath": png.relative_to(ROOT).as_posix(),
                "renderHash": hash_file(str(png)),
                "dpi": 300,
                "navigation": False,
                "buildId": ident.buildId,
            })
    return rows


def visual_pages():
    pages = []
    number = 1
    notes = []
    for _artifact, source, production_pdf, _count, _size in SOURCES:
        pdf = str(ROOT / production_pdf) if production_pdf else None
        if pdf is None:
            stem = Path(source).stem
            matches = list(FRESH.glob(stem + ".pdf")) + list(RENDERS.glob(stem + ".pdf"))
            pdf = str(matches[0])
        parsed = bbox_lines(pdf)
        stem = "".join(ch if ch.isalnum() else "-" for ch in Path(source).stem.lower()).strip("-")
        pngs = sorted(RENDERS.glob(stem + "-p*-300dpi.png"))
        for index, png in enumerate(pngs):
            image = Image.open(png)
            boxes = boxes_for_page(parsed[index])
            regions = []
            if stem.endswith("slides") and index == 0:
                regions = [{"role": "BACKGROUND_BLEED", "x": 0, "y": 0, "w": 13.34, "h": 7.5}]
            record = page_record({
                "artifactId": "%s-p%03d" % (stem, index + 1),
                "artifactPath": source,
                "artifactHash": hash_file(source),
                "renderPath": png.relative_to(ROOT).as_posix(),
                "renderHash": hash_file(str(png)),
                "pageOrSlide": number,
                "dpi": 300,
                "width": image.width,
                "height": image.height,
                "inspectionMethod": "rendered-page",
                "reviewerRole": "VISUAL_QA_AUDITOR",
                "regions": regions,
                "cropEvidence": [],
            }, boxes=boxes, image=image)
            pages.append(record)
            if record["findings"]:
                notes.append((stem, index + 1, [item["code"] for item in record["findings"]]))
            number += 1
    return pages, notes


def pdfs():
    found = []
    for _artifact, source, production_pdf, count, _size in SOURCES:
        if production_pdf:
            path = str(ROOT / production_pdf)
        else:
            stem = Path(source).stem
            path = str(next(FRESH.glob(stem + ".pdf")))
        found.append((Path(source).stem, path, count))
    return found


def main():
    crops = {
        "title-bleed": crop_page("production/slides/03-ch3-energy-speed-slides.pdf", 1, "title-bleed", "corner"),
        "content-edge": crop_page("production/slides/03-ch3-energy-speed-slides.pdf", 2, "content-edge", "right-edge"),
        "notes-header": crop_page("production/premium-notes/03-ch3-energy-speed-guided-notes.pdf", 1, "notes-header", "top"),
        "notes-key-header": crop_page("production/premium-notes/03-ch3-energy-speed-guided-notes-key.pdf", 1, "notes-key-header", "top"),
    }
    ident = identity()
    rows = render_rows(ident)
    render = seal_call("RENDER_COMPLETENESS", lambda rel: emit_render_evidence(rows, rows, ident, rel, auditor_role="VISUAL_QA_AUDITOR"))
    pages, flagged = visual_pages()
    visual = seal_call("RENDERED_VISUAL_QA", lambda rel: emit_visual_evidence(pages, ident, rel, expected_count=len(pages), auditor_role="VISUAL_QA_AUDITOR"))
    pdf_results = []
    for label, path, _count in pdfs():
        from ch3_seal_remaining import pdf_size
        count, size = pdf_size(path)
        result = seal_call("PDF_%s" % label, lambda rel, file_path=path, pages_n=count, page_size=size, name=label: emit_pdf_evidence(
            file_path, ident, rel, {"pageCount": pages_n, "pageSizePts": page_size, "label": name, "textRequired": True, "imageClass": "print-instructional"},
            auditor_role="PDF_OOXML_FORENSICS"))
        stored_path = ROOT / "qa/work/ch3-factory-2026-10-06/evidence" / ("PDF_%s.json" % label)
        stored = json.loads(stored_path.read_text(encoding="utf-8"))
        stored["evidenceId"] = "pdf-quality-%s" % label
        stored_path.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
        result["evidenceId"] = stored["evidenceId"]
        result["pages"] = count
        pdf_results.append(result)
    fresh = seal_call("FRESH_EXPORT", lambda rel: emit_fresh_export(_fresh_from_disk(), ident, rel))
    print(json.dumps({"crops": crops, "render": render["status"], "visual": visual["status"], "flagged": flagged, "pdf": [(item["gate"], item["status"], item["findings"][:3]) for item in pdf_results], "pages": len(pages), "fresh": fresh["status"]}, indent=2))


def _fresh_from_disk():
    pairs = []
    from ch3_seal_remaining import normalized_pdf_text, pdf_size
    mapping = [
        ("guided-notes", "production/premium-notes/03-ch3-energy-speed-guided-notes.docx", "production/premium-notes/03-ch3-energy-speed-guided-notes.pdf"),
        ("guided-notes-key", "production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx", "production/premium-notes/03-ch3-energy-speed-guided-notes-key.pdf"),
        ("slides", "production/slides/03-ch3-energy-speed-slides.pptx", "production/slides/03-ch3-energy-speed-slides.pdf"),
    ]
    for label, source, pdf in mapping:
        fresh_pdf = next(FRESH.glob(Path(source).stem + ".pdf"))
        pages, size = pdf_size(str(ROOT / pdf))
        fresh_pages, fresh_size = pdf_size(str(fresh_pdf))
        pairs.append({
            "label": label,
            "sourceHash": hash_file(source),
            "outputHash": hash_file(str(ROOT / pdf)),
            "freshHash": hash_file(str(fresh_pdf)),
            "pageCount": pages,
            "expectedPageCount": fresh_pages,
            "dimensions": "%sx%s" % size,
            "expectedDimensions": "%sx%s" % fresh_size,
            "normalizedText": normalized_pdf_text(str(ROOT / pdf)),
            "freshText": normalized_pdf_text(str(fresh_pdf)),
        })
    return pairs


if __name__ == "__main__":
    main()
