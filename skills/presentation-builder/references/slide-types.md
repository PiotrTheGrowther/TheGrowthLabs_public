# Slide Types

11 section types. Each maps from a block in the ingestion output. Pick the type per block based on shape and intent.

## Type catalog

### 1. `hook` - opening section (always first)
**When**: First section, always. Sets the thesis in 5-10 words.
**Content shape**: oversized headline (12-20 word max), optional kicker line above (`01 / 11`, the deck title, or a date), no body copy.
**Mapping signal**: pull from the first block. If the input is a transcript, use the first claim the speaker makes after the intro.

### 2. `metric` - one striking number
**When**: Any block that contains a number worth amplifying (`7x faster`, `1:7 ratio`, `3 minutes`, `82% retention`).
**Content shape**: one giant figure (`7x`), one short label line below (3-8 words: *"output per operator"*), optional 1-line context.
**Mapping signal**: scan body for numerals. If multiple numbers, pick the most surprising.

### 3. `before-after` - old way vs. new way
**When**: Block that compares two states (without X / with X · before / after · old / new).
**Content shape**: two stacked cards. Left/top: BEFORE state (3-4 short lines). Right/bottom: AFTER state (3-4 short lines).
**Mapping signal**: presence of "used to", "before", "now", "instead", "switched from".

### 4. `quote` - pull quote
**When**: A line in the input that lands harder when isolated. Use at least once per deck.
**Content shape**: large body of the quote (60-200 chars), small attribution below.
**Mapping signal**: declarative sentence with high signal density. Often the strongest sentence in a block.

### 5. `steps` - numbered process
**When**: Block describes a sequence of 3-7 actions.
**Content shape**: numbered cards (`01`, `02`, `03`), each with a 3-7 word action title + 1 line of detail.
**Mapping signal**: imperatives ("upload", "drop", "drag", "run", "open"), enumerated lists in source.

### 6. `timeline` - chronology / roadmap
**When**: Dates, milestones, or phases.
**Content shape**: vertical timeline. Each entry: date/label on left, title + 1-line detail on right.
**Mapping signal**: dates, year markers, phase names ("Q1", "v1", "Phase 2", "Now").

### 7. `logo-grid` - brand / tool / asset showcase
**When**: List of tools, brands, integrations, partners.
**Content shape**: 4-12 logos in a grid. Optional caption under each (1-3 words).
**Mapping signal**: comma-separated list of named entities ("Notion, Linear, Slack, GitHub"). Or when the user has supplied a folder of logos.

### 8. `comparison` - multi-axis table
**When**: Comparing options across criteria.
**Content shape**: table with 2-4 columns, 3-6 rows. Highlight the winner.
**Mapping signal**: phrases like "compared to", "vs", "the difference between", explicit pros/cons.

### 9. `terminal` - code / CLI moment
**When**: Block contains code, command-line output, or technical instruction.
**Content shape**: dark terminal-style block, mono font, optional scanlines, prompt char (`$` or `>`).
**Mapping signal**: backtick code in source, command-like text (`npm install`, `git push`, `ssh user@host`).

### 10. `workspace` - file tree / folder structure
**When**: Block describes a directory layout, file org, or system topology.
**Content shape**: indented tree with mono font, file/folder icons via unicode (`├─`, `└─`, `│`).
**Mapping signal**: words "folder", "directory", "structure", "tree", or actual file paths in source.

### 11. `cta` - closing call-to-action (always last)
**When**: Last section, always.
**Content shape**: one bold headline (5-10 words: *"Want to build one?"*), one link or button, one supporting line.
**Mapping signal**: pull from the user's intent for the deck. If the source has a CTA (newsletter signup, link, contact), use it. Else ask the user.

## Outline rules

- **Total sections**: 8-14
- **Required**: exactly 1 `hook`, exactly 1 `cta`, ≥1 `quote`, ≥1 `metric`, ≥1 `steps`, ≥1 `before-after`
- **Variety**: no more than 2 consecutive sections of the same type
- **Rhythm**: alternate dense (steps, comparison, terminal, workspace) with sparse (quote, metric, hook). A wall of all-dense sections kills the deck.

## Mapping examples

| Input block heading | Best section type |
|---|---|
| *"It took 3 minutes to generate"* | `metric` (number = 3) |
| *"Drop the zip into settings"* | `steps` (imperative sequence) |
| *"Used to use Claude Code, now Cowork"* | `before-after` |
| *"This skill makes professional decks"* | `hook` (if first) or `quote` |
| *"Folder has transcripts/, assets/, logos/"* | `workspace` |
| *"npm install -g claude-code"* | `terminal` |
| *"Notion, Slack, GitHub integrations"* | `logo-grid` |
| *"Get the skill on Substack"* | `cta` |
