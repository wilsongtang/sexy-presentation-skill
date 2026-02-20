# Data Template Guide

## Category Overview
Data slides make numbers dominant. Stats use `--size-stat` with accent color and 800 weight. Single-stat layouts get `impact`, dashboards get `workhorse`.

## Layout Map

| Layout | Pattern | Intensity | Slots | Key |
|--------|---------|-----------|-------|-----|
| big-stat-single | Data Spotlight | impact | stat_number, stat_label, stat_context | Stat at --size-stat, centered |
| big-stat-triple | Data Spotlight | impact | stat_1_number, stat_1_label, stat_2_number, stat_2_label, stat_3_number, stat_3_label | Middle stat dominant (1.15x + accent border) |
| metric-grid | Card Grid | workhorse | title, metric_1_value, metric_1_label, metric_2_value, metric_2_label, metric_3_value, metric_3_label, metric_4_value, metric_4_label | 2x2 card grid, first card dominant |
| chart-placeholder | Magazine Flow | workhorse | title, chart_description | Chart area placeholder div with dashed border |
| bar-comparison | Data Spotlight | impact | title, bar_1_label, bar_1_value, bar_2_label, bar_2_value, bar_3_label, bar_3_value | Horizontal bars as real divs with width % |
| percentage-ring | Data Spotlight | impact | title, percentage, label, context | CSS conic-gradient ring, not SVG |
| data-table | Magazine Flow | workhorse | title, table_content | Zebra striping var(--color-secondary) even rows |
| kpi-dashboard | Card Grid | workhorse | title, kpi_1_value, kpi_1_label, kpi_2_value, kpi_2_label, kpi_3_value, kpi_3_label, kpi_4_value, kpi_4_label | 2x2 metric card grid |

## Shared Rules for This Category
- Stat numbers: `--size-stat`, font-weight: 800, accent color, tight letter-spacing (-2px)
- All data slides include at least 1 motif element
- All templates have `overflow: hidden` on `.slide`
- Card layouts: first card gets accent border treatment

## Per-Layout Specifications

### big-stat-single
**Pattern:** Data Spotlight
**Intensity:** impact
**Slots:** stat_number, stat_label, stat_context
**Motif placement:**
- Rule at bottom-center for grounding
**Key design decisions:**
- Stat number at --size-stat, accent color, 800 weight
- Centered layout with overline context
- Label below at --size-header
- Context at --size-body, muted color

### big-stat-triple
**Pattern:** Data Spotlight
**Intensity:** impact
**Slots:** 3x(stat_N_number, stat_N_label)
**Motif placement:**
- Rule at bottom for grounding
**Key design decisions:**
- Three stats in a row
- Middle stat is dominant: flex:1.15, accent border, slightly larger text
- Flanking stats use standard border
- All stats at --size-stat with 800 weight

### metric-grid
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 4x(metric_N_value, metric_N_label)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 2x2 card grid
- First card gets accent border (dominant)
- Values at --size-header, labels at --size-caption

### chart-placeholder
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** title, chart_description
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Large chart area with dashed border (2px dashed var(--color-border))
- Chart area takes 70% of slide height
- Description below chart area at --size-caption

### bar-comparison
**Pattern:** Data Spotlight
**Intensity:** impact
**Slots:** title, 3x(bar_N_label, bar_N_value)
**Motif placement:**
- Rule at bottom
**Key design decisions:**
- Horizontal bars as real div elements
- Bar width set as percentage
- First bar uses accent color, others use muted color
- Labels at --size-body, values at --size-header

### percentage-ring
**Pattern:** Data Spotlight
**Intensity:** impact
**Slots:** title, percentage, label, context
**Motif placement:**
- Rule at bottom
**Key design decisions:**
- CSS conic-gradient ring (NOT SVG)
- Ring size: 300px
- Percentage number centered inside ring at --size-stat
- Border-radius: 50% to create circle

### data-table
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** title, table_content
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Zebra striping with var(--color-secondary) on even rows
- Header row uses accent color background
- Cell padding: 16px 24px
- Font-size: --size-caption for table data

### kpi-dashboard
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 4x(kpi_N_value, kpi_N_label)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 2x2 metric card grid
- First card accent border (dominant)
- Values at --size-header, labels at --size-caption
- Compact card padding (32px)
