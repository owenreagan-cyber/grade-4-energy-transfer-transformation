#!/usr/bin/env python3
"""Decode a Drive MCP `export_file` JSON result (as saved to an agent-tools
file) into the target binary. Avoids re-reading the large base64 into context.
"""
import base64
import json
import sys

src = sys.argv[1]
dst = sys.argv[2]
with open(src, "r", encoding="utf-8") as fh:
    payload = json.load(fh)
b64 = payload.get("base64", "")
if not b64:
    sys.exit("no base64 field in %s" % src)
with open(dst, "wb") as out:
    out.write(base64.b64decode(b64))
print("wrote", dst, len(b64), "b64 chars ->", end=" ")
print(__import__("os").path.getsize(dst), "bytes")
