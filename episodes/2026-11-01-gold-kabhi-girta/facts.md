# Facts — 2026-11-01-gold-kabhi-girta

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.
Two rows may go without a URL (CLAUDE.md §3): an invented scenario — source `hypothetical — <why realistic>` — and
arithmetic on other rows — source `computed from F1, F2`. Start an example row's claim with `Example:` /
`Worked example:` / `ILLUSTRATIVE`; the script must frame it as one ("maan lo", "ek typical …", a first-person
story) the first time it's said — fact_lint blocks an unframed first use.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | RBI set the SGB issue price for Series III (subscription 24 Oct–2 Nov 2016) at a nominal value of ₹3,007 per gram of 999-purity gold, the simple average of IBJA closing prices for 17–21 Oct 2016 (issue price ₹2,957 after a ₹50 discount) | https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=38377 | 2026-10-21 | RBI PR 21 Oct 2016, read directly. Use ₹3,007 (the gold price), not ₹2,957 (a bond discount). It is the IBJA 999 bullion rate, so a jeweller's price (making charges, GST) is higher. |
| F2 | RBI set the premature-redemption price for SGB 2019-20 Series V due 15 Oct 2026 at ₹14,725 per unit, the simple average of IBJA 999-gold closing prices for 12, 13 and 14 Oct 2026 | https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63807 | 2026-10-21 | RBI PR 14 Oct 2026, read directly. "Per unit" = per gram (F3). Say "RBI ke hisaab se ~₹14,700 per gram (IBJA average)", not "retail price". |
| F3 | An SGB is denominated in units of one gram of gold (so "per unit" in RBI redemption releases means per gram) | https://website.rbi.org.in/web/rbi/-/citizens-corner/sovereign-gold-bond-scheme-2495 | 2026-10-21 | RBI scheme circulars 2015–2018: "denominated in units of one gram of gold and multiples thereof" (found via search, citizens' corner page not opened). The redemption releases themselves do not say "gram"; the 2016 issue releases (F1, F7) say per gram. |
| F4 | RBI redemption price for SGB 2020-21 Series VI due 7 Sep 2026 was ₹15,384 per unit (IBJA 999 average for 3, 4, 7 Sep 2026) | https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63538 | 2026-10-21 | RBI PR 7 Sep 2026, read directly. |
| F5 | RBI redemption price for SGB 2020-21 Series VII due 19 Oct 2026 was ₹14,614 per unit (IBJA 999 average for 14, 15, 16 Oct 2026) | https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63822 | 2026-10-21 | RBI PR 16 Oct 2026, read directly. |
| F6 | Gold fell about 5% between the RBI's 7 Sep 2026 price (₹15,384) and 16 Oct 2026 price (₹14,614) per gram | computed from F4, F5 | 2026-10-21 | (15,384−14,614)/15,384 = 5.0%, about ₹770 per gram, over ~6 weeks, on IBJA 3-day averages. Say "lagbhag 5%", not "crash". |
| F7 | RBI SGB Series I 2016-17 price was ₹3,119 per gram (IBJA average 11–15 Jul 2016); Series IV nominal value was ₹2,943 per gram (Feb 2017), i.e. about 5.6% lower | https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=37518 | 2026-10-21 | Series I read directly (RBI PR 15 Jul 2016). Series IV (RBI PR 23 Feb 2017, nominal ₹2,943 before ₹50 discount) read directly at https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=39663. (3,119−2,943)/3,119 = 5.6%, ~7 months, weekly IBJA averages, not a trough. |
| F8 | Worked example: a fresher's take-home in 2016 ≈ ₹20,000/month | hypothetical — a typical entry-level in-hand around 2016, a round number; not from a survey | 2026-10-21 | Script must say "maan lo". |
| F9 | Worked example: a fresher's take-home now ≈ ₹30,000/month | hypothetical — a typical entry-level in-hand now, a round number; not from a survey | 2026-10-21 | "Maan lo"; don't call it the average fresher salary. |
| F10 | Worked example: 10 g of gold in Oct 2016 = ₹30,070 ≈ 1.5 months of a ₹20,000 salary | computed from F1, F8 | 2026-10-21 | 3,007×10 = 30,070; ÷20,000 = 1.50. |
| F11 | Worked example: 10 g of gold in Oct 2026 = ₹1,47,250 ≈ 4.9 months of a ₹30,000 salary | computed from F2, F3, F9 | 2026-10-21 | 14,725×10 = 1,47,250; ÷30,000 = 4.9. Per year: ₹3,60,000 salary, so 10 g ≈ 41% of a year's take-home. |
| F12 | Worked example: gold per gram is ~4.9× its Oct 2016 level (₹3,007 → ₹14,725) | computed from F1, F2 | 2026-10-21 | 14,725/3,007 = 4.90. Example on IBJA rates, not a promise it keeps rising; the salary example went 1.5× (F8→F9). |

```
10 g, Oct 2016: 3007*10 = ₹30,070 -> /20,000 = 1.5 months
10 g, Oct 2026: 14725*10 = ₹1,47,250 -> /30,000 = 4.9 months (41% of ₹3,60,000/yr)
price ratio 14725/3007 = 4.90x ; Sep7->Oct16 2026: 5.0% ; Jul2016->Feb2017: 5.6%
```

## Not usable (unverified)
- "Gold always rises over 10 years" / any forecast or long-run return: no primary source; don't claim.
- Retail/jeweller price on Dhanteras (making charges, GST): no primary source read; use IBJA/RBI figures and say so.
- Average fresher salary 2016 or now: no primary source read; F8, F9 are hypothetical.
- Gold's record high (~₹1.76 lakh per 10 g, 29 Jan 2026) and the 2013 fall: news only. Left out.
- Dhanteras 2026 date: not verified; don't state it.

## Expert take
- myth: "Sona kabhi girta nahi, Dhanteras pe lo, hamesha chadhta hai."
- so what: gold does fall. RBI's own prices dropped about 5% in six weeks this autumn [F6] and about 5.6% in seven months in 2016–17 [F7]; yet over ten years, 10 g went from about 1.5 months of a maan-lo fresher's pay to about 4.9 months [F10, F11], with the price ~4.9× [F12]. So it falls, and it can still be far above where it was.
- in ₹: 10 g ≈ ₹30,070 in 2016, ≈ ₹1,47,250 now [F10, F11]; on a maan-lo ₹30,000 salary that's about 4.9 months, around 41% of a year's take-home [F11].
- do: before Dhanteras, check the day's IBJA 999 rate and ask the jeweller to split the bill into gold value, making charge and GST.
- follow-up: "Toh abhi girne pe lena chahiye?" Nobody can say: it moved ~5% in six weeks and ~5.6% in 2016–17 [F6, F7]; the reel gives no buy/sell advice.
- jargon: IBJA = jewellers' association that publishes the daily gold rate [F1]; 999 purity = 24-carat; making charge = the jeweller's fee on top; SGB per unit = per gram [F3].

## Texture for the writers (not facts — don't put numbers from here on screen)
- Dhanteras = "kuch sone ka lena shubh hai" pressure; mummy/dadi: "chhota sa hi le lo".
- "Sona kabhi nahi girta" is a wedding-uncle WhatsApp-forward; every family has one.
- Fresher first-salary fantasy: "pehli salary mein mummy ko ek ring", then the gram rate.
- Jeweller shop vibes: the tray, the little scale, "aaj ka rate" board, making charges nobody asks about.
- Gen Z measures price in months of salary or phones, not in "returns".

## Culture now
Web search for this month's Indian/global trends came back thin; nothing below is confirmed as peaking this week. M1–M2 are Indian evergreen classics (≤ 2 allowed); M3–M4 come from imgflip's new-and-rising list (≈ 1–2 months old) and exist in `memes.py`. None was used in the last 4 reels.
- M1 · image · "Maal kidhar hai" · Hera Pheri: Indian "where's the money/gold?" reaction · peaked 2019-01 (evergreen) · https://imgflip.com/memesearch?q=Maal+kidhar+hai
- M2 · image · "Rasode me kaun tha" · Indian "who did this?" mystery reaction · peaked 2020-10 (evergreen) · https://imgflip.com/memesearch?q=Rasode+me+kaun+tha
- M3 · image · "Aura Farming" · global: gaining/losing status; "aura gaya" for a price drop · peaked 2026-09 · https://imgflip.com/memesearch?q=Aura+Farming
- M4 · ref · "Somebody get these beggars out of here" · Odyssey line, said when someone's too broke for a rich place (jeweller's shop) · peaked 2026-08 · https://imgflip.com/memesearch?q=beggars
