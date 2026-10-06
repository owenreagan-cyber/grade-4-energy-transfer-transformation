"""Semantic Chapter 2 guards. Negative tests call these with planted inputs.

A rebuilt release must not turn a planted content error into a pass.
"""
import os, re

REQUIRED_RELEASE = [
    "02-ch2-moving-objects-have-energy-guided-notes.pdf",
    "02-ch2-moving-objects-have-energy-guided-notes-key.pdf",
    "02-ch2-moving-objects-have-energy-slides.pptx",
    "02-ch2-moving-objects-have-energy-slides.pdf",
    "02-ch2-moving-objects-have-energy-quiz.pdf",
    "02-ch2-moving-objects-have-energy-practice.pdf",
    "02-ch2-moving-objects-have-energy-teacher-key.pdf",
    "02-ch2-friday-flex.pdf",
    "02-ch2-absent-student-recovery.pdf",
    "02-ch2-moving-marbles-student.pdf",
]

# Strings that must match in notes and on the slide that teaches that anchor.
SYNC_PAIRS = [
    ("motion — the process of an object changing", "motion — the process of an object changing"),
    ("Players cause their own motion. A ball does not.", "Players cause their own motion. A ball does not."),
    ("energy of motion — the energy an object possesses while it is",
     "energy of motion — the energy an object possesses while it is"),
    ("All moving objects have energy of", "All moving objects have energy of"),
    ("How do we know a moving object has energy?", "How do we know a moving object has energy?"),
    ("How are energy, change, and movement of objects related?",
     "How are energy, change, and movement of objects related?"),
]

def sync_ok(notes_blob, slides_blob):
    missing = []
    for note_s, slide_s in SYNC_PAIRS:
        if note_s not in notes_blob or slide_s not in slides_blob:
            missing.append(note_s[:40])
    return missing

def leak_outside(faces_before_reveal):
    """faces_before_reveal: list of student-visible strings from slides 1..12."""
    return [i + 1 for i, face in enumerate(faces_before_reveal) if re.search(r"\boutside\b", face, re.I)]

def vocab_order_ok(notes_blob, slide_faces):
    """V1 motion appears before V2 energy of motion in notes and in the deck."""
    n1, n2 = notes_blob.find("V1"), notes_blob.find("V2")
    if n1 < 0 or n2 < 0 or n1 > n2:
        return False
    v1 = next((i for i, f in enumerate(slide_faces) if "Vocabulary — Motion" in f or "VOCABULARY — MOTION" in f), None)
    v2 = next((i for i, f in enumerate(slide_faces) if "Energy of Motion" in f), None)
    return v1 is not None and v2 is not None and v1 < v2

def pacing_ok(required_minutes):
    return all(m <= 25.0 for m in required_minutes)

def speaker_time_ok(note_text, expected_min):
    m = re.search(r"TIME\s+([0-9.]+)\s+min", note_text)
    if not m:
        return False
    return abs(float(m.group(1)) - expected_min) < 0.01

def required_marked_optional(plan_line):
    return "OPTIONAL" in plan_line and "REQUIRED" not in plan_line

def retired_in_release(names):
    return [n for n in names if re.search(r"interactive-science-notebook|interactive-notebook", n, re.I)]

def manifest_p3_ok(manifest_text, exists):
    """Chapter 2 P3 master path must exist. exists(path) -> bool."""
    chunk = manifest_text.split("## Chapter 2")[-1].split("## Chapter 3")[0]
    m = re.search(r"\|\s*P3\s*\|[^|]*\|\s*`([^`]+)`", chunk)
    if not m:
        return False
    path = m.group(1).split("+")[0].strip().strip("`")
    if "student-notes/02-ch2" in path:
        return False
    return exists(path)

def friday_core(text):
    """True when Chapter 2 core is placed on Friday. Allows 'not Friday' and 'Friday is Chapter 1'."""
    bad = []
    for line in text.splitlines():
        low = line.lower()
        if "friday" not in low and "fri " not in low and "fri\t" not in low:
            continue
        if re.search(r"not [^.\n]{0,40}friday|friday[^.\n]{0,40}chapter 1|is chapter 1", low):
            continue
        if re.search(r"ch2|chapter 2|moving objects have energy", low) and re.search(
                r"session|core|teach|slides|quiz|first", low):
            # "after the quiz, not Friday" already skipped. A teaching row remains.
            if "optional after" in low:
                continue
            bad.append(line.strip()[:120])
    return bad

def playbook_days_ok(text):
    return ("Wed 10/14" in text and "Thu 10/15" in text
            and "Ch2 Session 1" in text and "Ch2 Session 2" in text
            and "Ch2 Block 1" not in text)

def release_inventory_ok(names):
    missing = [n for n in REQUIRED_RELEASE if n not in names]
    retired = retired_in_release(names)
    return missing, retired
