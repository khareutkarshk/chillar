# Usage — 2026-11-12-salary-12-days (agent runs, from notes/usage.jsonl)

Updated: 2026-10-22 07:09 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 10 | 221 | 131,503 | $0.17 |
| script | 4 | 44 | 81,560 | 943,071 | $1.99 |
| factcheck | 1 | 8 | 156 | 81,836 | $0.09 |
| voice | 2 | 12 | 380 | 71,892 | $0.13 |
| edit | 6 | 28 | 125,229 | 379,581 | $0.90 |
| package | 1 | 8 | 56 | 42,725 | $0.08 |
| components | 1 | 28 | 331 | 311,146 | $0.20 |
| **total** | 16 | 138 | 207,933 | 1,961,754 | **$3.58** |

Review rounds: script 2 · video 1.
Latest script quality: scores: stop 4 · laughs 4 (count 7/6) · specific 4 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 4 · fresh 3 · facts PASS
Score evidence: best laughs L9 · weakest fresh L12
Latest reviewer report: swipe risk: 0–3s low · 3–15s low · middle med · payoff med · blockers 0 · polish notes 6 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 10 warnings (qa.json updated 2026-10-22 07:06)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
