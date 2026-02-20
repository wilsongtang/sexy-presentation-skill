# Template Rewrites: Design System Integration

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Date:** 2026-02-19
**Author:** Claude (brainstorming session with creative director)
**Status:** Approved

## Context

The v2 design system added motifs, expanded typography (7 levels), image treatments, hero moment intensity classification, and 5 composition rules to the plugin. However, the 207 existing templates still use flat flexbox layouts with no motifs, no depth, no edge tension, and minimal typography hierarchy. This design covers rewriting all 207 templates to use the new design system.

### Scope

- All 207 templates across 10 categories
- Keep the 3-variant matrix (light/colored/reversed)
- Every template gets: motif slots, expanded typography, layered depth, edge tension, image treatment wrappers
- Hybrid approach: pattern recipes for workhorse templates, bespoke creative direction layered on for hero/impact
- Support 2, 3, 4, and 5 column layouts where applicable
- Use Sonnet subagents for parallel execution

## Design

### 1. Composition Pattern Library

Every template implements exactly one of 12 composition patterns. Each pattern defines where the dominant element sits, how edge tension is created, and where motifs go.

| # | Pattern | Dominant Element | Edge Tension | Best For |
|---|---------|-----------------|--------------|----------|
| 1 | **Hero Statement** | Display-scale text | Text flush to margin | Title slides, section breaks, single statements |
| 2 | **Asymmetric Split** | Larger side (60/40 or 70/30) | Content pushed to edge, visual bleeding off | Image+text, before/after, split content |
| 3 | **Full-Bleed Visual** | Image filling entire slide | Image bleeds all 4 edges | Cinematic photos, hero images |
| 4 | **Card Grid** | One card is larger/different | Cards approach edges, motif behind | Features, team bios, comparison items |
| 5 | **Stacked Hierarchy** | Title with overline→title→body descent | Sidebar motif or accent bar | Editorial, narrative content |
| 6 | **Data Showcase** | Giant stat number at stat/display scale | Number positioned off-center per rule of thirds | KPIs, single metrics, big numbers |
| 7 | **Magazine Flow** | Pullquote or callout breaking the grid | Callout overlaps column boundary | Long-form content, editorial |
| 8 | **Gallery Mosaic** | One image 2-3x larger than others | Largest image bleeds an edge | Photo collections, portfolios |
| 9 | **Timeline Track** | The connecting track/line itself | Track extends to both edges | Timelines, roadmaps, processes |
| 10 | **Table Matrix** | Header row with accent treatment | Table extends to slide edges | Data tables, comparison grids |
| 11 | **Centered Impact** | Single element dead-center (exception to no-centering rule) | Motif elements at corners/edges | Hero quotes, thank-you, CTA |
| 12 | **Layered Stack** | Mid-ground content card | Background layer bleeds edges, foreground element overlaps | Any slide needing z-axis depth |

Each pattern defines:
- **Motif placement map**: Where motif DOM elements go at each intensity (hero: 2-3, impact: 1-2, workhorse: 0-1)
- **Typography scale rules**: Which CSS vars to use for which text elements
- **Depth recipe**: How z-axis is created (overlapping, shadows, layered backgrounds)

### 2. Category Composition Guides

Each of the 10 template categories gets a composition guide that maps every layout to a pattern.

#### Category-to-Pattern Mapping

| Category (count) | Default Intensity | Primary Patterns Used |
|---|---|---|
| **title** (24) | hero | Hero Statement, Centered Impact, Full-Bleed Visual, Asymmetric Split |
| **content** (36) | workhorse | Magazine Flow, Card Grid, Stacked Hierarchy, Asymmetric Split |
| **data** (24) | impact | Data Showcase, Card Grid, Table Matrix |
| **image** (24) | hero/impact | Full-Bleed Visual, Gallery Mosaic, Asymmetric Split, Layered Stack |
| **comparison** (18) | workhorse | Asymmetric Split, Card Grid, Table Matrix |
| **timeline** (18) | workhorse | Timeline Track, Card Grid |
| **quote** (15) | impact | Centered Impact, Hero Statement, Asymmetric Split, Full-Bleed Visual |
| **team** (15) | workhorse | Card Grid, Stacked Hierarchy, Layered Stack |
| **structural** (18) | impact | Hero Statement, Stacked Hierarchy, Timeline Track |
| **closing** (15) | hero | Centered Impact, Card Grid, Asymmetric Split |

#### Color Mode Differentiation

The 3 color variants per layout are not just color swaps — each gets intentional treatment:

- **Light** (`-light`): White/neutral background. Motifs use `opacity: 0.08-0.15`. Text uses `--color-text`. Clean, airy.
- **Colored** (`-colored`): `--color-secondary` background. Motifs use `opacity: 0.12-0.20`. More visual presence.
- **Reversed** (`-reversed`): `--color-primary` (dark) background. Text switches to `--color-text-reversed`. Motifs use `opacity: 0.06-0.12`. High contrast, dramatic.

### 3. Rewritten Template HTML Structure

Every rewritten template includes:

1. **Pattern + intensity metadata** in comments and `data-pattern` attribute
2. **Motif DOM elements** with `motif-element` class, positioned absolutely
3. **Intensity class** on `.slide` root (`motif-subtle`, `motif-bold`, `motif-hero`)
4. **Overline slot** using the `.overline` utility class
5. **Dominant element differentiation** — one element is visually heavier (larger, accent border, shadow)
6. **CSS Grid over Flexbox** for layouts, with asymmetric column ratios (e.g., `1.2fr 1fr 1fr` not `1fr 1fr 1fr`)
7. **Expanded typography** — `--size-display`/`--size-stat` for hero/impact, `--size-title`/`--size-header`/`--size-body` for workhorse
8. **Speaker notes aside** on every template
9. **All colors via CSS variables** — no raw hex values
10. **Image treatment wrappers** using `.img-treatment` + `.img-treatment-overlay` pattern

#### Column Layout Support

Card Grid pattern supports 2-5 columns:

| Columns | Grid | Dominant Treatment | Heading Scale |
|---|---|---|---|
| 2 | `1.3fr 1fr` | Larger card, accent border, shadow | `--size-header` |
| 3 | `1.2fr 1fr 1fr` | Accent border-top, shadow, slight elevation | `--size-header` |
| 4 | `1.15fr 1fr 1fr 1fr` | Accent border-top, shadow | `--size-body` |
| 5 | `1fr 1fr 1fr 1fr 1fr` | Accent background tint on one card | `--size-caption` |

#### Before/After Example

**Before** (current `content-card-layout-colored`):
```html
<div class="slide" style="background-color: var(--color-secondary);">
  <h2 style="font-size: var(--size-header); font-weight: 600; margin-bottom: var(--gap);">
    {{title}}
  </h2>
  <div class="flex flex-row" style="gap: var(--gap); flex: 1; align-items: stretch;">
    <div style="flex: 1; border: 1px solid var(--color-border); border-radius: 16px; padding: 40px;">
      <h3 style="font-size: var(--size-body); font-weight: 600;">{{card_1_title}}</h3>
      <p style="font-size: var(--size-caption); color: var(--color-muted);">{{card_1_body}}</p>
    </div>
    <!-- card 2, card 3 identical -->
  </div>
</div>
```

**After** (rewritten — Card Grid pattern, workhorse intensity):
```html
<!-- Template: content-card-layout-colored -->
<!-- Pattern: card-grid | Intensity: workhorse | Dominant: card-1 -->
<div class="slide motif-subtle" data-pattern="card-grid"
     style="background-color: var(--color-secondary); padding: var(--margin);">

  <!-- Motif: subtle corner element (workhorse = 0-1 motifs) -->
  <div class="motif-element motif-rule"
       style="position:absolute; top:0; right:80px; width:1px; height:120px;"></div>

  <!-- Overline + Title -->
  <p class="overline" style="color: var(--color-accent);">{{overline}}</p>
  <h2 style="font-family: var(--font-header); font-size: var(--size-title);
             font-weight: 700; margin-bottom: calc(var(--gap) * 1.5);">
    {{title}}
  </h2>

  <!-- Card grid: card-1 is dominant -->
  <div style="display: grid; grid-template-columns: 1.2fr 1fr 1fr;
              gap: var(--gap); flex: 1; align-items: start;">

    <!-- Card 1: DOMINANT -->
    <div style="background: var(--color-background); border-radius: var(--radius, 12px);
                padding: 48px 40px; border-top: 3px solid var(--color-accent);
                box-shadow: 0 4px 24px rgba(0,0,0,0.08); position: relative; z-index: 1;">
      <h3 style="font-family: var(--font-header); font-size: var(--size-header);
                 font-weight: 700;">{{card_1_title}}</h3>
      <p style="font-size: var(--size-body); color: var(--color-muted);
                line-height: var(--line-height); margin-top: 16px;">{{card_1_body}}</p>
    </div>

    <!-- Card 2: supporting -->
    <div style="background: var(--color-background); border-radius: var(--radius, 12px);
                padding: 40px; border: 1px solid var(--color-border);">
      <h3 style="font-family: var(--font-header); font-size: var(--size-body);
                 font-weight: 600;">{{card_2_title}}</h3>
      <p style="font-size: var(--size-caption); color: var(--color-muted);
                line-height: var(--line-height); margin-top: 12px;">{{card_2_body}}</p>
    </div>

    <!-- Card 3: supporting -->
    <div style="background: var(--color-background); border-radius: var(--radius, 12px);
                padding: 40px; border: 1px solid var(--color-border);">
      <h3 style="font-family: var(--font-header); font-size: var(--size-body);
                 font-weight: 600;">{{card_3_title}}</h3>
      <p style="font-size: var(--size-caption); color: var(--color-muted);
                line-height: var(--line-height); margin-top: 12px;">{{card_3_body}}</p>
    </div>
  </div>

  <aside class="speaker-notes" hidden>{{speaker_notes}}</aside>
</div>
```

### 4. Execution Strategy

207 templates across 10 categories. 13 tasks total, 10 running in parallel.

#### Phase 1: Pattern Reference Files (1 task)

Create `templates/_patterns/` with 12 reference HTML files — one per composition pattern. Each contains:
- HTML skeleton with motif positions marked
- Comments explaining composition rules
- Typography scale mapping
- Motif placement at each intensity level

#### Phase 2: Category Guides (1 task)

Create 10 category guide files at `templates/_guides/<category>.md`. Each maps every layout to a pattern with:
- Pattern assignment per layout
- Default intensity for the category
- Bespoke creative notes for hero/impact layouts
- Column count variations where applicable

#### Phase 3: Parallel Template Rewrites (10 tasks — one per category)

Each category runs as a separate Sonnet subagent:

| Category | Templates | Subagent receives |
|---|---|---|
| title | 24 | Pattern refs + title guide |
| content | 36 | Pattern refs + content guide |
| data | 24 | Pattern refs + data guide |
| image | 24 | Pattern refs + image guide |
| comparison | 18 | Pattern refs + comparison guide |
| timeline | 18 | Pattern refs + timeline guide |
| quote | 15 | Pattern refs + quote guide |
| team | 15 | Pattern refs + team guide |
| structural | 18 | Pattern refs + structural guide |
| closing | 15 | Pattern refs + closing guide |

#### Phase 4: Cross-Category QA (1 task)

After all 10 category rewrites complete:
- Validate every template has required metadata (pattern, intensity, motif class)
- Check no raw hex colors or hardcoded pixel font sizes
- Verify dominant element exists in every template
- Spot-check 2-3 templates per category for composition rule compliance
- Update the template registry index

#### Total: 13 tasks, 10 run concurrently in Phase 3

## What's NOT in This Design

- New template layouts (only rewriting existing 207)
- Visual rhythm planner (future task)
- Smart image selection / color harmony filtering (future task)
- Animation system (not needed per user decision)
