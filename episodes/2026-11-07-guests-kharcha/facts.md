# Facts — guests-kharcha

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.
Two rows may go without a URL (CLAUDE.md §3): an invented scenario — source `hypothetical — <why realistic>` — and
arithmetic on other rows — source `computed from F1, F2`. Start an example row's claim with `Example:` /
`Worked example:` / `ILLUSTRATIVE`; the script must frame it as one ("maan lo", "ek typical …", a first-person
story) the first time it's said — fact_lint blocks an unframed first use.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | Example: a host family spends ₹100 per guest per visit (chai, namkeen, mithai) on 40 guests, every day for 5 days of Diwali | hypothetical — a typical open-house Diwali; ₹100 is a chai-plus-snack plate, 40 is relatives plus mohalla | 2026-10-21 | Invented scenario: script must say "maan lo". Not a survey average; don't say "families spend". |
| F2 | Worked example: ₹100 × 40 guests = ₹4,000 per day | computed from F1 | 2026-10-21 | python: 100*40 = 4000 |
| F3 | Worked example: ₹100 × 40 guests × 5 days = ₹20,000 for Diwali week (₹4,000 a day × 5) | computed from F1 | 2026-10-21 | python: 4000*5 = 20000. Assumes all 40 come every day (upper end); say "agar sab roz aaye". |
| F4 | GST on dried nuts (HSN 0802) and dried fruit/nut mixtures (HSN 0813) cut from 12% to 5%; pre-packaged labelled namkeen/bhujia/mixture (HSN 2106 90) 12% → 5%; effective 22 Sep 2025 (56th GST Council) | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2163555&reg=48&lang=2 | 2026-10-21 | library:L-GST-NUTS-CUT. PIB recommendations table rows 0802/0813/2106 90 and date. Cashew-specific and kaju katli/mithai rate not named — don't state it. Namkeen only pre-packaged and labelled. |

```
python: per_day = 100*40 = 4000 ; five_days = 4000*5 = 20000
```

## Expert take
- myth: "Sirf ₹100 ka chai-nashta hai, guest toh bhagwan hai, kya hi kharcha." [F1]
- so what: ₹100 is small only once; times headcount and days it becomes ₹4,000 a day and ₹20,000 for the week — a real budget line, not a "chhota kharcha". [F2, F3]
- in ₹: ₹4,000 per day, ₹20,000 for 5 days, if all 40 come daily (upper end of this made-up case). [F3]
- do: this week, write the guest list, set a per-guest plate cost, multiply by days, and fix the hosting number before shopping, not after.
- follow-up: "Sab 40 roz aate hain kya?" — No; the example is the upper end, so ₹20,000 is a ceiling here, not a prediction. [F1, F3] Packaged namkeen and dried nuts also carry 5% GST now, not 12%. [F4]
- jargon: GST → tax added to the shelf price; per head → per person; budget → pehle se tay kiya hua kharcha limit.

## Not usable (unverified)
- Average Indian household's Diwali hosting spend (no primary source; only private polls).
- Kaju katli / mithai per-kg price or GST rate (not named in PIB).

## Texture for the writers (not facts — don't put numbers from here on screen)
- Mummy's "bas chai hi toh hai" while the biscuit tin, namkeen and mithai box empty in 40 minutes.
- Guests who say "arre kuch nahi lenge" and then eat three kaju katli.
- Soan papdi box regifted in a loop; the host quietly knows which box it is.
- The aunt who counts plates like a scorecard; the kid sent to the shop for "dahi aur cold drink, jaldi".
- Dad insisting "Diwali ka budget alag hota hai" while the snack bill outgrows the electricity bill.

## Culture now
- M1 · image · "Did you say POTENTIAL blank" · pitch that sounds bigger than it is; caption a naive claim, then the reveal · peaked 2026-09 · https://imgflip.com/memesearch?q=Did+you+say+POTENTIAL
- M2 · image · "Why would I deceive you?" · deadpan denial of an obvious trap, fits "bas ₹100 hi toh hai" · peaked 2026-09 · https://imgflip.com/memesearch?q=Why+would+I+deceive+you
- M3 · image · "Bas karo bhai" · Indian image, the "enough now" plea when a bill keeps climbing; evergreen · peaked 2021-01 (evergreen) · https://imgflip.com/memesearch?q=Bas+karo+bhai
- M4 · image · "Bahar bohot khatarnak log hain" · Indian image, dramatic "outside is dangerous" for guests at the door; evergreen · peaked 2021-06 (evergreen) · https://imgflip.com/memesearch?q=Bahar+bohot+khatarnak+log+hain
- M5 · ref · "2026 is the new 2016" · caption trend of 2016 nostalgia and the "Great Meme Reset"; say it as a joke about "purane Diwali" · peaked 2026-01 · https://www.ypulse.com/newsfeed/2025/11/12/gen-z-is-planning-to-wipe-the-meme-slate-clean-in-2026/
