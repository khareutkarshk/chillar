verdict: REVISE
round: 1
swipe risk: 0–3s low · 3–15s med · middle med · payoff low

## Prior notes
None (round 1).

## qa items (copied)
- warn caption-band t=0.02 hook (hook-card) "Bill total" box y 1031–1224 → [director] see note below.
- warn top-heavy t=51.86 trust-vs-check (meme-format) content ends y 676 → [director|component:meme-format] see note below.
- qa errors: 0. Audio -14.1 LUFS / -2.1 dBTP OK.

## voice_check
1 flag: L4 40% ("मान लो" heard "बानलो"). Number heard correctly (120,000), so this is ASR noise. Polish only. No blocker.

## Notes
- [director] blocker t=9.18 and t=36.44 "Q1. Making charge?" and "Q3. HUID kya hai?" put numbered question labels on screen. This is a script-structure tell, the same family as "Step 1". There is also no Q2 anywhere, so the numbering looks like an error. → Drop the "Q1."/"Q3." prefixes. Use the headlines "*Making* charge?" and "*HUID* kya hai?".
- [director] polish t=0.02 hook: the stakes receipt wraps to 3 lines ("Sona, / 10 g / (rate)") and runs into the caption band (to y ~1300). → Shorten the labels to "Sona 10 g" and "Bill", or drop `wide` or `size`, so each row is one line and the card ends above y 1150.
- [director|component:meme-format] polish t=51.86 trust-vs-check: only panel 1 is visible, it sits top-heavy, and y 600–1100 is empty. → Set "dy": 220, or reveal both panels sooner (reveal ≤ 0.8).
- [director] polish t=18.9 meme "he tryna ignore it": the source image is covered in crying-face emojis, and our label sits on top of them. It is hard to read in 1 s, and the joke shape doesn't match "thoda kam?". → Pick another variant (pick 1 or 2), or move the label to y ~20 over the clean flames.
- [director] polish t=9–45: five marker-highlight paper cards (q1-making, uncle-quote, thoda-kam, q3-huid, huid-roll-number) look alike. → Turn uncle-quote or huid-roll-number into a statement or a chat bubble, or give it a different entrance.
- [editor] polish t=4.45: the coin SFX for viva-side-eye was dropped by the 2 s thinning. Only a minor sound is lost, so no action is needed.
- [voice] polish L4: if desired, respell "मान लो" as "maan lo" in tts.txt. It is probably fine as is.

## Checked and fine
- Numbers: 3% × 14,400 = ₹432. 3% × 1,34,400 = ₹4,032. 1,38,432 − 1,20,000 = ₹18,432. Indian grouping is correct, and the labels read correctly on their own ("₹18,432 extra", "Making pe bhi tax").
- Outro is complete with the disclaimer. The payoff receipt and stamp are clean.
- Theme (pastel) is consistent. Palette is clean. Transitions: 1 zoom and 1 whip, which is within the budget.
