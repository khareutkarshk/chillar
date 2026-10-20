# Facts — <episode>

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.
Two rows may go without a URL (CLAUDE.md §3): an invented scenario — source `hypothetical — <why realistic>` — and
arithmetic on other rows — source `computed from F1, F2`. Start an example row's claim with `Example:` /
`Worked example:` / `ILLUSTRATIVE`; the script must frame it as one ("maan lo", "ek typical …", a first-person
story) the first time it's said — fact_lint blocks an unframed first use.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | NPCI's UPI and Services Steering Committee decided on 13 Oct 2026 that, keeping the festive season in mind, MDR on select P2M UPI transactions will be implemented "immediately post Diwali" at a date to be notified separately — so it did NOT start on the earlier 15 Oct 2026 date | https://www.npci.org.in/uploads/UPI_MDR_on_Select_Merchant_Transactions_Shall_be_Implemented_Post_Diwali_4c9cdd77d5.pdf | 2026-10-20 | NPCI press release, Mumbai, 13 Oct 2026, p.1 (cached brand/sources/npci-mdr-post-diwali.pdf.pdf). No exact date yet — don't state one. Press talk of 8 Nov / 1 Jan 2027 is unofficial; say "Diwali ke baad, date abhi nahi aayi". The 15 Oct date comes from the DFS FAQ (F3). |
| F3 | Framework (FAQ dated 15 Sept 2026) was to take effect from 15 Oct 2026; MDR of 0.4% on P2M UPI transactions above ₹2,000; for transactions of ₹75,000 and above the MDR is capped at ₹300; payments up to ₹2,000 carry no MDR | https://financialservices.gov.in/sites/default/files/2026-09/FAQs---Merchant-Discount-Rate--MDR--on-Select-UPI--P2M--Transactions_0.pdf | 2026-10-20 | DFS/NPCI FAQ pp.1-2, 8 (cached brand/sources/dfs-upi-mdr-faq.pdf.pdf). FAQ table: ₹3,000 → 0.40% → ₹12; ₹50,000 → ₹200, "MDR paid by Merchant". Charge applies on the whole amount (0.4% of ₹3,000), not just the part above ₹2,000 — per FAQ table. Start date superseded by F1. |
| F4 | MDR is paid by the merchant: the FAQ table column reads "MDR paid by Merchant"; merchants cannot pass MDR on to customers ("consumers pay only the posted price"); PIB: "MDR is a charge within the merchant payment ecosystem. It is not a charge on customers making UPI payments" | https://financialservices.gov.in/sites/default/files/2026-09/FAQs---Merchant-Discount-Rate--MDR--on-Select-UPI--P2M--Transactions_0.pdf | 2026-10-20 | FAQ p.8 (table + "Can enterprise merchants pass the MDR to buyers? No…"); PIB release PRID 2310586 (via search-result quote, PIB page itself 403/JS-rendered when cached — wording of the PIB line not read in full text). Say "merchant pehle bharta hai" — who bears it economically after prices adjust is NOT in any source. |
| F5 | MDR is distributed only among the UPI ecosystem (banks, UPI app providers) to invest in infrastructure resilience, innovation, cybersecurity and customer service; fee distribution models are decided by the UPI and Services Steering Committee headed by NPCI. MDR is not a tax and not collected by the Government or NPCI | https://financialservices.gov.in/sites/default/files/2026-09/FAQs---Merchant-Discount-Rate--MDR--on-Select-UPI--P2M--Transactions_0.pdf | 2026-10-20 | FAQ pp.1-2. "Not a tax / not collected by Govt or NPCI" is from the PIB release (search-result summary only, not read in full). No per-party split published — an unofficial 40/30/20/10 split in one article is UNVERIFIED — do not use. |
| F6 | PIB (Ministry of Finance): MDR will apply to only about 4% of merchant transactions, so approximately 96% remain unaffected (≤₹2,000, or small merchants); small merchants receiving up to ₹1 lakh a month via UPI QR codes pay zero MDR; P2P transfers stay free regardless of amount | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2310586&reg=48&lang=1 | 2026-10-20 | Figures read via search-result quotes of the release dated 15–16 Sept 2026; pib.gov.in returns 403 to fetch. An estimate ("expected"), not a count. Zero-MDR for small merchants also in FAQ p.6 (no GST registration needed). |
| F7 | Essential / thin-margin sectors (railways, telecom, insurance, fuel, agricultural inputs) pay a flat ₹5 per transaction above ₹2,000; capital-market payments pay 0.02% capped at ₹300; UPI apps may NOT charge any platform fee on UPI payments | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2310586&reg=48&lang=1 | 2026-10-20 | PIB release (search quote) + FAQ p.4 on platform fee. Optional; the reel only needs one line at most. |
| F8 | Worked example: a shopkeeper with a ₹3,000 UPI sale would (once MDR starts) pay 0.4% = ₹12 and receive ₹2,988; the customer still pays exactly ₹3,000 | computed from F3, F4 | 2026-10-20 | Python: 3000*0.004 = 12.0; 3000-12 = 2988. Matches FAQ table (₹3,000 → ₹12). Hypothetical shopkeeper — frame as "maan lo". |

## Texture for the writers (not facts — don't put numbers from here on screen)
- The kirana/chai-tapri uncle with the Soundbox: "paisa aaya" voice is his daily heartbeat; he's never heard of "acquirer".
- Gen Z has scanned a QR for ₹20 samosa and ₹3,000 sneakers the same way — never once wondered who is paying for the rails.
- Everyone's reflex on "charge" news: "ab dukaan wala extra maangega" — the reel's twist is the rule says he can't add it to your bill.
- Diwali shopping season is exactly why it got pushed — retailers, mithai shops, electronics sales are about to peak.
- "UPI free hai" is treated as a law of nature, like free chutney with samosa; free for you ≠ free for the system.
- Group-chat bhaiya: "bhai ₹2,000 se upar pe cash do na" — the exact behaviour people may try.

## Culture now
- M1 · image · "somebody get these beggars outta here" · reaction used to shoo something unwelcome away; fits "MDR ko door karo" or shopkeeper reacting to a fee · peaked 2026-08 · https://imgflip.com/memesearch?q=somebody+get+these+beggars+outta+here
- M2 · image · "Peak Life Events" · ironic "this is what peak looks like" captioning of mundane milestones · peaked 2026-09 · https://imgflip.com/memesearch?q=Peak+Life+Events
- M3 · image · "Dekh raha hai na binod" · Indian classic: "are you watching this?" — said when someone is blatantly ignoring an obvious thing; OLD-BUT-EVERYWHERE, counts as the reel's one classic · peaked 2021-01 · https://imgflip.com/memesearch?q=Dekh+raha+hai+na+binod
- M4 · image · "Bilkul Ricks nahi lene ka" · Indian: "zero risk-taking" deadpan refusal; usable for the merchant refusing a ₹2,000+ sale fee · peaked 2020-06 · https://imgflip.com/memesearch?q=Bilkul+Ricks+nahi+lene+ka
- M5 · sound · "FAAAH" · global absurd-yell sting dropped right after a bad-news line · peaked 2026-09 · https://www.myinstants.com/en/search/?name=FAAAH
- M6 · ref · "aura" / "aura farming" · say "dukaan ka aura -₹12" when a merchant loses a bit per sale · peaked 2026-08 · https://knowyourmeme.com/memes/aura-farming
- M7 · ref · "Diwali ke baad" · the real news hook: NPCI itself said post-Diwali, so every "baad mein dekhte hain" joke lands this week · peaked 2026-10 · https://www.npci.org.in/uploads/UPI_MDR_on_Select_Merchant_Transactions_Shall_be_Implemented_Post_Diwali_4c9cdd77d5.pdf

Note: web searches for this week's Indian meme templates returned nothing dated Oct 2026 — M3/M4 are old Indian classics (≤1 classic per reel: use only one). No fresh verified Indian image template found; imgflip trending is global. Search ran 2026-10-20.
