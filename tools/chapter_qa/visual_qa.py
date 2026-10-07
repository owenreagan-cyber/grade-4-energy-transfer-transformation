"""Rendered visual evidence.

Source XML, extracted text, and contact sheets cannot satisfy this gate.
Every expected page needs a rendered inspection record.
"""

from __future__ import annotations

from pathlib import Path

from chapter_qa.emit import seal
from chapter_qa.evidence import REPO_ROOT
from chapter_qa.severity import resolve_severity

CATEGORIES = {
    "CLIPPING": "DETERMINISTIC",
    "OVERFLOW": "DETERMINISTIC",
    "TEXT_OUTSIDE_SAFE_AREA": "DETERMINISTIC",
    "TEXT_OVERLAP": "DETERMINISTIC",
    "OBJECT_OVERLAP": "DETERMINISTIC",
    "MID_WORD_SPLIT": "DETERMINISTIC",
    "FONT_TOO_SMALL": "DETERMINISTIC",
    "MISSING_GLYPH": "DEFERRED",
    "BROKEN_LINE_WRAP": "BOTH",
    "PAGE_BOUNDARY_ISSUE": "DETERMINISTIC",
    "PRINT_MARGIN_ISSUE": "DETERMINISTIC",
    "WRITING_SPACE_TOO_SMALL": "DETERMINISTIC",
    "BLANK_TOO_SMALL": "DETERMINISTIC",
    "DIAGRAM_UNREADABLE": "MODEL_VISUAL_REVIEW",
    "ANSWER_LEAKAGE_VISUAL": "BOTH",
    "LOW_CONTRAST": "DETERMINISTIC",
    "GRAYSCALE_FAILURE": "BOTH",
    "PROJECTOR_READABILITY": "MODEL_VISUAL_REVIEW",
    "TEACHER_STUDENT_CONFUSION": "MODEL_VISUAL_REVIEW",
    "INCONSISTENT_ALIGNMENT": "MODEL_VISUAL_REVIEW",
}

PROHIBITED_METHODS = {
    "source-xml",
    "docx-text",
    "pptx-text",
    "text-extraction",
    "contact-sheet",
}
RENDER_METHODS = {"rendered-page", "rendered-page+crop"}
SUSPICIOUS = {"CLIPPING", "OVERFLOW", "TEXT_OVERLAP", "OBJECT_OVERLAP", "MID_WORD_SPLIT"}
CODE_FOR = {
    "CLIPPING": "text_clipped",
    "OVERFLOW": "text_clipped",
    "TEXT_OUTSIDE_SAFE_AREA": "text_clipped",
    "PRINT_MARGIN_ISSUE": "text_clipped",
    "PAGE_BOUNDARY_ISSUE": "text_clipped",
    "TEXT_OVERLAP": "text_clipped",
    "OBJECT_OVERLAP": "text_clipped",
    "MID_WORD_SPLIT": "mid_word_split",
    "FONT_TOO_SMALL": "font_too_small",
    "WRITING_SPACE_TOO_SMALL": "writing_space_too_small",
    "BLANK_TOO_SMALL": "blank_too_small",
    "LOW_CONTRAST": "low_contrast",
}


def category_mode(name: str) -> str:
    return CATEGORIES[name]


def _overlap(a: dict, b: dict) -> bool:
    ax2 = a["x"] + a["w"]
    ay2 = a["y"] + a["h"]
    bx2 = b["x"] + b["w"]
    by2 = b["y"] + b["h"]
    return a["x"] < bx2 and b["x"] < ax2 and a["y"] < by2 and b["y"] < ay2


def _contrast_ratio(fg: str, bg: str) -> float:
    def channel(value: str):
        value = value.lstrip("#")
        return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lum(rgb):
        parts = []
        for item in rgb:
            parts.append(item / 12.92 if item <= 0.04045 else ((item + 0.055) / 1.055) ** 2.4)
        return 0.2126 * parts[0] + 0.7152 * parts[1] + 0.0722 * parts[2]

    values = (lum(channel(fg)), lum(channel(bg)))
    lighter, darker = max(values), min(values)
    return (lighter + 0.05) / (darker + 0.05)


def detect_boxes(boxes: list[dict], *, min_font_pt=12, min_writing_in=0.4, min_blank_in=0.4, margin_in=0.5, min_contrast=3.0) -> list[dict]:
    findings = []

    def add(category, message, lost=False):
        decision = resolve_severity(CODE_FOR[category], {"lost_instructional_content": lost})
        findings.append({
            "severity": decision["severity"],
            "code": category,
            "message": message,
            "failsGate": decision["failsGate"],
            "suspicious": category in SUSPICIOUS,
        })

    texts = [box for box in boxes if box.get("kind") == "text"]
    for box in boxes:
        page_w = box.get("pageWidthIn", 8.5)
        page_h = box.get("pageHeightIn", 11)
        if box["x"] < 0 or box["y"] < 0 or box["x"] + box["w"] > page_w or box["y"] + box["h"] > page_h:
            add("CLIPPING", "object extends outside the page", lost=True)
            add("OVERFLOW", "object overflows the page", lost=True)
            add("PAGE_BOUNDARY_ISSUE", "object crosses the page boundary", lost=True)
        if (
            box["x"] < margin_in
            or box["y"] < margin_in
            or box["x"] + box["w"] > page_w - margin_in
            or box["y"] + box["h"] > page_h - margin_in
        ):
            add("TEXT_OUTSIDE_SAFE_AREA", "object is outside the safe area")
            add("PRINT_MARGIN_ISSUE", "object enters the print margin")
        if box.get("kind") == "text" and box.get("fontPt", min_font_pt) < min_font_pt:
            add("FONT_TOO_SMALL", "text is %s pt" % box.get("fontPt"))
        if box.get("kind") == "writing" and box["h"] < min_writing_in:
            add("WRITING_SPACE_TOO_SMALL", "writing area is %s in tall" % box["h"])
        if box.get("kind") == "blank" and box["w"] < min_blank_in:
            add("BLANK_TOO_SMALL", "blank is %s in wide" % box["w"])
        if box.get("fg") and box.get("bg"):
            if _contrast_ratio(box["fg"], box["bg"]) < min_contrast:
                add("LOW_CONTRAST", "contrast is below %s:1" % min_contrast)
    for index, box in enumerate(texts):
        for other in texts[index + 1:]:
            if _overlap(box, other):
                add("TEXT_OVERLAP", "text boxes overlap")
                add("OBJECT_OVERLAP", "objects overlap")
    for first, second in zip(texts, texts[1:]):
        a = first.get("text") or ""
        b = second.get("text") or ""
        same_line = abs(first.get("y", 0) - second.get("y", 0)) < 0.05
        gap = second.get("x", 0) - (first.get("x", 0) + first.get("w", 0))
        hyphenated = a.endswith("-") and b[:1].isalpha()
        broken = (
            same_line
            and gap <= 0.15
            and a.isalpha()
            and b.isalpha()
            and len(a) <= 4
            and not a.endswith("-")
        )
        if hyphenated or broken:
            add("MID_WORD_SPLIT", "word continues from %r into %r" % (a, b))
    return findings


def _crop_exists(crop: dict) -> bool:
    if crop.get("dpi") != 600 or not crop.get("path"):
        return False
    path = Path(str(crop["path"]))
    if path.is_absolute() or ".." in path.parts:
        return False
    return (REPO_ROOT / path).is_file()


def _covers(region: dict, x_px: int, y_px: int, dpi: int) -> bool:
    x0 = region.get("x", 0) * dpi
    y0 = region.get("y", 0) * dpi
    return x0 <= x_px < x0 + region.get("w", 0) * dpi and y0 <= y_px < y0 + region.get("h", 0) * dpi


def _fringe_pixel(x: int, y: int, rgb: tuple, width: int, height: int) -> bool:
    """A near-white pixel on the outer two rows or columns is an export edge, not content."""
    if min(rgb) < 230:
        return False
    return x < 2 or y < 2 or x >= width - 2 or y >= height - 2


def margin_content_ink(image, dpi: int, regions=None, margin_in: float = 0.5) -> bool:
    """True when content ink sits in the margin outside an allowed bleed or decorative region."""
    margin = int(margin_in * dpi)
    if margin <= 0:
        return False
    pixels = image.convert("RGB")
    if pixels.width <= margin * 2 or pixels.height <= margin * 2:
        return True
    allowed = [region for region in (regions or []) if region.get("role") in ("BACKGROUND_BLEED", "DECORATIVE")]
    px = pixels.load()
    width, height = pixels.size

    def dirty(x: int, y: int) -> bool:
        rgb = px[x, y]
        if rgb == (255, 255, 255) or _fringe_pixel(x, y, rgb, width, height):
            return False
        return not any(_covers(region, x, y, dpi) for region in allowed)

    for y in range(margin):
        for x in range(width):
            if dirty(x, y) or dirty(x, height - 1 - y):
                return True
    for y in range(margin, height - margin):
        for x in range(margin):
            if dirty(x, y) or dirty(width - 1 - x, y):
                return True
    return False


def ink_in_margin(image, dpi: int, margin_in: float = 0.5) -> bool:
    margin = int(margin_in * dpi)
    if margin <= 0:
        return False
    if image.width <= margin * 2 or image.height <= margin * 2:
        return True
    pixels = image.convert("RGB")
    bands = [
        pixels.crop((0, 0, pixels.width, margin)),
        pixels.crop((0, pixels.height - margin, pixels.width, pixels.height)),
        pixels.crop((0, 0, margin, pixels.height)),
        pixels.crop((pixels.width - margin, 0, pixels.width, pixels.height)),
    ]
    for band in bands:
        colors = band.getcolors(maxcolors=band.width * band.height) or []
        for _count, rgb in colors:
            if rgb != (255, 255, 255):
                return True
    return False


def _crop_box(image, box, dpi: int):
    x0 = max(0, int(box["x"] * dpi))
    y0 = max(0, int(box["y"] * dpi))
    x1 = min(image.width, int((box["x"] + box["w"]) * dpi))
    y1 = min(image.height, int((box["y"] + box["h"]) * dpi))
    if x1 <= x0 or y1 <= y0:
        return None
    return image.convert("RGB").crop((x0, y0, x1, y1))


def _ink_in_box(image, box, dpi: int) -> int:
    crop = _crop_box(image, box, dpi)
    if crop is None:
        return 0
    colors = crop.getcolors(maxcolors=crop.width * crop.height) or []
    return sum(count for count, rgb in colors if rgb != (255, 255, 255) and min(rgb) < 230)


def _intersection(left: dict, right: dict):
    x0 = max(left["x"], right["x"])
    y0 = max(left["y"], right["y"])
    x1 = min(left["x"] + left["w"], right["x"] + right["w"])
    y1 = min(left["y"] + left["h"], right["y"] + right["h"])
    if x1 <= x0 or y1 <= y0:
        return None
    return {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}


def _ink_extent(image, box, dpi: int):
    crop = _crop_box(image, box, dpi)
    if crop is None:
        return None
    pixels = crop.load()
    xs = []
    ys = []
    for y in range(crop.height):
        for x in range(crop.width):
            rgb = pixels[x, y]
            if rgb != (255, 255, 255) and min(rgb) < 230:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    origin_x = max(0, int(box["x"] * dpi))
    origin_y = max(0, int(box["y"] * dpi))
    x0 = (origin_x + min(xs)) / dpi
    y0 = (origin_y + min(ys)) / dpi
    x1 = (origin_x + max(xs) + 1) / dpi
    y1 = (origin_y + max(ys) + 1) / dpi
    return {"x": x0, "y": y0, "w": max(0.01, x1 - x0), "h": max(0.01, y1 - y0)}


def _confirm_with_pixels(findings, boxes, image, dpi: int) -> list:
    """Drop geometry findings whose glyphs do not actually touch."""
    texts = [box for box in boxes if box.get("kind") == "text"]
    visible_overlap = False
    for index, box in enumerate(texts):
        ink = _ink_extent(image, box, dpi)
        if ink is None:
            continue
        for other in texts[index + 1:]:
            other_ink = _ink_extent(image, other, dpi)
            shared = _intersection(ink, other_ink) if other_ink else None
            if shared and shared["h"] > 0.06 and shared["w"] > 0.06 and _ink_in_box(image, shared, dpi):
                visible_overlap = True
                break
        if visible_overlap:
            break
    ordered = [box for box in boxes if box.get("kind") == "text"]
    hyphen_split = any(
        str(first.get("text") or "").endswith("-") and str(second.get("text") or "")[:1].isalpha()
        for first, second in zip(ordered, ordered[1:])
    )
    kept = []
    for finding in findings:
        if finding["code"] == "MID_WORD_SPLIT" and not hyphen_split:
            continue
        if finding["code"] in ("TEXT_OVERLAP", "OBJECT_OVERLAP") and not visible_overlap:
            continue
        if finding["code"] in ("CLIPPING", "OVERFLOW", "PAGE_BOUNDARY_ISSUE", "TEXT_OUTSIDE_SAFE_AREA", "PRINT_MARGIN_ISSUE"):
            if not margin_content_ink(image, dpi):
                continue
        kept.append(finding)
    return kept


def page_record(spec: dict, boxes=None, image=None) -> dict:
    """Inspect one rendered page. No boxes and no image is not an inspection."""
    method = spec.get("inspectionMethod") or ""
    findings = []
    ran = []
    skipped = [name for name, mode in CATEGORIES.items() if mode == "DEFERRED"]
    if not method or method in PROHIBITED_METHODS:
        findings.append({
            "severity": "BLOCKING",
            "code": "CLIPPING",
            "message": "inspection method %s cannot satisfy rendered visual QA" % (method or "missing"),
            "failsGate": True,
            "suspicious": False,
        })
    elif not boxes and image is None:
        findings.append({
            "severity": "BLOCKING",
            "code": "CLIPPING",
            "message": "detector received no render input",
            "failsGate": True,
            "suspicious": False,
        })
    else:
        if boxes:
            findings.extend(detect_boxes(boxes))
            ran.extend(
                name for name, mode in CATEGORIES.items()
                if mode == "DETERMINISTIC" and name != "LOW_CONTRAST"
            )
            if any(box.get("fg") and box.get("bg") for box in boxes):
                ran.append("LOW_CONTRAST")
            else:
                skipped.append("LOW_CONTRAST")
        if image is not None and boxes:
            findings = _confirm_with_pixels(findings, boxes, image, spec.get("dpi") or 300)
        if image is not None and margin_content_ink(image, spec.get("dpi") or 300, spec.get("regions")):
            decision = resolve_severity("text_clipped")
            findings.append({
                "severity": decision["severity"],
                "code": "TEXT_OUTSIDE_SAFE_AREA",
                "message": "content ink sits in the margin",
                "failsGate": decision["failsGate"],
                "suspicious": True,
            })
            if "TEXT_OUTSIDE_SAFE_AREA" not in ran:
                ran.append("TEXT_OUTSIDE_SAFE_AREA")
    suspicious = [item for item in findings if item.get("suspicious")]
    crops = [crop for crop in (spec.get("cropEvidence") or []) if _crop_exists(crop)]
    if suspicious and not crops:
        findings.append({
            "severity": "HIGH",
            "code": "CLIPPING",
            "message": "suspicious region has no 600 DPI crop",
            "failsGate": True,
            "suspicious": False,
        })
    return {
        "artifactId": spec.get("artifactId"),
        "artifactPath": spec.get("artifactPath"),
        "artifactHash": spec.get("artifactHash"),
        "renderPath": spec.get("renderPath"),
        "renderHash": spec.get("renderHash"),
        "pageOrSlide": spec.get("pageOrSlide"),
        "dpi": spec.get("dpi"),
        "width": spec.get("width"),
        "height": spec.get("height"),
        "inspectionMethod": method,
        "detectorsRun": ran,
        "detectorsSkipped": skipped,
        "findings": findings,
        "cropEvidence": crops,
        "reviewed": bool(spec.get("reviewerRole") == "VISUAL_QA_AUDITOR" and method in RENDER_METHODS and (boxes or image is not None)),
        "reviewerRole": spec.get("reviewerRole"),
    }


def emit_visual_evidence(pages: list[dict], identity, evidence_path: str, *, expected_count: int, auditor_role=None):
    reviewed = [page for page in pages if page.get("reviewed") and page.get("inspectionMethod") in RENDER_METHODS]
    findings = []
    fails = len(reviewed) != expected_count or expected_count <= 0
    for page in pages:
        if page.get("inspectionMethod") in PROHIBITED_METHODS:
            fails = True
        if page.get("reviewerRole") not in (None, "VISUAL_QA_AUDITOR", auditor_role):
            fails = True
        for item in page.get("findings") or []:
            findings.append({
                "severity": item["severity"],
                "code": item["code"],
                "message": "page %s: %s" % (page.get("pageOrSlide"), item["message"]),
            })
            fails = fails or item.get("failsGate", item["severity"] == "BLOCKING")
        deterministic = [name for name, mode in CATEGORIES.items() if mode == "DETERMINISTIC"]
        skipped = set(page.get("detectorsSkipped") or [])
        ran = set(page.get("detectorsRun") or [])
        if page.get("reviewed") and any(name not in ran and name not in skipped for name in deterministic):
            fails = True
    indexes = [page.get("pageOrSlide") for page in reviewed]
    if len(indexes) != len(set(indexes)):
        fails = True
    data = {
        "evidenceId": "rendered-visual-qa",
        "gateId": "RENDERED_VISUAL_QA",
        "auditorRole": auditor_role,
        "performed": bool(pages),
        "expectedInputs": ["page-%s" % number for number in range(1, expected_count + 1)],
        "observedInputs": ["page-%s" % page.get("pageOrSlide") for page in reviewed] if len(reviewed) == expected_count else [],
        "thingBeingCertified": "candidate-visual:%s" % identity.candidateHash,
        "independentEvidenceSource": "rendered-inspection:%s" % (reviewed[0].get("renderHash") if reviewed else "none"),
        "findings": findings,
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": bool(pages) and not fails,
            "detectorException": False,
            "requiredInputsPresent": bool(pages) and expected_count > 0,
            "missingRender": len(reviewed) != expected_count,
            "missingEvidence": not pages,
            "stale": False,
            "gateSpecificFailure": fails,
            "unavailableEvidence": False,
        },
        "inventory": [{
            "name": "renderedPages",
            "expected": expected_count,
            "observed": len(reviewed),
        }],
    }
    if expected_count <= 0:
        data["expectedInputs"] = []
        data["observedInputs"] = []
    return seal(data, identity, producer=True)
