---
name: Playground
description: Generate an interactive HTML playground for live presentation editing. Injects the current slides, theme, and template gallery into the playground template, and supports chat-driven iteration on individual slides.
version: 0.1.0
---

# Playground Skill

## Purpose

Launch an interactive, browser-based playground where the user can visually review all slides, browse the template gallery, switch themes, and request targeted edits through chat — all without rerunning the full pipeline from scratch.

## Playground Template

Base template: `CLAUDE_PLUGIN_ROOT/playground/playground-template.html`

The playground template provides:
- A slide preview panel (scrollable deck view + individual slide zoom)
- A template gallery sidebar (filterable by category)
- A theme switcher panel
- A chat input pane for iteration commands
- An export button row (PDF, PPTX, Figma, HTML)

## Generation Process

### Step 1: Read the Playground Template

Load `CLAUDE_PLUGIN_ROOT/playground/playground-template.html` and locate the following injection points (marked with `<!-- INJECT: ... -->` comments):

```html
<!-- INJECT: SLIDES_DATA -->
<!-- INJECT: THEME_DATA -->
<!-- INJECT: TEMPLATE_GALLERY -->
<!-- INJECT: BRAND_PROFILE -->
```

### Step 2: Inject Current Slides

Serialize the assembled HTML fragments from the `design-slide` step into a JavaScript array and inject at `<!-- INJECT: SLIDES_DATA -->`:

```html
<script id="slides-data" type="application/json">
[
  {
    "index": 0,
    "html": "<section class=\"slide\" ...>...</section>",
    "template_category": "title-slide",
    "template_path": "title-slide/01-centered.html",
    "title": "Slide Title"
  },
  ...
]
</script>
```

### Step 3: Inject Theme Data

Inject the resolved CSS variable block and theme metadata at `<!-- INJECT: THEME_DATA -->`:

```html
<script id="theme-data" type="application/json">
{
  "theme_id": "midnight-bold",
  "theme_name": "Midnight Bold",
  "google_fonts": ["Playfair Display:wght@700;900", "Inter:wght@400;500;600"],
  "css_variables": { "--color-primary": "#1a1a2e", ... }
}
</script>
<style id="active-theme">
  :root { /* resolved CSS variable block */ }
</style>
```

### Step 4: Inject Template Gallery

Enumerate all templates at `CLAUDE_PLUGIN_ROOT/templates/` and inject a gallery manifest at `<!-- INJECT: TEMPLATE_GALLERY -->`:

```html
<script id="template-gallery" type="application/json">
{
  "categories": [
    {
      "id": "title-slide",
      "label": "Title Slide",
      "templates": [
        {
          "id": "title-slide/01-centered",
          "label": "Centered Hero",
          "preview_src": "CLAUDE_PLUGIN_ROOT/templates/title-slide/01-centered/preview.png",
          "html_path": "CLAUDE_PLUGIN_ROOT/templates/title-slide/01-centered.html"
        }
      ]
    }
  ]
}
</script>
```

### Step 5: Inject Brand Profile (if available)

If `brand-profile.json` was generated, inject it at `<!-- INJECT: BRAND_PROFILE -->`:

```html
<script id="brand-profile" type="application/json">
{ /* brand-profile.json contents */ }
</script>
```

### Step 6: Output the Playground File

Write the fully injected HTML to:

```
./output/playground.html
```

Inform the user of the path and instruct them to open it in a browser. The playground is fully self-contained — all slide HTML is inline, and external resources (fonts, scripts) are loaded from CDN.

## Chat-Driven Iteration

The playground includes a chat input pane. When the user types commands into the chat, the playground posts the command to Claude Code (via the skill's message loop), which interprets and executes the appropriate sub-skill.

### Supported Iteration Commands

| User command | Action |
|---|---|
| "Change slide 3 to a two-column layout" | Re-run `design-slide` for slide 3 with new template category |
| "Make the title bigger on slide 1" | Re-run `design-slide` for slide 1 with a `design_notes` override |
| "Switch to the clean-light theme" | Re-run `select-theme`, then re-inject theme data and re-render all slides |
| "Add a new slide after slide 5 about market size" | Re-run `plan-slides` for the new slide, then `design-slide`, then re-inject |
| "Replace the image on slide 4" | Re-run `source-imagery` for slide 4's image slot, then `design-slide` for slide 4 |
| "Apply our brand colors" | Re-run `brand-profile` and re-inject brand overrides, re-render affected slides |
| "Delete slide 7" | Remove slide 7 from the slides array, re-inject |
| "Reorder: move slide 6 before slide 3" | Reorder the slides array, re-inject |
| "Export as PDF" | Trigger `export` skill with format `pdf` |

### Iteration Flow

1. Receive user command in chat input
2. Parse intent and affected slide(s)
3. Re-run the minimum necessary sub-skills (do not re-run the full pipeline)
4. Update only the changed slides in the playground's `slides-data` script block
5. Trigger a playground UI refresh (via `window.playgroundReload()`)
6. Confirm completion in the chat output pane

## Playground UI Features

The generated playground provides the following UI panels (all managed by the template's JavaScript):

### Slide Preview Panel

- Scrollable list of all slide thumbnails (miniature renders)
- Click a thumbnail to expand to full-width preview
- Keyboard navigation (arrow keys) between slides
- Slide index and template name shown below each thumbnail

### Template Gallery Sidebar

- Filterable by category (title slides, content, data, etc.)
- Drag a template onto a slide thumbnail to swap templates
- "Preview with content" — renders the current slide's content in the hovered template

### Theme Switcher Panel

- Dropdown of all available themes
- Live preview — hovering a theme name updates the deck preview in real time
- "Customize" button opens CSS variable editor for fine-tuning individual tokens

### Export Button Row

- PDF, PPTX, Figma, HTML buttons — each triggers the `export` skill with the appropriate format
- "Download playground.html" — saves the current state as a new standalone file

## Notes

- The playground file should not exceed 5MB in total. If slide HTML is large, lazy-load slide fragments via inline data URIs rather than embedding all at once.
- The playground does not require a server — it runs entirely in the browser using in-page JavaScript.
- For presentations with 30+ slides, enable virtual scrolling in the thumbnail strip to maintain performance.
