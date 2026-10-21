verdict: PASS

fact_lint: ok, no problems. All cited facts (F2, F3) are fresh library entries (checked 2026-10-21). scenes/scenes.json does not exist yet, so there is nothing to scan.

| line | claim | fact | status | fix |
|---|---|---|---|---|
| L3 | "Maan lo" dry-fruit box ₹2,100 | F1 (hypothetical, framed "maan lo") | ✅ | none |
| L4 | ₹100 GST, 5% | F1, F2 (dried nuts/mixtures 12%→5%) | ✅ | none |
| L6 | Fufaji's jeweller "making pe 5% alag" | F3 (5% is only the job-worker rate; buyer pays 3% on the total) | ✅ | The line shows this as fufaji's wrong claim. |
| L7 | ₹1,500, making included, 3% | F1, F3, F4 (₹50,000 × 3%) | ✅ | The ₹50,000 base is never said aloud, so it stays implied by the hypothetical story. |
| L8 | ₹1,600 total | F1 (₹100 + ₹1,500, re-computed) | ✅ | none |
| L9 | "Making pe alag 5% dikhe, toh poocho" | F3 | ✅ | none |
| L1/L10 | Jokes, "aura", sad violin | no number | ✅ | none |

Housekeeping: F4–F9 are sourced follow-up facts the script doesn't cite. They are harmless.
Length: the lint estimates ≈ 36 s, which is at the top of the 27–36 s range. The writer can watch this.
library: +0 (none recurring)
