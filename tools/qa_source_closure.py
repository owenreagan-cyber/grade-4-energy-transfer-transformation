"""Print the static source closure of a builder entrypoint."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chapter_qa.provenance import discover_static


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("entrypoint")
    args = parser.parse_args()
    print(json.dumps(discover_static(Path(args.entrypoint)), indent=2))


if __name__ == "__main__":
    main()
