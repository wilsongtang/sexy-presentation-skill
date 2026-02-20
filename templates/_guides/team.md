# Team Template Guide

## Category Overview
Team slides showcase people. Featured member: 2px accent border, 6px accent top stripe, 200px avatar. Grid members: 1px border, 80px avatar. First grid member gets accent treatment (dominant).

## Layout Map

| Layout | Pattern | Intensity | Slots | Key |
|--------|---------|-----------|-------|-----|
| featured | Asymmetric Split | impact | title, featured_name, featured_role, featured_bio, member_1_name, member_1_role, member_2_name, member_2_role, member_3_name, member_3_role | Featured 2:1 flex, accent border |
| grid-4 | Card Grid | workhorse | title, member_1_name, member_1_role, member_2_name, member_2_role, member_3_name, member_3_role, member_4_name, member_4_role | First card accent, 80px avatars |
| grid-6 | Card Grid | workhorse | title, member_1_name, member_1_role, member_2_name, member_2_role, member_3_name, member_3_role, member_4_name, member_4_role, member_5_name, member_5_role, member_6_name, member_6_role | First card accent, 2x3 grid |
| org-chart | Timeline Flow | workhorse | title, leader_name, leader_role, report_1_name, report_1_role, report_2_name, report_2_role, report_3_name, report_3_role | Connecting lines as real divs |
| profiles | Card Grid | workhorse | title, profile_1_name, profile_1_role, profile_1_bio, profile_2_name, profile_2_role, profile_2_bio, profile_3_name, profile_3_role, profile_3_bio | First card accent, includes bio |

## Shared Rules for This Category
- SVG person icon placeholders (NOT image slots) for avatars
- Featured member: 2px accent border, 6px accent top stripe, 200px avatar
- Grid members: 1px border, 80px avatar
- First grid member gets accent treatment (dominant)
- All templates have `overflow: hidden` on `.slide`
- At least 1 motif element per template

## Per-Layout Specifications

### featured
**Pattern:** Asymmetric Split
**Intensity:** impact
**Slots:** title, featured_name, featured_role, featured_bio, 3x(member_N_name, member_N_role)
**Motif placement:**
- Dot at top-right
**Key design decisions:**
- Featured member takes 2:1 flex ratio
- Featured card: 2px accent border, 6px accent top stripe
- 200px SVG avatar placeholder in featured card
- Supporting members in column to the right (80px avatars)
- Featured bio at --size-body

### grid-4
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 4x(member_N_name, member_N_role)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 2x2 grid of member cards
- First card accent border (dominant)
- 80px SVG avatar per card
- Name at --size-body, role at --size-caption
- Cards have 16px border-radius

### grid-6
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 6x(member_N_name, member_N_role)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 2 rows x 3 columns
- First card accent border (dominant)
- 80px SVG avatar per card
- Compact padding for 6-member layout
- Name at --size-body, role at --size-caption

### org-chart
**Pattern:** Timeline Flow
**Intensity:** workhorse
**Slots:** title, leader_name, leader_role, 3x(report_N_name, report_N_role)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Leader at top, reports below
- Connecting lines as real div elements (3px, var(--color-border))
- Leader card: accent border (dominant), 120px avatar
- Report cards: standard border, 80px avatars
- Vertical then horizontal line structure

### profiles
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, 3x(profile_N_name, profile_N_role, profile_N_bio)
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 3-column profile cards
- First card accent border (dominant)
- 80px SVG avatar per card
- Includes bio text at --size-caption
- Cards have generous padding (40px)
