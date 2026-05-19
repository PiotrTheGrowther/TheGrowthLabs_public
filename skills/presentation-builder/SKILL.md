---
name: presentation-builder
version: 0.1.0
description: |
  Turn written content (YouTube transcripts, PDFs, markdown/docx/txt docs,
  Notion pages) into a single self-contained vertical scroll-snap HTML
  presentation site. Use when the user asks for a presentation, slide deck,
  pitch deck, scroll-site, one-pager, HTML deck, or vertical site from a
  source document or transcript.
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

# Presentation Builder

You generate **one self-contained `.html` file** that renders a vertical scroll-snap presentation site from any written input. The file contains inlined CSS and JS, references external assets only via `./assets/` relative paths (or base64-embeds small SVGs), and works when opened directly in Chrome.

## When to invoke

User asks for any of: presentation · slide deck · pitch deck · scroll-site · one-pager · HTML deck · vertical site · "turn this into a presentation".

## Hard rules (non-negotiable)

1. **Single file output.** All CSS in one `<style>` block, all JS in one `<script>` block. No external CSS/JS files.
2. **Vertical scroll-snap.** Sections are full viewport height (`100vh` / `100dvh`), `scroll-snap-type: y mandatory` on the body.
3. **No generic AI aesthetics.** NEVER use Inter, Roboto, Arial, system-ui. NEVER use purple gradients on white. Pick a distinctive font pairing (see `assets/font-pairings.md`) and a bold aesthetic direction.
4. **No em-dashes.** Replace every `—` with `-`. This is a strict project rule.
5. **Brand layer is opt-in.** Only apply a brand when the user (a) provides an `assets/` or `brand/` or `logos/` folder AND (b) explicitly names the brand to use. Otherwise pick the aesthetic from content tone.
6. **Verify before handing back.** After writing the file, open it via headless browser (if available) and screenshot at least the hook and one mid section. If `Claude_in_Chrome` is not available, ask the user to spot-check.
7. **Output location.** Default to `./presentations/<slug>.html` relative to the working folder. Create the folder if it doesn't exist.

## Workflow (8 steps)

When invoked, follow this exact sequence. Do not skip steps.

### 1. Discover the input

- If the user named a file or pasted a path → resolve it directly.
- If the user pasted a Notion URL → use `notion-fetch` if available, otherwise ask them to export the page to markdown first.
- If neither → `Glob` the working folder for `**/*.{md,txt,pdf,docx}` and ask which to use via `AskUserQuestion`.

### 2. Ingest and chunk

Read `references/ingestion-patterns.md` for the per-format procedure. Summary:
- **YouTube transcript** → look for chapter markers (`*0:30 Title*`); fall back to topic-shift segmentation by paragraph clustering.
- **PDF** → use `Read` with the `pages` parameter; reconstruct sections from heading repetition + blank-line patterns.
- **Markdown / docx / txt** → use existing `#`/`##` headings as the skeleton.
- **Notion** → use heading blocks as section breaks.

Produce an internal list of `{heading, body}` blocks.

### 3. Outline the deck

Map blocks to section types from `references/slide-types.md`. The deck MUST include:
- exactly 1 `hook` (first section)
- exactly 1 `cta` (last section)
- at least 1 `quote`
- at least 1 `metric`
- at least 1 `steps`
- at least 1 `before-after`

Total length: **8-14 sections**. Print the outline to chat as a numbered list with section type for each. Do not ask for approval - proceed.

### 4. Commit to ONE aesthetic direction

Read `references/design-system.md`. Pick ONE direction based on content tone:
- **editorial** - long-form essay, founder writing, thoughtful → serif display + grid
- **brutalist** - technical, raw, manifesto → mono + heavy borders + asymmetry
- **retro-futuristic** - product launches, sci-fi adjacent → 80s gradients + grid floors
- **luxury** - high-end services, premium positioning → thin serifs + gold accents + black
- **industrial** - infrastructure, ops, internal tools → utility fonts + grid + ALL CAPS labels

Do NOT mix directions. Pick one and execute precisely. State your pick in chat before generating.

### 5. Brand layer (opt-in only)

`Glob` the working folder for `assets/`, `brand/`, `logos/`, `**/*logo*.{svg,png,jpg}`.

If the user has explicitly named a brand AND assets exist:
- Identify the relevant logo file(s)
- Inline small SVGs as base64; reference larger PNG/JPG via `./assets/...` relative paths
- Sample brand colors from the logo (or ask the user for hex codes)
- Override the aesthetic's CSS variables with brand colors

Otherwise: skip this step entirely.

### 6. Generate the HTML

- Start from `templates/base.html` (read it, copy into output).
- For each outlined section, read the matching `templates/section-<type>.html` and adapt it - rewrite copy to fit the source content. Keep the CSS class names; tweak inline styles only where the aesthetic demands.
- All section CSS lives in the single `<style>` block - merge per-section styles, deduplicate.
- Body copy must follow Piotr's rules: **no em-dashes**, plain language, no AI tells (passive voice piles, "delve", "landscape", "leverage", "unlock", "navigate the complexities", "stands as a testament", "evolving").
- Write the file to `./presentations/<kebab-case-slug>.html`.

### 7. Verify

Read `references/verification-rules.md` for the full checklist. Minimum verification:
- File written, valid HTML5
- No `—` characters in the output (grep for it)
- No occurrence of `Inter`, `Roboto`, `Arial`, `system-ui` in `font-family`
- All `./assets/...` referenced files actually exist on disk
- If `mcp__Claude_in_Chrome__*` is available: navigate to `file://` URL, screenshot the hook section + one mid section, confirm no overflow/404s

Fix issues found, re-verify, then continue.

### 8. Hand back

Output to chat:
1. File path (clickable)
2. One-line summary of section count + aesthetic direction
3. How to view: open in Chrome, or run `open <path>` in terminal
4. Suggested next prompts: *"now apply <brand>"*, *"rewrite section N"*, *"swap the aesthetic to <other>"*

## Reference files (load on demand)

| File | Load when |
|---|---|
| `references/ingestion-patterns.md` | Step 2 - any input parsing question |
| `references/slide-types.md` | Step 3 - section mapping |
| `references/design-system.md` | Step 4 - aesthetic + copy rules |
| `references/building-protocol.md` | Step 6 - HTML assembly mechanics |
| `references/verification-rules.md` | Step 7 - QA checklist |
| `assets/font-pairings.md` | Step 4 - picking fonts |
| `templates/base.html` | Step 6 - skeleton |
| `templates/section-*.html` | Step 6 - per section |
| `examples/from-yt-transcript.html` | When unsure what "good" looks like - read this as a reference output |

## Reuse other skills

- **`humanizer`** - after drafting headlines/body, mentally run the copy through humanizer rules (or invoke the skill if the user requests aggressive humanization). Strip AI tells.
- **`frontend-design`** plugin - the design principles in `references/design-system.md` extend it. If the user wants raw frontend output (not a presentation), defer to `frontend-design` instead.

## Common mistakes (avoid)

- Producing a generic Bootstrap-looking deck with Inter + purple buttons
- Forgetting `100dvh` fallback (mobile Safari)
- Cramming 6 bullets onto one section (limit: 3-7 items, and only on `steps`/`comparison` types)
- Skipping the brand check when the user already pointed at an `assets/` folder
- Wrapping every section in `<div class="container">` - kills the asymmetry
- Using SVG `<use>` without inlining the symbol (breaks in `file://`)
- Writing CTA links to `#` placeholders - either use a real link or ask the user
