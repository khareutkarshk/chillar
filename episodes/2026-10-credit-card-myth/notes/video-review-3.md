verdict: REVISE
round: 3
swipe risk: 0–3s med · 3–15s med · middle med · payoff low

## Prior notes (round 2)
- beta coin covering "Sahi version": fixed (t=32.8: coin sits below the card, "Sahi / Beta = karza" fully readable).
- zero odometer showed ₹0 early: fixed (t=27.5 still ₹180 on "tak:", t=28.2 ₹0 + FULL BILL stamp on "zero"). New problem below: the stamp covers the sub-line.
- dinner receipt dead space: still open (t=11.0: 2 items printed on a tall paper with a big empty lower half, caption "Hostel dinner,").
- whole-video top-heavy / empty bottom: still open (t=11.0, 14.8, 24.6, 27.5, 30.0, 32.8: ~35% of the frame under the caption is empty field).
- outpass/fineprint look-alike: partly fixed (outpass is now a receipt with a BAND circle, fineprint is a paper scrap). The fineprint shot is still a left headline plus a small scrap (~300 px wide in the frame) with lots of empty field.
- paid ₹1,000 clipped by coin: fixed (t=14.8). The coin is now far from the number, but the shot is sparse: small number, empty field.
- bar-chart tiny labels: partly fixed (t=30.0 labels ~20 px in the frame, readable, ₹0 chip visible). Bar chart has a flat yellow block with no texture, but it's legible.
- hook stakes slip small: still open (sheet t=0: slip ~140 px wide in the frame, headline dominates).
- izzat: still fine.

## QA errors (.cache/qa.json)
- 0 errors, 0 warnings, audio -14.0 LUFS / -1.0 dBTP. Nothing to route.

## Notes
- [director] t=27.88–29.12 (zero): at t=28.2 the FULL BILL stamp (y 1040) lands on top of the sub-line "Poora bill, due date tak" (it is cut off at "tak"). The stamp and text overlap, and the key line is lost on the punchline. → Move the stamp to x≈520, y≈1180 (below the sub-line, next to the caption band) or drop `sub`. Keep the ₹0 on "zero".
- [director] t=24.14–26.42 (fineprint): "Cashback" has the yellow marker swipe ending before the final "k" (frame t=24.6 shows the "k" black on dark, half outside the highlight), and the scrap is small (~300 px wide in the frame) beside a big headline. → Re-time the marker so it covers the whole word (or drop it), widen the scrap to ~860 px and tilt it ~-2°, and lower it to y≈600–700 in the frame so the lower half isn't empty.
- [director] whole video (t=11.0, 14.8, 24.6, 27.5, 30.0): every object sits above the caption and the bottom 35% is dark and empty, three rounds running. → Move the object y values down ≈ +200 px in the reel on these shots. On `paid` (t=14.8), enlarge ₹1,000 to ≈ 260 px and put the facepalm coin on the number's edge. On `adhoora`, shift the chart to y≈600 centre. Overlap one second paper where it fits.
- [director] t=10.04–13.1 (dinner): at t=11.0 only 2 of 3 items are printed and the receipt is a tall empty slab. → Crop the receipt to its content, or set step to ≈0.12 so the three items are printed by 10.6, and shift it down about 150 px.
- [director] t=0–3.9 (hook): the "Agla stop / Neelami" slip is tiny (≈140 px in the frame) and the lower 50% is empty at t=0.5. The frame's stakes are only the headline. → Enlarge the slip to ≈860 px, tilt it, and let the coin sit on its corner.
- [director] t=22.0–24.14 (outpass): the receipt is only ~590 px wide (sheet t=24: ~190 px in the frame) and the mascot floats below it. → Widen it to ≈860 px and put a red stamp in place of the circled "BAND" so it reads as the beat.

## Checked OK
- Night theme is consistent; fields change on chapter cuts (10.04, 26.42, 33.11); no structure labels, pills or tracked caps seen. Mono only inside printouts. Beta payoff lands and reads at phone size. ₹ values are in Indian grouping, matching the script (₹10,000, ₹1,000, ₹9,000, ₹180).
- Outro (sheet t=35.9) shows the MDR line, follow and the disclaimer.
