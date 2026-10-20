verdict: REVISE
round: 1
swipe risk: 0–3s med · 3–15s high · middle med · payoff med

## Prior notes
- none (round 1)

## qa errors
- 0 errors. 1 warn: `empty-paper` t=3.48 checkout (checklist), route director|component:checklist — paper 402px tall, text ends at 64% (confirmed on frame 3.48: bottom third of the paper is blank).

## Notes
- [director] blocker t=5.0–8.0 (scene `peak`): the meme is a white chart (life-events graph) with "LOSING VIRGINITY" / "WEDDING DAY" labels. It is off-palette (pure white slab on a green field), the sexual label is a brand-safety problem for a finance reel, our caption card "Sale ki raat, cousins group" sits on top of the chart's own "LIFE EVENTS" label (clipped, unreadable), and the original text is too small to read at phone size. Replace it with a different global image meme with a clean subject, or drop it. Keep it only if it reads in <1 s.
- [component:headline] blocker t≈11.1–12.8 (scene `shabd`): "Camouflaged." breaks as "Camouflag / ed." — a mid-word break on the key word, on a full-width haldi highlight. Fix: shrink the font size to fit one line, or let the component never break inside a word (the director can't fix this from scenes.json, as the word is 11 chars at the current size).
- [editor] blocker t=26–29 (outro): at t=27.5 the receipt is a blank cream paper with only "CHILLAR RECEIPT" and the field is nearly empty for ~2 s (the contact sheet at 27.0 shows the same). Frame shows no payoff or promise during that time. Print the MDR line earlier (start the tear-off by ~26 s) or add something that reads immediately.
- [director] polish t=3.48 checkout: paper is half-empty (qa warn). Size to rows or add a third row ("EMI ₹…", "Processing fee").
- [director] polish t=0 hook: receipt's "Phone · 6 EMI / No Cost" wraps into two columns that read jumbled; one line "Phone · 6 EMI · No Cost" would read in 1 s. Hook is otherwise on-brand (field, paper, Chillar coin).
- [director] polish t=24.5 meme: lands on "parda hatao" correctly and caption is legible; the photo is off-palette by nature (palette flag at 24.0 is expected for memes). Confirm it is global and this-month fresh per facts.md `## Culture now`.
- [editor] polish t=9–15 (rbi→shabd→parda): three consecutive text-on-navy shots (quote card, giant highlight, headline+card) with similar left-aligned layout; no paper object in `shabd` (a 3-second-test risk). Add a paper scrap/circular behind the quote.

## Verified OK
- Fields change on chapter cuts (green → navy → brown → near-black); theme consistent.
- Wordmark present on all frames until the outro; outro has the MDR line, follow and "Educational only. Not investment advice."
- Audio −14.0 LUFS / −1.5 dBTP.
