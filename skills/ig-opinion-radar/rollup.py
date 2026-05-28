#!/usr/bin/env python3
"""Stage 3 of ig-opinion-radar: roll up classifications by author.

Reads ./classified.jsonl (one JSON per line, each with
username, fullName, url, stance, confidence, quote, rationale).
Writes ./author_rollup.csv (ranked leaderboard) and prints the
leaderboard to stdout for quick eyeballing.

Score: sum(confidence for stance=yes) + 0.5 * sum(confidence for stance=partial).
Each author's "top" evidence = highest-confidence yes, falling back to
the first partial, then the first row.

Usage:
    cd ig-opinion-pipeline && python3 rollup.py
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent if __file__ != "<stdin>" else Path.cwd()
IN_PATH = HERE / "classified.jsonl"
OUT_PATH = HERE / "author_rollup.csv"

if not IN_PATH.exists():
    sys.exit(f"missing {IN_PATH} - run Stage 2 first")

rows = [json.loads(l) for l in IN_PATH.read_text().splitlines() if l.strip()]

by = defaultdict(lambda: {
    "fullName": "",
    "yes": 0, "partial": 0, "no": 0, "unrelated": 0,
    "score": 0.0,
    "top": None,
})

for r in rows:
    a = by[r["username"]]
    a["fullName"] = r.get("fullName") or a["fullName"]
    st = r.get("stance", "unrelated")
    c = float(r.get("confidence", 0))
    a[st] = a.get(st, 0) + 1
    if st == "yes":
        a["score"] += c
        if (not a["top"]) or c > float(a["top"].get("confidence", 0)):
            a["top"] = r
    elif st == "partial":
        a["score"] += 0.5 * c
        if not a["top"]:
            a["top"] = r
    else:
        if not a["top"]:
            a["top"] = r

ranked = sorted(by.items(), key=lambda kv: -kv[1]["score"])

# CSV
lines = ["rank,username,fullName,score,yes,partial,no,unrelated,top_quote,top_url,top_rationale,profile_url"]
for i, (u, d) in enumerate(ranked, 1):
    t = d["top"] or {}
    q = (t.get("quote") or "").replace('"', "'").replace("\n", " ")[:200]
    rat = (t.get("rationale") or "").replace('"', "'").replace("\n", " ")[:250]
    url = t.get("url", "")
    profile = f"https://www.instagram.com/{u}/"
    lines.append(
        f'{i},{u},"{d["fullName"]}",{d["score"]:.2f},'
        f'{d["yes"]},{d["partial"]},{d["no"]},{d["unrelated"]},'
        f'"{q}",{url},"{rat}",{profile}'
    )
OUT_PATH.write_text("\n".join(lines) + "\n")
print(f"wrote {OUT_PATH} ({len(ranked)} unique authors)\n", file=sys.stderr)

# Leaderboard to stdout
print(f"{'#':>3} {'score':>5}  y/p/n/u   {'username':32s}  {'fullName':30s}")
print("-" * 110)
for i, (u, d) in enumerate(ranked, 1):
    print(
        f"{i:>3} {d['score']:>5.2f}  "
        f"{d['yes']}/{d['partial']}/{d['no']}/{d['unrelated']}     "
        f"{u:32s}  {d['fullName'][:30]}"
    )
