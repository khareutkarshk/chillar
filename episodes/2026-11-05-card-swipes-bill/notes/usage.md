# Usage — 2026-11-05-card-swipes-bill (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 17:14 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 14 | 210 | 254,267 | $0.21 |
| script | 6 | 49 | 130,441 | 945,025 | $2.24 |
| factcheck | 1 | 11 | 158 | 165,901 | $0.12 |
| voice | 1 | 6 | 60 | 27,176 | $0.06 |
| edit | 5 | 67 | 94,812 | 1,353,206 | $1.48 |
| package | 1 | 4 | 58 | 56,844 | $0.09 |
| **total** | 15 | 151 | 225,739 | 2,802,419 | **$4.21** |

Review rounds: script 3 · video 1.
Latest script quality: scores: stop 4 · laughs 4 (count 7/6) · specific 5 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 4 · fresh 3 · facts PASS
Score evidence: best specific L8 · weakest fresh L6
Latest reviewer report: swipe risk: 0–3s low · 3–15s med · middle med · payoff low · blockers 0 · polish notes 6 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 2 warnings (qa.json updated 2026-10-21 17:12)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
