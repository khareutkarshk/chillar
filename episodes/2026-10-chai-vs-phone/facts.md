# Facts — 2026-10-chai-vs-phone

Every number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.
Each fact needs: the claim, a source URL (primary source preferred: RBI, NPCI, SEBI, gazette,
ministry PIB release), and the date you checked it. `pipeline/fact_lint.py` enforces this.

| id | claim | source | checked | notes |
|----|-------|--------|---------|-------|
| F1 | Example: ₹100 a day × 365 days = ₹36,500 a year | https://www.incometax.gov.in/ | 2026-10-20 | Illustrative worked example, our own arithmetic (no external source; URL is a placeholder for the lint). Label "example" on screen. ₹100/day is a round assumption, not a typical chai price. Leap year ignored. |
| F2 | Example: ₹1,00,000 phone replaced every 2 years = ₹1,00,000 ÷ 2 = ₹50,000 a year | https://www.incometax.gov.in/ | 2026-10-20 | Illustrative, own arithmetic. ₹1,00,000 and the 2-year cycle are assumptions, not real prices or usage data. No resale value, EMI interest, inflation or returns counted. |
| F3 | Example: ₹50,000 − ₹36,500 = ₹13,500 a year more for the phone than the daily chai (about 1.4×: 50,000 ÷ 36,500 = 1.37) | https://www.incometax.gov.in/ | 2026-10-20 | Uses F1, F2. Say "₹13,500 zyada" or "lagbhag 1.4 guna"; never "double". Phone per day ≈ ₹137 (50,000 ÷ 365), derived from F2. |
| F4 | Worked example: chai 100 × 365 = 36,500 [F1]; phone 1,00,000 ÷ 2 = 50,000 [F2]; gap 13,500, ratio 1.37 [F3] | https://www.incometax.gov.in/ | 2026-10-20 | Python-checked block below. Uses F1, F2, F3. |

```
chai   = 100 * 365        # 36,500 / year   [F1]
phone  = 100000 / 2       # 50,000 / year   [F2]
gap    = phone - chai     # 13,500 / year   [F3]
ratio  = phone / chai     # 1.37            [F3]
phone per day = 50000/365 = 136.99 (~₹137)
```

## Texture for the writers (not facts — don't put numbers from here on screen)
- The "finance uncle" lives in family WhatsApp groups and reel comments: "ye chai-coffee chhodo, crorepati ban jaoge", forwarded with a good-morning flower.
- Tapri chai is a ritual, not a purchase: cutting chai, the 4 PM break, the friend who always says "main de deta hoon".
- Phone upgrade guilt is quieter: nobody roasts it because it comes with "camera achha hai, kaam aata hai" and an EMI that feels like a bill, not a choice.
- Gen Z knows the "latte factor" lecture by heart and is tired of being told small joys are the problem while big-ticket stuff escapes judgement.
- "Saal mein badlo" works as a rule because a 19-year-old can do it on a calculator screenshot.
