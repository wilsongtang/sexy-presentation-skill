---
name: Design Slide
description: Generate a production-ready HTML fragment for a single slide. Receives a content block, theme CSS variables, and an assigned template. Applies CSS variable tokens, handles dynamic resizing, and passes a quality checklist before returning the fragment.
version: 0.1.0
---

# Design Slide Skill

## Purpose

Produce a single, self-contained HTML slide fragment that is visually polished, theme-consistent, and ready to be assembled into the full presentation document. This skill runs in parallel — one instance per slide — dispatched by the orchestrator.

## Inputs

Each invocation receives:

| Input | Source |
|---|---|
| Slide content block | One entry from the Slide Plan array (`plan-slides` output) |
| Theme CSS variables | Resolved block from `select-theme` skill |
| Template HTML | File at `slide.template_path` from the Slide Plan |
| Brand profile (optional) | `brand-profile.json` from `brand-profile` skill |
| Resolved images (optional) | Image URLs/base64 from `source-imagery` skill |
| Slide intensity level | `intensity` field from plan-slides classifier (`hero`, `impact`, `workhorse`) |
| Image treatments CSS | `components/image-treatments.css` utility classes |

## Process

### Step 1: Load Template

Read the template file at the specified `template_path`. Templates are HTML fragments containing:
- A `.slide` root container
- Named content slots marked with `data-slot` attributes (e.g., `data-slot="title"`, `data-slot="body"`, `data-slot="image"`)
- CSS custom property references (e.g., `var(--color-primary)`, `var(--font-heading)`)

### Step 2: Inject CSS Variables

Insert the theme CSS variable block into a `<style>` tag scoped to the slide's `.slide` container.

```html
<style>
  .slide[data-index="3"] {
    --color-primary: #1a1a2e;
    --color-accent: #e94560;
    --color-surface: #16213e;
    --color-text: #eaeaea;
    --font-heading: 'Playfair Display', serif;
    --font-body: 'Inter', sans-serif;
    --spacing-base: 32px;
    --radius-card: 8px;
  }
</style>
```

If a brand profile is provided, brand values take precedence over theme defaults for the following tokens: `--color-primary`, `--color-accent`, `--font-heading`, `--font-body`, and `--logo-url`.

### Step 3: Populate Content Slots

Replace each `data-slot` placeholder with the corresponding content from the slide content block:

- `data-slot="title"` → `slide.title`
- `data-slot="subtitle"` → `slide.subtitle` (omit element if null)
- `data-slot="body"` → rendered HTML list or paragraph from `slide.body`
- `data-slot="image"` → `<img>` tag with resolved src and alt text
- `data-slot="table"` → rendered `<table>` from `slide.table`
- `data-slot="chart"` → inline SVG or Chart.js canvas from `slide.chart`
- `data-slot="speaker-notes"` → hidden `<aside>` with speaker notes text

For bullet lists, render each body item as an `<li>` with appropriate nesting level class (`level-0`, `level-1`, `level-2`).

### Step 3.5: Inject Motif Elements

Based on the slide's `intensity` level, inject appropriate motif DOM elements from the active theme's motif CSS classes. Add the intensity class to the `.slide` root:

- `hero` → add `motif-hero` class to `.slide`, inject 2-3 motif elements at compositionally significant positions (corners, edges, behind content)
- `impact` → add `motif-bold` class to `.slide`, inject 1-2 motif elements
- `workhorse` → add `motif-subtle` class to `.slide`, inject 0-1 motif elements

All motif elements must be real `<div>` nodes with class `motif-element` plus the theme-specific motif class (e.g., `motif-circle`, `motif-rule`). Use `position: absolute` with specific `top`/`left`/`right`/`bottom` values. Never use CSS pseudo-elements.

Example:
```html
<div class="motif-element motif-circle" style="position: absolute; top: -60px; right: -40px; width: 300px; height: 300px;"></div>
```

### Step 3.6: Apply Image Treatments

When a slide contains imagery, wrap the `<img>` element in an image treatment container:

```html
<div class="img-treatment img-darken">
  <img src="..." alt="...">
  <div class="img-treatment-overlay"></div>
</div>
```

Treatment selection by intensity:
- `hero`: `.img-darken`, `.img-duotone`, or `.img-gradient-fade` (choose based on whether text overlays the image)
- `impact`: `.img-desaturate` or `.img-color-wash`
- `workhorse`: `.img-desaturate` for backgrounds, no treatment for content images

Never use an image without `object-fit: cover` and a meaningful `alt` attribute.

### Step 4: Handle Dynamic Resizing

Ensure the slide scales correctly across viewport widths:

- Use `aspect-ratio: 16 / 9` (or the presentation's declared ratio) on the `.slide` container
- Use `clamp()` for font sizes to maintain readability at different zoom levels:
  ```css
  font-size: clamp(1rem, 2.5vw, 2rem);
  ```
- Use CSS Grid or Flexbox for layout — avoid fixed pixel widths on content areas
- Images must use `object-fit: cover` with explicit `width` and `height` attributes to prevent layout shift

### Step 5: Specialized Content Rendering

#### Tables

```html
<table class="slide-table">
  <thead>
    <tr>
      <th>Column A</th>
      <th>Column B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Value</td>
      <td>Value</td>
    </tr>
  </tbody>
</table>
```

Style with zebra striping using `--color-surface` for even rows and transparent for odd rows.

#### Charts

For simple bar/line charts, generate an inline SVG. For complex charts, emit a `<canvas>` element with a `<script>` block that initializes Chart.js with the data from `slide.chart`:

```html
<canvas id="chart-3" width="600" height="350"></canvas>
<script>
  new Chart(document.getElementById('chart-3'), {
    type: 'bar',
    data: { /* injected from slide.chart */ },
    options: { responsive: true, maintainAspectRatio: false }
  });
</script>
```

#### Timelines

Render as a horizontal or vertical sequence of `.timeline-step` elements, each with a step number, heading, and body text.

## Quality Checklist

Before returning the HTML fragment, verify all of the following:

- [ ] All `data-slot` placeholders have been replaced (no empty `data-slot` attributes remain)
- [ ] No hardcoded hex colors — all colors use CSS custom properties
- [ ] No hardcoded pixel font sizes — all font sizes use `clamp()` or `em`/`rem`
- [ ] The slide container has `aspect-ratio` set correctly
- [ ] All `<img>` elements have non-empty `alt` attributes
- [ ] The slide renders without horizontal overflow at 1280px viewport width
- [ ] Heading hierarchy is correct (single `<h1>` for title, `<h2>` for subtitle)
- [ ] Contrast ratio between text and background meets WCAG AA (4.5:1 for body text)
- [ ] Speaker notes are present in a hidden `<aside>` (even if empty)
- [ ] No inline `style` attributes that could conflict with theme tokens
- [ ] Slide has the correct `motif-hero|motif-bold|motif-subtle` class matching its intensity
- [ ] All motif decorations are real DOM elements with class `motif-element` (no pseudo-elements)
- [ ] Image treatments use the `.img-treatment` wrapper pattern with `.img-treatment-overlay` div
- [ ] `--size-display` is only used on `hero` intensity slides
- [ ] `--size-stat` is only used on `hero` or `impact` intensity slides

If any checklist item fails, fix it before returning. Document any items that could not be resolved in an `<!-- QA: ... -->` HTML comment at the end of the fragment.

## Output Format

Return a single HTML fragment string:

```html
<!-- slide: index=3, template=two-column/02-image-right.html -->
<style>
  .slide[data-index="3"] { /* CSS variable block */ }
</style>
<section class="slide" data-index="3" data-template="two-column/02-image-right" data-layout="two-column">
  <div class="slide-content">
    <h1 class="slide-title" data-slot="title">Slide Title</h1>
    <div class="slide-body" data-slot="body">
      <!-- rendered body content -->
    </div>
  </div>
  <div class="slide-image" data-slot="image">
    <img src="..." alt="..." />
  </div>
  <aside class="speaker-notes" hidden data-slot="speaker-notes">
    Speaker notes text
  </aside>
</section>
```

Pass the returned fragment to the orchestrator for assembly into the full presentation document.
