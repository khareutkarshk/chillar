# Usage — 2026-11-02-decline-fee (agent runs, from notes/usage.jsonl)

Updated: 2026-11-01 23:31 local time. Agent totals exclude the interactive producer session and external services such as TTS.

| stage | runs | turns | prompt chars | cached read tokens | cost |
|---|---:|---:|---:|---:|---:|
| research | 1 | 30 | 606 | 511,912 | $0.32 |
| script | 4 | 41 | 82,109 | 724,895 | $1.46 |
| factcheck | 1 | 8 | 153 | 35,629 | $0.07 |
| voice | 2 | 5 | 374 | 20,440 | $0.14 |
| edit | 5 | 88 | 120,370 | 1,377,814 | $1.66 |
| package | 1 | 7 | 53 | 21,655 | $0.07 |
| **total** | 14 | 179 | 203,665 | 2,692,345 | **$3.72** |

Review rounds: script 2 · video 1.
Local source retrieval: 2 searches · 4 excerpts · 916 chars returned from 3,679 chars of matched sources
Latest script quality: scores: stop 4 · laughs 4 (count 7/6) · specific 4 · clarity 4 · insight 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
Score evidence: best laughs L4 "Pehle sirf aura jaata tha. (beat) Ab paise bhi?" · weakest payoff L18 "Aura ab bhi free mein jaata hai. (beat) Decline nahi." (reads slightly twisty)
Latest reviewer report: swipe risk: 0–3s low · 3–15s med · middle med · payoff low · blockers 0 · polish notes 10 · polished after this PASS (qa-guarded, not re-reviewed: look at the contact sheet)
Mechanical QA: 0 errors · 5 warnings (qa.json updated 2026-11-01 23:29)

## Producer session

Not included in the agent table. Record it with `npx ccusage@20.0.28 session`.

Producer session (ccusage@20.0.28 session total): start $1107.15 → end $1107.47 (Δ $0.32).
