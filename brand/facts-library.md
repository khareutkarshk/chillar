# Facts library

Facts that recur across reels (tax slabs, EPF, gratuity, standard deduction…), each with a primary
source and the date it was last verified. New episodes copy entries from here instead of researching
from scratch:

    .venv/bin/python pipeline/facts_library.py copy episodes/<ep> L-TAX-SLABS L-EPF-RATE
    .venv/bin/python pipeline/facts_library.py stale        # entries that must be re-verified

**Re-verify an entry only when it is stale:** `checked` older than 90 days, or `changes` = `budget`
and a Union Budget (1 Feb) has passed since `checked`, or a new circular/notification on the topic
is known. When re-verified, update `checked` here (and in the episode). Primary sources only; source
PDFs are cached in `brand/sources/` (`facts_library.py cache <url>`) because government sites often
block automated fetches. Episode-specific numbers (worked examples) stay in the episode's facts.md.

`changes`: `budget` (Union Budget, 1 Feb) · `notification` (gazette/circular, any time) · `stable` (statute).

| id | claim | source | checked | changes | notes |
|----|-------|--------|---------|---------|-------|
| L-TAX-SLABS | New regime slabs: ₹0–4 lakh nil · 4–8 lakh 5% · 8–12 lakh 10% · 12–16 lakh 15% · 16–20 lakh 20% · 20–24 lakh 25% · above 24 lakh 30% | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | budget | PIB, Budget 2025-26 (1 Feb 2025). Budget 2026-27 summary (https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf) lists no change to personal slabs → valid for tax year 2026-27. |
| L-TAX-REBATE | No income tax up to ₹12 lakh income under the new regime (rebate); ₹12.75 lakh for salaried because of the ₹75,000 standard deduction | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | budget | Not for special-rate income (capital gains). Rebate ₹60,000 (incometax.gov.in ITR FAQ). A rebate, not an exemption: marginal relief just above ₹12 lakh. |
| L-STD-DEDUCTION | Standard deduction for salaried under the new regime: ₹75,000 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | budget | Same PIB release (FM quote: ₹12.75 lakh for salaried). |
| L-IT-ACT-2025 | The Income-tax Act, 2025 replaced the 1961 Act from April 2026 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf | 2026-10-19 | stable | PIB Budget 2026-27 summary: "Income tax Act, 2025 will come into effect from April 2026". |
| L-EPF-RATE | EPF: employee pays 12% of basic wages (+DA); employer also pays 12%. For a new joiner above the EPF wage ceiling who is not already an EPS member, the employer's whole 12% goes to EPF (no pension share) | https://www.labour.gov.in/static/uploads/2025/06/93561f36d5094b0cfe52570b4e8d2dc1.pdf | 2026-10-19 | notification | MoLE EPF Scheme note. 8.33% EPS share only for EPS members, capped at the ceiling. New joiners above the ceiling barred from EPS since the 1 Sep 2014 amendment. Employer PF sits inside CTC, never in monthly salary. |
| L-EPF-CEILING | EPFO statutory wage ceiling raised from ₹15,000 to ₹25,000 a month, effective 17 Sep 2026 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2 | 2026-10-19 | notification | PIB 23 Sep 2026, Gazette S.O. 5109(E). Many employers still contribute 12% on full basic above the ceiling; some cap it — say "aksar/typically". |
| L-EPF-WITHDRAWAL | EPF partial withdrawal: up to 100% of the eligible balance (employee + employer share) after 12 months' service, with 25% kept as a minimum balance (CBT, 13 Oct 2025) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2178522&reg=48&lang=2 | 2026-10-19 | notification | 238th CBT meeting; clarification PIB 2179689. A new joiner's PF is "abhi locked" (first year), never locked forever. |
| L-LABOUR-CODES-WAGES | Labour Codes in force from 21 Nov 2025; "wages" = basic + DA + retaining allowance, and allowances above one-half of total remuneration are added back into wages (the "50% basic" rule) | https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2192463&reg=48&lang=2 | 2026-10-19 | notification | Definition: Code on Social Security 2020 s.2(88) and proviso, https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf . Effect: basic ≈ half of pay → bigger PF → smaller monthly in-hand. |
| L-GRATUITY | Gratuity = 15 days' wages per completed year (monthly wage ÷ 26 × 15), paid only after 5 years of continuous service (fixed-term employees: pro rata, after 1 year) | https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf | 2026-10-19 | stable | Code on Social Security 2020, s.53. ≈ 4.81% of annual basic; often shown inside CTC. |
| L-PT-MAHARASHTRA | Maharashtra professional tax for salaried above the threshold: ₹2,500 a year (₹200/month, ₹300 in February) | https://www.mahagst.gov.in/en/profession-tax-and-other-rate-schedule | 2026-10-19 | notification | MahaGST rate schedule, Schedule I entry 1. Varies by state. |
