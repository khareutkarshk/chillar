# Component backlog

Open requests from directors and reviewers. `produce.py <any ep> --only components` builds them in one
batch; done items get `- [x]`. One open line per component (produce.py merges repeats).

- [x] [component:asterisk-lawyer] an asterisk in a lawyer's coat for "Objection" → built as `glyph-character` (costume lawyer/crown/detective)  _(2026-10-sale-fine-print · edit-1-director)_
- [x] [component:phone-screen] chat screen with a pinned message → built as `chat-screen`  _(2026-10-no-cost-emi · edit-1-director)_
- [x] [component:headline] long word breaks mid-word → `CH.fitHead` shrink-to-fit, statement `fit` (default on)  _(2026-10-no-cost-emi · edit-6-director)_
- [x] [component:tier-compare] needs full width → `wide` / `width` params  _(2026-10-sale-fine-print · component-requests-1)_
- [x] [component:odometer-number] plain roll to ₹1,500 lands garbled → `CH.roll` lands exactly, neighbours hidden  _(2026-10-sale-fine-print · component-requests-1)_
- [x] [component:mascot-reaction] optional meme `sound` → `sound`/`soundAt`/`soundPick` params  _(2026-10-sale-fine-print · component-requests-1)_
- [x] [component:checklist] paper grows per row → `grow` param  _(earlier episode)_
- [x] [component:marker-highlight] optional paper behind the quote → `paper` param  _(earlier episode)_
- [x] [component:hook-card] `mascot: "none"` still drew a mascot → treated as no mascot  _(2026-10-27-diwali-bonus-tax · producer)_

- [x] [component:tier-compare] (28 px floor; amtSize exists) tier labels/amounts render ~20–22 px in 3-tier wide mode (even with amtSize 48); need ≥ 28 px (≈ 44 px wide mode), and an amount-size option so the key number is big and the card fits it  _(mdr-payer ×6, diwali-bonus-tax ×5)_
- [x] [component:chat-screen] (already 42/36 px, time padded) body text ≥ 40 px, name/time/header ≥ 36 px (or a `size` param); reserve right padding so the timestamp never overlaps the last word  _(credit-enquiry ×6)_
- [x] [component:calendar-flip] (type scales; height -1 fits) `width` param (560–880, default 860), page type scales with it, page height fits its text (now 77 % blank)  _(mdr-payer ×5)_
- [x] [component:meme] (covered: wide, height, position) `width`/`fit` param so portrait templates span ≈ 860 px; paper shrinks to the image + label text (half-empty paper warnings)  _(mdr-payer ×4, diwali-bonus-tax ×2)_
- [ ] [component:mithai-dabba] mascot x/y params; paper height fits the letter text (qa empty-paper), tray excluded from the paper measurement  _(diwali-bonus-tax ×2)_
- [ ] [component:glyph-character] wide-bubble / bubble `width` param, or count the glyph's ink in the object width so qa small-object stops firing  _(credit-enquiry ×4)_
- [x] (sub now sits below, flex none) [component:stamp] the `sub` line prints on top of the main text — set it below the main text inside the stamp  _(credit-enquiry)_
- [x] (decimal point gets own spacing) [component:odometer-number] with `decimals:1` the '0' and '.' draw on top of each other  _(mdr-payer)_
- [x] (title own row, no overlap) [component:split-compare] the title ('Rule') overlaps its own long text when the chits hold longer  _(mdr-payer)_
- [x] (new `minHeight` param, default 0) [component:receipt-list] with one item + total, the paper shrinks to the printed rows  _(mdr-payer)_
- [ ] [component:envelope] NEW: an addressed envelope ('Bill to / Address / Pincode') for letter beats — paper object per Note Fields  _(mdr-payer)_
