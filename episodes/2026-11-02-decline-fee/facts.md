# Facts — 2026-11-02-decline-fee

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.
Two rows may go without a URL (CLAUDE.md §3): an invented scenario — source `hypothetical — <why realistic>` — and
arithmetic on other rows — source `computed from F1, F2`. Start an example row's claim with `Example:` /
`Worked example:` / `ILLUSTRATIVE`; the script must frame it as one ("maan lo", "ek typical …", a first-person
story) the first time it's said — fact_lint blocks an unframed first use.

Bank = IndusInd Bank (NEVER name it on screen / caption / VO — say "ek private bank"). Source is the bank's own
"Revision in SA Charges Effective Oct-Nov '26" notice, linked from its official Schedule of Charges page.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | From 1 November 2026, one private bank charges ₹25 per transaction as "POS Transaction Decline Charges" on certain savings-account variants (Indus Delite, Indus Digi-start, Indus Online-Min Bal required, Indie Star/Superstar/Megastar); the current charge was Nil. | https://www.indusind.com/content/dam/indusind-corporate/schedule-of-charges/savings-account/Revision-in-SA-Charges-Effective-Oct-Nov-26.pdf | 2026-11-01 | VERIFIED indusind-rev-oct-nov-26.pdf.pdf p.2/§2(a) ("Effective 1st November 2026 … POS Transaction Decline Charges: Current Nil, Revised ₹25 Per Transaction"). Widest wording: "ek bank, kuch savings-account variants pe". NOT every account / not every bank. The notice does NOT say "for insufficient balance" on the POS row (the ATM row does) — say "declined POS transaction"; media reports tie it to insufficient funds but that isn't in the notice text. |
| F2 | From 1 November 2026 the same bank also charges ₹25 per transaction for an ATM transaction declined for insufficient funds at its own ATMs, on the same variants; current charge Nil. | https://www.indusind.com/content/dam/indusind-corporate/schedule-of-charges/savings-account/Revision-in-SA-Charges-Effective-Oct-Nov-26.pdf | 2026-11-01 | VERIFIED indusind-rev-oct-nov-26.pdf.pdf p.2/§2(b) ("ATM Transaction Decline: Insufficient Funds - IndusInd Bank ATM"). Only that bank's own ATMs per the notice. |
| F3 | The notice says all these fees are exclusive of GST, i.e. GST is added on top of ₹25. | https://www.indusind.com/content/dam/indusind-corporate/schedule-of-charges/savings-account/Revision-in-SA-Charges-Effective-Oct-Nov-26.pdf | 2026-11-01 | VERIFIED indusind-rev-oct-nov-26.pdf.pdf p.2 ("all the above fees mentioned are exclusive of GST"). GST rate not in the notice — don't state a rate or a final ₹ figure with GST. |
| F4 | The same notice adds a ₹50 per cheque charge for a cheque returned for a non-financial reason (was Nil) on the same variants. | https://www.indusind.com/content/dam/indusind-corporate/schedule-of-charges/savings-account/Revision-in-SA-Charges-Effective-Oct-Nov-26.pdf | 2026-11-01 | VERIFIED indusind-rev-oct-nov-26.pdf.pdf p.2/§2(c). Optional side-fact; a Gen Z viewer rarely writes cheques. |
| F5 | The bank's notice itself says that if the revised charges don't suit you, it has alternative savings-account options and you can contact the Relationship Manager or a branch representative. | https://www.indusind.com/content/dam/indusind-corporate/schedule-of-charges/savings-account/Revision-in-SA-Charges-Effective-Oct-Nov-26.pdf | 2026-11-01 | VERIFIED indusind-rev-oct-nov-26.pdf.pdf p.2 (closing paragraph). Basis for the "do:" — ask whether your variant is affected / other variants exist. Doesn't promise any specific variant is free of the charge. |
| F6 | Example: a month-end-broke account holder on an affected variant has 4 declined card payments in a month → 4 × ₹25 = ₹100 a month, ₹1,200 a year, before GST. | hypothetical — month-end low balance with a few failed swipes (chai, auto, canteen, Swiggy-type order) is a common student/first-job pattern; arithmetic on F1 | 2026-11-01 | computed from F1, F3 (python: 4*25=100; 100*12=1200). The "4 declines" count is invented — script must say "maan lo". Excludes GST (F3). |

```python
# 4 declines/month x Rs 25 (F1), excl GST (F3)
print(4*25, 4*25*12)   # 100 1200
```

## Expert take
- myth: "Card decline hua toh bas sharam ka moment tha — paisa toh nahi gaya." (declined = free)
- so what: At some banks a declined swipe is no longer free — one bank now bills ₹25 per declined POS transaction on certain savings variants, and charges are added on top of GST [F1][F3]. It hits exactly when the balance is lowest, and it only applies to specific account variants, so it's not "all banks" [F1].
- in ₹: Maan lo 4 declines in a month → ₹100 a month, ₹1,200 a year before GST [F6].
- do: This week open your bank's schedule of charges (app → account/ services, or the bank website) and check three things: which account variant you hold, whether "decline" charges are listed, and set a low-balance alert so you check balance before paying.
- follow-up: "Sab banks karte hain kya?" → No: this notice is one bank, listed variants only [F1]; the notice itself points to alternative savings-account options via branch/RM [F5]. Also "kya ATM pe bhi?" → yes, for that bank's own ATM, insufficient-funds declines, ₹25 [F2].
- jargon: POS = shop pe card swipe machine; decline = payment refuse ho gaya; schedule of charges = bank ki fees ki list; variant = account ka type/plan; GST = fee ke upar extra tax (added on top, F3).

## Texture for the writers (not facts — don't put numbers from here on screen)
- 25th-30th ka scene: balance ₹40, chai-sutta-auto sab "UPI se kar lenge", card ka last swipe canteen/Zomato pe.
- Decline ki sharam: "aunty-ji, machine kharab hai" — standard cover-up line at the counter, billing wala dost jhoota smile.
- "Paisa nahi gaya par penalty aa gayi" = hum bank ko tip de rahe hain for being broke; "garibi pe subscription".
- Salary credit hone se pehle ka countdown; friends splitting bills "tu bhej de, main end me de dunga".
- Gen Z checks balance by trying a payment — iske liye ab fee lag sakti hai; app ke balance-check se free hai.

## Culture now
- M1 · image · "UNO Draw 25 Cards" · "UNO or Draw 25" — pick the awkward option or take 25; the beat: ₹25 per decline = literally draw 25 · evergreen (everywhere, classic) · https://imgflip.com/meme/UNO-Draw-25-Cards
- M2 · image · "Things To Say" · new imgflip template — a list of things people say in a situation; beat: things you say at the billing counter after a decline ("machine kharab hai") · peaked 2026-11 · https://imgflip.com/memesearch?q=Things+To+Say
- M3 · image · "It's La Peace" · reaction template of calm-before-chaos/peace taken away; beat: "salary aane tak peace" shattered by a decline fee · peaked 2026-10 · https://imgflip.com/memesearch?q=La+Peace
- M4 · image · "Sentry mog" · new imgflip template that's rising this month; beat: the bank "mogging" the broke account holder · peaked 2026-10 · https://imgflip.com/memesearch?q=Sentry+mog
- M7 · ref · "aura" / "aura -1000" · Gen Z slang for social-standing points; beat: declined at the counter = aura loss, and now it costs ₹25 too · peaked 2026-10 · https://knowyourmeme.com/memes/aura-points
- Note: web searches found no dated Oct–Nov 2026 Indian trend roundup (latest was March 2026) — Indian rows are classics; writers should keep to ≤2 evergreen per reel (M1/M5/M6 are all evergreen: pick at most 2).

## Not usable (unverified)
- That the ₹25 POS charge applies specifically "for insufficient balance" — notice's POS row only says "POS Transaction Decline Charges"; the reason is in media reports (newsd.in, newstrack) only, not the bank's text.
- That PNB (or any other bank) is also charging ₹25 from 1 Nov 2026 — only secondary news reports; no official notice found. Don't generalise to "banks".
- That Federal Bank charges ₹25 for domestic debit-card decline (search snippet of its 1 Apr 2026 master schedule; not opened/verified, and never name banks on screen anyway).
- GST rate on the ₹25 / total with-GST figure — rate not in the notice.
- Number of customers affected / whether it applies to the credit cards — not in the notice.
