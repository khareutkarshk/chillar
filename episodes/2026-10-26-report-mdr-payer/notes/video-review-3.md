verdict: REVISE
round: 3
swipe risk: 0–3s low · 3–15s med · middle med · payoff low

## Prior notes
- L6 voice re-take: still open (t=18.0). voice_check flags it at 33% and "merchant" is not heard. The Merchant stamp at 19.12 depends on that word.
- L8 voice re-take: still open (t=23.5). Flagged at 50%.
- L13 voice re-take: still open (t=41.7). Flagged at 57%. "ninety-six" is not heard cleanly, so the 96 on screen is unconfirmed by the voice.
- tier-compare tiny text (t=13.6): still open as polish. qa warns about ~20 px text. The caption repeats ₹2,000 large.
- calendar / skeleton small or empty paper (t=6.06, 12.66): still open as polish. qa warnings.
- short shots: now voice-note (20.32, 2.28 s against 2.6 s) and bhai-crown (22.6, 0.92 s against 1.2 s). Still open as polish. The stamp-merchant shot no longer appears in qa.
- Aura meme freshness: unverified, polish.

## qa errors
- None. qa reports 0 errors and 7 warnings, all copied above.
- Audio is −14.0 LUFS and −1.5 dBTP, which is fine.
- Palette: the 12.0 s and 39.0 s frames are flagged at about 1% off-palette. This is the meme photos, so it is acceptable.

## Notes
- [editor] blocker t=18.0–20.0 voice: re-take line L6 ("Bill पे address लिखा है: merchant."). Whisper heard "बिल बे अड्रेस लिखाएं" at 33%. This is the third round it has failed. → re-take it with "merchant" spelled phonetically ("मर्चेंट") in tts.txt, or add it to pronunciations.tsv. If it still fails, rewrite the line so the stamp word is clear.
- [editor] blocker t=23.5–25.8 voice: re-take line L8 ("भाई, तुझसे मान्गा किसने?"). Whisper heard "तुट से" at 50%. → re-take it, or rewrite it to "भाई, किसने माँगा?".
- [editor] blocker t=41.7–44.1 voice: re-take line L13. Whisper heard "तबक्भग 96% मुर्षिन … लेटर बनाई ने" at 57%. The 96 odometer is on screen. A number that is not clearly spoken, or a wrong one, is a blocker. → write "छियानवे percent" in tts.txt, and use "merchant" phonetically as in L6. Re-take it.
- [component:tier-compare] polish t=13.6: the ₹2,000 amounts are about 20 px and the "se upar" card is mostly empty. → backlog: an amount-size option.
- [director] polish t=6.06 / 12.66: the calendar paper is 608 px wide and mostly blank, and the skeleton meme is 574 px wide. → add a width param, or fill the paper.
- [editor] polish t=20.32 / 22.6: hold voice-note to 2.6 s and bhai-crown to 1.2 s, or merge them.
- [director] polish t=38.13: check "Aura" against facts.md `## Culture now`. If nothing backs it, treat it as the one old-classic allowance.
