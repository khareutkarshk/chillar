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
| F2 | Premature final settlement of EPF (job lost, no new job) now needs 12 months of unemployment instead of 2; final withdrawal of the EPS pension account now needs 36 months instead of 2. In case of unemployment 75% of the PF balance can be withdrawn immediately and the remaining 25% after one year | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2178522&reg=48&lang=2 | 2026-10-19 | library:L-EPF-UNEMPLOYMENT. 12 months / 36 months from the 238th CBT release; 75% now + 25% after one year from PIB 2179689 (https://www.pib.gov.in/PressReleasePage.aspx?PRID=2179689&reg=48&lang=2): "In case of unemployment, 75% PF balance ... can be withdrawn immediately. Remaining 25% can also be withdrawn after one year." Nuance: 12 months is for the full premature settlement; the 75% can come out sooner under partial withdrawal. Older EPFO FAQ still says 2 months — stale. (from 2026-10-epf-explained F10) |
| F3 | The whole PF balance (including the 25% minimum balance) can be withdrawn on retirement after 55, permanent disability, incapacity to work, retrenchment, voluntary retirement or leaving India permanently. EPS pension at 58 is unaffected, but a pension needs at least 10 years of EPS membership | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2179689&reg=48&lang=2 | 2026-10-19 | library:L-EPF-FULL-WITHDRAWAL. PIB 2179689 (cached): "Full withdrawal ... is also allowed in case of retirement after attaining 55 years of service, permanent disability, incapacity to work, retrenchment, voluntary retirement or leaving India permanently etc." Writers: the age for full PF withdrawal is 55 here, not 58 — 58 is the pension (EPS) age. Resigning is not on this list (that is the 12-month route in F10). (from 2026-10-epf-explained F11) |
| F4 | SEBI PR 70/2025 (8 Nov 2025): digital gold / e-gold products are neither notified as securities nor regulated as commodity derivatives and operate entirely outside SEBI's purview; none of the securities-market investor protection mechanisms are available; may expose investors to counterparty and operational risks | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | library:L-SEBI-DIGITALGOLD. p.1. Say "SEBI ke dayre ke bahar", not "illegal"; "may", not "will". No later SEBI action found (not exhaustive). (from 2026-11-04-digital-gold-sebi F1-F4) |
| F5 | Gratuity = 15 days' wages per completed year (monthly wage ÷ 26 × 15), paid only after 5 years of continuous service (fixed-term employees: pro rata, after 1 year) | https://www.labour.gov.in/static/uploads/2025/07/b0620548445580767b5c0d18c95c26f7.pdf | 2026-10-19 | library:L-GRATUITY. Code on Social Security 2020, s.53. ≈ 4.81% of annual basic; often shown inside CTC. |
| F1 | Worked example: a fresher whose essentials (rent, food, EMI, phone, travel) cost ₹25,000 a month needs 6 × ₹25,000 = ₹1,50,000 as a layoff fund; setting aside ₹10,000 a month builds it in 15 months | hypothetical — typical metro fresher with a shared flat; the 6-month size is a common rule of thumb, not a law | 2026-10-21 | Size by essentials, not salary. "6 months" is a planning rule of thumb with no regulatory source — say "ek rule of thumb", never "RBI/SEBI kehta hai". |
| F6 | Computed: 6 × ₹25,000 = ₹1,50,000; ₹1,50,000 ÷ ₹10,000 per month = 15 months; at ₹5,000 a month = 30 months | computed from F1 | 2026-10-21 | Arithmetic only. |

```
essentials/month = 25,000 ; 6 months = 1,50,000
at 10,000/month -> 15 months ; at 5,000/month -> 30 months
```

## Expert take
- myth: "Dhanteras pe sona kharidna hi shubh hai — wahi paisa safe hai." (gold = savings)
- so what: A layoff needs cash you can reach this week; PF is slow-locked — full settlement after job loss now needs 12 months of unemployment, only 75% can come out immediately [F2], and gratuity needs 5 years of service [F5]. Digital gold sits outside SEBI's purview [F4]. So the fresher's real safety net is a separate cash fund. [F2][F5][F4]
- in ₹: Maan lo essentials ₹25,000/month → ₹1,50,000 fund = 6 months; ₹10,000/month builds it in 15 months (₹1,20,000 saved in the first year). [F1][F6]
- do: This week: add up one month of essentials (rent, food, EMI, phone, travel) and set a ₹ auto-transfer on salary day to a separate account.
- follow-up: "PF to hai na, wahi se nikaal lenge?" — Not fully, not fast: 75% is allowed immediately on unemployment, the remaining 25% after a year, and full premature settlement needs 12 months of unemployment [F2]; full withdrawal is allowed straight away on retrenchment [F3].
- jargon: emergency fund = job gaye to bhi kiraya-khana chalane wala alag paisa; layoff/retrenchment = company ne nikaal diya; unemployment withdrawal = PF se job-gap ka paisa nikalna.

## Texture for the writers (not facts — don't put numbers from here on screen)
- Dhanteras group chats: "kuch khareedna hai" pressure, mummy asking whether a steel utensil counts.
- Freshers fear the "restructuring" email and Friday 5 pm calendar invites titled "Quick sync".
- Salary-day to 5th: money vanishes into rent, Swiggy, and "sirf aaj" EMIs.
- LinkedIn "open to work" green banner culture; friends posting "we're hiring" that never reply.
- Parents think PF is the safety net; the fresher knows notice period + joining-gap risk.
- Sending to the friend in a shaky job: warm, never preachy.

## Not usable (unverified)
- "Fresher hiring is down" — no 2026 primary release found (latest EPFO payroll data found was July 2025, and it shows rising 18-25 additions); keep it as a vibe ("hiring slow hai"), no number, no claim of a trend.
- "6 months of expenses is the right size" — rule of thumb, no primary source (only used as the hypothetical in F1).
- Savings-account / liquid-fund returns — not researched; don't mention.

## Culture now
- M1 · image · "Did you say POTENTIAL blank" · HR/boss says "potential" instead of a real offer; use for vague "growth opportunity" job talk · peaked 2026-09 · https://imgflip.com/memetemplates
- M2 · image · "Hera pheri Kya Gunda Banegare Tu" · Indian evergreen: dreams vs reality of a career; used for hopeless "plan" jokes (evergreen classic) · peaked 2026-10 · https://imgflip.com/memetemplates
- M3 · image · "Dekh raha hai na binod" · Indian evergreen: friend watching your mess unfold; for the friend who ignores the fund talk (evergreen classic) · peaked 2026-10 · https://imgflip.com/memetemplates
- M4 · sound · "Aayein Meme" · confused "aayein?" reaction after a shock line; use on a surprise number · peaked 2026-10 · https://www.myinstants.com
- M5 · ref · "Quick sync" · the dread calendar invite before layoffs, said not shown · peaked 2026-10 · https://www.reddit.com/r/developersIndia/
