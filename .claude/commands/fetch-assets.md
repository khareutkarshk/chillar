---
description: Find, license-check, download and log assets from the allowed sources only
argument-hint: <query> [sfx|music|image|video|icon]
---

Fetch assets for: **$ARGUMENTS**

Use only `pipeline/fetch_assets.py` (it re-checks the license on the source at download time,
refuses anything not on the allow-list, and logs to `assets/licenses.json` with a snapshot).

1. Work out the kind (sfx / music / image / video / icon) and a good English query (sources index
   English). Style is illustrated: photos/video (Pexels/Pixabay) only if truly needed.
2. Preview: `.venv/bin/python pipeline/fetch_assets.py search "<query>" --kind <kind> -n 5`
   (add `--max-dur` for SFX, `--min-dur 60` for music, `--source freesound,mixkit,...` to narrow).
3. Download the best 2–3: `... get "<query>" --kind <kind> -n 3 --dest <episode>/assets` (or
   `brand/_audition/files/<slot>` for brand sounds, then rebuild the audition page with `audition`).
4. Never download from anywhere else, never use real brand logos/app sounds, copyrighted memes or
   realistic banknotes. Pixabay audio needs a visible Chrome window (Cloudflare) — keep volume tiny.
5. Report: file, source, license, attribution needed, and the licenses.json entry.
