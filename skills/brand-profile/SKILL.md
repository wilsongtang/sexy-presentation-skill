---
name: Brand Profile
description: Extract brand guidelines from a PDF brand book, a URL, or a natural language description. Output a validated brand-profile.json that overrides theme defaults and ensures on-brand presentation output.
version: 0.1.0
---

# Brand Profile Skill

## Purpose

Parse brand guidelines from whatever the user provides and produce a standardized `brand-profile.json` file that downstream skills (`select-theme`, `design-slide`, `playground`) can consume to enforce brand consistency throughout the presentation.

## Input Sources

### Source 1: PDF Brand Book

Use PyMuPDF to extract text and color swatches from a brand guidelines PDF:

```python
import fitz
import re

doc = fitz.open("brand-guidelines.pdf")
for page in doc:
    # Extract text
    text = page.get_text("text")

    # Extract color annotations / drawings for swatch detection
    drawings = page.get_drawings()
    for d in drawings:
        if d.get("fill"):
            print(d["fill"])  # RGB tuple

    # Extract images (logos)
    for img in page.get_images(full=True):
        xref = img[0]
        base_image = doc.extract_image(xref)
        print(base_image["ext"], len(base_image["image"]))
```

Look for sections with headings like: "Colors", "Typography", "Logo", "Voice and Tone", "Spacing", "Do's and Don'ts".

Use regex patterns to extract hex codes:
```python
hex_pattern = re.compile(r'#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b')
rgb_pattern = re.compile(r'RGB[:\s]+(\d{1,3})[,\s]+(\d{1,3})[,\s]+(\d{1,3})')
pantone_pattern = re.compile(r'Pantone[®\s]+(\d+\s*[A-Z]*)')
```

### Source 2: URL

Fetch the page at the provided URL and extract brand signals:

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

# Extract CSS custom properties from stylesheets
# Extract meta theme-color
meta_color = soup.find("meta", {"name": "theme-color"})

# Extract dominant colors from images using Pillow
# Extract font-family from computed styles
```

Also attempt to fetch a linked brand or press kit page (look for links containing "brand", "press", "media-kit", "guidelines").

### Source 3: Natural Language Description

When the user describes their brand verbally:

- "Our primary color is #FF6B35 and our secondary is #1A1A2E"
- "We use Helvetica Neue for headings and Georgia for body text"
- "Our logo is a simple wordmark in white on dark backgrounds"

Parse these descriptions directly into the brand profile fields.

Ask follow-up questions for any missing required fields:
- "What is your primary brand color (hex or Pantone)?"
- "Do you have a secondary or accent color?"
- "What fonts does your brand use for headings and body text?"
- "Do you have a logo file I can reference?"
- "Are there any colors or styles that should never be used?"

## Extraction Targets

| Signal | Where to look | Output field |
|---|---|---|
| Primary color | Color swatch, first named color | `primary_color` |
| Secondary color | Second named color swatch | `secondary_color` |
| Accent / CTA color | Button color, highlight color | `accent_color` |
| Background color | Recommended background swatches | `background_color` |
| Text color | Body text swatch | `text_color` |
| Heading font | Typography section | `heading_font` |
| Body font | Body/paragraph typography | `body_font` |
| Logo URL / base64 | Logo section, embedded image | `logo_url` |
| Logo safe area | Clearspace specification | `logo_safe_area_px` |
| Brand voice | Voice/tone section | `voice_keywords` |
| Forbidden colors | Don't use / off-brand colors | `forbidden_colors` |
| Forbidden fonts | Don't use fonts | `forbidden_fonts` |
| Min font size | Accessibility / legibility rules | `min_font_size_px` |

## Brand-Profile JSON Schema

```json
{
  "$schema": "https://sexy-presentation.dev/schemas/brand-profile.json",
  "brand_name": "Acme Corp",
  "extracted_from": "pdf | url | natural_language",
  "source_ref": "brand-guidelines-v3.pdf",
  "extracted_at": "ISO8601 timestamp",
  "confidence": "high | medium | low",
  "confidence_notes": "Primary colors extracted with high confidence. Fonts inferred from PDF text rendering.",

  "colors": {
    "primary": "#FF6B35",
    "secondary": "#1A1A2E",
    "accent": "#FFD166",
    "background_light": "#FAFAFA",
    "background_dark": "#0D0D1A",
    "text_primary": "#1A1A1A",
    "text_inverse": "#FFFFFF",
    "forbidden": ["#FF0000", "#00FF00"]
  },

  "typography": {
    "heading_font": "Helvetica Neue, Arial, sans-serif",
    "body_font": "Georgia, 'Times New Roman', serif",
    "mono_font": null,
    "heading_weight": "700",
    "body_weight": "400",
    "min_font_size_px": 14,
    "forbidden_fonts": ["Comic Sans MS", "Papyrus"]
  },

  "logo": {
    "primary_url": "https://cdn.acme.com/logo-primary.svg",
    "inverse_url": "https://cdn.acme.com/logo-inverse.svg",
    "safe_area_px": 16,
    "preferred_placement": "top-left | top-right | bottom-left | bottom-right"
  },

  "voice": {
    "keywords": ["professional", "innovative", "clear", "confident"],
    "avoid_words": ["synergy", "leverage", "disruptive"],
    "formality": "formal | semi-formal | casual"
  },

  "presentation_rules": {
    "always_show_logo": true,
    "logo_on_every_slide": false,
    "logo_on_slides": ["title", "closing", "section_break"],
    "slide_number_style": "bottom-right | bottom-center | none",
    "footer_text": "Confidential — Acme Corp 2025"
  }
}
```

## Validation

After generating the JSON, validate against the schema:

1. Verify all color values are valid hex codes (`#RRGGBB` format)
2. Verify font names are web-safe or available on Google Fonts
3. Verify logo URLs are accessible (HTTP 200) or are valid base64 data URIs
4. Check that `forbidden_colors` do not conflict with `colors.primary` or `colors.accent`
5. Warn if `confidence` is `low` for any critical field (primary color, heading font)

## How Brand Overrides Theme

When `brand-profile.json` is passed to `select-theme` or `design-slide`, brand values override the corresponding theme CSS variables:

| `brand-profile.json` field | CSS variable overridden |
|---|---|
| `colors.primary` | `--color-primary` |
| `colors.accent` | `--color-accent` |
| `colors.background_dark` or `background_light` | `--color-background` |
| `colors.text_primary` | `--color-text` |
| `typography.heading_font` | `--font-heading` |
| `typography.body_font` | `--font-body` |
| `logo.primary_url` | `--logo-url` |

Theme values not covered by the brand profile remain unchanged.

## Memory Integration

### Write to Brand Memory
Save the generated profile to `memory/brand/<brand-name-slug>.json`. This persists across sessions and projects.

### Write to Project Memory
Record which brand profile is active for the current project so the orchestrator auto-loads it in future sessions.

### Multiple Brands
Users can maintain multiple brand profiles. When starting a new project:
1. If the user specifies a brand, load that profile
2. If only one brand exists, use it automatically
3. If multiple brands exist and none specified, ask the user to choose

### Updating Profiles
When the user says "update brand" or provides new guidelines:
1. Load the existing profile from Brand Memory
2. Show current values for the fields being updated
3. Merge changes (don't replace the entire profile)
4. Save updated profile back to Brand Memory

## Output

Save `brand-profile.json` to the working directory and to `memory/brand/<brand-name-slug>.json`. Return its contents to the calling skill. Inform the user of the confidence level and any fields that could not be extracted, offering to accept manual input for missing values.
