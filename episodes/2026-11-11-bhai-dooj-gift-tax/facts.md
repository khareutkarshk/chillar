# Facts — 2026-11-11-bhai-dooj-gift-tax

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | Income-tax Act 2025, s.92(2)(m)(i): if a person receives, in a tax year, from any person or persons, any sum of money without consideration, the total of which exceeds ₹50,000, the whole of such sum is taxed (income from other sources) | https://prsindia.org/files/bills_acts/bills_parliament/2025/The_Income-tax_Bill,_2025.pdf | 2026-10-21 | Bill text, PDF p.159 (cached: brand/sources/it-bill-2025.pdf.pdf): "any sum of money without consideration, the total of which exceeds fifty thousand rupees, the whole of such sum". Whole amount, not just the excess. Total across all givers in the year. Exactly ₹50,000 or less = not taxed. Official ITD/egazette pages blocked (403/SSL) — section numbering 92(2)(m)/92(3)/92(5)(g) matches ITD pages seen in search results; enacted Act No. 30 of 2025 (in force 1 Apr 2026, see F2). Writer: say "total", "puri raqam", not "excess". |
| F2 | The Income-tax Act, 2025 replaced the 1961 Act from April 2026 | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2026/feb/doc202621776101.pdf | 2026-10-19 | PIB Budget 2026-27 summary: "Income tax Act, 2025 will come into effect from April 2026". (library L-IT-ACT-2025) |
| F3 | Income-tax Act 2025, s.92(3)(a): the ₹50,000 rule in s.92(2)(m) "shall not apply to any sum of money or any property received from any relative" — so a gift from a relative is not taxed, whatever the amount | https://prsindia.org/files/bills_acts/bills_parliament/2025/The_Income-tax_Bill,_2025.pdf | 2026-10-21 | PDF p.159. Same sub-section also exempts gifts on the occasion of the individual's marriage and under a will/inheritance. Widest wording: "relative se mile paise pe ye rule lagta hi nahi". The ITD's own FAQ (not opened, blocked) is understood to say the same for the old Act. |
| F4 | s.92(5)(g) "relative" of an individual means: spouse; brother or sister; brother or sister of the spouse; brother or sister of either parent; any lineal ascendant or descendant (maternal and paternal); lineal ascendant/descendant of the spouse; and the spouse of anyone in those categories (other than spouse) | https://prsindia.org/files/bills_acts/bills_parliament/2025/The_Income-tax_Bill,_2025.pdf | 2026-10-21 | PDF p.160, items (A)–(G). So behen/bhai, bhabhi/jija (spouse of a sibling), mama/chacha/mausi/bua, nana-nani/dada-dadi all count. |
| F5 | Cousins, friends, neighbours and colleagues are not in the s.92(5)(g) "relative" list, so cash from them counts under the ₹50,000 total | computed from F1, F4 | 2026-10-21 | Derived by reading the F4 list (cousin, friend, Rakhi-bandhi "dharam bhai" are absent). Say "cousin / dost / padosi", and "dharam ka bhai", never "sab non-relatives" loosely. Tax professionals note this is a reading of the list; no CBDT clarification on cousins seen. |
| F6 | Worked example: Behen gets ₹21,000 + ₹11,000 + ₹5,100 as Bhai Dooj tika from her real bhai, bhabhi and mama = ₹37,100, all from relatives, so tax on the gift is ₹0 whatever the total | computed from F3, F4 | 2026-10-21 | Illustrative amounts. Frame as "maan lo". Relatives' gifts are not counted toward the ₹50,000 at all. |
| F7 | Worked example: Behen gets ₹60,000 across the year from a college friend and a cousin (two non-relatives, e.g. ₹30,000 each) = ₹60,000 total, above ₹50,000, so the whole ₹60,000 is taxed, not ₹10,000 | computed from F1, F4 | 2026-10-21 | Illustrative amounts. ₹50,000 cliff: ₹50,000 → nil; ₹50,001 → whole ₹50,001. Tax at her slab (see L-TAX-SLABS if needed — not copied; writer shouldn't state a tax amount). |

```python
relatives = 21000 + 11000 + 5100
print(relatives)            # 37100 -> exempt, s.92(3)(a)
non_rel = 30000 + 30000
print(non_rel, non_rel > 50000, "taxable amount =", non_rel)  # 60000 True 60000
```

## Expert take
- myth: "Bhai Dooj pe behen ko cash diya/mila toh gift tax lagega, ₹50,000 se upar toh sidha notice" [F1]
- so what: Rule ka ₹50,000 wala hissa sirf non-relatives ke liye hai; relative se mile paise pe wo rule lagta hi nahi — ₹5,100 ho ya ₹5 lakh. Behen/bhai, bhabhi, mama-mausi sab "relative" hain. Ulta khatra tab hai jab ₹50,000 cross ho aur dene wala cousin ya dost ho: tab puri raqam taxable, sirf upar ka hissa nahi. [F1, F3, F4, F5]
- in ₹: ek behen ko bhai-bhabhi-mama se ₹37,100 mile = tax ₹0. Dost + cousin se ₹60,000 mile = puri ₹60,000 income mein jud jaati hai. [F6, F7]
- do: Is hafte apne bank/UPI se bhejo, cash nahi (paper trail), aur gift ka note ya message "Bhai Dooj gift" likh do — aur batao ki cousin/dost se saal bhar mein ₹50,000 ke paas pahunche toh total jodo.
- follow-up: "Aur nayi Income-tax Act 2025 mein kuch badla?" — Act 1 April 2026 se chalu hai; gift rule wahi ₹50,000 total, relative exempt, aur relatives ki list mein bhai-behen, unke spouse, mama-chacha-mausi-bua shamil hain. [F1, F2, F3, F4]
- jargon: "relative" → income tax ki list mein jo log aate hain (bhai-behen, maa-baap, dada-dadi, mama-chacha, unke spouse); "without consideration" → bina kuch badle mein diye, free mein.

## Texture for the writers (not facts — don't put numbers from here on screen)
- Bhai Dooj: tika, mithai ka dabba, behen ke ghar jaana, aur "gift kya laya?" ka pressure. Bhai ka UPI "₹501 sent" aur behen ka "bas itna?" roast.
- WhatsApp family group pe koi chacha "CA ne bola gift pe tax lagta hai" forward kar deta hai — Diwali-week tax-gyaan.
- Siblings ek doosre ko "tax bachane ke liye" cash cheeni-jhapti karte hain; bhai bolta hai "main toh free mein rakhi ka kharcha de raha tha".
- Kuch behnein bhaiya se "laptop wala gift" maangti hain; bhai ka budget aur ek EMI.
- Cousin-wali behen aur "rakhi bandhi dharam ki behen" — ye hi confusing zone hai.

## Culture now
- M1 · image · "Did you say POTENTIAL blank" · reaction template: someone mishears a hopeful word and pounces — use for "kya bola, gift pe tax?" · peaked 2026-09 · https://imgflip.com/memetemplates
- M2 · sound · "Aayein Meme" · confused "aayein?" reaction sound, perfect for "gift pe tax?!" confusion · peaked evergreen (check) · https://www.myinstants.com
- M3 · image · "Bas karo bhai" · Indian classic "stop it, brother" — evergreen, fits bhai-behen beat · peaked evergreen · https://imgflip.com/memetemplates
- M4 · ref · "aura / aura points" · Gen Z slang, "bhai ne gift diya, +500 aura" · peaked 2026-09 · https://www.ypulse.com/newsfeed/2025/11/12/gen-z-is-planning-to-wipe-the-meme-slate-clean-in-2026/
- M5 · ref · "Kokilaben 'Rasode mein kaun tha'" · desi family-drama line, usable as "gift mein kaun tha?" · peaked evergreen · https://www.republicworld.com/entertainment/kokilaben-meme-and-other-templates-that-were-all-over-the-internet

(Searches did not surface a verified this-week Indian template; M3/M5 are evergreen — max 2 allowed. M2's sound recency is unconfirmed; drop if validate flags it.)

## Not usable (unverified)
- Official ITD/indiacode/egazette text of the enacted Act 30 of 2025 s.92 could not be opened (403 / SSL); facts rest on the Bill text (PRS hosts the Lok Sabha Bill No. 24 of 2025) with the same section numbers. Enacted wording could differ slightly (Select Committee changes).
- Cash receipt limit of ₹2 lakh (old s.269ST) and its section under the 2025 Act — not verified; keep out.
- Any claim about tax on interest earned from a gifted sum, or clubbing — not verified.
- Any tax amount payable on a taxed gift (slab) — not computed.
