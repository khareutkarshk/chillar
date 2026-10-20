verdict: PASS

fact_lint: ok, no problems. Library had no fresh entries for these facts; F2/F4 re-verified against cached RBI E-mandate Framework 2026 (source_index). F1/F3/F5/F8 not cited in the script.

| line | claim | fact | status | fix |
|---|---|---|---|---|
| L1 | Free trial ended March, debit still in October (story) | none (narrative, no number) | ✅ | — |
| L3 | "UPI autopay pe PIN daala… woh PIN recurring debit ki permission thi" | F6 | ✅ | F6 supports AutoPay for recurring subscriptions; paraphrase OK |
| L4 | Bank sent SMS 24 h before | F2 | ✅ | RBI: ≥24 h pre-transaction notification; SMS is a permitted mode (customer may choose SMS/email). Doesn't say "every autopay" |
| L6 | 6 trials, ₹199/month → ₹14,328/year | F9 | ✅ | 6×199=1,194; ×12=14,328 re-done; framed "maan lo"; hypothetical; Indian grouping OK |
| L9 | Open UPI app's Autopay/Mandates section, pause or revoke | F7 | ✅ | NPCI "pause or revoke anytime"; no app named |
| L10 | Cancel asks PIN or OTP | F4 | ✅ | RBI: opt-out validated using AFA; PIN/OTP paraphrase acceptable |
| jokes | L2, L5, L7, L11 | — | ✅ | no unsourced numbers |

scenes.json: not present (scenes/ empty) — nothing to scan.
Note: F7 source is a 2020-era NPCI doc; no contradicting newer rule found (low risk).
library: +2 (L-RBI-EMANDATE-PRENOTIFY, L-RBI-EMANDATE-OPTOUT)
