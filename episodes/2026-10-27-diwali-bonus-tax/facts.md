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
| F1 | Salary due from an employer in the tax year, or paid in it, is taxed under the head "Salaries" (section 15, Income-tax Act 2025) | https://www.incometaxindia.gov.in/w/section-15-223 | 2026-10-21 | Official page returned 403 to fetch; wording seen only as a search snippet of that page. Section 15 does not name "bonus" — say "bonus salary jaisa hi taxable hai", not a statute quote. No separate exemption for a cash bonus found. |
| F2 | New regime slabs: ₹0–4 lakh nil · 4–8 lakh 5% · 8–12 lakh 10% · 12–16 lakh 15% · 16–20 lakh 20% · 20–24 lakh 25% · above 24 lakh 30% | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | library:L-TAX-SLABS. PIB, Budget 2025-26 (1 Feb 2025). Budget 2026-27 summary (https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf) lists no change to personal slabs → valid for tax year 2026-27. |
| F3 | No income tax up to ₹12 lakh income under the new regime (rebate); ₹12.75 lakh for salaried because of the ₹75,000 standard deduction | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | library:L-TAX-REBATE. Not for special-rate income (capital gains). Rebate ₹60,000 (incometax.gov.in ITR FAQ). A rebate, not an exemption: marginal relief just above ₹12 lakh. |
| F4 | Standard deduction for salaried under the new regime: ₹75,000 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2 | 2026-10-19 | library:L-STD-DEDUCTION. Same PIB release (FM quote: ₹12.75 lakh for salaried). |
| F5 | The Income-tax Act, 2025 replaced the 1961 Act from April 2026 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf | 2026-10-19 | library:L-IT-ACT-2025. PIB Budget 2026-27 summary: "Income tax Act, 2025 will come into effect from April 2026". |
| F6 | Employer must deduct TDS on salary at the time of payment; for tax year 2026-27 under section 392(1) of the new Act, resetting the TDS computation from 1 April 2026 using projected income, deductions and tax regime | https://www.incometax.gov.in/iec/foportal/help/all-topics/e-filing-services/%20tds%20compliance-faq | 2026-10-21 | FAQ 19–20. Dept: "no change in policy" vs old s.192. TDS is the employer's projection-based withholding, not the final tax (settled in your ITR). FAQ does NOT say "average rate" or "may differ" — that is script framing of "projected". |
| F7 | TDS on salary is at the average rate on estimated annual income (s.392(1) / old s.192(1)) | https://www.incometaxindia.gov.in/w/section-392-5 | 2026-10-21 | UNVERIFIED — do not use: official page blocked (403); only secondary sites/snippet. Say "employer poore saal ka andaaza lagake kaatta hai" (supported by F6). |
| F8 | Employer gifts/vouchers count as nil perquisite if total ≤ ₹15,000 in the tax year (was ₹5,000); cash gifts fully taxable as salary | https://kpmg.com/xx/en/our-insights/gms-flash-alert/2026/flash-alert-2026-081.html | 2026-10-21 | UNVERIFIED — do not use: KPMG only (Income-tax Rules 2026, notified 20 Mar 2026); CBDT/PIB text not retrievable. |
| F9 | Worked example: assume new regime, salary ₹15,00,000 a year, Diwali bonus ₹1,00,000, only the ₹75,000 standard deduction, no other income/deductions, 4% cess ignored. Tax without bonus ₹93,750; with bonus ₹1,08,750; extra tax ₹15,000 (bonus sits in the 15% slab); about ₹85,000 of the ₹1,00,000 stays | hypothetical — invented salary/bonus, realistic mid-level metro pay; tax computed from F2, F4 | 2026-10-21 | Script must frame as "maan lo". 4% cess is real but not in our verified rows → true figure ≈ ₹84,400, so say "lagbhag". Bonus-month TDS may be higher/lower than ₹15,000; squared up by year-end/ITR. |
| F10 | Worked example: assume salary ₹9,00,000 + ₹50,000 bonus, new regime: taxable ₹8,75,000 after ₹75,000 deduction, slab tax ₹27,500 fully cancelled by the rebate → ₹0 tax on that bonus | hypothetical — invented salary; computed from F2, F3, F4 | 2026-10-21 | Shows "not one flat rate for everyone". Optional contrast line. Rebate ₹60,000 > ₹27,500 (F3). |

```
# python check (F2 slabs, F4 std deduction, no cess)
salary 15,00,000: taxable 14,25,000 -> tax 93,750
salary+bonus 16,00,000: taxable 15,25,000 -> tax 1,08,750 ; difference 15,000 ; bonus kept 85,000
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- Bonus mail lands, group chat goes "party kab", then the credit alert: "bhai ye kaat kaun raha hai?"
- Everyone spends the bonus (phone, Goa, parents' gift) before it's credited; the credited amount is the villain's origin story.
- "30% katega" is canteen folklore; everyone's slab differs and nobody has opened their own Form 16.
- HR's "TDS applicable" line, the Diwali hamper of dry fruit nobody asked for, mithai box vs actual cash.
- Lower credit → "company ne bonus kaat liya" — actually your own tax withheld; the ITR sorts the rest.

## Culture now
- M1 · image · "Peak Life Events" · new imgflip template (≈2 months): bland milestone vs absurd "peak" event; use for "peak: bonus aaya, TDS bhi aaya" · peaked 2026-08 · https://imgflip.com/meme/Peak-Life-Events
- M2 · image · "paisa laya" · Indian reaction template, demanding money; old but still evergreen desi (the one classic) · peaked 2019-12 · https://imgflip.com/meme/paisa-laya
- M3 · image · "Dekh raha hai na binod" · Indian evergreen "noticing the outrage" — payslip vs promised bonus · peaked 2020-06 · https://imgflip.com/meme/Dekh-raha-hai-na-binod
