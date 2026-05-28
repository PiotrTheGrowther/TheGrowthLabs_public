---
name: ig-opinion-radar
description: >
  Find Instagram authors who hold a specific opinion or belief, expressed as a
  full sentence (not a keyword). Runs a 3-stage pipeline: (1) lexical wide-net
  via xpoz-mcp keyword search, (2) in-session semantic classification of each
  caption, (3) author rollup ranked by stance + confidence. Use when user says
  "find people on IG who think X", "find authors who believe Y", "opinion search
  on Instagram", "find creators who endorse <belief>", "ig opinion radar",
  "scan IG for stance Z", or pastes a belief/value statement and wants the
  people who hold it.
---

# IG Opinion Radar

Lexical search alone can't find opinions — keyword presence doesn't equal endorsement, and people paraphrase. This skill wraps the **xpoz-mcp** keyword search in a 2-stage pipeline that turns a belief sentence into a ranked list of authors who actually hold that belief, with cited evidence.

## Preconditions

- `xpoz-mcp` MCP connected (project scope). Verify tools `mcp__xpoz-mcp__getInstagramPostsByKeywords` etc. are available. If not, stop and tell the user.
- Read access to `~/.openrouter-key` is NOT required — the semantic layer is Claude reading captions in-session, no external LLM call.

## Core architecture

```
                  ┌── Stage 1: lexical harvest (xpoz, parallel)
                  │      4-6 boolean queries per opinion
                  │      → ~100-300 candidate posts
                  │
   OPINION ──────┤
                  │
                  └── Stage 2: in-session classification (Claude reads each caption)
                         stance ∈ {yes, partial, no, unrelated}
                         + confidence + evidence_quote + rationale
                                  │
                                  └── Stage 3: author rollup + score
                                          score = Σ(conf × stance_weight)
                                          weights: yes=1.0, partial=0.5
```

## Invocation

```
/ig-opinion-radar <opinion sentence in any language>
```

Examples:
- `/ig-opinion-radar ubezpieczenie na życie to forma odpowiedzialności za rodzinę`
- `/ig-opinion-radar AI agents will replace marketing teams within 3 years`
- `/ig-opinion-radar bieganie to najtańsza forma terapii`

If no argument is passed:
> What opinion or belief should I scan IG for? Give me a full sentence, not just keywords - I need the value statement.

## Stage 1 — Lexical harvest

### 1.1 — Translate opinion into 4-6 lexical proxies

The opinion is a sentence; xpoz only does keyword matching. Decompose it into the **2-3 phrase families** that people actually use to express it in captions:

| Family | What to capture |
|---|---|
| Direct value | Exact phrase + close synonyms ("odpowiedzialność za rodzinę" + "za bliskich") |
| Action / behavior | What someone *does* if they hold the opinion ("zabezpieczam rodzinę", "kupiłem polisę dla dzieci") |
| Loved-ones framing | "dla bliskich", "dla najbliższych", "dla rodziny" |
| Legacy / future | "przyszłość dzieci", "spokój rodziny" |
| Emotional anchor | "miłość", "troska", "kocham" + family terms |

Always combine with the **subject anchor** (the noun phrase of the opinion - e.g. `"polisa na życie" OR "ubezpieczenie na życie"`) using AND.

**Boolean rules (xpoz syntax)**:
- AND / OR / NOT must have terms on both sides
- Wrap multi-word phrases in `"double quotes"`
- **AVOID nested parens with mixed AND/OR — xpoz silently degrades to OR-of-all-tokens.** Always prefer flat queries. If you need multiple anchor variants, fire them as separate parallel calls instead of one nested boolean. Verified: `(A OR B) AND (C OR D)` returned 0 in-domain hits; `A AND C` (where A is the strongest anchor and C is the strongest co-term) returned 30 valid hits in the same cache.
- No field operators (`from:`, `lang:`) — they get stripped
- Forward slashes treated as spaces

**Preferred query shape**:
```
strongest_anchor AND strongest_co_term
```
e.g. `bieganie AND terapia` — not `("bieganie" OR "biegam") AND ("terapia" OR "terapeutyczne")`. To cover variants, fan out into N flat parallel queries:
```
bieganie AND terapia
biegam AND terapia
biegaczka AND terapia
```

### 1.2 — Fire queries in parallel

For each of the 4-6 families, one `getInstagramPostsByKeywords` call. **Always**:
- `forceLatest: true` — bypass cache, fetch real-time
- `limit: 200` — wide net
- `fields: ["id","userId","username","fullName","caption","createdAtDate","likeCount","codeUrl"]`
- **`startDate`: today minus 5 weeks (35 days), in YYYY-MM-DD** — recency filter, mandatory
- `userPrompt:` include the original opinion sentence (improves NLP-driven relevance)

Send all calls in a single message (parallel tool use).

**Recency rule (mandatory)**: pass `startDate` = (today − 35 days). Old content (2018, 2022, 226 weeks ago) is noise for active-creator discovery — the goal is to find creators currently posting on the topic, not historical posts. Compute the date in the current turn — don't hard-code. If the user explicitly asks for a different window ("past year", "all time", "last 7 days"), override and document the change in the output.

### 1.3 — Dedupe + filter language noise

After all returns:
- Dedupe by post `id`
- Drop posts whose caption is clearly non-target language (e.g. Italian / English / Russian on a Polish opinion search)
- Drop posts that hit on coincidental keywords but are off-topic (pet insurance for a life-insurance opinion, OC for a family-responsibility opinion, etc.)

Write deduped corpus to `ig-opinion-pipeline/posts.jsonl`, one JSON object per line with fields `id, username, fullName, date, likes, url, caption`.

## Stage 2 — Semantic classification (in-session)

For each post in `posts.jsonl`, read the caption and judge it yourself. Output one line per post to `ig-opinion-pipeline/classified.jsonl`:

```json
{"username":"...","fullName":"...","url":"...","stance":"yes|partial|no|unrelated","confidence":0.0-1.0,"quote":"<≤140 chars from caption>","rationale":"<one sentence>"}
```

### Stance rubric

| Stance | Use when |
|---|---|
| **yes** | Author personally endorses the opinion. Sales/agent content counts as `yes` if framing is unambiguously value-based (love, responsibility, family-protection-as-value). |
| **partial** | Frames the topic in the direction of the opinion but without the explicit value anchor. E.g. mentions family as one of several beneficiaries, but doesn't name the value. |
| **no** | Frames the topic differently. Catches negation, alternative framings (investment, tax optimization, business income protection, generic awareness), and product-mechanics posts that ignore the value question. |
| **unrelated** | Coincidental keyword match; post is about something else entirely. |

### Confidence calibration

- 0.90-1.00 — explicit verbatim or near-verbatim endorsement (the opinion's key words appear together with affirmative framing)
- 0.70-0.89 — clear thematic endorsement using paraphrase
- 0.40-0.69 — leaning but ambiguous; might be `partial`
- < 0.40 — weak evidence; usually `no` or `unrelated`

### Rules

- Treat **negation** as `no` (e.g. "ubezpieczenie na życie to NIE jest odpowiedzialność")
- Treat **quoting** without endorsement as `no`
- A post can be a single-line caption with hashtags — score `partial` low-confidence if signal is only in hashtags
- A brand account (PZU, ERGO, NN) gets the same rubric as any other author

## Stage 3 — Author rollup + ranking

Run `rollup.py` in the pipeline directory. It:
- Groups classifications by username
- Computes `score = Σ(yes × confidence) + Σ(partial × 0.5 × confidence)`
- Picks each author's strongest evidence quote (highest-confidence `yes`, falling back to `partial`)
- Writes `author_rollup.csv`: `rank, username, fullName, score, yes, partial, no, top_quote, top_url, top_rationale`

The script is in the skill folder: `Research_skills/ig-opinion-radar/rollup.py`. Copy it into the pipeline directory or invoke it inline.

## Output format to user

Three-part deliverable:

### Part 1 — Tier-1 table (score ≥ 0.80, the people who really hold this opinion)

| # | Author | Profile link | Score | Best quote | Evidence post |
|---|---|---|---|---|---|

Profile link is `https://www.instagram.com/<username>/`. Evidence post is the `top_url` from rollup (the Instagram permalink).

### Part 2 — Tier 2 + Tier 3 summary

Brief paragraph naming Tier 2 (`partial`, score 0.2-0.79) and Tier 3 (`no` / counter-framings, score 0.0) — one line each, listing authors and what their alternative frame is (investment / business income / product mechanics / etc.). This is signal too — it tells you who *doesn't* hold the opinion and why.

### Part 3 — Artefacts + next moves

Always list at the bottom:
- `posts.jsonl` — raw corpus (with permalink URLs)
- `classified.jsonl` — classifications
- `author_rollup.csv` — full leaderboard
- Suggested next steps (enrichment, Notion push, content fingerprint)

## File layout

For every run:
```
ig-opinion-pipeline/
├── posts.jsonl              # Stage 1 output (deduped corpus)
├── classified.jsonl         # Stage 2 output (your stance judgments)
├── author_rollup.csv        # Stage 3 output (ranked leaderboard)
└── email_summary.html       # Stage 4 output (only if --email flag passed)
```

Use the current working directory as the parent. If a previous `ig-opinion-pipeline/` exists from another run, archive it first or use a dated suffix (e.g. `ig-opinion-pipeline-2026-05-21-marathon/`).

## Stage 4 — Email delivery (opt-in)

If the user invokes with `--email` (or `--email <recipient>`), fire off an email after Stage 3 completes.

### Mechanism: n8n webhook

The skill does NOT call Gmail / SMTP / external mail providers directly. It POSTs a JSON payload to an n8n webhook; n8n handles the actual Gmail send. This keeps credentials out of the skill, lets you swap delivery channels (Slack, Telegram) without touching the skill, and makes cron-scheduled runs trivial via n8n.

### Webhook URL resolution

Look for the webhook URL in this order:
1. `IG_OPINION_RADAR_WEBHOOK` env var
2. `~/.ig-opinion-radar-webhook` file (single line)
3. If neither, stop and tell the user to set one of them

### Header token (Header Auth)

The webhook is gated by n8n Header Auth. The sender MUST include header `X-Radar-Token: <token>`. Resolve the token in this order:
1. `--token <value>` CLI flag
2. `IG_OPINION_RADAR_TOKEN` env var
3. `~/.ig-opinion-radar-token` file (single line)
4. If none, stop and tell the user to set one of them

The token is a shared secret stored in two places: the n8n credential `IG Opinion Radar Token` (Header Auth) and the local file/env var above. They must be identical strings. Regenerate with `openssl rand -hex 32` if leaked.

### Recipient

Default to `you@example.com` (set `DEFAULT_TO` in `send_email.py` to your own address). Override the primary with `--email <recipient@domain>` (maps to `send_email.py --to <recipient>`). Optional cc/bcc via repeated `--cc <addr>` and `--bcc <addr>` flags on `send_email.py`. Emails are always sent **from** whichever Gmail account is wired into the n8n `Gmail Send` credential (fixed in n8n, not settable from the skill).

### Payload shape

`Research_skills/ig-opinion-radar/send_email.py` constructs and POSTs this JSON:

```json
{
  "opinion": "<the original opinion sentence>",
  "to": "you@example.com",
  "subject": "IG Opinion Radar: <opinion truncated to 60 chars> - N authors",
  "summary": {
    "tier1_count": 6,
    "tier2_count": 12,
    "total_authors": 21,
    "corpus_size": 30,
    "date_window": "2026-04-22 to 2026-05-27"
  },
  "html_body": "<full HTML email body with Tier 1/2/3 tables + clickable profile links + evidence post links>",
  "markdown_body": "<same as html_body but markdown>",
  "csv_attachment_b64": "<base64-encoded author_rollup.csv>",
  "csv_filename": "ig-opinion-radar-<slug>-<date>.csv",
  "run_artefacts_path": "<absolute path to ig-opinion-pipeline-* folder>"
}
```

### n8n workflow shape (build once)

Standard 3-node flow:
1. **Webhook trigger** — POST endpoint, expects the payload above
2. **Function node** — decode `csv_attachment_b64` into a binary file
3. **Gmail Send** — `to` = payload.to, `subject` = payload.subject, `htmlBody` = payload.html_body, attach the CSV

Optional 4th node: log row to a Sheets tab (`Date | Opinion | Tier1 Count | Recipient | Status`) for audit/cron observability.

### Execution

Call the helper script after Stage 3:
```
python3 Research_skills/ig-opinion-radar/send_email.py \
  --pipeline-dir ig-opinion-pipeline-<slug>-<date> \
  --opinion "<original opinion>" \
  --to <recipient or default>
```

The script reads `author_rollup.csv` + `classified.jsonl` from the pipeline dir, renders the email body, base64s the CSV, and POSTs. On success, log the n8n response in chat. On failure, surface the HTTP error verbatim.

## Cost discipline

- xpoz `forceLatest: true` is expensive. 4-6 parallel calls per run is the design ceiling — don't loop endlessly trying to refine.
- Stage 2 is free (in-session) but token-heavy. Filter aggressively in Stage 1.3 before classifying — typical post counts after dedup+filter: 30-80, sweet spot is ~50.
- Don't enrich (follower count etc.) by default — only when user explicitly asks.

## Common gotchas

- **Boolean query collapse**: long OR-chains with many parens sometimes return ~1 result from cache. Workaround: split into 2-3 simpler parallel queries with `forceLatest: true`.
- **Non-target-language hits**: phrases like "polisa życiowa" can lexically match Italian "polizia" plurals; "bieg" matches English "begin/began/biggest". Always do Stage 1.3 language filter.
- **3-letter root anchor collisions**: Polish 3-letter roots (`bieg`, `lot`, `pas`, `dom`, `kot`) collide with English tokens via substring matching. **Always use the inflected forms** (`bieganie`, `biegam`, `biegaczka`) and skip bare roots. Same rule applies to other languages.
- **Brand accounts dominate**: a single brand may have 5 posts in the corpus. Rollup naturally weights this (high score = many posts). That's correct — but flag it in the output ("X dominates with N posts").
- **Sales agents over-cluster on yes**: when the opinion's domain has a sales class (insurance agents, supplement vendors, coaches), they will mostly endorse the opinion. Surface the rare counter-framings (Tier 3) explicitly — they're more informative than the obvious yes-cluster.
- **xpoz subtitles**: `getInstagramPostsByKeywords` also searches video subtitles — captions returned may include auto-transcribed Reel audio. Treat as caption text.
- **Sparse-discourse opinions**: not every belief has dense IG articulation. Hobbies (running, cycling, climbing), niche subcultures, and visually-driven topics often have hashtag-only captions with no value language. See "Sparseness guard" below.

## Sparseness guard

After Stage 1.3 dedup + filter, if the surviving corpus has **<10 candidates**, do NOT force a Tier-1 table. Instead, report:

1. **Honest count**: "Found N candidate posts after filtering Y raw hits"
2. **Pattern explanation**: why the discourse is thin (English captions, hashtag-only, video-heavy, sales-class missing, etc.)
3. **The N candidates themselves**: list them with stance judgment, even if all are `partial` or `no`
4. **Zero-yes flag**: if no post scores `yes`, say so explicitly — that IS the finding

A thin honest report beats a fabricated leaderboard. The user benefits more from "this opinion isn't articulated on IG in this language" than from a weak ranking padded with `partial` rows.

## Anti-patterns

- ❌ Calling out to an external LLM (OpenAI/OpenRouter/Anthropic API) for Stage 2 — Claude in-session already does this perfectly and avoids auth/latency/cost
- ❌ Running Stage 2 over hundreds of posts — if you have >100 after dedup, tighten Stage 1 queries first
- ❌ Keyword-only matching without semantic Stage 2 — that's just an xpoz search, defeats the skill's purpose
- ❌ Skipping Stage 1.3 noise filter — beauty pageant accounts will pollute Polish life-insurance results

## Push to Notion (on request)

If the user says "push Tier 1 to Notion" or similar, map the rollup into your own Notion Leads database (set the database ID in your environment). Map:
- Name → `fullName`
- LinkedIn URL → Instagram URL (`https://www.instagram.com/<username>/`)
- Search Criteria → `opinion=<opinion_slug>`
- Notes → `top_quote`
