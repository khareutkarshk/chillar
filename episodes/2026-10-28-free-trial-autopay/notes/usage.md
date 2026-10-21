# Usage — 2026-10-28-free-trial-autopay (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 05:51 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 16 | 260 | 230,357 | $0.25 |
| script | 2 | 14 | 46,345 | 246,518 | $0.82 |
| factcheck | 1 | 10 | 160 | 116,570 | $0.10 |
| voice | 2 | 11 | 388 | 71,389 | $0.10 |
| edit | 9 | 61 | 140,792 | 955,290 | $1.46 |
| package | 1 | 7 | 60 | 28,011 | $0.07 |
| **total** | 16 | 119 | 188,005 | 1,648,135 | **$2.80** |

Review rounds: script 1 · video 2.
Local source retrieval: 8 searches · 12 excerpts · 2,817 chars returned from 10,406 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 5/3) · specific 4 · clarity 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
Latest reviewer report: swipe risk: 0–3s low · 3–15s low · middle low · payoff low · blockers 0 · polish notes 3 · STALE: final.mp4 rendered after this review
Mechanical QA: 0 errors · 2 warnings (qa.json updated 2026-10-21 05:15)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
