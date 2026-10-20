---
description: Generate 5 cover-text + first-frame + hook-line packages, score them, recommend one
argument-hint: <episode folder or slug>
---

Package episode **$ARGUMENTS** (resolve to `episodes/<slug>` if a bare slug is given).

Read `script.md`, `facts.md`, `cover.md` and CLAUDE.md §4 (retention rules).

For a dated Chillar Report or another time-sensitive claim, resolve the planned posting date from the folder
name and recheck the primary source as of that date before writing the posting package. If the update is over
5 days old by then, recommend it as a brief item and ask for a fresher lead.

1. Write **5 distinct packages**. Each = cover text (≤ 5 words, Bricolage Grotesque, sentence case) + cover_field (chapter slot), first frame (what is
   literally on screen at t=0 — must show the stakes, using our components: hook-card, printed
   receipt-list, odometer-number…), and hook line (sentence 1 = the question, Hinglish).
   Vary the angle: mistake-framed, surprising-math, myth-busting, ₹ escalation, deadpan question.

2. **Score each 1–5** on: curiosity (would a 20-year-old stop scrolling?), clarity (understood in
   1 second, on a 3:4 grid crop), honesty (does the payoff deliver exactly this? no get-rich bait).
   Show a table. Honesty < 4 is disqualified.

3. **Recommend one** with a one-line reason. Ask before overwriting `cover.md`; if I agree, update
   `cover.md` and sentence 1 of `script.md`, then run `.venv/bin/python pipeline/cover.py episodes/<slug>`
   and show me `output/cover.png` and `output/cover_grid_preview.png`.

4. Also write `output/post.md`: Instagram caption (Hinglish, ≤ 3 short lines + CTA), 5–8 relevant
   hashtags, the line "Educational only. Not investment advice.", "Paid partnership" if
   `paid_partnership: true`, and "ai_voice: true — check Meta AI-label rules" if voice/voice.json says
   `ai_generated`. Sources: list the facts.md URLs.
