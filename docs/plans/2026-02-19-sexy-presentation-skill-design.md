# Sexy Presentation Skill — Design Document

**Date:** 2026-02-19
**Status:** Approved

## Summary

A Claude Code plugin that creates magazine-quality, visually stunning presentations. Uses HTML + Tailwind CSS as the intermediate format, exports to PDF, editable PPTX, and Figma. Features an interactive playground for design iteration, a 200+ template corpus, and a multi-agent architecture with parallel subagents for scalable, context-efficient production.

## Core Architecture

### Four Layers

```
INPUT LAYER            DESIGN SYSTEM              PLAYGROUND                    EXPORT + IMAGERY
─────────────         ─────────────              ─────────────                 ─────────────
Natural language  →                            → Template Gallery             → HTML
Structured MD     →   Template Corpus (207+)   →   (visual thumbnails)        → PDF (Puppeteer)
Existing PPTX     →   Component Library        → Config Panel                 → Figma (MCP)
Existing PDF      →   Theme Presets            →   (dropdowns/sliders)        → PPTX (pptxgenjs)
                  →   Layout Engine            → Chat Iteration               →
                  →   Brand Profile System     →   ("make it darker")         → Unsplash API
                                               → Live Preview                 → Pexels/Pixabay
                                               →   (instant updates)          → AI Image-Gen Prompts
```

## Agent Roster

| Agent | Role | Context Received | When Called |
|-------|------|-----------------|------------|
| **Orchestrator** | Manages full workflow, dispatches agents, tracks progress, assembles output | Full slide plan, theme, brand profile | Always — the conductor |
| **Slide Designer** | Designs individual slide HTML from content + template | 1 slide's content + theme + 2-3 templates + brand profile | Step 3, parallelized (one per slide) |
| **Copy Editor** | Rewrites headlines, cleans text, tightens prose, ensures voice consistency | Slide text + brand voice guidelines | On demand — user or orchestrator invokes |
| **Image Director** | Art-directs imagery: sources from Unsplash/Pexels, writes AI image-gen prompts | Theme + deck mood + slide content + brand imagery guidelines | Step 3 (parallel) + on demand |
| **Table Designer** | Creates beautifully styled HTML tables with proper formatting | Table data + theme + brand profile | When slide contains tabular data |
| **Timeline Agent** | Builds timeline/process flow visualizations | Timeline data + theme + brand profile | When slide contains process/timeline content |
| **Infographic Agent** | Creates data viz, stat callouts, icon grids, metric dashboards | Data/stats + theme + brand profile | When slide contains data/metrics |
| **Playground Agent** | Manages interactive playground experience | Full deck HTML + theme + templates | Step 4, interactive loop |
| **Art Director** | Reviews full deck screenshots for visual issues | Screenshots of all slides + design checklist | Step 5, after playground |
| **Graphics Polisher** | Final consistency pass — spacing, alignment, motifs, visual coherence | Full HTML + Art Director feedback + brand profile | Step 6, after Art Director |

## Workflow

```
ORCHESTRATOR manages everything
    │
    ├─ Step 1: ANALYZE INPUT
    │   Parse PPTX/PDF/MD/natural language → Slide Data format
    │
    ├─ Step 2: PLAN SLIDES
    │   Decide structure, assign templates, select theme
    │   Identify specialized content (tables, timelines, infographics)
    │
    ├─ Step 3: PARALLEL DESIGN
    │   ├─ Slide Designer ×N (one per slide, parallel)
    │   ├─ Table Designer (for slides with tabular data)
    │   ├─ Timeline Agent (for process/timeline slides)
    │   ├─ Infographic Agent (for data/metrics slides)
    │   ├─ Image Director (sources imagery + writes gen prompts)
    │   └─ Copy Editor (optional — if input text needs cleanup)
    │
    ├─ Step 4: PLAYGROUND (interactive)
    │   Playground Agent manages:
    │   ├─ Template Gallery — browse and apply templates
    │   ├─ Config Panel — theme, colors, fonts, columns, backgrounds
    │   ├─ Chat-driven iteration — natural language changes
    │   └─ Can call Copy Editor or Image Director on demand
    │
    ├─ Step 5: ART DIRECTOR REVIEW
    │   Screenshots → visual QA → feedback list
    │   (alignment, contrast, spacing, consistency, readability)
    │
    ├─ Step 6: GRAPHICS POLISHER
    │   Applies Art Director feedback + final consistency pass
    │
    └─ Step 7: EXPORT (parallel)
        ├─ PDF (Puppeteer/Playwright)
        ├─ PPTX (pptxgenjs, reconstructed & editable)
        └─ Figma (via Figma MCP server)
```

## Context Window Strategy

Each agent receives only what it needs to minimize context usage:

| Agent | Context Size | Contents |
|-------|-------------|----------|
| Slide Designer | Small | 1 slide's content + theme + 2-3 templates + brand profile (~50 lines JSON) |
| Image Director | Small | Slide titles/descriptions + art direction brief + brand imagery rules |
| Table/Timeline/Infographic | Small | Specific data + theme + brand profile |
| Copy Editor | Small | Text to edit + brand voice guidelines |
| Playground Agent | Medium | Full deck HTML + theme + available templates |
| Art Director | Medium | Screenshots (images) + design checklist |
| Graphics Polisher | Large | Full HTML + Art Director feedback + brand profile |

## Template Corpus (207+ templates)

Templates are composable: **Purpose x Layout x Visual Treatment**

| Category | Layouts | x Treatments | = Templates |
|----------|---------|-------------|-------------|
| Title / Cover | 8 | x 3 | 24 |
| Content / Body | 12 | x 3 | 36 |
| Data / Statistics | 8 | x 3 | 24 |
| Image / Visual | 8 | x 3 | 24 |
| Comparison | 6 | x 3 | 18 |
| Timeline / Process | 6 | x 3 | 18 |
| Quote / Testimonial | 5 | x 3 | 15 |
| Team / People | 5 | x 3 | 15 |
| Structural (divider, TOC) | 6 | x 3 | 18 |
| Closing / CTA | 5 | x 3 | 15 |
| **Total** | **69 layouts** | | **207** |

**Visual treatments** (the x3 multiplier):
1. **Light** — white/cream background
2. **Colored** — tinted background using theme palette
3. **Reversed** — dark background, light text

Each template is a Tailwind HTML snippet parameterized by CSS variables. Swap theme = all templates update.

## Theme System

### Theme Presets

Each theme defines: color palette, typography, spacing, visual motif, background modes.

| Theme | Vibe | Style |
|-------|------|-------|
| Keynote Minimal | Apple-style clean | White/black/accent blue |
| Pitch Bold | Startup energy | Dark bg, vibrant accent |
| Consulting Polish | McKinsey/BCG feel | Navy/white/gold |
| Editorial | Magazine spread | Serif headers, muted tones |
| Creative Pop | TED talk energy | Bold colors, large type |
| Data Story | Analytics/charts | Cool grays, data accent colors |

### Theme Structure

```json
{
  "name": "consulting-polish",
  "colors": {
    "primary": "#1E2761",
    "secondary": "#CADCFC",
    "accent": "#D4AF37",
    "background": "#FFFFFF",
    "text": "#2D2D2D",
    "text_reversed": "#FFFFFF"
  },
  "typography": {
    "header_font": "Georgia",
    "body_font": "Calibri",
    "title_size": "44px",
    "header_size": "24px",
    "body_size": "16px"
  },
  "spacing": {
    "margin": "1in",
    "gap": "0.5in",
    "density": "comfortable"
  },
  "motif": "subtle-border-left",
  "background_modes": ["light", "colored", "reversed"]
}
```

## Brand Guide Integration

### Brand Profile System

A structured JSON extraction of brand guidelines, injected into every agent's context.

**Input sources:**
- PDF brand guide (parsed by Claude)
- URL to brand page (fetched and parsed)
- User describes brand verbally
- Existing `brand-profile.json` file

**Brand Profile Skill** extracts/creates the profile. Run once, reuse for every deck.

### brand-profile.json

```json
{
  "company": "Acme Corp",
  "colors": {
    "primary": "#1E3A5F",
    "secondary": "#4A90D9",
    "accent": "#FF6B35",
    "background": "#FFFFFF",
    "text": "#2D2D2D",
    "forbidden": ["#FF0000"]
  },
  "typography": {
    "header_font": "Montserrat",
    "body_font": "Open Sans",
    "min_body_size": "14px",
    "rules": ["Never use italic for headers"]
  },
  "logo": {
    "primary": "path/to/logo.svg",
    "icon_only": "path/to/icon.svg",
    "placement_rules": "Top-right corner, minimum 0.5in margin",
    "min_clear_space": "1x logo height on all sides"
  },
  "imagery": {
    "style": "Authentic photography, natural lighting, diverse people",
    "avoid": "Stock photo cliches, clip art, overly staged shots",
    "filters": "Slight warm tone, no heavy saturation"
  },
  "layout_rules": [
    "Always use left-aligned body text",
    "Minimum 1in margins on all sides",
    "Section dividers use primary color background"
  ]
}
```

**Brand profile overrides theme defaults.** Theme says navy blue, brand guide says `#1E3A5F` — brand wins.

## Image Director Details

The Image Director agent handles all visual imagery with three capabilities:

1. **Art Direction** — Analyzes deck theme, mood, and content to define a visual direction (e.g., "warm editorial photography, natural light, human-centered"). Informed by brand imagery guidelines when a brand profile exists.

2. **Image Sourcing** — Searches Unsplash/Pexels/Pixabay with art-direction-aware queries. Not just keyword matching — understands mood, composition, and brand fit.

3. **Image-Gen Prompts** — Writes detailed prompts for AI image generators (Midjourney, DALL-E, nano banana, etc.) tailored to each slide's content and the overall art direction. Prompts can be copied or piped to image-gen tools.

Callable on demand: "find me a better hero image for slide 3" or "write a prompt for an abstract data viz background."

## Playground

An interactive HTML file with three interaction modes:

1. **Template Gallery** — Visual grid of template thumbnails. Click to apply. Categories match the template corpus structure.

2. **Config Panel** — Sidebar controls:
   - Theme preset (dropdown)
   - Color palette (swatches or custom hex)
   - Font pairing (dropdown with live preview)
   - Column count (1-4)
   - Background mode (white / colored / dark reversed)
   - Logo upload + placement
   - Page numbering style
   - Spacing/density (compact / comfortable / spacious)

3. **Chat-Driven Iteration** — Natural language changes processed by Claude: "make the headers bigger", "switch to 3 columns", "add more whitespace."

## Input Parsing

Multi-tool approach with fallbacks for malformed files:

| Input | Primary Tool | Fallback |
|-------|-------------|----------|
| PPTX | python-pptx | markitdown, LibreOffice CLI |
| PDF | PyMuPDF | pdf.js, pdftotext (poppler) |
| Markdown | Direct parse | — |
| Natural language | Claude analysis | — |

All inputs normalize to Slide Data intermediate format:

```json
{
  "slides": [
    {
      "purpose": "title",
      "title": "...",
      "subtitle": "...",
      "content_blocks": [],
      "speaker_notes": "...",
      "layout_hints": ["full-bleed", "centered"],
      "images": [],
      "data": null
    }
  ]
}
```

## Export Pipeline

- **PDF** — Puppeteer/Playwright renders HTML at 1920x1080, prints to PDF
- **PPTX** — pptxgenjs reconstructs layouts from HTML (editable output)
- **Figma** — Figma MCP server integration pushes slides as native Figma components
- **HTML** — Source files viewable directly in browser

## Plugin File Structure

```
sexy-presentation-skill/
├── package.json
├── skills/
│   ├── presentation.md            # Orchestrator entry point
│   ├── analyze-input.md           # Input parsing
│   ├── plan-slides.md             # Slide structure planning
│   ├── design-slide.md            # Single slide HTML generation
│   ├── select-theme.md            # Theme selection & customization
│   ├── source-imagery.md          # Image sourcing & art direction
│   ├── brand-profile.md           # Brand guide extraction
│   ├── playground.md              # Playground generation
│   ├── export.md                  # Export to PDF/PPTX/Figma
│   ├── qa-art-director.md         # QA review instructions
│   └── polish-graphics.md         # Final polish instructions
├── agents/
│   ├── orchestrator.md            # Workflow conductor
│   ├── slide-designer.md          # Individual slide design
│   ├── copy-editor.md             # Text cleanup & rewriting
│   ├── image-director.md          # Art direction + sourcing + gen prompts
│   ├── table-designer.md          # Beautiful table layouts
│   ├── timeline-agent.md          # Timeline/process visualizations
│   ├── infographic-agent.md       # Data viz & infographics
│   ├── art-director.md            # Visual QA review
│   ├── graphics-polisher.md       # Final consistency pass
│   └── playground-agent.md        # Interactive playground management
├── templates/
│   ├── index.json                 # Template registry
│   ├── title/
│   ├── content/
│   ├── data/
│   ├── image/
│   ├── comparison/
│   ├── timeline/
│   ├── quote/
│   ├── team/
│   ├── structural/
│   └── closing/
├── themes/
│   ├── keynote-minimal.json
│   ├── pitch-bold.json
│   ├── consulting-polish.json
│   ├── editorial.json
│   ├── creative-pop.json
│   └── data-story.json
├── components/
│   ├── icons.html
│   ├── boxes.html
│   ├── grids.html
│   ├── page-numbers.html
│   └── logos.html
├── scripts/
│   ├── export-pdf.js
│   ├── export-pptx.js
│   ├── parse-pptx.py
│   ├── parse-pdf.py
│   └── fetch-images.js
└── playground/
    └── playground-template.html
```

## Design Decisions

1. **HTML + Tailwind over Reveal.js** — Maximum design flexibility, no framework constraints, plays to Claude's HTML generation strengths.
2. **Composable templates (Purpose x Layout x Treatment)** — Achieves 207+ templates from 69 base layouts without hand-crafting each one.
3. **Decomposed plugin with parallel subagents** — Keeps context windows small, enables parallelism, and allows specialized agents to focus on what they do best.
4. **Brand profile as override layer** — Compact JSON (~50 lines) injected into every agent without bloating context. Overrides theme defaults.
5. **Editable PPTX export via pptxgenjs** — More complex than image-based export but produces editable output users can modify in PowerPoint/Google Slides.
6. **Image Director with gen-prompt capability** — Bridges stock photography (Unsplash) and AI generation, giving users options for both.
7. **Multi-stage QA (Art Director → Graphics Polisher)** — Separates identification of issues from fixing them, using fresh-eye agents for honest review.
