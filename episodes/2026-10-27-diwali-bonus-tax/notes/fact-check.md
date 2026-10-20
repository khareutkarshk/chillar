verdict: PASS

fact_lint: ok, no problems. scenes/scenes.json: not present (nothing to scan).
Library F2–F5 are fresh (checked 2026-10-19), so I only checked that the script says no more than they support. F1, F6 and the worked examples were checked 2026-10-21.

| line | claim | fact | status | fix |
|---|---|---|---|---|
| L1–3 | Bonus mail, cart, mummy's lifafa (jokes, no numbers) | – | ✅ | – |
| L5 | "Bonus salary jaisa hi taxable" + stamp "Bonus = salary" | F1 | ✅ | F1 was seen only as a snippet of s.15 (the page returned 403). The script wording matches the "not a statute quote" caveat. |
| L6 | Slabs run from zero to thirty percent | F2 | ✅ | – |
| L7 | Last lifafa gets the biggest cut (joke) | F2 | ✅ | – |
| L9 | Maan lo: new regime, ₹15 lakh salary, ₹1 lakh bonus | F9 | ✅ | Framed as "Maan lo". |
| L10 | Extra tax about ₹15,000; slip fine print "sirf standard deduction, cess ignored" | F9 | ✅ | I re-did the arithmetic. Taxable ₹14.25L gives tax ₹93,750. Taxable ₹15.25L gives ₹1,08,750. The difference is ₹15,000. "Lagbhag" and the cess note keep it honest. |
| L11 | In hand about ₹85,000 | F9 | ✅ | ₹1,00,000 − ₹15,000 = ₹85,000, and the true figure with cess is about ₹84,400. |
| L12 | ₹9 lakh salary + ₹50,000 bonus, rebate makes tax zero | F10, F3 | ✅ | Taxable ₹8.75L. Slab tax is ₹20,000 + ₹7,500 = ₹27,500, below the ₹60,000 rebate. Framed as "Maan lo dost". |
| L13 | Mummy gave the whole lifafa (joke) | – | ✅ | – |
| L15 | Company didn't cut the bonus; the employer withholds TDS on a yearly estimate | F6 | ✅ | The script says "andaaza", not "average rate" (F7 unused, correctly). |
| L17 | Your slab decides what is left; the account is settled in the ITR | F2, F6 | ✅ | – |
| L16/L18 | HR's "TDS as applicable" and mummy jokes | – | ✅ | No numbers. |

Unused rows F4, F5, F7, F8 are fine. F7 and F8 are UNVERIFIED, so they must not be added to the script.

Library write-back: nothing to update. F2–F5 were not re-verified, so their `checked` dates are unchanged.

library: +0 (none recurring)
