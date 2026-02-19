---
name: presentation
description: Create a magazine-quality presentation from any input — text, PDF, PPTX, or topic description. Launches the full orchestrator pipeline with parallel slide design.
arguments:
  - name: input
    description: "Path to input file (PDF, PPTX, text) OR a topic description in quotes"
    required: true
  - name: slides
    description: "Target number of slides (default: auto-detect from content)"
    required: false
  - name: theme
    description: "Theme name to use (e.g., keynote-minimal, pitch-bold). Omit to be prompted."
    required: false
  - name: brand
    description: "Brand profile name to apply (must exist in memory/brand/)"
    required: false
  - name: format
    description: "Export format: html (default), pdf, pptx, figma"
    required: false
  - name: preset
    description: "Model routing preset: balanced (default), quality-first, cost-saver, speed"
    required: false
---

# /presentation Command

You are the entry point for creating presentations with the sexy-presentation plugin.

## What You Do

When the user runs `/presentation`, you orchestrate the full pipeline:

1. **Parse input** — determine what the user provided (file path, URL, or text)
2. **Load configuration** — model routing preset, brand profile, theme
3. **Launch the Orchestrator agent** — which runs the 7-step pipeline:
   - Analyze input (skill: analyze-input)
   - Select theme (skill: select-theme, with brand overrides if applicable)
   - Plan slides (skill: plan-slides)
   - Design slides in parallel (agent: slide-designer, one per slide)
   - Source imagery (skill: source-imagery)
   - QA pass (skill: qa-art-director + agent: graphics-polisher)
   - Assemble and deliver (skill: playground or export)

## Input Handling

### File input
```
/presentation ./quarterly-report.pdf
/presentation ./existing-deck.pptx
/presentation ./notes.txt
```
- PDF: parsed via `scripts/parse-pdf.py`
- PPTX: parsed via `scripts/parse-pptx.py`
- Text/Markdown: read directly

### Topic input
```
/presentation "AI in Healthcare: Current State and Future Directions"
/presentation "Q4 2025 Sales Results" --slides 12
```
- The orchestrator generates content from the topic description

### URL input
```
/presentation https://example.com/blog-post
```
- Fetch and extract content from the URL

## Configuration

### Model routing
Load from `config/model-routing.json`. Apply the preset specified by `--preset` or use "balanced" default.

### Brand profile
If `--brand` specified, load from `memory/brand/<name>.json`. If only one brand exists, auto-apply it. If multiple brands exist and none specified, ask.

### Theme
If `--theme` specified, load directly. Otherwise, run the select-theme skill interactively.

## Example Invocations

```
# Minimal — interactive theme selection
/presentation "Company Overview for Investors"

# Full specification
/presentation ./data.pdf --slides 15 --theme pitch-bold --brand acme-corp --format pdf --preset quality-first

# Quick cost-effective deck
/presentation "Team standup update" --slides 5 --theme keynote-minimal --preset speed
```

## Output

After the pipeline completes:
1. Open the interactive playground (default) OR export to the requested format
2. Report: slide count, theme used, model routing preset, estimated cost tier
3. Offer iteration: "Would you like to adjust any slides?"

## Error Recovery

| Error | Action |
|---|---|
| Input file not found | Ask user to provide correct path |
| PDF/PPTX parse fails | Fall back to alternative parser, report to user |
| Theme not found | Show available themes, ask user to choose |
| Brand profile not found | Offer to create one via brand-profile skill |
| Slide design fails for one slide | Retry once, then skip and report |
| Export fails | Report error, offer alternative format |
