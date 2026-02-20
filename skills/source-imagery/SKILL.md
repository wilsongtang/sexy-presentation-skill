---
name: Source Imagery
description: Source high-quality images for presentation slides using three modes — art direction briefs, Unsplash search via fetch-images.js, and AI image-generation prompts. Applies presentation-specific image guidelines.
version: 0.1.0
---

# Source Imagery Skill

## Purpose

Provide a resolved image (URL or base64 blob) for every image slot in the Slide Plan that has `needs_imagery: true` or a null `src` in its images array. Produce images that are compositionally suited for slide backgrounds, panels, and inline placements.

## Three Sourcing Modes

### Mode 1: Art Direction Brief

Use this mode when the image slot has a descriptive `alt` text or `design_notes` that suggest a specific scene, mood, or subject.

An art direction brief is a short, precise description of the desired image that can be used as a search query or generation prompt. Write briefs in the following format:

```
Subject: [main subject or scene]
Mood: [emotional tone — dramatic, calm, energetic, etc.]
Lighting: [golden hour, studio, moody overcast, etc.]
Color palette: [dominant colors that complement the theme]
Composition: [rule of thirds, centered, wide angle, portrait, etc.]
Usage: [full bleed background, right panel, inline square]
Avoid: [anything to exclude — people, text, logos, clutter]
```

Example brief:

```
Subject: Empty modern conference room with city skyline view
Mood: Calm, aspirational
Lighting: Soft natural light, late afternoon
Color palette: Blues and greys to complement midnight-bold theme
Composition: Wide angle, slight low angle, shallow depth of field
Usage: Full bleed background, text will overlay left 40%
Avoid: People, visible branding, clutter on tables
```

### Mode 2: Unsplash Search

Use Unsplash for photographic images when the brief calls for real-world photography.

Reference script: `CLAUDE_PLUGIN_ROOT/scripts/fetch-images.js`

#### How to Use fetch-images.js

```bash
node CLAUDE_PLUGIN_ROOT/scripts/fetch-images.js \
  --query "modern conference room city skyline" \
  --orientation landscape \
  --color blue \
  --count 5 \
  --output ./images/slide-3/
```

Parameters:

| Flag | Values | Notes |
|---|---|---|
| `--query` | String | Keyword query from art direction brief |
| `--orientation` | `landscape`, `portrait`, `squarish` | Use `landscape` for 16:9 slides |
| `--color` | `black_and_white`, `black`, `white`, `yellow`, `orange`, `red`, `purple`, `magenta`, `green`, `teal`, `blue` | Match theme palette where possible |
| `--count` | 1–10 | Request multiple options, pick best |
| `--output` | Directory path | Where to save downloaded images |

#### Image Selection Criteria

From the returned candidates, prefer images that:

1. Have a clear focal area that does not conflict with text placement zones
2. Match the theme's color temperature (warm themes → warm-toned images, dark themes → high-contrast or dark-background images)
3. Are at least 1920px wide for full-bleed use, 960px wide for panel use
4. Have no embedded text, watermarks, or logos
5. Have an appropriate emotional tone for the slide's content

#### Attribution

Unsplash images require attribution in free-tier usage. Append photographer credit to the slide's `speaker_notes` field and include a hidden attribution `<span>` in the slide HTML:

```html
<span class="photo-credit" aria-hidden="true">
  Photo by <a href="https://unsplash.com/@username">Photographer Name</a> on Unsplash
</span>
```

### Mode 3: AI Image-Generation Prompts

Use this mode when:
- No suitable Unsplash result exists
- The image requires a specific illustration style, abstract graphic, or conceptual visualization
- The brief calls for branded or custom imagery

Generate a prompt optimized for diffusion models (Stable Diffusion, DALL-E, Midjourney):

#### Prompt Structure

```
[Style descriptor], [subject description], [environment/setting],
[lighting description], [color palette], [composition],
[quality modifiers]
```

Example:

```
Cinematic photography, empty futuristic boardroom with floor-to-ceiling windows
overlooking a nighttime cityscape, dramatic blue and purple ambient lighting,
cool steel and glass tones, wide angle lens, rule of thirds composition,
ultra high resolution, sharp focus, no people, no text
```

#### Negative Prompt (for models that support it)

```
text, watermark, logo, people, faces, clutter, low quality, blurry,
cartoon, illustration (if photo style required), oversaturated
```

#### Output

Return the prompt string and specify which generation service to use:
- `dalle3` for DALL-E 3 via OpenAI API
- `stable-diffusion` for local/API SD inference
- `midjourney` for Midjourney (manual step, provide prompt only)

## Image Guidelines for Presentations

### Composition Rules

- **Full-bleed background slides**: subject must not occupy the center — leave a clear zone for text overlay. Brief should specify "text overlay [left/right/top/bottom] [percentage]% of frame."
- **Right/left panel images**: portrait or near-square orientation preferred; subject centered vertically.
- **Inline images**: square or landscape; clean background; subject clearly isolated.

### Technical Requirements

| Usage | Minimum resolution | Aspect ratio |
|---|---|---|
| Full bleed background | 1920 × 1080px | 16:9 |
| Half-panel | 960 × 1080px | ~1:2 |
| Inline square | 600 × 600px | 1:1 |
| Inline landscape | 800 × 450px | 16:9 |

### Style Consistency

All images in a single presentation should share a consistent visual language. Establish the style in the first art direction brief and carry it through:

- Same photographic style (lifestyle, architectural, abstract, etc.)
- Consistent color temperature (warm or cool)
- Similar level of human presence (none, silhouettes, portraits, etc.)
- Consistent contrast level

## Output Format

For each image slot, return:

```json
{
  "slot_id": "img_0",
  "slide_index": 3,
  "mode_used": "unsplash | ai_prompt | brief_only",
  "src": "https://images.unsplash.com/... or base64 or null",
  "alt": "Full description for accessibility",
  "attribution": "Photo by Name on Unsplash or null",
  "prompt_used": "Generation prompt or search query used",
  "resolution": "1920x1080",
  "position_hint": "full_bleed | right_panel | inline"
}
```

Pass all resolved image objects to the `design-slide` skill for injection into the relevant HTML fragments.
