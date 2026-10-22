verdict: REVISE
round: 1
swipe risk: 0–3s med · 3–15s med · middle med · payoff low

## Prior notes
None (round 1).

## qa warnings (no errors; copied with routes)
- small-object t=0.02 s1-hook (594px of 880) → [director|component:hook-card]
- short-shot t=1.52 s2-calendar 1.38s < 1.6 → [editor]
- short-shot t=2.9 s3-chat 2.00s < 2.6 → [editor]
- empty-paper t=3.9 s3-chat, text ends at 66% → [director|component:chat-screen]
- small-object t=3.9 s3-chat 630px → [director|component:chat-screen]
- short-shot t=4.06 s3-sideeye 0.84s < 1.0 → [editor]
Voice: 0 flagged, all 100% — OK. sfx_dropped: outro coin only (printer wins) — fine.

## Notes
- [director|component:passbook-page] blocker t=6.74–10.27 Passbook rows read "Din 31Late r…": the date column runs into the particulars, with no gap, and "Late reply" is cut to "r…" (frames 7.6 and 10.1). It reads as a rendering bug, and it is the payoff object. → Shorten the row text to "Late" or "Jurmana". Give the date column a fixed width (e.g. "D31"), or set size lower than 44. The component must not ellipsize rows that fit when the date is shortened.
- [director|component:chat-screen] blocker t=2.9–4.9 The chat joke never lands. The third message, "Day 30. *Update?*", which is the highlighted beat, is never visible. At 3.0 (contact sheet) the card is empty, and at 3.9 only 2 of 3 messages show, with the bottom third of the card blank. The shot is 2.0s, but stagger 0.45 plus entrance eats it. The "bhool jaoge" punchline (3.5–4.0) plays over an unfinished chat. → Cut the chat to 2 messages ("Report mein galti hai" / "Ticket raised 🙂") and set stagger ≤ 0.25 so both are in by ~3.2. Or hold the shot to ≥ 2.6s. Set width 860 and grow:true so the paper hugs its content.
- [director] polish t=2.9–4.9 The chat card is pinned left (x 20–340) with a large empty area to its right and below, and the mascot at 4.06 is a brief 0.84s flash. → Centre the card on the content edge at width 860. Hold the side-eye 1.0s+ and land it on "jaoge" (t≈4.0), or drop it.
- [director|component:hook-card] polish t=0.02 Frame 1 shows the stake (Day 1 → Day 30) but the slip is only ~600px wide and sits mid-frame, so the top third is empty. → wide:true / bigger size so the slip spans ~860px; keep the circle on Day 30.
- [editor] polish t=1.52 The calendar (1.38s) shows only "DAY 1 / Complaint: pending". The flip to DAY 30 is never seen, so the "tees din" idea is lost. → Hold the calendar to 1.6s+ and use the pages ["DAY 1","DAY 30"] with flip ≤ 0.1, so DAY 30 lands on "tees". Free the time by trimming s3-chat's tail.
- [director] polish t=4.9–6.74 The s4-rule receipt has a black printer slot bar on top, but only "Din 1-30 / Company ka time" are visible at 5.5. The key row "Din 31 se ₹100/din" (at 1.12) arrives only at ~6.0. The money line is not on screen when "tees din ke baad" is spoken. → Set items[1].at ≈ 0.5 so "₹100 / din" shows by ~5.4.
- [director] polish t=7.18 The stamp "₹100 ROZ" and the passbook are two stacked objects, which is good. The stamp sits dead-centre and covers the rows that print next (the 2nd–4th rows build underneath it). → Move the stamp to the right/low (x≈560,y≈1050) so the passbook rows stay readable.

Composition summary: 5 shots, 5 different objects (slip, calendar, chat, receipt, passbook), so it is varied rather than templated. The weak points are the truncated passbook text and the unfinished chat beat. Everything else is on-brand: calm theme, no eyebrow labels, outro complete with disclaimer.
