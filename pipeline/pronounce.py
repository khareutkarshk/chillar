#!/usr/bin/env python3
"""Hear Sunny the way a Hindi speaker would, find the exact words it says wrong, and fix them with a verified
respelling in brand/pronunciations.tsv.

  pronounce.py check episodes/<ep>        -> .cache/pronounce.json: per line, the words Sunny said differently
  pronounce.py solve episodes/<ep>        -> try respellings for every bad word, keep the one that is heard right
                                             (twice), append it to brand/pronunciations.tsv; exit 1 if any word is
                                             still unsolved
  pronounce.py sweep [--solve]            -> check every past reel's voice; .cache/pronounce_sweep.json + summary
  pronounce.py stress                     -> every channel word + brand/pronounce_corpus.txt in carrier lines, two
                                             takes each; words missed in both get verified lexicon rows
  pronounce.py probe "<tts text>"         -> synthesize one line with the channel voice and print what is heard

The judge is Sarvam's own recogniser (saaras:v3, mode "verbatim": no normalisation, so "बारहों" for "बारह" and
"गुमशुद्धा" for "गुमशुदा" come through as said, and numbers come back as the words spoken). Whisper medium heard
those as correct; it also invents most of what it "misses" in Hinglish. Each clip is cached by its audio hash, so
re-checks are free. Cost: TTS ₹2 / 1,000 chars, STT ≈ ₹0.5 a minute.

Only Devanagari words are judged (English words in Latin come back transliterated; too noisy to score).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import difflib
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ROOT, env, session  # noqa: E402
from lib.episode import load  # noqa: E402
import tts  # noqa: E402

STT_URL = "https://api.sarvam.ai/speech-to-text"
STT_MODEL, STT_MODE = "saaras:v3", "verbatim"
CACHE = ROOT / ".cache" / "stt"
DEV = re.compile(r"[ऀ-ॣ०-ॿ]+")
PAD = 0.25            # seconds either side of a line clip
OK = 0.8              # normalised similarity at which a heard word counts as the written word
TRIES = 6             # respellings tried per word
CONFIRM = 2           # a respelling must be heard right in this many fresh takes

# ----------------------------------------------------------------------------- numbers as spoken (verbatim mode)
ONES = ("शून्य एक दो तीन चार पाँच छह सात आठ नौ दस ग्यारह बारह तेरह चौदह पंद्रह सोलह सत्रह अठारह उन्नीस बीस इक्कीस "
        "बाईस तेईस चौबीस पच्चीस छब्बीस सत्ताईस अट्ठाईस उनतीस तीस इकतीस बत्तीस तैंतीस चौंतीस पैंतीस छत्तीस सैंतीस "
        "अड़तीस उनतालीस चालीस इकतालीस बयालीस तैंतालीस चवालीस पैंतालीस छियालीस सैंतालीस अड़तालीस उनचास पचास इक्यावन "
        "बावन तिरेपन चौवन पचपन छप्पन सत्तावन अट्ठावन उनसठ साठ इकसठ बासठ तिरसठ चौंसठ पैंसठ छियासठ सड़सठ अड़सठ "
        "उनहत्तर सत्तर इकहत्तर बहत्तर तिहत्तर चौहत्तर पचहत्तर छिहत्तर सतहत्तर अठहत्तर उन्यासी अस्सी इक्यासी बयासी "
        "तिरासी चौरासी पचासी छियासी सतासी अठासी नवासी नब्बे इक्यानवे बानवे तिरानवे चौरानवे पचानवे छियानवे सत्तानवे "
        "अट्ठानवे निन्यानवे").split()


def hindi_number(n: int) -> list[str]:
    if n < 100:
        return [ONES[n]]
    out = []
    for size, word in ((10 ** 7, "करोड़"), (10 ** 5, "लाख"), (1000, "हज़ार"), (100, "सौ")):
        if n >= size:
            out += hindi_number(n // size) + [word]
            n %= size
    return out + ([ONES[n]] if n else [])


def spoken_words(text: str) -> list[str]:
    """The Devanagari words a listener should hear for a tts line: tags stripped, ₹/digits expanded."""
    t = tts.strip_tags(text)

    def num(m: re.Match) -> str:
        v = int(m.group(2).replace(",", ""))
        return " ".join(hindi_number(v)) + (" रुपए" if m.group(1) else "")
    t = re.sub(r"(₹)?\s?(\d[\d,]*)(?![\d.])", num, t)
    return DEV.findall(t)


SAME = {"छः": "छह", "छे": "छह", "छै": "छह", "ये": "यह", "वो": "वह", "मैने": "मैंने"}              # one word, several accepted spellings
LIGHT = {"है", "हैं", "में", "मे", "हूं", "हूँ", "नहीं", "नही", "भी", "ही", "तो", "को", "का", "की", "के", "से", "पे", "ने"}


def norm(w: str) -> str:
    """ASR spelling noise out: nukta, chandrabindu/anusvara/half-nasals, short/long i-u, visarga, ये/ए."""
    w = SAME.get(w, w).replace("़", "").replace("ँ", "ं").replace("ः", "")
    w = re.sub(r"[ङञणनम]्(?=[क-ह])", "ं", w).replace("्", "")      # पाञ्च = पांच; खत्म = खतम
    w = re.sub(r"ये$", "ए", re.sub(r"यी$", "ई", w))
    for a, b in (("ी", "ि"), ("ू", "ु"), ("ई", "इ"), ("ऊ", "उ"), ("ॉ", "ो"), ("ऑ", "ओ"), ("ऐ", "ए"), ("ष", "श"), ("व", "ब")):
        w = w.replace(a, b)
    return w


def same(a: str, b: str) -> bool:
    """Heard as written? Short words must match exactly (बारह/बारहों, नौ/नो are real misses); longer ones may
    carry one letter of ASR spelling noise. Light function words are never judged."""
    if a in LIGHT:
        return True
    na, nb = norm(a), norm(b)
    if na == nb:
        return True
    if len(na) <= 4:
        return False
    return difflib.SequenceMatcher(None, na, nb).ratio() >= OK


def sim(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def diff(expected: list[str], heard: list[str]) -> list[dict]:
    """Expected words the listener did not hear as written: [{word, i, heard}] (heard = the aligned word or '')."""
    sm = difflib.SequenceMatcher(None, [norm(w) for w in expected], [norm(w) for w in heard], autojunk=False)
    bad = []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            continue
        for k, i in enumerate(range(a0, a1)):
            cand = heard[b0:b1]
            h = cand[min(k, len(cand) - 1)] if cand else ""
            # ASR glues/splits words: the word inside a neighbour, or two heard words that make it, is fine
            joined = norm("".join(heard[max(0, b0 - 1):b1 + 1]))
            if any(same(expected[i], c) for c in cand) or (len(norm(expected[i])) >= 5 and norm(expected[i]) in joined):
                continue
            bad.append({"word": expected[i], "i": i, "heard": h})
    return bad


# ----------------------------------------------------------------------------- the judge
def hear(wav: Path, a: float | None = None, b: float | None = None) -> str:
    """Transcript (verbatim) of wav[a:b], cached by the clip's audio."""
    with tempfile.TemporaryDirectory() as d:
        clip = Path(d) / "c.wav"
        cut = ["-ss", f"{max(0.0, a - PAD):.2f}", "-to", f"{b + PAD:.2f}"] if a is not None else []
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), *cut, "-ar", "16000", "-ac", "1", str(clip)],
                       check=True)
        data = clip.read_bytes()
    key = hashlib.sha1(data + f"{STT_MODEL}{STT_MODE}".encode()).hexdigest()[:20]
    CACHE.mkdir(parents=True, exist_ok=True)
    hit = CACHE / f"{key}.txt"
    if hit.exists():
        return hit.read_text()
    k = env("SARVAM_API_KEY")
    if not k:
        sys.exit("SARVAM_API_KEY missing in .env")
    for attempt in range(7):
        r = session.post(STT_URL, headers={"api-subscription-key": k}, timeout=90,
                         files={"file": ("c.wav", io.BytesIO(data), "audio/wav")},
                         data={"model": STT_MODEL, "mode": STT_MODE, "language_code": "hi-IN"})
        if r.status_code == 200:
            break
        if r.status_code not in (429, 500, 502, 503) or attempt == 6:
            sys.exit(f"Sarvam STT {r.status_code}: {r.text[:300]}")
        import time
        time.sleep(min(60, 4 * 2 ** attempt))
    text = r.json().get("transcript", "")
    hit.write_text(text)
    return text


def say(text: str, cfg: dict) -> Path:
    """One fresh (uncached) take of a tts line with the channel voice → temp wav."""
    segs = tts.direction(tts.respell(text)[0])
    pace = float(cfg["pace"]) * (segs[0].pace if segs else 1.0)
    audio = tts.sarvam_request(" ".join(s.text for s in segs), cfg, pace)
    f = Path(tempfile.mkstemp(suffix=".wav", dir=tempfile.gettempdir())[1])
    f.write_bytes(audio)
    return f


# ----------------------------------------------------------------------------- per-episode check
def line_spans(ep) -> list[tuple[str, float, float]]:
    words = json.loads((ep.cache / "words.json").read_text())
    spans: dict[str, list[float]] = {}
    for w in words:
        s = spans.setdefault(w["line"], [w["start"], w["end"]])
        s[1] = max(s[1], w["end"])
    out = list(spans.items())
    # aligned line ends run early (the last word gets clipped): each window runs to the next line's start
    return [(k, a, max(b, out[i + 1][1][0] - PAD) if i + 1 < len(out) else b + 0.6) for i, (k, (a, b)) in enumerate(out)]


def check(ep_dir: str, workers: int = 4) -> dict:
    ep = load(ep_dir)
    tl = [x for x in (ep.dir / "voice" / "tts.txt").read_text().splitlines() if tts.strip_tags(x)]
    wav = ep.cache / "voice_clean.wav"
    spans = line_spans(ep)
    with cf.ThreadPoolExecutor(workers) as ex:
        heard = list(ex.map(lambda s: hear(wav, s[1], s[2]), spans))
    rows = []
    for (lid, a, b), h, i in zip(spans, heard, range(len(spans))):
        said = tl[i] if i < len(tl) else ""
        exp, got = spoken_words(tts.respell(said)[0]), DEV.findall(h)
        bad = diff(exp, got) if exp else []
        # the window's edges catch a neighbour's words: only judge words that aren't at a clipped edge
        rows.append({"line": lid, "t": [round(a, 2), round(b, 2)], "tts": said, "heard": h,
                     "match": round(1 - len(bad) / len(exp), 2) if exp else 1.0, "bad": bad})
    out = {"episode": ep.name, "judge": f"sarvam {STT_MODEL} {STT_MODE}", "rows": rows,
           "bad_words": sum(len(r["bad"]) for r in rows)}
    (ep.cache / "pronounce.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out


# ----------------------------------------------------------------------------- respelling candidates
NASAL_FOR = {**{c: "ङ्" for c in "कखगघ"}, **{c: "ञ्" for c in "चछजझ"}, **{c: "ण्" for c in "टठडढ"},
             **{c: "न्" for c in "तथदधन"}, **{c: "म्" for c in "पफबभम"}}


def candidates(word: str, roman: str = "") -> list[str]:
    """Respellings to try, most plausible first. roman = the writer's Roman spelling of the word in script.md."""
    out: list[str] = []
    vocab = _vocab()
    # never a respelling that is itself another word ("यह → या" turned "this" into "or" and passed the judge)
    add = lambda w: (w and w != word and w not in out and (w not in vocab or norm(w) == norm(word))   # noqa: E731
                     and out.append(w))
    # 0. a postposition glued on (जिसपे, उसपे): Sunny swallows it; written apart it's said apart
    m0 = re.fullmatch(r"(.{2,}?)(पे|पर|से|में|को|का|की|के|ने|वाला|वाली|वाले)", word)
    if m0:
        out.append(f"{m0.group(1)} {m0.group(2)}")
    # 1. nasal spelled out by the next consonant's class (पाँच → पाञ्च; Sunny drops ँ/ं mid-word)
    add(re.sub(r"[ँं](?=([क-ह]))", lambda m: NASAL_FOR.get(m.group(1), "न्"), word))
    add(re.sub(r"[ँं](?=[क-ह])", "न्", word))
    # 2. a doubled/aspirated conjunct read too hard (गुमशुदा → गुमशुद्धा): break it with a hyphenated syllable split
    m = re.search(r"([क-ह][ा-ौ]?)([क-ह][ा-ौ]?)$", word)
    if len(word) >= 5 and m:
        add(word[:m.start()] + "-" + word[m.start():])
    # 3. final -ह after a vowel sound said as an extra syllable (बारह → बारहों): write the vowel as spoken
    add(re.sub(r"([क-ह])ह$", r"\1ा", word))
    add(re.sub(r"ह$", "ह्", word))
    # 4. vowel length nudges
    for a, b in (("ि", "ी"), ("ी", "ि"), ("ु", "ू"), ("ू", "ु")):
        if a in word:
            add(word.replace(a, b, 1))
    # 5. the writer's own Roman spelling (Sunny often reads Hinglish words in Latin as intended)
    if roman and re.fullmatch(r"[A-Za-z'-]+", roman):
        add(roman.lower())
    return out[:TRIES]


_VOCAB: set[str] | None = None


def _vocab() -> set[str]:
    """Every Devanagari word the channel has written in a tts.txt (the guard against respelling into a real word)."""
    global _VOCAB
    if _VOCAB is None:
        _VOCAB = {w for p in (ROOT / "episodes").glob("*/voice/tts.txt") for w in DEV.findall(p.read_text())}
    return _VOCAB


def roman_for(ep, line_idx: int, word_i: int, n_exp: int) -> str:
    """The script.md word at the same relative position (tts.txt keeps script words and order)."""
    spoken = [ln for ln in ep.lines if ln.spoken]
    if line_idx >= len(spoken):
        return ""
    ws = re.findall(r"[A-Za-z'-]+", spoken[line_idx].spoken)
    if not ws or not n_exp:
        return ""
    return ws[min(len(ws) - 1, round(word_i * len(ws) / n_exp))]


def solve_word(line: str, word: str, roman: str, cfg: dict) -> str | None:
    """'' = the word as written is heard right in fresh takes (the shipped take was unlucky: re-take the line);
    a respelling = written that way it's heard right every time; None = nothing passed."""
    if all(heard_right_variant(line, word, word, cfg) for _ in range(CONFIRM)):
        return ""
    for cand in candidates(word, roman):
        variant = re.sub(rf"(?<![{tts._WORD}]){re.escape(word)}(?![{tts._WORD}])", cand, line, count=1)
        if all(heard_right_variant(variant, word, cand, cfg) for _ in range(CONFIRM)):
            return cand
    return None


def heard_right_variant(variant: str, word: str, cand: str, cfg: dict) -> bool:
    """The candidate replaces the word in the line; the listener must hear the *original* word."""
    f = say(variant, cfg)
    try:
        got = DEV.findall(hear(f))
    finally:
        f.unlink(missing_ok=True)
    exp = spoken_words(variant.replace(cand, word, 1))
    return not any(b["word"] == word for b in diff(exp, got))


def add_rows(rows: list[tuple[str, str, str]]) -> None:
    lex = tts.LEXICON
    have = {w for w, _ in tts.lexicon()}
    new = [r for r in rows if r[0] not in have]
    if new:
        with lex.open("a") as f:
            for w, s, why in new:
                f.write(f"{w}\t{s}\t{why}\n")


def solve(ep_dir: str, report: dict | None = None) -> tuple[list[tuple[str, str, str]], list[str], list[str]]:
    """→ (lexicon rows added, unsolved notes, line ids to re-take). Also written to .cache/pronounce_fix.json."""
    ep = load(ep_dir)
    cfg = {**tts.DEFAULTS, **ep.config.get("tts", {})}
    report = report or check(ep_dir)
    fixed, unsolved, seen, retakes = [], [], set(), set()
    for idx, r in enumerate(report["rows"]):
        for b in r["bad"]:
            w = b["word"]
            if w in seen or not DEV.fullmatch(w):
                continue
            seen.add(w)
            line = tts.respell(r["tts"])[0]
            # a number word that only exists inside an expanded figure (₹6,200) can't be respelled in place
            if not re.search(rf"(?<![{tts._WORD}]){re.escape(w)}(?![{tts._WORD}])", line):
                if w in ONES or w in ("सौ", "हज़ार", "लाख", "करोड़", "रुपए"):
                    unsolved.append(f"{r['line']} figure read wrong ('{w}' heard '{b['heard']}') — write it in words in tts.txt")
                continue
            roman = roman_for(ep, idx, b["i"], len(spoken_words(line)))
            cand = solve_word(line, w, roman, cfg)
            if cand == "":
                retakes.add(r["line"])
                print(f"  ↻ {w}: heard right in {CONFIRM} fresh takes → re-take {r['line']} (no respelling)")
            elif cand:
                fixed.append((w, cand, f"auto: heard '{b['heard'] or '—'}', fixed + verified ×{CONFIRM} by "
                                       f"Sarvam {STT_MODEL} ({ep.name})"))
                print(f"  ✓ {w} → {cand}  (was heard '{b['heard']}')")
            else:
                unsolved.append(f"{r['line']} '{w}' heard '{b['heard']}' — no respelling passed")
                print(f"  ✗ {w}: no respelling passed (heard '{b['heard']}')")
    add_rows(fixed)
    # a respelled word changes its line's text, so that line gets a new take on the next tts.py run by itself
    (ep.cache / "pronounce_fix.json").write_text(json.dumps(
        {"fixed": fixed, "unsolved": unsolved, "retake": sorted(retakes)}, indent=1, ensure_ascii=False))
    return fixed, unsolved, sorted(retakes)


def sweep(do_solve: bool) -> dict:
    eps = [p.parent.parent for p in sorted((ROOT / "episodes").glob("*/.cache/words.json"))
           if not p.parent.parent.name.startswith("_") and (p.parent.parent / "voice" / "tts.txt").exists()
           and (p.parent.parent / ".cache" / "voice_clean.wav").exists()]
    words: dict[str, list] = {}
    per = {}
    for d in eps:
        try:
            r = check(str(d))
        except Exception as ex:                      # an old reel whose words.json predates the line ids
            print(f"  skip {d.name}: {ex}")
            continue
        per[d.name] = r["bad_words"]
        for row in r["rows"]:
            for b in row["bad"]:
                words.setdefault(b["word"], []).append({"ep": d.name, "line": row["line"], "heard": b["heard"],
                                                        "tts": row["tts"]})
        print(f"  {d.name}: {r['bad_words']} word(s) heard differently")
    out = {"episodes": per, "words": dict(sorted(words.items(), key=lambda kv: -len(kv[1])))}
    (ROOT / ".cache" / "pronounce_sweep.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    if do_solve:
        for d in eps:
            if per.get(d.name):
                print(f"solve {d.name}")
                solve(str(d), json.loads((d / ".cache" / "pronounce.json").read_text()))
    return out


CORPUS = ROOT / "brand" / "pronounce_corpus.txt"
PER_LINE = 5


def stress(cfg: dict, workers: int = 2) -> dict:
    """Every channel word (all tts.txt + brand/pronounce_corpus.txt) said in carrier lines, two fresh takes each.
    A word missed in both takes is a real Sunny problem → solve_word (verified respelling, lexicon row); missed in
    one is take luck (voice_check + a re-take handle it per reel)."""
    words = sorted({w for line in CORPUS.read_text().splitlines() if not line.startswith("#")
                    for w in DEV.findall(line)} | _vocab())
    lexed = dict(tts.lexicon())
    words = [w for w in words if w not in lexed and w not in LIGHT]
    lines = [words[i:i + PER_LINE] for i in range(0, len(words), PER_LINE)]

    parts_p = ROOT / ".cache" / "pronounce_stress_parts.json"      # resumable: a group heard twice is done
    parts = json.loads(parts_p.read_text()) if parts_p.exists() else {}

    def run(group: list[str]) -> list[tuple[str, int]]:
        text = "सुनो, " + ", ".join(group) + "।"
        if text in parts:
            return [tuple(x) for x in parts[text]]
        misses = {w: 0 for w in group}
        for _ in range(2):
            f = say(text, cfg)
            try:
                got = DEV.findall(hear(f))
            finally:
                f.unlink(missing_ok=True)
            for b in diff(spoken_words(tts.respell(text)[0]), got):
                if b["word"] in misses:
                    misses[b["word"]] += 1
        parts[text] = [(w, k) for w, k in misses.items() if k]
        parts_p.write_text(json.dumps(parts, ensure_ascii=False))
        return parts[text]

    with cf.ThreadPoolExecutor(workers) as ex:
        found = [x for res in ex.map(run, lines) for x in res]
    real = sorted(w for w, k in found if k == 2)
    flaky = sorted(w for w, k in found if k == 1)
    print(f"stress: {len(words)} words · {len(real)} missed in both takes · {len(flaky)} in one")
    fixed, unsolved = [], []
    for w in real:
        cand = solve_word(f"सुनो, {w}।", w, "", cfg)
        if cand:
            fixed.append((w, cand, f"stress test: missed in 2/2 carrier takes, fixed + verified ×{CONFIRM} by "
                                   f"Sarvam {STT_MODEL}"))
            print(f"  ✓ {w} → {cand}")
        elif cand == "":
            flaky.append(w)
        else:
            unsolved.append(w)
            print(f"  ✗ {w}: no respelling passed")
    add_rows(fixed)
    out = {"words": len(words), "fixed": fixed, "unsolved": unsolved, "flaky": sorted(set(flaky))}
    (ROOT / ".cache" / "pronounce_stress.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("check", "solve"):
        sub.add_parser(c).add_argument("episode")
    sw = sub.add_parser("sweep")
    sw.add_argument("--solve", action="store_true")
    sub.add_parser("stress")
    pr = sub.add_parser("probe")
    pr.add_argument("text")
    pr.add_argument("--episode", default=str(ROOT / "episodes" / "_template"))
    a = ap.parse_args()
    if a.cmd == "check":
        r = check(a.episode)
        print(f"pronounce: {r['bad_words']} word(s) heard differently → .cache/pronounce.json")
        for row in r["rows"]:
            for b in row["bad"]:
                print(f"  ! {row['line']} '{b['word']}' heard '{b['heard'] or '—'}'")
        return 0
    if a.cmd == "solve":
        fixed, unsolved, retakes = solve(a.episode)
        print(f"solve: {len(fixed)} respelled → brand/pronunciations.tsv, {len(retakes)} line(s) to re-take"
              f"{' (' + ','.join(retakes) + ')' if retakes else ''}, {len(unsolved)} unsolved")
        for u in unsolved:
            print(f"  ! {u}")
        return 1 if unsolved else 0
    if a.cmd == "sweep":
        r = sweep(a.solve)
        print(f"sweep: {len(r['words'])} distinct word(s) across {len(r['episodes'])} reels → .cache/pronounce_sweep.json")
        for w, v in list(r["words"].items())[:30]:
            print(f"  {w} ×{len(v)}  heard: {', '.join(sorted({x['heard'] or '—' for x in v}))[:60]}")
        return 0
    if a.cmd == "stress":
        ep = load(str(ROOT / "episodes" / "_template"))
        stress({**tts.DEFAULTS, **ep.config.get("tts", {})})
        return 0
    ep = load(a.episode)
    cfg = {**tts.DEFAULTS, **ep.config.get("tts", {})}
    f = say(a.text, cfg)
    print(hear(f))
    f.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
