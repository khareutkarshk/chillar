# Usage — 2026-10-31-epf-wage-ceiling (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 05:51 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 27 | 437 | 435,040 | $0.28 |
| script | 4 | 34 | 74,361 | 602,692 | $1.34 |
| factcheck | 4 | 34 | 25,172 | 392,132 | $0.47 |
| voice | 1 | 7 | 60 | 62,296 | $0.06 |
| edit | 6 | 58 | 91,220 | 1,023,135 | $1.22 |
| package | 1 | 7 | 58 | 28,595 | $0.07 |
| components | 1 | 34 | 331 | 443,816 | $0.23 |
| **total** | 18 | 201 | 191,639 | 2,987,706 | **$3.68** |

Review rounds: script 3 · video 1.
Local source retrieval: 7 searches · 16 excerpts · 3,521 chars returned from 403,423 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 4/3) · specific 4 · clarity 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
Latest reviewer report: swipe risk: 0–3s low · 3–15s med · middle low · payoff med · blockers 0 · polish notes 6 · STALE: final.mp4 rendered after this review
Mechanical QA: 0 errors · 1 warnings (qa.json updated 2026-10-21 05:51)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
