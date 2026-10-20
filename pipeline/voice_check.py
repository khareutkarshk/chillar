#!/usr/bin/env python3
"""Listen to the voiceover the way a viewer would: transcribe it and compare it line by line with tts.txt.

  voice_check.py episodes/<ep>          -> .cache/voice_check.md (+ .json); prints one summary line

Runs after clean + align (it uses .cache/voice_clean.wav and the line times in .cache/words.json).
Whisper "medium" (int8, CPU) — "small" can't hear nasals, which is how "khansa" shipped as "khasa".
It flags, it never fixes: the voice agent / reviewer judges each flag (ASR spelling noise is normal).

Flags per line:
  low-match   few of the line's Hindi words were heard as written (a skipped or mangled word)
  nasal       a word with a mid-word nasal (ँ/ं before a consonant) whose heard form has no nasal at all —
              Sunny drops them; the fix is a brand/pronunciations.tsv row (खाँसा → खान्सा)
  number      a digit/number word in tts.txt whose spoken form doesn't show up
Exit 0 always (advisory); `flags` in the json is what produce.py reads.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.episode import load  # noqa: E402

MODEL = "medium"
DEV = re.compile(r"[ऀ-ॣ०-ॿ]+")         # Devanagari words, not the danda । ॥
MIN_WORDS = 3                  # a line with fewer Hindi words is too short to score (ASR glues them)
NASAL_MID = re.compile(r"[ँं](?=[क-ह])")          # nasal followed by a consonant inside the word
NASALS = set("ँंनमणङञ")
MATRAS = re.compile(r"[ा-्॑-ॗॢॣ़]")   # vowel signs, virama, nukta
LOW_MATCH = 0.6
PAD = 0.12                     # seconds of context either side of a line clip


def skeleton(w: str) -> str:
    """Consonant skeleton of a Devanagari word — ASR vowel spelling noise mostly disappears; any nasal reads as न."""
    return MATRAS.sub("", w.replace("ँ", "न").replace("ं", "न"))


def best(word: str, heard: list[str]) -> tuple[str, float]:
    sk = skeleton(word)
    scored = [(h, difflib.SequenceMatcher(None, sk, skeleton(h)).ratio()) for h in heard]
    glued = "".join(skeleton(h) for h in heard)          # ASR glues short words: "बानर्का", "स्टार्खान्सा"
    if len(sk) >= 2 and sk in glued:
        scored.append((next((h for h in heard if sk in skeleton(h)), word), 1.0))
    return max(scored, key=lambda x: x[1], default=("", 0.0))


def transcribe_lines(wav: Path, spans: list[tuple[float, float]]) -> list[list[str]]:
    """One transcription per line clip — a single pass drifts its word times and skips stretches of a fast read."""
    from faster_whisper import WhisperModel
    m = WhisperModel(MODEL, device="cpu", compute_type="int8")
    out = []
    for a, b in spans:
        segs, _ = m.transcribe(str(wav), language="hi", clip_timestamps=[max(0.0, a - PAD), b + PAD],
                               vad_filter=False, beam_size=1, condition_on_previous_text=False)
        out.append(" ".join(s.text.strip() for s in segs).split())
    return out


def check(ep_dir: str) -> dict:
    ep = load(ep_dir)
    tts = [x.strip() for x in (ep.dir / "voice" / "tts.txt").read_text().splitlines() if x.strip()]
    words = json.loads((ep.cache / "words.json").read_text())
    spans: dict[str, list[float]] = {}
    for w in words:
        a = spans.setdefault(w["line"], [w["start"], w["end"]])
        a[1] = max(a[1], w["end"])
    lines = list(spans.items())
    heard = transcribe_lines(ep.cache / "voice_clean.wav", [tuple(v) for _, v in lines])
    rows, flags = [], 0
    for i, (lid, (a, b)) in enumerate(lines):
        said = tts[i] if i < len(tts) else ""
        got = heard[i]
        got_dev = [g for x in got for g in DEV.findall(x)]
        mine = DEV.findall(said)
        f = []
        if mine:
            score = sum(best(w, got_dev)[1] >= 0.6 for w in mine) / len(mine)
            if score < LOW_MATCH and len(mine) >= MIN_WORDS:
                f.append(f"low-match {score:.0%}")
        else:
            score = 1.0
        for w in mine:
            if NASAL_MID.search(w):
                h, r = best(w, got_dev)
                if not (set(h) & NASALS):
                    f.append(f"nasal: '{w}' heard as '{h or '—'}' → add a pronunciations.tsv row (spell the nasal as न्/म्)")
        if re.search(r"\d", said) and not any(re.search(r"\d", g) for g in got) and len(got) < len(said.split()) * 0.6:
            f.append("number: check the figure is read in full")
        flags += bool(f)
        rows.append({"line": lid, "t": [round(a, 2), round(b, 2)], "tts": said, "heard": " ".join(got),
                     "match": round(score, 2), "flags": f})
    out = {"episode": ep.name, "model": MODEL, "lines": len(rows), "flags": flags, "rows": rows}
    (ep.cache / "voice_check.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    md = [f"# Voice check — {ep.name} (faster-whisper {MODEL})", "",
          f"{len(rows)} lines, **{flags} flagged**. ASR spelling noise is normal; judge only the flags.", "",
          "| line | t | tts.txt | heard | match | flags |", "|---|---|---|---|---|---|"]
    md += [f"| {r['line']} | {r['t'][0]:.1f}–{r['t'][1]:.1f} | {r['tts']} | {r['heard']} | {r['match']:.0%} | "
           f"{'; '.join(r['flags']) or '—'} |" for r in rows]
    (ep.cache / "voice_check.md").write_text("\n".join(md) + "\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    a = ap.parse_args()
    r = check(a.episode)
    print(f"voice check: {r['lines']} lines, {r['flags']} flagged → .cache/voice_check.md")
    for row in r["rows"]:
        for f in row["flags"]:
            print(f"  ! {row['line']} {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
