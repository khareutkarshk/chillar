verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s med · middle med · payoff low

## Prior notes
None (round 1).

## qa warnings (no errors)
- [director|component:calendar-flip] polish t=11.85 s05-date paper half-empty (352px, text ends at 60%) → shrink the paper or add a second row/bigger year.
- [director|component:chat-screen] polish t=18.06 s07-chat half-empty paper (55%) → grow the paper per message, or raise the text size.
- [director] polish t=32.88 s12-calc 18 words in 2.6 s → cut the calculator's extra labels to ≤14 words, or hold it ≥3 s.
- [editor] polish t=32.91 s12-calc "₹100" shows 1.2 s before the voice says it (L12 at 34.0) → reveal the result on "₹100" (tapStart later or result at ~1.1 s).
- [director|component:checklist] polish t=42.3 s14-who half-empty paper (65%) → grow the paper per row.

## Voice
- L3 "hoga" heard as "hit ho gaya" (89%) is ASR noise on a fast line, not a missing word. No blocker. Optional [voice] polish: re-take L3 if it sounds rushed.
- sfx_dropped: coin@9.45 (s04b-smug), typing@16.91 (s07-chat), coin@52.7 → none is a meme or foley joke. No action.

## Notes
- [director] polish t=0.5 Frame 1 reads as a universal rule: "CARD SWIPE · DECLINED · Decline fee ₹25". The voice and caption say "ek bank … lega?". → change the receipt meta to "Ek bank, kuch accounts" (or title "EK BANK · CARD SWIPE"), so a paused frame doesn't claim every bank does it.
- [director] polish t=0–52 Composition is repetitive. receipt-list appears 4× (s01, s06, s10, s17), always a top-third paper with the same layout, and glyph-character 3× (s03, s11b, s15). → Make one receipt full-bleed or low and off-centre (s10-atm: width 860, dy ~400). Turn s15 into a close-up of the "₹25*" line on the passbook, not another glyph.
- [director] polish t=25.38 s09-uno: the UNO "draw 25" meme is an evergreen classic. The joke shape (balance check → ₹25) lands on "balance kam pada?" and reads fast, but the label "₹25 decline fee" is small at labelSize 52. → raise labelSize to ~64 and give the first label room. Count the meme as 1 of the 2 evergreen slots.
- [editor] polish t=15.5–20.9 Cluster: stamp ₹25 "tax alag" at 15.6, then the chat. The "typing" foley was dropped, so the chat plays silent. → move the stamp 0.4 s earlier, or accept it. Low priority.
- [director] polish t=47.3 s16 meme-format two-panel: the "Nah/Haan" panels sit small in the upper band (~half the width in the sheet). → enlarge the panel to the full content width (~860 px).

## Judgement
- 3-second test: passes. Note fields, receipts, the passbook, the coin and the calculator are all Chillar.
- Rhythm: shots are 1.2–4 s with a held 3.9 s plan slip. The chapter field changes sit on the chapter cuts (note20, 50, 500, bone). The outro is complete with the disclaimer.
- Numbers: ₹25, 4×25=₹100 and ₹1,200 match the script. "tax alag" and "maan lo" scope them correctly.
