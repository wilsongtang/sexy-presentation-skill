# Structural Template Guide

## Category Overview
Structural slides provide navigation and organization within the deck. Section divider: large background number (600px, 6% opacity, real div). Transition: single sentence at `--size-title`.

## Layout Map

| Layout | Pattern | Intensity | Slots | Key |
|--------|---------|-----------|-------|-----|
| section-divider | Centered Hero | impact | section_number, section_title | 600px bg number, overline "Section N" |
| agenda | Magazine Flow | workhorse | title, agenda_1, agenda_2, agenda_3, agenda_4 | Numbered circles accent color |
| chapter-marker | Centered Hero | impact | chapter_number, chapter_title, chapter_subtitle | Similar to section-divider + subtitle |
| recap | Card Grid | workhorse | title, recap_1, recap_2, recap_3 | Key takeaway cards |
| toc | Magazine Flow | workhorse | title, toc_1, toc_2, toc_3, toc_4, toc_5 | Dot-leader rows |
| transition | Minimal Statement | impact | transition_text | Single sentence, max whitespace |

## Shared Rules for This Category
- Background numbers: real div elements, 600px font size, 6% opacity
- Numbered circles use accent color background with white number text
- All templates have `overflow: hidden` on `.slide`
- At least 1 motif element per template

## Per-Layout Specifications

### section-divider
**Pattern:** Centered Hero
**Intensity:** impact
**Slots:** section_number, section_title
**Motif placement:**
- Rule at bottom-left
- Dot at top-right
**Key design decisions:**
- 600px background number as real div, 6% opacity, centered
- "Section N" overline above title
- Title at --size-title
- Number behind content (z-index: 0, content z-index: 1)

### agenda
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** title, agenda_1, agenda_2, agenda_3, agenda_4
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Numbered circles (40px) with accent color background
- White number text centered in circle
- Items listed vertically with generous gap (24px)
- Item text at --size-body

### chapter-marker
**Pattern:** Centered Hero
**Intensity:** impact
**Slots:** chapter_number, chapter_title, chapter_subtitle
**Motif placement:**
- Rule at bottom-left
- Dot at top-right
**Key design decisions:**
- Similar to section-divider but with subtitle
- 600px background number, 6% opacity
- Title at --size-title, subtitle at --size-body
- Chapter number as overline context

### recap
**Pattern:** Card Grid
**Intensity:** workhorse
**Slots:** title, recap_1, recap_2, recap_3
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- 3-column card grid of key takeaways
- First card dominant (accent border)
- Cards have icon/number prefix
- Text at --size-body

### toc
**Pattern:** Magazine Flow
**Intensity:** workhorse
**Slots:** title, toc_1, toc_2, toc_3, toc_4, toc_5
**Motif placement:**
- Dot at bottom-right
**Key design decisions:**
- Dot-leader rows connecting item to page number
- Repeating dots as real characters (not pseudo-elements)
- Item text at --size-body
- Numbered items with accent color numbers

### transition
**Pattern:** Minimal Statement
**Intensity:** impact
**Slots:** transition_text
**Motif placement:**
- Rule at left edge
**Key design decisions:**
- Single sentence at --size-title
- Maximum whitespace — content <30% of slide
- Thin accent line below text (40px wide)
- Text offset from center for editorial feel
