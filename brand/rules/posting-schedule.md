# Posting schedule — one Reel every day

One timetable for the week: what goes out each day, when it's made, and when it's posted.
Post time: **7:30 PM IST** every day (Sunday 11:00 AM). After 3 weeks, check Instagram Insights →
"Most active times" for @chillar.ind and move the slot to where the followers actually are.

## The week
| day | series | format | theme (default) | made | posted |
|---|---|---|---|---|---|
| **Mon** | Chillar Report — the week's money news | 60 s | calm | Mon 9 AM–2 PM (news must be fresh) | Mon 7:30 PM |
| **Tue** | Chillar in 60 — one concept | 60 s | pastel | Mon 3–7 PM | Tue 7:30 PM |
| **Wed** | Myth vs Math — one debunk | 30 s | night | Tue | Wed 7:30 PM |
| **Thu** | ₹100 vs ₹1,00,000 — escalation | 60 s | pastel | Wed | Thu 7:30 PM |
| **Fri** | Chillar in 60 — quick concept | 30 s | pastel / calm | Thu | Fri 7:30 PM |
| **Sat** | Myth vs Math — deep dive | 90 s | night | Fri | Sat 7:30 PM |
| **Sun** | ₹100 vs ₹1,00,000 — weekend spending | 30 s | pastel | Sat | Sun 11:00 AM |

Per week: 3 × 30 s · 3 × 60 s · 1 × 90 s. The theme column is a default — the director still picks
by the script's mood (CLAUDE.md §1).

## A production day (one reel, made the day before it posts)
| time | step |
|---|---|
| 9:00 | fresh session → `/make-reel <topic> <format>`: library facts + research, cover, writers' room |
| 11:30 | fact-check → `/compact` → voiceover (Sunny, automatic) |
| 12:30 | director → editor → qa → draft render → video review (≤ 3 rounds) |
| 16:00 | delivery render, `igcheck` "upload-safe", look at the contact sheet yourself |
| 17:00 | `/package` → post.md; on the laptop, schedule it in Meta Business Suite: upload `output/final.mp4` as-is + `output/cover.jpg` as the cover, caption from post.md, no app music/filters/trim. Phone posting only with the original file (cable/cloud, never WhatsApp) and "Upload at highest quality" on |
| 17:15 | `notes/usage.md` (ccusage) |

Monday is the exception: the Report is made and posted the same day, and Tuesday's reel is made
Monday afternoon.

## Weekly rhythm
- **Sunday, 30 min:** pick the 7 topics for next week from the backlog below (one concept per reel,
  no repeats within 4 weeks); run `pipeline/facts_library.py stale` and re-verify anything stale
  before the week starts.
- **Every day, 10 min after posting:** reply to comments for the first hour; note topic requests in
  the backlog.
- **Saturday:** `npx ccusage@latest daily` for the week — cost per reel should trend down.
- **Buffer:** keep 2 finished reels in `episodes/` that aren't date-bound (concepts, myths). If a day's
  reel fails review after 3 rounds, post a buffer reel and finish the other one tomorrow.
- **Around 1 Feb (Union Budget):** the Monday Report covers it; every `budget` entry in the facts
  library is stale until re-verified — no tax reel ships before that.

## Topic backlog (starter — education only, no products, no return promises)
- **Chillar in 60:** CTC vs in-hand ✓ (shipped) · old vs new tax regime · what TDS actually is ·
  how a credit score moves · EMI = principal + interest · why the PF interest rate matters · gratuity in
  2 lines · HRA in plain words · inflation eats savings · how UPI is free.
- **Myth vs Math:** "12 lakh pe tax lagta hai" · "PF is locked forever" · "credit card = debt trap
  always" · "renting is throwing money away" · "FD is risk-free" · "salary hike = richer".
- **₹100 vs ₹1,00,000:** ₹100/day chai over 10 years · ₹500 vs ₹50,000 late fee · min due vs full
  bill · ₹1,000 SIP habit vs one ₹1,00,000 purchase (illustrative maths, cite facts for any rate).
- **Chillar Report:** RBI policy, EPFO and tax notifications, new UPI/NPCI rules, budget — whatever
  happened that week, from primary sources.

Daily posting is real now, so the outro sign-off can promise it ("Agla receipt kal.").
