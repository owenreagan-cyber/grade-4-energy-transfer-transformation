"""Run a chapter's pre-freeze certification gates.

Usage: .venv/bin/python tools/certify_chapter.py --chapter 2
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

CH2 = [
    [PY, "qa_ch2_semantic.py"],
    [PY, "qa_ch2_golden.py", "--mode", "pre-freeze"],
    [PY, "qa_ch2_schedule.py"],
    [PY, "qa_ch2_slides.py"],
    [PY, "qa_ch2_guided_notes.py"],
    [PY, "qa_teacher_playbook.py"],
    [PY, "qa_ch2_fresh_export.py"],
    [PY, "qa_ch2_retired_image.py"],
    [PY, "qa_release_parity.py", "--chapter", "2"],
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    a = ap.parse_args()
    if a.chapter != 2:
        sys.exit("certify_chapter: chapter %s is not wired yet" % a.chapter)
    for cmd in CH2:
        cmd[1] = os.path.join(HERE, cmd[1])
        print("RUN", os.path.basename(cmd[1]))
        if subprocess.call(cmd) != 0:
            sys.exit("certification failed at " + os.path.basename(cmd[1]))
    print("[PASS] chapter 2 certification gates")


if __name__ == "__main__":
    main()
