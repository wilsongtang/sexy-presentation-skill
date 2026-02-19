---
name: Analyze Input
description: Parse and extract structured slide content from PPTX, PDF, markdown, or natural language input. Outputs a normalized Slide Data JSON ready for downstream slide planning and design.
version: 0.1.0
---

# Analyze Input Skill

## Purpose

Convert any user-supplied input — file, URL, or plain text — into a normalized **Slide Data JSON** object that downstream skills (plan-slides, design-slide, etc.) can consume reliably.

## Supported Input Types

### 1. PPTX Files

Primary parser: **python-pptx**

```python
from pptx import Presentation

prs = Presentation("input.pptx")
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                print(para.text)
```

Fallback parser: **markitdown**

Use markitdown when python-pptx fails (encrypted files, corrupted XML, unusual OOXML extensions):

```bash
markitdown input.pptx > output.md
```

Then parse the resulting markdown as described below.

Extract from PPTX:
- Slide title and body text (preserving heading hierarchy)
- Speaker notes
- Image alt text and embedded image blobs
- Table data as 2D arrays
- Chart data series labels and values
- Slide layout name (for template hint)

### 2. PDF Files

Primary parser: **PyMuPDF (fitz)**

```python
import fitz

doc = fitz.open("input.pdf")
for page_num, page in enumerate(doc):
    text = page.get_text("dict")  # structured blocks
    images = page.get_images(full=True)
```

Fallback parser: **pdftotext**

```bash
pdftotext -layout input.pdf output.txt
```

Extract from PDF:
- Page-by-page text blocks with font size hints (large = heading)
- Embedded images (extract as base64 for downstream use)
- Table regions (heuristic: aligned columns of short text)

### 3. Markdown

Parse markdown directly using heading structure to infer slide boundaries:

- `# Heading` → new slide, title
- `## Subheading` → slide subtitle or section break
- Bullet lists → body content
- `---` or `***` → explicit slide break
- Fenced code blocks → code slide content
- `![alt](url)` → image slot with alt text as art direction brief

### 4. Natural Language

When the user provides a topic, outline, or description in plain text:

1. Identify the presentation topic and apparent goal (inform, persuade, pitch, train).
2. Infer a logical slide structure (title, agenda, content slides, conclusion, CTA).
3. Extract any explicit content the user mentioned (facts, names, data points).
4. Flag slots that require the user to supply real data vs. placeholder content.

Ask clarifying questions if the input is too sparse:
- "How many slides are you targeting?"
- "Who is the audience?"
- "Do you have any data or statistics to include?"

## Output Format: Slide Data JSON

```json
{
  "meta": {
    "title": "Presentation Title",
    "author": "Author Name or null",
    "source_type": "pptx | pdf | markdown | natural_language",
    "slide_count": 12,
    "aspect_ratio": "16:9 | 4:3 | A4",
    "notes": "Any top-level notes or caveats from parsing"
  },
  "slides": [
    {
      "index": 0,
      "layout_hint": "title_slide | section_break | content | two_column | image_full | data_chart | table | timeline | blank",
      "title": "Slide Title",
      "subtitle": "Optional subtitle",
      "body": [
        {
          "type": "bullet_list | paragraph | numbered_list | code | quote",
          "content": "Text content here",
          "level": 0
        }
      ],
      "images": [
        {
          "slot_id": "img_0",
          "src": "base64_or_url_or_null",
          "alt": "Image description for art direction",
          "position_hint": "full_bleed | right_panel | inline"
        }
      ],
      "table": null,
      "chart": null,
      "speaker_notes": "Optional speaker notes text"
    }
  ]
}
```

### Table Schema (when present)

```json
{
  "headers": ["Column A", "Column B", "Column C"],
  "rows": [
    ["value", "value", "value"]
  ],
  "caption": "Optional caption"
}
```

### Chart Schema (when present)

```json
{
  "chart_type": "bar | line | pie | scatter | area",
  "title": "Chart title",
  "series": [
    {
      "label": "Series name",
      "data": [1, 2, 3, 4]
    }
  ],
  "x_axis_labels": ["Q1", "Q2", "Q3", "Q4"],
  "y_axis_label": "Revenue ($M)"
}
```

## Error Handling

| Condition | Action |
|---|---|
| PPTX parse fails with python-pptx | Retry with markitdown, note fallback in `meta.notes` |
| PDF has no extractable text (scanned) | Notify user, offer to proceed with image-only slides |
| Input is ambiguous | Ask clarifying questions before proceeding |
| Missing required content slots | Mark slot as `"content": null` and flag for user review |
| Aspect ratio unclear | Default to 16:9, confirm with user |

## Passing Output Downstream

Pass the complete Slide Data JSON to:
- `plan-slides` skill for structure and template assignment
- `brand-profile` skill if brand extraction is also needed
- `design-slide` directly if the plan is already known

The Slide Data JSON is the single source of truth for all content throughout the presentation pipeline.
