# Usage — _pilot-human (agent runs, from notes/usage.jsonl)

Updated: 2026-10-22 15:31 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| factcheck | 1 | 6 | 143 | 80,344 | $0.07 |
| voice | 1 | 7 | 45 | 42,696 | $0.05 |
| edit | 13 | 152 | 185,528 | 2,209,039 | $1.81 |
| package | 1 | 7 | 43 | 26,788 | $0.06 |
| **total** | 16 | 172 | 185,759 | 2,358,867 | **$2.00** |

Review rounds: script 0 · video 1.
Latest reviewer report: swipe risk: 0–3s med · 3–15s low · middle low · payoff low · blockers 0 · polish notes 6 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 11 warnings (qa.json updated 2026-10-22 15:30)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
