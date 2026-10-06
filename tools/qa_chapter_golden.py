"""Generic entry point. Chapter 2 is the first implementation.

Usage: .venv/bin/python tools/qa_chapter_golden.py --chapter 2 [--mode pre-freeze]
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--mode", default="pre-freeze")
    ap.add_argument("--root", default=None)
    a = ap.parse_args()
    if a.chapter != 2:
        sys.exit("chapter %s golden baseline is not implemented yet; Chapter 2 is the reference" % a.chapter)
    cmd = [sys.executable, os.path.join(HERE, "qa_ch2_golden.py"), "--mode", a.mode]
    if a.root:
        cmd.extend(["--root", a.root])
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
