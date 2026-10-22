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
| F1 | Worked example: ek typical ₹40,000 in-hand salary, 1 Nov ko credit. By 12 Nov: rent+maid+wifi share ₹14,000, credit card bill ₹6,200, 4 subscriptions autopay ₹1,347, food delivery (9 orders) ₹3,600, weekend cafe/outing/cab ₹4,100, sale shopping ₹3,200, UPI to friends ₹1,800 = ₹34,247 gone; ₹5,753 left for 18 days (≈ ₹319/day) | hypothetical — a typical metro first-job in-hand pay and typical line items; invented, not a real slip or bill | 2026-10-21 | Script must say "maan lo / ek typical". Arithmetic checked in python. Split spends are illustrative, not statistics — never say "average Indian spends". |
| F2 | RBI Digital Payments – E-mandate Framework 2026 (21 Apr 2026): issuer must send a pre-transaction notification at least 24 hours before the actual debit; customer can choose the mode (SMS, email etc.); must show merchant name, amount, date/time, references, reason | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374 | 2026-10-21 | library:L-RBI-EMANDATE-PRENOTIFY. Pre-transaction Notification (a)-(b), mode choice clause. FASTag/NCMC auto-replenish exempt — don't say "every". (from 2026-10-28-free-trial-autopay F2/F3) |
| F3 | RBI E-mandate Framework 2026: customer must get a facility to opt out of any particular transaction or the whole e-mandate; opt-out validated by issuer using AFA (PIN/OTP-type check) | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374 | 2026-10-21 | library:L-RBI-EMANDATE-OPTOUT. Wording: "validated by the issuer using AFA" — script may say PIN/OTP only as paraphrase. (from 2026-10-28-free-trial-autopay F4) |
| F4 | EPF: employee pays 12% of basic wages (+DA); employer also pays 12%. For a new joiner above the EPF wage ceiling who is not already an EPS member, the employer's whole 12% goes to EPF (no pension share) | https://www.labour.gov.in/static/uploads/2025/06/93561f36d5094b0cfe52570b4e8d2dc1.pdf | 2026-10-19 | library:L-EPF-RATE. MoLE EPF Scheme note. 8.33% EPS share only for EPS members, capped at the ceiling. New joiners above the ceiling barred from EPS since the 1 Sep 2014 amendment. Employer PF sits inside CTC, never in monthly salary. |
| F5 | RBI defines the Interest-Free Credit Period as the time from the transaction date to the payment due date, in which payment is interest-free "subject to the payment of entire outstanding on or before the payment due date" | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13155 | 2026-10-19 | library:L-CC-INTEREST-FREE. RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025, RBI/DOR/2025-26/155, 28 Nov 2025, para 3 definitions (xvi). Cached brand/sources/rbi-cc-master-direction.html. CAUTION: RBI issued entity-wise 2025 directions (Commercial Banks, RBI/DOR/2025-26/155, 28 Nov 2025, page id=13155, "updated as on 1 Oct 2026"); I could NOT read their text (PDF behind a captcha), so I can't confirm the repeal wording or that clauses are unchanged. Keep claims general; no clause numbers on screen. RE-VERIFIED 2026-10-19 against the CURRENT text: RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025, RBI/DOR/2025-26/155, 28 Nov 2025, para 5(16). RBI PDF is captcha-gated; text read from the verbatim taxguru reproduction, cached brand/sources/rbi-cc-2025-cb-taxguru-fulltext.html. Replaces the 2022 Master Direction (withdrawn Dec 2025). Separate directions exist for UCBs/RRBs/NBFCs — same wording not verified there. (from 2026-10-credit-card-myth F1) |
| F6 | Minimum Amount Due is the least part of the bill a cardholder must pay "to not be treated as an overdue bill" — paying it is not the same as clearing the bill | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13155 | 2026-10-19 | library:L-CC-MIN-DUE. RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025, RBI/DOR/2025-26/155, 28 Nov 2025, para 5(17). RBI PDF is captcha-gated; text read from the verbatim taxguru reproduction, cached brand/sources/rbi-cc-2025-cb-taxguru-fulltext.html. Replaces the 2022 Master Direction (withdrawn Dec 2025). Separate directions exist for UCBs/RRBs/NBFCs — same wording not verified there. (from 2026-10-credit-card-myth F3) |
| F7 | Example: the 4 subscription autopays total ₹1,347 a month = ₹16,164 a year | computed from F1 | 2026-10-21 | 1,347 × 12. Say "agar chalte rahe"; the 4 apps are invented. |
| F8 | Example: ₹5,753 left ÷ 18 remaining days (13–30 Nov) ≈ ₹319 a day | computed from F1 | 2026-10-21 | 5,753/18 = 319.6; say "lagbhag ₹320". |
| F9 | Example: the five small items (food ₹3,600 + outing ₹4,100 + sale ₹3,200 + UPI ₹1,800 + subscriptions ₹1,347) = ₹14,047, about the same as rent+maid+wifi ₹14,000, i.e. a second rent | computed from F1 | 2026-10-21 | 3600+4100+3200+1800+1347 = 14047. Say "milke doosra rent" (approx., not exact). |

```
items: rent 14000 + cc 6200 + subs 1347 + food 3600 + outing 4100 + shopping 3200 + upi 1800 = 34247
left = 40000 - 34247 = 5753 ; /18 = 319.6 ; subs*12 = 16164
```

## Expert take
- myth: "Salary toh bahut thi, pata nahi kahan gayi" — lagta hai ek bada kharcha khaa gaya.
- so what: Koi ek bada kharcha nahi tha — 7 chhoti-chhoti leaks the, aur sabse sasti-dikhne wali (autopay) har mahine bina poochhe chalti hai; RBI rules mein tumhe debit se pehle notice aur opt-out milta hai, bas use dekhna padta hai. [F2][F3]
- in ₹: ₹40,000 mein se 12 din mein ₹34,247 gaye; baaki ₹5,753 = lagbhag ₹320 roz; sirf subscriptions ₹1,347 mahina = ₹16,164 saal. [F1][F7][F8]
- do: Is hafte UPI/bank SMS scroll karo, subscriptions ki list banao, jo use nahi hota uska autopay band karo.
- follow-up: "Autopay band kaise karte hain?" — RBI framework: debit se kam-se-kam 24 ghante pehle notification aana chahiye, aur customer kisi ek transaction ya poora e-mandate opt-out kar sakta hai (PIN/OTP-type check ke saath). [F2][F3]
- jargon: autopay/e-mandate = "tumhare account se apne-aap kat'ne ki permission"; interest-free period = "bill ki poori payment due date tak karo toh byaj nahi" [F5]; minimum due = "sirf overdue na kehlane ka least amount, bill clear nahi" [F6].

## Texture for the writers (not facts — don't put numbers from here on screen)
- 1 tareekh ko salary credit ka SMS, 12 tareekh ko "balance check karne ki himmat nahi" — Zomato-style order-ka-notification-flood, par brand naam nahi.
- Rent + ghar bhejna + "bhai ye mera hissa" UPI requests — dost group chat mein "baad mein de dunga".
- "Sale hai, bachat hai" logic: kharidne se paisa bachta hai (jo nahi bachta).
- Month-end pe maggi, chai aur "ghar ka khana yaad aa raha hai".
- Credit card ka bill 3rd ko aata hai aur salary ka kuch hissa pehle hi uska ho chuka hota hai (due-date wali tension). Don't claim every card's cycle.
- Subscriptions: "free trial" jo yaad nahi kab shuru hui.

## Culture now
Indian meme trackers I could reach (idiotic.media) have nothing newer than April 2026, so Indian image rows are NOT confirmed this month — writer should lean on Chillar reactions and the global rows below; do not invent Indian templates.
- M1 · image · "Why would I deceive you?" · deadpan denial face ("mere paas paisa hai, main kyun jhooth bolunga") — use for "balance theek hai" lie · peaked 2026-09 · https://imgflip.com/memesearch?q=Why+would+I+deceive+you
- M2 · image · "It's La Peace" · calm-after-chaos shrug for "ab kuch nahi bachta, toh tension bhi nahi" · peaked 2026-09 · https://imgflip.com/memesearch?q=It%27s+La+Peace
- M3 · sound · "FAAAH" · sharp comic fail sting at the "₹5,753 bache" reveal · peaked 2026-09 · https://www.myinstants.com/en/search/?name=FAAAH
- M4 · ref · "aura" / "aura farming" · Gen Z slang for coolness points — "salary ke saath aura bhi 12 tareekh tak khatam" · peaked 2026-09 · https://www.ypulse.com/newsfeed/2025/11/12/gen-z-is-planning-to-wipe-the-meme-slate-clean-in-2026/
- M5 · ref · "2026 is the new 2016" / meme reset · nostalgia-based, "2016 mein 40k bahut hote the" angle · peaked 2026-01 · https://www.ypulse.com/newsfeed/2025/11/12/gen-z-is-planning-to-wipe-the-meme-slate-clean-in-2026/

## Not usable (unverified)
- Any "average Indian spends X% on food delivery/subscriptions" statistic — no primary source checked.
- Real subscription prices / app names — brand names banned and not sourced.
