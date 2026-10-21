# Usage — 2026-11-11-bhai-dooj-gift-tax (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 20:06 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 42 | 170 | 843,301 | $0.43 |
| script | 4 | 42 | 76,526 | 998,700 | $1.74 |
| factcheck | 1 | 5 | 160 | 77,823 | $0.09 |
| voice | 1 | 8 | 62 | 61,859 | $0.06 |
| edit | 5 | 53 | 100,968 | 772,946 | $1.01 |
| package | 1 | 5 | 60 | 72,523 | $0.09 |
| **total** | 13 | 155 | 177,946 | 2,827,152 | **$3.43** |

Review rounds: script 2 · video 1.
Local source retrieval: 3 searches · 9 excerpts · 1,976 chars returned from 1,696,406 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 3/3) · specific 3 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
Score evidence: best laughs L8 · weakest specific L7
Latest reviewer report: swipe risk: 0–3s low · 3–15s med · middle med · payoff low · blockers 0 · polish notes 8 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 2 warnings (qa.json updated 2026-10-21 20:04)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
