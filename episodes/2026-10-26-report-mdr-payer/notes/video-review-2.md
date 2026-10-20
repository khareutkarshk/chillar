verdict: REVISE
round: 2
swipe risk: 0–3s low · 3–15s med · middle med · payoff low

## Prior notes
- L6 voice re-take: still open (t=18.0) — voice_check still flags L6 at 33%, "merchant" not heard.
- L8 voice re-take: still open (t=23.5) — flagged at 50%.
- L13 voice re-take: still open (t=41.7) — flagged at 57%, "ninety-six" and "letter" not clean. The 96 odometer is on screen.
- tier-compare tiny text (t=13.6): still open. The frame at 14.5 shows "₹2,000 tak" and "₹2,000 se upar" small on cards. qa now lists it as a warning, not an error. I downgrade it to polish, because the caption below repeats ₹2,000 large and it reads.
- calendar / skeleton / cart small or empty paper: still open (t=6.06, 12.66, 27.36). qa still lists them as warnings. Polish.
- short shots (stamp 19.12, voice-note 20.12): still open. qa warnings. At 19.5 the stamp reads fine.
- Aura meme freshness: unverified. Polish.

## Notes
- [editor] blocker t=18.0–20.0 voice: re-take line L6 ("Bill पे address लिखा है: merchant."). Whisper heard "बिल बे अड्रेस लिखाएं", so "merchant" is missing. The Merchant stamp at 19.12 depends on the word. → re-take, or retime/rewrite the line so "merchant" is clear.
- [editor] blocker t=23.5–25.8 voice: re-take line L8 ("भाई, तुझसे मान्गा किसने?"). 50% match, "तुझसे" garbled. → re-take.
- [editor] blocker t=41.7–44.1 voice: re-take line L13 ("लगभग ninety-six percent merchant payments के लिए यह letter बना ही नहीं"). 57% match. A wrong number is a blocker. → re-take, or spell the number the way pronunciations.tsv says to.
- [component:tier-compare] polish t=13.6–16.2: the 2,000 threshold is the key number but sits in ~20 px text on small cards, and the "se upar" card is mostly empty yellow. → backlog: an amount-size option, so the number is big and the card fits it.
- [director] polish t=6.06 / 12.66 / 27.36: calendar paper is 608 px wide and mostly blank, the skeleton meme is 574 px, and the cart receipt is 69% blank. → widen the paper or fill it, and add a width param.
- [editor] polish t=19.12 / 20.12 / 51.12: extend stamp-merchant, voice-note and smug to their minDuration, or merge them.
- [director] polish t=38.13: check "Aura" against facts.md `## Culture now`. If nothing backs it, treat it as the one old-classic allowance.
