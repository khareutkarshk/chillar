verdict: PASS

fact_lint: ok, no problems. F2 (L-RBI-ZERO-PCT-2013) fresh but not cited in script. F3 UNVERIFIED, not cited, not used. scenes/scenes.json: not present.
Arithmetic re-done: discount = 0 if cart<5000 else min(10%×cart,1500). ₹100→0; ₹4,999→0; ₹5,000→₹500 (10%); ₹15,000→₹1,500 (10%); ₹1,00,000→₹1,500 = 1.5%. All correct.

| line · claim | fact | status | fix |
|---|---|---|---|
| L1 "Maan lo, ₹1,00,000 ke phone pe 10% off" (+ "₹10,000 bache?") | F1 hypothetical, framed "Maan lo"; F4 | ✅ | – |
| L4 "₹100 pe bhi 10% milega. Bas cart ₹5,000 ka ho." (star quote) | F1, F4 | ✅ | – |
| L7 "Maximum ₹1,500 … ₹10,000 nahi" | F1, F4 | ✅ | – |
| L8 "Yaani 1.5%" + stamp | F4: 1,500/1,00,000 | ✅ | – |
| L10 "10% sirf ₹5,000 se ₹15,000 tak" | F4 | ✅ | – |
| L11 jokes | no numbers | ✅ | – |
| Memes M1/M3 | Culture now; no factual claim | ✅ | – |

library: +0 (none recurring)
