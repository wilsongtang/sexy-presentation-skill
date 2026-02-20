# Content Template Guide

## Category Overview
Content slides are workhorse — title uses `--size-header`, body uses `--size-body`. Exception: magazine-flow gets `impact` intensity. These slides carry the bulk of presentation information.

## Layout Map

| Layout | Pattern | Intensity | Slots | Motif | Key |
|--------|---------|-----------|-------|-------|-----|
| single-column | Magazine Flow | workhorse | title, body | dot bottom-right | Simple title + body, max-width 1400px |
| two-column | Magazine Flow | workhorse | title, col_1, col_2 | dot bottom-right | 55/45 column split with 1px divider |
| three-column | Card Grid | workhorse | title, col_1, col_2, col_3 | dot bottom-right | First col flex:1.15 + accent border |
| icon-grid-2x2 | Card Grid | workhorse | title, icon_1_title, icon_1_body, icon_2_title, icon_2_body, icon_3_title, icon_3_body, icon_4_title, icon_4_body | dot bottom-right | 2x2 grid, first card dominant |
| icon-grid-2x3 | Card Grid | workhorse | title, icon_1_title, icon_1_body, icon_2_title, icon_2_body, icon_3_title, icon_3_body, icon_4_title, icon_4_body, icon_5_title, icon_5_body, icon_6_title, icon_6_body | dot bottom-right | 2x3 grid, first card dominant |
| icon-grid-3x3 | Card Grid | workhorse | title, icon_1_title, icon_1_body, icon_2_title, icon_2_body, icon_3_title, icon_3_body, icon_4_title, icon_4_body, icon_5_title, icon_5_body, icon_6_title, icon_6_body, icon_7_title, icon_7_body, icon_8_title, icon_8_body, icon_9_title, icon_9_body | dot bottom-right | 3x3 grid, headings at --size-caption |
| numbered-list | Magazine Flow | workhorse | title, item_1, item_2, item_3, item_4, item_5, item_6 | rule bottom-left | Numbered circles with accent color |
| card-layout | Card Grid | workhorse | title, card_1_title, card_1_body, card_2_title, card_2_body, card_3_title, card_3_body | dot bottom-right | 3-column cards, first dominant |
| magazine-flow | Magazine Flow | impact | title, body, pull_quote | vline bottom-right | 60/40 columns, pull quote as dominant |
| sidebar-content | Asymmetric Split | workhorse | title, body, sidebar | dot sidebar-top | 65/35 split, sidebar has accent top bar |
| text-image-left | Asymmetric Split | workhorse | title, body, image | dot text-panel | 45% image left, .img-treatment.img-desaturate |
| text-image-right | Asymmetric Split | workhorse | title, body, image | dot text-panel | 45% image right, .img-treatment.img-desaturate |

## Shared Rules for This Category
- Title uses `--size-header` (NOT display or title)
- Body text uses `--size-body` with `line-height: var(--line-height)`
- Card Grid layouts: first card gets `flex: 1.15` + `border: 2px solid var(--color-accent)`
- Image slots use `.img-treatment.img-desaturate` wrapper
- Each template includes at least 1 motif element
- All templates have `overflow: hidden` on `.slide`

## Per-Layout Specifications

### single-column
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** title, body
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Simple title + body layout
- Body max-width 1400px for readability
- Line-height 1.7 for body text

### two-column
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** title, col_1, col_2
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 55/45 column split (not equal)
- 1px divider between columns
- Both columns use --size-body

### three-column
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, col_1, col_2, col_3
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- First column gets flex:1.15 + accent border (dominant)
- Other columns get flex:1 + standard border
- 16px border-radius on columns

### icon-grid-2x2
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 4x(icon_N_title, icon_N_body)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 2x2 grid layout using CSS grid or flex-wrap
- First card is dominant (accent border)
- Decorative accent square (56x56px) in each card

### icon-grid-2x3
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 6x(icon_N_title, icon_N_body)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 2 rows x 3 columns
- First card dominant
- Heading at --size-body, description at --size-caption

### icon-grid-3x3
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 9x(icon_N_title, icon_N_body)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 3x3 grid — dense layout
- Headings drop to --size-caption
- Compact padding (24px)

### numbered-list
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** title, item_1 through item_6
**Motif placement:**
- Rule at bottom-left
**Key design decisions:**
- Numbered circles (40px) with accent color background
- Number in white, centered in circle
- Items listed vertically with generous gap

### card-layout
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 3x(card_N_title, card_N_body)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 3-column card grid
- First card dominant (accent border)
- Each card has decorative accent square

### magazine-flow
**Pattern:** Magazine Flow
**Intensity:** impact
**Slots:** title, body, pull_quote
**Motif placement:**
- Vertical line at bottom-right
**Key design decisions:**
- 60/40 column split
- Pull quote in side column is the dominant element
- Pull quote uses --size-header, italic, accent color border-left
- Body uses generous line-height (1.7)

### sidebar-content
**Pattern:** Asymmetric Split
**Intensity:** workhorse
**Slots:** title, body, sidebar
**Motif placement:**
- Dot at top of sidebar panel
**Key design decisions:**
- 65/35 main/sidebar split
- Sidebar has 4px accent top stripe
- Sidebar background: 0.03 opacity accent color

### text-image-left
**Pattern:** Asymmetric Split
**Intensity:** workhorse
**Slots:** title, body, image
**Motif placement:**
- Dot in text panel
**Key design decisions:**
- 45% image left, 55% text right
- Image wraps in `.img-treatment.img-desaturate`
- 3px accent divider between panels
- Image bleeds to left edge

### text-image-right
**Pattern:** Asymmetric Split
**Intensity:** workhorse
**Slots:** title, body, image
**Motif placement:**
- Dot in text panel
**Key design decisions:**
- 55% text left, 45% image right
- Image wraps in `.img-treatment.img-desaturate`
- 3px accent divider between panels
- Image bleeds to right edge
