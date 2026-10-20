# Component backlog

Open requests from directors and reviewers. `produce.py <any ep> --only components` builds them in one
batch; done items get `- [x]`.

- [x] [component:asterisk-lawyer] an asterisk in a lawyer's coat for "Objection" → built as `glyph-character` (costume lawyer/crown/detective)  _(2026-10-sale-fine-print · edit-1-director)_
- [x] [component:phone-screen] chat screen with a pinned message → built as `chat-screen`  _(2026-10-no-cost-emi · edit-1-director)_
- [x] [component:headline] long word breaks mid-word → `CH.fitHead` shrink-to-fit, statement `fit` (default on)  _(2026-10-no-cost-emi · edit-6-director)_
- [x] [component:tier-compare] needs full width → `wide` / `width` params  _(2026-10-sale-fine-print · component-requests-1)_
- [x] [component:odometer-number] plain roll to ₹1,500 lands garbled → `CH.roll` lands exactly, neighbours hidden  _(2026-10-sale-fine-print · component-requests-1)_
- [x] [component:mascot-reaction] optional meme `sound` → `sound`/`soundAt`/`soundPick` params  _(2026-10-sale-fine-print · component-requests-1)_
- [x] [component:checklist] paper grows per row → `grow` param  _(earlier episode)_
- [x] [component:marker-highlight] optional paper behind the quote → `paper` param  _(earlier episode)_
- [ ] **[component:calendar-flip]:** add a `width` param (paper up to 860 px) and scale the page type with it. The paper is 608 px wide and 77 % blank.  _(2026-10-26-report-mdr-payer · video-review-2, t=6.06)_
- [ ] **[component:meme]:** add a `width`/`fit` param so portrait templates (Waiting Skeleton) fill ≈ 860 px. It renders at 574 px now.  _(2026-10-26-report-mdr-payer · video-review-2, t=12.66)_
- [ ] **[component:tier-compare]:** tier amounts render at ~20 px; they need to be ≥ 28 px.  _(2026-10-26-report-mdr-payer · qa t=13.59)_
- [ ] **[component:chat-screen]:** the name, time and header text renders at 26–35 px; it needs to be at least 36 px.  _(2026-10-credit-enquiry · edit-1-director.txt)_
- [ ] **[component:stamp]:** a `sub` line prints on top of the stamp's main text, so I dropped all subs.  _(2026-10-credit-enquiry · edit-1-director.txt)_

- [component:chat-screen] (2026-10-credit-enquiry) message text renders 34–35 px and name/timestamps 26–30 px even at width 880 — needs a `size` param or a ≥ 36 px default so qa small-text passes.
- [component:glyph-character] (2026-10-credit-enquiry) only the speech bubble counts as "paper" (370–520 px), so qa flags small-object on every glyph shot — either a wide bubble option or exempt the glyph's ink from the paper-width check.
- [ ] `[component:chat-screen]` needs a size setting or a default of 36 px or more for message text.  _(2026-10-credit-enquiry · edit-3-director.txt)_
- [ ] `[component:glyph-character]` needs a wide-bubble option, or qa should count the glyph as part of the object's width.  _(2026-10-credit-enquiry · edit-3-director.txt)_
- [ ] [component:chat-screen] polish t=10.62, 32.16, 40.46, 47.42, 64.48: bubble/time/header text 26–35 px (qa small-text warnings). Fix in the component: raise body to ≥ 40 px and time/header to ≥ 36 px. On the sheet the chat cards read small inside a wide empty field at 12 s, 33 s, 42 s, 48 s.  _(2026-10-credit-enquiry · video-review-1.md)_
- [ ] **[component:chat-screen]** names, times and bubble text need to be at least 36 px, or the component needs a size param.  _(2026-10-credit-enquiry · edit-5-director.txt)_
- [ ] **[component:glyph-character]** the bubble needs a width or size param so qa doesn't flag it as a small object.  _(2026-10-credit-enquiry · edit-5-director.txt)_
- [ ] [component:chat-screen] polish t=49.5 the timestamp "11:58 PM" overlaps the word "hey" in the "me" bubble (also crush-hey at 32). Fix: reserve right padding for the time inside the bubble.  _(2026-10-credit-enquiry · video-review-2.md)_
- [ ] `[component:odometer-number]` with `decimals:1`, the "0" and the "." draw on top of each other.  _(2026-10-26-report-mdr-payer · edit-1-director.txt)_
- [ ] `[component:tier-compare]` with two `reveal:"results"` tiers, the amount labels render at about 20 px; they need to be 28 px or more.  _(2026-10-26-report-mdr-payer · edit-1-director.txt)_
- [ ] `[component:split-compare]` the "Rule" title overlapped its own long text when the chits had more time on screen.  _(2026-10-26-report-mdr-payer · edit-1-director.txt)_
- [ ] `[component:calendar-flip]` needs a width/wide setting and a page sized to its text.  _(2026-10-26-report-mdr-payer · edit-1-director.txt)_
- [ ] `[component:envelope]` an addressed envelope ("Bill to / Address / Pincode") for the cover's letter idea. For now that beat is a paper chit with blank address lines.  _(2026-10-26-report-mdr-payer · edit-1-director.txt)_
- [ ] `[component:calendar-flip]` needs a `width`/`wide` setting so it can span the full 860–880 px. The paper also needs to fit the date text, which currently ends 23% of the way down a 628 px page.  _(2026-10-26-report-mdr-payer · edit-5-director.txt)_
- [ ] `[component:receipt-list]` with one item and a total, the paper should shrink to the printed rows.  _(2026-10-26-report-mdr-payer · edit-5-director.txt)_
- [ ] `[component:meme]` needs a `wide` setting for meme pictures that are too narrow.  _(2026-10-26-report-mdr-payer · edit-5-director.txt)_
- [ ] `[component:tier-compare]` the tier amounts (₹2,000 tak / se upar) render at about 20 px, below the 28 px minimum.  _(2026-10-26-report-mdr-payer · edit-5-director.txt)_
- [ ] [component:tier-compare] polish t=13.6–16.2: the 2,000 threshold is the key number but sits in ~20 px text on small cards, and the "se upar" card is mostly empty yellow. → backlog: an amount-size option, so the number is big and the card fits it.  _(2026-10-26-report-mdr-payer · video-review-2.md)_
- [ ] `[component:calendar-flip]` add `width` (up to 860 px) and scale the page type with it.  _(2026-10-26-report-mdr-payer · edit-8-director.txt)_
- [ ] `[component:meme]` add `width`/`fit` so portrait templates fill about 860 px.  _(2026-10-26-report-mdr-payer · edit-8-director.txt)_
- [ ] `[component:tier-compare]` amounts need to be at least 28 px.  _(2026-10-26-report-mdr-payer · edit-8-director.txt)_
- [ ] `[component:calendar-flip]` add a `width` param (560–880, default 860) and scale the page text with it, so a 3-page calendar fills its paper.  _(2026-10-26-report-mdr-payer · fix-2-director.txt)_
- [ ] `[component:meme]` add a `width` param (up to 880) so a portrait template like Waiting Skeleton can span the content width.  _(2026-10-26-report-mdr-payer · fix-2-director.txt)_
- [ ] `[component:tier-compare]` the tier amounts render at about 20 px; they need to be at least 28 px.  _(2026-10-26-report-mdr-payer · fix-2-director.txt)_
