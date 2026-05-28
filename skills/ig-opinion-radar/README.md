# IG Opinion Radar

A Claude skill that finds Instagram authors who **hold a specific opinion** - expressed as a full sentence, not a keyword - and ranks them by how strongly they endorse it, with cited evidence.

Lexical search alone can't find opinions: keyword presence isn't endorsement, and people paraphrase. This skill wraps an Instagram keyword search in a 3-stage pipeline that turns a belief sentence into a ranked list of the people who actually hold it.

## What you get

- **Tier-1 leaderboard** - authors who clearly hold the opinion (score ≥ 0.80), with profile links and the exact evidence quote
- **Tier 2 / Tier 3 breakdown** - who frames the topic differently, and how (the counter-framings are often the most useful signal)
- **Artefacts** - `posts.jsonl` (raw corpus), `classified.jsonl` (per-post stance judgments), `author_rollup.csv` (full ranked leaderboard)
- **Optional email delivery** - a one-flag `--email` hand-off that POSTs the rollup to your own n8n webhook, which sends a formatted summary with the CSV attached

## How it works

```
                  ┌── Stage 1: lexical harvest (parallel keyword search)
                  │      4-6 flat "A AND B" queries per opinion
   OPINION ──────┤
                  ├── Stage 2: in-session classification (Claude reads each caption)
                  │      stance ∈ {yes, partial, no, unrelated} + confidence + evidence
                  └── Stage 3: author rollup + score
                         score = Σ(yes × conf) + Σ(partial × 0.5 × conf)
```

The semantic layer is **Claude reading captions in-session** - no external LLM API call, no extra auth or cost.

## Prerequisites

This skill is not fully self-contained - it depends on two external pieces you supply:

| Dependency | Why | Required for |
|---|---|---|
| An Instagram keyword-search MCP (the skill is written against [`xpoz-mcp`](https://xpoz.ai), tools like `getInstagramPostsByKeywords`) | Stage 1 harvest | Core skill |
| An n8n webhook + Gmail (or swap for Slack/Telegram) | Stage 4 email delivery | Only the `--email` flag |

Without the MCP the harvest stage can't run. The email stage is fully optional - skip it and you still get the leaderboard + CSV. The n8n webhook shape is documented in `SKILL.md` → Stage 4 (build once, then point `~/.ig-opinion-radar-webhook` at it).

## Install

### Claude Cowork (recommended for non-devs)

1. Download `ig-opinion-radar.zip` from the parent folder ([direct link](../ig-opinion-radar.zip))
2. Open Claude Cowork
3. Settings → Capabilities → Skills → Add Skill
4. Drag the zip into the upload area

### Claude Code (CLI)

```bash
# Clone or download this folder, then:
cp -r ig-opinion-radar ~/.claude/skills/
```

The skill auto-loads on the next session.

## Use it

> Use the ig-opinion-radar skill to find IG authors who believe "life insurance is a form of responsibility to your family".

Claude decomposes the sentence into 4-6 lexical query families, harvests recent posts (last 5 weeks), reads each caption, scores every author, and writes the artefacts to `./ig-opinion-pipeline-<slug>-<date>/`.

### Email delivery

Add `--email` to also send the summary to your default recipient, or `--email someone@domain.com` to override:

```bash
python3 send_email.py \
  --pipeline-dir ig-opinion-pipeline-<slug> \
  --opinion "<the opinion sentence>" \
  --to you@example.com
```

Set `DEFAULT_TO` in `send_email.py` to your own address, and point `IG_OPINION_RADAR_WEBHOOK` (env var or `~/.ig-opinion-radar-webhook`) at your n8n webhook. The webhook is gated by a header token (`X-Radar-Token`) - see `SKILL.md` → Stage 4.

## Files

| File | What |
|---|---|
| `SKILL.md` | Full stage-by-stage spec: query decomposition, stance rubric, confidence calibration, anti-patterns, output format |
| `rollup.py` | Stage 3 - groups classifications by author, scores, picks best evidence quote, writes `author_rollup.csv` |
| `send_email.py` | Stage 4 - renders the HTML/markdown summary, base64s the CSV, POSTs to your n8n webhook |

## Notes

- Works in any language - the examples in `SKILL.md` are Polish, but the pipeline is language-agnostic
- Built for active-creator discovery: it filters to the last 5 weeks by default so you find people *currently* posting on the topic
- Honest about thin discourse: if a belief isn't articulated much on IG, it tells you that instead of padding a fake leaderboard
