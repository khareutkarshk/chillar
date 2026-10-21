verdict: PASS
round: 1
swipe risk: 0–3s med · 3–15s low · middle low · payoff low

## Prior notes
None (round 1).

## QA warnings (copied, routed)
- [director|component:hook-card] polish t=0.02 s01-hook paper spans 586px of 880 (small-object).
- [director|component:phone-note] polish t=11.62 s06-box-safar paper 826px tall, text ends at 65% (empty-paper).

## Voice
- L4 "number: check figure read in full": ASR noise (heard only "सरकार के"); captions align "₹100 sarkar ke". Not a blocker.
- L9 40% match ("Making pe alag 5% dikhe, toh poocho"): whisper heard garbage; aligner found every word at 25.94–28.4. Probably fast delivery plus ASR noise. Polish: [voice] re-listen once to L9 (phonetic: "making pe alag five percent dikhe, toh poocho"). Not a blocker.

## Notes
- [director|component:hook-card] polish t=0.02 Frame 1 hook paper is narrow (paper about 290 px in a 540 frame, wide:false). Labels wrap mid-phrase ("Dry fruit / box", "Sarkar ko / gift") and the red ₹ ---- drops to its own line. → set `wide: true` (about 860 px wide) so each row sits on one line, and shorten "Sarkar ko gift" to "Sarkar ko".
- [director] polish t=11.6–13.0 s06 Box ka safar: the total "₹100 GST: wapas nahi" is on screen while the voice says "Box ghoom ke wapas aayega" and has not yet said "Tax nahi" (12.24). The paper is also half-empty. → delay the total to about 12.3 s and cut the paper height to its content (`minHeight` or fewer rows).
- [editor] polish t=21.4 s09c Chillar bubble "Aura: gaya" appears at 21.42, before the spoken "gaya" (21.7). It gives the punchline away early. → start the mascot at 21.65.
- [director] polish t=7.6–10.4 s05 ₹100 is a bare number with no paper object, and the content zone below it (y 950–1150) is empty. → put the number on a torn slip or move dy down about 80 px. Optional.
- [director] polish t=28.4–30.7 s12 Expectation/Reality: no real meme image or sound. The reel has zero real memes, so the reaction beat leans on Chillar only. If a fresh global meme fits "receipt thrown out with the wrapper", swap one in; otherwise leave.
- [editor] polish t=30.4 caption "wrapper ke saath phenk" wraps to two lines and the last word is highlighted late. → keep it on one line, or split the captions after "wrapper ke".
- [editor] polish t=0.0 No caption is visible on frame 1 (the first-word fade-in). → make sure "Is Diwali sarkar ko" is drawn at t=0.

Sound: sfx_dropped is all rank 1–3 foley that lost the 2 s thinning to nearby stamps or the printer. This is acceptable and the main beats keep their sound.
