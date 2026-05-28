# TheGrowthLabs Public

Open-source artifacts from [TheGrowthLabs](https://thegrowthlabs.io) - an AI-native marketing agency. Skills, workflows, and prompts we use to multiply marketing output without growing the team.

## What's here

### Claude Skills

| Skill | What it does |
|---|---|
| [`presentation-builder`](./skills/presentation-builder/) | Turns transcripts, PDFs, markdown, or Notion pages into a single self-contained vertical scroll-snap HTML presentation site. No generic AI aesthetics. |
| [`growgo-presentation-builder`](./skills/growgo-presentation-builder/) | Growgo-branded variant of `presentation-builder`. Same scroll-site format, with Growgo brand baked in: Roboto, `#FEBF2D` yellow accent, `#EFEFEF` background, yellow-highlight signature, dark/white logo, ekspercka tone. PL + EN auto-detect. |
| [`ig-opinion-radar`](./skills/ig-opinion-radar/) | Finds Instagram authors who hold a specific opinion (a full sentence, not a keyword) and ranks them by how strongly they endorse it, with cited evidence. Lexical harvest → in-session semantic classification → scored author leaderboard + CSV. Optional one-flag email delivery. Language-agnostic. |

### Workflows

| Workflow | What it does |
|---|---|
| [`Ghostwrite-and-CMP-workflow.md`](./Ghostwrite-and-CMP-workflow.md) | End-to-end content marketing pipeline - ingestion through generation. |

## Using these in Claude Cowork

Most skills here ship as a `.zip` you drag into Cowork's Settings → Capabilities → Skills. Each skill folder has a README with install steps.

## Using these in Claude Code (CLI)

```bash
# clone this repo
git clone https://github.com/PiotrTheGrowther/TheGrowthLabs_public.git

# copy any skill into your local skills folder
cp -r TheGrowthLabs_public/skills/presentation-builder ~/.claude/skills/
```

The skill auto-loads on the next Claude Code session.

## Contributing

Issues and PRs welcome. If you build on top of one of these skills, open a PR or send a link - happy to feature it here.

## License

MIT
