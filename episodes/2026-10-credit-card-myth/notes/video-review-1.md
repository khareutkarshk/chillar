verdict: REVISE
round: 1
swipe risk: 0–3s med · 3–15s med · middle med · payoff low

## Prior notes
- none (round 1)

## QA errors (.cache/qa.json)
- 0 errors, 0 warnings, audio -14.0 LUFS / -1.2 dBTP. Nothing to route.

## Notes
- [director] whole video: every shot is the same shape, a card or receipt in the top half and the caption at y≈1300. The bottom 35% of the frame (below the caption, around the wordmark) is empty dark field in all frames pulled (t=11.5, 21, 31.5). It looks top-heavy and template-like. → Vary composition. Drop some objects lower or larger, tilt or overlap two papers, and put a scene's object nearer the caption band. Use the `size` and position params.
- [director] t=3.88, 22.0, 24.14 (neelami / outpass / fineprint) use the `statement` component three times, and the first two are visually near-identical paper strips. Hook, neelami and the galat split card also read as one component repeated. → Swap at least two for different objects. Neelami could be a "ghar ki neelami" notice slip with a red pen mark. Outpass could be a hostel outpass slip with a stamped CANCEL. Fineprint could be a cashback ad scrap with a magnifier on a tiny footnote line.
- [component:statement] t=24.0 (outpass): the mascot overlaps the end of the body line ("Sign: Card (warden)" is clipped by the coin's head), and the line also runs to the card edge. → Move the mascot to the lower-right empty space, or shorten the body to "Free period: CANCEL." and put "Sign: Card (warden)" on a second line.
- [director] t=0–3.9 hook: the receipt reads "Naya card — aa gaya / Papa ka chit — Card = karza". "aa gaya" is a non-amount and "chit" is a small mono line, so the stakes don't read at a glance. → Make the stakes one big objectified line, e.g. a big "Card = karza?" slip with Papa's ballpoint scrawl. Cut the two-row receipt. Frame 1 should show the fear (neelami / karza), not a label list.
- [director] t=10.04–12.4 (dinner receipt): the receipt is nearly empty at t=11.5, with only the title and a dashed line and no items printed while the voice says "Hostel dinner, mere card pe:". The big paper has dead space for 2+ s. → Print the lines faster (step 0.55 → ~0.3), or shrink the receipt height to its content. Land the ₹10,000 total with a red stamp-style circle on the "pe:" beat.
- [editor] t=13.14–15.66 (paid ₹1,000): "Bhar diya. Sorted." is small and left-aligned above a big number. The "CA samjha" joke lands on a mascot with a magnifier that is only 300 px and tucked under the number. → Enlarge the mascot reaction (facepalm/smug) and give it the right-hand space. Hold it a beat after "samjha." instead of cutting to the statement at 15.66.
- [component:bar-chart] t=28.7 (adhoora): the bar chart's caption "Pehla mahina · illustration: 2%/mahina" and the labels "Poora bill / Adhoora bill" are tiny (~9 px at 540 wide, i.e. ~18 px in the reel). The "0" bar is a bare line, so the comparison is unclear. A yellow slab with "180" circled reads weakly. → Bump labels and caption to ≥ 30 px reel size. Make the zero bar visibly labelled "₹0". Put "₹180" on the bar, not just "180".
- [director] t=26.42 (zero): the odometer shows ₹180 big while the voice says "interest zero". The roll to ₹0 starts at 0.55 s and ends ~27.9, so the frame at 27.0 shows a stale number against the payoff word. → Start the roll at the stressed "tak:" beat. At t=27.9 show ₹0 with the stamp, with no lingering ₹180.
- [director] t=31–33 (beta): "Papa sahi the." The split shows Papa's "Card = karza" first (t=31.5), and the "Sahi version: Beta = karza" card pops in late. The punchline "beta" (32.76) lands only after the reveal, so the joke is somewhat telegraphed by the written card before the word. → Time revealAt to the spoken "beta" (≈32.5) so the card appears on the word. Then hold ~0.5 s for the smug coin before the outro cut.
- [editor] overall: the mascot appears at only ~5 moments and in 300 px at the same x=780,y=1110 each time. The one transition (zoom@24.14) is fine. Retention is ok on beats (36 visual beats), but the 3–15 s stretch is mostly flat cream cards on a dark green field. → Vary mascot x/y and size per beat. Add one big move (a punch or a toss-in from off-screen) on the izzat two-panel at 8.08, where the smug→crying contrast should be the laugh.
- [director] t=8.08 (izzat two-panel): the panel is a short strip at the top (y 255–667 box) with the mascot icon small inside a dark tile. The "smug → crying" joke is not readable, because only the first panel shows at t=8.5. → Show both panels stacked and large, with the crying coin at full size on the "paise nahi" beat (9.4).

## Checked OK
- Outro at 34.5/35.9: complete (MDR line, Follow @chillar.ind, disclaimer), bone→dark field.
- Theme night consistent; fields change on chapter cuts (10.04, 26.42, 33.11). Off-palette ≤ 0.28 %.
- No structure labels, no eyebrow pills. Mono text appears only inside printouts.
