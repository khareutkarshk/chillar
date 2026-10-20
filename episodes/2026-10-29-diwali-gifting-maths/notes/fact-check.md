verdict: PASS

fact_lint: ok, no problems. scenes/ is empty (no scenes.json to scan). Library `fresh` listed nothing, so F1/F2 were re-checked against the cached PIB 2163555 (0802 and 0813 rows "12% → 5%"; effective 22 Sep 2025).

| line | claim | fact | status | fix |
|---|---|---|---|---|
| L3 | ek dabba ₹600 ("maan lo") | F4 hypothetical, framed | ✅ | — |
| L5 | tees ghar ("maan lo") | F5 hypothetical, framed | ✅ | — |
| L6 | 30 × ₹600 = ₹18,000 | F6 computed: 600×30 = 18000 | ✅ | — |
| L12 | badaam-pista GST 12% → 5% | F1: HSN 0802 covers almonds and pistachios | ✅ | — |
| L12 | "pichhle saal hi" | F2: effective 22 Sep 2025, and this Diwali is Oct/Nov 2026 | ✅ | — |
| L16 | ₹12,000 budget ("maan lo") ÷ 30 = ₹400 | F7: 12000/30 = 400 | ✅ | — |
| L17 | ₹400 wala dabba | F7 | ✅ | — |
| jokes | no hidden numbers; "ek hi dabba" is not a figure | — | ✅ | — |

F3 and F8 are not cited in the script. F8 is UNVERIFIED and must stay out.
library: +1 (L-GST-NUTS-CUT)
