verdict: REVISE
round: 1
swipe risk: 0–3s low · 3–15s med · middle med · payoff low

## Prior notes
None (round 1).

## qa warnings (copied)
- top-heavy t=8.7 s06-chacha-parcel (receipt-list) → route director|component:receipt-list, "dy": 280 or taller paper.
- empty-paper t=14.46 s08-forty-guests (receipt-list) → route director|component:receipt-list, size paper to printed rows.

## Notes
- [voice-resolved] L7 (resolved 2026-10-21 by producer: re-voiced पाञ्च; whisper on 17.6–21.5 s hears "पांच दिन अगर सब रोज आये तो बीस हजार" — flag was a stale-timing window) t=17.7–20.3: whisper heard "पाँच" as "रूपे" (and ₹20,000 as "बीस हज़ार रूपे रूपे…"), so "paanch din" is lost. → Add a pronunciations.tsv row spelling it with a nasal "पान्च दिन", and re-voice L7. Optionally respell ₹20,000 as "बीस हज़ार".
- [director] blocker t=17.9–18.4 s11: the odometer shows "₹4,000" under the label "5 din, agar sab roz aaye" (the sheet frame at 18.0 shows exactly this). Read alone, that says 5 days costs ₹4,000, which is false. → Start the roll sooner (rollStart 0.1) or start `from` at 20,000. Alternatively change the label to "Ek din ₹4,000 × 5" until it lands.
- [director] polish t=7.5–10.3 s06 chacha receipt: for about 2.5 s only the header "CHACHA KA ORDER" is on screen. The items are blank, and the middle of the screen is empty (frame 8.7). The punchline "parcel ₹100" has no visual until after it is spoken. → "step": 0.25, so "nahi / nahi" print on "kuch nahi khate". Set "dy": 280. Land the ₹100 row and the total on "parcel" (~10.26).
- [director] polish t=14.46 s08: half-empty paper (qa). The "…" row plus a double rule leaves dead space, and the ₹4,000 total is covered or duplicated by the stamp. → Drop the "…" row. Add a "Guest 2" row, or reduce minHeight. Move the stamp lower so it doesn't repeat the circled total.
- [director] polish t=11.3 s08a: the odometer label "Maan lo" repeats the caption "Maan lo" directly below it. The number reads "1 guest" at 12.0, before "40" is spoken. → label "Roz ke guest"; start `from` at 40 or roll earlier.
- [director] polish t=17.7–21.4: the ₹20,000 odometer and the ₹20,000 stamp show at the same time (frame 21.0), and s14 says it a third time. The same number appears 3 times in 4 s. → Remove the s12 stamp, or make s11 say "5 din" and let the stamp carry the number.
- [director] polish: s03/s10 glyph characters and s07 were not in the contact-sheet frames, so I did not check them. s16's two-panel at 28.7 stacks well. The chapters use only 1 meme, which is fine.
- [editor] polish: sfx_dropped has "ding" at 12.55 (s08a) and "printer" at 13.26. The 40-ding joke has no ding sound. → Move s07's ding to ~12.5, where "40 guest, 40 ding" plays, if the 2 s thinning allows it.
- [director] polish: the s02/s04 hook-adjacent shots and the callback are fine. The payoff (s15 receipt → s16 two-panel) is clean, and the outro is complete with the disclaimer.
