# Ingestion Patterns (Growgo variant)

Same logic as the parent skill, plus one Growgo-specific step: **language detection**.

## Language detection (Growgo addition)

Before chunking, detect the source language:

1. Sample the first 500 words of the input.
2. Count Polish-specific characters: `ą ć ę ł ń ó ś ź ż`.
3. If count ≥ 5 - source is Polish. Generate output in Polish.
4. If count < 5 - source is English (or another language - confirm with user if uncertain).
5. Set the deck's language flag. All copy must match.

If the source is mixed (PL transcript with EN quotes), generate in the dominant language and keep EN technical terms native (e.g., "prompt", "workflow", "use case" stay English in PL copy - per `growgo-brand` tone-overview).

## YouTube transcript (.txt / .md)

Two cases - identical to parent skill.

**Case A - transcript with chapter markers.** Look for patterns like:
```
*0:00 Wstęp*       (PL)
*0:30 What we're building today*    (EN)
```
Split on chapter markers - each is one block.

**Case B - flat transcript, no markers.** Segment by topic shift:
1. Drop filler tokens. PL fillers: *no, więc, generalnie, w sumie, jakby*. EN fillers: *um, uh, like, you know, right?*.
2. Cluster paragraphs by transition signals. PL: *"Dobra, to teraz...", "No i tak..."*, *"Następna rzecz..."*, *"Pokażę wam..."*. EN: same as parent.
3. Target 8-14 blocks. Merge under 60 words; split over 400 words.

## PDF

Same as parent. Use `Read` with `pages` parameter, extract headings from font size signals.

For Polish PDFs: watch for diacritics in heading detection - some PDFs encode `ł` weirdly.

## Markdown / .docx / plain text

Same as parent. Use `#` / `##` heading structure.

For .docx: try `pandoc` via Bash. If absent, ask user to export as md.

## Notion page

Same as parent. Use `notion-fetch` MCP. Walk block tree, heading blocks = section breaks.

## After ingestion

Output is the same shape as parent:
```
[
  {heading: "...", body: "...", language: "pl|en"},
  ...
]
```

Then proceed to section mapping (`slide-types.md`) and generation.

## Edge cases

- **Empty input** - stop, tell the user.
- **Single block (< 200 words)** - too short. Offer one-pager instead.
- **Mixed languages** - generate in the dominant, keep EN technical terms native.
- **Code blocks** - send to `terminal` section (but de-prioritize - Growgo audience is mostly non-tech).
- **Source has emoji** - strip them. Growgo brand bans emoji.
