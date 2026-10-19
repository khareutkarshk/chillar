verdict: REVISE
round: 3
swipe risk: 0–3s low · 3–15s low · middle low · payoff low-med
## Notes
Ranked by what it would actually cost viewers or the channel.

### Blocker (one parameter change; nothing else needs re-review)
- [component:odometer-number|director] t=22.17–22.6 With count mode, the held start frame now reads as a statement: label "Haath mein:" / big "₹1,00,000" / "/mahina" / sub "₹10,37,617/saal ÷ 12 · example". The VO says "Haath mein:" over it at the same moment (21.80–22.50). A paused frame or screenshot says the in-hand pay is ₹1,00,000 a month, and the ÷12 line under it is arithmetically false (₹10,37,617 ÷ 12 = ₹86,468). That is a number on screen that contradicts F9, at the payoff. Round 2's label "₹1,00,000 nahi. Haath mein:" framed it as the myth; dropping "nahi" removed that framing. The TAX ₹0 · ALIBI stamp riding in until 22.40 adds a second unrelated claim to the same frame. → Fix any one of these:
  (a) restore the label "₹1,00,000 nahi. Haath mein:";
  (b) draw the held start value as the myth (in quotes, "₹1,00,000?", or with the pen strike used on the sticker) and switch to the plain style when the count starts;
  (c) keep the sub line hidden until the count lands (about 23.6) and show the label as "1 lakh?" until then.
  Option (a) or (c) needs nothing else changed. Then re-check the frames at 22.4 and 23.8.

### Polish (would not cost viewers; do only if touching the file anyway)
- [component:outro] t=27.55–27.6 One frame still shows the receipt as a grey translucent card mid-snap. It's a single frame and invisible at speed. → If edited: hard opacity snap on frame 1 (opacity 0→1 within 1 frame) with the scale pop doing the motion.
- [editor] t=22.1–22.4 The TAX ₹0 · ALIBI stamp (y 234–366, inside safe) floats over the new teal chapter above "Haath mein:" for 0.3 s. It's fine once the blocker is fixed (it then reads as a carry-over). Cleaner: let it slide off with the cut, ending at about 22.25.
- [component:mithai-dabba] t=16.6–18.8 The locker nameplate is fine: "Your PF" is about 48px, "₹66,600/saal" about 34px, and the sub "tumhare naam pe" about 30px. It's readable and doesn't need fixing.

## Round-2 notes verified (fresh frames)
- Odometer FIXED: "₹1,00,000" is legible from the cut (22.17 label, number by 22.4), held about 0.3 s, then counts down as one tabular number (91,589 → 86,937 → 86,469) and lands on ₹86,468 at about 23.6–23.8. The underline draws at 23.8, and the ding moved to 23.7 on the landing, inside the spoken "₹86,468" (22.56–24.12). No blank or clipped digits.
- Audio FIXED: re-measured output/final.mp4 with ffmpeg ebur128: −14.0 LUFS integrated, −1.1 dBTP true peak. Matches mix_report.json final_true_peak_dbtp.
- 3.40–3.55 FIXED: the slip-in dabba and slip are on screen from 3.44. The one-frame caption gap at 3.44 is invisible.
- Outro FIXED: prints top-down (header 27.8 → rule 28.1 → MDR/Gyaan 28.5 → disclaimer + stub 28.9), tears at about 29.2, Chillar at 29.9. Final frame complete with "Educational only. Not investment advice." and "Agla receipt jaldi."
- Tax beat FIXED: scratch 21.32, stamp impact about 21.37 on "₹0" (21.34), held to 22.40 (about 1.0 s); shocked reaction 21.45; ₹0 circle (21.9) clears the "Income tax" label. Stamp top edge y=234 (safe ≥220).
- Locker FIXED: paper interior with shelves, laddoo drops in at about 16.0 on "PF" (16.16), door shuts with nameplate by 16.6, padlock and "12 mahine" at about 18.3 on "locked" (18.16).
- Reactions FIXED: facepalm (7.3) and open-to-work (13.8–15.1) clear the slip meta line; the open-to-work label is readable.
- Lid FIXED: Chillar's arm pushes the lid (26.6), lid shut by 26.9 on "nahi" (26.78), held 0.6 s; mascot inside the right margin; sticker strike readable.
- Entrances: snaps everywhere sampled; no grey fades except the single outro frame noted above.
- Palette report clean (≤0.01%). Numbers match F9 with Indian grouping everywhere except the blocker frame. Night theme consistent. Two thappas. No AI-look tells: no caps pills, page-flip is a real move, shots vary through the middle.
