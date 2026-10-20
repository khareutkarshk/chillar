# Facts — <episode>

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | ILLUSTRATIVE offer used in the reel (invented, not any real bank/app): "10% instant discount*" with fine print: card-only, minimum cart ₹5,000, maximum discount ₹1,500 | n/a — hypothetical, Chillar-made | 2026-10-20 | Say "ek offer socho"/"fine print kuch aisa hota hai"; never name a bank or app. Cap and minimum are typical-shaped numbers, not a claim about any real offer. |
| F3 | CCPA's Guidelines for Prevention of Misleading Advertisements and Endorsements, 2022 (issued 9 Jun 2022 under Sec 18, Consumer Protection Act 2019) cover free-claim, bait and disclaimer rules for ads in any medium | https://consumeraffairs.nic.in/sites/default/files/PIB1897389.pdf | 2026-10-20 | UNVERIFIED — do not use. consumeraffairs.nic.in unreachable (timeout/refused x3); only law-firm/Vikaspedia summaries read. Disclaimer wording (may clarify, must not contradict/hide material info) not confirmed from gazette. Use only as a "kisi ko bhi suno" idea, no on-screen claim. |
| F4 | Worked example on F1 offer: cart ₹100 → ₹0 off (below ₹5,000 minimum) = 0%; cart ₹4,999 → ₹0 = 0%; cart ₹5,000 → ₹500 = 10%; cart ₹15,000 → ₹1,500 = 10% (cap hit); cart ₹1,00,000 → ₹1,500 off = 1.5% effective, not ₹10,000 | computed from F1 | 2026-10-20 | Formula: 0 if cart<5000 else min(10% × cart, 1500). Effective % = discount ÷ cart. Cap is hit at ₹15,000; beyond that the % only falls. Headline "10%" is true only between ₹5,000 and ₹15,000. |
| F2 | RBI circular of 17 Sep 2013 (RBI/2013-14/292): in zero-percent EMI schemes on credit card outstandings the interest is often camouflaged and passed on as processing fee; "the very concept of zero percent interest is non-existent"; some banks loaded sourcing costs (DSA commission) into the RoI; such schemes "only serve the purpose of alluring and exploiting the vulnerable customers" | https://www.rbi.org.in/scripts/BS_CircularIndexDisplay.aspx?Id=8461 | 2026-10-20 | library:L-RBI-ZERO-PCT-2013. Para 3. Cached brand/sources/rbi-zero-pct-2013.html. A 2013 circular to banks, not a ban on offers; say "RBI ne kaha", not "illegal"/"banned". Dec 2025 RBI card directions reportedly bar labelling interest-bearing EMI "zero-cost" — only news-confirmed, not read in primary. (from 2026-10-no-cost-emi F1/F2) |

```
discount(cart) = 0 if cart < 5000 else min(0.10*cart, 1500)
100      -> 0      -> 0.0%
4,999    -> 0      -> 0.0%
5,000    -> 500    -> 10.0%
15,000   -> 1,500  -> 10.0%
1,00,000 -> 1,500  -> 1.5%   (ad said ₹10,000)
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- Everyone has stared at a cart at 11:58 pm, adding a ₹199 cable just to cross the "minimum spend" line.
- The asterisk is the most-read character in Indian shopping and the least-read in Indian terms & conditions.
- "Card-only" means the 10% exists only if you own the one card the sale is sponsored by — the rest of us watch it like a movie.
- Cart-padding: buying things you don't need to "unlock" a discount, then calling it savings.
- Sale-day ritual: price screenshots, WhatsApp group "bhai, link bhej", the price quietly changing at checkout.
- Big-ticket buyers (phone, laptop, TV) are the ones who hit the cap hardest; the ₹100 cart gets nothing.

## Culture now
- M1 · image · "Why would I deceive you?" · Elizabeth Holmes line; use it as the sale banner's voice reassuring you the "10%" is real · peaked 2026-09 · https://imgflip.com/meme/Why-would-I-deceive-you
- M2 · image · "Did you say POTENTIAL blank" · mocking vague hedge-words in a claim; fits "up to"/"*" fine print · peaked 2026-09 · https://imgflip.com/meme/Did-you-say-POTENTIAL-blank
- M3 · sound · "VINE BOOM SOUND" · the thud on a reveal; use when the real % lands (1.5%) · classic, everywhere (≤1 old-but-everywhere allowed) · https://www.myinstants.com/
- M4 · ref · "aura" · Gen Z slang: +/− aura points; "−1000 aura" for padding the cart to hit the minimum · peaked 2026-09 · https://knowyourmeme.com/memes/aura
