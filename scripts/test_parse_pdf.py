"""Tests for PDF parser."""
import json
import subprocess


def test_parse_pdf_handles_missing_file():
    result = subprocess.run(
        ["python3", "scripts/parse-pdf.py", "nonexistent.pdf"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
