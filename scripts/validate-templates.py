#!/usr/bin/env python3
"""Validate all HTML templates against v2 design system requirements."""
import os
import re
import sys
import json
from pathlib import Path

TEMPLATE_DIR = Path("templates")
CATEGORIES = [
    "title", "content", "data", "image", "comparison",
    "timeline", "quote", "team", "structural", "closing"
]

# Typography tokens that are restricted by intensity
HERO_ONLY_TOKENS = ["--size-display"]
HERO_IMPACT_TOKENS = ["--size-stat"]


def parse_metadata(html):
    """Extract template metadata from HTML comments."""
    meta = {}
    m = re.search(r'<!-- Template: (\S+) -->', html)
    if m:
        meta["id"] = m.group(1)
    m = re.search(r'<!-- Slots: (.+?) -->', html)
    if m:
        meta["slots"] = [s.strip() for s in m.group(1).split(",")]
    m = re.search(r'<!-- Composition: (.+?) \| Intensity: (\w+) -->', html)
    if m:
        meta["composition"] = m.group(1).strip()
        meta["intensity"] = m.group(2).strip()
    return meta


def validate_template(filepath):
    """Validate a single template file. Returns list of issues."""
    issues = []
    html = filepath.read_text()
    meta = parse_metadata(html)

    # 1. Metadata completeness
    if "id" not in meta:
        issues.append("MISSING: Template ID comment")
    if "slots" not in meta:
        issues.append("MISSING: Slots comment")
    if "composition" not in meta:
        issues.append("MISSING: Composition/Intensity comment")

    # 2. All declared slots must appear as {{slot_name}} in HTML
    if "slots" in meta:
        for slot in meta["slots"]:
            if "{{" + slot + "}}" not in html:
                issues.append(f"SLOT_MISSING: '{slot}' declared but not found in HTML")

    # 3. No hardcoded hex colors (allow #fff, white, black, rgba, transparent)
    hex_colors = re.findall(r'(?<!var\()#[0-9a-fA-F]{3,8}\b', html)
    allowed_hex = {"#fff", "#ffffff", "#000", "#000000"}
    for hc in hex_colors:
        if hc.lower() not in allowed_hex:
            issues.append(f"HARDCODED_COLOR: {hc} — use CSS variable instead")

    # 4. Motif elements present (at least one for light templates)
    if "motif-element" not in html:
        issues.append("NO_MOTIF: Template has no motif-element DOM nodes")

    # 5. Typography token restrictions
    intensity = meta.get("intensity", "workhorse")
    if intensity != "hero":
        for token in HERO_ONLY_TOKENS:
            if token in html:
                issues.append(f"TYPOGRAPHY: {token} used but intensity is '{intensity}' (hero only)")
    if intensity == "workhorse":
        for token in HERO_IMPACT_TOKENS:
            if token in html:
                issues.append(f"TYPOGRAPHY: {token} used but intensity is 'workhorse' (hero/impact only)")

    # 6. Image treatment wrapper check
    if "<img" in html and "img-treatment" not in html:
        # Exception: images that are decorative placeholders (SVG icons)
        if "{{image" in html or 'src="{{' in html:
            issues.append("IMG_NO_TREATMENT: <img> with slot but no .img-treatment wrapper")

    # 7. Slide root element present
    if 'class="slide' not in html:
        issues.append("NO_SLIDE_ROOT: Missing .slide root element")

    # 8. Overflow hidden for edge-tension motifs
    if "motif-element" in html and "overflow: hidden" not in html and "overflow:hidden" not in html:
        issues.append("WARN: Motif elements present but no overflow:hidden on slide (may clip unexpectedly)")

    return issues


def main():
    total_issues = 0
    total_files = 0
    category_filter = sys.argv[1] if len(sys.argv) > 1 else None

    for category in CATEGORIES:
        if category_filter and category != category_filter:
            continue
        cat_dir = TEMPLATE_DIR / category
        if not cat_dir.exists():
            print(f"WARNING: {cat_dir} not found")
            continue

        light_files = sorted(cat_dir.glob("*-light.html"))
        for f in light_files:
            issues = validate_template(f)
            total_files += 1
            if issues:
                total_issues += len(issues)
                print(f"\n{f.relative_to('.')}:")
                for issue in issues:
                    print(f"  - {issue}")

    print(f"\n{'='*60}")
    print(f"Validated {total_files} light templates")
    print(f"Issues found: {total_issues}")
    if total_issues == 0:
        print("ALL TEMPLATES PASS v2 VALIDATION")
    sys.exit(1 if total_issues > 0 else 0)


if __name__ == "__main__":
    main()
