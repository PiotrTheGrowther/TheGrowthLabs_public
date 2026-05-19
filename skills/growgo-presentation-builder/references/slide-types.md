# Slide Types (Growgo variant)

11 section types - same library as parent. Growgo-specific notes added.

## Type catalog

### 1. `hook` - opening section (always first)
**When**: First section, always.
**Content shape**: Logo top-left + kicker line + oversized headline with **yellow highlight on 1-2 key words**.
**Growgo-specific**:
- Logo (dark variant) embedded as inline SVG, top-left, width 130px
- Headline must have `<span class="hl">...</span>` on key term (signature element)
- Background: `#EFEFEF` light

### 2. `metric` - one striking number
**When**: Any block with a number worth amplifying.
**Content shape**: Giant figure + short label below.
**Growgo-specific**:
- Background: `#1E1E1E` dark (high contrast)
- Figure color: `#FEBF2D` yellow
- 6-dot motif (yellow) decorative in top-right corner (opacity 0.15, large)
- Label text: white

### 3. `before-after` - old way vs. new way
**When**: Comparing two states.
**Content shape**: Two cards, before / after.
**Growgo-specific**:
- Light bg (`#EFEFEF`)
- "Before" card: `#D5D5D5` with shadow
- "After" card: `#FEBF2D` yellow bg, dark text - this is the on-brand highlight
- Arrow between cards: `#1E1E1E`

### 4. `quote` - pull quote
**When**: A landing-sentence isolated.
**Content shape**: Large italic-weight quote + attribution.
**Growgo-specific**:
- Use Polish „..." or English "..." per language
- 6-dot grey motif as background decoration (opacity 0.1)
- Note: Roboto has no italic by design - use weight 300 Light for emphasis instead

### 5. `steps` - numbered process
**When**: 3-7 ordered actions.
**Content shape**: Numbered cards.
**Growgo-specific**:
- Step number colors cycle: yellow `#FEBF2D` → green `#259A53` → blue `#52679C` → purple `#9868A9` → back to yellow
- These are the ONLY places where green/blue/purple are allowed
- Card bg: `#D5D5D5` with shadow on light section

### 6. `timeline` - chronology / roadmap
**When**: Dates, milestones, phases.
**Content shape**: Vertical timeline.
**Growgo-specific**:
- Date column left-aligned in Polish (`19.05.2026`) or English (`2026-05-19`) per language
- Dot markers: `#FEBF2D` yellow
- Connecting line: `#888888` grey

### 7. `logo-grid` - tool / partner / asset showcase
**When**: List of named entities.
**Content shape**: 4-12 logos in a grid.
**Growgo-specific**:
- Card bg: `#D5D5D5` with shadow
- Captions: kicker style (`#888888`, mono-ish, uppercase, letter-spacing 0.08em)
- If user has provided their own logos, use those. Otherwise, ask.

### 8. `comparison` - multi-axis table
**When**: Comparing options across criteria.
**Content shape**: 2-4 column table.
**Growgo-specific**:
- Header row: `#1E1E1E` bg, white text
- Alternating rows: `#FFFFFF` / `#F5F5F5` (still in a light card on `#EFEFEF` section)
- Winner column: text in `#1E1E1E`, bold weight, with yellow highlight on winner label

### 9. `terminal` - code / CLI moment
**When**: Code blocks in source.
**Growgo-specific**: **De-prioritize for Growgo decks.** Growgo audience is non-technical marketers. Only use if source explicitly contains code/CLI content. If used, follow parent styling (dark window with traffic-light dots).

### 10. `workspace` - file tree / folder structure
**When**: Block describes directory layout.
**Growgo-specific**: **De-prioritize for Growgo decks.** Same reasoning - non-tech audience. Only use if source explicitly has file structures.

### 11. `cta` - closing call-to-action (always last)
**When**: Last section, always.
**Content shape**: Headline + 1-2 buttons + footer line.
**Growgo-specific**:
- Background: `#1E1E1E` dark (mirrors a possible dark variant)
- White logo (`Growgo_LOGO_V3_white.svg`) top-left
- Primary CTA button: `#FEBF2D` yellow bg, `#1E1E1E` text
- Secondary CTA button: transparent, white border
- Headline: yellow highlight on key word

## Outline rules

- **Total**: 8-14 sections
- **Required**: exactly 1 `hook`, exactly 1 `cta`, ≥1 `quote`, ≥1 `metric`, ≥1 `steps`, ≥1 `before-after`
- **Variety**: no more than 2 consecutive same-type sections
- **Rhythm**: alternate dense (steps, comparison) with sparse (quote, metric, hook). Wall of dense kills the deck.
- **Background rhythm**: don't put 3+ consecutive light bg sections. Use metric (dark) and CTA (dark) to break up.

## Mapping examples (Growgo context)

| Input block heading | Best section type |
|---|---|
| *"3 minuty od transkryptu do prezentacji"* | `metric` |
| *"Pierwsze 4 kroki uruchomienia"* | `steps` |
| *"Wcześniej / teraz"* / *"Before / After"* | `before-after` |
| *"Główna teza warsztatu"* | `hook` (if first) |
| *"Mapa narzędzi"* / *"Stack"* | `logo-grid` |
| *"Plan 8 tygodni"* | `timeline` |
| *"Co dostaniesz / Co nie dostaniesz"* | `comparison` |
| *"Dlaczego warto teraz"* | `cta` |
