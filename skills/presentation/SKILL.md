---
name: Sexy Presentation
description: Create magazine-quality presentations with 200+ templates, parallel subagents, and interactive playground. Use this skill when the user wants to create, redesign, or export a presentation.
version: 0.1.0
---

# Sexy Presentation Skill

## When to Activate

Activate this skill whenever the user mentions any of the following keywords or intents:
- slides, slide deck, slide show
- presentation, present
- pitch, pitch deck
- keynote, PowerPoint, PPTX
- deck (in a presentation context)
- "make me a presentation", "create a deck", "build slides", "redesign my slides"
- export to PDF/PPTX/Figma from an existing presentation

## Full Workflow

### Step 1: Analyze Input

Delegate to the `analyze-input` skill to parse whatever the user has provided:
- An uploaded PPTX or PDF file
- A markdown outline
- A natural language description
- A URL to a doc or existing presentation

Output: **Slide Data JSON** — a structured representation of all slide content.

Reference: `CLAUDE_PLUGIN_ROOT/skills/analyze-input/SKILL.md`

### Step 2: Select Theme

Delegate to the `select-theme` skill to choose or confirm a visual theme.

- Present available themes from `CLAUDE_PLUGIN_ROOT/themes/`
- If the user has brand guidelines, run `brand-profile` skill first
- Output: a resolved CSS variable block ready for injection

Reference: `CLAUDE_PLUGIN_ROOT/skills/select-theme/SKILL.md`

### Step 3: Check Brand (Optional)

If the user provides a brand PDF, URL, or description, delegate to the `brand-profile` skill before finalizing the theme.

- Output: `brand-profile.json` that overrides theme defaults
- Brand profile is passed into `design-slide` and `select-theme`

Reference: `CLAUDE_PLUGIN_ROOT/skills/brand-profile/SKILL.md`

### Step 4: Plan Slides

Delegate to the `plan-slides` skill to determine the presentation structure.

- Slide count and order
- Template category assignment per slide
- Identification of specialized content (charts, timelines, tables, maps)

Output: **Slide Plan array** with each entry containing slide index, content block, and assigned template.

Reference: `CLAUDE_PLUGIN_ROOT/skills/plan-slides/SKILL.md`

### Step 5: Dispatch Orchestrator (Parallel Subagents)

Spawn parallel subagents — one per slide — each running the `design-slide` skill.

Each subagent receives:
- The slide's content block from the Slide Plan
- The resolved theme CSS variables
- The assigned template path from `CLAUDE_PLUGIN_ROOT/templates/`

Collect all returned HTML fragments and assemble into a full presentation document.

Reference: `CLAUDE_PLUGIN_ROOT/skills/design-slide/SKILL.md`
Reference: `CLAUDE_PLUGIN_ROOT/agents/`
Reference: `CLAUDE_PLUGIN_ROOT/templates/`

### Step 6: Source Imagery (If Needed)

If any slides require images, delegate to the `source-imagery` skill.

- Art direction briefs for each image slot
- Unsplash queries or AI generation prompts
- Images are injected into the relevant HTML fragments

Reference: `CLAUDE_PLUGIN_ROOT/skills/source-imagery/SKILL.md`

### Step 7: QA — Art Director Pass

Delegate to the `qa-art-director` skill to review the assembled presentation.

- Run checklist against each slide
- Categorize issues by severity
- Return a structured feedback report

Reference: `CLAUDE_PLUGIN_ROOT/skills/qa-art-director/SKILL.md`

### Step 8: Polish Graphics

Delegate to the `polish-graphics` skill, passing the Art Director feedback.

- Apply all required fixes
- Run a final consistency verification pass

Reference: `CLAUDE_PLUGIN_ROOT/skills/polish-graphics/SKILL.md`

### Step 9: Interactive Playground

Delegate to the `playground` skill to open an interactive editor.

- Inject slides, theme, and template gallery into the playground
- Allow the user to iterate via chat commands
- Re-run design/polish sub-steps as needed on changed slides

Reference: `CLAUDE_PLUGIN_ROOT/skills/playground/SKILL.md`
Reference: `CLAUDE_PLUGIN_ROOT/playground/playground-template.html`

### Step 10: Export

When the user is satisfied, delegate to the `export` skill.

- Supported formats: PDF, PPTX, Figma, HTML
- Each format has its own script or integration

Reference: `CLAUDE_PLUGIN_ROOT/skills/export/SKILL.md`
Reference: `CLAUDE_PLUGIN_ROOT/scripts/`

## Key References

| Resource | Path |
|---|---|
| Agents | `CLAUDE_PLUGIN_ROOT/agents/` |
| Templates | `CLAUDE_PLUGIN_ROOT/templates/` |
| Themes | `CLAUDE_PLUGIN_ROOT/themes/` |
| Playground template | `CLAUDE_PLUGIN_ROOT/playground/playground-template.html` |
| Export scripts | `CLAUDE_PLUGIN_ROOT/scripts/` |
| Sub-skills | `CLAUDE_PLUGIN_ROOT/skills/` |

## Notes

- Always confirm the desired output format before starting (PDF, PPTX, Figma, or HTML).
- If the user provides partial input (e.g., only a topic), ask clarifying questions: audience, tone, slide count preference, and any existing brand assets.
- Parallel subagent dispatch (Step 5) is the primary performance lever — do not serialize slide generation unless a dependency exists between slides.
- The playground step is optional but strongly recommended for presentations with more than 5 slides, to allow user review before final export.
