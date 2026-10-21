verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s low · middle med (slips, odometers and charts run in a row, 16–45 s) · payoff low

## Prior notes
None (round 1).

## qa (0 errors, 4 warnings; all copied as polish)
- empty-paper t=4.5 mummy-chat → [director|component:chat-screen]
- top-heavy t=58.92 myth-math → [director]
- empty-paper t=63.24 chacha-chat → [director|component:chat-screen]
- empty-paper t=70.06 nobody-chacha → [director|component:meme-format]

voice_check: 28 lines, 0 flagged. The low matches (L12 67%, L14 67%) are ASR noise on numbers that were heard correctly (30,000 and 1,47,250). Not a blocker.
Numbers checked against the screen: 3,007×10 = 30,070. 1,47,250 / 30,070 ≈ 4.9. 30,070 / 20,000 = 1.5. 1,47,250 / 30,000 ≈ 4.9. All consistent. The odometer reads ₹1,31,441 mid-roll at 39 s, which is normal.

## Notes
- [director] polish t=58.92 The Myth card sits alone at the top (content ends y≈630), the middle of the screen is empty, and the Math half has not appeared yet. → Add "dy": 190 to myth-math, or bring revealAt forward to about 1.4 s so the pair is on screen sooner.
- [director] polish t=50.5 The Odyssey video meme is a dark, blurry blob (frame measured 15.67% off-palette). "Jeweller ne calculator" does not read in 1 s, so the reaction relies on the headline alone. → Use a brighter global reaction clip, or add `"wide": true` and a larger `labelSize`. Alternatively, swap it for a Chillar mascot reaction (side-eye or shocked) with a bubble.
- [director|component:meme-format] polish t=70.06 "Nobody:" shows alone for 1.2 s, with a large empty field below the card. The paper is half-empty. → Set reveal to about 0.5 s, or set "dy": 180 to centre it.
- [director|component:chat-screen] polish t=4.5 and t=63.24 The chat paper is half-empty (550 px and 364 px tall). → Size the paper to the rows, or raise the font size so the rows are bigger.
- [director] polish t=0 The hook receipt wraps "Oct 2026" onto two lines, while "Oct 2016" fits on one. At t=2.9 the caption "kitne mahine ki salary?" touches the receipt's torn edge. → Shorten the labels to "2016" and "2026", or widen the label column. Add dy of about -40 on the hook, or move the caption lower.
- [director] polish t=16–45 Five receipt, odometer or bar-chart shots run back to back (didi-slip, rbi-2016, didi-months, main-slip, didi-vs-main, gold-2026). → Swap one of the slips (probably main-slip) for a Chillar reaction or a hand-drawn object. This is optional.
