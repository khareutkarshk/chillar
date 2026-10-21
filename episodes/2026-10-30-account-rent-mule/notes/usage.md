# Usage — 2026-10-30-account-rent-mule (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 05:42 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 28 | 292 | 605,432 | $0.40 |
| script | 4 | 44 | 63,265 | 757,342 | $1.41 |
| factcheck | 4 | 28 | 17,617 | 335,022 | $0.40 |
| voice | 1 | 6 | 61 | 41,307 | $0.06 |
| edit | 6 | 68 | 89,595 | 942,411 | $1.29 |
| package | 1 | 8 | 59 | 38,231 | $0.07 |
| **total** | 17 | 182 | 170,889 | 2,719,745 | **$3.65** |

Review rounds: script 3 · video 1.
Local source retrieval: 5 searches · 9 excerpts · 1,993 chars returned from 15,731 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 5/3) · specific 4 · clarity 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
Latest reviewer report: swipe risk: 0–3s low · 3–15s med · middle low · payoff low · blockers 0 · polish notes 7 · STALE: final.mp4 rendered after this review
Mechanical QA: 0 errors · 0 warnings (qa.json updated 2026-10-21 05:41)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
