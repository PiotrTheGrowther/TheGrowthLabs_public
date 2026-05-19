# Growgo Presentation Builder

A Growgo-branded variant of [`presentation-builder`](../presentation-builder/). Same output format (single self-contained vertical scroll-snap HTML file), but the aesthetic is **locked to the official Growgo brand system** - no aesthetic picking, no font choice, just on-brand decks every time.

## What's locked vs the parent skill

| Parent skill | This variant |
|---|---|
| 5 aesthetic directions to pick from | One locked direction: Growgo brand |
| Bans Roboto | Roboto required (Growgo's only font) |
| Generic palette per content tone | Locked palette: `#FEBF2D` / `#1E1E1E` / `#EFEFEF` |
| White or any bg | `#EFEFEF` light grey only - never pure white |
| Headlines may be centered | Always left-aligned |
| No signature element | Yellow highlight `#FEBF2D` on 1-2 key words per hook |
| No brand mark | 6-dot motif + logo embedded in hook + cta |
| English-first | Auto-detect from source (PL or EN) |
| Free tone | Locked to "ekspercka" tone (per Growgo brand) |

## See it in action

[`examples/from-yt-transcript.html`](./examples/from-yt-transcript.html) - the same source as the parent skill's example, but rendered with the Growgo brand. Side-by-side comparison shows what the brand layer does.

## Install

### Claude Cowork

1. Download `growgo-presentation-builder.zip` from the parent folder ([direct link](../growgo-presentation-builder.zip))
2. Open Claude Cowork
3. Settings → Capabilities → Skills → Add Skill
4. Drag the zip into the upload area

### Claude Code (CLI)

```bash
cp -r growgo-presentation-builder ~/.claude/skills/
```

## Use it

Same workflow as the parent. Open a folder with source content, then:

> Use the growgo-presentation-builder skill on this transcript.

Claude reads the skill, finds the file, outlines 8-14 sections, generates the HTML with Growgo brand applied (Roboto, yellow highlight, dark logo on hook, white logo on CTA, ekspercka tone), writes to `./presentations/<slug>.html`.

## What's in the box

```
growgo-presentation-builder/
├── SKILL.md                          entry point - 8-step workflow
├── references/
│   ├── ingestion-patterns.md         per-format parsing + language detection
│   ├── slide-types.md                11 section types with growgo styling
│   ├── design-system.md              locked palette, Roboto, signature, logo rules
│   ├── tone-ekspercka.md             expert tone rules (PL + EN)
│   ├── building-protocol.md          HTML assembly
│   └── verification-rules.md         static + dynamic checks
├── templates/
│   └── base.html                     growgo-branded scaffold
├── examples/
│   └── from-yt-transcript.html       reference output (same source as parent)
└── assets/
    └── logos/                        embedded brand SVGs (dark, white, 6-dot, favicon)
```

## Hard rules

- Font: Roboto (loaded from Google Fonts)
- Background: `#EFEFEF` light grey, NEVER pure white
- Accent: `#FEBF2D` yellow (highlight bg + CTA, never as text color on light bg)
- All headlines left-aligned
- Yellow highlight `<span class="hl">` on 1-2 key words in the hook
- Dark logo on hook section, white logo on CTA section
- Aspect ratio 3.25:1 for logo - never deformed
- No em-dashes (`—` → `-`)
- No emoji - anywhere
- "Growgo" spelling only - never "GrowGo" or "GROWGO"
- Ekspercka tone: "Proponujemy" not "Rekomendujemy", "Warto" not "Zalecamy"

## Composability with growgo-brand skill

This skill is **self-contained** - it does not require the `growgo-brand` skill. Visual and tone rules are copied here for offline / Cowork use.

If both skills are present, this one takes precedence for HTML presentation output. The `growgo-brand` skill remains the source of truth for docx/pptx/xlsx where it composes with `anthropic-skills:docx`, `anthropic-skills:pptx`, etc.

## Credits

Built by [TheGrowthLabs](https://github.com/PiotrTheGrowther/TheGrowthLabs_public). Based on the parent `presentation-builder` skill, branded with the official Growgo design system.

## License

MIT
