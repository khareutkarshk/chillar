# Usage — 2026-11-08-diwali-receipt (agent runs, from notes/usage.jsonl)

Updated: 2026-10-22 07:07 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 12 | 151 | 162,824 | $0.18 |
| script | 6 | 59 | 105,699 | 1,002,151 | $2.35 |
| factcheck | 1 | 5 | 156 | 78,163 | $0.09 |
| voice | 2 | 11 | 380 | 69,336 | $0.11 |
| edit | 5 | 62 | 105,969 | 1,263,184 | $1.28 |
| package | 1 | 7 | 56 | 30,110 | $0.08 |
| **total** | 16 | 156 | 212,411 | 2,605,768 | **$4.08** |

Review rounds: script 3 · video 1.
Latest script quality: scores: stop 4 · laughs 4 (count 6/3) · specific 4 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 3 · fresh 4 · facts PASS
Score evidence: best payoff L8 · weakest speak L7
Latest reviewer report: swipe risk: 0–3s med · 3–15s low · middle low · payoff low · blockers 0 · polish notes 9 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 3 warnings (qa.json updated 2026-10-21 19:26)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
