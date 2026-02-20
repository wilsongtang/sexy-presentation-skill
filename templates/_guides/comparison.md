# Comparison Template Guide

## Category Overview
Comparison slides highlight differences. The right/pros/after panel gets `border: 2px solid var(--color-accent)` + accent heading. Left/cons/before gets `1px` border.

## Layout Map

| Layout | Pattern | Intensity | Slots | Key |
|--------|---------|-----------|-------|-----|
| side-by-side | Comparison Matrix | impact | title, left_heading, left_bullets, right_heading, right_bullets | Right panel dominant |
| pros-cons | Comparison Matrix | impact | title, pros_heading, pros_items, cons_heading, cons_items | Pros side dominant with accent |
| before-after | Comparison Matrix | impact | title, before_heading, before_body, after_heading, after_body | After side dominant |
| feature-matrix | Card Grid | workhorse | title, feature_1, feature_2, feature_3, feature_4, col_1_name, col_2_name | Accent checkmarks for featured column |
| versus | Comparison Matrix | impact | title, left_label, left_content, right_label, right_content, center_vs | "VS" at --size-stat as dominant |
| stacked-compare | Comparison Matrix | workhorse | title, item_1_label, item_1_value, item_2_label, item_2_value, item_3_label, item_3_value | Horizontal bars for values, first item dominant |

## Shared Rules for This Category
- Right/pros/after panel: `border: 2px solid var(--color-accent)` + accent heading color
- Left/cons/before panel: `border: 1px solid var(--color-border)` + standard heading
- Vertical divider between panels: real div, 1px width
- All templates have `overflow: hidden` on `.slide`
- At least 1 motif element per template

## Per-Layout Specifications

### side-by-side
**Pattern:** Comparison Matrix
**Intensity:** impact
**Slots:** title, left_heading, left_bullets, right_heading, right_bullets
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- Right panel dominant (accent border)
- Bullet items in each panel
- Panels have 16px border-radius, 48px padding
- Divider between panels

### pros-cons
**Pattern:** Comparison Matrix
**Intensity:** impact
**Slots:** title, pros_heading, pros_items, cons_heading, cons_items
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- Pros (right) side dominant with accent treatment
- Cons (left) side subdued
- Each item prefixed with icon/symbol

### before-after
**Pattern:** Comparison Matrix
**Intensity:** impact
**Slots:** title, before_heading, before_body, after_heading, after_body
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- After (right) side dominant with accent treatment
- Arrow or transition indicator between panels
- Body text at --size-body

### feature-matrix
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, feature rows, col_1_name, col_2_name
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Table-like layout with feature rows
- Featured column gets accent checkmarks
- Row borders using var(--color-border)
- Header row with accent background

### versus
**Pattern:** Comparison Matrix
**Intensity:** impact
**Slots:** title, left_label, left_content, right_label, right_content, center_vs
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- "VS" text at --size-stat as dominant element between panels
- "VS" uses accent color, 800 weight
- Equal panels on either side
- Both panels have borders but right has accent

### stacked-compare
**Pattern:** Comparison Matrix
**Intensity:** workhorse
**Slots:** title, 3x(item_N_label, item_N_value)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Vertical stack of comparison bars
- Horizontal bars as real divs with width percentages
- First item dominant (accent color bar)
- Others use muted color bars
