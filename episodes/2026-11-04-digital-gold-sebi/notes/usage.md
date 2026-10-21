# Usage — 2026-11-04-digital-gold-sebi (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 16:38 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 23 | 234 | 416,485 | $0.28 |
| script | 4 | 31 | 75,424 | 650,307 | $1.62 |
| factcheck | 1 | 9 | 159 | 99,947 | $0.11 |
| voice | 1 | 7 | 61 | 59,020 | $0.07 |
| edit | 5 | 68 | 84,388 | 1,163,878 | $1.20 |
| package | 1 | 7 | 59 | 32,139 | $0.07 |
| **total** | 13 | 145 | 160,325 | 2,421,776 | **$3.36** |

Review rounds: script 2 · video 1.
Local source retrieval: 7 searches · 7 excerpts · 1,736 chars returned from 1,948 chars of matched sources
Latest script quality: scores: stop 3 · laughs 4 (count 5/3) · specific 4 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 4 · fresh 3 · facts PASS
Score evidence: best laughs L8 · weakest stop L1
Latest reviewer report: swipe risk: 0–3s low · 3–15s med · middle med · payoff low · blockers 0 · polish notes 6 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 1 warnings (qa.json updated 2026-10-21 16:37)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
