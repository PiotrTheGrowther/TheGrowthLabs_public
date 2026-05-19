# Font Pairings

Curated pairings by aesthetic direction. All are Google Fonts (free, hosted, instant access).
**Forbidden everywhere**: plain *Inter*, *Roboto*, *Arial*, *system-ui*, *Times New Roman*, *Helvetica*.

## editorial

Pick ONE pairing per deck:

| Display | Body | Mono | Google Fonts URL |
|---|---|---|---|
| Fraunces | Inter Tight | JetBrains Mono | `family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,700&family=Inter+Tight:wght@400;500;700&family=JetBrains+Mono:wght@400;500` |
| Instrument Serif | Inter Tight | JetBrains Mono | `family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400;500;700&family=JetBrains+Mono:wght@400;500` |
| Newsreader | Geist | JetBrains Mono | `family=Newsreader:opsz,wght@6..72,300;6..72,500;6..72,700&family=Geist:wght@400;500;700&family=JetBrains+Mono:wght@400;500` |

## brutalist

| Display | Body | Mono | Google Fonts URL |
|---|---|---|---|
| Space Grotesk | JetBrains Mono | JetBrains Mono | `family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500;700` |
| Archivo | IBM Plex Mono | IBM Plex Mono | `family=Archivo:wdth,wght@62..125,400;62..125,500;62..125,800&family=IBM+Plex+Mono:wght@400;500;700` |

## retro-futuristic

| Display | Body | Mono | Google Fonts URL |
|---|---|---|---|
| VT323 | Space Mono | Space Mono | `family=VT323&family=Space+Mono:wght@400;700` |
| Major Mono Display | Geist Mono | Geist Mono | `family=Major+Mono+Display&family=Geist+Mono:wght@400;500` |

## luxury

| Display | Body | Mono | Google Fonts URL |
|---|---|---|---|
| Cormorant Garamond | Inter Tight | JetBrains Mono | `family=Cormorant+Garamond:wght@300;500;700&family=Inter+Tight:wght@300;400&family=JetBrains+Mono:wght@400` |
| Italiana | Inter Tight | JetBrains Mono | `family=Italiana&family=Inter+Tight:wght@300;400&family=JetBrains+Mono:wght@400` |

## industrial

| Display | Body | Mono | Google Fonts URL |
|---|---|---|---|
| Archivo | Archivo | IBM Plex Mono | `family=Archivo:wdth,wght@62..125,400;62..125,500;62..125,700;62..125,900&family=IBM+Plex+Mono:wght@400;500` |
| Suisse Int'l (sub: Geist) | Geist | JetBrains Mono | `family=Geist:wght@400;500;700&family=JetBrains+Mono:wght@400;500` |

## Loading template

In `<head>`, always:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{family_query}&display=swap" rel="stylesheet">
```

In CSS, declare with full fallback chain:

```css
:root {
  --font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
  --font-body: 'Inter Tight', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, 'Cascadia Code', monospace;
}
```

Note: the fallback chain may include forbidden families (`Times New Roman`) - this is OK as a LAST-RESORT fallback only. They must never appear as the primary family.

## Substitutions for paid foundry fonts

If you want a foundry font but it is not free:

| Foundry font | Closest free sub |
|---|---|
| Söhne | Geist |
| PP Editorial New | Fraunces or Instrument Serif |
| PP Neue Machina | Space Grotesk |
| Saol Display | Cormorant Garamond |
| Neue Haas Grotesk | Geist or Archivo |
| Suisse Int'l | Geist |
| Suisse Int'l Mono | Geist Mono or JetBrains Mono |

Leave an HTML comment near the font load tag noting the substitution, so a future edit can swap to the licensed font.
