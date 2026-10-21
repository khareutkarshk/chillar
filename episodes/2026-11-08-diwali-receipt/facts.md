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
| F1 | Worked example: dry-fruit gift box priced ₹2,000 before tax, GST 5% = ₹100 (bill ₹2,100); gold jewellery priced ₹50,000 before tax (gold + making together), GST 3% = ₹1,500 (bill ₹51,500); total GST on the two = ₹1,600 | hypothetical — a typical Diwali gift box and a small jewellery buy; computed from F2, F3 | 2026-10-21 | Pre-tax prices invented. Dry-fruit rate per F2 covers dried nuts/mixtures only, not mithai. |
| F2 | GST on dried nuts (HSN 0802) and dried fruit/nut mixtures (HSN 0813) cut from 12% to 5%; pre-packaged labelled namkeen/bhujia/mixture (HSN 2106 90) 12% → 5%; new rates effective 22 Sep 2025 (56th GST Council) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2163555&reg=48&lang=2 | 2026-10-21 | library:L-GST-NUTS-CUT. PIB recommendations table rows 0802/0813/2106 90 and implementation date. Cashew-specific and kaju katli/mithai rate not named — don't state it. Namkeen only pre-packaged and labelled. (from 2026-10-29-diwali-gifting-maths F1-F3) |
| F3 | GST on gold jewellery is 3% of the total transaction value (gold + making charges together; since 01.07.2017); the 5% rate is only a registered job worker's charge on job charges, not the retail buyer's bill | https://gstcouncil.gov.in/sites/default/files/2024-02/sectoral-fq-gems-jewellery.pdf | 2026-10-21 | library:L-GST-GOLD-JEWELLERY. CBIC sectoral FAQ p.4, cached gst-gems-jewellery-faq.pdf.pdf. Many blogs wrongly say "5% on making" for buyers. (from 2026-11-03-gold-bill-decoded F1-F3) |
| F4 | GST on gold jewellery is 3% of the total transaction value, whether the making charge is shown separately or not | https://gstcouncil.gov.in/sites/default/files/2024-02/sectoral-fq-gems-jewellery.pdf | 2026-10-21 | library:L-GST-JEWELLERY. CBIC sectoral FAQ p.4. The 5% rate is only the registered job worker rate on job charges, not the retail bill. (from 2026-11-03-gold-bill-decoded F1/F2) |
| F5 | HUID is a six-digit alphanumeric code unique per hallmarked jewellery article, laser-marked; checkable via Verify HUID in the BIS Care app | https://services.bis.gov.in/php/BIS_2.0/BISBlog/?p=560 | 2026-10-21 | library:L-HUID. BIS blog (2022). Say six-character. Hallmarking mandatory only in notified districts. (from 2026-11-03-gold-bill-decoded F4/F5) |
| F6 | SEBI PR 70/2025 (8 Nov 2025): digital gold / e-gold products are neither notified as securities nor regulated as commodity derivatives and operate entirely outside SEBI's purview; none of the securities-market investor protection mechanisms are available; may expose investors to counterparty and operational risks | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | library:L-SEBI-DIGITALGOLD. p.1. Say "SEBI ke dayre ke bahar", not "illegal"; "may", not "will". No later SEBI action found (not exhaustive). (from 2026-11-04-digital-gold-sebi F1-F4) |
| F7 | RBI defines the Interest-Free Credit Period as the time from the transaction date to the payment due date, in which payment is interest-free "subject to the payment of entire outstanding on or before the payment due date" | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13155 | 2026-10-19 | library:L-CC-INTEREST-FREE. RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025, RBI/DOR/2025-26/155, 28 Nov 2025, para 3 definitions (xvi). Cached brand/sources/rbi-cc-master-direction.html. CAUTION: RBI issued entity-wise 2025 directions (Commercial Banks, RBI/DOR/2025-26/155, 28 Nov 2025, page id=13155, "updated as on 1 Oct 2026"); I could NOT read their text (PDF behind a captcha), so I can't confirm the repeal wording or that clauses are unchanged. Keep claims general; no clause numbers on screen. RE-VERIFIED 2026-10-19 against the CURRENT text: RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025, RBI/DOR/2025-26/155, 28 Nov 2025, para 5(16). RBI PDF is captcha-gated; text read from the verbatim taxguru reproduction, cached brand/sources/rbi-cc-2025-cb-taxguru-fulltext.html. Replaces the 2022 Master Direction (withdrawn Dec 2025). Separate directions exist for UCBs/RRBs/NBFCs — same wording not verified there. (from 2026-10-credit-card-myth F1) |
| F8 | Every billing statement must carry RBI's warning: making only the minimum payment every month would stretch repayment over months/years with compounded interest on the outstanding balance | https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=13155 | 2026-10-19 | library:L-CC-MIN-PAY-WARNING. RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025, RBI/DOR/2025-26/155, 28 Nov 2025, para as F4. Same CAUTION. RE-VERIFIED 2026-10-19 against the CURRENT text: RBI (Commercial Banks – Credit Cards and Debit Cards: Issuance and Conduct) Directions, 2025, RBI/DOR/2025-26/155, 28 Nov 2025, para 23(3) legend. RBI PDF is captcha-gated; text read from the verbatim taxguru reproduction, cached brand/sources/rbi-cc-2025-cb-taxguru-fulltext.html. Replaces the 2022 Master Direction (withdrawn Dec 2025). Separate directions exist for UCBs/RRBs/NBFCs — same wording not verified there. (from 2026-10-credit-card-myth F5) |
| F9 | Toll-free helpline 1930 is operational to get assistance in lodging online cyber complaints; NCRP is I4C's reporting platform | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095&reg=3&lang=1 | 2026-10-21 | library:L-CYBER-1930. Same PIB release. Say "1930" only. (from 2026-10-30-account-rent-mule F3) |

```
2000*0.05=100 ; 50000*0.03=1500 ; total 1600
```

## Not usable (unverified)
- Mithai/kaju katli GST rate — F2 doesn't name it; not checked.
- Any figure on Diwali spend totals or gold sales volume — no primary source read.

## Expert take
- myth: "Diwali ka bill = jitna dukaan ne bola, bas."
- so what: Har cheez ki receipt me GST alag line hai aur rate alag — dry fruit 5% [F2], gold jewellery 3% on gold + making dono [F3][F4]. Receipt padho = pata chalta hai paisa kahan gaya.
- in ₹: ₹2,000 ke dry-fruit box pe ₹100 GST, ₹50,000 ke gold pe ₹1,500 — Diwali pe ₹1,600 sirf tax [F1].
- do: Is Diwali har bill pe GST line dekho aur jewellery pe HUID code check karo [F5].
- follow-up: "Card se kharida to?" — due date tak poora bill bhara to interest-free [F7]; sirf minimum bharna lamba kheench deta hai [F8]. "Digital gold safe?" — SEBI ke dayre ke bahar, risk ho sakta hai [F6]. Scam ho to 1930 [F9].
- jargon: GST = bill me juda sarkari tax; HUID = jewellery pe laser-marked 6-character pehchaan code [F5]; minimum due = card ka sabse chhota hissa, baaki pe interest [F8].

## Texture for the writers (not facts — don't put numbers from here on screen)
- Mummy ka "bas ek box lena hai" jo teen box ban jaata hai; gift boxes ghoom-phir ke wapas ghar aate hain.
- Dhanteras pe gold/silver coin ki line; "ye toh pichle saal wala box hai" detection.
- "No cost EMI" sale-season; salary Diwali se pehle aati hai aur 15 din me gayab.
- Safai, rangoli, patakhe bahas, family WhatsApp group ki 40 "Shubh Deepawali" images.
- Bonus woh paisa hai jo aate hi gayab ho jaata hai.

## Culture now
- M1 · ref · "Diwali ki safai" · annual cleaning-ritual memes, "ghar saaf ya rishte?" jokes; say, don't show · peaked 2026-10 · https://www.ibtimes.co.in/diwalikisafai-trends-twitter-these-memes-are-proof-you-are-not-alone-annual-cleaning-ritual-853296
- M2 · ref · "Aura" · Gen Z slang "+1000 aura / -500 aura" for cool/uncool moves; say it as a receipt line · peaked 2026-09 · https://imgflip.com/memesearch?q=aura
- M3 · image · "Two Buttons" · classic choice-panic template; evergreen, fits sweets vs savings · peaked 2026-10 · https://imgflip.com/meme/Two-Buttons
- M4 · sound · "Sad Violin (the meme one)" · sad-violin sting after a painful total · peaked 2026-10 · https://www.myinstants.com/en/search/?name=sad+violin
