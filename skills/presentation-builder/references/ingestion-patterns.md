# Ingestion Patterns

Per-format procedure for turning raw input into `{heading, body}` blocks ready for section mapping.

## YouTube transcript (.txt / .md)

Two cases.

**Case A - transcript with chapter markers.** Look for patterns like:
```
*0:00 Intro*
*0:30 What we're building today*
*1:15 Uploading the skill*
```
Or numbered chapters at line starts (`1. Intro`, `## 0:30 What we're building`). Split on these markers - each chapter is one block.

**Case B - flat transcript, no markers.** Segment by topic shift:
1. Drop filler tokens (`um`, `uh`, `like`, `you know`, `right?`) when extracting copy - keep them out of headlines, may keep one or two in body to preserve voice.
2. Cluster paragraphs by semantic proximity. Look for transition signals: *"All right, so..."*, *"Now,..."*, *"The next thing..."*, *"Let me show you..."*. Each transition starts a new block.
3. Target 8-14 blocks total. Merge adjacent blocks under 60 words; split blocks over 400 words.

For each block, write a 3-7 word heading that captures the action or claim, not the topic. *"Upload the skill zip"* beats *"About the skill"*.

## PDF

1. Use `Read` with the `pages` parameter. Always read in chunks (max 20 pages per call).
2. First pass: extract all text. Look for repeated formatting that signals headings - lines under 10 words, followed by a blank line, often in title case.
3. Use those lines as section breaks. If the PDF has a TOC, use it as the skeleton.
4. Tables: convert to comparison-style sections (use `comparison` slide type). Mark them in the outline.
5. Figures/diagrams: out of scope v1 - mention to the user that diagrams were skipped.

## Markdown / .docx / plain text

1. Markdown - use `#` and `##` headings as block boundaries. Body is everything until the next heading at the same or higher level.
2. .docx - convert to markdown first via `pandoc` if available (`Bash` tool). If pandoc absent, ask the user to export as markdown or txt.
3. Plain text - apply the YouTube-flat-transcript clustering approach.

## Notion page

1. Use `notion-fetch` with the page URL.
2. Walk the block tree. Heading blocks (h1, h2, h3) are section boundaries. Body is the flat text of children until the next heading.
3. Toggles: expand and include their inner content as part of the parent block.
4. Embeds (videos, images): skip in v1, mention them to the user.

## After ingestion

You should have a list like:
```
[
  {heading: "Upload the skill zip", body: "Go to settings, capabilities..."},
  {heading: "Set up your folder", body: "Inside the folder, drop your transcripts..."},
  ...
]
```

Hand this off to step 3 (outline) - map each block to a section type from `slide-types.md`.

## Edge cases

- **Empty input** - stop, tell the user.
- **Single block input** (< 200 words total) - too short for a presentation, ask if they want a one-pager instead.
- **Mixed languages** - keep the source language for copy, do not translate unless asked.
- **Code blocks in input** - send them to a `terminal` slide type; keep formatting.
