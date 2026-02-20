#!/usr/bin/env python3
"""Regenerate index.json from template HTML metadata comments."""
import re
import json
from pathlib import Path

TEMPLATE_DIR = Path("templates")
CATEGORIES = [
    "title", "content", "data", "image", "comparison",
    "timeline", "quote", "team", "structural", "closing"
]


def parse_template(filepath):
    """Parse template metadata from HTML comments."""
    html = filepath.read_text()
    entry = {}

    m = re.search(r'<!-- Template: (\S+) -->', html)
    if m:
        entry["id"] = m.group(1)

    m = re.search(r'<!-- Slots: (.+?) -->', html)
    if m:
        slots = [s.strip() for s in m.group(1).split(",")]
        entry["slots"] = {s: True for s in slots}

    m = re.search(r'<!-- Composition: (.+?) \| Intensity: (\w+) -->', html)
    if m:
        entry["composition"] = m.group(1).strip()
        entry["intensity"] = m.group(2).strip()

    # Parse category, layout, treatment from filename
    parts = filepath.stem.rsplit("-", 1)
    treatment = parts[1] if len(parts) > 1 else "light"
    layout = parts[0]
    category = filepath.parent.name

    entry["category"] = category
    entry["layout"] = layout
    entry["treatment"] = treatment
    entry["file"] = f"{category}/{filepath.name}"
    entry["description"] = f"{layout.replace('-', ' ').title()} ({treatment}) — {entry.get('composition', 'unknown')} composition"

    # Tags from composition and intensity
    tags = []
    if entry.get("intensity"):
        tags.append(entry["intensity"])
    if entry.get("composition"):
        tags.append(entry["composition"].lower().replace(" ", "-"))
    tags.append(treatment)
    entry["tags"] = tags

    return entry


def main():
    templates = []
    for category in CATEGORIES:
        cat_dir = TEMPLATE_DIR / category
        if not cat_dir.exists():
            continue
        for f in sorted(cat_dir.glob("*.html")):
            entry = parse_template(f)
            if entry.get("id"):
                templates.append(entry)

    registry = {
        "$schema": "./schema.json",
        "version": "0.2.0",
        "templates": templates
    }

    output = TEMPLATE_DIR / "index.json"
    with open(output, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"Registry updated: {len(templates)} templates")


if __name__ == "__main__":
    main()
