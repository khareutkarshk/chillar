verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s med · middle med · payoff low

## Prior notes
- none (round 1)

## QA errors
- none (errors: 0). Warnings copied below.
- warn t=8.34 s4-audit checklist: paper 65% filled → [director|component:checklist] see polish
- warn t=15.18 s7-passbook: paper 68% filled → [director|component:passbook-page] see polish

## Voice / SFX
- voice_check: 0 flagged lines. Low L1 match (60%) is ASR noise on "Bhai Dooj", not a pronunciation fault.
- sfx_dropped: coin@3.93 (side-eye), printer@12.24 and @13.98 (receipt/passbook), coin@31.54. The receipt and passbook print silently, but the stamp at 12.85 covers that moment. Only the passbook is a gap.

## Notes
- [director] polish t=13.98–16.84 s7-passbook: paper is half-empty (qa warn) and the small mono rows are hard to read at phone size. The ₹60,000 line is spoken at 15.6, but the shot only ever shows ₹30,000 rows. → Set `size` to 56+ and use rows `Cousin ₹30,000` and `Dost ₹30,000`, so the page shows ₹60,000 when it is spoken. Or drop the passbook and reuse the receipt-list with a ₹60,000 total.
- [director] polish t=7.14–9.74 s4-audit: paper is half-empty (qa warn). → Add a 4th row (e.g. "Dakshina?" ok:false) or enlarge the type so the paper fills.
- [director] polish t=16.84–19.4 s8-mausi-vs-tax: the left card ("Mausi / Cousin ghar ka") sits alone for 1.6 s with grey, low-contrast type, and the frame is mostly empty field. → Set `revealAt` ≈ 0.9 so "Tax / Cousin bahar ka" lands on "tax ke liye" (18.42), and use ink instead of the faded grey.
- [director] polish t=26.06–27.0 s12-payoff: the "Cousin-dost" panel is dim and faded when the voice says "cousin-dost" at 27.05. The reveal arrives about a second after the payoff starts. → Set `reveal` to 0.5 or lower so both panels are readable by 27.0.
- [director] polish t=9.74–12.24 and 24.04–26.06: phone-note is used twice (s5, s11), both as small cream cards in the upper third of a navy field. The ₹10,000 strike line on s11 is a thin shot. → Make s11 a big-number object, e.g. a "₹10,000" circled in blue ballpoint, instead of another note card.
- [director] polish t=7.14–26.06: one navy field for 19 s, with the content cards all hugging the upper area. → Add a chapter field change at ~16.84 (the cousin twist), e.g. calm or note10.
- [director] polish t=19.4 s9 meme ("Did you say POTENTIAL blank"): the label sits on an anime image. It lands on the word after "bahar ka", which is correct, and reads fast. Note: this is a niche reaction template. Keep it only if it counts as one of the 2 evergreen classics.
- [editor] polish t=13.98 and 31.04: the printer foley for the passbook was dropped to the stamp. → Give the passbook row a short typewriter or coin tick at ~14.5 so the page isn't silent.
