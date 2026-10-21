# Usage — 2026-11-10-card-bill-coming (agent runs, from notes/usage.jsonl)

Updated: 2026-10-21 20:02 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 11 | 221 | 188,254 | $0.18 |
| script | 4 | 35 | 86,184 | 658,394 | $1.97 |
| factcheck | 1 | 10 | 158 | 139,047 | $0.13 |
| voice | 2 | 12 | 384 | 71,826 | $0.13 |
| edit | 6 | 68 | 156,015 | 1,361,124 | $1.47 |
| package | 1 | 5 | 58 | 74,713 | $0.11 |
| **total** | 15 | 141 | 243,020 | 2,493,358 | **$3.99** |

Review rounds: script 2 · video 1.
Local source retrieval: 2 searches · 6 excerpts · 1,302 chars returned from 75,406 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 7/6) · specific 4 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 4 · fresh 3 · facts PASS
Score evidence: best payoff L19 · weakest fresh L16
Latest reviewer report: swipe risk: 0–3s low · 3–15s med · middle med · payoff low · blockers 0 · polish notes 5 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 6 warnings (qa.json updated 2026-10-21 19:58)

## Producer session

Not included in the agent table. Record it with `npx ccusage@latest session`.
