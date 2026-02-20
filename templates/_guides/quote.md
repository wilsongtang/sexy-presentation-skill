# Quote Template Guide

## Category Overview
Quote slides feature spoken words and attributions. Decorative quotation marks: 320px, accent color, 12% opacity, real div elements. Quote text: `--size-title`, italic, header font.

## Layout Map

| Layout | Pattern | Intensity | Slots | Key |
|--------|---------|-----------|-------|-----|
| large-centered | Minimal Statement | impact | quote_text, attribution | Decorative marks above/below, max-width 1400px |
| sidebar-portrait | Asymmetric Split | impact | quote_text, attribution, image | 40% image, .img-treatment.img-desaturate |
| minimal | Minimal Statement | impact | quote_text, attribution | No decorative marks, thin accent line only |
| stacked | Magazine Flow | workhorse | quote_1_text, quote_1_attribution, quote_2_text, quote_2_attribution | First quote dominant (larger font) |
| editorial | Editorial Spread | impact | quote_text, attribution, context | Column layout with divider |

## Shared Rules for This Category
- Quote text: `--size-title`, italic, `font-family: var(--font-header)`
- Attribution: uppercase, letter-spacing 0.08em, em-dash prefix, `--size-caption`
- Decorative quotation marks: real div elements (NOT pseudo-elements), 320px, accent color, 12% opacity
- All templates have `overflow: hidden` on `.slide`
- At least 1 motif element per template

## Per-Layout Specifications

### large-centered
**Pattern:** Minimal Statement
**Intensity:** impact
**Slots:** quote_text, attribution
**Motif placement:**
- Rule at left edge (vertical)
**Key design decisions:**
- Decorative opening quote mark above (320px, accent, 12% opacity)
- Decorative closing quote mark below (same)
- Quote text centered, max-width 1400px
- Attribution below with em-dash prefix
- Generous whitespace

### sidebar-portrait
**Pattern:** Asymmetric Split
**Intensity:** impact
**Slots:** quote_text, attribution, image
**Motif placement:**
- Dot in text panel
**Key design decisions:**
- 40% image left, 60% quote right
- Image wraps in `.img-treatment.img-desaturate`
- 3px accent divider between panels
- Quote text at --size-title in text panel
- Decorative quote mark in text panel

### minimal
**Pattern:** Minimal Statement
**Intensity:** impact
**Slots:** quote_text, attribution
**Motif placement:**
- Rule at left edge
**Key design decisions:**
- NO decorative quotation marks
- Only a thin 40px accent line below quote
- Maximum whitespace — content <30% of slide
- Quote text offset from center

### stacked
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** 2x(quote_N_text, quote_N_attribution)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Two quotes stacked vertically
- First quote is dominant (--size-title font)
- Second quote is smaller (--size-body)
- Divider between quotes
- First quote has decorative mark

### editorial
**Pattern:** Editorial Spread
**Intensity:** impact
**Slots:** quote_text, attribution, context
**Motif placement:**
- Vertical line at split point
**Key design decisions:**
- Two-column layout: quote left, context right
- Column rule divider
- Quote text at --size-title
- Context at --size-body, provides background
- Decorative quote mark in quote column
