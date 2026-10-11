#!/usr/bin/env python3
"""Independent multimodal slide inspector (ollama qwen3-vl:30b).

Provides a reusable, deterministic vision-analysis path for rendered slide
images. The vision model inspects each image BLIND (no builder metadata,
no prior QA results, no coordinate expectations) and returns structured JSON.

Usage:
    python3 vision.py --image <png> --prompt-file <prompt> [--out <json>]
    python3 vision.py --image <png> --rubric slides  [--out <json>]
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.request
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3-vl:30b"

# --------------------------------------------------------------------------- #
# Prompt templates
# --------------------------------------------------------------------------- #
SLIDE_RUBRIC = (
    "You are an independent instructional-slide reviewer for a Grade 4 "
    "science presentation (ages 9-10). Inspect the slide image CAREFULLY and "
    "report ONLY what you can actually see. Do not assume anything not visible.\n"
    "Answer these questions:\n"
    "1. TEXT: Is any text clipped, cut off at an edge, overlapping other text, "
    "or overflowing its box? Quote any problematic text.\n"
    "2. READABILITY: Are fonts large enough to read from the back of a "
    "classroom when projected? Note any text that looks too small.\n"
    "3. IMAGES: Are any images distorted, stretched, blurry, pixelated, or "
    "wrongly proportioned? Describe each image you see.\n"
    "4. OVERLAP: Do any elements overlap or collide in a confusing way?\n"
    "5. LABELS: Are any labels, badges, or captions incorrect, missing, or "
    "misplaced?\n"
    "6. HIERARCHY: Is the visual hierarchy clear (title, body, callouts)? Is "
    "alignment consistent?\n"
    "7. SCIENCE: Does anything look scientifically WRONG or misleading for a "
    "Grade 4 energy lesson?\n"
    "8. ANSWER LEAK: Does the slide reveal an answer that a student should "
    "still be predicting or writing on their own?\n"
    "9. COMPOSITION: Is the page visually consistent and well composed?\n"
    "Return STRICT JSON with this exact shape (no prose outside the JSON):\n"
    "{\n"
    "  \"summary\": \"one sentence\",\n"
    "  \"text_issues\": [\"...\"],\n"
    "  \"readability_issues\": [\"...\"],\n"
    "  \"image_issues\": [\"...\"],\n"
    "  \"overlap_issues\": [\"...\"],\n"
    "  \"label_issues\": [\"...\"],\n"
    "  \"hierarchy_issues\": [\"...\"],\n"
    "  \"science_issues\": [\"...\"],\n"
    "  \"answer_leak\": [\"...\"],\n"
    "  \"composition_issues\": [\"...\"],\n"
    "  \"overall\": \"PASS\" | \"WARN\" | \"FAIL\"\n"
    "}"
)

IPAD_RUBRIC = (
    "You are an independent device-QA reviewer. This is a screenshot from a "
    "physical iPad (A16) running a Google Slides presentation. Report ONLY "
    "what you can actually see.\n"
    "1. What app/content is shown? Is a presentation slide visible?\n"
    "2. Is slide text readable and not clipped?\n"
    "3. Are any images distorted, missing, or clipped?\n"
    "4. Are there any unexpected overlays, permission dialogs, or error "
    "messages visible?\n"
    "5. If a video slide is shown, is the video frame proportionate "
    "(landscape video not squished into a portrait box, or vice versa)?\n"
    "Return STRICT JSON: {\"summary\": str, \"content\": str, \"issues\": [str], "
    "\"overall\": \"PASS\"|\"WARN\"|\"FAIL\"}"
)


def analyze(image_path: str, prompt: str, model: str = MODEL,
            timeout: int = 600, format_json: bool = True) -> dict:
    """Send an image + prompt to ollama and return the parsed response."""
    p = Path(image_path)
    data = base64.b64encode(p.read_bytes()).decode("utf-8")
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [data],
        "stream": False,
        "options": {"temperature": 0.0, "think": False},
    }
    # NOTE: ollama's `format: "json"` caused empty responses on qwen3-vl;
    # rely on prompt-requested JSON + robust parsing instead (format_json ignored).
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode("utf-8"))
    text = resp.get("response", "")
    return _parse_json(text)


def _parse_json(text: str) -> dict:
    """Best-effort extract a JSON object from model output."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # strip code fences
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    # find first { ... last }
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    return {"raw": text, "parse_error": True}


def main():
    ap = argparse.ArgumentParser(description="Independent multimodal slide inspector")
    ap.add_argument("--image", required=True)
    ap.add_argument("--prompt-file", help="file containing the prompt")
    ap.add_argument("--rubric", choices=["slides", "ipad"], help="built-in rubric")
    ap.add_argument("--out", help="write JSON to file")
    args = ap.parse_args()

    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    elif args.rubric == "slides":
        prompt = SLIDE_RUBRIC
    elif args.rubric == "ipad":
        prompt = IPAD_RUBRIC
    else:
        prompt = SLIDE_RUBRIC

    result = analyze(args.image, prompt)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
