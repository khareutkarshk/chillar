# Usage — 2026-11-01-gold-kabhi-girta (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 16:10 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 27 | 226 | 497,468 | $0.41 |
| script | 4 | 41 | 78,639 | 878,719 | $2.35 |
| factcheck | 1 | 9 | 158 | 104,430 | $0.10 |
| voice | 1 | 7 | 60 | 45,701 | $0.09 |
| edit | 5 | 76 | 122,386 | 1,632,398 | $1.88 |
| package | 1 | 7 | 58 | 30,580 | $0.09 |
| **total** | 13 | 167 | 201,527 | 3,189,296 | **$4.92** |

Review rounds: script 2 · video 1.
Latest script quality: scores: stop 4 · laughs 4 (count 9/9) · specific 4 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 3 · fresh 3 · facts PASS
Score evidence: best laughs L16 · weakest fresh L11
Latest reviewer report: swipe risk: 0–3s low · 3–15s low · middle med (slips, odometers and charts run in a row, 16–45 s) · payoff low · blockers 0 · polish notes 6 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 3 warnings (qa.json updated 2026-10-21 16:08)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
