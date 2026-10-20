verdict: REVISE
round: 1
swipe risk: 0–3s low · 3–15s med · middle med (many white-receipt/chat cards in a row) · payoff low

## Prior notes
None (round 1).

## qa errors copied
- [editor] blocker audio: true peak -0.9 dBTP on final.mp4 (max −1.0) → limit at −1.5 dBTP before the AAC encode.

## voice_check
27 lines, 0 flagged. No voice re-takes needed. (sfx_dropped not read — shell blocked; editor to confirm any meme/foley sound dropped at 42.06 and 49.17.)

## Notes
- [editor] blocker t=full mix: true peak −0.9 dBTP fails the −1.0 limit → add limiter at −1.5 dBTP in mix.py, re-run mix and igcheck.
- [director] polish t=42.06–43.5 ignore-meme: the image sits left-aligned at 605 px wide (x 50–655), leaving the right half of the content zone empty and the caption faded/ghosted underneath ("daal diya."). Fix: centre it or scale it up to ≈ 860 px wide (add width param or a slight tilt toss), so it fills the zone like the other objects.
- [director] polish t=49.17 beggars-meme: the Odyssey clip is very dark and blurry; "Mera 'hey'" label is readable but the picture says nothing at a glance. Fix: swap for a brighter global reaction image/video (e.g. a cleaner "rejected/denied" template) or drop it. The meme budget (90 s ≤ 7) is fine. Also the "Rejected." headline is fine. Check that "Mera 'hey'" lands on "Rejection" (L20, 49.2) — it does.
- [director] polish t=0.5 hook: the receipt already shows "Card apply · Diwali week 4" in frame 1, which gives away the L4 setup before it is spoken. Fix: change the stake rows to show only "Score check (khud) roz" plus a "?" on the second row, or hold the "4" until the odometer rolls at ~6 s. Also the text wraps to two lines per row; shorten labels to "Score check" / "Card apply".
- [director] polish t=20.06 neend, t=30.3 otp-excited, t=59.84 hey-counts: glyph-characters span only 370–494 px (qa small-object). Fix: raise size from 320–340 to ≈ 520 or use the wide param so the glyph fills the 860 px width. Bubble text stays ≥ 36 px.
- [component:chat-screen] polish t=10.62, 32.16, 40.46, 47.42, 64.48: bubble/time/header text 26–35 px (qa small-text warnings). Fix in the component: raise body to ≥ 40 px and time/header to ≥ 36 px. On the sheet the chat cards read small inside a wide empty field at 12 s, 33 s, 42 s, 48 s.
- [director] polish t=27–45: the middle runs the same white-card-on-field shape repeatedly (receipt, chat, receipt, split, chat, receipt, chat, checklist, receipt). Fix: convert one receipt (e.g. lender-opens at 33.6, a single "HARD" row, nearly empty) into a big stat/odometer or a Chillar reaction (shocked) to vary the beat.
- [director] polish t=33.6 lender-opens: the receipt has one row and the caption "hai" is a stranded single word at 36 s. Fix: extend the caption window or merge the shot with voucher-vs-enquiry; or add a stamp "ENQUIRY +1".
- [director] polish t=63.3–69.1 mausi-callback/nazar-math: the final chat/split pair reads clearly; the payoff "Aadhi sahi" lands. No change, except add one Chillar smug reaction at the last line if the budget allows.
