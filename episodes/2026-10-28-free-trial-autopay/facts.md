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
| F1 | RBI's Digital Payments – E-mandate Framework, 2026 (21 Apr 2026, effective immediately) covers recurring payments on cards, PPIs and UPI | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374 | 2026-10-21 | RBI/CO.DPSS.POLC.No.S56/02.14.003/2026-27. Cached brand/sources/rbi-emandate-2026.html. |
| F2 | The issuer (your bank/app) must send a pre-debit notification at least 24 hours before the actual debit | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374 | 2026-10-21 | Excerpt: "An issuer shall send a pre-transaction notification to the customer, at least 24 hours prior to the actual charge / debit." FASTag/NCMC auto-replenish mandates are exempt — don't say "every" autopay. |
| F3 | The notice must show merchant name, amount, date and time of debit, reference numbers and the reason for the debit | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374 | 2026-10-21 | Excerpt: "at the minimum, inform the customer about the merchant's name, transaction amount, date and time of debit, reference number of transaction and e-mandate, reason for debit". |
| F4 | The customer must get a facility to opt out of any particular transaction or the whole e-mandate; the opt-out is validated with AFA (PIN/OTP-type extra check) and confirmed to the customer | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374 | 2026-10-21 | Excerpt: "facility to opt-out of any particular transaction or the e-mandate. Any such opt-out shall be validated by the issuer using AFA." |
| F5 | Recurring debits up to ₹15,000 per transaction can go through without extra authentication (AFA); above that they need AFA | https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13374 | 2026-10-21 | Excerpt: "All recurring transactions may be authorised without AFA up to ₹15,000/- per transaction." Separate higher limits apply to insurance premiums, mutual funds, credit card bills — not used; don't state the ₹1 lakh figure (sources conflict). |
| F6 | UPI AutoPay exists for recurring e-mandates: subscriptions, utility bills, insurance premiums, SIPs, EMIs | https://www.pib.gov.in/FactsheetDetails.aspx?id=150962&NoteId=150962&ModuleId=16&reg=48&lang=1 | 2026-10-21 | PIB UPI factsheet (via search summary; paraphrase only). |
| F7 | You can see a mandate's details under "Active mandates" in your UPI app and pause or revoke it anytime | https://www.npci.org.in/uploads/UPI_Auto_Pay_Brand_Guidelines_bcabed7282.pdf | 2026-10-21 | NPCI AutoPay brand guidelines (2020-era doc): "pause or revoke the mandate anytime". Menu names differ per app — say "Autopay / Mandates section", never name an app. Mandate lives at bank level: deleting the app doesn't cancel it (Mint-based reports; not primary → don't state as fact). |
| F8 | Reports (Mint, via Angel One, 23 Feb 2026) say RBI asked NPCI to examine a rise in UPI AutoPay complaints: wrong deductions and trouble cancelling mandates | https://www.angelone.in/news/market-updates/rbi-asks-npci-to-review-rise-in-upi-autopay-debit-complaints-report | 2026-10-21 | UNVERIFIED — do not use as flat fact. No RBI/NPCI release found. If used, only as "reports say"; no complaint numbers exist. Safer: lead with F2/F4 (the rules), skip the review. |
| F9 | Worked example: Typical: 6 free trials forgotten at ₹199 a month each = ₹1,194 a month, ₹14,328 a year | hypothetical — ₹199/month is a typical OTT/app subscription price; the count mirrors the send-to friend | 2026-10-21 | 6×199=1,194; ×12=14,328 (python). Script must frame it as "maan lo". |

```
6 x 199 = 1194 per month
1194 x 12 = 14328 per year
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- "7-day free trial" is signed up at 2 a.m. with the intention to cancel on day 6; day 6 never comes.
- The ₹1 / ₹2 mandate-setup debit looks harmless, so nobody reads the "autopay" screen.
- Bank SMS about a ₹199 debit gets swiped away like a spam message; it's lost among OTPs.
- Everyone has the friend who pays for a music, a video and a cloud-storage plan "just in case" and can't name all six.
- The "I'll cancel tomorrow" lie; the free trial that ended in March and still charges in October.
- Classic desi horror: finding out from the bank statement at month-end, in front of your parents' "Kitna kharcha kiya?" interrogation.

## Culture now
Search coverage this month was thin (no dated October roundups found); rows below are the freshest confirmed.
- M1 · image · "Waiting Skeleton" · skeleton waiting forever; use for "cancel kar dunga" on day 6 · peaked 2026-10 (evergreen classic, the one old-but-everywhere allowed) · https://imgflip.com/memetemplate/Waiting-Skeleton
- M2 · ref · "aura" / "farming aura" · slang for cool-points; "-1000 aura" for paying for 6 apps you don't use · peaked 2026-09 · https://www.ypulse.com/newsfeed/2025/11/12/gen-z-is-planning-to-wipe-the-meme-slate-clean-in-2026/
- M3 · ref · "2026 is the new 2016" · nostalgia meme; when subscriptions were one plan and zero mandates · peaked 2026-01 · https://latination.com/gen-z-trends-memes-viral-2026/
- M4 · ref · "Everyone knows I am a good girl" · Indian Gen Z protest-reel line; use as a deadpan self-defence ("main toh free trial pe tha") · peaked 2026-07 · https://www.dailypioneer.com/news/fits-slay-signs-say-memes-stay-gen-z-goes-lol-itical
