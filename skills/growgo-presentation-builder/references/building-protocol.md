# Building Protocol (Growgo variant)

Same assembly approach as the parent skill. Growgo-specific additions below.

## Assembly order

1. Read `templates/base.html`. Growgo-branded skeleton.
2. For each section in your outline, read `templates/section-<type>.html`.
3. Merge into one HTML file:
   - All `<style>` blocks deduplicated and merged
   - All `<script>` blocks merged
   - Each section's HTML appended into `<main id="deck">`
4. Inject brand assets (logos) inline as SVG (base64 not needed - they are small SVG files).
5. Verify the language flag and generate copy in PL or EN consistently.
6. Apply ekspercka tone rules to every word.
7. Write the file.

## Slug rules

- kebab-case
- max 60 chars
- strip stop words PL: *jak, to, jest, na, w, dla* - EN: *the, a, how, to*
- transliterate Polish chars: `ł→l, ą→a, ę→e, ó→o, ś→s, ć→c, ń→n, ź→z, ż→z`
- example: `growgo-warsztat-ai-marketing.html`

## CSS variable bootstrap

Set Growgo variables at the top of the merged `<style>`. See `references/design-system.md` for the full block.

The Growgo palette is **not adjustable**. Do not override `--gg-yellow`, `--gg-dark`, `--gg-bg-light`, or `--gg-font`.

## Font loading

Always:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
```

Fallback chain in CSS: `'Roboto', 'Calibri', 'Arial', sans-serif`.

## Logo embedding

Inline the SVG directly in the HTML. Do not base64-encode (the SVG source is already small and tree-readable).

Example for hook section:

```html
<div class="brand-mark">
  <svg width="130" height="40" viewBox="0 0 130 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- full SVG path data from assets/logos/Growgo_LOGO_V3.svg -->
  </svg>
</div>
```

For CTA section: use the white variant (`Growgo_LOGO_V3_white.svg`).

Aspect ratio: always 3.25:1. Never set both width and height independently - compute one from the other.

## Yellow highlight implementation

```html
<h1>Sprawdź jak <span class="hl">AI</span> zmienia marketing</h1>
```

```css
.hl {
  background: var(--gg-yellow);
  color: var(--gg-dark);
  padding: 0.05em 0.25em;
  border-radius: 2px;
  display: inline-block;
  line-height: 1.05;
}
```

Place on hook headline always. Optionally on 1-2 other section titles. Wrap 1-2 words only - never longer.

## Scroll-snap mechanics

Same as parent skill. `scroll-snap-type: y mandatory`, each section `min-height: 100dvh`.

## Section reveal animation

Same as parent. IntersectionObserver + `.in-view` class. Honor `prefers-reduced-motion`.

## Navigation

Same as parent. Right-edge dot-rail (one dot per section). Hidden on mobile (< 768px).

**Dot styling for Growgo**:
- Default: `#888888` muted
- Active: `#FEBF2D` yellow + scale 1.6

## Mobile

- Sections work at 375px wide
- Two-column layouts collapse to single column under 768px
- Display font sizes scale via `clamp()`
- Logo stays top-left at all sizes

## File size budget

Same as parent: < 200 KB. Roboto loads from Google Fonts so it doesn't count against the budget. Embedded SVGs are small. No raster images embedded by default.

## What to NOT do

Same as parent, plus:
- Do not introduce a second font (Roboto only)
- Do not use Anthropic's frontend-design "aesthetic direction" prompt - this skill is locked to Growgo
- Do not put the logo at the bottom of a section (top-left always)
- Do not write copy in mixed language
- Do not use emoji ever
- Do not center any headline (left-align only)
- Do not use Polish phrases like "Rekomendujemy" or English "We recommend"
