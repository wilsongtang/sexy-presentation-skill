---
name: QA Art Director
description: Run a thorough visual quality assurance pass over the assembled presentation. Applies an Art Director checklist to each slide, generates screenshots where possible, and returns a structured issue report categorized by severity.
version: 0.1.0
---

# QA Art Director Skill

## Purpose

Act as a senior art director reviewing the assembled presentation before it reaches the user or is sent to export. Catch visual, typographic, layout, and brand consistency issues. Produce a clear, actionable issue report that the `polish-graphics` skill can execute against.

## Inputs

- Assembled presentation HTML (all slides)
- Slide Plan array (for context on intended design)
- Theme CSS variable block (for checking adherence)
- Brand profile JSON (if available, for brand compliance checks)

## Screenshot Generation

Where the environment supports a headless browser, generate a PNG screenshot of each slide for visual inspection:

```bash
node CLAUDE_PLUGIN_ROOT/scripts/screenshot-slides.js \
  --input ./output/presentation.html \
  --output ./output/qa-screenshots/ \
  --slides-selector ".slide" \
  --width 1280 \
  --height 720
```

Screenshots are named `slide-00.png`, `slide-01.png`, etc.

If screenshots cannot be generated, perform the QA pass by reading the HTML and CSS directly. Note in the report that visual inspection was HTML-only.

## Art Director Checklist

Apply all checklist items to every slide. Record pass/fail per item per slide.

### Typography

- [ ] **T1** — A single `<h1>` heading is present on each content slide (not zero, not two)
- [ ] **T2** — Heading font matches `--font-heading` CSS variable (no hardcoded font-family overrides)
- [ ] **T3** — Body font matches `--font-body` CSS variable
- [ ] **T4** — No more than two typefaces appear on any single slide
- [ ] **T5** — Font sizes follow the defined scale (`--font-size-heading-xl/lg/md`, `--font-size-body`)
- [ ] **T6** — Line height is comfortable for body text (minimum 1.4 for paragraphs)
- [ ] **T7** — Bullet lists have no more than 6 items per slide
- [ ] **T8** — No bullet list item wraps to more than 2 lines at 1280px viewport

### Color and Contrast

- [ ] **C1** — All text passes WCAG AA contrast ratio (4.5:1 for body, 3:1 for large headings)
- [ ] **C2** — No colors appear that are not defined in the theme CSS variables or brand profile
- [ ] **C3** — Accent color is used sparingly — maximum 2 distinct uses per slide
- [ ] **C4** — Background color is consistent across the presentation (except intentional section breaks)
- [ ] **C5** — No pure white (#FFFFFF) text on pure black (#000000) background or vice versa (use near-values for visual softness)

### Layout and Spacing

- [ ] **L1** — All content is within the safe zone (minimum 5% margin from slide edges on all sides)
- [ ] **L2** — No text or image overflow beyond the slide boundaries
- [ ] **L3** — Consistent spacing between heading and body (matches `--spacing-base` or `--spacing-tight`)
- [ ] **L4** — Grid/flex layouts align correctly — no ragged baselines or misaligned columns
- [ ] **L5** — Two-column slides have balanced content weight (neither column is dramatically more dense)
- [ ] **L6** — Slide number (if shown) is consistently positioned across all slides

### Images

- [ ] **I1** — All image slots are filled — no broken images, placeholder boxes, or empty containers
- [ ] **I2** — Images use `object-fit: cover` and do not appear stretched or squished
- [ ] **I3** — Full-bleed background images have sufficient contrast with overlaid text
- [ ] **I4** — Images are visually consistent in style across the presentation (no jarring style mix)
- [ ] **I5** — No image has visible compression artifacts at the displayed size
- [ ] **I6** — All `<img>` elements have descriptive `alt` attributes

### Brand Compliance (if brand profile provided)

- [ ] **B1** — Primary brand color is used correctly (not substituted with a similar but off-brand color)
- [ ] **B2** — Logo appears on required slides as specified in `brand_profile.presentation_rules.logo_on_slides`
- [ ] **B3** — Logo has the correct safe area clearance on all sides
- [ ] **B4** — No forbidden colors appear anywhere in the presentation
- [ ] **B5** — No forbidden fonts appear anywhere in the presentation
- [ ] **B6** — Footer text matches `brand_profile.presentation_rules.footer_text` (if specified)

### Consistency Across Slides

- [ ] **X1** — Title style is identical across all content slides (same font, size, color, position)
- [ ] **X2** — Section break slides use a consistent template
- [ ] **X3** — The closing slide uses the designated closing template
- [ ] **X4** — Transition between slides (if HTML export) is consistent and not jarring
- [ ] **X5** — Charts and tables use a consistent visual style (same color palette, border radius, header style)

## Issue Severity Classification

Classify each failed checklist item by severity:

| Severity | Definition | Example |
|---|---|---|
| `critical` | Presentation cannot be used in this state | Text overflows off slide, broken image on title slide |
| `high` | Significant visual or brand problem that will be noticed | Off-brand color on primary CTA, WCAG contrast failure |
| `medium` | Noticeable inconsistency that reduces professionalism | Two slightly different heading sizes on adjacent slides |
| `low` | Minor polish opportunity | Slightly uneven padding on one slide's bullet list |
| `suggestion` | Optional improvement that would enhance quality | "Consider a stronger image for slide 6" |

## Output Format: Issue Report

```json
{
  "qa_summary": {
    "total_slides": 14,
    "slides_with_issues": 4,
    "issue_counts": {
      "critical": 1,
      "high": 2,
      "medium": 3,
      "low": 5,
      "suggestion": 2
    },
    "screenshot_dir": "./output/qa-screenshots/",
    "qa_method": "headless_screenshots | html_only",
    "reviewed_at": "ISO8601 timestamp"
  },
  "issues": [
    {
      "id": "QA-001",
      "severity": "critical",
      "slide_index": 3,
      "checklist_item": "L2",
      "description": "Body text overflows the right edge of the slide at 1280px viewport width.",
      "affected_element": ".slide[data-index='3'] .slide-body",
      "screenshot_ref": "./output/qa-screenshots/slide-03.png",
      "suggested_fix": "Reduce font size by one step or apply `overflow: hidden` with text truncation. Consider splitting content across two slides."
    },
    {
      "id": "QA-002",
      "severity": "high",
      "slide_index": 7,
      "checklist_item": "C1",
      "description": "Body text (#888BA0) on background (#16213E) has a contrast ratio of 3.2:1, below the WCAG AA threshold of 4.5:1.",
      "affected_element": ".slide[data-index='7'] .slide-body p",
      "screenshot_ref": "./output/qa-screenshots/slide-07.png",
      "suggested_fix": "Lighten the text color to #A8ABB8 or darker to achieve at least 4.5:1 ratio against the background."
    }
  ]
}
```

## Passing Output Downstream

Pass the full Issue Report JSON to the `polish-graphics` skill for automated remediation of `critical`, `high`, and `medium` severity issues.

`low` and `suggestion` issues should be presented to the user for their decision — some may prefer to skip low-priority fixes to save time.

If there are zero `critical` or `high` issues, inform the user that the presentation passed QA and proceed to the playground or export step. If there are `critical` issues, do not proceed to export until they are resolved.
