---
name: Export
description: Export the finalized presentation to PDF, PPTX, Figma, or HTML using dedicated scripts and integrations. Handles format-specific rendering fidelity concerns and returns the exported file path.
version: 0.1.0
---

# Export Skill

## Purpose

Take the assembled, QA-approved presentation HTML and convert it to the user's requested output format. Each format uses a dedicated script or integration to maximize fidelity.

## Supported Export Formats

| Format | Script / Integration | Best For |
|---|---|---|
| PDF | `CLAUDE_PLUGIN_ROOT/scripts/export-pdf.js` | Print, email, universal sharing |
| PPTX | `CLAUDE_PLUGIN_ROOT/scripts/export-pptx.js` | Editable decks, corporate use |
| Figma | Figma MCP integration | Design handoff, further editing |
| HTML | Direct file save | Web embedding, interactive decks |
| Per-slide HTML | Auto-generated alongside any export | Figma import, individual editing |

## Format 1: PDF Export

Reference script: `CLAUDE_PLUGIN_ROOT/scripts/export-pdf.js`

The PDF export script uses a headless browser (Playwright/Puppeteer) to render each slide at full resolution and print to PDF.

### Usage

```bash
node CLAUDE_PLUGIN_ROOT/scripts/export-pdf.js \
  --input ./output/presentation.html \
  --output ./output/presentation.pdf \
  --width 1920 \
  --height 1080 \
  --slides-selector ".slide" \
  --delay 500
```

### Parameters

| Flag | Default | Description |
|---|---|---|
| `--input` | required | Path to the assembled presentation HTML |
| `--output` | `./output/presentation.pdf` | Output PDF path |
| `--width` | `1920` | Viewport width in pixels |
| `--height` | `1080` | Viewport height in pixels |
| `--slides-selector` | `.slide` | CSS selector identifying each slide element |
| `--delay` | `300` | Milliseconds to wait after page load (for fonts/animations) |
| `--print-background` | `true` | Include CSS backgrounds in PDF |
| `--format` | `A4 landscape` | Page format — use `A4 landscape` for 16:9, `A4 portrait` for 4:3 |

### PDF Quality Checklist

Before returning the PDF path, verify:

- [ ] All slides render on separate pages (no slide cut across page boundary)
- [ ] Fonts are embedded (check with `pdffonts output.pdf`)
- [ ] Images are sharp (not pixelated) at 100% zoom
- [ ] Backgrounds and gradients are present (not white-background fallback)
- [ ] Slide numbers are correct and sequential
- [ ] File size is reasonable (flag if > 50MB for a standard deck)

### PDF Accessibility

Add PDF metadata and accessibility tags by passing additional flags:

```bash
node export-pdf.js ... \
  --pdf-title "Presentation Title" \
  --pdf-author "Author Name" \
  --pdf-subject "Presentation subject" \
  --pdf-keywords "keyword1, keyword2"
```

## Format 2: PPTX Export

Reference script: `CLAUDE_PLUGIN_ROOT/scripts/export-pptx.js`

The PPTX export script uses python-pptx to construct a native PowerPoint file from the slide data and HTML design output.

### Usage

```bash
node CLAUDE_PLUGIN_ROOT/scripts/export-pptx.js \
  --slides-json ./output/slide-plan.json \
  --theme-json ./output/theme.json \
  --images-dir ./output/images/ \
  --output ./output/presentation.pptx
```

### PPTX Construction Logic

The script bridges the HTML/CSS design to PowerPoint's XML format:

1. Create a new `Presentation` object with the correct slide dimensions (16:9 = 10in × 5.625in)
2. For each slide in the Slide Plan:
   - Add a new slide using the closest available slide layout
   - Map CSS-styled text boxes to PPTX text frames with matching font, size, and color
   - Insert images as picture shapes at the correct position and size
   - Convert CSS grid/flex layouts to PPTX absolute positioning (x, y, width, height in EMUs)
   - Add speaker notes to the notes placeholder
3. Apply theme colors to the slide master

### PPTX Limitations

PPTX cannot faithfully reproduce all CSS capabilities. Document the following known fidelity gaps to the user:

- CSS gradients → flattened to solid color or gradient stop approximation
- CSS animations/transitions → removed (static output)
- CSS `clip-path` and complex masks → approximated with shapes
- Web fonts → substituted with system fonts if not embedded
- CSS Grid layouts → converted to absolute positioning (may drift slightly)

### PPTX Quality Checklist

- [ ] Correct slide count matches the HTML presentation
- [ ] Titles and body text are editable text frames (not images)
- [ ] Images are actual picture shapes (not HTML canvas renders)
- [ ] Speaker notes are present and readable in Notes view
- [ ] File opens without errors in PowerPoint and Keynote
- [ ] Slide master reflects the theme colors

## Format 3: Figma Export

Integration: Figma MCP (Model Context Protocol)

Use the Figma MCP tool to create a new Figma file containing each slide as a frame.

### Figma MCP Workflow

```
1. Authenticate with Figma MCP
2. Create a new file: "Presentation Title — [date]"
3. Set page dimensions to 1920 × 1080px
4. For each slide:
   a. Create a frame named "Slide [N] — [title]"
   b. Import the slide's layout as a Figma frame (use HTML-to-Figma conversion via MCP)
   c. Set up auto-layout where applicable
   d. Create components for repeated elements (headers, footers, icons)
5. Apply Figma styles matching the theme variables:
   - Color styles for all theme colors
   - Text styles for all font/size combinations
6. Set up a Figma prototype with slide transitions
7. Share the file URL with the user
```

### Figma Export Output

Return:
- The Figma file URL
- A summary of components and styles created
- Instructions for how to edit individual slides

## Format 4: HTML Export

Direct file save — the simplest export format.

### HTML Export Process

1. Take the fully assembled presentation HTML (with all slides inline)
2. Inline all critical CSS (theme variables, slide layout styles) into a `<style>` block
3. Convert all external image URLs to base64 data URIs for full portability
4. Add a minimal presentation shell with keyboard navigation:
   ```javascript
   // Arrow key navigation between slides
   document.addEventListener('keydown', (e) => {
     if (e.key === 'ArrowRight') showSlide(currentIndex + 1);
     if (e.key === 'ArrowLeft') showSlide(currentIndex - 1);
     if (e.key === 'f') document.documentElement.requestFullscreen();
   });
   ```
5. Add a progress bar and slide counter
6. Save to `./output/presentation.html`

### HTML Export Options

- `--include-speaker-notes` — add a speaker notes panel below each slide (toggle with `N` key)
- `--autoplay [seconds]` — auto-advance slides after N seconds
- `--no-controls` — hide the navigation UI (for embedding in iframes)
- `--embed-fonts` — download and base64-encode all Google Fonts for full offline use

## Format 5: Per-Slide HTML Export (Figma-Ready)

Export each slide as a standalone, self-contained HTML page for Figma import and individual editing.

### Output Structure

```
output/
  deck.html              # Full assembled deck (playground, PDF export)
  slides/
    slide-01.html         # Standalone page — own <html>, theme vars, fonts
    slide-02.html
    ...
    slide-N.html
  assets/                 # Shared images referenced by slides
```

### Per-Slide HTML Structure

Each standalone slide file is a complete HTML document:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920, height=1080, initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <!-- Google Fonts links for theme fonts -->
  <style>
    :root { /* Full theme CSS variables inlined */ }
    /* Base slide styles inlined from base.html */
    /* Motif CSS inlined from theme motif file */
    /* Image treatment CSS inlined */
  </style>
</head>
<body>
  <div class="slide" data-index="N" data-intensity="hero|impact|workhorse">
    <!-- Motif DOM elements -->
    <!-- Slide content -->
  </div>
</body>
</html>
```

### Key Requirements

- **Self-contained**: No external CSS or JS dependencies (except Google Fonts CDN)
- **One slide per file**: Each file renders exactly one 1920×1080 slide
- **Motif elements included**: Real DOM elements, not pseudo-elements
- **Image treatments included**: CSS utility classes inlined in the `<style>` block
- **Editable**: A designer can open any file in a browser, edit in DevTools, or import into Figma

### Usage

This format is always generated alongside the primary export format. When the user requests any export, also generate the `slides/` directory. The user can opt out with `--no-slide-html`.

### Figma Import Workflow

1. Generate per-slide HTML files
2. Open each in a browser at 1920×1080 viewport
3. Use Figma's "Import from URL" or screenshot-to-frame workflow
4. Motif elements, image treatments, and text are all real DOM — selectable and editable after import

## Post-Export Actions

After any export:

1. Report the output file path to the user
2. Report the file size
3. Offer to open the file (for HTML and PDF)
4. Offer to re-export in a different format
5. Offer to make any final edits before re-exporting

## Error Handling

| Error | Recovery Action |
|---|---|
| Headless browser not installed | Prompt user to run `npm install` in plugin root |
| python-pptx missing | Prompt user to run `pip install python-pptx` |
| Figma MCP not authenticated | Guide user through Figma API token setup |
| Output directory does not exist | Create it automatically |
| Font embedding fails | Warn user, proceed with system font fallback |
| Image too large for PPTX | Resize image to max 2048px before embedding |
