# Timeline Template Guide

## Category Overview
Timeline slides show sequential events, processes, and progressions. Connecting lines are real divs (NOT pseudo-elements). Active dots are filled accent (20px). Future dots are border-only, transparent.

## Layout Map

| Layout | Pattern | Intensity | Slots | Key |
|--------|---------|-----------|-------|-----|
| horizontal | Timeline Flow | workhorse | title, point_1_date, point_1_label, point_2_date, point_2_label, point_3_date, point_3_label, point_4_date, point_4_label, point_5_date, point_5_label | Labels alternate above/below |
| vertical | Timeline Flow | workhorse | title, point_1_date, point_1_title, point_1_body, point_2_date, point_2_title, point_2_body, point_3_date, point_3_title, point_3_body, point_4_date, point_4_title, point_4_body | Labels alternate left/right |
| milestone | Timeline Flow | impact | title, milestone_1_date, milestone_1_title, milestone_1_body, milestone_2_date, milestone_2_title, milestone_2_body, milestone_3_date, milestone_3_title, milestone_3_body | Larger cards, first/active dominant |
| roadmap | Timeline Flow | workhorse | title, phase_1_title, phase_1_body, phase_2_title, phase_2_body, phase_3_title, phase_3_body, phase_4_title, phase_4_body | Phase cards with accent top stripe on first |
| steps | Timeline Flow | workhorse | title, step_1_number, step_1_title, step_1_body, step_2_number, step_2_title, step_2_body, step_3_number, step_3_title, step_3_body, step_4_number, step_4_title, step_4_body | Numbered circles as dominant elements |
| branching | Timeline Flow | workhorse | title, trunk, branch_1_label, branch_1_items, branch_2_label, branch_2_items | Trunk line splits to branches |

## Shared Rules for This Category
- Connecting lines: real div with `background: var(--color-border)`, 3px width/height
- Active dots: filled accent, 20px diameter, border-radius: 50%
- Future dots: border-only (2px solid var(--color-border)), transparent fill, 16px diameter
- First or active step is dominant (accent border/fill + larger element)
- All templates have `overflow: hidden` on `.slide`
- At least 1 motif element per template

## Per-Layout Specifications

### horizontal
**Pattern:** Timeline Flow
**Intensity:** workhorse
**Slots:** title, 5x(point_N_date, point_N_label)
**Motif placement:**
- Dot at start of timeline line
**Key design decisions:**
- Horizontal connecting line across slide
- Labels alternate above/below the line
- First point is active (filled accent dot)
- Others are border-only dots
- Date at --size-caption, label at --size-body

### vertical
**Pattern:** Timeline Flow
**Intensity:** workhorse
**Slots:** title, 4x(point_N_date, point_N_title, point_N_body)
**Motif placement:**
- Dot at top of timeline
**Key design decisions:**
- Vertical connecting line on left side
- Content alternates left/right of the line
- First point active (filled accent)
- Date at --size-caption, title at --size-body, body at --size-caption

### milestone
**Pattern:** Timeline Flow
**Intensity:** impact
**Slots:** title, 3x(milestone_N_date, milestone_N_title, milestone_N_body)
**Motif placement:**
- Rule at bottom
**Key design decisions:**
- Larger milestone cards (vs simple dots)
- First/active milestone has accent border + larger dot
- Cards have 16px border-radius, 32px padding
- Connecting line between milestone cards

### roadmap
**Pattern:** Timeline Flow
**Intensity:** workhorse
**Slots:** title, 4x(phase_N_title, phase_N_body)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Phase cards in horizontal row
- First phase has 4px accent top stripe (dominant)
- Others have standard border
- Connecting arrows between phases

### steps
**Pattern:** Timeline Flow
**Intensity:** workhorse
**Slots:** title, 4x(step_N_number, step_N_title, step_N_body)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Numbered circles (56px) as dominant elements
- First step number uses accent fill
- Others use border-only circles
- Step number at --size-header, white text on accent
- Connecting line between circles

### branching
**Pattern:** Timeline Flow
**Intensity:** workhorse
**Slots:** title, trunk, branch_1_label, branch_1_items, branch_2_label, branch_2_items
**Motif placement:**
- Dot at bottom
**Key design decisions:**
- Trunk line vertical, splits to 2 horizontal branches
- Branch points have accent dots
- Each branch has a label card
- Lines as real div elements (3px wide)
