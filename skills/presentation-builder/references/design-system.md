# Design System

Extends `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design/skills/frontend-design/SKILL.md`. Read that file too if you have not already.

## The five aesthetic directions

Pick ONE per deck. Do not mix. State your pick before generating.

### editorial
- **Use for**: founder essays, long-form thinking, opinion pieces, manifestos.
- **Typography**: display = *Fraunces* or *PP Editorial New*. Body = *Inter Tight* (heavier than 400) or *Söhne*. NEVER plain *Inter*.
- **Color**: cream/off-white background (`#f4f0e8`), deep ink text (`#0a0a0a`), one accent (deep teal `#0e4d4a`, oxblood `#7d1a1a`, or burnt orange `#c44116`).
- **Layout**: 12-col grid, generous margins, large body line-height (1.5-1.7). Drop caps welcome.
- **Motion**: very subtle. Fade-in on scroll, no horizontal motion.

### brutalist
- **Use for**: technical demos, raw documentation, contrarian pieces.
- **Typography**: display = *Space Grotesk* or *Neue Haas Grotesk*. Body = *JetBrains Mono* (yes, mono in body). 
- **Color**: pure white (`#ffffff`) or pure black (`#000000`). One screaming accent (`#ff3300`, `#00ff66`, electric yellow `#fff200`). No grays.
- **Layout**: 1-2 px solid borders everywhere. Asymmetric. Numbered labels in margins (`§ 04`, `[03/12]`).
- **Motion**: hard cuts, no easing. `step-end` timing. Glitch effects on hover.

### retro-futuristic
- **Use for**: product launches, sci-fi adjacent, AI/agent topics with playful angle.
- **Typography**: display = *VT323*, *Space Mono*, or *PP Neue Machina*. Body = *Söhne* or *Inter Tight*.
- **Color**: deep purple/black background (`#0a0521`), neon accents (cyan `#00f0ff`, magenta `#ff00aa`, lime `#aaff00`). Gradient meshes OK. **Forbidden**: purple-to-pink linear gradients on white.
- **Layout**: grid floor in perspective, sun-disc backgrounds, scan-line overlays.
- **Motion**: glow pulses, gradient shifts, terminal cursor blinks.

### luxury
- **Use for**: premium services, high-end positioning, agencies, real estate, hospitality.
- **Typography**: display = *Cormorant Garamond* or *Saol Display*. Body = *Söhne Light* or *Inter Tight Light*.
- **Color**: rich black (`#0c0c0c`), bone white (`#f7f4ec`), one metallic accent (gold `#c5a572`, copper `#b87333`).
- **Layout**: vast whitespace, thin hairline rules, tight typographic hierarchy. Centered preferred.
- **Motion**: slow fades, gentle parallax, never bouncy.

### industrial
- **Use for**: infrastructure, ops, internal tooling, B2B SaaS.
- **Typography**: display = *Söhne Breit* or *Suisse Int'l Mono*. Body = *Söhne* or *Suisse Int'l*.
- **Color**: cool grey background (`#e8e8e6`), high-contrast text (`#0a0a0a`), safety-orange accent (`#ff5a1f`).
- **Layout**: utility labels, ALL-CAPS section names, gridlines visible, technical drawings vibe.
- **Motion**: machined - tick, snap, slide. Never bouncy.

## Typography rules (universal)

- Display font size: clamp(3rem, 8vw, 7rem) for hooks, clamp(2rem, 5vw, 4rem) for headers.
- Body line-length: 50-72 characters max.
- Letter-spacing: tighten display (-0.02em to -0.04em), open small caps (+0.08em).
- **NEVER** use: *Inter (plain)*, *Roboto*, *Arial*, *system-ui*, *Helvetica (system default)*, *Times New Roman*.
- Pair: one distinctive display + one refined body. Never three font families.

## Color rules

- One dominant color (60% of pixels), one secondary (30%), one accent (10%).
- Use CSS custom properties:
  ```css
  :root {
    --bg: #f4f0e8;
    --fg: #0a0a0a;
    --accent: #c44116;
    --muted: #8c8678;
  }
  ```
- Contrast: text on background must be ≥ 4.5:1.
- **Forbidden**: purple-to-pink gradients on white, "fintech" gradients (cyan-to-magenta on dark blue), beige-and-mint pastel combos.

## Motion rules

- CSS-only. No JS animation libs.
- One signature page-load animation. Stagger child reveals with `animation-delay: calc(var(--i) * 80ms)`.
- Scroll-triggered reveals via `IntersectionObserver` + adding a `.in-view` class. Keep the JS under 20 lines.
- Respect `prefers-reduced-motion: reduce` - disable all non-essential motion.

## Spatial composition

- Asymmetry beats centered alignment 80% of the time. The 20%: luxury aesthetic.
- Overlap text and shapes intentionally. Grid-breaking elements (a quote that bleeds off the left edge).
- Generous whitespace OR controlled density - never lukewarm middle.

## Background details

Avoid flat backgrounds on hero sections. Add ONE of:
- Subtle noise/grain (SVG filter `<filter><feTurbulence/></filter>`, opacity 0.04)
- Gradient mesh (radial gradient with 3 stops)
- Geometric pattern (CSS `background-image: radial-gradient(...)` dotted)
- Single decorative element (a large numeral, an SVG diagram)

## Copy rules

These apply to every word generated for the deck:

1. **No em-dashes.** Replace `—` with `-`. Strict.
2. **Plain language.** Short, direct sentences. Cut adjectives.
3. **Banned AI tells**: *delve*, *landscape*, *leverage*, *unlock*, *navigate the complexities*, *stands as a testament*, *evolving*, *vibrant*, *seamless*, *journey* (when figurative), *robust*.
4. **Active voice** unless passive is genuinely better.
5. **No "rule of three"** in every sentence. Mix rhythms.
6. **Headlines**: claim a thing, do not describe a thing. *"Drop the zip. It works."* beats *"How to upload the skill file."*
7. **CTA copy**: imperative + outcome. *"Get the skill"* + *"3-minute setup"*. Not *"Click here to learn more about our solution"*.

## Forbidden visual patterns

- Generic SaaS hero with centered headline + two buttons + abstract gradient blob
- Three-card pricing layout
- Floating screenshot on a tilted angle behind a CTA
- Stock-photo-style illustrations of business people
- Emoji as section icons (only when explicitly requested for tone)
- Multi-step progress bars on non-form content
