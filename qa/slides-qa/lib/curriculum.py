#!/usr/bin/env python3
"""Curriculum + Guided Notes parity audit for a deck's extracted text.

Compares deck text against the accepted Chapter 1 baseline
(qa/slides-qa/ch1/expected_ch1.json, derived from the canonical Guided Notes
handoff + slideshow manifest). Deterministic, text-based; no builder metadata
or prior QA results are consulted.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


def load_expected(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower().strip()


def check_structure(expected: dict, slides: list[dict]) -> list[dict]:
    """Slide-count + video-slide structural checks."""
    findings = []
    exp = expected["expected"]
    total = len(slides)
    video = [s for s in slides if s.get("has_video_shape") or s.get("video_hint")]
    findings.append({
        "check": "slide_count",
        "expected": exp["totalSlides"],
        "actual": total,
        "status": "PASS" if total == exp["totalSlides"] else "FAIL",
    })
    findings.append({
        "check": "video_slide_count",
        "expected": exp["videoSlides"],
        "actual": len(video),
        "status": "PASS" if len(video) == exp["videoSlides"] else "FAIL",
        "detail": [s["index"] for s in video],
    })
    return findings


def check_big_question(expected: dict, slides: list[dict]) -> list[dict]:
    bq = _norm(expected["bigQuestion"])
    found = any(bq in _norm(s["text"]) for s in slides)
    return [{
        "check": "big_question_exact",
        "expected": expected["bigQuestion"],
        "actual": "present" if found else "MISSING",
        "status": "PASS" if found else "FAIL",
    }]


def check_vocabulary(expected: dict, slides: list[dict]) -> list[dict]:
    findings = []
    all_text = _norm(" ".join(s["text"] for s in slides))
    for group in expected["vocabulary"]:
        for term in group["terms"]:
            t = _norm(term["term"])
            d = _norm(term["definition"])
            findings.append({
                "check": f"vocab_term_{term['term']}",
                "expected": term["term"],
                "actual": "present" if t in all_text else "MISSING",
                "status": "PASS" if t in all_text else "FAIL",
            })
            # definition is paraphrase-tolerant: check key words
            key = _norm(term["definition"]).split()[0:3]
            def_ok = all(w in all_text for w in key)
            findings.append({
                "check": f"vocab_def_{term['term']}",
                "expected": term["definition"],
                "actual": "present" if def_ok else "MISSING/DIFFERS",
                "status": "PASS" if def_ok else "FAIL",
            })
    return findings


def check_banned(expected: dict, slides: list[dict]) -> list[dict]:
    findings = []
    for s in slides:
        low = _norm(s["text"])
        for word in expected["bannedVocabulary"]:
            if _norm(word) in low:
                findings.append({
                    "check": f"banned_{word}",
                    "expected": "absent",
                    "actual": f"present on slide {s['index']}",
                    "status": "FAIL",
                    "slide": s["index"],
                })
    # forbidden word "proof" must not appear in slide-visible text
    for s in slides:
        if re.search(r"\bproof\b", s["text"], flags=re.I):
            findings.append({
                "check": "forbidden_proof",
                "expected": "absent (use 'evidence')",
                "actual": f"present on slide {s['index']}",
                "status": "FAIL",
                "slide": s["index"],
            })
    if not any(f["check"].startswith("banned_") for f in findings):
        findings.append({"check": "banned_vocabulary", "expected": "absent",
                         "actual": "absent", "status": "PASS"})
    if not any(f["check"] == "forbidden_proof" for f in findings):
        findings.append({"check": "forbidden_proof", "expected": "absent",
                         "actual": "absent", "status": "PASS"})
    return findings


def check_notes_models(expected: dict, slides: list[dict]) -> list[dict]:
    """Verify the N1/N3 model chains and fill answers are present."""
    findings = []
    all_text = _norm(" ".join(s["text"] for s in slides))
    for n in expected["notes"]:
        if "model" in n:
            chain = " -> ".join(n["model"])
            # model chains may be split across text nodes; check term adjacency loosely
            terms = [_norm(t) for t in n["model"]]
            present = all(t in all_text for t in terms)
            findings.append({
                "check": f"model_{n['id']}",
                "expected": chain,
                "actual": "present" if present else "MISSING",
                "status": "PASS" if present else "FAIL",
            })
        if "blank" in n:
            b = _norm(n["blank"])
            findings.append({
                "check": f"blank_answer_{n['id']}",
                "expected": n["blank"],
                "actual": "present" if b in all_text else "MISSING",
                "status": "PASS" if b in all_text else "FAIL",
            })
    # N2 five forms
    for form in expected["notes"][1]["forms"]:
        f = _norm(form)
        findings.append({
            "check": f"form_{form}",
            "expected": form,
            "actual": "present" if f in all_text else "MISSING",
            "status": "PASS" if f in all_text else "FAIL",
        })
    return findings


def check_review(expected: dict, slides: list[dict]) -> list[dict]:
    letters = "".join(expected["reviewAnswers"]["correctLetters"])
    # find review slides (34-45 range) and confirm answer letters appear
    review_text = _norm(" ".join(
        s["text"] for s in slides if 34 <= s["index"] <= 45
    ))
    missing = [c for c in set(expected["reviewAnswers"]["correctLetters"])
               if _norm(c) not in review_text]
    return [{
        "check": "review_answer_letters",
        "expected": letters,
        "actual": "present" if not missing else f"missing {missing}",
        "status": "PASS" if not missing else "WARN",
    }]


def run(expected_path: str, slides: list[dict]) -> dict:
    exp = load_expected(expected_path)
    checks = []
    checks += check_structure(exp, slides)
    checks += check_big_question(exp, slides)
    checks += check_vocabulary(exp, slides)
    checks += check_banned(exp, slides)
    checks += check_notes_models(exp, slides)
    checks += check_review(exp, slides)
    return {"checks": checks,
            "summary": {
                "pass": sum(1 for c in checks if c["status"] == "PASS"),
                "fail": sum(1 for c in checks if c["status"] == "FAIL"),
                "warn": sum(1 for c in checks if c["status"] == "WARN"),
                "total": len(checks),
            }}


def main():
    import argparse
    from structural import load_pptx, load_txt
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected", required=True)
    ap.add_argument("--pptx")
    ap.add_argument("--txt")
    args = ap.parse_args()
    if args.pptx:
        slides = load_pptx(args.pptx)
    elif args.txt:
        slides = load_txt(args.txt)
    else:
        raise SystemExit("provide --pptx or --txt")
    print(json.dumps(run(args.expected, slides), indent=2))


if __name__ == "__main__":
    main()
