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
| F1 | EPFO statutory wage ceiling revised from ₹15,000 to ₹25,000 a month, effective 17 Sep 2026, by Gazette notification S.O. 5109(E) of the Ministry of Labour and Employment; first revision since September 2014 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2 | 2026-10-21 | PIB 23 Sep 2026: "revision of the statutory wage ceiling from Rs.15,000 to Rs.25,000 per month, effective September 17, 2026 … Gazette Notification S.O. 5109(E)". Effective 17 Sep, NOT 1 Oct: September payroll is split-period at many employers, so October is the first full month (our inference — say "pehla poora mahina", not "1 October se"). Gazette text itself not retrieved; PIB is the primary cite. |
| F6 | More than 51 lakh additional formal-sector workers in the ₹15,000–₹25,000 monthly wage range come under mandatory EPFO coverage (EPF, EPS and EDLI) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2 | 2026-10-21 | PIB 2313829: "more than 51 lakh additional formal sector workers in the Rs.15,000 - Rs.25,000 monthly wage range under mandatory EPFO coverage". EPFO regional office's expectation, say "lagbhag/expected". Who it hits: wage (basic+DA) 15–25k, not CTC or gross. |
| F7 | Worked example: maan lo basic wages ₹22,000. Employee 12% on the old ₹15,000 cap = ₹1,800; on full ₹22,000 = ₹2,640; extra deduction ₹840 a month, so in-hand falls by ₹840 | computed from F1, F2 | 2026-10-21 | ILLUSTRATIVE arithmetic: 12%×15,000=1,800; 12%×22,000=2,640; diff 840. Assumes the employer deducts on actual basic up to ₹25,000 (aksar). Max extra at ₹25,000 wages = 3,000−1,800 = ₹1,200. Some employers/employees were already paying on full basic — for them nothing changes. Employer's 12% sits in CTC, never in in-hand. |
| F8 | The 12% contribution rate is unchanged; only the wage it is calculated on (up to the ceiling) changed | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2 | 2026-10-21 | PIB mentions only the ceiling and the EPS cap change, no rate change; rate itself per F2. UNVERIFIED — do not use: G.S.R. 847(E) of 25 Sep 2026 (EPS amendment) and the EPFO FAQ's 1–16 Sep / 17 Sep split — seen only in secondary summaries / unreadable PDF. |
| F2 | EPF: employee pays 12% of basic wages (+DA); employer also pays 12%. For a new joiner above the EPF wage ceiling who is not already an EPS member, the employer's whole 12% goes to EPF (no pension share) | https://www.labour.gov.in/static/uploads/2025/06/93561f36d5094b0cfe52570b4e8d2dc1.pdf | 2026-10-19 | library:L-EPF-RATE. MoLE EPF Scheme note. 8.33% EPS share only for EPS members, capped at the ceiling. New joiners above the ceiling barred from EPS since the 1 Sep 2014 amendment. Employer PF sits inside CTC, never in monthly salary. |
| F3 | EPFO statutory wage ceiling raised from ₹15,000 to ₹25,000 a month, effective 17 Sep 2026 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2 | 2026-10-19 | library:L-EPF-CEILING. PIB 23 Sep 2026, Gazette S.O. 5109(E). Many employers still contribute 12% on full basic above the ceiling; some cap it — say "aksar/typically". |
| F4 | Of the employer's 12%, 8.33% goes to the Employees' Pension Scheme (EPS) for EPS members, calculated only on wages up to the ceiling: the maximum EPS share rises from ₹1,250 to ₹2,083 a month with the ₹25,000 ceiling (effective 17 Sep 2026); the rest of the 12% (3.67%) goes to EPF | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2313829&reg=48&lang=2 | 2026-10-19 | library:L-EPS-SHARE. PIB 2313829 (cached): "maximum employer pension contribution at 8.33% will rise from Rs.1,250 to Rs.2,083 per month". The 3.67% EPF remainder is arithmetic (12 − 8.33), not stated in the PIB text; EPFO FAQ https://pmvbry.epfindia.gov.in/faq-epfo/ says "The employer pays 12% out of which 8.33% is diverted to Pension Fund." Not true for our example: a new joiner above the ceiling is not an EPS member (see F2), so all 12% goes to EPF. ₹2,083 = 8.33% × ₹25,000, rounded. (from 2026-10-epf-explained F7) |
| F5 | Labour Codes in force from 21 Nov 2025; "wages" = basic + DA + retaining allowance, and allowances above one-half of total remuneration are added back into wages (the "50% basic" rule) | https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2192463&reg=48&lang=2 | 2026-10-19 | library:L-LABOUR-CODES-WAGES. Definition: Code on Social Security 2020 s.2(88) and proviso, https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf . Effect: basic ≈ half of pay → bigger PF → smaller monthly in-hand. |

```
basic 22,000 -> old cap 12% x 15,000 = 1,800 ; new 12% x 22,000 = 2,640 ; extra 840/month
max (basic 25,000): 3,000 - 1,800 = 1,200/month
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- First job, second or third salary: the offer letter said one number, the credit SMS says a smaller one, nobody in HR explains.
- The fresher friend's group chat: "bhai salary kam aayi, kuch kata kya?" → someone replies "PF hoga".
- PF feels like money vanishing into a government locker; the twist is it's your money, with interest, you just can't spend it on Diwali shopping.
- Salary-slip literacy is near zero: people read only net pay and CTC, never the "EPF" line in the middle.
- Diwali month makes it sting — gifting, EMI on the new phone, and the credit lands short.
- HR's answer is always "as per policy"; the reel is the explanation HR never gives.

## Culture now
Searches found no India-specific template dated Oct 2026 (only Mar 2026 / 2025 items, too old), so no Indian image rows are claimed — Chillar reactions carry the desi beats. Global rows from imgflip new & rising via memes.py (last 4 reels' memes excluded).
- M1 · image · "Why would I deceive you?" · deadpan fake-reassurance still; use for HR/employer saying it's all for your benefit · peaked 2026-09 · https://imgflip.com/memetemplates
- M2 · image · "Did you say POTENTIAL blank" · mock-excited repeat of a promised word ("did you say take-home?"); fits CTC vs in-hand · peaked 2026-09 · https://imgflip.com/memetemplates
- M3 · sound · "Sad Violin (the meme one)" · tiny-tragedy sting under a disappointing number · peaked 2026-10 · https://www.myinstants.com/
