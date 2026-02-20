---
name: Polish Graphics
description: Apply targeted fixes to slides based on the Art Director QA report. Remediates critical, high, and medium severity issues, then runs a final consistency verification pass across the full presentation.
version: 0.1.0
---

# Polish Graphics Skill

## Purpose

Take the structured Issue Report from `qa-art-director` and systematically apply fixes to each affected slide. After all fixes are applied, run a lightweight final consistency check to ensure no new issues were introduced and that the presentation is visually coherent end-to-end.

## Inputs

- Issue Report JSON from `qa-art-director` skill
- Assembled presentation HTML (the slides to be edited)
- Slide Plan array (for reference on intended design intent)
- Theme CSS variable block
- Brand profile JSON (if available)

## Remediation Process

### Step 1: Triage Issues

Sort the Issue Report by severity: `critical` → `high` → `medium`.

For each issue, determine the remediation strategy:

| Issue type | Remediation strategy |
|---|---|
| Text overflow | Reduce font size, shorten text, or split slide |
| Contrast failure | Adjust text or background color token |
| Off-brand color | Replace with correct brand token |
| Missing image | Re-trigger `source-imagery` for that slot |
| Layout misalignment | Adjust CSS Grid/Flex values |
| Inconsistent title style | Normalize via CSS rule override |
| Forbidden font | Replace with approved font |
| Logo missing/misplaced | Inject logo element at correct position |
| Broken image | Fetch replacement via `source-imagery` |

### Step 2: Apply Fixes Slide by Slide

For each issue in the triage order:

1. Identify the affected slide index and CSS selector from `issue.affected_element`
2. Load the current HTML fragment for that slide
3. Apply the fix (CSS override, content edit, element addition/removal)
4. Re-run the `design-slide` quality checklist for that slide only (not the full skill)
5. Mark the issue as resolved in a running `fixes_applied` log

#### Common Fix Patterns

**Fix: Text Overflow (L2)**
```css
/* Add to slide's scoped style block */
.slide[data-index="N"] .slide-body {
  overflow: hidden;
  font-size: clamp(0.875rem, 1.25vw, 1.1rem); /* one step down */
}
```
If content is still too dense after font reduction, split the slide into two slides and update the Slide Plan accordingly.

**Fix: Contrast Failure (C1)**
Compute the contrast ratio between the failing color pair. Adjust the lighter color in the pair by increasing lightness in HSL space until the ratio reaches 4.5:1 for body text or 3:1 for large headings.

```javascript
// Pseudo-code for contrast adjustment
function lightenToMeetContrast(textColor, bgColor, targetRatio) {
  let hsl = hexToHSL(textColor);
  while (contrastRatio(hslToHex(hsl), bgColor) < targetRatio) {
    hsl.l = Math.min(hsl.l + 2, 100);
  }
  return hslToHex(hsl);
}
```

Apply the adjusted color as a scoped CSS override on the affected element — do not modify the global theme variable, as other slides may use it correctly.

**Fix: Missing or Broken Image (I1)**
Re-invoke the `source-imagery` skill for the specific slot:
- Pass the original art direction brief (from the slide's `images[].alt` field)
- Request a new image
- Inject the resolved image URL/base64 into the slide HTML

**Fix: Inconsistent Title Style (X1)**
Audit all slide titles and extract the most common style (font, size, color, position). Apply that style as a global rule for `.slide-title` in the presentation's shared CSS, then remove any per-slide overrides that deviate.

**Fix: Logo Missing (B2)**
Inject the logo `<img>` element at the correct position (from `brand_profile.logo.preferred_placement`) with the specified safe area:

```html
<div class="slide-logo" style="
  position: absolute;
  top: var(--logo-safe-area, 24px);
  left: var(--logo-safe-area, 24px);
">
  <img src="[brand_profile.logo.primary_url]"
       alt="[brand_name] logo"
       height="40" />
</div>
```

**Fix: Font Size Hierarchy (T5)**
If a slide's heading uses a non-standard size, replace the inline size with the appropriate CSS variable reference:
- Main title → `var(--font-size-heading-xl)`
- Subtitle → `var(--font-size-heading-lg)`
- Section heading → `var(--font-size-heading-md)`
- Body → `var(--font-size-body)`

### Step 3: Handle Low-Severity and Suggestions

For issues with severity `low` or `suggestion`:

1. Present each to the user with a brief description and the suggested fix
2. Apply fixes that the user approves
3. Skip fixes that the user declines
4. Note skipped items in the final report

### Step 4: Re-render Affected Slides

After all fixes are applied, re-render any slide whose HTML was modified by calling `design-slide` for that slide with the updated content. This ensures the quality checklist is re-run and the fix did not introduce new issues.

## Final Consistency Verification

After all individual fixes are applied, run a lightweight consistency pass across the complete presentation:

### Consistency Checks

| Check | Method |
|---|---|
| **Title position uniformity** | Compare bounding box top/left of `.slide-title` across all slides — flag deviation > 4px |
| **Color token adherence** | Scan all `style` attributes and `<style>` blocks for hardcoded hex values not in the theme palette |
| **Font family uniformity** | Confirm only theme-specified fonts appear in computed styles |
| **Image fill consistency** | Verify all image-slot images use `object-fit: cover` |
| **Spacing rhythm** | Spot-check that padding/margin values are multiples of `--spacing-tight` (16px) |
| **Slide count integrity** | Confirm final slide count matches the Slide Plan's `total_slides` |
| **Data slide accuracy** | Confirm chart/table HTML contains the correct data (spot-check 3 data slides) |

### Consistency Report

```json
{
  "consistency_check": {
    "passed": true,
    "checked_at": "ISO8601 timestamp",
    "slides_checked": 14,
    "new_issues_found": 0,
    "checks": {
      "title_position_uniformity": "pass",
      "color_token_adherence": "pass",
      "font_family_uniformity": "pass",
      "image_fill_consistency": "pass",
      "spacing_rhythm": "pass",
      "slide_count_integrity": "pass",
      "data_slide_accuracy": "pass"
    }
  }
}
```

If `new_issues_found > 0`, log them and apply fixes before declaring the pass complete. Do not iterate more than 3 times — if issues persist after 3 rounds, surface them to the user with a description.

## Output Format

Return a Polish Report:

```json
{
  "polish_summary": {
    "issues_received": 13,
    "issues_resolved": 11,
    "issues_skipped_user": 2,
    "slides_modified": ["slide-3", "slide-7", "slide-11"],
    "consistency_check_passed": true,
    "presentation_ready": true,
    "polished_at": "ISO8601 timestamp"
  },
  "fixes_applied": [
    {
      "issue_id": "QA-001",
      "slide_index": 3,
      "fix_applied": "Reduced body font size from 1.25rem to 1.05rem. Content no longer overflows at 1280px.",
      "resolved": true
    }
  ],
  "unresolved_issues": [],
  "user_skipped": [
    {
      "issue_id": "QA-009",
      "reason": "User declined — prefers current layout"
    }
  ]
}
```

Pass the polished presentation HTML and the Polish Report back to the main `presentation` skill. The presentation is now ready for the playground step and final export.
