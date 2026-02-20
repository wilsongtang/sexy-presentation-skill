# Presentation v2: Design System Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade the presentation plugin's visual design system with motif rendering, expanded typography, image treatments, hero moment classification, improved creative direction, and Figma-compatible per-slide export.

**Architecture:** Infrastructure-first approach — build the design system primitives (typography, motifs, image treatments) first, then update the agent/skill prompts that consume them, then update export. No template rewrites in this scope (deferred).

**Tech Stack:** CSS custom properties, inline SVG, HTML DOM elements, JSON schema updates. Prompt engineering for agent/skill updates.

---

### Task 1: Expand typography scale in theme schema

**Files:**
- Modify: `themes/schema.json`

**Step 1: Add new typography fields to schema**

Add `display_size`, `stat_size`, and `overline_size` to the typography schema. These are optional to avoid breaking existing themes before they're updated.

```json
"typography": {
  "type": "object",
  "required": ["header_font", "body_font", "title_size", "header_size", "body_size"],
  "properties": {
    "header_font": { "type": "string" },
    "body_font": { "type": "string" },
    "display_size": { "type": "string", "description": "80-120px. Hero slides, single powerful words." },
    "stat_size": { "type": "string", "description": "64-96px. Big numbers, KPIs." },
    "title_size": { "type": "string" },
    "header_size": { "type": "string" },
    "body_size": { "type": "string" },
    "caption_size": { "type": "string" },
    "overline_size": { "type": "string", "description": "11-13px. Uppercase category labels." },
    "line_height": { "type": "string" }
  }
}
```

**Step 2: Add motif_css_path to schema**

Add a new optional top-level property to the theme schema:

```json
"motif_css_path": { "type": "string", "description": "Path to theme motif CSS file relative to plugin root" }
```

**Step 3: Verify schema is valid JSON**

Run: `python3 -c "import json; json.load(open('themes/schema.json'))"`
Expected: No output (success)

**Step 4: Commit**

```bash
git add themes/schema.json
git commit -m "feat(v2): expand theme schema with display/stat/overline typography and motif_css_path"
```

---

### Task 2: Update all 6 theme JSONs with new typography values

**Files:**
- Modify: `themes/keynote-minimal.json`
- Modify: `themes/pitch-bold.json`
- Modify: `themes/consulting-polish.json`
- Modify: `themes/editorial.json`
- Modify: `themes/creative-pop.json`
- Modify: `themes/data-story.json`

**Step 1: Add typography values to each theme**

For each theme, add `display_size`, `stat_size`, `overline_size`, and `motif_css_path`. Values per theme:

| Theme | display_size | stat_size | overline_size | motif_css_path |
|---|---|---|---|---|
| keynote-minimal | 96px | 72px | 12px | themes/keynote-minimal/motif.css |
| pitch-bold | 112px | 80px | 13px | themes/pitch-bold/motif.css |
| consulting-polish | 88px | 68px | 11px | themes/consulting-polish/motif.css |
| editorial | 96px | 72px | 12px | themes/editorial/motif.css |
| creative-pop | 120px | 96px | 13px | themes/creative-pop/motif.css |
| data-story | 88px | 72px | 11px | themes/data-story/motif.css |

Example for keynote-minimal — add these three keys inside the `"typography"` object:

```json
"display_size": "96px",
"stat_size": "72px",
"overline_size": "12px"
```

And add this as a new top-level key:

```json
"motif_css_path": "themes/keynote-minimal/motif.css"
```

Repeat for all 6 themes with the values from the table above.

**Step 2: Validate each theme against schema**

Run: `python3 -c "import json; [json.load(open(f'themes/{t}.json')) for t in ['keynote-minimal','pitch-bold','consulting-polish','editorial','creative-pop','data-story']]; print('All valid')"`
Expected: `All valid`

**Step 3: Commit**

```bash
git add themes/*.json
git commit -m "feat(v2): add display/stat/overline typography and motif_css_path to all 6 themes"
```

---

### Task 3: Update base.html with new CSS variables

**Files:**
- Modify: `templates/base.html`

**Step 1: Add new CSS variables to :root block**

In `templates/base.html`, add the 3 new typography variables and the overline utility class inside the `<style>` block. Insert after the `--size-caption` line and before `--line-height`:

```css
      --size-display: {{typography.display_size}};
      --size-stat: {{typography.stat_size}};
      --size-overline: {{typography.overline_size}};
```

**Step 2: Add overline utility class**

Add after the `.logo` rule and before the closing `</style>` tag:

```css
    .overline {
      font-size: var(--size-overline);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-weight: 600;
      color: var(--color-muted);
    }

    .motif-element {
      position: absolute;
      pointer-events: none;
      z-index: 0;
    }
```

**Step 3: Add motif CSS link placeholder**

In the `<head>`, add after the Tailwind config `</script>` and before `</head>`:

```html
  <!-- Theme motif styles -->
  <style>{{motif_css}}</style>
  <!-- Image treatment utilities -->
  <style>{{image_treatments_css}}</style>
```

**Step 4: Verify HTML is well-formed**

Run: `python3 -c "f=open('templates/base.html').read(); assert '{{typography.display_size}}' in f; assert '.motif-element' in f; assert '{{motif_css}}' in f; print('OK')"`
Expected: `OK`

**Step 5: Commit**

```bash
git add templates/base.html
git commit -m "feat(v2): add display/stat/overline CSS vars, motif-element base class, and treatment slots to base.html"
```

---

### Task 4: Create image treatments CSS

**Files:**
- Create: `components/image-treatments.css`

**Step 1: Write the image treatments file**

Create `components/image-treatments.css` with all 6 treatment utility classes. Each uses a real child `<div>` overlay (not pseudo-elements) for Figma/PPTX compatibility. The CSS defines the wrapper and overlay styles:

```css
/* Image Treatment Utilities
   Usage: Wrap an <img> in a <div class="img-treatment img-darken">
   The overlay <div class="img-treatment-overlay"> sits inside the wrapper.
   All treatments use real DOM elements for Figma/PPTX export compatibility. */

.img-treatment {
  position: relative;
  overflow: hidden;
  display: inline-block;
}

.img-treatment img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.img-treatment-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

/* Darken — semi-transparent dark overlay for text legibility */
.img-darken .img-treatment-overlay {
  background: rgba(0, 0, 0, 0.45);
}

/* Gradient Fade — fades image to solid color on bottom edge */
.img-gradient-fade .img-treatment-overlay {
  background: linear-gradient(
    to bottom,
    transparent 40%,
    var(--color-background) 100%
  );
}

/* Desaturate — reduced saturation to let brand colors dominate */
.img-desaturate img {
  filter: saturate(0.25);
}

/* Color Wash — brand accent tint at low opacity */
.img-color-wash .img-treatment-overlay {
  background: var(--color-accent);
  opacity: 0.2;
  mix-blend-mode: multiply;
}

/* Duotone — maps image to two brand colors */
.img-duotone img {
  filter: grayscale(100%) contrast(1.1);
}
.img-duotone .img-treatment-overlay {
  background: var(--color-primary);
  mix-blend-mode: color;
  opacity: 0.85;
}

/* Blur Edge — gaussian blur on edges, sharp center */
.img-blur-edge .img-treatment-overlay {
  backdrop-filter: blur(0px);
  -webkit-backdrop-filter: blur(0px);
  mask-image: radial-gradient(ellipse 70% 70% at center, transparent 50%, black 100%);
  -webkit-mask-image: radial-gradient(ellipse 70% 70% at center, transparent 50%, black 100%);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
```

**Step 2: Verify file exists and has all 6 classes**

Run: `python3 -c "css=open('components/image-treatments.css').read(); classes=['img-darken','img-gradient-fade','img-desaturate','img-color-wash','img-duotone','img-blur-edge']; missing=[c for c in classes if c not in css]; print(f'Missing: {missing}' if missing else 'All 6 treatments present')"`
Expected: `All 6 treatments present`

**Step 3: Commit**

```bash
git add components/image-treatments.css
git commit -m "feat(v2): add 6 image overlay treatment CSS utilities for Figma-compatible export"
```

---

### Task 5: Create motif CSS for keynote-minimal theme

**Files:**
- Create: `themes/keynote-minimal/motif.css`

**Step 1: Create theme motif directory and CSS**

The keynote-minimal motif uses thin horizontal rules and subtle dot accents. All decorative elements are real DOM nodes styled by this CSS.

```css
/* Motif: keynote-minimal — clean-whitespace
   Thin horizontal rules and subtle dot accents.
   Applied to real .motif-element DOM nodes inside .slide */

/* Subtle horizontal rule — placed at bottom third of slide */
.motif-rule {
  width: 120px;
  height: 1px;
  background: var(--color-border);
}

/* Dot accent — small circle placed at grid intersections */
.motif-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-accent);
  opacity: 0.25;
}

/* Thin vertical line — for editorial column effect */
.motif-vline {
  width: 1px;
  height: 80px;
  background: var(--color-border);
  opacity: 0.4;
}

/* Intensity: subtle — default for workhorse slides */
.motif-subtle .motif-rule { opacity: 0.3; width: 80px; }
.motif-subtle .motif-dot { opacity: 0.15; }
.motif-subtle .motif-vline { opacity: 0.2; }

/* Intensity: bold — for impact slides */
.motif-bold .motif-rule { opacity: 0.5; width: 160px; }
.motif-bold .motif-dot { opacity: 0.35; width: 8px; height: 8px; }
.motif-bold .motif-vline { opacity: 0.5; height: 120px; }

/* Intensity: hero — for hero slides */
.motif-hero .motif-rule { opacity: 0.6; width: 240px; height: 2px; background: var(--color-accent); }
.motif-hero .motif-dot { opacity: 0.5; width: 10px; height: 10px; }
.motif-hero .motif-vline { opacity: 0.6; height: 200px; background: var(--color-accent); }
```

**Step 2: Verify file**

Run: `test -f themes/keynote-minimal/motif.css && echo "OK" || echo "MISSING"`
Expected: `OK`

**Step 3: Commit**

```bash
git add themes/keynote-minimal/
git commit -m "feat(v2): add keynote-minimal motif CSS — thin rules and dot accents"
```

---

### Task 6: Create motif CSS for pitch-bold theme

**Files:**
- Create: `themes/pitch-bold/motif.css`

**Step 1: Create theme motif CSS**

Pitch-bold uses large accent color blocks and corner fills.

```css
/* Motif: pitch-bold — bold-accent-blocks
   Large accent color blocks and corner fills.
   Applied to real .motif-element DOM nodes inside .slide */

/* Accent block — large rectangular color slab */
.motif-block {
  background: var(--color-accent);
  border-radius: 0;
}

/* Corner fill — triangular or rectangular corner accent */
.motif-corner {
  width: 200px;
  height: 200px;
  background: var(--color-accent);
  opacity: 0.12;
}

/* Accent stripe — horizontal bar across slide */
.motif-stripe {
  height: 6px;
  width: 100%;
  background: var(--color-accent);
  opacity: 0.8;
}

/* Intensity: subtle */
.motif-subtle .motif-block { opacity: 0.06; }
.motif-subtle .motif-corner { opacity: 0.06; width: 120px; height: 120px; }
.motif-subtle .motif-stripe { opacity: 0.3; height: 3px; }

/* Intensity: bold */
.motif-bold .motif-block { opacity: 0.1; }
.motif-bold .motif-corner { opacity: 0.12; width: 240px; height: 240px; }
.motif-bold .motif-stripe { opacity: 0.6; height: 6px; }

/* Intensity: hero */
.motif-hero .motif-block { opacity: 0.15; }
.motif-hero .motif-corner { opacity: 0.2; width: 360px; height: 360px; }
.motif-hero .motif-stripe { opacity: 1; height: 8px; }
```

**Step 2: Commit**

```bash
git add themes/pitch-bold/
git commit -m "feat(v2): add pitch-bold motif CSS — accent blocks and corner fills"
```

---

### Task 7: Create motif CSS for consulting-polish theme

**Files:**
- Create: `themes/consulting-polish/motif.css`

**Step 1: Create theme motif CSS**

Consulting-polish uses pinstripe borders and muted geometric frames.

```css
/* Motif: consulting-polish — pinstripe-borders
   Pinstripe borders and muted geometric frames.
   Applied to real .motif-element DOM nodes inside .slide */

/* Pinstripe border — double thin line */
.motif-pinstripe {
  border: 1px solid var(--color-border);
  outline: 1px solid var(--color-border);
  outline-offset: 4px;
  opacity: 0.4;
}

/* Geometric frame — thin rectangular border inset from slide edge */
.motif-frame {
  border: 1px solid var(--color-border);
  opacity: 0.3;
}

/* Corner bracket — L-shaped accent in corners */
.motif-bracket {
  width: 40px;
  height: 40px;
  border-left: 2px solid var(--color-muted);
  border-top: 2px solid var(--color-muted);
  opacity: 0.3;
}

/* Intensity: subtle */
.motif-subtle .motif-pinstripe { opacity: 0.2; }
.motif-subtle .motif-frame { opacity: 0.15; }
.motif-subtle .motif-bracket { opacity: 0.15; width: 30px; height: 30px; }

/* Intensity: bold */
.motif-bold .motif-pinstripe { opacity: 0.4; }
.motif-bold .motif-frame { opacity: 0.3; }
.motif-bold .motif-bracket { opacity: 0.35; width: 50px; height: 50px; }

/* Intensity: hero */
.motif-hero .motif-pinstripe { opacity: 0.5; border-color: var(--color-accent); outline-color: var(--color-accent); }
.motif-hero .motif-frame { opacity: 0.4; border-color: var(--color-accent); }
.motif-hero .motif-bracket { opacity: 0.5; width: 60px; height: 60px; border-color: var(--color-accent); }
```

**Step 2: Commit**

```bash
git add themes/consulting-polish/
git commit -m "feat(v2): add consulting-polish motif CSS — pinstripe borders and geometric frames"
```

---

### Task 8: Create motif CSS for editorial theme

**Files:**
- Create: `themes/editorial/motif.css`

**Step 1: Create theme motif CSS**

Editorial uses column rules, drop cap styling, and thin dividers.

```css
/* Motif: editorial — editorial-columns
   Column rules, serif drop caps, thin dividers.
   Applied to real .motif-element DOM nodes inside .slide */

/* Column rule — vertical divider between content columns */
.motif-column-rule {
  width: 1px;
  background: var(--color-border);
  align-self: stretch;
  opacity: 0.5;
}

/* Horizontal divider — thin line with subtle serif character */
.motif-divider {
  width: 100%;
  height: 1px;
  background: var(--color-border);
  opacity: 0.4;
}

/* Drop cap marker — large decorative initial letter styling hint */
.motif-dropcap-marker {
  width: 60px;
  height: 60px;
  border-bottom: 2px solid var(--color-accent);
  opacity: 0.3;
}

/* Pull rule — short accent line above or below a pull quote */
.motif-pull-rule {
  width: 60px;
  height: 3px;
  background: var(--color-accent);
  opacity: 0.6;
}

/* Intensity: subtle */
.motif-subtle .motif-column-rule { opacity: 0.3; }
.motif-subtle .motif-divider { opacity: 0.25; }
.motif-subtle .motif-dropcap-marker { opacity: 0.15; }
.motif-subtle .motif-pull-rule { opacity: 0.3; width: 40px; }

/* Intensity: bold */
.motif-bold .motif-column-rule { opacity: 0.5; }
.motif-bold .motif-divider { opacity: 0.4; }
.motif-bold .motif-dropcap-marker { opacity: 0.3; width: 80px; height: 80px; }
.motif-bold .motif-pull-rule { opacity: 0.7; width: 80px; }

/* Intensity: hero */
.motif-hero .motif-column-rule { opacity: 0.6; width: 2px; background: var(--color-accent); }
.motif-hero .motif-divider { opacity: 0.5; height: 2px; background: var(--color-accent); }
.motif-hero .motif-dropcap-marker { opacity: 0.5; width: 100px; height: 100px; border-width: 3px; }
.motif-hero .motif-pull-rule { opacity: 1; width: 100px; height: 4px; }
```

**Step 2: Commit**

```bash
git add themes/editorial/
git commit -m "feat(v2): add editorial motif CSS — column rules, dividers, and pull rules"
```

---

### Task 9: Create motif CSS for creative-pop theme

**Files:**
- Create: `themes/creative-pop/motif.css`

**Step 1: Create theme motif CSS**

Creative-pop uses circles, triangles, and overlapping geometric shapes.

```css
/* Motif: creative-pop — geometric-shapes
   Circles, triangles, overlapping geometric shapes.
   Applied to real .motif-element DOM nodes inside .slide */

/* Circle — decorative round shape */
.motif-circle {
  border-radius: 50%;
  background: var(--color-accent);
  opacity: 0.08;
}

/* Triangle — CSS triangle using borders */
.motif-triangle {
  width: 0;
  height: 0;
  border-left: 80px solid transparent;
  border-right: 80px solid transparent;
  border-bottom: 140px solid var(--color-primary);
  opacity: 0.06;
}

/* Square — rotated 45deg to appear as diamond */
.motif-diamond {
  width: 100px;
  height: 100px;
  background: var(--color-secondary);
  transform: rotate(45deg);
  opacity: 0.06;
}

/* Half circle — semicircle accent */
.motif-halfcircle {
  width: 200px;
  height: 100px;
  background: var(--color-accent);
  border-radius: 200px 200px 0 0;
  opacity: 0.08;
}

/* Intensity: subtle */
.motif-subtle .motif-circle { opacity: 0.05; }
.motif-subtle .motif-triangle { opacity: 0.04; }
.motif-subtle .motif-diamond { opacity: 0.04; }
.motif-subtle .motif-halfcircle { opacity: 0.05; }

/* Intensity: bold */
.motif-bold .motif-circle { opacity: 0.1; }
.motif-bold .motif-triangle { opacity: 0.08; }
.motif-bold .motif-diamond { opacity: 0.08; }
.motif-bold .motif-halfcircle { opacity: 0.1; }

/* Intensity: hero */
.motif-hero .motif-circle { opacity: 0.15; }
.motif-hero .motif-triangle { opacity: 0.12; border-bottom-color: var(--color-accent); }
.motif-hero .motif-diamond { opacity: 0.12; background: var(--color-accent); }
.motif-hero .motif-halfcircle { opacity: 0.15; }
```

**Step 2: Commit**

```bash
git add themes/creative-pop/
git commit -m "feat(v2): add creative-pop motif CSS — circles, triangles, and geometric shapes"
```

---

### Task 10: Create motif CSS for data-story theme

**Files:**
- Create: `themes/data-story/motif.css`

**Step 1: Create theme motif CSS**

Data-story uses grid lines, subtle graph paper patterns, and data-point dots.

```css
/* Motif: data-story — grid-data-points
   Grid lines, subtle graph paper, data-point dots.
   Applied to real .motif-element DOM nodes inside .slide */

/* Grid line — horizontal or vertical rule for graph-paper feel */
.motif-gridline-h {
  width: 100%;
  height: 1px;
  background: var(--color-border);
  opacity: 0.15;
}

.motif-gridline-v {
  width: 1px;
  height: 100%;
  background: var(--color-border);
  opacity: 0.15;
}

/* Data dot — small filled circle representing a data point */
.motif-data-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-accent);
  opacity: 0.3;
}

/* Axis line — thicker line for chart axes */
.motif-axis {
  background: var(--color-muted);
  opacity: 0.3;
}
.motif-axis-x {
  width: 100%;
  height: 2px;
}
.motif-axis-y {
  width: 2px;
  height: 100%;
}

/* Intensity: subtle */
.motif-subtle .motif-gridline-h,
.motif-subtle .motif-gridline-v { opacity: 0.08; }
.motif-subtle .motif-data-dot { opacity: 0.15; width: 6px; height: 6px; }
.motif-subtle .motif-axis { opacity: 0.15; }

/* Intensity: bold */
.motif-bold .motif-gridline-h,
.motif-bold .motif-gridline-v { opacity: 0.2; }
.motif-bold .motif-data-dot { opacity: 0.35; width: 10px; height: 10px; }
.motif-bold .motif-axis { opacity: 0.35; }

/* Intensity: hero */
.motif-hero .motif-gridline-h,
.motif-hero .motif-gridline-v { opacity: 0.25; }
.motif-hero .motif-data-dot { opacity: 0.5; width: 12px; height: 12px; background: var(--color-accent); }
.motif-hero .motif-axis { opacity: 0.5; background: var(--color-accent); }
```

**Step 2: Commit**

```bash
git add themes/data-story/
git commit -m "feat(v2): add data-story motif CSS — grid lines, data dots, and axis accents"
```

---

### Task 11: Update plan-slides skill with hero moment classifier

**Files:**
- Modify: `skills/plan-slides/SKILL.md`

**Step 1: Add intensity classification section**

Insert a new section `### 5. Intensity Classification` after the existing `### 4. Pacing and Flow Review` section and before `## Output Format`. Add this content:

```markdown
### 5. Intensity Classification (Hero Moments)

After template assignment and pacing review, make a second pass to tag each slide with an **intensity level**. This tag tells the slide-designer how dramatically to treat the slide.

| Level | Meaning | Visual treatment |
|---|---|---|
| `hero` | The room goes quiet. Big reveal, emotional peak, key insight. | `--size-display` typography, full-bleed imagery with treatment, `motif-hero` class, maximum whitespace, max 10 words on screen |
| `impact` | Important supporting beat. Carries weight but not the climax. | `--size-stat` for numbers or enlarged title, image treatments, `motif-bold` class, 2 content elements maximum |
| `workhorse` | Carries the argument. Content-dense but still polished. | Standard typography scale, clean layout, `motif-subtle` class, edge tension and one-dominant-element rules apply |

**Classification signals:**

- Title slide (first slide) → `hero`
- Closing / CTA slide (last slide) → `hero`
- Single stat or number as primary content → `impact` (or `hero` if it's THE key number)
- Single sentence or short phrase as only content → `hero`
- Strong pull quote or testimonial → `impact`
- Section break / chapter divider → `impact`
- All other content slides → `workhorse`

**Every slide gets elevated treatment.** The difference between `hero` and `workhorse` is dramatic vs. controlled — not good vs. filler. There are no throwaway slides.

Add the `intensity` field to each slide in the output array.
```

**Step 2: Update the output JSON example**

In the existing Slide Plan output example, add `"intensity": "hero"` to the first slide object and `"intensity": "impact"` to the second.

**Step 3: Commit**

```bash
git add skills/plan-slides/SKILL.md
git commit -m "feat(v2): add hero moment intensity classifier to plan-slides skill"
```

---

### Task 12: Rewrite slide-designer agent with creative direction (Opus)

**Files:**
- Modify: `agents/slide-designer.md`

**Note:** This task requires Opus model — it's the creative core of the upgrade.

**Step 1: Rewrite the Design Principles and Anti-Patterns sections**

Replace the existing `## Design Principles` section (5 bullet points) and `## Anti-Patterns` section with the following. Keep all other sections (Input, Output, Design Process steps 1-4, Quality Checklist, Memory Integration) unchanged.

Replace `## Design Principles` with:

```markdown
## Composition Rules

These are non-negotiable. Every slide must satisfy all five.

### 1. Rule of Thirds
The primary content element anchors to a thirds intersection — not dead center. On a 1920×1080 slide, the four power points are at (640, 360), (1280, 360), (640, 720), (1280, 720). Place the dominant element at or near one of these points.

Exception: Full-bleed imagery with a centered overlay text block is acceptable if the image carries the visual weight to the edges.

### 2. Scale Contrast
At least a 3:1 size ratio between the largest and smallest text elements on any slide. If the title is 48px, nothing else on the slide should be larger than 16px body text. If you're using `--size-display` at 96px, the body text at 18px gives you a 5.3:1 ratio — that's the energy you want.

A slide where everything is roughly the same size has no hierarchy. The eye doesn't know where to land.

### 3. One Dominant Element
Every slide has exactly one visual anchor — the thing the eye hits first. It could be a huge number, a hero photo, a display-sized word, or a bold color block. Everything else on the slide exists to support or contextualize that anchor.

If you can't identify the dominant element, the slide doesn't have one. Fix it.

### 4. Edge Tension
At least one element should approach, touch, or break the slide edge. Full-bleed images, text flush against the margin, color blocks bleeding off-screen, motif elements extending past the boundary. Nothing should float timidly in the middle.

Edge tension creates dynamism. It makes a slide feel like a crop of a larger composition rather than a card placed on a table.

### 5. Layered Depth
Create z-axis depth through overlapping elements: text over images (with appropriate treatment), cards casting shadows over backgrounds, motif elements behind content, color blocks partially obscured by other elements.

Flat, side-by-side layouts where nothing overlaps are a last resort. Even a subtle shadow or a motif element peeking behind a content block creates depth.
```

Replace `## Anti-Patterns (DO NOT)` with:

```markdown
## Anti-Patterns

These kill the visual energy. Never do them.

- **Centered-everything** — Centering is a crutch. It's only appropriate for single hero statements and quotes. Multi-element slides should use asymmetric placement anchored to the rule of thirds.
- **Equal-weight siblings** — If three cards are shown, one must be visually dominant (larger, different color, different z-level). Equal-weight items create visual monotony.
- **Naked bullet lists** — Plain text bullets are a PowerPoint 2003 artifact. Every list item needs a visual anchor: a number, an icon, a colored marker, or a card container. If you're reaching for `<ul><li>`, stop and rethink the layout.
- **Empty corners** — If three quadrants have content, the fourth needs a motif element, a decorative shape, or deliberate negative space with a clear compositional purpose. Dead corners make a slide look unfinished.
- **Uniform backgrounds** — Don't use the same background treatment for every slide. Alternate between light, dark, image-backed, and color-blocked slides to create rhythm.
- **Text-only slides** (except hero statements) — Even content-heavy slides should have at least one visual element: a motif, a color block, an icon, or an accent shape.
- **Small, centered images** — Images are either full-bleed, half-bleed, or placed with edge tension. Never a small rectangle floating in the center with text underneath.
```

**Step 2: Add per-intensity design guidance**

Add a new section after Anti-Patterns:

```markdown
## Intensity-Driven Design

The `intensity` field from the slide plan tells you how dramatic to go.

### hero intensity
- Use `--size-display` (80-120px) for the primary text
- Maximum 10 words visible on screen
- Full-bleed imagery with `.img-darken`, `.img-duotone`, or `.img-gradient-fade` treatment
- `motif-hero` class on the slide for maximum decorative intensity
- The slide should be breathtaking. If it doesn't make someone pause, it's not hero enough.

### impact intensity
- Use `--size-stat` (64-96px) for numbers or key phrases
- Maximum 2 content elements (e.g., a big number and a label)
- Image treatments encouraged: `.img-desaturate`, `.img-color-wash`
- `motif-bold` class on the slide
- Overline text (`.overline` class) above headings for category context

### workhorse intensity
- Standard typography scale (`--size-title`, `--size-header`, `--size-body`)
- All five composition rules still apply — workhorse doesn't mean boring
- `motif-subtle` class on the slide
- Overline text encouraged for section context
- Edge tension and one-dominant-element rules are mandatory even here
```

**Step 3: Update the model field in YAML frontmatter**

Confirm the frontmatter still reads `model: opus`. Do not change this.

**Step 4: Commit**

```bash
git add agents/slide-designer.md
git commit -m "feat(v2): rewrite slide-designer with composition rules, anti-patterns, and intensity-driven design"
```

---

### Task 13: Update model routing config

**Files:**
- Modify: `config/model-routing.json`

**Step 1: Move orchestrator from creative to support tier**

In `config/model-routing.json`, move `"orchestrator"` from the `tiers.creative.agents` array to `tiers.support.agents`. The creative tier should only contain `"slide-designer"` and `"art-director"`.

After edit:
```json
"creative": {
  "description": "Design-critical agents that require highest visual and creative quality",
  "model": "opus",
  "agents": ["slide-designer", "art-director"]
},
"support": {
  "description": "Agents requiring good reasoning but not peak creative ability",
  "model": "sonnet",
  "agents": ["orchestrator", "copy-editor", "image-director", "table-designer", "timeline-agent", "infographic-agent"]
},
```

**Step 2: Verify JSON is valid**

Run: `python3 -c "import json; json.load(open('config/model-routing.json')); print('Valid')"`
Expected: `Valid`

**Step 3: Commit**

```bash
git add config/model-routing.json
git commit -m "feat(v2): move orchestrator to support tier (sonnet), keep only slide-designer and art-director on opus"
```

---

### Task 14: Update export skill with per-slide HTML mode

**Files:**
- Modify: `skills/export/SKILL.md`

**Step 1: Add per-slide HTML export section**

Insert a new section after `## Format 4: HTML Export` and before `## Post-Export Actions`. Add:

```markdown
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
```

**Step 2: Update the Supported Export Formats table**

Add a row to the table at the top of the skill:

```
| Per-slide HTML | Auto-generated alongside any export | Figma import, individual editing |
```

**Step 3: Commit**

```bash
git add skills/export/SKILL.md
git commit -m "feat(v2): add per-slide standalone HTML export for Figma-compatible output"
```

---

### Task 15: Update design-slide skill to reference new systems

**Files:**
- Modify: `skills/design-slide/SKILL.md`

**Step 1: Update the inputs table**

Add two new rows to the Inputs table:

```
| Slide intensity level | `intensity` field from plan-slides classifier (`hero`, `impact`, `workhorse`) |
| Image treatments CSS | `components/image-treatments.css` utility classes |
```

**Step 2: Add motif element injection guidance**

After `### Step 3: Populate Content Slots`, add a new step:

```markdown
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
```

**Step 3: Add image treatment guidance**

After the motif section, add:

```markdown
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
```

**Step 4: Update the quality checklist**

Add these items to the existing quality checklist:

```markdown
- [ ] Slide has the correct `motif-hero|motif-bold|motif-subtle` class matching its intensity
- [ ] All motif decorations are real DOM elements with class `motif-element` (no pseudo-elements)
- [ ] Image treatments use the `.img-treatment` wrapper pattern with `.img-treatment-overlay` div
- [ ] `--size-display` is only used on `hero` intensity slides
- [ ] `--size-stat` is only used on `hero` or `impact` intensity slides
```

**Step 5: Commit**

```bash
git add skills/design-slide/SKILL.md
git commit -m "feat(v2): update design-slide skill with motif injection, image treatments, and intensity guidance"
```

---

### Task 16: Final validation and integration commit

**Files:**
- All files from tasks 1-15

**Step 1: Verify all new files exist**

Run:
```bash
echo "=== Schema ===" && python3 -c "import json; s=json.load(open('themes/schema.json')); print('display_size' in s['properties']['typography']['properties'])" && \
echo "=== Themes ===" && python3 -c "import json; [json.load(open(f'themes/{t}.json')) for t in ['keynote-minimal','pitch-bold','consulting-polish','editorial','creative-pop','data-story']]; print('All 6 valid')" && \
echo "=== Motifs ===" && ls themes/*/motif.css | wc -l && \
echo "=== Image Treatments ===" && test -f components/image-treatments.css && echo "Present" && \
echo "=== Base HTML ===" && python3 -c "f=open('templates/base.html').read(); assert '--size-display' in f; assert '.motif-element' in f; print('OK')" && \
echo "=== Model Routing ===" && python3 -c "import json; r=json.load(open('config/model-routing.json')); assert 'orchestrator' in r['tiers']['support']['agents']; print('OK')"
```

Expected:
```
=== Schema ===
True
=== Themes ===
All 6 valid
=== Motifs ===
6
=== Image Treatments ===
Present
=== Base HTML ===
OK
=== Model Routing ===
OK
```

**Step 2: Run existing tests to verify nothing broke**

Run: `python3 -m pytest scripts/test_parse_pptx.py scripts/test_parse_pdf.py -v`
Expected: 3 tests pass

**Step 3: Push to remote**

```bash
git push origin feat/plugin-implementation
```

---

## Deferred: Template Rewrites (Future Task)

All 207+ existing templates need rewriting to leverage the new design system:
- Use motif DOM elements per theme
- Apply expanded typography (display, stat, overline)
- Use image treatment wrappers
- Follow the new composition rules (rule of thirds, edge tension, layered depth)
- Respect intensity levels in template variants

**Priority order for future rewrite:** title (8 layouts) → content (12 layouts) → data (8 layouts) → image (8 layouts) → comparison, timeline, quote, team, structural, closing
