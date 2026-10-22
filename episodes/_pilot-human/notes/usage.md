# Usage — _pilot-human (agent runs, from notes/usage.jsonl)

Updated: 2026-10-22 15:05 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| factcheck | 1 | 6 | 143 | 80,344 | $0.07 |
| voice | 1 | 7 | 45 | 42,696 | $0.05 |
| edit | 9 | 96 | 145,225 | 1,493,673 | $1.34 |
| package | 1 | 7 | 43 | 26,788 | $0.06 |
| **total** | 12 | 116 | 145,456 | 1,643,501 | **$1.52** |

Review rounds: script 0 · video 2.
Latest reviewer report: swipe risk: 0–3s low · 3–15s low · middle low · payoff low · blockers 0 · polish notes 0 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 3 warnings (qa.json updated 2026-10-22 15:04)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
