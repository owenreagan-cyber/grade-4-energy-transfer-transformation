#!/usr/bin/env python3
import sys
from pathlib import Path

def audit_pdf(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError:
        print("Missing pypdf. Run: pip install pypdf")
        sys.exit(1)

    try:
        reader = PdfReader(str(path))
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return

    total_pages = len(reader.pages)
    total_chars = 0
    empty_pages = []

    print(f"\n========================================")
    print(f"  PDF AUDIT: {path.name}")
    print(f"========================================")
    print(f"File Size        : {path.stat().st_size / 1024:.1f} KB")
    print(f"Total Pages      : {total_pages}")

    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        chars = len(text.strip())
        total_chars += chars
        if chars == 0:
            empty_pages.append(idx + 1)

    print(f"Total Characters : {total_chars}")
    print(f"Avg Chars / Page : {total_chars // total_pages if total_pages else 0}")

    if empty_pages:
        print(f"⚠️  WARNING: Blank or rasterized pages without text: {empty_pages}")
    else:
        print("✓ Accessible text layer confirmed on all pages.")

    if reader.metadata:
        producer = reader.metadata.get("/Producer", "Unknown")
        creator = reader.metadata.get("/Creator", "Unknown")
        print(f"Engine / Producer: {producer} | {creator}")
    print("========================================\n")

def audit_image(path: Path):
    try:
        from PIL import Image
    except ImportError:
        print("Missing pillow. Run: pip install pillow")
        sys.exit(1)

    try:
        with Image.open(path) as img:
            print(f"\n========================================")
            print(f"  IMAGE AUDIT: {path.name}")
            print(f"========================================")
            print(f"Dimensions       : {img.width} × {img.height} px")
            print(f"Aspect Ratio     : {img.width / img.height:.2f}")
            print(f"Format / Mode    : {img.format} / {img.mode}")
            print(f"File Size        : {path.stat().st_size / 1024:.1f} KB")
            print("========================================\n")
    except Exception as e:
        print(f"Error reading image: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_doc.py <path-to-file>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"File not found: {target}")
        sys.exit(1)

    suffix = target.suffix.lower()
    if suffix == ".pdf":
        audit_pdf(target)
    elif suffix in [".png", ".jpg", ".jpeg", ".webp", ".svg"]:
        audit_image(target)
    else:
        print(f"Unsupported extension: {suffix}. Supported: .pdf, .png, .jpg, .jpeg, .webp")

if __name__ == "__main__":
    main()
