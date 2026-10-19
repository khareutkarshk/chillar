# Fact-check: 2026-10-12lpa-in-hand

checked: 2026-10-19 · tax year 2026-27 (Income-tax Act, 2025) · Labour Codes in force since 21 Nov 2025
fact_lint: ok (0 problems; warnings: F3/F5/F6 not cited, which is fine because they are texture or inputs to F9)
scenes/scenes.json: does not exist yet, so there was nothing to scan. Re-run this check on scenes.json params after /render plans the scenes.

**verdict: BLOCK** (2 rows: L6, L8)

## Line table

| line | claim as written | fact | status | fix |
|---|---|---|---|---|
| L2 | Mummy: "12 lakh ka offer, 1 lakh mahina!" (joke) | F9 | ✅ | None. This is the myth being debunked. ₹12,00,000 ÷ 12 = ₹1,00,000, and PIB 2098406 itself uses the phrase "average income of Rs.1 lakh per month". |
| L3 | Ek typical slip dekho. (+ tag "example: Maharashtra, new regime") | F9 | ✅ | None. The example framing arrives before the first figure. |
| L4 | CTC matlab Cost to Company. "Cash Tumhare Credit" nahi. (joke) + stamp "COST TO COMPANY" | F9 | ✅ | None. The line expands a standard HR term and carries no number. The fake expansion is obviously a gag and smuggles in no figure. Optional: F9 never defines CTC, so add "CTC = cost to company" to the F9 notes. |
| L6 | Pehla laddoo: company ka PF. Seedha retirement aur pension mein. + tag "Employer PF ₹66,600/saal → PF + pension (EPS)" | F4, F9 | ⚠ overstated + ⚠ source dead | (1) **"aur pension" / "PF + pension (EPS)" is wrong for this example.** Basic is ₹46,250/month, above the EPF wage ceiling (₹25,000 from 17 Sep 2026; F5). A member who joins with wages above the ceiling and was not already an EPS member is outside EPS, so the employer's full 12% goes to EPF. This has been EPS para 6 since the 1 Sep 2014 amendment, and it is unchanged by the Sep 2026 ceiling revision. An existing EPS member gets at most 8.33% × ₹25,000 = ₹2,083/month (PIB 2313829), not 8.33% of basic. Fix the line to "Seedha retirement fund mein." (or "Seedha PF account mein. Retirement wala.") and the tag to "Employer PF ₹66,600/saal → retirement (EPF)". (2) The F4 source https://www.epfindia.gov.in/site_en/FAQ.php now redirects (301) to epfo.gov.in/site_en/FAQ.php, which returns 404. Replace it with https://www.labour.gov.in/static/uploads/2025/06/93561f36d5094b0cfe52570b4e8d2dc1.pdf (MoLE/PIB: employee 12%, employer 12%) and https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829 (8.33% pension share, capped at ₹2,083/month). Rewrite the F4 claim to "employee 12%, employer 12%; for EPS members 8.33% of wages up to the ₹25,000 ceiling goes to pension (max ₹2,083/mo), the rest to EPF; members above the ceiling at joining are not in EPS, so the whole 12% goes to EPF". The F4 `checked` date of 2026-10-19 is not supported (the source is dead). Revert it, or re-date it once the URL is replaced. |
| L7 | Doosra: gratuity, 5 saal baad. Tum abhi se "open to work" ho. (joke) + tag "Gratuity ₹26,683/saal — after 5 yrs" | F7, F9 | ✅ | None. Code on Social Security s.53(1) says "continuous service for not less than five years". Explanation 3 gives monthly wage ÷ 26 × 15, so 5,55,000/12 ÷ 26 × 15 = 26,682.69 ≈ ₹26,683. The joke only implies "leave before 5 years and you don't get it", which s.53(1) supports for a regular employee. The exceptions (death or disablement, fixed-term pro rata after 1 year per PIB 21 Nov 2025 and CSS Central Rules) are not contradicted. No change to the 5-year rule for permanent employees in 2026. |
| L8 | Teesra: tumhara apna PF — tumhare naam pe, par locked. + visual "laddoos go into a locker with a padlock" + tags "Your PF ₹66,600/saal", "Prof. tax (Maharashtra) ₹2,500/saal" | F4, F8, F9 | ⚠ overstated (unsourced "locked") | None of F4, F8 or F9 says "locked". Since the EPFO CBT decision of 13 Oct 2025 (238th meeting), members can withdraw up to 100% of the *eligible* balance; 25% must stay as a minimum balance; the minimum service is 12 months for all partial withdrawals, with no reason needed under "special circumstances". The MoLE EPF note also confirms that withdrawals and advances exist. So a padlock that reads as permanent goes past the facts. Minimal fix: say "…tumhare naam pe, par **abhi** locked." That is true for a new joiner's first 12 months. Add a fact F10 (EPFO CBT 13 Oct 2025: partial withdrawal after 12 months' service, 25% minimum balance stays; primary: EPFO press brief "PressBrief_MOL&EChairs238thMeetingCBT_EPF_13102025.pdf", which currently 404s after the epfindia → epfo.gov.in move, so find its new URL or the PIB copy) and cite it. Keep the padlock but tag it "12 mahine" / "rules apply", never "never withdrawable". The numbers on this line are fine: ₹66,600 = 12% × 5,55,000 ✅. PT ₹2,500 = ₹200 × 11 + ₹300 (Feb), Schedule I entry 1, "1/4/2023 onwards", men > ₹10,000/mo and women > ₹25,000/mo ✅. |
| L9 | Sab Income Tax ko kos rahe the. Tax: ₹0. (joke) + stamp "TAX ₹0 · ALIBI" | F1, F2, F9 | ✅ | None. Re-computed below: taxable ₹10,31,717 ≤ ₹12,00,000, so slab tax ₹43,172 is fully rebated (s.156(2) cap ₹60,000), giving tax ₹0 and cess ₹0. Optional: add the ITA 2025 citation (s.202(1) table, s.156(2), s.19 Sl.2(a)) to F1/F2 next to the PIB 2025 release, since that release is from the 1961-Act Budget 2025-26. |
| L10 | Haath mein: ₹86,468 mahina. + odometer ₹1,00,000 → ₹86,468; 3 of 22 laddoos | F9 | ✅ | None. 10,37,617.31 / 12 = 86,468.11. The gap is 13.53%, and 3/22 = 13.64%, so the visual share is honest. If L6 changes, ₹86,468 does not change, because the EPS/EPF split has no effect on in-hand pay. |
| L11 | Ye mummy ko bhejo. Mithai wapas nahi hogi. (joke) | — | ✅ | None. No claim and no number. |

Non-spoken: cover.md stamp "₹86,468" matches F9 ✅. Cover text has no "example" qualifier. That is acceptable because frame 1 and L3 carry it, but don't add "your salary" wording anywhere.

## Fact-by-fact verification

| fact | source opened | result |
|---|---|---|
| F1 | PIB 2098406 (1 Feb 2025): slabs 0–4 nil · 4–8 5% · 8–12 10% · 12–16 15% · 16–20 20% · 20–24 25% · >24 30%. **Income-tax Act, 2025 (Gazette 21 Aug 2025) s.202(1) table gives the identical bands.** Budget 2026-27 summary (PIB, Feb 2026), Part B Direct Taxes: no change to personal slabs. Finance Bill 2026 (incometax.gov.in): only cl.47 amends s.202, omitting s.202(2)(a)(iii) (the s.144 reference). The rates in s.202(1) are untouched. I found no later 2026 change. | ✅ re-verified |
| F2 | PIB 2098406 quote ("no income tax payable upto income of Rs. 12 lakh … Rs.12.75 lakh for salaried … standard deduction of Rs. 75,000"). ITA 2025 **s.156(2)(a)**: rebate = 100% of tax or ₹60,000, whichever is less, if income ≤ ₹12 lakh; s.156(2)(b) provides marginal relief. **s.19(1) Table Sl.2(a)**: standard deduction ₹75,000 where tax is computed under s.202(1). Finance Bill 2026 does not amend s.19 or s.156. | ✅ re-verified |
| F3 | Budget 2026-27 summary: "Income tax Act, 2025 will come into effect from April 2026". | ✅ re-verified (not cited) |
| F4 | epfindia FAQ URL is now **404** (301 to epfo.gov.in, then 404). Substitute: MoLE/PIB EPF Scheme note gives employee 12% and employer 12% ✅. The 8.33%/3.67% split as stated omits the ceiling cap and the EPS-eligibility rule (see L6). | ⚠ source dead, claim incomplete. Not re-verified. |
| F5 | PIB 2313829 (23 Sep 2026): ceiling ₹15,000 → ₹25,000 effective 17 Sep 2026, S.O. 5109(E); EPS max ₹1,250 → ₹2,083/month. | ✅ re-verified (not cited) |
| F6 | PIB 2192463 (21 Nov 2025): codes effective 21 Nov 2025. CSS 2020 s.2(88) and first proviso: allowances above one-half of all remuneration are added back to wages. | ✅ re-verified (not cited). Caveat for F9: if the employer's PF contribution (exclusion (c)) counts toward "all remuneration", the example's exclusions (₹5,51,717 allowances + ₹66,600 employer PF = ₹6,18,317) exceed half of ₹11,73,317 by about ₹31,659, which would push wages and therefore PF up slightly. The provision is read both ways. The example is labelled "typical slip", so this does not block. Consider "basic ≈ 50%" → "basic ~50% (assumed structure)" in the F9 notes. |
| F7 | CSS 2020 s.53(1) 5-year rule; s.53(2) 15 days per completed year (or part over 6 months); Explanation 3 ÷26 ×15. PIB 21 Nov 2025: fixed-term employees get gratuity after 1 year. | ✅ re-verified |
| F8 | MahaGST "Rate Schedules under the Professions Tax Act, 1975" PDF (page updated 19/10/2026), Schedule I entry 1, "1/4/2023 onwards": ₹2,500 p.a. = ₹200/month, ₹300 in February. | ✅ re-verified |
| F9 | Re-computed independently (below). Every figure matches. Also checked: under s.202(2)(a)(iv) the new regime disallows the s.19 Sl.1 deduction (professional tax). F9 correctly does **not** subtract PT from taxable income, only from in-hand. | ✅ re-verified (math) |

## F9 re-computation
```
employer PF  = 0.12 × 5,55,000                 = 66,600
gratuity     = 5,55,000/12 ÷ 26 × 15           = 26,682.69 → 26,683
gross        = 12,00,000 − 66,600 − 26,682.69  = 11,06,717.31 → 11,06,717
taxable      = 11,06,717 − 75,000 (s.19)       = 10,31,717  ≤ 12,00,000 ✔
slab tax     = 0 + 20,000 + 10% × 2,31,717     = 43,172
rebate s.156(2)(a) = min(43,172, 60,000)       = 43,172  → tax 0, cess 4% × 0 = 0
in-hand      = 11,06,717 − 66,600 − 2,500      = 10,37,617/yr → 86,468.11/mo → ₹86,468
gap          = 1,00,000 − 86,468 = 13,532/mo (13.53%); 12,00,000 − 10,37,617 = 1,62,383/yr
```

## Blocking rows
1. **L6**: "Seedha retirement aur pension mein" / tag "PF + pension (EPS)". The example employee (basic ₹46,250/mo, above the ₹25,000 ceiling) is not in EPS as a new member, so the whole employer 12% goes to EPF. Change to "Seedha retirement fund mein." and the tag to "→ retirement (EPF)". Replace the dead F4 URL and fix the F4 wording.
2. **L8**: "par locked" plus the padlock locker has no fact behind it and is overstated after the Oct 2025 EPFO withdrawal liberalisation. Change to "par abhi locked", add an F10 for the 12-month / 25% minimum-balance rule, and keep the visual from implying "never".

## Sources opened
- PIB 2098406: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2098406&reg=48&lang=2
- PIB Budget 2026-27 summary: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf
- Income-tax Act, 2025 (Gazette CG-DL-E-22082025-265620; copy used): https://www.taxheal.com/wp-content/uploads/2025/08/income-Tax-Act-2025.pdf. ss.19, 156, 202. The incometaxindia.gov.in section pages returned 403.
- Finance Bill 2026: https://www.incometax.gov.in/iec/foportal/sites/default/files/2026-03/Finance_Bill.pdf
- Code on Social Security 2020: https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf
- PIB Labour Codes 21 Nov 2025: https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2192463&reg=48&lang=2
- PIB 2313829 (EPF ceiling ₹25,000): https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2
- MoLE EPF Scheme note: https://www.labour.gov.in/static/uploads/2025/06/93561f36d5094b0cfe52570b4e8d2dc1.pdf
- EPFO FAQ (dead): https://www.epfindia.gov.in/site_en/FAQ.php
- EPS eligibility above ceiling (secondary, 6 Oct 2026): https://www.angelone.in/news/personal-finance/eps-pension-epfo-mandates-membership-for-employees-earning-up-to-25-000
- EPFO CBT 238th meeting, 13 Oct 2025 (secondary): https://www.scconline.com/blog/post/2025/10/15/epfo-announced-100-percent-early-pf-withdrawal-reforms-238-cbt-meeting-update/
- MahaGST PT schedule: https://www.mahagst.gov.in/public/uploads/mvatservices/1761635767Rate%20Schedules%20under%20the%20Professions%20Tax%20Act,%201975%201.pdf


## Resolution (producer, 2026-10-19)
- L6 → "Seedha retirement fund mein.", tag "→ retirement fund (EPF)"; F4 re-sourced (MoLE EPF note) and reworded with the ceiling/EPS-joining rule.
- L8 → "par abhi locked" + F10 (CBT 13 Oct 2025, PIB 2178522); padlock tagged "12 mahine".
- verdict after fixes: PASS
