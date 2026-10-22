verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s low · middle med · payoff med

## Prior notes
None (round 1).

## qa warnings (no errors; routes copied from qa.json)
- caption-band t=0.02 hook-card "Report"/"12 Nov" in y 1164–1263 → [director] lift hook stakes card (dy 110 → ~0 or smaller size) so it ends above y 1150.
- top-heavy t=3.01 s02-roll → [director|component:odometer-number] dy -120 → ~+60.
- top-heavy t=13.12 s06-receipt → [director|component:receipt-list] dy 0 → ~200.
- early-number t=21.53 s10-food "₹3,600" 1.2 s before voice → [editor] reveal pinned total on its word.
- early-number t=44.23 s19-calc "₹16,164" 1.5 s before voice → [editor] show result on "saal ke".
- empty-paper / late-text t=30.58 s13-gang → [director|component:phone-note] see note below.
- empty-paper t=48.55 s21-sms, t=52.42 s23-optout, t=57.96 s25-closed → [director|component:chat-screen/checklist].
- short-shot t=50.46 o22-crying 0.96 s → [editor] hold to ≥1.0 s.

## Notes
- [editor] polish t=29.4–32.7 s13-gang: frame 30.58 shows only "Cafe, Cab" on a half-empty card while the caption already says "UPI pe bhai mera". Items trail the voice by ~1.5 s, and the "Saat log, ek main" button line lands after the laugh. → stagger 0.45 → 0.25, first item printed on the cut, and shrink the paper to its content (or use fewer rows).
- [editor] polish t=56.8–59.8 s25-closed (payoff): frame 57.96 shows the X on "Salary mili" and "Chor mile" while the voice is on "Salary nahi mili", with the paper half empty. "Chor mile / Chaabi wapas" tick in after the words. → stagger 0.8 → 0.5 so ticks land on "chor mil gaye" and "chaabi wapas meri". The strongest visual is also just a checklist: add the smug/shrug Chillar on the last tick.
- [director] polish t=11.9–15.0 s06-receipt: the receipt is nearly empty at 12 s (only the header), with its single line arriving at ~2 s, so the first 2 s have nothing to read over "Sabse aage rent". → print the "Rent, maid, wifi" line on the cut (at 0.2).
- [director] polish t=17.7–21.5, t=36.5–40.6: the same SALARY KAHAN GAYI receipt appears three times (plus the chat/slip shots). It is a cumulative tally, so it works as a callback, but give the third receipt a different entrance, e.g. a zoom into the total, since the first two are similar.
- [director] polish t=47.5–50.5 s21-sms (the RBI joke): the card is half empty and small (~416 px) for the reel's turn ("Khatkhataya tha!"). → bigger paper or add a "24 ghante pehle" mark-up at full width.
- [director] polish t=44.2 s19-calc: the stamp "₹16,164 saal ka" appears at 47.8 after the calc, while the voice said it at ~46.4. Keep the stamp (budget is 2, ok), but align it to "saal ke".
- Memes: only a FAAAH sound at 5.8 s, which fits the "bada chor" beat and is a global meme. The sheet shows no image memes, which is fine. Say so if it has been leaned on in recent reels.
- Numbers checked: 14,000+6,200+3,600+3,200+4,100+1,800+1,347 = 34,247, and 40,000 − 34,247 = 5,753 ✓. 1,347×12 = 16,164 ✓. "Chhote wale" 14,047 = the five small items ✓. Indian grouping OK. The hook says "Salary: last seen 1 Nov" with "mann lo ₹40,000", which is framed as hypothetical, so the 40,000 is not misleading.
- Voice: 0 flags, no [voice] notes. Normal ASR noise on L2 (67%) and L18 (67%).
- Outro is complete: MDR line, Follow, disclaimer. Last payoff frame (59.8) is clean. Frame 60.0 shows an empty receipt as the outro tears in, which is fine because it is 0.2 s.
- sfx_dropped: the ding at 3.89 lost to the FAAAH meme (which is later at 5.86); the odometer lands silent, so a [editor] polish: move the ding to the roll's end (~4.5 s) if budget allows.
