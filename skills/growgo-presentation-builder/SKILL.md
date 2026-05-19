---
name: growgo-presentation-builder
version: 0.1.0
description: |
  Growgo-branded variant of presentation-builder. Turns written content
  (YouTube transcripts, PDFs, markdown/docx/txt docs, Notion pages) into a
  single self-contained vertical scroll-snap HTML presentation site,
  styled with the official Growgo brand system (Roboto, #FEBF2D yellow
  accent, #EFEFEF light grey background, #1E1E1E dark, yellow-highlight
  signature on key phrases, 6-dot motif). Use when the user asks for a
  Growgo presentation, growgo deck, growgo prezentacja, growgo HTML,
  growgo scroll-site, or any deck "in Growgo brand / w stylu Growgo".
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Growgo Presentation Builder

A branded variant of `presentation-builder`. Same output format (single self-contained vertical scroll-snap HTML file), but the aesthetic is locked to the official Growgo brand system. No aesthetic picking, no font choice - just a clean, on-brand deck every time.

## When to invoke

User asks for any of: *growgo presentation · growgo deck · prezentacja growgo · growgo HTML · growgo scroll-site · deck "in Growgo brand"*. Also when the user has explicitly said the deliverable is for Growgo.

For brand-agnostic decks, use the parent `presentation-builder` skill instead.

## What's locked (vs the parent skill)

| Parent skill | This variant |
|---|---|
| 5 aesthetic directions to pick from | **One locked direction**: Growgo brand |
| Bans Roboto | **Roboto required** (Growgo's only font) |
| Generic palette per content tone | **Locked palette**: `#FEBF2D` / `#1E1E1E` / `#EFEFEF` / `#383838` / `#888888` |
| White or any bg allowed | **`#EFEFEF` light grey only** - never pure white |
| Headlines may be centered | **Always left-aligned** - never centered |
| No signature element | **Yellow highlight `#FEBF2D` on 1-2 key words per hook headline** |
| No brand mark | **6-dot motif + logo** embedded in hook + cta |
| English-first | **Auto-detect from source** - PL or EN |
| Free tone | **Locked to "ekspercka" tone** (per Growgo brand) |

## Hard rules (non-negotiable)

1. **Font is Roboto.** Loaded from Google Fonts. Fallback chain: `'Roboto', 'Calibri', 'Arial', sans-serif`. No other fonts anywhere.
2. **Background is `#EFEFEF`.** Never `#FFFFFF`. Dark sections use `#1E1E1E`.
3. **Yellow `#FEBF2D` is the only accent.** Never as text color on light bg - only as highlight bg under dark text, or CTA button bg.
4. **Yellow highlight on the hook.** Hook headline must wrap 1-2 key words in `<span class="hl">...</span>` (yellow bg, dark text). This is the Growgo signature.
5. **Logo embedded.** Dark logo SVG inlined as base64 in hook section (top-left). White logo SVG in CTA section (top-left, since CTA is dark bg). Aspect ratio locked at 3.25:1.
6. **6-dot motif as decoration.** Use `GrowGo-Logo-Icon-Yellow.svg` (yellow) or `ICON-grey.svg` (subtle watermark) on quote/metric sections.
7. **All headlines left-aligned.** No exception except timeline date column.
8. **Icons only `#1E1E1E` / `#FFFFFF` / `#FEBF2D`.** No green/blue/purple/red icons.
9. **No em-dashes.** `—` becomes `-`. Strict.
10. **No emoji.** Anywhere. Growgo brand bans them in all communication.
11. **Tone: "ekspercka".** Bezosobowa narracja, bullet points, "proponujemy" not "rekomendujemy". See `references/tone-ekspercka.md`.
12. **Language: auto-detect.** Read the source content - if PL, generate PL output (use Polish quote marks „..."). If EN, generate EN. Never mix.

## Workflow (same 8 steps as parent, with growgo-specific overrides)

### 1. Discover input
Same as parent: locate file, fall back to Glob + AskUserQuestion.

### 2. Ingest and chunk
Same as parent. See `references/ingestion-patterns.md`. **Detect language** during this step (Polish word frequency vs English).

### 3. Outline the deck
Same as parent: 8-14 sections, must include 1 hook + 1 cta + ≥1 quote + ≥1 metric + ≥1 steps + ≥1 before-after.

**Growgo-specific:** for non-tech audiences (workshop participants, marketers), de-prioritize `terminal` and `workspace` section types unless source content explicitly contains code or file structures.

### 4. Aesthetic direction
**Skip this step.** Growgo aesthetic is locked. Move straight to generation.

### 5. Brand layer
**Always on for this skill.** Brand assets (logos, favicon, 6-dot SVG) are bundled in `assets/logos/`. The skill embeds them automatically.

### 6. Generate the HTML
- Start from `templates/base.html` (this variant's growgo-specific base).
- For each section, use the matching `templates/section-<type>.html` partial.
- All CSS uses Growgo CSS variables (see `references/design-system.md` section 8).
- Hook section: wrap 1-2 key words in `<span class="hl">...</span>` (yellow highlight).
- Apply ekspercka tone rules to all copy. See `references/tone-ekspercka.md`.
- **Polish source = Polish output.** Use Polish typographic conventions: „cudzysłowy", spacja przed jednostkami, separator tysięcy jako spacja.
- Write to `./presentations/<slug>.html`.

### 7. Verify
Same checks as parent, **except**:
- Roboto is REQUIRED (not banned)
- The forbidden font check is: `Inter|Arial|Helvetica|Times New Roman|system-ui` (Roboto is whitelisted)
- Additional check: yellow highlight present on hook headline (`grep -c 'class="hl"'` must be ≥1)
- Additional check: NO emoji (`grep -P '[\x{1F300}-\x{1FAFF}]'` must return empty)
- Additional check: ekspercka tone - no `Rekomendujemy|Zalecamy|Musicie|Trzeba|Myślę że|Widzę że`
- Additional check: no banned universal Growgo phrases - `Mieliśmy ogromną przyjemność|Z przyjemnością podzielimy|Pragniemy zaprezentować|Mechanizm funkcjonowania polega na|niezwykle ważny`
- Additional check: spelling "Growgo" - never "GrowGo", "GROWGO", "growgo" (except in URLs/handles)

### 8. Hand back
Same as parent. Note in the handback: *"Growgo brand applied: Roboto, #FEBF2D yellow accent, yellow-highlight signature on hook, dark logo embedded."*

## Reference files

| File | Purpose |
|---|---|
| `references/ingestion-patterns.md` | Same as parent - per-format parsing |
| `references/slide-types.md` | Same 11 section types as parent |
| `references/design-system.md` | **Growgo-specific** - locked palette, Roboto, signature element, logo rules |
| `references/tone-ekspercka.md` | **Growgo-specific** - expert tone rules (PL + EN) |
| `references/building-protocol.md` | Same as parent - HTML assembly |
| `references/verification-rules.md` | Parent rules + Growgo-specific checks |
| `templates/base.html` | **Growgo-branded** scaffold (Roboto, EFEFEF bg, CSS variables) |
| `templates/section-*.html` | **Growgo-branded** partials (yellow highlight, 6-dot motif, dark cards) |
| `assets/logos/` | Brand SVGs - logo dark, logo white, 6-dot yellow, 6-dot grey, favicon |
| `examples/from-yt-transcript.html` | Reference output |

## Composability with growgo-brand skill

This skill is **self-contained** - it does not require the `growgo-brand` skill to be loaded. The visual and tone rules are copied here for offline / Cowork use.

If both skills are present, this one takes precedence for presentation output. The `growgo-brand` skill remains the source of truth for docx/pptx/xlsx where it composes with anthropic-skills:docx, anthropic-skills:pptx, etc.

## Common mistakes (avoid)

- Using pure `#FFFFFF` background instead of `#EFEFEF` (this is the #1 brand violation)
- Centering headlines (left-align only)
- Skipping the yellow highlight on the hook (it's the signature)
- Yellow text on light bg (forbidden - low contrast)
- Using green/blue/purple as icon colors (they're only for step numbers and accent stripes)
- Mixing PL and EN copy in the same deck
- Centered logo (always top-left, with clear space)
- Cropping the logo to fit a tight container (scale down instead - aspect ratio is locked at 3.25:1)
- Using emoji (banned everywhere in Growgo)
- "Rekomendujemy" / "Zalecamy" / "Musicie" (use "Proponujemy" / "Warto" / "Najskuteczniejszym podejściem jest")
