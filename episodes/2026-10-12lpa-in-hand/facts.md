# Facts — 2026-10-12lpa-in-hand

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Primary sources only. Tax year 2026-27 (1 Apr 2026 – 31 Mar 2027), new tax regime (the default).

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | New regime slabs: ₹0–4 lakh nil · 4–8 lakh 5% · 8–12 lakh 10% · 12–16 lakh 15% · 16–20 lakh 20% · 20–24 lakh 25% · above 24 lakh 30% | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | PIB, Budget 2025-26 (1 Feb 2025). Union Budget 2026-27 summary (PIB, Feb 2026: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf) lists no change to personal slabs, so these continue for tax year 2026-27. |
| F2 | No income tax up to ₹12 lakh income under the new regime (rebate); limit is ₹12.75 lakh for salaried because of the ₹75,000 standard deduction | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | FM quote in the PIB release. Not for special-rate income (capital gains). Rebate is ₹60,000 (incometax.gov.in ITR FAQ). It's a rebate, not an exemption: just above ₹12 lakh it drops away (marginal relief applies). |
| F3 | The Income-tax Act, 2025 replaced the 1961 Act from April 2026 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf | 2026-10-19 | PIB Budget 2026-27 summary: "Income tax Act, 2025 will come into effect from April 2026". Optional texture — not needed for the math. |
| F4 | EPF: employee pays 12% of basic wages (+DA); employer also pays 12%. For a new joiner whose wages are above the EPF wage ceiling (₹25,000/month from 17 Sep 2026) and who is not already an EPS member, the employer's whole 12% goes to EPF (no pension share) | https://www.labour.gov.in/static/uploads/2025/06/93561f36d5094b0cfe52570b4e8d2dc1.pdf | 2026-10-19 | MoLE EPF Scheme note (12%/12%; 8.33% EPS share only for EPS members, capped at the ceiling). Ceiling: PIB 2313829 (F5). EPS membership above the ceiling barred for new joiners since 1 Sep 2014 amendment. The example's basic (₹46,250/month) is above the ceiling → employer PF = retirement fund (EPF). Employer PF sits inside CTC, never in the monthly salary. |
| F5 | EPFO statutory wage ceiling raised from ₹15,000 to ₹25,000 a month, effective 17 Sep 2026 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2 | 2026-10-19 | PIB, 23 Sep 2026, Gazette S.O. 5109(E). Many employers still contribute 12% on full basic above the ceiling (as in our example); some cap it — state "aksar/typically". |
| F6 | Labour Codes in force from 21 Nov 2025; "wages" = basic + DA + retaining allowance, and allowances above one-half of total remuneration are added back into wages (the "50% basic" rule) | https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2192463&reg=48&lang=2 | 2026-10-19 | PIB 21 Nov 2025 (codes effective). Definition: Code on Social Security 2020 s.2(88) and proviso, https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf . Effect: basic ≈ half of pay → PF (12% of basic) is bigger → monthly in-hand smaller. |
| F7 | Gratuity = 15 days' wages per completed year (monthly wage ÷ 26 × 15), paid only after 5 years of continuous service (fixed-term employees: pro rata, after 1 year) | https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf | 2026-10-19 | Code on Social Security 2020, s.53 (lines: "dividing the monthly rate of wages last drawn by him by twenty-six and multiplying the quotient by fifteen"; "continuous service for not less than five years"). ≈ 4.81% of annual basic; often shown inside CTC. |
| F8 | Maharashtra professional tax for salaried earning above the threshold: ₹2,500 a year (₹200/month, ₹300 in February) | https://www.mahagst.gov.in/en/profession-tax-and-other-rate-schedule | 2026-10-19 | MahaGST rate schedule (Schedule I, entry 1). Varies by state; example uses Maharashtra. |
| F9 | Worked example (₹12,00,000 CTC, Maharashtra, new regime, tax year 2026-27): basic ₹5,55,000 (≈50% of pay) · employer PF ₹66,600 · gratuity accrual ₹26,683 · gross salary ₹11,06,717 · employee PF ₹66,600 · professional tax ₹2,500 · taxable ₹10,31,717 → income tax ₹0 · in-hand ₹10,37,617/yr = **≈ ₹86,468/month** · gap vs "₹1 lakh/month" ≈ ₹13,532/month (₹1,62,383/yr) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | Computed from F1, F2, F4, F6, F7, F8 (script in notes below). An EXAMPLE structure — real CTCs vary (variable pay, insurance, meal cards, PF capped at ceiling). Say "ek typical slip", never "your salary". |
| F10 | EPF partial withdrawal: up to 100% of the eligible PF balance (employee + employer share) after a minimum 12 months' service, with 25% kept as a minimum balance (CBT, 13 Oct 2025) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2178522&reg=48&lang=2 | 2026-10-19 | 238th CBT meeting. So a new joiner's PF is "abhi locked" (first year), not locked forever — never show a permanent lock. Clarification: PIB 2179689. |

## Worked example (reproducible)
```
CTC 12,00,000 · basic 5,55,000 (50.1% of gross, F6)
employer PF  = 12% × 5,55,000          = 66,600   (F4)  ← in CTC, not in salary
gratuity     = 5,55,000/12 ÷ 26 × 15   = 26,683   (F7)  ← in CTC, paid after 5 yrs
gross        = 12,00,000 − 66,600 − 26,683 = 11,06,717
employee PF  = 12% × 5,55,000          = 66,600   (F4)
prof. tax    = 2,500                              (F8)
taxable      = 11,06,717 − 75,000      = 10,31,717 ≤ 12,00,000 → tax 0 (F1, F2)
in-hand      = 11,06,717 − 66,600 − 2,500 = 10,37,617 / yr ≈ 86,468 / month
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- Offer letters say "CTC"; HR calls and parents' WhatsApp calls say "12 lakh!". Relatives hear "1 lakh mahina".
- First payslip day: the ₹86k credit SMS vs the ₹1 lakh you already "spent" in your head (rent, EMI, trip).
- Gratuity is money "for the version of you who survives 5 years in this company".
- Employer PF + your PF both go to the PF account — real money, just locked; it's savings, not a scam.
- Tax isn't the villain this time: at 12 LPA under the new regime, income tax is zero.
