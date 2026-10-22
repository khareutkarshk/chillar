"""Episode loading: script.md (chapters, spoken lines, fact ids, joke marks, directions),
facts.md (fact table), cover.md, episode.toml."""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

FACT_RE = re.compile(r"\[(F\d+)\]")
JOKE_RE = re.compile(r"\[JOKE\]", re.I)
DIRECTION_RE = re.compile(r"\{[^}]*\}")
# screenplay delivery marks the writer puts in a line, like an actor's script (never spoken, never captioned):
# pauses where they fall, a mood/pace for what follows, (cont'd) = this line carries on the last one's thought
PERF_RE = re.compile(r"\((beat|pause|long pause|breath|deadpan|excited|warm|soft|fast|slow|cont'?d)\)", re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

DEFAULTS = {
    "voice": {"file": "voice/voice.wav", "denoise": "rnnoise", "silence_threshold_db": -42,
              "max_gap_s": 0.28, "presence_db": 3.5, "lufs": -14},
    "align": {"model": "medium", "language": "hi"},
    "music": {"track": "", "under_voice_db": -22},
    "render": {"quality": "delivery"},
}


@dataclass
class Line:
    id: str
    chapter: str
    raw: str
    spoken: str
    facts: list[str] = field(default_factory=list)
    joke: bool = False
    directions: list[str] = field(default_factory=list)
    perf: list[tuple[int, str]] = field(default_factory=list)   # (spoken words before the mark, mark)


@dataclass
class Episode:
    dir: Path
    meta: dict
    lines: list[Line]
    chapters: list[str]
    facts: dict[str, dict]
    cover: dict
    config: dict
    chapter_fields: dict[str, str] = field(default_factory=dict)   # "## Twist {field: note2000}"

    @property
    def name(self) -> str:
        return self.dir.name

    @property
    def cache(self) -> Path:
        p = self.dir / ".cache"
        p.mkdir(exist_ok=True)
        return p

    @property
    def output(self) -> Path:
        p = self.dir / "output"
        p.mkdir(exist_ok=True)
        return p

    @property
    def format(self) -> str:
        """Duration format "30" | "60" | "90" from script.md target_seconds (nearest); "12" = a pilot test only."""
        try:
            t = float(self.meta.get("target_seconds", 60) or 60)
        except ValueError:
            t = 60.0
        return min(("12", "30", "60", "90"), key=lambda f: abs(int(f) - t))

    @property
    def theme(self) -> str:
        """Look for this episode: scenes.json "theme" (the director's pick for the script's mood) >
        episode.toml [render] theme > brand default in tokens.json."""
        import json
        sp = self.dir / "scenes" / "scenes.json"
        if sp.exists():
            try:
                t = json.loads(sp.read_text()).get("theme")
                if t:
                    return t
            except ValueError:
                pass
        if self.config["render"].get("theme"):
            return self.config["render"]["theme"]
        root = Path(__file__).resolve().parents[2]
        return json.loads((root / "brand" / "tokens.json").read_text())["theme"]

    @property
    def spoken_text(self) -> str:
        return "\n".join(l.spoken for l in self.lines if l.spoken)


def frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        line = re.sub(r"\s+#.*$", "", line)
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip().strip('"').strip("'")
            meta[k.strip()] = {"true": True, "false": False}.get(v.lower(), v)
    return meta, text[m.end():]


FIELD_RE = re.compile(r"\{\s*field\s*:\s*([\w-]+)\s*\}")


def parse_script(text: str) -> tuple[dict, list[Line], list[str], dict[str, str]]:
    """Chapter names are internal structure for the writer/director — they never appear on screen."""
    meta, body = frontmatter(text)
    body = COMMENT_RE.sub("", body)
    lines, chapters, chapter, n = [], [], "Intro", 0
    fields: dict[str, str] = {}
    for raw in body.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("## "):
            head = s[3:]
            fm = FIELD_RE.search(head)
            chapter = re.sub(r"\s+", " ", DIRECTION_RE.sub("", head)).strip()
            if fm:
                fields[chapter] = fm.group(1)
            chapters.append(chapter)
            continue
        if s.startswith("#"):
            continue
        facts = FACT_RE.findall(s)
        directions = [d.strip("{} ") for d in DIRECTION_RE.findall(s)]
        spoken = DIRECTION_RE.sub("", JOKE_RE.sub("", FACT_RE.sub("", s)))
        perf = []
        for m in PERF_RE.finditer(spoken):
            perf.append((len(PERF_RE.sub(" ", spoken[:m.start()]).split()), m.group(1).lower().replace("'", "")))
        spoken = re.sub(r"\s+", " ", PERF_RE.sub(" ", spoken)).strip()
        spoken = re.sub(r"\s+([,.?!।])", r"\1", spoken)
        n += 1
        lines.append(Line(f"L{n}", chapter, s, spoken, facts, bool(JOKE_RE.search(s)), directions, perf))
    if not chapters:
        chapters = ["Intro"]
    return meta, lines, chapters, fields


def parse_facts(text: str) -> dict[str, dict]:
    facts = {}
    for row in text.splitlines():
        if not row.strip().startswith("|"):
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.fullmatch(r"F\d+", cells[0]):
            continue
        url = re.search(r"https?://[^\s>)\]]+", cells[2])
        facts[cells[0]] = {"id": cells[0], "claim": cells[1], "source": url.group(0) if url else "",
                           "source_text": cells[2], "checked": cells[3], "notes": cells[4] if len(cells) > 4 else ""}
    return facts


def load(ep_dir: str | Path) -> Episode:
    d = Path(ep_dir).resolve()
    meta, lines, chapters, chapter_fields = parse_script((d / "script.md").read_text())
    facts = parse_facts((d / "facts.md").read_text()) if (d / "facts.md").exists() else {}
    cover = frontmatter((d / "cover.md").read_text())[0] if (d / "cover.md").exists() else {}
    cfg = {k: dict(v) for k, v in DEFAULTS.items()}
    if (d / "episode.toml").exists():
        for k, v in tomllib.loads((d / "episode.toml").read_text()).items():
            cfg.setdefault(k, {}).update(v)
    return Episode(d, meta, lines, chapters, facts, cover, cfg, chapter_fields)


# --- words -------------------------------------------------------------------------------
def tokenize(text: str) -> list[str]:
    """Caption/alignment tokens: whitespace split, keep ₹ amounts and punctuation attached."""
    # punctuation-only tokens ("—", "-", "…") are not spoken: never a caption word or an alignment target
    return [t for t in text.split() if re.search(r"[\w₹%]", t)]


def norm(tok: str) -> str:
    return re.sub(r"[^\w₹%]", "", tok.lower())
