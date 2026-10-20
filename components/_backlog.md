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
