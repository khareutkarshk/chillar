# Facts — gold-bill-decoded

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | GST on gold jewellery is 3% of the total transaction value of the jewellery (since 01.07.2017) | https://gstcouncil.gov.in/sites/default/files/2024-02/sectoral-fq-gems-jewellery.pdf | 2026-10-21 | CBIC sectoral FAQ p.4: "GST is payable at the rate of 3% of the total transaction value of jewellery". Library-grade. Says "3% on total value", answering "3% on total or 3% on gold + 5% on making?" |
| F2 | The 3% applies to the whole bill value — gold plus making charges together — not a separate 5% on making charges at the shop counter | https://gstcouncil.gov.in/sites/default/files/2024-02/sectoral-fq-gems-jewellery.pdf | 2026-10-21 | p.4 same Q&A. Many blogs say "5% GST on making" — that is wrong for a retail buyer. The 5% is only the job worker's rate on job charges (to the manufacturer). Don't say "5% on making" for buyers. Retail bill = 3% on all. |
| F3 | The 5% GST rate applies to a registered job worker's job charges only (jeweller ↔ karigar), not to the retail customer | https://gstcouncil.gov.in/sites/default/files/2024-02/sectoral-fq-gems-jewellery.pdf | 2026-10-21 | p.4: "job worker, if registered... 5% on job charges only". Use only if the script needs the "5% myth" line; widest wording: "karigar-level job work, not your bill". |
| F4 | HUID is a six-digit alphanumeric code, unique per jewellery article, laser-marked by the hallmarking centre along with BIS logo and purity mark | https://services.bis.gov.in/php/BIS_2.0/BISBlog/?p=560 | 2026-10-21 | BIS blog (dated 2022): "unique HUID code is generated from the BIS server for each jewellery article". Say "six-character code" (BIS text says six-digit alphanumeric). |
| F5 | You can check a HUID with the "Verify HUID" feature in the BIS Care mobile app | https://services.bis.gov.in/php/BIS_2.0/BISBlog/?p=560 | 2026-10-21 | Same page. Name is an official govt app (BIS Care) — CLAUDE.md bans recommending apps; say "sarkari BIS Care app" only as an official verification tool, or cut the name if the reviewer objects. |
| F6 | Mandatory hallmarking covers 14, 18, 20, 22, 23 and 24 carat gold jewellery/artefacts (IS 1417) | https://services.bis.gov.in/php/BIS_2.0/BISBlog/?p=560 | 2026-10-21 | "in notified districts" — coverage is district-wise (phased), so say "notified districts / kai shehar"; don't say "everywhere in India". 2022 page; a later phase reportedly added districts (2026) — unverified here. |
| F7 | BIS hallmarking charge is ₹45 per piece of gold jewellery irrespective of weight | https://services.bis.gov.in/php/BIS_2.0/BISBlog/?p=560 | 2026-10-21 | Page dated Oct 2022; fee may have been revised since — say "BIS ka fee ₹45 per piece tha (2022 page)". Safest: don't put on screen as current. A jeweller's own hallmark charge on your bill may differ. |
| F8 | Worked example: 10 g of 22-carat jewellery, gold value ₹1,20,000, making charge 12% = ₹14,400; subtotal ₹1,34,400; 3% GST = ₹4,032; bill ₹1,38,432 | hypothetical — realistic round-number gold price and a typical 8–25% making-charge ask; invented numbers, not today's rate | 2026-10-21 | Makes: GST is on the making too (₹14,400 × 3% = ₹432 of the ₹4,032). Extra paid over gold alone = ₹18,432 = 15.4% of the gold value. Script must say "maan lo". Making % is set by each jeweller — "kai jewellers 8–25%" is NOT sourced; use only "jeweller decides", unsourced. |
| F9 | Worked example: of the ₹1,38,432 bill, ₹14,400 is making charge and ₹4,032 is GST — together ₹18,432 that isn't gold you can melt for full value | computed from F8 | 2026-10-21 | Careful: "can't melt for full value" is a general claim — keep as "making charge aapko resale pe wapas nahi milta" only if sourced; it's NOT sourced here, so keep to arithmetic. |

```
gold ₹1,20,000 | making 12% ₹14,400 | subtotal ₹1,34,400 | GST 3% ₹4,032 | total ₹1,38,432
GST on making alone = ₹432 ; extras over gold = ₹18,432 = 15.36% of gold value
```

## Not usable (unverified)
- Making charges are fixed by law or capped at some % — no primary source; making charge is set by the jeweller and negotiable (not found in CBIC/BIS).
- Typical making-charge range (8–25%) — only blogs.
- Current hallmarking district count / the 2026 sixth phase (380 districts) — only a news snippet; BIS notification not opened.
- Today's gold price / Dhanteras date price — not a primary source and changes daily.
- Whether GST (3%) also applies on the ₹45 hallmark fee, and whether the fee changed after 2022 — not confirmed.
- Old-gold exchange / buyback deduction rules — no primary source.

## Expert take
- myth: "Making charge ka alag 5% GST lagta hai, aur HUID bas ek sticker hai." (F2, F4)
- so what: GST is a flat 3% on the *whole* bill, making included — so every rupee of making charge also carries 3% tax; and the making charge itself is the jeweller's number, which is where the real money hides. [F1, F2, F8]
- in ₹: On a ₹1,20,000 piece, ₹14,400 making + ₹4,032 GST = ₹18,432 extra, a bill of ₹1,38,432 — one-time, on one purchase (the year-view is the same single Dhanteras purchase). [F8, F9]
- do: Before paying, ask for an itemised bill (gold weight, rate, making %, GST) and check that the HUID printed on the bill matches the HUID punched on the piece.
- follow-up: "Papa: kya HUID sahi hai ye kaise pata?" → Hallmark ka six-character HUID BIS ke Verify HUID feature se check hota hai. [F4, F5]
- jargon: making charge = jeweller ki banai ki fees; HUID = har gehne ka apna six-character ID; hallmark = sarkari purity ka thappa; GST = sarkari tax jo bill mein judta hai.

## Texture for the writers (not facts — don't put numbers from here on screen)
- Dhanteras = "shagun" purchase: a chandi coin or a small chain, mummy ne budget pehle se fix kiya hai, jeweller ke yahan "aunty ji, aap ke liye special rate".
- The bill is a long slip with 6 columns nobody reads; the jeweller says "bas making thodi si hai".
- Dad's line: "Humare jeweller pe 40 saal se jaate hain" — trust beats paperwork.
- Dhanteras crowd, pressure to pay UPI / cash quickly while 12 people wait behind you.
- The cousin who bought a "gold coin" off a reel and now has no bill.

## Culture now
- M1 · image · "somebody get these beggars outta here" · mock-royal dismissal: the speaker waves away a lowly/poor thing; use for a jeweller waving away a "discount" request · peaked 2026-08 · https://imgflip.com/memesearch?q=somebody+get+these+beggars
- M2 · image · "Aura Farming" · gaining aura points through effortless confidence; use when the jeweller acts casual about the bill · peaked 2025-10 · https://imgflip.com/memesearch?q=aura+farming
- M3 · image · "Ab itna kharcha ho hi gaya" · Indian classic: "kharcha toh ho hi gaya, ek aur sahi" — fits adding making charge to an already big bill (evergreen) · peaked 2021-04 · https://imgflip.com/memesearch?q=ab+itna+kharcha
- M4 · image · "Bas karo bhai" · Indian classic: begging someone to stop (evergreen) — use when the bill keeps adding lines · peaked 2020-09 · https://imgflip.com/memesearch?q=bas+karo+bhai
- M5 · sound · "Sad Violin (the meme one)" · dramatic tragic sting after a loss — use after the final total · peaked 2024-06 · https://www.myinstants.com/en/search/?name=sad+violin
- M6 · ref · "Cockroach Janta Party" · youth satire movement from May 2026 about unemployment/frustration (no politicians; mention only the "cockroach" joke if at all) · peaked 2026-05 · https://www.brut.media/in/
- M7 · ref · "Mere Mehboob Qayamat Hogi" reel trend · dramatic Kishore Kumar remix lip-sync; use as the dramatic "qayamat hogi" when the bill lands · peaked 2026-08 · https://www.freepressjournal.in/lifestyle/chetan-bhagat-ranveer-brar-zakir-khan-join-viral-reel-trend-after-anupam-kher-why-should-gen-z-have-all-the-fun-watch
