# Building Protocol

Step-by-step assembly of the single HTML file.

## Assembly order

1. Read `templates/base.html`. This is your skeleton.
2. For each section in your outline, read the matching `templates/section-<type>.html`.
3. Merge:
   - Concatenate all section HTML into the `<main id="deck">` element in base.
   - Merge all per-section `<style>` blocks into the single `<style>` in `<head>`. Deduplicate `:root` variables and shared utility classes.
   - Merge any per-section `<script>` blocks into the single `<script>` at the bottom.
4. Set CSS custom properties at the top of `<style>` based on your chosen aesthetic direction.
5. Write the final file to `./presentations/<slug>.html`.

## Slug rules

- kebab-case
- derived from the source: YT transcript title, PDF filename, Notion page title
- max 60 chars
- strip stop words (*"the"*, *"a"*, *"how to"*)
- example: `pro-presentations-cowork.html`

## CSS variable bootstrap

At the top of the merged `<style>`, set the aesthetic in CSS variables:

```css
:root {
  /* set by chosen aesthetic */
  --bg: #f4f0e8;
  --fg: #0a0a0a;
  --accent: #c44116;
  --muted: #8c8678;
  --font-display: 'Fraunces', serif;
  --font-body: 'Inter Tight', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* shared spacing scale */
  --space-1: 0.5rem;
  --space-2: 1rem;
  --space-3: 1.5rem;
  --space-4: 2rem;
  --space-6: 4rem;
  --space-8: 8rem;
}
```

Every section partial references these variables. Brand overrides only need to change `--bg`, `--fg`, `--accent`.

## Brand overlay (when user supplied assets)

If a brand layer is being applied:
1. Find the logo file(s) in the user's `assets/` or `logos/` folder.
2. Sample dominant + secondary colors from the logo (ask the user if you cannot determine).
3. Override `--bg`, `--fg`, `--accent` accordingly.
4. Embed small SVG logos as base64 in `background-image` or inline `<svg>`. Reference larger raster files via relative path `./assets/<filename>`.
5. Add a small brand mark on the hook section and the cta section (top-left or bottom-right).

## Font loading

Use Google Fonts `<link>` in `<head>` for any font that has free hosting. For paid foundry fonts (PP Editorial New, Söhne, Saol Display), substitute the closest free alternative and leave a comment noting the substitution.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,700&family=Inter+Tight:wght@400;500;700&display=swap" rel="stylesheet">
```

## Scroll-snap mechanics

The base template sets:
```css
html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }
body { overflow-y: scroll; }
section.snap { scroll-snap-align: start; scroll-snap-stop: always; min-height: 100dvh; }
```

Each section must use `class="snap"` and `min-height: 100dvh` (with `100vh` fallback). Do not set fixed `height` - some sections need to grow on narrow viewports.

## Section reveal animation

Reusable, in the single `<script>`:

```js
const io = new IntersectionObserver(
  entries => entries.forEach(e => e.isIntersecting && e.target.classList.add('in-view')),
  { threshold: 0.25 }
);
document.querySelectorAll('section.snap').forEach(s => io.observe(s));
```

Each section's CSS uses `.snap:not(.in-view) > *` to hide children until the section reveals, then transitions in.

## Navigation

Add a fixed dot-rail on the right edge (`position: fixed; right: 1.5rem; top: 50%`). One dot per section. Active dot enlarges. Clicking jumps to section.

This goes in base.html. Skip on narrow screens (`@media (max-width: 768px) { .nav-rail { display: none; } }`).

## Mobile

- All sections must work at 375px wide.
- Two-column section layouts (`before-after`, `comparison`) collapse to single column under 768px.
- Display font sizes scale via `clamp()` - never fixed px.
- Test in DevTools mobile mode before handing back.

## File size budget

- Target < 200 KB total for the .html file.
- If embedding logos pushes over 200 KB, reference them via relative path instead of base64.
- No inline images > 50 KB base64-encoded.

## What to NOT do

- Do not load any JS framework (React, Vue, Alpine). Vanilla only.
- Do not load Tailwind via CDN - write your own CSS.
- Do not embed Google Analytics or any tracking.
- Do not use `<iframe>` for videos in v1 - link out instead.
- Do not write more than 600 lines of CSS - if you hit that, you are overdoing it.
