---
name: Plan Slides
description: Takes normalized Slide Data JSON and produces a structured Slide Plan array — deciding slide count, assigning template categories, and flagging specialized content blocks for dedicated treatment.
version: 0.1.0
---

# Plan Slides Skill

## Purpose

Transform the raw Slide Data JSON (from `analyze-input`) into an actionable **Slide Plan array** that tells each downstream design subagent exactly which template to use, what content to render, and what special handling is required.

## Inputs

- **Slide Data JSON** from the `analyze-input` skill
- **Theme CSS variables** from the `select-theme` skill (used to recommend templates that complement the theme)
- **User preferences** (if provided): target slide count, pacing, emphasis slides

## Decision Process

### 1. Determine Slide Count

If the input already contains explicit slides (from a PPTX or structured markdown), preserve the original count unless the user asks to consolidate or expand.

If the input is natural language or a sparse outline:

| Word count / complexity | Recommended slides |
|---|---|
| < 200 words, 1 topic | 5–8 slides |
| 200–600 words, 2–4 topics | 8–15 slides |
| 600–1500 words, 4+ topics | 15–25 slides |
| Full document / report | 25+ slides, suggest chapter breaks |

Always reserve slots for: title slide, agenda/overview (if 8+ slides), section breaks (every 4–6 content slides), and a closing/CTA slide.

### 2. Assign Template Categories

For each slide, select the most appropriate template category from the available set at `CLAUDE_PLUGIN_ROOT/templates/`. Use the slide's `layout_hint` from Slide Data as the primary signal, then apply the rules below.

| Content signal | Template category |
|---|---|
| Title only, first slide | `title-slide` |
| Title + short text, standalone point | `statement` |
| Title + 3–5 bullets | `bullet-list` |
| Title + 2 parallel sections | `two-column` |
| Title + body text paragraph | `editorial` |
| Single large image + caption | `image-full-bleed` |
| Image left/right + text | `image-split` |
| Data table | `table` |
| Bar / line / pie chart | `chart` |
| Sequential steps or phases | `timeline` |
| Team bios | `team-grid` |
| Pull quote or testimonial | `quote` |
| Stats / KPIs (2–4 numbers) | `metrics` |
| Map or geography data | `map` |
| Cover for new section | `section-break` |
| Closing / thank you / CTA | `closing` |
| No strong signal | `content` (generic) |

### 3. Identify Specialized Content

Flag slides that require non-standard processing so the orchestrator can route them correctly:

- **Tables**: pass raw table data to `design-slide` with `specialized: "table"`
- **Charts**: pass chart series data to `design-slide` with `specialized: "chart"` — include chart type recommendation
- **Timelines**: extract ordered steps, pass with `specialized: "timeline"`
- **Maps**: flag geography data for map rendering with `specialized: "map"`
- **Code blocks**: flag for syntax-highlighted code slide with `specialized: "code"`
- **Image-heavy slides**: flag for `source-imagery` skill with `needs_imagery: true`

### 4. Pacing and Flow Review

After the initial template assignment, review the sequence for pacing issues:

- Avoid more than 3 consecutive bullet-list slides — insert a statement, metrics, or image slide to break the rhythm
- Ensure section breaks appear at logical chapter boundaries
- The closing slide should always be the last slide
- If there is only one section break or none, consider whether the presentation needs clearer chapter structure

Reorder or add slides as needed. Document any additions made (with reason) in the plan's `notes` field.

## Output Format: Slide Plan Array

```json
{
  "plan_meta": {
    "total_slides": 14,
    "theme_id": "midnight-bold",
    "generated_at": "ISO8601 timestamp",
    "notes": "Added 2 section breaks for pacing. Consolidated 3 sparse bullet slides into 1 two-column slide."
  },
  "slides": [
    {
      "index": 0,
      "template_category": "title-slide",
      "template_path": "CLAUDE_PLUGIN_ROOT/templates/title-slide/01-centered.html",
      "title": "Slide Title",
      "subtitle": "Optional subtitle",
      "body": [],
      "images": [],
      "table": null,
      "chart": null,
      "specialized": null,
      "needs_imagery": false,
      "speaker_notes": "",
      "design_notes": "Use the hero variant with large title treatment"
    },
    {
      "index": 1,
      "template_category": "metrics",
      "template_path": "CLAUDE_PLUGIN_ROOT/templates/metrics/03-three-up.html",
      "title": "Key Numbers",
      "subtitle": null,
      "body": [],
      "images": [],
      "table": null,
      "chart": null,
      "specialized": null,
      "needs_imagery": false,
      "speaker_notes": "Explain each metric briefly",
      "design_notes": "Three equal-width stat cards with large numerals"
    }
  ]
}
```

### Template Path Selection

For each template category, multiple variants may exist under `CLAUDE_PLUGIN_ROOT/templates/<category>/`. Select the variant that best fits:

1. The amount of content (short vs. dense text)
2. The number of visual elements (single image vs. gallery)
3. The theme's aesthetic (bold/editorial vs. minimal/corporate)

If uncertain, default to the `01-` prefixed variant (canonical default for the category).

## Passing Output Downstream

Pass the complete Slide Plan array to:
- The **orchestrator** which dispatches one `design-slide` subagent per slide entry
- The `source-imagery` skill for any slides with `needs_imagery: true`
- The `qa-art-director` skill after all slides are assembled (pass the plan as context for the checklist)
