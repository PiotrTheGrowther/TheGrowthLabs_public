# Growgo Design System

Source of truth for visual rules in this skill. Mirrors `growgo-brand` reference but scoped to HTML scroll-site output.

## Palette (CSS variables)

```css
:root {
  /* Brand core */
  --gg-yellow: #FEBF2D;
  --gg-dark: #1E1E1E;
  --gg-text: #383838;
  --gg-text-secondary: #888888;
  --gg-white: #FFFFFF;

  /* Backgrounds - NEVER pure white */
  --gg-bg-light: #EFEFEF;
  --gg-bg-dark: #1E1E1E;
  --gg-card-light: #D5D5D5;
  --gg-card-dark: #2A2A2A;
  --gg-card-dark-alt: #3A3A3A;

  /* Section accents - stripes/step numbers ONLY, never icons */
  --gg-green: #259A53;
  --gg-blue: #52679C;
  --gg-purple: #9868A9;

  /* Semantic */
  --gg-success: #259A53;
  --gg-warning: #E8A317;   /* not #FEBF2D - reserved for brand accent */
  --gg-error: #D94F30;
  --gg-neutral: #888888;

  /* Typography */
  --gg-font: 'Roboto', 'Calibri', 'Arial', sans-serif;
  --gg-line-height: 1.6;
  --gg-line-height-tight: 1.2;

  /* Spacing scale */
  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-3: 1.5rem;
  --space-4: 2rem;
  --space-6: 4rem;
  --space-8: 8rem;

  --maxw: 1280px;
}
```

## Allowed text+bg pairings (WCAG AA)

| Text | Background | Contrast |
|---|---|---|
| `#1E1E1E` | `#EFEFEF` | ~14:1 OK |
| `#1E1E1E` | `#D5D5D5` | ~10:1 OK |
| `#1E1E1E` | `#FEBF2D` | ~9:1 OK |
| `#383838` | `#EFEFEF` | ~9:1 OK |
| `#FFFFFF` | `#1E1E1E` | ~14:1 OK |
| `#FFFFFF` | `#2A2A2A` | ~11:1 OK |
| `#888888` | `#EFEFEF` | ~3.5:1 OK (≥18pt only) |

**Forbidden**:
- `#FEBF2D` text on `#FFFFFF` or `#EFEFEF` (never enough contrast)
- `#888888` on `#1E1E1E`
- `#D5D5D5` card on `#EFEFEF` bg for text (only for box backgrounds)

## Typography (HTML/Web)

| Role | Size | Weight | Color |
|---|---|---|---|
| H1 (hook headline) | clamp(2.5rem, 7vw, 5rem) | 700 Bold | `var(--gg-dark)` |
| H2 (section title) | clamp(2rem, 5vw, 3.5rem) | 700 Bold | `var(--gg-dark)` |
| H3 (sub-section / card title) | clamp(1.25rem, 2.5vw, 1.75rem) | 500 Medium | `var(--gg-dark)` |
| Body | 1rem | 400 Regular | `var(--gg-text)` |
| Small / caption / kicker | 0.875rem | 400 Regular | `var(--gg-text-secondary)` |
| Large callout number | clamp(6rem, 20vw, 14rem) | 700 Bold | `var(--gg-yellow)` |

**Always left-aligned.** No centered headlines (timeline date column is the only exception). Line-height: 1.6 body, 1.2 tight (display).

**Letter-spacing**: 0 default. -0.02em only on giant callout numbers (60pt+).

## The signature element: yellow highlight

This is the Growgo brand mark in typography. **Required on the hook headline.** Optional on 1-2 other section titles.

```html
<h1>Wdrożenie <span class="hl">AI</span> w marketingu</h1>
```

```css
.hl {
  background: var(--gg-yellow);
  color: var(--gg-dark);
  padding: 0 0.2em;
  border-radius: 2px;
}
```

Rules:
- Wrap 1-2 words only - never an entire phrase
- The word must be the conceptual key of the headline (the "what")
- Light bg sections: yellow `#FEBF2D` under dark `#1E1E1E` text
- Dark bg sections: same yellow bg, same dark text (still readable)
- Never on the entire title - it loses meaning
- Never as an underline or border - only as solid background fill

## 6-dot motif (brand mark)

Available as `assets/logos/GrowGo-Logo-Icon-Yellow.svg` (yellow on transparent) and `assets/logos/ICON-grey.svg` (grey watermark).

Suggested usage:
- Top-right corner of `metric` section, large (300px+, opacity 0.15)
- Decorative element on `quote` section, behind the quote mark
- Subtle watermark on `cta` section (yellow version on dark bg)

Never:
- Cropped or partially visible
- Stretched (it's a square arrangement of 6 circles, aspect ratio 1:0.99)
- Overlapping logo or text

## Logo placement

| Asset | Where | Size |
|---|---|---|
| `Growgo_LOGO_V3.svg` (dark) | Hook section, top-left, in `.brand-mark` | width ~130px (height 40px, aspect 3.25:1 LOCKED) |
| `Growgo_LOGO_V3_white.svg` | CTA section, top-left (dark bg) | Same dimensions |
| `Vectors-Wrapper-5.svg` (9-dot yellow) | Optional: divider sections | Up to 400px |

**Embed as base64 inline SVG** so the file is self-contained:
```html
<div class="brand-mark">
  <svg width="130" height="40" viewBox="0 0 130 40">...</svg>
</div>
```

Aspect ratio rule (CRITICAL): logo aspect is exactly 3.25:1. Always compute: `height = width / 3.25`. Never set both independently.

## Card system

**Light context** (`#EFEFEF` bg):
- Card bg: `#D5D5D5`
- Card text: `#1E1E1E` (titles), `#383838` (body)
- **Shadow REQUIRED**: `box-shadow: 0 2px 6px rgba(0,0,0,0.12);`

**Dark context** (`#1E1E1E` bg):
- Card bg: `#2A2A2A` (or `#3A3A3A` for contact cards)
- Card text: `#FFFFFF` (titles), `#FFFFFF` (body, but reduced opacity for secondary)
- **No shadow** on dark bg

Step number / accent stripe colors (numbered cards only):
- Step 1: `#FEBF2D` (yellow)
- Step 2: `#259A53` (green)
- Step 3: `#52679C` (blue)
- Step 4: `#9868A9` (purple)
- Step 5+: cycle back to yellow

## Section background pattern

For an 11-section deck, rough rhythm:
- Hook: light (`#EFEFEF`)
- Metric: dark (`#1E1E1E`) - white text + huge yellow figure
- Before-after: light
- Steps: light
- Quote: light (with 6-dot motif decoration)
- Workspace/Terminal/Comparison: light (cards) or dark (cards)
- Timeline: light
- CTA: dark (`#1E1E1E`) - reverse of hook

Avoid 3+ consecutive same-bg sections. Alternate creates visual rhythm.

## Motion rules

- CSS-only animations
- Reveal on scroll via IntersectionObserver (same as parent skill)
- `prefers-reduced-motion: reduce` disables all motion
- No flashy effects - Growgo aesthetic is calm-confident, not playful

## Forbidden visual patterns

- Pure white background `#FFFFFF` anywhere as primary bg
- Centered headlines
- Yellow `#FEBF2D` as text color on light bg
- Mixed fonts (Roboto only, no display secondary)
- Italic Roboto for emphasis (use weight 700 or yellow highlight instead)
- Drop shadows on dark bg cards
- 3D effects, gradients on data charts
- Emoji as section icons or decoration
- Cropped or distorted logos
- Section accent colors (green/blue/purple) used as icon colors or backgrounds
