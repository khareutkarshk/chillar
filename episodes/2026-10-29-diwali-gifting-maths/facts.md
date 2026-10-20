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
| F1 | GST on dried nuts (almonds, pistachios etc., HSN 0802) and dried fruit/nut mixtures (HSN 0813) was cut from 12% to 5% by the 56th GST Council | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2163555&reg=48&lang=2 | 2026-10-21 | PIB recommendations table, HSN 0802 and 0813 rows: "12% → 5%". Cashew-specific and mithai/kaju katli rate NOT named in the table — don't say kaju katli's GST rate. |
| F2 | The new GST rates took effect from 22 September 2025 | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2163555&reg=48&lang=2 | 2026-10-21 | "Recommendation relating to date of implementation": "with effect from 22nd September 2025". So this is the second Diwali on the new rates. |
| F3 | Pre-packaged namkeen, bhujia, mixture (HSN 2106 90) GST went from 12% to 5% | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2163555&reg=48&lang=2 | 2026-10-21 | Only pre-packaged and labelled; loose/unbranded not covered in that row. |
| F4 | Worked example: one dabba of kaju katli costs ₹600 (assumed) | hypothetical — a 500 g box from a decent mithai shop is roughly this range | 2026-10-21 | Invented price; script must say "maan lo". Not a real shop's price. |
| F5 | Worked example: 30 households in the mohalla/family list | hypothetical — a joint-family + neighbours + office list this size is common | 2026-10-21 | Invented scenario. |
| F6 | Worked example: 30 dabbas x ₹600 = ₹18,000 | computed from F4, F5 | 2026-10-21 | python: 600*30 = 18000. |
| F7 | Worked example: a ₹12,000 gifting budget over 30 households = ₹400 each | computed from F5 | 2026-10-21 | python: 12000/30 = 400. The ₹12,000 budget is assumed. |
| F8 | Gifts of money/goods from non-relatives: taxable once the year's aggregate crosses ₹50,000; gifts from specified relatives exempt | https://www.incometaxindia.gov.in/w/tax-treatment-of-gifts-received-by-an-individual-or-huf | 2026-10-21 | UNVERIFIED — do not use. Official page returned 403 to me; only seen via search summary. Mithai boxes are far below this anyway. |

Worked example (python):
```
600 * 30 = 18000      # F4 x F5 -> F6
12000 / 30 = 400.0    # F7
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- Every house has the "gift recycling" box: the Soan Papdi that has done three Diwalis and returned to the original sender.
- The family WhatsApp group becomes a logistics ministry: "Mamaji ko kaju katli, Sharma uncle ko sirf dry fruits, watchman ko ₹500 aur mithai."
- Cousins compare box weight; the box looks big but is 40% tray and plastic.
- The guilt tier list: neighbour who gave you last year gets a bigger box than you planned. Gifting is reciprocal debt.
- Mom has a notebook/phone note of who gave what in which year, a real ledger.
- Gen Z cuts the list, goes for a diya + chocolate combo, or "UPI karo, mithai khud lo".

## Culture now
- M1 · image · "Dekh raha hai na binod" · Indian classic: someone watching a mess unfold, used when you see others over-spend; evergreen Indian template, not new · peaked 2021-01 · https://knowyourmeme.com/memes/dekh-raha-hai-na-binod
- M2 · image · "Bas karo bhai" · Indian reaction: stop it, enough; fits a gift list that keeps growing · peaked 2021-01 · https://imgflip.com/memesearch?q=Bas+karo+bhai
- M3 · image · "Aura Farming" · global Gen Z: gaining cool points; use for the person who gifts the biggest box · peaked 2025-06 · https://knowyourmeme.com/memes/aura-farming
- M4 · sound · "Aayein Meme" · Indian-origin sound of confused "huh?" at an absurd number (check: video/sound rule is global only — drop if validate blocks) · peaked 2025-10 · https://www.myinstants.com/
- M5 · ref · "Great Meme Reset" · Gen Z TikTok complaint about a meme drought; say it for a tired joke · peaked 2025-11 · https://www.ypulse.com/newsfeed/2025/11/12/gen-z-is-planning-to-wipe-the-meme-slate-clean-in-2026/
- M6 · ref · "aura" as slang (gaining or losing aura) · peaked 2026-09 · https://knowyourmeme.com/memes/aura-farming
- M7 · ref · "Mithai Wars" · Diwali brand campaign that framed sweets as election candidates, so the sweets-ranking joke lands · peaked 2025-10 · https://www.socialsamosa.com/experts-speak/this-diwali-brands-bet-on-humour-connect-with-gen-z-10544901
