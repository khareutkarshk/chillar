# Usage — 2026-10-26-report-mdr-payer (agent runs, from notes/usage.jsonl)

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 53 | 212 | 1,086,329 | $0.51 |
| script | 4 | 29 | 70,865 | 372,567 | $1.27 |
| factcheck | 1 | 13 | 158 | 191,642 | $0.16 |
| voice | 2 | 12 | 384 | 68,100 | $0.12 |
| edit | 10 | 119 | 204,966 | 2,011,260 | $2.36 |
| fix | 3 | 8 | 41,804 | 65,060 | $0.22 |
| package | 1 | 4 | 58 | 38,602 | $0.07 |
| **total** | 22 | 238 | 318,447 | 3,833,560 | **$4.72** |

Review rounds: script 2 · video 3.
Local source retrieval: 9 searches · 28 excerpts · 6,120 chars returned from 34,372 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 6/6) · specific 4 · clarity 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
Latest video quality: swipe risk: 0–3s low · 3–15s med · middle med · payoff low · blockers 3 · polish notes 4
Final mechanical QA: 0 errors · 6 warnings
Producer session (the main Claude Code session) is not included — note it from `npx ccusage@latest session`.

## Producer session (ccusage)

ccusage all-sessions total: $717.66 at start → $718.88 at end (+$1.22, 2026-10-20). Post-deliver producer fixes: Sunny re-take via pronunciations.tsv, realign, 4 surgical scenes.json timing edits, delivery re-render.
