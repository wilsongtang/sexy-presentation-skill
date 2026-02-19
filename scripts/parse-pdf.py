#!/usr/bin/env python3
"""Parse PDF files into Slide Data JSON format.

Usage: python3 parse-pdf.py <input.pdf>
Output: JSON to stdout
"""
import json
import os
import sys


def parse_with_pymupdf(filepath):
    import fitz  # PyMuPDF
    doc = fitz.open(filepath)
    slides = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        slide_data = {
            "purpose": "content",
            "title": lines[0] if lines else f"Slide {page_num + 1}",
            "subtitle": "",
            "content_blocks": [],
            "speaker_notes": "",
            "layout_hints": [],
            "images": [],
            "data": None
        }
        for line in lines[1:]:
            slide_data["content_blocks"].append({
                "type": "text",
                "content": line
            })
        # Check for images
        image_list = page.get_images()
        for img in image_list:
            slide_data["images"].append({
                "description": f"Image on page {page_num + 1}",
                "xref": img[0]
            })
        # First page is likely a title slide
        if page_num == 0:
            slide_data["purpose"] = "title"
            if len(lines) > 1:
                slide_data["subtitle"] = lines[1]
                slide_data["content_blocks"] = [
                    {"type": "text", "content": l} for l in lines[2:]
                ]
        slides.append(slide_data)
    doc.close()
    return {"slides": slides}


def parse_with_pdftotext(filepath):
    import subprocess
    result = subprocess.run(
        ["pdftotext", "-layout", filepath, "-"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {result.stderr}")
    # Split on form feed characters (page breaks)
    pages = result.stdout.split("\f")
    slides = []
    for i, page_text in enumerate(pages):
        lines = [l.strip() for l in page_text.split("\n") if l.strip()]
        if not lines:
            continue
        slide_data = {
            "purpose": "title" if i == 0 else "content",
            "title": lines[0],
            "subtitle": lines[1] if len(lines) > 1 and i == 0 else "",
            "content_blocks": [
                {"type": "text", "content": l}
                for l in (lines[2:] if i == 0 else lines[1:])
            ],
            "speaker_notes": "",
            "layout_hints": [],
            "images": [],
            "data": None
        }
        slides.append(slide_data)
    return {"slides": slides}


def main():
    if len(sys.argv) != 2:
        print("Usage: parse-pdf.py <input.pdf>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    try:
        data = parse_with_pymupdf(filepath)
    except Exception as e:
        print(f"PyMuPDF failed ({e}), trying pdftotext...", file=sys.stderr)
        try:
            data = parse_with_pdftotext(filepath)
        except Exception as e2:
            print(f"All parsers failed: {e2}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
