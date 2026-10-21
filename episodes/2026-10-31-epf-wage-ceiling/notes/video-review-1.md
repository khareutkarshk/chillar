verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s med · middle low · payoff med

## Prior notes
- none (round 1)

## qa
- warn late-text t=11.25 years (calendar-flip), route director|component:calendar-flip — 33% of words shown 0.8 s after cut. Fresh frame 11.25 shows only "SEP 2026" on the final page (the 2014/2020 pages flipped by too fast); it reads, so non-blocking.

## Notes
- [director] polish t=10.42 calendar-flip flips 2014→2020→2026 inside ~0.6 s, so "saalon baad" (years passing) is not seen. → set flip ≈0.25 and start pages at "SEP 2020", or extend `years` to ≥1.9 s, so the year change registers before "2026".
- [director] polish t=23.8–24.3 bar-chart: contact-sheet frame at 24.0 shows only the title and "Pehle / Ab" labels, no bars, and it sits in a big empty area. → set stagger 0.1 and start the bar growth on the cut so bars are visible by 24.1 s.
- [director] polish t=0.0 hook stakes: "PF kata −₹2,640" next to "In-hand −₹840" reads as if PF cut ₹2,640 more. The true extra deduction is ₹840 (₹2,640 vs the old ₹1,800). → relabel the first row "PF ab" / "₹2,640" with no minus, or use "PF zyada kata" / "−₹840".
- [director] polish t=3.36 meme-deceive (Why would I deceive you?): an older classic, and the label bar sits over the lower face. Lands on "Policy" and reads well. → if the channel has leaned on it, swap; otherwise move the label to y≈92 so it clears the mouth.
- [editor] polish t=21.5 locker-room: the "Socha" card is greyed and the right "Asal" card is not yet visible at 21.5, so the joke's setup is half the frame in a large empty zone. → no fix needed beyond keeping revealAt 1.8 on "ghar ka kamra" (22.96). Check that the reveal lands on "ghar", not later.
- [editor] polish sfx: the "ding" on the new ₹25,000 number and the print sound for the slip were dropped, which is fine. The sad violin at 17.1 lands right on "₹840 kam", which is good. No action.
- voice: 0 flagged lines. L6 shows 60% match, which is ASR noise on "refresh"/"Baaki aate hi honge". It reads as normal speech, so not a blocker.
