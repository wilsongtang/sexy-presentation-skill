# Title Template Guide

## Category Overview
Title slides are hero moments — every title slide gets `hero` intensity with `--size-display` for the main title and `overflow: hidden` on `.slide`. These are the first impression of each section or the entire presentation.

## Layout Map

| Layout | Pattern | Slots | Motif | Key |
|--------|---------|-------|-------|-----|
| centered-hero | Centered Hero | title, subtitle | rule bottom-left + dot top-right | Display title centered with upward bias |
| split-image | Asymmetric Split | title, subtitle, image | dot top-right in text panel | 45/55 split, .img-treatment.img-desaturate, 3px accent divider |
| full-bleed-photo | Full Bleed | title, subtitle, image | rule top-right | .img-darken, text bottom-left, text-reversed colors |
| gradient-overlay | Full Bleed | title, subtitle, image | rule bottom-left | .img-gradient-fade, text bottom-left, gradient to --color-background |
| logo-focused | Centered Hero | title, subtitle, logo | rule bottom-center + dot top-right | Logo max-height:80px centered above title |
| minimal-text | Minimal Statement | title | rule bottom-left | Single title only, max whitespace, offset from center |
| asymmetric | Asymmetric Split | title, subtitle | dot top-right | 60/40 text split, left=title, right=subtitle with 0.04 opacity accent panel |
| editorial-spread | Editorial Spread | title, subtitle, image | vline at split point | 60% image left, 40% text right, .img-treatment.img-desaturate |

## Shared Rules for This Category
- ALL title slides use `hero` intensity
- ALL title slides use `--size-display` for the main title
- ALL title slides have `overflow: hidden` on `.slide`
- Subtitles use `--size-header` for dramatic scale contrast (4:1+)
- Each template includes exactly 2 motif elements

## Per-Layout Specifications

### centered-hero
**Pattern:** Centered Hero
**Intensity:** hero
**Slots:** title, subtitle
**Motif placement:**
- Rule at bottom-left for grounding
- Dot at top-right for balance
**Key design decisions:**
- Content vertically centered with slight upward bias (padding-bottom > padding-top)
- Max-width 1400px on content container
- z-index: 1 on content wrapper

### split-image
**Pattern:** Asymmetric Split
**Intensity:** hero
**Slots:** title, subtitle, image
**Motif placement:**
- Dot at top-right of text panel
**Key design decisions:**
- 45% image / 55% text split (never 50/50)
- Image wraps in `.img-treatment.img-desaturate`
- 3px accent divider line between panels
- Image bleeds to edge (zero padding)

### full-bleed-photo
**Pattern:** Full Bleed
**Intensity:** hero
**Slots:** title, subtitle, image
**Motif placement:**
- Rule at top-right for balance
**Key design decisions:**
- `.img-darken` treatment for text legibility
- Text positioned at bottom-left third
- Title and subtitle use white/light colors over dark image

### gradient-overlay
**Pattern:** Full Bleed
**Intensity:** hero
**Slots:** title, subtitle, image
**Motif placement:**
- Rule at bottom-left
**Key design decisions:**
- `.img-gradient-fade` treatment — gradient from transparent to --color-background
- Text positioned at bottom-left
- Gradient ensures text legibility without full darkening

### logo-focused
**Pattern:** Centered Hero
**Intensity:** hero
**Slots:** title, subtitle, logo
**Motif placement:**
- Rule at bottom-center
- Dot at top-right
**Key design decisions:**
- Logo centered above title, max-height: 80px
- Logo is NOT wrapped in .img-treatment (it's a brand asset)
- Subtle spacing between logo and title

### minimal-text
**Pattern:** Minimal Statement
**Intensity:** hero
**Slots:** title
**Motif placement:**
- Rule at bottom-left
**Key design decisions:**
- Single title only — no subtitle slot
- Maximum whitespace, content occupies <30% of slide
- Text offset from center for editorial feel

### asymmetric
**Pattern:** Asymmetric Split
**Intensity:** hero
**Slots:** title, subtitle
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- 60/40 text-only split (no image)
- Left panel: title at --size-display
- Right panel: subtitle with subtle accent background (0.04 opacity)
- Vertical divider between panels

### editorial-spread
**Pattern:** Editorial Spread
**Intensity:** hero
**Slots:** title, subtitle, image
**Motif placement:**
- Vertical line (vline) at the split point
**Key design decisions:**
- 60% image left, 40% text right
- Image wraps in `.img-treatment.img-desaturate`
- Overline for category context
- Dramatic size contrast between overline, title, and subtitle
