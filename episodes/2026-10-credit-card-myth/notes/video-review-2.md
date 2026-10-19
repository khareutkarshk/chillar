verdict: REVISE
round: 2
swipe risk: 0–3s med · 3–15s med · middle med · payoff med

## Prior notes (round 1)
- top-heavy / empty bottom 35%: still open (sheet 0–33 s, frames t=9.5, 11.0, 27.6, 32.8 — everything sits above the caption, below it is empty).
- statement used 3× / hook-neelami-galat look alike: still open (hook t=0 is now a headline plus a small "Agla stop / Neelami" slip, which is better. Neelami t=3.9 is now a calendar page, which is fixed. Outpass t=22 and fineprint t=24 still read as near-identical headline + strip).
- outpass mascot clipping body line: still open at t=24 (coin sits right under "(warden)", the body wraps to 4 lines in a narrow box).
- hook stakes: mostly fixed (the "karza" headline reads in 1 s). The slip is small, ~560 px wide (hook box 59–946 per qa, but the slip is tiny in the frame at t=0).
- dinner receipt dead space: still open (t=11.0 has only "Biryani x 6" printed on a tall empty receipt while the voice says "Hostel dinner,").
- paid ₹1,000 / CA samjha: partly fixed (facepalm coin is bigger) but the sheet at t=15 shows the number clipped by the coin ("₹1,00"). Still open.
- bar-chart tiny labels: still open at t=30 (labels "Poora bill" / "Adhoora bill" / caption ~9–10 px in the frame, bar "0" is only a line).
- zero odometer: still open. t=27.6 shows ₹0 already, before the word "zero" (27.94), so the punchline number is given away early. The "FULL BILL" stamp is not on screen yet at 27.6, and the frame is mostly empty field.
- beta reveal timing: partly fixed (the card is up by 32.8 with "beta" on screen at the spoken word), but see the new note about the coin covering the text.
- mascot variety: improved (different x/y/size per beat).
- izzat two-panel: fixed (t=9.5 shows both panels stacked, smug and crying, readable).

## QA errors (.cache/qa.json)
- 0 errors, 0 warnings, audio -14.0 LUFS / -1.0 dBTP. Nothing to route.

## Notes
- [director] t=32.0–33.1 (beta): the smug coin (x680, size 440) covers the right half of "Sahi version" (frame t=32.8 reads "Sahi versi"), and the strike line runs across "Card = karza". This is the final punchline, and the key text is hidden. → Move the smug mascot to x≈800, y≈1150, size ≈ 320, below the card. Or shorten the right title to "Sahi" so nothing is clipped.
- [director] t=26.42–27.94 (zero): ₹0 is on screen at t=27.6, before the voice says "zero" (27.94), and the field below it is empty. → Start the roll later (rollStart ≈ 1.3, from the stressed "tak:"), so ₹180 is still showing until "interest". Land ₹0 + the FULL BILL stamp on the "zero" word. Enlarge the ₹ number and drop it toward the caption band, so the lower half isn't empty.
- [director] t=10.04–13.1 (dinner receipt): at t=11.0 the receipt is a tall empty paper with one line, while the voice is on "Hostel dinner,". The ₹10,000 only appears at ~12.4. → Set step to ≈0.15 so all 3 items print by 11.0. Crop the receipt height to its content, and drop it lower (centre y≈700) so it sits nearer the caption.
- [director] whole video (t=9.5, 11.0, 27.6, 32.8): every shot is an object in the top 55% of the frame. Caption at y≈1300 and the wordmark follow, then 25% of the frame is empty dark field. It feels like the same template repeated. → Re-position objects with y params ≈ +150–250 px. Overlap two papers on one shot (e.g. the statement with the outpass slip). Let the mascot sit on a paper's edge instead of floating.
- [director] t=22.0 and 24.14 (outpass, fineprint): two headline-plus-strip shots in a row with the same layout (left headline, small paper strip, tiny coin). The outpass body wraps to four lines and the coin touches "(warden)". → Make outpass a real hostel slip, a wide paper (≈860 px) with a red "CANCEL" stamp. Make fineprint a cashback ad scrap, with the fine-print line in readable 30 px+ text instead of the unseen `sub`.
- [component:bar-chart] t=28.7 (adhoora): labels and caption are ~10 px in the frame (≈20 px in the reel), and the ₹0 bar is a hairline. → Raise the label and caption font to ≥ 30 px in the reel and give the Poora bill bar a visible ₹0 chip. Centre-left align the chart so it spans ~860 px.
- [editor] t=13.14–14.9 (paid): the coin overlaps "₹1,000" (the sheet at t=15 shows "₹1,00" cut off by the coin's head). → Shift the facepalm mascot x from 640 to ≈ 760 and y lower (≈1150), or shrink the number size to 150.
- [director] t=0–3.9 (hook): the "Agla stop / Neelami" slip is small (≈ 200 px in the frame) and the lower 50% of the frame is empty at t=0, so the stakes are just the headline. → Enlarge the slip to full content width (≈ 860 px) and tilt it, with the mascot overlapping its corner.

## Checked OK
- Night theme is consistent; fields change on chapter cuts (10.04, 26.42, 33.11). No structure labels or eyebrow pills on the frames pulled. Mono only inside printouts. Outro is complete (MDR line, follow, disclaimer). Indian grouping is correct (₹10,000, ₹1,000, ₹9,000).
- The izzat two-panel now lands the joke.
