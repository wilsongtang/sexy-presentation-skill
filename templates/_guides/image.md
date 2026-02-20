# Image Template Guide

## Category Overview
Image slides let visuals dominate. ALL `<img>` tags wrap in `.img-treatment`. Motifs are minimal on image slides to avoid competing with the visuals.

## Layout Map

| Layout | Pattern | Intensity | Slots | Treatment | Key |
|--------|---------|-----------|-------|-----------|-----|
| full-bleed | Full Bleed | hero | image, caption | .img-darken | Caption bottom-left, text-reversed |
| half-bleed-left | Asymmetric Split | impact | image, title, body | .img-desaturate | 45% image left |
| half-bleed-right | Asymmetric Split | impact | image, title, body | .img-desaturate | 45% image right |
| gallery-2x2 | Card Grid | workhorse | title, image_1, image_2, image_3, image_4, caption | .img-color-wash | 2x2 grid, all same treatment |
| gallery-strip | Edge Tension | workhorse | title, image_1, image_2, image_3, image_4 | .img-color-wash | Horizontal strip, images bleed to edges |
| captioned-center | Centered Hero | impact | image, title, caption | .img-desaturate | Centered image 60% width, title below |
| before-after | Comparison Matrix | impact | title, before_image, after_image, before_label, after_label | .img-desaturate | "After" gets accent treatment |
| overlapping-cards | Layered Stack | impact | title, image_1, image_2, image_3 | .img-color-wash | Center z-index:3, flanking +/-6deg |

## Shared Rules for This Category
- EVERY `<img>` tag wraps in `.img-treatment` container
- All `<img>` tags MUST have `alt` attribute with slot or descriptive text
- Motifs are minimal (1-2 elements max)
- All templates have `overflow: hidden` on `.slide`

## Per-Layout Specifications

### full-bleed
**Pattern:** Full Bleed
**Intensity:** hero
**Slots:** image, caption
**Treatment:** .img-darken
**Motif placement:**
- Rule at top-right
**Key design decisions:**
- Image covers entire 1920x1080, zero padding
- Caption at bottom-left with reversed text colors
- Uses --size-display for the title at bottom-left

### half-bleed-left
**Pattern:** Asymmetric Split
**Intensity:** impact
**Slots:** image, title, body
**Treatment:** .img-desaturate
**Motif placement:**
- Dot in text panel top-right
**Key design decisions:**
- 45% image left, 55% text right
- 3px accent divider between panels
- Image bleeds to left edge

### half-bleed-right
**Pattern:** Asymmetric Split
**Intensity:** impact
**Slots:** image, title, body
**Treatment:** .img-desaturate
**Motif placement:**
- Dot in text panel top-left
**Key design decisions:**
- 55% text left, 45% image right
- 3px accent divider between panels
- Image bleeds to right edge

### gallery-2x2
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, image_1, image_2, image_3, image_4, caption
**Treatment:** .img-color-wash
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 2x2 grid of images, all same treatment
- 8px gap between images
- Title above, caption below
- All images get border-radius: 8px

### gallery-strip
**Pattern:** Edge Tension
**Intensity:** workhorse
**Slots:** title, image_1, image_2, image_3, image_4
**Treatment:** .img-color-wash
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- Horizontal strip of images
- Images bleed to left and right edges (zero padding on sides)
- Title above the strip
- Equal image widths

### captioned-center
**Pattern:** Centered Hero
**Intensity:** impact
**Slots:** image, title, caption
**Treatment:** .img-desaturate
**Motif placement:**
- Rule at bottom
**Key design decisions:**
- Centered image at 60% width
- Title below image at --size-title
- Caption at --size-caption
- Generous whitespace around image

### before-after
**Pattern:** Comparison Matrix
**Intensity:** impact
**Slots:** title, before_image, after_image, before_label, after_label
**Treatment:** .img-desaturate
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- "After" side gets accent border treatment (2px vs 1px)
- Vertical divider between panels
- Labels below each image
- Both images same treatment

### overlapping-cards
**Pattern:** Layered Stack
**Intensity:** impact
**Slots:** title, image_1, image_2, image_3
**Treatment:** .img-color-wash
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Center card z-index:3, flanking z-index:1-2
- Flanking cards rotated +/-6deg
- 4px white borders on all cards for separation
- Shadow depth increases with z-index
- Negative margins for overlap effect
