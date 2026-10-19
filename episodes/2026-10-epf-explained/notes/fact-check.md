# Fact-check: 2026-10-epf-explained  (2026-10-19)

Verdict: PASS. fact_lint ok (0 problems). scenes.json does not exist yet, so on-screen numbers were checked from the {visual} tags in script.md.
Fresh library entries (F2, F3, F4, F5): only checked that the lines say no more than the fact. F1, F6, F9, F11 re-read in cached PIB copies. F19 arithmetic re-run in Python.
UNVERIFIED rows (F9 auto-settlement limit, F12 auto-transfer, F13, F14, F15 Rs 5 lakh, F16 same-rate VPF, F18 36 months): the script cites none of those parts. F12-F18 and F5, F7, F8, F10 are uncited.

| line | claim | fact | status | fix |
|---|---|---|---|---|
| Hook L1 | Har mahine PF bharta hai | F2 | ✅ | none |
| Hook L2 | UAN password joke | JOKE | ✅ | no number |
| Setup 1 | Basic ka 12% tumse, 12% company se | F2 | ✅ | none |
| Setup 2 | 12 LPA pe aksar ₹11,100/month; screen basic ₹46,250, ₹5,550 + ₹5,550 | F3, F19 | ✅ | 12% x 46,250 = 5,550. "aksar" matches the F3 caveat. 50%-basic assumption stated in F19. |
| Setup 2 tag | "new joiner, ceiling ke upar → poora 12% EPF mein" | F2 | ✅ | none |
| Setup 3 | Itna tumne kabhi khud save nahi kiya | JOKE | ✅ | no number |
| Setup 4 | Company hissa in-hand mein nahi, par tumhara | F2 | ✅ | none |
| Setup 5 | Shagun jaisa nahi, yeh wapas milta hai | F11, JOKE | ✅ | F11: full withdrawal on retirement etc. and partial after 12 months. Line says no more than that. |
| Esc 1 | Byaaj 8.25%, har saal meeting mein tay hota hai; screen "8.25% · 2025-26 · CBT recommended" | F1 | ✅ | PIB: CBT recommends for FY 2025-26. Ratified by the Finance Ministry in Jun 2026 per press (PTI via ETV Bharat, Outlook Money), but no primary notification, so keep the screen text "recommended", never "notified". Advisory only: the line is fine as is. |
| Esc 2 | Credit saal mein ek baar | F6 | ✅ | PIB 2178522: annual credit by July 2025 |
| Esc 3 | Rate yahi rahe toh 30 saal baad ₹1.65 crore; screen 1 saal ₹1,39,152, 10 saal ₹20,39,930, ₹1,65,05,027 | F1, F19 | ✅ | Python re-run: 139152 / 2039930 / 16505027 match. Conditional wording kept ("agar 8.25% hi rahe"). |
| Esc 4 | ₹1.25 crore sirf byaaj, daala ₹40 lakh; screen ₹1,25,09,027, ₹39,96,000 | F19 | ✅ | 11,100 x 360 = 39,96,000. 1,65,05,027 - 39,96,000 = 1,25,09,027. |
| Esc 5 | Byaaj ne teen guna kamaya | F19, JOKE | ✅ | 1.25 cr / 0.40 cr = 3.13x, so "teen guna" holds |
| Payoff 1 | Khulega kab? 12 mahine naukri ke baad | F9 | ✅ | PIB 2178522: 12 months for all partial withdrawals |
| Payoff 2 | Naukri chalte 25% andar hi rehta hai | F4 | ✅ | PIB: 25% minimum balance at all times |
| Payoff 3 | Baaki nikalo: padhai, shaadi, ghar, ya bina wajah bhi | F9 | ✅ | Essential needs (education, marriage), housing, and special circumstances with no reason needed. |
| Payoff 4 | Sarkari naam "special circumstances" | F9, JOKE | ✅ | Category name confirmed in PIB 2178522 |
| Payoff 5 | Jo aaj nikala, uska aage ka byaaj bhi gaya; screen phone ₹1,00,000, ₹10.8 lakh kam after 30 yrs (agar 8.25%) | F6, F19 | ✅ | 100000 x 1.0825^30 = 10,78,542, about 10.8 lakh. ₹1,00,000 phone is labelled as the example in F19. Conditional wording kept on screen. |
| Payoff 6-7 | Duniya ka sabse mehenga phone; chabi UAN password | JOKE | ✅ | no numbers |

No library changes needed: the `checked` dates for L-EPF-* entries were not re-verified from source and stay as they are. F19 is an episode-specific computation and was not added to the library.
