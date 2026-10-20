# Usage — 2026-10-27-diwali-bonus-tax (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 03:48 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 33 | 524 | 682,843 | $0.45 |
| script | 4 | 32 | 66,526 | 452,936 | $1.28 |
| factcheck | 1 | 8 | 158 | 70,063 | $0.09 |
| voice | 1 | 8 | 60 | 69,988 | $0.07 |
| edit | 9 | 103 | 170,697 | 2,059,265 | $2.29 |
| package | 4 | 28 | 232 | 171,988 | $0.29 |
| components | 3 | 93 | 991 | 1,217,621 | $0.68 |
| **total** | 23 | 305 | 239,188 | 4,724,704 | **$5.15** |

Review rounds: script 2 · video 2.
Latest script quality: scores: stop 4 · laughs 4 (count 7/6) · specific 4 · clarity 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
Latest reviewer report: swipe risk: 0–3s low · 3–15s low · middle med · payoff low · blockers 0 · polish notes 7 · STALE: final.mp4 rendered after this review
Mechanical QA: 0 errors · 11 warnings (qa.json updated 2026-10-21 03:44)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.

Producer session: ccusage not recorded (start-of-session ccusage call declined; session spanned a VS Code restart).
