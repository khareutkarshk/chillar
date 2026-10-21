# Usage — 2026-11-07-guests-kharcha (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 18:04 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 13 | 181 | 215,215 | $0.20 |
| script | 4 | 26 | 69,511 | 440,671 | $1.26 |
| factcheck | 1 | 5 | 156 | 71,250 | $0.07 |
| voice | 2 | 14 | 380 | 120,241 | $0.11 |
| edit | 10 | 88 | 149,384 | 1,322,812 | $1.82 |
| package | 1 | 5 | 56 | 57,386 | $0.09 |
| **total** | 19 | 151 | 219,668 | 2,227,575 | **$3.55** |

Review rounds: script 2 · video 2.
Latest script quality: scores: stop 3 · laughs 4 (count 4/3) · specific 4 · clarity 4 · insight 4 · escalation 4 · payoff 5 · speak 4 · fresh 3 · facts PASS
Score evidence: best payoff L10 · weakest stop L1
Latest reviewer report: swipe risk: 0–3s low · 3–15s low · middle med · payoff low · blockers 1 · polish notes 0 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 1 warnings (qa.json updated 2026-10-21 18:03)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
