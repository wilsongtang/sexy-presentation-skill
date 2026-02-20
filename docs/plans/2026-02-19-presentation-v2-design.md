# Presentation Plugin v2: Design System Upgrade

**Date:** 2026-02-19
**Author:** Claude (brainstorming session with creative director)
**Status:** Approved

## Context

The v1 plugin produces structurally correct but visually boring presentations. Templates are flat flexbox layouts with no decorative elements, no typographic drama, and no image integration sophistication. The target user is an agency creative director pitching complex ideas to clients — every slide must earn its place visually.

### Design Language

The desired aesthetic combines three qualities:
1. **Cinematic imagery** — full-bleed photos, duotone treatments, images as film stills
2. **Bold typography** — oversized type, dramatic scale contrast, words as visual elements
3. **Layered compositions** — overlapping elements, breaking grid, depth effects

### Constraints

- No animation system needed (static visual quality only)
- All output must be editable in Figma and PowerPoint after export
- Motif/decorative elements must be real DOM nodes, not CSS pseudo-elements
- Slides must export as standalone HTML pages for Figma import
- Use Sonnet subagents for all implementation except creative writing tasks
- Template rewrites are deferred to a future task

## Design

### 1. Motif Rendering System

Each theme declares a `motif` field but nothing renders it. Adding a motif CSS + DOM element system.

**Per-theme motif file:** `themes/<name>/motif.css` defining base styles for `.motif-element` variants.

**Real DOM elements:** Motifs are injected as actual `<div>` and `<svg>` elements with class `.motif-element`, positioned absolutely within the slide. This ensures:
- Visible in PPTX screenshots
- Mappable to Figma objects (selectable, editable, deletable)
- No pseudo-element fragility

**Intensity classes:**
- `.motif-subtle` — low opacity, small scale, corner placement
- `.motif-bold` — higher opacity, larger, more prominent
- `.motif-hero` — dramatic, multiple elements, color blocking

**Theme motif signatures:**
| Theme | Motif style |
|---|---|
| keynote-minimal | Thin horizontal rules, subtle dot accents |
| pitch-bold | Large accent color blocks, corner fills |
| consulting-polish | Pinstripe borders, muted geometric frames |
| editorial | Column rules, serif drop caps, thin dividers |
| creative-pop | Circles, triangles, overlapping geometric shapes |
| data-story | Grid lines, subtle graph paper, data-point dots |

**Theme JSON addition:** `"motif_css_path": "themes/<name>/motif.css"`

**Implementation model:** Sonnet

### 2. Expanded Typography Scale (4 → 7 levels)

| Level | Variable | Use case | Range |
|---|---|---|---|
| **Display** | `--size-display` | Single powerful word/phrase, hero slides | 80-120px |
| **Pull stat** | `--size-stat` | Big numbers, KPIs, dramatic data | 64-96px |
| Title | `--size-title` | Slide titles (existing) | 48-60px |
| Header | `--size-header` | Section headings (existing) | 24-36px |
| Body | `--size-body` | Paragraph text (existing) | 16-18px |
| Caption | `--size-caption` | Labels, footnotes (existing) | 12-14px |
| **Overline** | `--size-overline` | Category labels, eyebrow text | 11-13px |

**Overline style:** `text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600`

**Files changed:** 6 theme JSONs, `base.html`, `templates/schema.json`

**Implementation model:** Sonnet

### 3. Image Overlay Treatment System

CSS utility classes for image treatments, applied via wrapper `<div>` with real styles (not pseudo-elements) for Figma/PPTX compatibility.

| Class | Effect | Use case |
|---|---|---|
| `.img-duotone` | Two-color mapping via filter + blend modes | Hero images, mood boards |
| `.img-gradient-fade` | Gradient overlay fading to solid color | Text-over-image slides |
| `.img-darken` | Semi-transparent dark overlay | Full-bleed photo backgrounds |
| `.img-blur-edge` | Gaussian blur on edges, sharp center | Background atmosphere |
| `.img-desaturate` | Reduced saturation | Supporting imagery |
| `.img-color-wash` | Brand accent tint at low opacity | Unified visual tone |

**File:** `components/image-treatments.css` (new)

**Implementation model:** Sonnet

### 4. Hero Moment Classifier

Added to `plan-slides` skill as a second pass after template assignment.

**Intensity levels:**
| Level | Meaning | Visual treatment |
|---|---|---|
| `hero` | Room goes quiet. Big reveal, emotional peak. | Display typography, full-bleed imagery, motif-bold, max whitespace |
| `impact` | Important supporting beat. Carries weight. | Pull-stat sizing, image treatments, motif-bold or motif-subtle |
| `workhorse` | Carries the argument. Content-dense but polished. | Standard typography, clean layout, motif-subtle |

**Classification signals:**
- Single stat/number → `impact` or `hero`
- Title and closing slides → `hero`
- Single sentence/phrase → `hero`
- Strong quote → `impact`
- Section breaks → `impact`
- Everything else → `workhorse`

Every slide gets elevated treatment — the difference is dramatic vs. controlled, not good vs. filler.

**Files changed:** `skills/plan-slides/SKILL.md`

**Implementation model:** Sonnet

### 5. Slide-Designer Creative Direction Rewrite

The highest-leverage change. Replacing 5 vague principles with specific composition rules.

**Composition rules:**
1. **Rule of thirds** — Primary content anchors to thirds intersection, not dead center
2. **Scale contrast** — At least 3:1 size ratio between largest and smallest text
3. **One dominant element** — Every slide has exactly one visual anchor
4. **Edge tension** — At least one element approaches or touches the slide edge
5. **Layered depth** — Overlapping elements, text over images. Flat side-by-side is last resort

**Anti-patterns:**
- No centered-everything layouts
- No equal-weight elements — if three items, one is visually dominant
- No naked bullet lists — bullets need icons, numbers, or visual anchors
- No empty corners — motif element or deliberate negative space

**Per-intensity guidance:**
- `hero`: `--size-display`, max 10 words, image treatment required
- `impact`: `--size-stat` for numbers or enlarged `--size-title`, 2 content elements max
- `workhorse`: Standard scale but edge tension and one-dominant-element rules apply

**Files changed:** `agents/slide-designer.md`

**Implementation model:** Opus (creative writing — composition rules need nuanced articulation)

### 6. Per-Slide Standalone HTML Export

Each slide exports as a self-contained HTML page for Figma import.

**Output structure:**
```
output/
  deck.html              # Full assembled deck (playground, PDF export)
  slides/
    slide-01.html         # Standalone page
    slide-02.html
    ...
  assets/                 # Shared images
```

**Each standalone slide includes:**
- Full `<html>`/`<head>` with theme CSS variables inlined
- Google Fonts `<link>` tags
- Image treatment CSS utilities inlined
- Motif elements as real DOM nodes
- Single `<div class="slide">` content
- Viewport: `1920x1080`

**Files changed:** `skills/export/SKILL.md`, export scripts

**Implementation model:** Sonnet

### 7. Model Routing Update

| Task | Model |
|---|---|
| Motif CSS files | Sonnet |
| Typography scale updates | Sonnet |
| Image treatment utilities | Sonnet |
| Plan-slides hero classifier | Sonnet |
| Slide-designer rewrite | **Opus** |
| Per-slide export | Sonnet |

Update `config/model-routing.json`: orchestrator moves from `creative` tier to `support` tier (Sonnet). Only slide-designer stays on Opus.

## Deferred to Future Task

### Template Rewrites (207+ templates)
All existing templates need rewriting to use the new design system (motifs, expanded typography, composition rules, image treatments). This is the largest body of work and should be its own task after infrastructure is in place. Current templates still work — they just won't leverage new capabilities.

**Priority order:** title (8) → content (12) → data (8) → image (8) → rest

### Visual Rhythm Planner
Intelligent alternation of dark/light, dense/sparse, left-heavy/right-heavy across the full deck. The hero classifier covers the most important aspect.

### Smart Image Selection
Filtering Unsplash results by color harmony with the active theme. Requires image analysis beyond CSS.
