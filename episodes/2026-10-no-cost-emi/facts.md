# Facts — No Cost EMI ka hidden cost

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | RBI (17 Sep 2013, RBI/2013-14/292) said "the very concept of zero percent interest is non-existent": in zero-percent EMI schemes on credit card outstandings the interest is often camouflaged and passed on to the customer as processing fee | https://www.rbi.org.in/scripts/BS_CircularIndexDisplay.aspx?Id=8461 | 2026-10-20 | Para 3. Cached brand/sources/rbi-zero-pct-2013.html. A 2013 circular to banks, not a ban on offers; don't say "RBI banned no-cost EMI" — offers still run. |
| F2 | Same RBI circular: some banks also loaded sourcing costs (e.g. DSA commission) into the rate of interest; RBI said such schemes "only serve the purpose of alluring and exploiting the vulnerable customers" | https://www.rbi.org.in/scripts/BS_CircularIndexDisplay.aspx?Id=8461 | 2026-10-20 | Para 3. Say "RBI ne kaha", not "illegal". |
| F3 | Worked example (illustrative, NOT a real offer): ₹60,000 phone, 6-month EMI at an assumed 15% p.a. gives EMI ₹10,442, total paid ₹62,652, interest ₹2,652. "No cost" means that ₹2,652 is hidden in the price or the discount you give up | https://www.rbi.org.in/scripts/BS_CircularIndexDisplay.aspx?Id=8461 (+ python calc below) | 2026-10-20 | 15% is an assumption, not a sourced rate; say "maan lo". Rests on F1 (interest doesn't vanish). Retailer-discount mechanics are common practice but not stated in the RBI circular. |

```
P=60000, n=6, r=15%/12
EMI = P*r*(1+r)^n/((1+r)^n-1) = 10442.03  -> ₹10,442
total = 10442.03*6 = 62652.17 -> ₹62,652
interest = ₹2,652 (4.4% of price)
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- "No cost" is read as "free" — everyone has a cousin who "took iPhone on EMI, kuch extra nahi laga."
- Checkout on festive-sale days: 3 EMI options, user taps "No cost" in 2 seconds without doing maths.
- The real tell: the cash/UPI price is lower than the EMI price on the same product page, and nobody compares.
- Processing/"convenience" fee line appears at the last step, after you've mentally bought it.
- Gen Z lives on instalments (phone, sneakers, laptop) — EMI feels like a personal-brand upgrade, not a loan.
- Self-roast: "meri salary EMI ka EMI bharne mein jaati hai."

## Culture now
- M1 · image · "Why would I deceive you?" · deadpan Elizabeth Holmes reassurance; use for the seller saying "no cost, trust me" · peaked 2026-09 · https://imgflip.com/memesearch?q=Why+would+I+deceive+you
- M2 · image · "Peak Life Events" · imgflip rising template of mundane "peak" moments; use for tapping "No cost EMI" at checkout · peaked 2026-09 · https://imgflip.com/memesearch?q=Peak+Life+Events
- M3 · sound · "VINE BOOM SOUND" · global sting on a reveal; hit it when the interest number lands · peaked 2026-10 · https://www.myinstants.com/en/search/?name=vine+boom
- M4 · ref · "aura farming" · global slang for effortless cool; "no cost EMI = aura ka loss" · peaked 2026-09 · https://imgflip.com/memesearch?q=Aura
