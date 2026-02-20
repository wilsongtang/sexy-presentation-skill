# Closing Template Guide

## Category Overview
Closing slides wrap up the presentation. thank-you and cta use `--size-display` (hero). contact/social are workhorse. Hero closings get radial gradient accent (5% opacity).

## Layout Map

| Layout | Pattern | Intensity | Slots | Key |
|--------|---------|-----------|-------|-----|
| thank-you | Centered Hero | hero | subtitle | "Thank You" hardcoded at display, subtitle is slot |
| contact | Card Grid | workhorse | title, name, email, phone, website | Icon + text pairs in card grid |
| cta | Centered Hero | hero | cta_text, cta_subtitle | CTA text at display size |
| social | Card Grid | workhorse | title, platform_1, handle_1, platform_2, handle_2, platform_3, handle_3, platform_4, handle_4 | Horizontal icon row |
| qr-code | Centered Hero | impact | title, qr_image, url | QR NOT in .img-treatment |

## Shared Rules for This Category
- Hero closing slides (thank-you, cta) get subtle radial gradient accent (5% opacity)
- "Thank You" text is hardcoded (not a slot)
- QR code images are NOT wrapped in .img-treatment
- All templates have `overflow: hidden` on `.slide`
- At least 1 motif element per template

## Per-Layout Specifications

### thank-you
**Pattern:** Centered Hero
**Intensity:** hero
**Slots:** subtitle
**Motif placement:**
- Rule at bottom-left
- Dot at top-right
**Key design decisions:**
- "Thank You" hardcoded at --size-display, not a slot
- Subtitle is the only user-provided slot
- Radial gradient accent background (5% opacity, centered)
- Generous whitespace

### contact
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, name, email, phone, website
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Card grid with icon + text pairs
- Each contact method in its own card
- First card (name) dominant with accent border
- Icons as simple SVG or Unicode symbols

### cta
**Pattern:** Centered Hero
**Intensity:** hero
**Slots:** cta_text, cta_subtitle
**Motif placement:**
- Rule at bottom-left
- Dot at top-right
**Key design decisions:**
- CTA text at --size-display
- Subtitle at --size-header
- Radial gradient accent background (5% opacity)
- Centered layout with dramatic scale contrast

### social
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 4x(platform_N, handle_N)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Horizontal row of social cards
- Each card: platform name + handle
- First card accent border (dominant)
- Compact card layout

### qr-code
**Pattern:** Centered Hero
**Intensity:** impact
**Slots:** title, qr_image, url
**Motif placement:**
- Rule at bottom
- Dot at top-right
**Key design decisions:**
- QR image centered, NOT wrapped in .img-treatment
- QR image max-width: 300px
- Title above at --size-title
- URL below at --size-caption, muted color
- Generous whitespace around QR
