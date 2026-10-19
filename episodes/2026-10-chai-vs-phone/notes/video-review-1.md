verdict: REVISE
round: 1
swipe risk: 0–3s low · 3–15s med · middle med · payoff med

## Prior notes
- none (round 1)

## QA warnings (copied)
- [director|component:calendar-flip] t=21.04 small-object: paper spans 612px (content width 880) → widen the calendar (width param) to ≈ 860.
- [director|component:receipt-list] t=33.02 small-text: text at 35 px → make rows ≥ 36 px.

## Notes
- [director|component:hook-card] t=0 "₹1,00,000" runs past the right edge of the receipt paper (clipped at x≈460/540, last zero touches the edge) and the "(example)" sub-lines wrap to two lines, so the stakes look cramped. Frame 1 is the stakes frame → shorten labels (drop "(example)" or put it on the paper's footer), reduce the amount font or widen the paper so the number sits inside with a margin.
- [director|component:marker-highlight] t=5.68–8.2 headline "Chai = barbaadi!!!" wraps with a lone "!" on its own line (frame at 6.0). Looks like a bug → cut to "Chai = *barbaadi*!!" at a size that fits one line, or lower size from 196.
- [director|component:calendar-flip] t=19.84–22.5 "Tapri pe absent" shows a big blank calendar page: no visual joke, nothing happens for ~2.6 s while the caption carries it. Add the content (Chai, crossed-out days / red pen X marks, or Chillar side-eye at the empty tapri) and make it full width (see qa).
- [director] t=13.94, 31.82, 49.96 receipt-list used three times (plus the outro receipt) with the same black-header look; the middle section also repeats "Bade Mama" statement (3.72, 22.5). Vary: make one of them a different object (e.g. phone-bill slip, passbook, or the bars at 42.9 as the payoff) or change the entrance on the repeat.
- [director|component:receipt-list] t=13.94 the receipt holds just two lines in a tall empty paper until the total prints; ₹100 line is the only thing for ~1.7 s. Tighten the totalAt or enlarge the type so the frame reads at a glance.
- [director] t=47.54 final "rule" frame is a centred headline + coin with no paper object, and it is the payoff of the video — the one moment that should feel like a stamp/thappa. Consider the rule on a stamped paper scrap (within the stamp budget) instead of bare text.
- [director] t=45.0 the yearly-bars chart is the right payoff idea, but the "Chai" bar is blank white next to a flat haldi block, labels are tiny (Chai/Phone/example). Enlarge the labels and add a pen mark on the gap so it reads in 1 s.

Checked and fine: wordmark present on every frame, outro complete with MDR line + follow + disclaimer, audio −14 LUFS / −1 dBTP, no structure labels, no eyebrow pills.
