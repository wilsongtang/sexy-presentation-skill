# Sexy Presentation Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Claude Code plugin with 10 specialized agents, 11 skills, 207+ composable HTML/Tailwind templates, an interactive playground, and export pipelines for PDF/PPTX/Figma.

**Architecture:** Multi-agent plugin where an Orchestrator dispatches parallel Slide Designer subagents (one per slide), supported by specialized agents (Copy Editor, Image Director, Table Designer, Timeline, Infographic). QA pipeline uses Art Director + Graphics Polisher agents. Interactive playground for real-time design iteration.

**Tech Stack:** Claude Code plugin (markdown skills/agents), Tailwind CSS (templates), Node.js (pptxgenjs export, Puppeteer PDF), Python (PPTX/PDF input parsing), Unsplash API (image sourcing), Figma MCP (Figma export).

**Design doc:** `docs/plans/2026-02-19-sexy-presentation-skill-design.md`

---

## Phase 1: Plugin Scaffold

### Task 1: Create plugin manifest

**Files:**
- Create: `.claude-plugin/plugin.json`

**Step 1: Create the manifest file**

```json
{
  "name": "sexy-presentation",
  "version": "0.1.0",
  "description": "Magazine-quality presentation design with 200+ templates, parallel subagents, and interactive playground",
  "author": {
    "name": "Wilson Tang"
  },
  "keywords": ["presentation", "slides", "design", "tailwind", "pptx", "pdf", "figma"]
}
```

**Step 2: Verify plugin structure is valid**

Run: `ls .claude-plugin/plugin.json`
Expected: File exists

**Step 3: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat: initialize plugin scaffold with manifest"
```

---

### Task 2: Create directory structure

**Files:**
- Create directories: `commands/`, `agents/`, `skills/`, `templates/`, `themes/`, `components/`, `scripts/`, `playground/`
- Create template subdirectories: `templates/title/`, `templates/content/`, `templates/data/`, `templates/image/`, `templates/comparison/`, `templates/timeline/`, `templates/quote/`, `templates/team/`, `templates/structural/`, `templates/closing/`

**Step 1: Create all directories**

```bash
mkdir -p commands agents skills/{presentation,analyze-input,plan-slides,design-slide,select-theme,source-imagery,brand-profile,playground,export,qa-art-director,polish-graphics}
mkdir -p templates/{title,content,data,image,comparison,timeline,quote,team,structural,closing}
mkdir -p themes components scripts playground
```

**Step 2: Verify structure**

Run: `find . -type d | sort | head -30`
Expected: All directories present

**Step 3: Commit**

```bash
git add -A
git commit -m "feat: create full plugin directory structure"
```

---

## Phase 2: Theme System

### Task 3: Define the theme JSON schema

**Files:**
- Create: `themes/schema.json`

**Step 1: Write the theme schema**

This schema defines the contract all themes must follow. Every template reads CSS variables generated from these values.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Presentation Theme",
  "type": "object",
  "required": ["name", "colors", "typography", "spacing", "motif", "background_modes"],
  "properties": {
    "name": { "type": "string" },
    "display_name": { "type": "string" },
    "description": { "type": "string" },
    "colors": {
      "type": "object",
      "required": ["primary", "secondary", "accent", "background", "text", "text_reversed"],
      "properties": {
        "primary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "secondary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "accent": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "background": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "text": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "text_reversed": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "muted": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "border": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" }
      }
    },
    "typography": {
      "type": "object",
      "required": ["header_font", "body_font", "title_size", "header_size", "body_size"],
      "properties": {
        "header_font": { "type": "string" },
        "body_font": { "type": "string" },
        "title_size": { "type": "string" },
        "header_size": { "type": "string" },
        "body_size": { "type": "string" },
        "caption_size": { "type": "string" },
        "line_height": { "type": "string" }
      }
    },
    "spacing": {
      "type": "object",
      "required": ["margin", "gap", "density"],
      "properties": {
        "margin": { "type": "string" },
        "gap": { "type": "string" },
        "density": { "type": "string", "enum": ["compact", "comfortable", "spacious"] }
      }
    },
    "motif": { "type": "string" },
    "background_modes": {
      "type": "array",
      "items": { "type": "string", "enum": ["light", "colored", "reversed"] }
    }
  }
}
```

**Step 2: Commit**

```bash
git add themes/schema.json
git commit -m "feat: add theme JSON schema"
```

---

### Task 4: Create all 6 starter themes

**Files:**
- Create: `themes/keynote-minimal.json`
- Create: `themes/pitch-bold.json`
- Create: `themes/consulting-polish.json`
- Create: `themes/editorial.json`
- Create: `themes/creative-pop.json`
- Create: `themes/data-story.json`

**Step 1: Write keynote-minimal.json**

```json
{
  "name": "keynote-minimal",
  "display_name": "Keynote Minimal",
  "description": "Apple-style clean presentation with generous whitespace and subtle accents",
  "colors": {
    "primary": "#1D1D1F",
    "secondary": "#86868B",
    "accent": "#0071E3",
    "background": "#FFFFFF",
    "text": "#1D1D1F",
    "text_reversed": "#FFFFFF",
    "muted": "#86868B",
    "border": "#D2D2D7"
  },
  "typography": {
    "header_font": "SF Pro Display, Helvetica Neue, Arial, sans-serif",
    "body_font": "SF Pro Text, Helvetica Neue, Arial, sans-serif",
    "title_size": "48px",
    "header_size": "28px",
    "body_size": "18px",
    "caption_size": "14px",
    "line_height": "1.5"
  },
  "spacing": {
    "margin": "80px",
    "gap": "40px",
    "density": "spacious"
  },
  "motif": "clean-whitespace",
  "background_modes": ["light", "reversed"]
}
```

**Step 2: Write pitch-bold.json**

```json
{
  "name": "pitch-bold",
  "display_name": "Pitch Bold",
  "description": "Startup energy with dark backgrounds and vibrant accent colors",
  "colors": {
    "primary": "#FFFFFF",
    "secondary": "#A0A0A0",
    "accent": "#FF6B2B",
    "background": "#0D0D0D",
    "text": "#FFFFFF",
    "text_reversed": "#0D0D0D",
    "muted": "#666666",
    "border": "#333333"
  },
  "typography": {
    "header_font": "Inter, Helvetica Neue, Arial, sans-serif",
    "body_font": "Inter, Helvetica Neue, Arial, sans-serif",
    "title_size": "56px",
    "header_size": "32px",
    "body_size": "18px",
    "caption_size": "14px",
    "line_height": "1.6"
  },
  "spacing": {
    "margin": "64px",
    "gap": "32px",
    "density": "comfortable"
  },
  "motif": "bold-accent-blocks",
  "background_modes": ["reversed", "colored"]
}
```

**Step 3: Write consulting-polish.json**

```json
{
  "name": "consulting-polish",
  "display_name": "Consulting Polish",
  "description": "McKinsey/BCG-style professional presentation with navy and gold accents",
  "colors": {
    "primary": "#1E2761",
    "secondary": "#CADCFC",
    "accent": "#D4AF37",
    "background": "#FFFFFF",
    "text": "#2D2D2D",
    "text_reversed": "#FFFFFF",
    "muted": "#6B7280",
    "border": "#E5E7EB"
  },
  "typography": {
    "header_font": "Georgia, Cambria, serif",
    "body_font": "Calibri, Arial, sans-serif",
    "title_size": "44px",
    "header_size": "24px",
    "body_size": "16px",
    "caption_size": "12px",
    "line_height": "1.5"
  },
  "spacing": {
    "margin": "72px",
    "gap": "36px",
    "density": "comfortable"
  },
  "motif": "subtle-border-left",
  "background_modes": ["light", "colored", "reversed"]
}
```

**Step 4: Write editorial.json**

```json
{
  "name": "editorial",
  "display_name": "Editorial",
  "description": "Magazine-spread aesthetic with serif headers and muted earth tones",
  "colors": {
    "primary": "#2C2C2C",
    "secondary": "#8B7355",
    "accent": "#C1440E",
    "background": "#FAF7F2",
    "text": "#2C2C2C",
    "text_reversed": "#FAF7F2",
    "muted": "#9B9B9B",
    "border": "#E0D5C5"
  },
  "typography": {
    "header_font": "Playfair Display, Georgia, serif",
    "body_font": "Source Sans Pro, Calibri, sans-serif",
    "title_size": "52px",
    "header_size": "28px",
    "body_size": "17px",
    "caption_size": "13px",
    "line_height": "1.7"
  },
  "spacing": {
    "margin": "80px",
    "gap": "40px",
    "density": "spacious"
  },
  "motif": "editorial-columns",
  "background_modes": ["light", "colored", "reversed"]
}
```

**Step 5: Write creative-pop.json**

```json
{
  "name": "creative-pop",
  "display_name": "Creative Pop",
  "description": "TED talk energy with bold colors and oversized typography",
  "colors": {
    "primary": "#E8175D",
    "secondary": "#474787",
    "accent": "#F7B731",
    "background": "#FFFFFF",
    "text": "#2C3A47",
    "text_reversed": "#FFFFFF",
    "muted": "#778CA3",
    "border": "#D1D8E0"
  },
  "typography": {
    "header_font": "Poppins, Arial Black, sans-serif",
    "body_font": "Open Sans, Calibri, sans-serif",
    "title_size": "60px",
    "header_size": "36px",
    "body_size": "18px",
    "caption_size": "14px",
    "line_height": "1.6"
  },
  "spacing": {
    "margin": "60px",
    "gap": "30px",
    "density": "comfortable"
  },
  "motif": "geometric-shapes",
  "background_modes": ["light", "colored", "reversed"]
}
```

**Step 6: Write data-story.json**

```json
{
  "name": "data-story",
  "display_name": "Data Story",
  "description": "Analytics-focused presentation with cool grays and data accent colors",
  "colors": {
    "primary": "#2D3748",
    "secondary": "#4A5568",
    "accent": "#3182CE",
    "background": "#F7FAFC",
    "text": "#1A202C",
    "text_reversed": "#F7FAFC",
    "muted": "#A0AEC0",
    "border": "#E2E8F0"
  },
  "typography": {
    "header_font": "IBM Plex Sans, Roboto, sans-serif",
    "body_font": "IBM Plex Sans, Roboto, sans-serif",
    "title_size": "44px",
    "header_size": "24px",
    "body_size": "16px",
    "caption_size": "12px",
    "line_height": "1.5"
  },
  "spacing": {
    "margin": "64px",
    "gap": "32px",
    "density": "compact"
  },
  "motif": "data-grid-lines",
  "background_modes": ["light", "colored", "reversed"]
}
```

**Step 7: Validate all themes parse as valid JSON**

Run: `for f in themes/*.json; do echo "$f:"; python3 -c "import json; json.load(open('$f')); print('  VALID')" 2>&1; done`
Expected: All 7 files (6 themes + schema) report VALID

**Step 8: Commit**

```bash
git add themes/
git commit -m "feat: add 6 starter themes with schema"
```

---

## Phase 3: Template System Foundation

### Task 5: Create the template registry schema and index

**Files:**
- Create: `templates/schema.json`
- Create: `templates/index.json`

**Step 1: Write template schema**

Each template entry in the registry describes its purpose, layout, and treatment.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Template Registry Entry",
  "type": "object",
  "required": ["id", "category", "layout", "treatment", "file", "description"],
  "properties": {
    "id": { "type": "string", "description": "Unique template ID: category-layout-treatment" },
    "category": {
      "type": "string",
      "enum": ["title", "content", "data", "image", "comparison", "timeline", "quote", "team", "structural", "closing"]
    },
    "layout": { "type": "string", "description": "Layout variant name" },
    "treatment": {
      "type": "string",
      "enum": ["light", "colored", "reversed"]
    },
    "file": { "type": "string", "description": "Relative path to HTML template file" },
    "description": { "type": "string" },
    "tags": { "type": "array", "items": { "type": "string" } },
    "slots": {
      "type": "object",
      "description": "Content slots this template accepts",
      "properties": {
        "title": { "type": "boolean" },
        "subtitle": { "type": "boolean" },
        "body": { "type": "boolean" },
        "image": { "type": "boolean" },
        "icon_grid": { "type": "boolean" },
        "stats": { "type": "boolean" },
        "table": { "type": "boolean" },
        "timeline": { "type": "boolean" },
        "quote": { "type": "boolean" },
        "speaker_notes": { "type": "boolean" }
      }
    }
  }
}
```

**Step 2: Write initial index.json with first category (title slides)**

Start with the 8 title slide layouts x 3 treatments = 24 entries. We'll add the remaining categories in subsequent tasks.

```json
{
  "$schema": "./schema.json",
  "version": "0.1.0",
  "templates": [
    {
      "id": "title-centered-hero-light",
      "category": "title",
      "layout": "centered-hero",
      "treatment": "light",
      "file": "title/centered-hero-light.html",
      "description": "Centered title and subtitle on clean white background",
      "tags": ["minimal", "clean", "hero"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-centered-hero-colored",
      "category": "title",
      "layout": "centered-hero",
      "treatment": "colored",
      "file": "title/centered-hero-colored.html",
      "description": "Centered title on theme-colored background",
      "tags": ["bold", "colored", "hero"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-centered-hero-reversed",
      "category": "title",
      "layout": "centered-hero",
      "treatment": "reversed",
      "file": "title/centered-hero-reversed.html",
      "description": "Centered title with light text on dark background",
      "tags": ["dark", "dramatic", "hero"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-split-image-light",
      "category": "title",
      "layout": "split-image",
      "treatment": "light",
      "file": "title/split-image-light.html",
      "description": "Title text left, full-height image right, light background",
      "tags": ["split", "image", "balanced"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-split-image-colored",
      "category": "title",
      "layout": "split-image",
      "treatment": "colored",
      "file": "title/split-image-colored.html",
      "description": "Title on colored panel left, image right",
      "tags": ["split", "image", "colored"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-split-image-reversed",
      "category": "title",
      "layout": "split-image",
      "treatment": "reversed",
      "file": "title/split-image-reversed.html",
      "description": "Title with light text on dark panel left, image right",
      "tags": ["split", "image", "dark"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-full-bleed-photo-light",
      "category": "title",
      "layout": "full-bleed-photo",
      "treatment": "light",
      "file": "title/full-bleed-photo-light.html",
      "description": "Full-screen photo with light overlay and title text",
      "tags": ["photo", "immersive", "overlay"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-full-bleed-photo-colored",
      "category": "title",
      "layout": "full-bleed-photo",
      "treatment": "colored",
      "file": "title/full-bleed-photo-colored.html",
      "description": "Full-screen photo with colored gradient overlay",
      "tags": ["photo", "gradient", "immersive"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-full-bleed-photo-reversed",
      "category": "title",
      "layout": "full-bleed-photo",
      "treatment": "reversed",
      "file": "title/full-bleed-photo-reversed.html",
      "description": "Full-screen photo with dark overlay and light title text",
      "tags": ["photo", "dark", "cinematic"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-gradient-overlay-light",
      "category": "title",
      "layout": "gradient-overlay",
      "treatment": "light",
      "file": "title/gradient-overlay-light.html",
      "description": "Subtle gradient background with centered title",
      "tags": ["gradient", "subtle", "modern"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-gradient-overlay-colored",
      "category": "title",
      "layout": "gradient-overlay",
      "treatment": "colored",
      "file": "title/gradient-overlay-colored.html",
      "description": "Bold gradient using theme colors with title",
      "tags": ["gradient", "bold", "vibrant"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-gradient-overlay-reversed",
      "category": "title",
      "layout": "gradient-overlay",
      "treatment": "reversed",
      "file": "title/gradient-overlay-reversed.html",
      "description": "Dark gradient with light title text",
      "tags": ["gradient", "dark", "dramatic"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-logo-focused-light",
      "category": "title",
      "layout": "logo-focused",
      "treatment": "light",
      "file": "title/logo-focused-light.html",
      "description": "Large centered logo with title below on white",
      "tags": ["logo", "brand", "corporate"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-logo-focused-colored",
      "category": "title",
      "layout": "logo-focused",
      "treatment": "colored",
      "file": "title/logo-focused-colored.html",
      "description": "Large centered logo on colored background",
      "tags": ["logo", "brand", "colored"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-logo-focused-reversed",
      "category": "title",
      "layout": "logo-focused",
      "treatment": "reversed",
      "file": "title/logo-focused-reversed.html",
      "description": "Large centered logo on dark background",
      "tags": ["logo", "brand", "dark"],
      "slots": { "title": true, "subtitle": true, "image": true }
    },
    {
      "id": "title-minimal-text-light",
      "category": "title",
      "layout": "minimal-text",
      "treatment": "light",
      "file": "title/minimal-text-light.html",
      "description": "Just the title, maximum whitespace, no subtitle",
      "tags": ["minimal", "bold-text", "statement"],
      "slots": { "title": true }
    },
    {
      "id": "title-minimal-text-colored",
      "category": "title",
      "layout": "minimal-text",
      "treatment": "colored",
      "file": "title/minimal-text-colored.html",
      "description": "Bold title on colored background, nothing else",
      "tags": ["minimal", "bold-text", "colored"],
      "slots": { "title": true }
    },
    {
      "id": "title-minimal-text-reversed",
      "category": "title",
      "layout": "minimal-text",
      "treatment": "reversed",
      "file": "title/minimal-text-reversed.html",
      "description": "Bold light title on dark background, maximum impact",
      "tags": ["minimal", "bold-text", "dark"],
      "slots": { "title": true }
    },
    {
      "id": "title-asymmetric-light",
      "category": "title",
      "layout": "asymmetric",
      "treatment": "light",
      "file": "title/asymmetric-light.html",
      "description": "Off-center title with decorative element, light background",
      "tags": ["creative", "asymmetric", "dynamic"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-asymmetric-colored",
      "category": "title",
      "layout": "asymmetric",
      "treatment": "colored",
      "file": "title/asymmetric-colored.html",
      "description": "Off-center title with geometric accent on colored bg",
      "tags": ["creative", "asymmetric", "colored"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-asymmetric-reversed",
      "category": "title",
      "layout": "asymmetric",
      "treatment": "reversed",
      "file": "title/asymmetric-reversed.html",
      "description": "Off-center title with accent shape on dark background",
      "tags": ["creative", "asymmetric", "dark"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-editorial-spread-light",
      "category": "title",
      "layout": "editorial-spread",
      "treatment": "light",
      "file": "title/editorial-spread-light.html",
      "description": "Magazine-style title with large serif text and thin rule lines",
      "tags": ["editorial", "magazine", "elegant"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-editorial-spread-colored",
      "category": "title",
      "layout": "editorial-spread",
      "treatment": "colored",
      "file": "title/editorial-spread-colored.html",
      "description": "Magazine-style title on warm tinted background",
      "tags": ["editorial", "magazine", "tinted"],
      "slots": { "title": true, "subtitle": true }
    },
    {
      "id": "title-editorial-spread-reversed",
      "category": "title",
      "layout": "editorial-spread",
      "treatment": "reversed",
      "file": "title/editorial-spread-reversed.html",
      "description": "Magazine-style title with light text on dark background",
      "tags": ["editorial", "magazine", "dark"],
      "slots": { "title": true, "subtitle": true }
    }
  ]
}
```

**Step 3: Validate JSON**

Run: `python3 -c "import json; d=json.load(open('templates/index.json')); print(f'{len(d[\"templates\"])} templates registered'); assert len(d['templates']) == 24"`
Expected: `24 templates registered`

**Step 4: Commit**

```bash
git add templates/schema.json templates/index.json
git commit -m "feat: add template registry schema and 24 title slide entries"
```

---

### Task 6: Create the base HTML template wrapper

**Files:**
- Create: `templates/base.html`

**Step 1: Write the base slide wrapper**

This is the HTML shell every template slide renders inside. It loads Tailwind via CDN and sets CSS custom properties from the theme.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920, height=1080, initial-scale=1">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    :root {
      /* Theme colors — injected by orchestrator */
      --color-primary: {{colors.primary}};
      --color-secondary: {{colors.secondary}};
      --color-accent: {{colors.accent}};
      --color-background: {{colors.background}};
      --color-text: {{colors.text}};
      --color-text-reversed: {{colors.text_reversed}};
      --color-muted: {{colors.muted}};
      --color-border: {{colors.border}};

      /* Typography */
      --font-header: {{typography.header_font}};
      --font-body: {{typography.body_font}};
      --size-title: {{typography.title_size}};
      --size-header: {{typography.header_size}};
      --size-body: {{typography.body_size}};
      --size-caption: {{typography.caption_size}};
      --line-height: {{typography.line_height}};

      /* Spacing */
      --margin: {{spacing.margin}};
      --gap: {{spacing.gap}};
    }

    @page {
      size: 1920px 1080px;
      margin: 0;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      font-family: var(--font-body);
      font-size: var(--size-body);
      line-height: var(--line-height);
      color: var(--color-text);
      background-color: var(--color-background);
    }

    .slide {
      width: 1920px;
      height: 1080px;
      padding: var(--margin);
      position: relative;
      display: flex;
      flex-direction: column;
    }

    h1, h2, h3, h4, h5, h6 {
      font-family: var(--font-header);
    }

    .page-number {
      position: absolute;
      bottom: 24px;
      right: 40px;
      font-size: var(--size-caption);
      color: var(--color-muted);
    }

    .logo {
      position: absolute;
      top: 24px;
      right: 40px;
      max-height: 48px;
      width: auto;
    }
  </style>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            'theme-primary': 'var(--color-primary)',
            'theme-secondary': 'var(--color-secondary)',
            'theme-accent': 'var(--color-accent)',
            'theme-bg': 'var(--color-background)',
            'theme-text': 'var(--color-text)',
            'theme-text-rev': 'var(--color-text-reversed)',
            'theme-muted': 'var(--color-muted)',
            'theme-border': 'var(--color-border)',
          },
          fontFamily: {
            'header': 'var(--font-header)',
            'body': 'var(--font-body)',
          }
        }
      }
    }
  </script>
</head>
<body>
  <!-- SLIDE CONTENT INJECTED HERE -->
  {{slide_content}}
</body>
</html>
```

**Step 2: Commit**

```bash
git add templates/base.html
git commit -m "feat: add base HTML template wrapper with theme CSS variables"
```

---

### Task 7: Build exemplar title slide templates (all 8 layouts, light treatment)

**Files:**
- Create: `templates/title/centered-hero-light.html`
- Create: `templates/title/split-image-light.html`
- Create: `templates/title/full-bleed-photo-light.html`
- Create: `templates/title/gradient-overlay-light.html`
- Create: `templates/title/logo-focused-light.html`
- Create: `templates/title/minimal-text-light.html`
- Create: `templates/title/asymmetric-light.html`
- Create: `templates/title/editorial-spread-light.html`

These are the 8 "light" treatment title templates. Each is a `<div class="slide">` fragment that goes inside base.html. The "colored" and "reversed" treatments in Task 8 are variations of these with different background/text colors.

**Step 1: Write centered-hero-light.html**

```html
<!-- Template: title-centered-hero-light -->
<!-- Slots: title, subtitle -->
<div class="slide items-center justify-center text-center">
  <h1 style="font-size: var(--size-title); font-weight: 700; letter-spacing: -0.02em; max-width: 1400px;">
    {{title}}
  </h1>
  <p style="font-size: var(--size-header); color: var(--color-muted); margin-top: var(--gap); max-width: 1000px;">
    {{subtitle}}
  </p>
</div>
```

**Step 2: Write split-image-light.html**

```html
<!-- Template: title-split-image-light -->
<!-- Slots: title, subtitle, image -->
<div class="slide !p-0 flex-row">
  <div class="flex flex-col justify-center" style="width: 50%; padding: var(--margin);">
    <h1 style="font-size: var(--size-title); font-weight: 700; letter-spacing: -0.02em;">
      {{title}}
    </h1>
    <p style="font-size: var(--size-header); color: var(--color-muted); margin-top: var(--gap);">
      {{subtitle}}
    </p>
  </div>
  <div style="width: 50%; overflow: hidden;">
    <img src="{{image}}" alt="" style="width: 100%; height: 100%; object-fit: cover;">
  </div>
</div>
```

**Step 3: Write full-bleed-photo-light.html**

```html
<!-- Template: title-full-bleed-photo-light -->
<!-- Slots: title, subtitle, image -->
<div class="slide !p-0 items-center justify-center text-center" style="position: relative;">
  <img src="{{image}}" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.3;">
  <div style="position: relative; z-index: 10; max-width: 1200px; padding: var(--margin);">
    <h1 style="font-size: var(--size-title); font-weight: 700; letter-spacing: -0.02em;">
      {{title}}
    </h1>
    <p style="font-size: var(--size-header); color: var(--color-muted); margin-top: var(--gap);">
      {{subtitle}}
    </p>
  </div>
</div>
```

**Step 4: Write gradient-overlay-light.html**

```html
<!-- Template: title-gradient-overlay-light -->
<!-- Slots: title, subtitle -->
<div class="slide items-center justify-center text-center"
     style="background: linear-gradient(135deg, var(--color-background) 0%, var(--color-secondary) 100%);">
  <h1 style="font-size: var(--size-title); font-weight: 700; letter-spacing: -0.02em; max-width: 1400px;">
    {{title}}
  </h1>
  <p style="font-size: var(--size-header); color: var(--color-muted); margin-top: var(--gap); max-width: 1000px;">
    {{subtitle}}
  </p>
</div>
```

**Step 5: Write logo-focused-light.html**

```html
<!-- Template: title-logo-focused-light -->
<!-- Slots: title, subtitle, image (logo) -->
<div class="slide items-center justify-center text-center" style="gap: var(--gap);">
  <img src="{{image}}" alt="Logo" style="max-height: 200px; max-width: 400px; object-fit: contain;">
  <h1 style="font-size: var(--size-title); font-weight: 700; letter-spacing: -0.02em; max-width: 1200px;">
    {{title}}
  </h1>
  <p style="font-size: var(--size-header); color: var(--color-muted); max-width: 900px;">
    {{subtitle}}
  </p>
</div>
```

**Step 6: Write minimal-text-light.html**

```html
<!-- Template: title-minimal-text-light -->
<!-- Slots: title -->
<div class="slide items-center justify-center">
  <h1 style="font-size: calc(var(--size-title) * 1.4); font-weight: 800; letter-spacing: -0.03em; max-width: 1400px; text-align: center;">
    {{title}}
  </h1>
</div>
```

**Step 7: Write asymmetric-light.html**

```html
<!-- Template: title-asymmetric-light -->
<!-- Slots: title, subtitle -->
<div class="slide !p-0 flex-row" style="position: relative;">
  <div style="position: absolute; right: 0; top: 0; width: 40%; height: 100%; background: var(--color-secondary); opacity: 0.3;"></div>
  <div class="flex flex-col justify-end" style="padding: var(--margin); padding-bottom: 120px; width: 65%; position: relative; z-index: 10;">
    <h1 style="font-size: var(--size-title); font-weight: 700; letter-spacing: -0.02em;">
      {{title}}
    </h1>
    <p style="font-size: var(--size-header); color: var(--color-muted); margin-top: calc(var(--gap) * 0.5);">
      {{subtitle}}
    </p>
  </div>
</div>
```

**Step 8: Write editorial-spread-light.html**

```html
<!-- Template: title-editorial-spread-light -->
<!-- Slots: title, subtitle -->
<div class="slide items-start justify-center" style="padding-left: calc(var(--margin) * 1.5);">
  <div style="border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border); padding: var(--gap) 0; max-width: 1200px;">
    <h1 style="font-size: var(--size-title); font-weight: 400; font-style: italic; letter-spacing: -0.01em; font-family: var(--font-header);">
      {{title}}
    </h1>
    <p style="font-size: var(--size-body); color: var(--color-muted); margin-top: var(--gap); text-transform: uppercase; letter-spacing: 0.15em;">
      {{subtitle}}
    </p>
  </div>
</div>
```

**Step 9: Verify all 8 files exist**

Run: `ls templates/title/*-light.html | wc -l`
Expected: `8`

**Step 10: Commit**

```bash
git add templates/title/
git commit -m "feat: add 8 title slide light-treatment templates"
```

---

### Task 8: Generate colored and reversed title slide treatments

**Files:**
- Create: `templates/title/*-colored.html` (8 files)
- Create: `templates/title/*-reversed.html` (8 files)

Each treatment is a variation of the light template:
- **Colored**: Replace `background-color` with `var(--color-secondary)`, keep dark text
- **Reversed**: Replace `background-color` with `var(--color-primary)`, swap text to `var(--color-text-reversed)`, swap muted to `rgba(255,255,255,0.6)`

**Step 1: Create a generation script**

Create `scripts/generate-treatments.py` that reads each `*-light.html` template and generates the colored and reversed variants by making the appropriate CSS variable swaps.

```python
#!/usr/bin/env python3
"""Generate colored and reversed treatment variants from light templates."""
import os
import re
import sys

def make_colored(html):
    """Colored treatment: secondary background, keep dark text."""
    # Add background color to the slide div
    html = html.replace(
        'Template: title-',
        'Template: title-'
    )
    # Replace light treatment reference
    html = re.sub(r'(Template: \S+)-light', r'\1-colored', html)
    # For slides without explicit background, add one to .slide
    if 'background' not in html.split('class="slide')[1].split('>')[0]:
        html = html.replace(
            'class="slide',
            'class="slide" style="background-color: var(--color-secondary);',
            1
        ).replace('" style="', '; ', 1) if 'style="' in html.split('class="slide')[1].split('>')[0] else html.replace(
            'class="slide',
            'class="slide',
            1
        )
    return html

def make_reversed(html):
    """Reversed treatment: primary dark background, light text."""
    html = re.sub(r'(Template: \S+)-light', r'\1-reversed', html)
    # Swap text colors
    html = html.replace('var(--color-text)', 'var(--color-text-reversed)')
    html = html.replace('var(--color-muted)', 'rgba(255,255,255,0.6)')
    # Add dark background
    html = html.replace('var(--color-background)', 'var(--color-primary)')
    return html

def process_directory(template_dir):
    light_files = [f for f in os.listdir(template_dir) if f.endswith('-light.html')]
    for filename in light_files:
        filepath = os.path.join(template_dir, filename)
        with open(filepath) as f:
            light_html = f.read()

        # Generate colored
        colored_name = filename.replace('-light.html', '-colored.html')
        with open(os.path.join(template_dir, colored_name), 'w') as f:
            f.write(make_colored(light_html))
        print(f"  Created {colored_name}")

        # Generate reversed
        reversed_name = filename.replace('-light.html', '-reversed.html')
        with open(os.path.join(template_dir, reversed_name), 'w') as f:
            f.write(make_reversed(light_html))
        print(f"  Created {reversed_name}")

if __name__ == '__main__':
    dirs = sys.argv[1:] if len(sys.argv) > 1 else ['templates/title']
    for d in dirs:
        print(f"Processing {d}/")
        process_directory(d)
```

**Step 2: Run the generator**

Run: `python3 scripts/generate-treatments.py templates/title`
Expected: 16 new files created (8 colored + 8 reversed)

**Step 3: Verify all 24 title templates exist**

Run: `ls templates/title/*.html | wc -l`
Expected: `24`

**Step 4: Commit**

```bash
git add scripts/generate-treatments.py templates/title/
git commit -m "feat: add treatment generator and complete 24 title slide templates"
```

---

### Task 9: Build content slide templates (12 layouts x 3 treatments = 36)

**Files:**
- Create: `templates/content/*.html` (36 files)
- Modify: `templates/index.json` (add 36 entries)

Follow the same pattern as title slides:
1. Write 12 light-treatment layouts
2. Run `generate-treatments.py` for colored/reversed variants
3. Add entries to index.json

**Content slide layouts (12):**

| Layout | Description |
|--------|-------------|
| `single-column` | Full-width body text with title |
| `two-column` | Content split into two equal columns |
| `three-column` | Content in three columns |
| `icon-grid-2x2` | 4 items with icon + title + description |
| `icon-grid-2x3` | 6 items with icon + title + description |
| `icon-grid-3x3` | 9 items with icon + brief label |
| `numbered-list` | Numbered items with descriptions |
| `card-layout` | Content in rounded card containers |
| `magazine-flow` | Editorial-style flowing text with pull quote |
| `sidebar-content` | Narrow sidebar + wide content area |
| `text-image-left` | Image left, text right |
| `text-image-right` | Text left, image right |

**Step 1: Write each light-treatment template** (follow the pattern from title slides — each is a `<div class="slide">` fragment using CSS variables)

**Step 2: Run treatment generator**

Run: `python3 scripts/generate-treatments.py templates/content`

**Step 3: Add all 36 entries to index.json**

**Step 4: Verify**

Run: `ls templates/content/*.html | wc -l`
Expected: `36`

**Step 5: Commit**

```bash
git add templates/content/ templates/index.json
git commit -m "feat: add 36 content slide templates (12 layouts x 3 treatments)"
```

---

### Task 10: Build remaining template categories

Repeat the Task 9 pattern for each remaining category. Each task follows:
1. Write light-treatment layouts
2. Generate colored/reversed variants
3. Add to index.json
4. Verify count
5. Commit

**Categories to build:**

| Category | Layouts | Templates | Key features |
|----------|---------|-----------|-------------|
| `data` | 8 | 24 | Big stat callouts, metric grids, chart placeholders |
| `image` | 8 | 24 | Full-bleed, half-bleed, gallery grid, caption styles |
| `comparison` | 6 | 18 | Before/after, pros/cons, side-by-side options |
| `timeline` | 6 | 18 | Horizontal, vertical, milestone markers, branching |
| `quote` | 5 | 15 | Large quote, attribution, decorative marks |
| `team` | 5 | 15 | Profile cards, headshot grids, role descriptions |
| `structural` | 6 | 18 | Section divider, TOC/agenda, chapter markers |
| `closing` | 5 | 15 | CTA, contact info, thank you, QR code, social links |

**For each category, commit separately:**

```bash
git add templates/<category>/ templates/index.json
git commit -m "feat: add <N> <category> slide templates (<L> layouts x 3 treatments)"
```

**Step final: Verify total template count**

Run: `python3 -c "import json; d=json.load(open('templates/index.json')); print(f'{len(d[\"templates\"])} total templates')"`
Expected: `207`

---

## Phase 4: Component Library

### Task 11: Create HTML component snippets

**Files:**
- Create: `components/icons.html`
- Create: `components/boxes.html`
- Create: `components/grids.html`
- Create: `components/page-numbers.html`
- Create: `components/logos.html`
- Create: `components/dividers.html`

Each component file contains multiple reusable HTML snippet patterns that agents can reference when building slides.

**Step 1: Write icons.html** — Icon-in-circle patterns, icon + label combos, icon grid helpers

**Step 2: Write boxes.html** — Card containers, callout boxes, bordered panels, highlighted blocks

**Step 3: Write grids.html** — CSS grid helpers for 2-col, 3-col, 4-col, 2x2, 2x3, 3x3

**Step 4: Write page-numbers.html** — Bottom-right, bottom-center, styled number, fraction (3/10)

**Step 5: Write logos.html** — Top-right, top-left, bottom-center, watermark placements

**Step 6: Write dividers.html** — Thin rule, thick accent, gradient fade, dotted

**Step 7: Commit**

```bash
git add components/
git commit -m "feat: add reusable HTML component library"
```

---

## Phase 5: Agent Definitions

### Task 12: Create orchestrator agent

**Files:**
- Create: `agents/orchestrator.md`

The orchestrator is the conductor — it manages the full workflow, dispatches subagents, and assembles output.

```markdown
---
description: Orchestrates the full presentation creation workflow. Dispatches parallel subagents for slide design, manages QA pipeline, and assembles final output. Use this agent when creating or redesigning a complete presentation.
capabilities:
  - Parse and analyze input files (PPTX, PDF, markdown, natural language)
  - Plan slide structure and assign templates
  - Dispatch parallel slide designer agents
  - Identify content needing specialized agents (tables, timelines, infographics)
  - Manage the playground interaction loop
  - Coordinate Art Director review and Graphics Polisher pass
  - Trigger exports to PDF, PPTX, and Figma
---

# Orchestrator Agent

You are the conductor of the presentation design pipeline. You manage the full workflow from input to export.

## Workflow

### Step 1: Analyze Input
...
[Full orchestrator instructions with step-by-step workflow, dispatch patterns, context injection strategy for each subagent, and error handling]
```

**Step 1: Write the complete orchestrator agent definition** — Include the full 7-step workflow, subagent dispatch patterns, context packaging for each agent type, and assembly logic.

**Step 2: Commit**

```bash
git add agents/orchestrator.md
git commit -m "feat: add orchestrator agent definition"
```

---

### Task 13: Create slide-designer agent

**Files:**
- Create: `agents/slide-designer.md`

```markdown
---
description: Designs individual slide HTML from content data and a template. Receives one slide's content, the active theme, 2-3 relevant templates, and optional brand profile. Outputs a complete HTML slide fragment. This agent is parallelized — one instance per slide.
capabilities:
  - Generate magazine-quality HTML+Tailwind slide fragments
  - Apply theme CSS variables for consistent styling
  - Adapt content to template layouts with dynamic resizing
  - Respect brand profile constraints when provided
---

# Slide Designer Agent

You design one slide at a time. You receive:
- **Slide content**: title, body, images, data, speaker notes
- **Theme**: CSS variables and design tokens
- **Templates**: 2-3 relevant template HTML files to use as starting points
- **Brand profile** (optional): Constraints that override theme defaults

## Design Principles
...
```

**Step 1: Write the complete slide-designer agent** — Template selection logic, content adaptation rules, dynamic resizing behavior, CSS variable usage patterns.

**Step 2: Commit**

```bash
git add agents/slide-designer.md
git commit -m "feat: add slide-designer agent definition"
```

---

### Task 14: Create remaining 8 agents

**Files:**
- Create: `agents/copy-editor.md`
- Create: `agents/image-director.md`
- Create: `agents/table-designer.md`
- Create: `agents/timeline-agent.md`
- Create: `agents/infographic-agent.md`
- Create: `agents/playground-agent.md`
- Create: `agents/art-director.md`
- Create: `agents/graphics-polisher.md`

Each agent follows the same format: YAML frontmatter with description + capabilities, then detailed instructions.

**Key agent details:**

**copy-editor.md** — Focus on: headline rewriting, prose tightening, voice consistency, brand voice adherence. On-demand callable.

**image-director.md** — Three modes: art direction (define visual direction for deck), image sourcing (Unsplash/Pexels queries), image-gen prompts (Midjourney/DALL-E/nano banana prompt writing). Include example prompts for different slide contexts.

**table-designer.md** — Specialized in: alternating row colors, header treatments, cell padding, accent borders, responsive sizing. Reference `components/grids.html` patterns.

**timeline-agent.md** — Horizontal and vertical timelines, milestone markers, branching paths, numbered steps, icon integration.

**infographic-agent.md** — Big stat callouts (60-72pt numbers), icon grids, metric dashboards, comparison charts, percentage bars. Reference `templates/data/` patterns.

**playground-agent.md** — Manages the interactive playground: template gallery navigation, config panel state, chat-driven iteration. Can dispatch Copy Editor or Image Director on demand.

**art-director.md** — Visual QA checklist: alignment, contrast ratios, spacing consistency, text overflow, element overlap, margin compliance, readability. Uses slide screenshots for review.

**graphics-polisher.md** — Final pass: spacing normalization, alignment fixes, motif consistency, visual coherence across all slides. Receives Art Director feedback as input.

**Step 1: Write each agent definition with complete instructions**

**Step 2: Verify all 10 agents exist**

Run: `ls agents/*.md | wc -l`
Expected: `10`

**Step 3: Commit per agent or batch**

```bash
git add agents/
git commit -m "feat: add all 10 agent definitions"
```

---

## Phase 6: Skill Definitions

### Task 15: Create orchestrator entry-point skill

**Files:**
- Create: `skills/presentation/SKILL.md`

This is the main entry point — the skill that Claude auto-activates when a user wants to create a presentation.

```markdown
---
name: Sexy Presentation
description: Create magazine-quality presentations with 200+ templates, parallel subagents, and interactive playground. Use this skill when the user wants to create, redesign, or export a presentation.
version: 0.1.0
---

# Sexy Presentation

## When to Activate

Activate when the user:
- Wants to create a new presentation
- Wants to redesign an existing PPTX or PDF
- Mentions slides, deck, presentation, pitch deck, keynote
- Provides a file that looks like presentation content

## Workflow

1. **Determine input type** — file upload, markdown, or natural language description
2. **Invoke analyze-input skill** to parse the input
3. **Invoke select-theme skill** to choose a visual theme
4. **Check for brand profile** — look for brand-profile.json in the project
5. **Dispatch orchestrator agent** to manage the full pipeline
6. **Present playground** for user iteration
7. **Export** to requested formats

## Available Agents

Reference agents at: `CLAUDE_PLUGIN_ROOT/agents/`

- `orchestrator.md` — Full pipeline conductor
- `slide-designer.md` — Individual slide HTML (parallelizable)
- `copy-editor.md` — Text cleanup (on-demand)
- `image-director.md` — Art direction + image sourcing + gen prompts
- `table-designer.md` — Beautiful tables
- `timeline-agent.md` — Timeline visualizations
- `infographic-agent.md` — Data viz and infographics
- `playground-agent.md` — Interactive playground management
- `art-director.md` — Visual QA review
- `graphics-polisher.md` — Final consistency pass
...
```

**Step 1: Write the complete presentation skill**

**Step 2: Commit**

```bash
git add skills/presentation/SKILL.md
git commit -m "feat: add main presentation skill entry point"
```

---

### Task 16: Create all supporting skills

**Files:**
- Create: `skills/analyze-input/SKILL.md`
- Create: `skills/plan-slides/SKILL.md`
- Create: `skills/design-slide/SKILL.md`
- Create: `skills/select-theme/SKILL.md`
- Create: `skills/source-imagery/SKILL.md`
- Create: `skills/brand-profile/SKILL.md`
- Create: `skills/playground/SKILL.md`
- Create: `skills/export/SKILL.md`
- Create: `skills/qa-art-director/SKILL.md`
- Create: `skills/polish-graphics/SKILL.md`

Each skill has YAML frontmatter with `name`, `description`, `version` and detailed instructions.

**Key skill details:**

**analyze-input** — Instructions for parsing PPTX (python-pptx → markitdown fallback), PDF (PyMuPDF → pdftotext fallback), markdown (direct), natural language (Claude analysis). Output: Slide Data JSON.

**plan-slides** — Takes Slide Data, decides slide count, assigns template categories, identifies specialized content (tables → table-designer, timelines → timeline-agent, data → infographic-agent).

**design-slide** — Instructions for a single slide: receive content + theme + templates, generate HTML fragment, apply CSS variables, handle dynamic resizing.

**select-theme** — Present available themes to user, allow customization, generate CSS variable block. Reference `CLAUDE_PLUGIN_ROOT/themes/`.

**source-imagery** — Three modes: art direction brief, Unsplash/Pexels search (reference `scripts/fetch-images.js`), AI image-gen prompt writing.

**brand-profile** — Extract brand guidelines from PDF/URL/description into `brand-profile.json`. Schema validation against design doc spec.

**playground** — Generate the interactive playground HTML from `CLAUDE_PLUGIN_ROOT/playground/playground-template.html`. Inject current slides, theme, and template gallery.

**export** — Export instructions for each format: PDF (reference `scripts/export-pdf.js`), PPTX (reference `scripts/export-pptx.js`), Figma (Figma MCP integration).

**qa-art-director** — Visual QA checklist, screenshot generation, issue categorization.

**polish-graphics** — Takes Art Director feedback, applies fixes, final consistency verification.

**Step 1: Write each skill definition**

**Step 2: Verify all 11 skills exist**

Run: `find skills -name "SKILL.md" | wc -l`
Expected: `11`

**Step 3: Commit**

```bash
git add skills/
git commit -m "feat: add all 11 skill definitions"
```

---

## Phase 7: Input Parsing Scripts

### Task 17: Write PPTX parser

**Files:**
- Create: `scripts/parse-pptx.py`
- Create: `scripts/test_parse_pptx.py`

**Step 1: Write the failing test**

```python
"""Tests for PPTX parser."""
import json
import subprocess
import pytest


def test_parse_pptx_outputs_valid_slide_data(tmp_path):
    """Parser should output valid Slide Data JSON."""
    # Create a minimal test PPTX using python-pptx
    from pptx import Presentation
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Test Title"
    slide.placeholders[1].text = "Test Subtitle"
    pptx_path = tmp_path / "test.pptx"
    prs.save(str(pptx_path))

    result = subprocess.run(
        ["python3", "scripts/parse-pptx.py", str(pptx_path)],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "slides" in data
    assert len(data["slides"]) >= 1
    assert data["slides"][0]["title"] == "Test Title"


def test_parse_pptx_handles_missing_file():
    result = subprocess.run(
        ["python3", "scripts/parse-pptx.py", "nonexistent.pptx"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
```

**Step 2: Run test to verify it fails**

Run: `python3 -m pytest scripts/test_parse_pptx.py -v`
Expected: FAIL

**Step 3: Write the parser**

```python
#!/usr/bin/env python3
"""Parse PPTX files into Slide Data JSON format.

Usage: python3 parse-pptx.py <input.pptx>
Output: JSON to stdout

Falls back to markitdown if python-pptx fails.
"""
import json
import sys

def parse_with_pptx(filepath):
    from pptx import Presentation
    prs = Presentation(filepath)
    slides = []
    for slide in prs.slides:
        slide_data = {
            "purpose": "content",
            "title": "",
            "subtitle": "",
            "content_blocks": [],
            "speaker_notes": "",
            "layout_hints": [],
            "images": [],
            "data": None
        }
        for shape in slide.shapes:
            if shape.has_text_frame:
                if shape == slide.shapes.title:
                    slide_data["title"] = shape.text_frame.text
                elif shape.placeholder_format and shape.placeholder_format.idx == 1:
                    slide_data["subtitle"] = shape.text_frame.text
                else:
                    slide_data["content_blocks"].append({
                        "type": "text",
                        "content": shape.text_frame.text
                    })
            if shape.shape_type == 13:  # Picture
                slide_data["images"].append({
                    "description": shape.name,
                    "width": shape.width,
                    "height": shape.height
                })
        if slide.has_notes_slide:
            slide_data["speaker_notes"] = slide.notes_slide.notes_text_frame.text
        # Detect purpose from layout
        layout_name = slide.slide_layout.name.lower()
        if "title" in layout_name:
            slide_data["purpose"] = "title"
        elif "section" in layout_name:
            slide_data["purpose"] = "structural"
        slides.append(slide_data)
    return {"slides": slides}

def parse_with_markitdown(filepath):
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "markitdown", filepath],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"markitdown failed: {result.stderr}")
    # Parse markitdown output into slide data
    slides = []
    current_slide = None
    for line in result.stdout.split("\n"):
        if line.startswith("# "):
            if current_slide:
                slides.append(current_slide)
            current_slide = {
                "purpose": "content",
                "title": line[2:].strip(),
                "subtitle": "",
                "content_blocks": [],
                "speaker_notes": "",
                "layout_hints": [],
                "images": [],
                "data": None
            }
        elif current_slide and line.strip():
            current_slide["content_blocks"].append({
                "type": "text",
                "content": line.strip()
            })
    if current_slide:
        slides.append(current_slide)
    return {"slides": slides}

def main():
    if len(sys.argv) != 2:
        print("Usage: parse-pptx.py <input.pptx>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    import os
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    try:
        data = parse_with_pptx(filepath)
    except Exception as e:
        print(f"python-pptx failed ({e}), trying markitdown...", file=sys.stderr)
        try:
            data = parse_with_markitdown(filepath)
        except Exception as e2:
            print(f"All parsers failed: {e2}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
```

**Step 4: Run tests**

Run: `python3 -m pytest scripts/test_parse_pptx.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add scripts/parse-pptx.py scripts/test_parse_pptx.py
git commit -m "feat: add PPTX parser with fallback to markitdown"
```

---

### Task 18: Write PDF parser

**Files:**
- Create: `scripts/parse-pdf.py`
- Create: `scripts/test_parse_pdf.py`

Same pattern as Task 17: failing test first, then implementation with PyMuPDF primary + pdftotext fallback. Output: Slide Data JSON.

**Step 1: Write failing test**
**Step 2: Run test, verify fail**
**Step 3: Write parser with fallback chain**
**Step 4: Run test, verify pass**
**Step 5: Commit**

```bash
git add scripts/parse-pdf.py scripts/test_parse_pdf.py
git commit -m "feat: add PDF parser with fallback to pdftotext"
```

---

## Phase 8: Export Scripts

### Task 19: Write PDF export script

**Files:**
- Create: `scripts/export-pdf.js`
- Create: `scripts/package.json`

**Step 1: Initialize Node.js project for scripts**

```json
{
  "name": "sexy-presentation-scripts",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "puppeteer": "^23.0.0",
    "pptxgenjs": "^3.12.0"
  }
}
```

**Step 2: Write export-pdf.js**

```javascript
#!/usr/bin/env node
/**
 * Export HTML slides to PDF.
 *
 * Usage: node export-pdf.js <input.html> <output.pdf>
 *
 * Renders each .slide element as a 1920x1080 page.
 */
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function exportPDF(inputPath, outputPath) {
  const absoluteInput = path.resolve(inputPath);
  if (!fs.existsSync(absoluteInput)) {
    console.error(`File not found: ${absoluteInput}`);
    process.exit(1);
  }

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(`file://${absoluteInput}`, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: outputPath,
    width: '1920px',
    height: '1080px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  await browser.close();
  console.log(`PDF exported to ${outputPath}`);
}

const [,, input, output] = process.argv;
if (!input || !output) {
  console.error('Usage: node export-pdf.js <input.html> <output.pdf>');
  process.exit(1);
}
exportPDF(input, output);
```

**Step 3: Install dependencies**

Run: `cd scripts && npm install`

**Step 4: Commit**

```bash
git add scripts/package.json scripts/package-lock.json scripts/export-pdf.js
git commit -m "feat: add PDF export script using Puppeteer"
```

---

### Task 20: Write PPTX export script

**Files:**
- Create: `scripts/export-pptx.js`

Uses pptxgenjs to reconstruct slide layouts from HTML structure into editable PPTX.

**Step 1: Write export-pptx.js** — Reads HTML slide files, parses layout structure, recreates in pptxgenjs with editable text boxes, images, and shapes.

**Step 2: Write basic test** — Create a simple slide HTML, export to PPTX, verify file is valid.

**Step 3: Commit**

```bash
git add scripts/export-pptx.js
git commit -m "feat: add editable PPTX export script using pptxgenjs"
```

---

### Task 21: Write Unsplash image fetch script

**Files:**
- Create: `scripts/fetch-images.js`

**Step 1: Write fetch-images.js**

```javascript
#!/usr/bin/env node
/**
 * Fetch images from Unsplash API.
 *
 * Usage: node fetch-images.js --query "nature landscape" --count 5 --output ./images/
 *
 * Requires UNSPLASH_ACCESS_KEY environment variable.
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

function searchUnsplash(query, count = 5) {
  const key = process.env.UNSPLASH_ACCESS_KEY;
  if (!key) {
    console.error('Set UNSPLASH_ACCESS_KEY environment variable');
    process.exit(1);
  }

  return new Promise((resolve, reject) => {
    const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=${count}&orientation=landscape`;
    const options = { headers: { 'Authorization': `Client-ID ${key}` } };

    https.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const parsed = JSON.parse(data);
        resolve(parsed.results.map(r => ({
          id: r.id,
          url: r.urls.regular,
          download: r.links.download_location,
          description: r.description || r.alt_description,
          credit: `${r.user.name} on Unsplash`
        })));
      });
    }).on('error', reject);
  });
}

// Parse args and run
const args = process.argv.slice(2);
const queryIdx = args.indexOf('--query');
const countIdx = args.indexOf('--count');
const query = queryIdx >= 0 ? args[queryIdx + 1] : args[0];
const count = countIdx >= 0 ? parseInt(args[countIdx + 1]) : 5;

if (!query) {
  console.error('Usage: node fetch-images.js --query "search term" [--count N]');
  process.exit(1);
}

searchUnsplash(query, count).then(results => {
  console.log(JSON.stringify(results, null, 2));
});
```

**Step 2: Commit**

```bash
git add scripts/fetch-images.js
git commit -m "feat: add Unsplash image fetch script"
```

---

## Phase 9: Playground

### Task 22: Build the interactive playground HTML

**Files:**
- Create: `playground/playground-template.html`

The playground is a self-contained HTML file with three panels:
1. **Template Gallery** (left sidebar) — Visual grid of template thumbnails
2. **Live Preview** (center) — Current slide rendered at scale
3. **Config Panel** (right sidebar) — Theme, colors, fonts, layout controls

**Step 1: Write playground-template.html** — Full interactive HTML with:
- Template gallery with category tabs and clickable thumbnails
- Config panel with: theme dropdown, color pickers, font selector, column count, background mode toggle, logo upload, page number style, spacing density
- Live preview area that updates on config changes
- JavaScript for state management and real-time preview updates
- Tailwind CDN for styling the playground UI itself
- Export buttons (triggers export scripts)

**Step 2: Verify it opens in browser**

Run: `open playground/playground-template.html`
Expected: Interactive playground loads with all three panels

**Step 3: Commit**

```bash
git add playground/
git commit -m "feat: add interactive playground template"
```

---

## Phase 10: Brand Profile System

### Task 23: Create brand profile skill and schema

**Files:**
- Create: `skills/brand-profile/SKILL.md`
- Create: `skills/brand-profile/schema.json`

**Step 1: Write brand-profile schema.json** — JSON Schema matching the design doc's brand-profile.json spec (company, colors, typography, logo, imagery, layout_rules).

**Step 2: Write SKILL.md** — Instructions for extracting brand guidelines from PDF/URL/description into the schema. Include:
- How to parse a PDF brand guide
- How to fetch and parse a brand guide URL
- How to interview the user for brand details
- How to validate output against schema
- How the brand profile overrides theme defaults

**Step 3: Commit**

```bash
git add skills/brand-profile/
git commit -m "feat: add brand profile extraction skill and schema"
```

---

## Phase 11: Integration & QA

### Task 24: Create the /presentation command

**Files:**
- Create: `commands/presentation.md`

```markdown
---
name: presentation
description: Create or redesign a magazine-quality presentation with interactive design playground
---

Invoke the `presentation` skill to begin the presentation workflow.

Accept input as:
- A file path to an existing PPTX or PDF
- Markdown content or outline
- A natural language description of what you want

Examples:
- `/presentation redesign quarterly-report.pptx`
- `/presentation create a pitch deck for an AI startup`
- `/presentation` (interactive — will ask what you want to build)
```

**Step 1: Write the command definition**

**Step 2: Commit**

```bash
git add commands/presentation.md
git commit -m "feat: add /presentation slash command"
```

---

### Task 25: End-to-end validation

**Step 1: Verify complete plugin structure**

Run: `find . -type f | grep -v '.git/' | grep -v 'node_modules' | sort`
Expected: All files from the design doc's file structure are present

**Step 2: Verify plugin manifest is valid**

Run: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); print('VALID')"`

**Step 3: Verify all JSON files parse**

Run: `for f in $(find . -name '*.json' | grep -v node_modules | grep -v .git); do echo "$f:"; python3 -c "import json; json.load(open('$f')); print('  VALID')" 2>&1; done`

**Step 4: Verify template count**

Run: `python3 -c "import json; d=json.load(open('templates/index.json')); print(f'{len(d[\"templates\"])} templates')"`
Expected: `207`

**Step 5: Verify agent count**

Run: `ls agents/*.md | wc -l`
Expected: `10`

**Step 6: Verify skill count**

Run: `find skills -name 'SKILL.md' | wc -l`
Expected: `11`

**Step 7: Run Python tests**

Run: `python3 -m pytest scripts/ -v`
Expected: All tests pass

**Step 8: Final commit**

```bash
git add -A
git commit -m "feat: complete plugin integration validation"
```

---

## Summary

| Phase | Tasks | What it produces |
|-------|-------|-----------------|
| 1. Scaffold | 1-2 | Plugin manifest + directory structure |
| 2. Themes | 3-4 | Schema + 6 starter themes |
| 3. Templates | 5-10 | 207+ composable HTML templates + registry |
| 4. Components | 11 | Reusable HTML snippet library |
| 5. Agents | 12-14 | 10 specialized agent definitions |
| 6. Skills | 15-16 | 11 skill definitions |
| 7. Input Parsing | 17-18 | PPTX + PDF parsers with fallbacks |
| 8. Export | 19-21 | PDF, PPTX, and image fetch scripts |
| 9. Playground | 22 | Interactive HTML playground |
| 10. Brand Profile | 23 | Brand guide extraction system |
| 11. Integration | 24-25 | Slash command + end-to-end validation |
