verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s med · middle low · payoff low

## Prior notes
- none (round 1)

## qa
- warn short-shot t=18.12 o08-stamp 1.04s < 1.2s [editor] (see polish 1)
- no errors; voice_check 0 flagged (L1/L8 75% = ASR noise on "account"/"OTP"; not a blocker).

## Notes
- [editor] polish t=18.12 SUSPECT stamp is on screen 1.04s (min 1.2s) → extend duration to ≥1.25s (ends ~19.16 cut, so start it at ~17.95 or let it run to 19.2). Frame 18.5 shows it lands well on "naam?" and reads instantly.
- [director] polish t=4.56–6.88 and t=16.86–19.16 receipt-list sits in top third (box h≈410–530 px) leaving a dead band y≈600–1100 above captions. → raise receipt `width`/add a 4th line (e.g. "Bank statement: tumhara naam"), or set dy≈+160 so the object sits mid-field.
- [director] polish t=12.38–14.0 meme "Maal kidhar hai": the headline "Ek hi naam: tumhara" duplicates the caption being spoken at the same time and the meme is a knife-waving frame. → keep, but change headline to a reaction ("Grader ka mood") or drop headline so caption carries the line; also the meme is an old classic—note it as the one classic allowed in this reel.
- [director] polish t=19.16 Pattinson/Chris Hansen meme follows right after the SUSPECT stamp: same "you're caught" beat twice. → fine to keep, but shorten the stamp or the meme (1.5 s) so only one lands.
- [editor] polish dropped SFX: printer@16.86 (s08-list) and whoosh@13.87 lost the 2 s thinning; s08 prints silently. → acceptable; optionally move stamp thunk to 18.25 and keep printer by nudging s08 print step.
- [director] polish t=20.66 checklist shows only first row "Account" at 21.0 while voice is on "OTP" — rows lag the speech by ~1 s. → reduce `stagger` 0.15→0.1 or start checklist 0.4 s earlier so each word lands with its row.
- [director] polish t=28.66–31.86 outro: second Follow strip slides over/duplicates the first (30.0 vs 31.8 frames show Follow slip moving to a tilted position beside mascot). Complete and disclaimer present; no change needed beyond confirming the tear isn't reading as a duplicate.
