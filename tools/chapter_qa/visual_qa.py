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
        hyphenated = a.endswith("-") and b[:1].isalpha()
        broken = (
            same_line
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
        if image is not None and ink_in_margin(image, spec.get("dpi") or 300):
            decision = resolve_severity("text_clipped")
            findings.append({
                "severity": decision["severity"],
                "code": "TEXT_OUTSIDE_SAFE_AREA",
                "message": "non-white pixels sit in the margin",
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
