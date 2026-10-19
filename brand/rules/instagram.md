# Instagram upload spec (so Reels don't break after upload)

Source: Meta's Reels spec in the Instagram Platform reference (checked 2026-10-19) — recorded in
`brand/tokens.json` `"instagram"`. Meta's hard limits: MP4/MOV with the moov atom at the front and no
edit lists · H.264 or HEVC, progressive, closed GOP, 4:2:0 · 23–60 fps · width ≤ 1920 · VBR ≤ 25 Mbps ·
AAC ≤ 48 kHz mono/stereo, 128 kbps · 3 s – 15 min · ≤ 300 MB · cover JPEG, sRGB, ≤ 8 MB, 9:16.

**Our export is stricter, always:**
- **1080×1920, 9:16, 30 fps constant**, H.264 High 4.2, `yuv420p`, 1 s closed GOP, CRF 18 capped at
  16 Mbps, BT.709 colour tags, `+faststart`, no edit lists, metadata stripped. Not HEVC (uploads from
  some devices/transcodes glitch on it).
- **Audio:** AAC 128 kbps, 48 kHz, stereo, −14 LUFS / −1 dBTP. Never upload silent video.
- **`output/final.mp4` is always re-encoded by `pipeline/mix.py` with `ig_export.encode_args()`** —
  never stream-copied from the renderer (the raw render has 8 s keyframe gaps and an edit list).
- **Cover:** `output/cover.jpg` (JPEG, sRGB, 1080×1920). Key text inside the 3:4 grid crop
  (1080×1440, y 240–1680).
- **Gate:** `make_reel.py` ends with the `igcheck` stage (`pipeline/ig_export.py check output/final.mp4
  --cover output/cover.jpg`). Nothing is posted unless it prints "upload-safe".

**Upload habits:** upload the file itself (not a WhatsApp/Telegram-forwarded copy, which is
recompressed); in the Instagram app turn on *Settings → Data usage and media quality → Upload at
highest quality*; upload on Wi-Fi; don't trim or add filters in the IG editor (it re-encodes and can
shift the captions out of the safe zone). Our formats (30/60/90 s) stay under 3 min, the limit for
Reels being recommended to non-followers.

**Profile picture:** `brand/profile/dp-<theme>.jpg` (1080×1080, Chillar side-eye, no text — it has to
read as a 110 px circle). Rebuild with `pipeline/profile_pic.py`. Current DP: `dp-night.jpg`.
