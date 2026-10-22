verdict: PASS
round: 1
swipe risk: 0–3s med · 3–15s low · middle low · payoff low

## Prior notes
None (round 1).

## QA warnings (no errors) — routes copied
- warn short-shot t=0.0 s1-hook 1.42s < 1.5 [editor]
- warn small-object t=0.02 s1-hook paper 594px [director|component:hook-card]
- warn dense/short-shot/read-hold t=3.04–3.84 s3-chat 17 words, 1.86s [director/editor]
- warn short-shot t=3.76 s3-sideeye 1.14s [editor]
- warn early-number t=6.1 "₹100 / din" shown 1.1s before voice [editor]
- warn read-hold t=6.3 s4-rule [editor|director]
- warn dense t=7.34 s5-passbook 26 words/2.9s; empty-paper t=7.88; read-hold t=8.94 [director|component:passbook-page]
- Voice check: 0 flagged. sfx_dropped: outro coin only (not a joke) — fine.

## Notes
- [director] polish t=0.02 Frame 1 is a small card (594px) top-left with a lot of empty field, and the cover promise ("Day 30 circled in blue ballpoint") is not there: "Day 30" is red text, not circled. → widen the hook-card (wide:true / bigger paper) and make the Day 30 row carry the blue circle; keep the circle param on the Day 30 amount.
- [editor] polish t=0–1.42 hook shot is 1.42s, under minDuration. → hold s1-hook to ≥1.5s (shift the s2 cut to ~1.55, on "complaint").
- [director] polish t=3.04 s3-chat: 17 words in 1.9s, and the chat isn't readable. → cut to 2 bubbles ("Report mein galti hai" / "Ticket raised 🙂"), drop the third, or extend to ≥2.6s.
- [editor] polish t=6.1 "₹100 / din" appears 1.1s before "₹100" is spoken (7.18). → set that row's `at` to ~1.0s so it lands on "har din", and hold s4 into the next line (L-cut).
- [director] polish t=7.34 passbook: 26 words and half-empty paper; "+100" repeated 4× reads as a table, not a joke. → 3 rows with bigger size (52+), grow paper to rows; circle the 400 on "kharcha".
- [director] polish t=3.76 side-eye Chillar is 1.14s and sits low-right, away from the chat. → run it to the shot end (≥1.2s) and land it on "bhool jaoge".
- Observation: "Is video ka MDR: 0%" in the outro is brand-mandated, though off-topic for a credit-report reel. No change.
