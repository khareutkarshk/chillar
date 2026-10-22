verdict: PASS

fact_lint: ok, no problems. Library: F2, F3 fresh (checked 2026-10-21) — script lines checked for scope only. scenes/scenes.json absent (scenes dir empty) — nothing to scan. Arithmetic redone: 14000+6200+1347+3600+4100+3200+1800=34,247; 40,000−34,247=5,753; 1,347×12=16,164; five small items=14,047 ≈ 14,000.

| line | claim | fact | status | fix |
|---|---|---|---|---|
| L2 | Maan lo ₹40,000, bache ₹5,753 | F1 | ✅ framed "maan lo" | – |
| L5 | rent+maid+wifi ₹14,000 | F1 | ✅ | – |
| L7 | card bill ₹6,200 | F1 | ✅ | – |
| L9 | nau food orders ₹3,600 | F1 | ✅ | – |
| L10 | sale ₹3,200 | F1 | ✅ | – |
| L11 | "Saat ki gang" | F1 (7 line items) | ✅ computed from F1 count | – |
| L15 | 4 subscriptions ₹1,347/mahina | F1 | ✅ | – |
| L17 | ₹16,164 saal ("chalte rahe toh") | F7 | ✅ | – |
| L18 | RBI: kam-se-kam 24 ghante pehle message | F2 | ✅ "kam-se-kam" matches source; FASTag/NCMC exempt, script doesn't say "every" | – |
| L19 | PIN-OTP check, ek debit ya poora autopay rok sakte ho | F3 | ✅ paraphrase of AFA, ok | – |
| L20 | chhote walon ne milke doosra rent | F9 | ✅ approx (14,047 vs 14,000) | – |
| jokes (L1,6,9,12,14,21) | no numbers | – | ✅ | – |

Culture: M3 meme tagged on L2 is in facts.md Culture now (Sep 2026) — not a factual claim.
facts F4–F6, F8 uncited in script but have URLs/computed; left in table.
library: +0 (none recurring)
