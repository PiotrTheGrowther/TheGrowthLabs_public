━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WORKFLOW 1: CMP INGESTION           [Daily @ 7:00 AM]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  DATA SOURCES (3 branches in parallel)
  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
  │   YOUTUBE       │  │   X / TWITTER   │  │   NEWSLETTERS   │
  │                 │  │                 │  │                 │
  │ Monitored       │  │ Monitored       │  │ Dedicated email │
  │ channels        │  │ accounts        │  │ inbox           │
  │                 │  │                 │  │                 │
  │ RSS feed +      │  │ Social API      │  │ Email API       │
  │ transcript API  │  │ Recent posts    │  │ Full body       │
  │                 │  │                 │  │ extraction      │
  │ Filter: 36h     │  │                 │  │ newer_than: 2d  │
  │ window          │  │                 │  │                 │
  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
           │                    │                     │
           │   Normalize to unified schema:           │
           │   source_type / author / title /         │
           │   raw_text / content_hash / url          │
           │                    │                     │
           └────────────────────┼─────────────────────┘
                                ↓
                         [Deduplicate]
                         Hash on normalized text
                                ↓
                    ┌─────────────────────┐
                    │   AIRTABLE          │
                    │   RAW_CONTENT       │
                    │                     │
                    │ ~50-70 items/day    │
                    │ YT / X / Newsletter │
                    └─────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WORKFLOW 2: CMP GENERATION          [Mon + Wed + Fri @ 9:00 AM]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    ┌─────────────────────┐
                    │   AIRTABLE          │
                    │   RAW_CONTENT       │
                    │   (rolling 30 days) │
                    │   ~500-700 items    │
                    └──────────┬──────────┘
                               ↓
                    ┌──────────────────────┐
                    │  IF Has Content?     │
                    └──────┬──────┬────────┘
                         YES     NO → Slack warning
                           ↓
              ┌────────────────────────────┐
              │  STAGE 1 - ANALYZE         │
              │  GPT-4o-mini | temp 0.2    │
              │  Persona: Trend Analyst    │
              │  → 5-8 themes + hashes     │
              └────────────┬───────────────┘
                           ↓
              ┌────────────────────────────┐
              │  STAGE 2 - IDEATE          │
              │  GPT-4o-mini | temp 0.7    │
              │  Persona: Strategist       │
              │  → 3 draft topics          │
              │  + source references       │
              └────────────┬───────────────┘
                           ↓
                    [Validate references]
                    Drop hallucinated ones
                           ↓
              ┌────────────────────────────┐
              │  STAGE 3 - REFINE          │
              │  GPT-4o-mini | temp 0.3    │
              │  Persona: Editor           │
              │  → 3 polished topics       │
              │  title + angle + brief     │
              └────────────┬───────────────┘
                           ↓
              ┌────────────────────────────┐
              │  Extract Slack Message     │
              │  Generate topic_id:        │
              │  cmp_YYYYMMDD_1/2/3        │
              └──────┬──────────┬──────────┘
                     ↓          ↓
             ┌───────────┐  ┌──────────────────────┐
             │   SLACK   │  │   AIRTABLE            │
             │  #cmp-    │  │   TOPIC_SUGGESTIONS   │
             │  content  │  │                       │
             │  -ideas   │  │ title / brief / angle │
             │           │  │ topic_id / run_id     │
             │ title     │  │ source references     │
             │ brief     │  │ confidence            │
             │ topic_id  │  └──────────────────────┘
             └───────────┘
                    ↑
             USER reads,
             picks a topic,
             copies topic_id


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WORKFLOW 3: GHOSTWRITER             [On-demand, Slack slash command]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  USER types:
  /ghostwriter_cmp cmp_topic_id
              ↓
  ┌─────────────────────────────────┐
  │  Parse Slack Input              │
  │  Extract topic_id from command  │
  └──────────────┬──────────────────┘
                 ↓
  ┌─────────────────────────────────┐
  │  Parallel lookup                │
  │                                 │
  │  [Brand Memory sub-workflow]    │
  │  persona / tone / pillars /     │
  │  writing rules                  │
  │                                 │
  │  [Airtable TOPIC_SUGGESTIONS]   │
  │  fetch by topic_id →            │
  │  title + brief + angle +        │
  │  source references[]            │
  └──────────────┬──────────────────┘
                 ↓
  ┌─────────────────────────────────┐
  │  Airtable RAW_CONTENT           │
  │  Fetch original source material │
  │  matched by source references   │
  └──────────────┬──────────────────┘
                 ↓
  ┌─────────────────────────────────┐
  │  Build Prompt                   │
  │  system: brand voice + rules    │
  │  user: topic brief/angle +      │
  │        source excerpts          │
  └──────────────┬──────────────────┘
                 ↓
  ┌─────────────────────────────────┐
  │  CLAUDE OPUS                    │
  │  temp 0.6 | max 4000 tokens     │
  │                                 │
  │  OUTPUT:                        │
  │  - LinkedIn post                │
  │  - X thread                     │
  │  - Hashtags                     │
  │  - Posting note                 │
  └──────────────┬──────────────────┘
                 ↓
        ┌────────┴────────┐
        ↓                 ↓
  ┌──────────┐   ┌─────────────────┐
  │  NOTION  │   │ Mark topic used │
  │ Ghostwr. │   │ Airtable:       │
  │  DB page │   │ used_for_content│
  │          │   │ = true          │
  │ LinkedIn │   └─────────────────┘
  │ X thread │
  │ Sources  │
  └──────────┘
        ↓
  Slack ✅ reply


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HANDOFF KEYS (what connects the 3 workflows)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  content_hash  →  connects RAW_CONTENT to TOPIC_SUGGESTIONS
                   (traces every generated topic back to its sources)

  topic_id      →  connects TOPIC_SUGGESTIONS to Ghostwriter
                   (cmp_YYYYMMDD_N — USERS's handoff key)