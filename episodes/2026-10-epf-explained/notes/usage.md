# Usage — 2026-10-epf-explained (session 2026-10-19)

ccusage `session` all-time total: start $663.56 → end $674.99 ⇒ **≈ $11.43 for this episode**
(1,523,793,861 → 1,550,054,183 total tokens ⇒ ≈ 26.3M, mostly cache reads). Made the old way: producer
session routing in-session subagents (before pipeline/produce.py existed) — this is the baseline.

Subagent tokens (from hand-backs): research 124k · scriptwriter 46k/51k/54k · script-reviewer 40k/45k/45k ·
fact-checker 37k · director 154k/106k/128k · editor 41k/48k/32k · video-reviewer 32k/26k/27k.

Review rounds: script 3 (PASS in round 3) · fact-check 1 (PASS) · video 3 (REVISE ×3) → creator chose
"fix 2 bugs, deliver"; producer fixed the empty open locker (15 s) and late passbook rows (27 s).
post.md was regenerated afterwards by the new packager agent through produce.py ($0.13) as a live test.
