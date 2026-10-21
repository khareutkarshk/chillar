# Facts — 2026-11-04-digital-gold-sebi

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.
Two rows may go without a URL (CLAUDE.md §3): an invented scenario — source `hypothetical — <why realistic>` — and
arithmetic on other rows — source `computed from F1, F2`. Start an example row's claim with `Example:` /
`Worked example:` / `ILLUSTRATIVE`; the script must frame it as one ("maan lo", "ek typical …", a first-person
story) the first time it's said — fact_lint blocks an unframed first use.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | SEBI's press release PR No. 70/2025 dated 8 Nov 2025 is titled "Caution to public regarding dealing in 'Digital Gold'" | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | HTML page: sebi.gov.in/media-and-notifications/press-releases/nov-2025/caution-to-public-regarding-dealing-in-digital-gold-_97676.html. Cached sebi-digital-gold-pr70.pdf. Latest SEBI word found; no later withdrawal/new rule turned up in search (not exhaustive) — say "SEBI ne Nov 2025 mein kaha". |
| F2 | Digital gold products are neither notified as securities nor regulated as commodity derivatives; they operate entirely outside SEBI's purview | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | p.1: "neither notified as securities nor regulated as commodity derivatives. They operate entirely outside the purview of SEBI." Say "SEBI ke dayre ke bahar", not "illegal"/"scam" — SEBI never says that. |
| F3 | Digital gold may expose investors to counterparty and operational risks | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | p.1: "may entail significant risks … may expose investors to counterparty and operational risks." "May", not "will". Counterparty = the seller/vault company not delivering. |
| F4 | None of the investor protection mechanisms under securities market purview are available for investments in digital gold / e-gold products | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | p.1: "none of the investor protection mechanisms under securities market purview shall be available". Don't claim there is no protection of any kind (consumer law etc. isn't addressed). |
| F5 | SEBI-regulated gold products are exchange-traded commodity derivative contracts, Gold ETFs offered by Mutual Funds, and Electronic Gold Receipts (EGRs) tradeable on exchanges; they are bought through SEBI-registered intermediaries | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | p.1. Education only: name the categories, never recommend one. |
| F6 | SEBI said it came to its notice that some entities were offering "digital gold"/e-gold products to investors, which prompted the caution | https://www.sebi.gov.in/sebi_data/attachdocs/nov-2025/1762580259409.pdf | 2026-10-21 | p.1 ("It has come to the notice of SEBI that some …"). Don't name any app/company. |
| F7 | Example: a friend puts ₹10 of "gold" on a payment app and assumes it is as safe as a SEBI-regulated product | hypothetical — tiny gold top-ups on apps are a common habit among young users | 2026-10-21 | Framing only; no returns/price claims. Script must say "maan lo". |

## Expert take
- myth: "App pe gold hai, SEBI-approved hoga; sab regulated hai."
- so what: SEBI itself says digital gold sits outside its purview, so securities-market investor protection doesn't apply [F2][F4]; your risk is the seller delivering what the app shows [F3]. A regulated route exists: Gold ETFs, EGRs, exchange-traded derivatives via SEBI-registered intermediaries [F5].
- in ₹: ₹10 ka gold chhota lagta hai, par rule size ka nahi hota: ₹10 ho ya zyada, protection ka sawaal same hai [F4][F7].
- do: this week, open your gold app and find who actually holds the gold and what happens if they stop; ask "kya yeh SEBI-regulated hai?" before adding more.
- follow-up: "Toh kya digital gold illegal hai?" — SEBI didn't say that; it said it's outside its purview and carries risks [F2][F3]. "Toh gold kahan lein?" — SEBI named its regulated categories [F5].
- jargon: purview → "jiske regulator ke dayre mein"; counterparty risk → "jisse khareeda woh hi fail ho jaye"; ETF → "exchange pe bikne wala gold ka fund"; EGR → "gold ki electronic receipt jo exchange pe chalti hai".

## Texture for the writers (not facts — don't put numbers from here on screen)
- Gen Z buys "gold" in tiny top-ups after UPI payments or on festive/Dhanteras nudges: feels like a savings game, not an investment.
- App UI shows a "24K, 99.9% pure" badge and people read it as a government stamp.
- Parents trust physical gold at the sunar; "app wala gold" is where the dad-vs-kid argument begins.
- The friend who sends "bhai ₹10 ka gold le liya 😎" to the group chat — that's the send-to.
- "Regulated" has become a vibe word, like "verified".

## Culture now
- M1 · image · "Maal kidhar hai" · Hera Pheri line: demanding where the goods are; use for "gold kidhar hai?" · peaked 2026-10 (evergreen Indian classic) · https://imgflip.com/memesearch?q=Maal+kidhar+hai
- M2 · image · "Why would I deceive you?" · Elizabeth Holmes deadpan line, new on imgflip this month; for any too-trusting promise · peaked 2026-09 · https://imgflip.com/memesearch?q=Why+would+I+deceive+you
- M3 · image · "Aura Farming" · aura slang; farming aura by looking legit (e.g. a gold badge) · peaked 2026-10 · https://imgflip.com/memesearch?q=Aura+Farming
- M4 · sound · "FAAAH" · global meme sound for a sudden fail/reveal · peaked 2026-10 · https://www.myinstants.com/en/search/?name=FAAAH
- M5 · ref · "aura minus" · Gen Z slang for a cool-losing move · peaked 2026-10 · https://www.ypulse.com/newsfeed/2025/11/12/gen-z-is-planning-to-wipe-the-meme-slate-clean-in-2026/

## Not usable (unverified)
- Any specific app's gold partner, vault or insurance claims — no primary source; don't name or claim.
- GST rate on digital gold purchases — not verified from a primary source; leave out.
- Any SEBI action after Nov 2025 (new rules bringing digital gold under regulation) — none found, not exhaustively confirmed.
- Indian meme trends for Oct 2026 — searches returned only 2025/Jan 2026 roundups; M1 is an evergreen classic.
