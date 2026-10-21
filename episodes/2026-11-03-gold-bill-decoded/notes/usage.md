# Usage — 2026-11-03-gold-bill-decoded (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 16:36 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 23 | 168 | 364,688 | $0.27 |
| script | 5 | 39 | 93,712 | 828,613 | $1.98 |
| factcheck | 3 | 23 | 477 | 305,690 | $0.27 |
| voice | 2 | 18 | 386 | 194,635 | $0.16 |
| edit | 7 | 79 | 144,933 | 1,640,743 | $1.81 |
| package | 1 | 8 | 59 | 41,851 | $0.08 |
| **total** | 19 | 190 | 239,735 | 3,376,220 | **$4.56** |

Review rounds: script 2 · video 2.
Local source retrieval: 8 searches · 17 excerpts · 3,345 chars returned from 13,425 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 8/6) · specific 5 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 4 · fresh 3 · facts PASS
Score evidence: best specific L8 · weakest fresh L11
Latest reviewer report: swipe risk: 0–3s low · 3–15s low · middle med · payoff low · blockers 0 · polish notes 1 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 0 warnings (qa.json updated 2026-10-21 16:35)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
