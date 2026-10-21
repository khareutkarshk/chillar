verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s med · middle med · payoff low

## Prior notes
None (round 1).

## qa (0 errors, 9 warnings — copied with routes)
- short-shot t=3.02 sms-muted 2.26s<2.6 [editor]; t=5.28 maam 1.54s<1.8 [editor]; t=19.66 cart 1.72s<1.8 [editor]; t=21.38 meme-baskaro 1.42s<1.5 [editor]
- empty-paper t=13.07 / 25.86 / 29.5 calendar-flip [director|component:calendar-flip]; t=20.52 phone-note [director|component:phone-note]; t=54.58 checklist [director|component:checklist]

Voice: only flag is L13 (75%, "number: check figure read in full"). Whisper heard "पूरा भरता तो" and missed "₹750 / ₹0". Likely ASR noise because the text is short. Not a blocker.

## Notes
- [director] polish t=19.66–21.4 "Diwali cart" phone-note: the paper is ~900 px tall, and at t=20.52 only 3 lines are printed in the top third. The rest is blank paper. The sheet at 21.0 shows the same. Fix: set the paper height to the printed rows, or drop the card to 4 big rows with larger text. Ideally, hold the shot to ≥1.8 s.
- [director] polish t=36.04–38.7 bar-chart: at 36.5 only the ₹750 bar shows. The "Poora bhara" bar is empty, with no ₹0 label, so the contrast with ₹0 isn't visible until later. The grey ₹750 label also sits low-contrast on the bone field. Fix: show an explicit "₹0" on the second bar at the spoken "₹0", and use ink for the ₹750 label.
- [director] polish t=13.07, 25.86, 29.5 calendar-flip shots are half-empty paper (qa). Three calendar-flips in a row on the same field also feel repetitive. Fix: shorten pages or enlarge the details text; swap one (e.g. 29.5) for a different object.
- [editor] polish t=3.02, 5.28, 19.66, 21.38: four shots are shorter than minDuration. Fix: extend them by ~0.1–0.3 s each. The audio anchors the cuts, so only extend into the neighbouring shot's tail.
- [editor] polish t=39.0: the Fanum meme video is 3% off-palette (expected for a meme). It is a global video with sound, so it is fine. The label "Byaaj / Mera cart" reads well and lands right after "bas dekhenge bola tha".
- Comedy: the library-fine metaphor (ma'am / issue date vs due date) is clear and gets a callback at the end ("Saari kitaabein, beta"). The payoff checklist delivers the cover promise. The outro is complete with the disclaimer.
