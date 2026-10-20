#!/usr/bin/env python3
"""The production line as a script — the producer's routing without the producer's tokens.

  produce.py episodes/<ep> --topic "<topic>" [--format 60]        new reel, start to finish
  produce.py episodes/<ep> --from STAGE                           resume (after a stop, or a fix)
  produce.py episodes/<ep> --only STAGE                           one stage
  produce.py episodes/<ep> --only fix                             after a 3-round video stop: one headless pass on
                                                                  the last review's notes + qa, no new review;
                                                                  then --from deliver
  produce.py episodes/<ep> --from align --accept-length           creator accepted a voice outside the range
  produce.py episodes/<ep> --dry-run                              print the agent commands, run nothing

Stages: research → script → factcheck → voice → align → edit → deliver → package → usage

Each agent runs headless (`claude -p --agent <name>`), fresh every round, with a lean context:
no MCP servers, no skills, no hooks, only the tools its .claude/agents/<name>.md lists, and the model
from its frontmatter pinned to a full model id (aliases drift with the CLI version). Agents hand off
through files (script.md, notes/*.md, scenes.json); the script reads only the verdict lines.
Every run's real cost (`total_cost_usd`), turns, tokens and model are appended to
notes/usage.jsonl; the `usage` stage writes notes/usage.md.

Stops (exit 3, reason in notes/STOP.md) — the producer asks the creator, then resumes with --from:
  · script review: no PASS after 3 rounds          · fact-check: still BLOCK after one fix cycle
  · video review: no PASS after 3 rounds           · voice outside the format range
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from agent_context import build_brief, edit_inputs

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "bin" / "python")
AGENTS = ROOT / ".claude" / "agents"
STAGES = ["research", "script", "factcheck", "voice", "align", "edit", "deliver", "package", "usage"]
MAX_ROUNDS = 3
REVISE_EFFORT = "medium"         # director revisions / fix passes (the first plan keeps the frontmatter's high)
OUTRO_S = 3.5                    # outro receipt after the voice
CLEAN = 0.95                     # audio_clean trims ≈ 5 % of the raw voice (measured on 4 reels: 0.94–0.96)

# frontmatter alias -> pinned model id (update here when the brand moves to a new model)
MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5"}
MIN_CLI = (2, 1, 280)            # oldest Claude Code that serves the models above
# safety caps per agent run (USD) — generous; a run that hits one is logged and flagged, not retried
BUDGET = {"researcher": 1.5, "scriptwriter": 1.5, "script-reviewer": 1.0, "fact-checker": 1.0, "voice": 0.8,
          "director": 3.0, "editor": 1.0, "video-reviewer": 1.0, "component-dev": 2.0, "packager": 0.4}
# Bash the agents may run without a prompt (headless runs can't ask). Everything else is denied.
BASH_OK = [".venv/bin/python", "python3", "npx", "ffmpeg", "ffprobe", "ls", "cat", "head", "tail", "grep", "wc",
           "sed", "jq", "mkdir", "cp", "find", "diff", "cd", "echo", "sort", "uniq", "awk"]
# Headless runs finish in < 6 min, so the 5-minute cache is enough; the CLI's default 1-hour cache bills
# writes at 2x input instead of 1.25x (≈ $1.5 a reel, measured on chai-vs-phone).
ENV = {**os.environ, "FORCE_PROMPT_CACHING_5M": "1"}
LEAN = ["--strict-mcp-config", "--disable-slash-commands", "--settings", '{"disableAllHooks": true}',
        "--permission-mode", "acceptEdits", "--output-format", "stream-json", "--verbose", "--no-session-persistence"]


# ------------------------------------------------------------------ claude CLI
def _ver(binary: str) -> tuple:
    try:
        out = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=30).stdout
        return tuple(int(x) for x in re.findall(r"(\d+)\.(\d+)\.(\d+)", out)[0])
    except Exception:
        return (0, 0, 0)


def find_cli() -> str:
    """Newest Claude Code binary: $CHILLAR_CLAUDE, the VS Code extension's bundled one, or PATH."""
    cands = [os.environ.get("CHILLAR_CLAUDE", "")]
    cands += sorted((str(p) for p in Path.home().glob(".vscode*/extensions/anthropic.claude-code-*/resources/native-binary/claude")),
                    key=lambda p: _ver(p), reverse=True)
    cands += [shutil.which("claude") or ""]
    best = max((c for c in cands if c and Path(c).exists()), key=_ver, default="")
    if not best or _ver(best) < MIN_CLI:
        sys.exit(f"produce: need Claude Code ≥ {'.'.join(map(str, MIN_CLI))} for {MODELS['opus']} "
                 f"(found {best or 'none'} {'.'.join(map(str, _ver(best))) if best else ''}). Run `claude update`.")
    return best


def parse_stream(out: str) -> tuple[dict, list[dict]]:
    """stream-json → (the final result event, every tool call with the size of what it returned). The calls show
    where an agent's cache writes go (each tool result is written to the cache once, then re-read every turn)."""
    res, calls, by_id = {}, [], {}
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(ev, dict):
            continue
        msg = ev.get("message")
        for c in (msg.get("content") if isinstance(msg, dict) else None) or []:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "tool_use":
                i = c.get("input") or {}
                what = i.get("file_path") or i.get("command") or i.get("pattern") or i.get("query") or ""
                by_id[c.get("id")] = call = {"tool": c.get("name"), "what": str(what)[:160], "chars": 0}
                calls.append(call)
            elif c.get("type") == "tool_result" and c.get("tool_use_id") in by_id:
                body = c.get("content")
                by_id[c["tool_use_id"]]["chars"] = len(body if isinstance(body, str) else json.dumps(body))
        if ev.get("type") == "result":
            res = ev
    return res, calls


def tool_summary(calls: list[dict]) -> dict:
    """{tool: [calls, result chars]} + the 3 biggest reads — enough to see a wasteful run in usage.jsonl."""
    out: dict = {}
    for c in calls:
        n, k = out.get(c["tool"], [0, 0])
        out[c["tool"]] = [n + 1, k + c["chars"]]
    big = sorted((c for c in calls if c["tool"] in ("Read", "Bash")), key=lambda c: -c["chars"])[:3]
    out["_biggest"] = [f"{c['what'][-60:]} ({c['chars']})" for c in big]
    return out


def frontmatter(agent: str) -> dict:
    text = (AGENTS / f"{agent}.md").read_text()
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    meta = {}
    for line in (m.group(1) if m else "").splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta


class Line:
    def __init__(self, ep: Path, dry: bool):
        self.ep, self.dry = ep, dry
        self.cli = "claude" if dry else find_cli()
        self.log = ep / "notes" / "usage.jsonl"
        self.out = ep / ".cache" / "agents"
        self.out.mkdir(parents=True, exist_ok=True)
        (ep / "notes").mkdir(exist_ok=True)

    def agent(self, name: str, prompt: str, stage: str, effort: str = "", *,
              tools_override: str | None = None, bash_allow: list[str] | None = None) -> str:
        """effort overrides the frontmatter's (revisions run a level below the first pass)."""
        meta = frontmatter(name)
        if effort:
            meta["effort"] = effort
        model = MODELS.get(meta.get("model", "sonnet"), meta.get("model", "sonnet"))
        tools = tools_override or ",".join(t.strip() for t in meta.get("tools", "Read").split(","))
        allowed_bash = ([".venv/bin/python"] if name == "component-dev" else BASH_OK) if bash_allow is None else bash_allow
        allow = [t for t in tools.split(",") if t != "Bash"] + ([f"Bash({b}:*)" for b in allowed_bash] if "Bash" in tools else [])
        cmd = [self.cli, "-p", "--agent", name, "--model", model, "--tools", tools, "--allowedTools", " ".join(allow),
               "--max-budget-usd", str(BUDGET.get(name, 1.0)), *LEAN]
        if meta.get("effort"):
            cmd += ["--effort", meta["effort"]]
        cmd.append(prompt)
        print(f"  ▸ {name} ({model}, {meta.get('effort', '-')}) — {prompt[:90]}", flush=True)
        if self.dry:
            return "verdict: PASS (dry run)"
        t0 = time.time()
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=ENV)
        d, calls = parse_stream(r.stdout)
        if not d:
            d = {"result": (r.stdout + r.stderr)[-2000:], "is_error": True}
        u = d.get("usage", {})
        rec = {"at": dt.datetime.now().isoformat(timespec="seconds"), "stage": stage, "agent": name,
               "prompt_chars": len(prompt),
               "models": list(d.get("modelUsage", {})), "cost": round(d.get("total_cost_usd", 0) or 0, 4),
               "turns": d.get("num_turns"), "secs": round(time.time() - t0),
               "effort": meta.get("effort"),
               "tokens": {k: u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")},
               "cache_1h": (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0),
               "tools": tool_summary(calls),
               "error": d.get("subtype") if d.get("is_error") or d.get("subtype", "success") != "success" else None}
        with self.log.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        n = len(list(self.out.glob(f"{stage}-*.txt"))) + 1
        self.last_out = self.out / f"{stage}-{n}-{name}.txt"
        self.last_out.write_text(d.get("result", ""))
        self.last_out.with_suffix(".tools.json").write_text(json.dumps(calls, indent=1, ensure_ascii=False))
        flag = f"  ⚠ {rec['error']}" if rec["error"] else ""
        if rec["cache_1h"]:
            flag += f"  ⚠ {rec['cache_1h']} cache tokens written at the 1-hour rate"
        if rec["models"] and not any(m.startswith(model) for m in rec["models"]):
            flag += f"  ⚠ ran on {rec['models']}, expected {model}"
        print(f"    ${rec['cost']:.2f} · {rec['turns']} turns · {rec['secs']} s{flag}", flush=True)
        if rec["error"] and "budget" in str(rec["error"]):
            print(f"    ⚠ {name} hit its ${BUDGET.get(name)} cap — check its output before trusting it", flush=True)
        return d.get("result", "")

    def scoped_agent(self, name: str, ep: Path, task: str, stage: str, mode: str,
                     *, note: Path | None = None, effort: str = "") -> str:
        """Run scene/review work with a bounded brief and only the tools needed for that role."""
        brief = build_brief(ep, name, mode, task, edit_inputs(ep, name, mode, note), note=note,
                            max_chars=32000 if name == "director" and mode == "first" else 24000)
        prompt = (f"{task}\n\nUse this bounded context brief as your source set; do not rediscover context "
                  f"with broad shell reads. Brief size: {len(brief)} chars.\n\n{brief}")
        tools = {
            "director": "Read,Write,Edit,Bash",
            "editor": "Read,Edit,Bash",
            "video-reviewer": "Read,Write,Bash",
            "component-dev": "Read,Write,Edit,Bash",
            "scriptwriter": "Read,Write,Edit,Bash",
            "script-reviewer": "Read,Write,Bash",
        }.get(name)
        return self.agent(name, prompt, stage, effort, tools_override=tools,
                          bash_allow=[".venv/bin/python"] if tools and "Bash" in tools else [])

    def sh(self, *args: str, check: bool = True) -> int:
        print(f"  $ {' '.join(args)}", flush=True)
        if self.dry:
            return 0
        r = subprocess.run(list(args), cwd=ROOT, capture_output=True, text=True)
        tail = "\n".join((r.stdout + r.stderr).strip().splitlines()[-6:])
        if tail:
            print("    " + tail.replace("\n", "\n    "), flush=True)
        if check and r.returncode:
            stop(self.ep, f"`{' '.join(args)}` failed (exit {r.returncode})", tail)
        return r.returncode


DRY = False


def verdict(path: Path) -> str:
    if DRY:
        return "PASS"
    if not path.exists():
        return "MISSING"
    m = re.search(r"verdict:\s*\**\s*(PASS|REVISE|BLOCK)", path.read_text(), re.I)
    return m.group(1).upper() if m else "UNKNOWN"


def stop(ep: Path, why: str, detail: str = "") -> None:
    (ep / "notes" / "STOP.md").write_text(f"# Stopped {dt.datetime.now():%Y-%m-%d %H:%M}\n\n{why}\n\n{detail}\n")
    print(f"\n■ STOP: {why}\n  (notes/STOP.md — decide, then resume with --from <stage>)")
    sys.exit(3)


NOTE_ROUTE = re.compile(r"^\s*-\s*\[([^\]]+)\]", re.M)


def routes(text: str) -> set[str]:
    """Owners named in note lines: `- [director] …`, `- [component:bar-chart] …`, `- [director|component:x] …`."""
    return {r.strip().split(":")[0] for tag in NOTE_ROUTE.findall(text) for r in tag.split("|")}


def routed(review: Path, who: str) -> bool:
    return review.exists() and who in routes(review.read_text())


BACKLOG = ROOT / "components" / "_backlog.md"
COMP_TAG = re.compile(r"\[component:([\w-]+)\]")


def backlog(ep: Path, source: str, items: list[str]) -> int:
    """Component requests (director asks, polish notes) go to ONE shared list that `--only components` works through
    in a batch — a mid-episode component-dev run cost ≈ $0.85 for work the director had already worked around."""
    if not items:
        return 0
    have = BACKLOG.read_text() if BACKLOG.exists() else ("# Component backlog\n\nOpen requests from directors and "
                                                         "reviewers. `produce.py <any ep> --only components` builds "
                                                         "them in one batch; done items get `- [x]`.\n")
    new = []
    for x in items:
        body = re.sub(r"^\s*[-*\d.]+\s*", "", x).strip()
        if body and body[:80] not in have:
            new.append(f"- [ ] {body}  _({ep.name} · {source})_")
    if new:
        BACKLOG.write_text(have.rstrip("\n") + "\n" + "\n".join(new) + "\n")
        print(f"  {len(new)} component request(s) → components/_backlog.md (built in batch: --only components)")
    return len(new)


def director(L: Line, ep: Path, prompt: str, stage: str, effort: str = "") -> None:
    """Run the director; its [component:*] requests go to the shared backlog (it works around them in scenes.json)."""
    import re
    m = re.search(r"notes/video-review-(\d+)\.md", prompt)
    note = ep / "notes" / f"video-review-{m.group(1)}.md" if m else None
    mode = "first" if prompt.startswith("Plan ") else "revision"
    L.scoped_agent("director", ep, prompt, stage, mode, note=note, effort=effort)
    if L.dry:
        return
    backlog(ep, L.last_out.name, [x for x in L.last_out.read_text().splitlines() if COMP_TAG.search(x)])


NOTE_LINE = re.compile(r"^\s*-\s*\[([^\]]+)\]\s*(blocker|polish)?(.*)$", re.M)


def notes_for(review: Path, who: str, sev: str | None = None) -> list[str]:
    """Note lines routed to `who` (director / editor / component), optionally only one severity."""
    if not review.exists():
        return []
    out = []
    for m in NOTE_LINE.finditer(review.read_text()):
        owners = {r.strip().split(":")[0] for r in m.group(1).split("|")}
        if who in owners and (sev is None or (m.group(2) or "blocker") == sev):
            out.append(m.group(0).strip())
    return out


# ------------------------------------------------------------------ stages
def st_research(L: Line, ep: Path, a) -> None:
    if not (ep / "script.md").exists():
        shutil.copytree(ROOT / "episodes" / "_template", ep, dirs_exist_ok=True)
    s = (ep / "script.md").read_text()
    s = re.sub(r"target_seconds: \d+", f"target_seconds: {a.format}", s)
    (ep / "script.md").write_text(s)
    L.agent("researcher", f"Research {ep.relative_to(ROOT)} — topic: {a.topic}. Format {a.format} s.", "research")


def duration(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def spoken_words(ep: Path) -> int:
    sys.path.insert(0, str(ROOT / "pipeline"))
    from lib.episode import load
    return len(load(str(ep)).spoken_text.split())


def length_miss(L: Line, ep: Path, a) -> str:
    """Time the passed script with the real voice (tts.py --probe, a few paise) — the words/s estimate is off by up
    to 25 % between reels, and a miss found at align costs a script round + fact-check + voice again."""
    if L.dry or a.accept_length:
        return ""
    if L.sh(PY, "pipeline/tts.py", str(ep), "--probe", check=False):
        return ""                    # no probe (API down): align still checks the real voice
    total = duration(ep / ".cache" / "probe.wav") * CLEAN + OUTRO_S
    lo, hi = json.loads((ROOT / "brand" / "tokens.json").read_text())["formats"][str(a.format)]["seconds"]
    print(f"  length probe: ≈ {total:.1f} s incl. outro (format {lo}–{hi} s)")
    if lo <= total <= hi:
        return ""
    wps = spoken_words(ep) / max(total - OUTRO_S, 1)
    goal = (lo + hi) / 2 - total
    return (f"Sunny reads this script in ≈ {total:.0f} s incl. outro (real voice, measured) — outside {lo}–{hi} s. "
            f"{'Add' if goal > 0 else 'Cut'} ≈ {abs(goal) * wps:.0f} words (she reads ≈ {wps:.1f} words/s; trust this "
            "over the lint's estimate). Keep the best jokes; change nothing else.")


def lint_gate(L: Line, ep: Path) -> None:
    """Mechanical misses (length, framing of example facts, uncited numbers, laugh count, recently used memes) go back
    to the writer once, before an Opus review is spent finding them: 5 of 6 first reviews failed on exactly these."""
    if L.dry:
        return
    r = subprocess.run([PY, "pipeline/fact_lint.py", str(ep), "--json"], cwd=ROOT, capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
    except json.JSONDecodeError:
        return
    miss = [p for p in j.get("problems", []) if not re.match(r"F\d+:", p)]       # facts.md rows aren't the writer's
    miss += [w for w in j.get("warnings", []) if "already used in" in w]          # a meme last week's reel used
    miss += [s for s in j.get("script", [])[1:] if re.search(r"outside|first laugh|minimum|absolute|support an", s)]
    if not miss:
        return
    print(f"  lint gate: {len(miss)} mechanical miss(es) → writer, before the review")
    L.scoped_agent("scriptwriter", ep, f"Before review: fix only these fact_lint misses in {ep.relative_to(ROOT)}/script.md, "
                   "keep every joke that isn't involved, re-run fact_lint until they're gone. Misses: " + " | ".join(miss[:10]),
                   "script", "revision", effort=REVISE_EFFORT)


def st_script(L: Line, ep: Path, a) -> None:
    e = ep.relative_to(ROOT)
    start = len(list((ep / "notes").glob("script-review-*.md"))) + 1
    fix = ""
    last = MAX_ROUNDS + a.extra_rounds           # rounds past the cap only when the creator grants them
    for n in range(start, last + 1):
        if n == 1:
            topic = f" Topic: {a.topic}." if a.topic else ""
            L.scoped_agent("scriptwriter", ep, f"Write {e}/script.md, {a.format} s format.{topic} Fill cover.md first if it still "
                           "has placeholders, and the script.md frontmatter (title, series, concept).", "script", "first")
        elif fix:
            L.scoped_agent("scriptwriter", ep, f"Fix the length of {e}/script.md: {fix}", "script", "revision",
                           note=ep / "notes" / f"script-review-{n - 1}.md", effort=REVISE_EFFORT)
        else:
            L.scoped_agent("scriptwriter", ep, f"Revise {e}/script.md using only actionable items in "
                           f"{e}/notes/script-review-{n - 1}.md. Preserve unmentioned lines.", "script", "revision",
                           note=ep / "notes" / f"script-review-{n - 1}.md", effort=REVISE_EFFORT)
        if not fix:
            lint_gate(L, ep)
        prior = ep / "notes" / f"script-review-{n - 1}.md" if n > 1 else None
        L.scoped_agent("script-reviewer", ep, f"Review {e}/script.md, round {n}." +
                       (" This is a length-only fix: check changed lines and preserve the rest." if fix else "") +
                       (f" Verify unresolved items in {prior.relative_to(ROOT)}, then assess the current draft." if prior else ""),
                       "script", "revision" if prior else "first", note=prior)
        v = verdict(ep / "notes" / f"script-review-{n}.md")
        print(f"  script review {n}: {v}")
        if v == "PASS":
            fix = length_miss(L, ep, a)
            if not fix:
                return
    if fix:
        stop(ep, f"script PASSed but the length probe misses: {fix}",
             "trim/extend the script (new review round) or accept it (--accept-length), then --from factcheck")
    stop(ep, f"script review: no PASS after {last} rounds", f"last notes: notes/script-review-{last}.md · "
         "options: accept the draft with --from factcheck, or one more round with --from script --extra-rounds N")


def st_factcheck(L: Line, ep: Path, a) -> None:
    e = ep.relative_to(ROOT)
    fc = ep / "notes" / "fact-check.md"
    for cycle in (1, 2):
        L.agent("fact-checker", f"Fact-check {e} (script.md against facts.md; scenes.json if it exists). "
                "Write notes/fact-check.md with the verdict line first.", "factcheck")
        v = verdict(fc)
        print(f"  fact-check {cycle}: {v}")
        if v == "PASS":
            return
        if cycle == 2:
            break
        n = len(list((ep / "notes").glob("script-review-*.md")))
        fc_note = ep / "notes" / "fact-check.md"
        L.scoped_agent("scriptwriter", ep, f"Fix only the BLOCK rows listed in {e}/notes/fact-check.md in {e}/script.md "
                       "(change nothing else).", "factcheck", "revision", note=fc_note)
        L.scoped_agent("script-reviewer", ep, f"Review only the lines changed for {e}/notes/fact-check.md in {e}/script.md, "
                       f"round {n + 1} (PASS if they're fixed and still funny).", "factcheck", "revision", note=fc_note)
    stop(ep, "fact-check still BLOCK after one fix cycle",
         "see notes/fact-check.md · options: fix the BLOCK rows (facts.md source / script line) then --from factcheck, "
         "or accept a row the creator has verified and --from voice")


def clean_align(L: Line, ep: Path) -> None:
    L.sh(PY, "pipeline/make_reel.py", str(ep), "--only", "clean")
    L.sh(PY, "pipeline/make_reel.py", str(ep), "--only", "align")


def st_voice(L: Line, ep: Path, a) -> None:
    """The voice agent writes tts.txt + the take; the pipeline then *listens* (voice_check.py, whisper medium) and
    sends flagged lines back once. 'khansa' shipped as 'khasa' because nothing listened after the agent."""
    e = ep.relative_to(ROOT)
    L.agent("voice", f"Make the voiceover for {e}.", "voice")
    if L.dry:
        return
    for attempt in (1, 2):
        clean_align(L, ep)
        L.sh(PY, "pipeline/voice_check.py", str(ep), check=False)
        vc = ep / ".cache" / "voice_check.json"
        flags = json.loads(vc.read_text()).get("flags", 0) if vc.exists() else 0
        if not flags or attempt == 2:
            if flags:
                print(f"  ⚠ {flags} voice line(s) still flagged — the video reviewer gets .cache/voice_check.md")
            return
        L.agent("voice", f"Fix the flagged lines in {e}/.cache/voice_check.md (heard vs written, whisper medium): a real "
                "mispronunciation → add a row to brand/pronunciations.tsv (it applies to every reel) or respell in "
                "tts.txt; ASR spelling noise → ignore. Then regenerate with tts.py once. Don't run whisper yourself.",
                "voice", REVISE_EFFORT)


def st_align(L: Line, ep: Path, a) -> None:
    c = ep / ".cache"
    v, vc, wj = ep / "voice" / "voice.wav", c / "voice_clean.wav", c / "words.json"
    fresh = v.exists() and vc.exists() and wj.exists() and v.stat().st_mtime <= vc.stat().st_mtime <= wj.stat().st_mtime
    if not fresh:                                  # the voice stage already cleaned + aligned this take
        clean_align(L, ep)
    if L.dry:
        return
    dur = duration(ep / ".cache" / "voice_clean.wav")
    fmt = json.loads((ROOT / "brand" / "tokens.json").read_text())["formats"][str(a.format)]["seconds"]
    total = dur + OUTRO_S
    print(f"  voice {dur:.1f} s + outro ≈ {total:.1f} s (format {fmt[0]}–{fmt[1]} s)")
    if not fmt[0] <= total <= fmt[1] and not a.accept_length:
        stop(ep, f"voice is {dur:.1f} s (+ outro ≈ {total:.1f} s) — outside {fmt[0]}–{fmt[1]} s",
             "trim/extend the script (new review round) or accept it, then --from align")


def draft(L: Line, ep: Path) -> int:
    return L.sh(PY, "pipeline/make_reel.py", str(ep), "--from", "validate", "--quality", "draft", check=False)


def st_edit(L: Line, ep: Path, a) -> None:
    e = ep.relative_to(ROOT)
    wt, wj = ep / ".cache" / "words.txt", ep / ".cache" / "words.json"
    if wj.exists() and (not wt.exists() or wt.stat().st_mtime < wj.stat().st_mtime):   # episodes aligned before words.txt
        sys.path.insert(0, str(ROOT / "pipeline"))
        from align import words_txt
        wt.write_text(words_txt(json.loads(wj.read_text())))
    start = len(list((ep / "notes").glob("video-review-*.md"))) + 1
    last = MAX_ROUNDS + a.extra_rounds
    for n in range(start, last + 1):
        prev =ep / "notes" / f"video-review-{n - 1}.md"
        if n == 1:
            director(L, ep, f"Plan {e}/scenes/scenes.json from script.md + .cache/words.txt; validate + qa clean.", "edit")
            L.scoped_agent("editor", ep, f"Tighten {e}/scenes/scenes.json (director's first pass); validate + qa clean.", "edit", "first")
        else:
            # only the roles the review routed notes to. A component runs now only for a *blocker* (the frame is
            # broken without it); component polish waits in the backlog for the batch run
            backlog(ep, prev.name, [x for x in notes_for(prev, "component", "polish") if COMP_TAG.search(x)])
            if notes_for(prev, "component", "blocker"):
                L.scoped_agent("component-dev", ep, f"Fix the [component:*] blocker notes in {e}/notes/video-review-{n - 1}.md "
                                 "(skip polish notes and any already done).", "edit", "revision", note=prev)
            if routed(prev, "director"):
                director(L, ep, f"Revise {e}/scenes/scenes.json from the [director] notes in "
                         f"{e}/notes/video-review-{n - 1}.md and .cache/qa.json.", "edit", REVISE_EFFORT)
            if routed(prev, "editor"):
                L.scoped_agent("editor", ep, f"Apply the [editor] notes in {e}/notes/video-review-{n - 1}.md to "
                               f"{e}/scenes/scenes.json (skip any already resolved).", "edit", "revision", note=prev)
        if draft(L, ep):            # qa blocked the render: one fix pass, then try again
            director(L, ep, f"qa blocked the render of {e}: fix every error in .cache/qa.json "
                     "(route [editor] timing errors too). Validate + qa clean.", "edit", REVISE_EFFORT)
            if draft(L, ep):
                stop(ep, "qa still blocks the draft render after a fix pass", "see .cache/qa.json")
        L.scoped_agent("video-reviewer", ep, f"Review the draft of {e}, round {n} → notes/video-review-{n}.md.",
                       "edit", "review", note=prev if n > 1 else None)
        v = verdict(ep / "notes" / f"video-review-{n}.md")
        print(f"  video review {n}: {v}")
        if v == "PASS":
            polish(L, ep, ep / "notes" / f"video-review-{n}.md")
            return
    stop(ep, f"video review: no PASS after {last} rounds",
         f"last notes: notes/video-review-{last}.md · draft: output/final.mp4 · "
         "options: fix specific notes then --from deliver, or one more round with --from edit --extra-rounds N")


def qa_clean(L: Line, ep: Path) -> bool:
    return all(L.sh(PY, "pipeline/make_reel.py", str(ep), "--only", st, check=False) == 0 for st in ("validate", "build", "qa"))


def polish(L: Line, ep: Path, review: Path) -> None:
    """A PASS still carries the reviewer's polish notes (an empty frame, a chart at 60 % width, a 0.8 s blink) — they
    used to be dropped on the way to delivery. One cheap pass applies them; if qa isn't clean afterwards, the
    reviewed plan is restored, so polish can never cost the PASS."""
    e = ep.relative_to(ROOT)
    backlog(ep, review.name, [x for x in notes_for(review, "component") if COMP_TAG.search(x)])
    d, ed = notes_for(review, "director"), notes_for(review, "editor")
    if not (d or ed) or L.dry:
        return
    sj = ep / "scenes" / "scenes.json"
    keep = sj.read_text()
    rule = ("Polish pass after a PASS, no review follows: apply these notes where they're cheap and safe, change nothing "
            "else, stay inside CLAUDE.md; skip a note you can't do cleanly and say why. Validate + qa clean.")
    print(f"  polish: {len(d)} director + {len(ed)} editor note(s) from {review.name}")
    if d:
        director(L, ep, f"{rule} The [director] notes in {e}/notes/{review.name} (+ qa.json warnings routed to "
                 "director: late-content, narrow-frame, small-object).", "edit", REVISE_EFFORT)
    if ed:
        L.scoped_agent("editor", ep, f"{rule} The [editor] notes in {e}/notes/{review.name}.",
                       "edit", "revision", note=review)
    if not qa_clean(L, ep):
        sj.write_text(keep)
        qa_clean(L, ep)
        print("  ⚠ polish broke qa — restored the reviewed scenes.json")


def st_components(L: Line, ep: Path, a) -> None:
    """Batch-build the shared component backlog (run weekly, or before a reel that needs one) — one component-dev
    session for many requests instead of a run inside every episode."""
    open_items = [x for x in (BACKLOG.read_text().splitlines() if BACKLOG.exists() else []) if x.startswith("- [ ]")]
    if not open_items:
        print("  components/_backlog.md: nothing open")
        return
    L.agent("component-dev", f"Work through the open items in components/_backlog.md ({len(open_items)} open): the "
            "most-requested / most reusable first, at most 4 this run. For each: build or fix it, run "
            "pipeline/component_gallery.py <name>, check its preview.png, then tick it `- [x]` with a 6-word note. "
            "A request a scenes.json param already covers → tick it with that param.", "components")


def st_fix(L: Line, ep: Path, a) -> None:
    """The creator's 'fix it and ship' after a 3-round stop: the routed roles apply the LAST review's notes once,
    headless (never in the producer session), then validate/build/qa must be clean. No new review round."""
    e = ep.relative_to(ROOT)
    n = len(list((ep / "notes").glob("video-review-*.md")))
    if not n:
        sys.exit("produce: --only fix needs a notes/video-review-*.md")
    notes = f"{e}/notes/video-review-{n}.md"
    final = ("Final targeted pass, no review round follows: fix exactly these notes, keep everything else as it is, "
             "and stay within CLAUDE.md (stamp budget, safe zones) — if a note is impossible under it, skip it and say why.")
    if routed(ep / "notes" / f"video-review-{n}.md", "component"):
        L.scoped_agent("component-dev", ep, f"Fix the [component:*] notes in {notes}. {final}",
                       "fix", "revision", note=ep / "notes" / f"video-review-{n}.md")
    if routed(ep / "notes" / f"video-review-{n}.md", "director"):
        director(L, ep, f"Revise {e}/scenes/scenes.json from the [director] notes in {notes} and .cache/qa.json. {final}",
                 "fix", REVISE_EFFORT)
    if routed(ep / "notes" / f"video-review-{n}.md", "editor"):
        L.scoped_agent("editor", ep, f"Apply the [editor] notes in {notes} to {e}/scenes/scenes.json. {final}",
                       "fix", "revision", note=ep / "notes" / f"video-review-{n}.md")
    if not qa_clean(L, ep):
        director(L, ep, f"qa blocks {e}: fix every error in .cache/qa.json (route [editor] timing errors too). "
                 "Validate + qa clean.", "fix", REVISE_EFFORT)
        if not qa_clean(L, ep):
            stop(ep, "qa still blocks after the fix pass", "see .cache/qa.json")
    print("  fix pass done, qa clean → --from deliver")


def st_deliver(L: Line, ep: Path, a) -> None:
    L.sh(PY, "pipeline/make_reel.py", str(ep), "--from", "validate", "--quality", "delivery")
    print("  → look at output/contact_sheet.png before calling it done (CLAUDE.md §8)")


def st_package(L: Line, ep: Path, a) -> None:
    L.agent("packager", f"Write {ep.relative_to(ROOT)}/output/post.md.", "package")


def st_usage(L: Line, ep: Path, a) -> None:
    if not L.log.exists():
        return
    recs = [json.loads(x) for x in L.log.read_text().splitlines() if x.strip()]
    by: dict[str, dict] = {}
    for r in recs:
        s = by.setdefault(r["stage"], {"cost": 0.0, "runs": 0, "turns": 0, "prompt_chars": 0, "cache_read": 0})
        s["cost"] += r["cost"]; s["runs"] += 1; s["turns"] += r["turns"] or 0
        s["prompt_chars"] += r.get("prompt_chars", 0)
        s["cache_read"] += r.get("tokens", {}).get("cache_read_input_tokens", 0)
    total = sum(s["cost"] for s in by.values())
    rounds = {k: len(list((ep / "notes").glob(f"{k}-review-*.md"))) for k in ("script", "video")}
    lines = [f"# Usage — {ep.name} (agent runs, from notes/usage.jsonl)", "",
             "| stage | runs | turns | prompt chars | cached read tokens | cost |", "|---|---:|---:|---:|---:|---:|"]
    lines += [f"| {k} | {v['runs']} | {v['turns']} | {v['prompt_chars']:,} | {v['cache_read']:,} | ${v['cost']:.2f} |" for k, v in by.items()]
    lines += [f"| **total** | {sum(v['runs'] for v in by.values())} | {sum(v['turns'] for v in by.values())} | "
              f"{sum(v['prompt_chars'] for v in by.values()):,} | {sum(v['cache_read'] for v in by.values()):,} | **${total:.2f}** |", "",
              f"Review rounds: script {rounds['script']} · video {rounds['video']}."]
    script_reviews = sorted((ep / "notes").glob("script-review-*.md"), key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    video_reviews = sorted((ep / "notes").glob("video-review-*.md"), key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    if script_reviews:
        score = next((x.strip() for x in script_reviews[-1].read_text().splitlines() if x.lower().startswith("scores:")), "scores not recorded")
        lines.append(f"Latest script quality: {score}")
    if video_reviews:
        review_text = video_reviews[-1].read_text()
        risk = next((x.strip() for x in review_text.splitlines() if x.lower().startswith("swipe risk:")), "swipe risk not recorded")
        blockers = len(re.findall(r"^\s*-\s*\[[^\]]+\]\s*blocker\b", review_text, re.M | re.I))
        polish_n = len(re.findall(r"^\s*-\s*\[[^\]]+\]\s*polish\b", review_text, re.M | re.I))
        lines.append(f"Latest video quality: {risk} · blockers {blockers} · polish notes {polish_n}")
    qa_path = ep / ".cache" / "qa.json"
    if qa_path.exists():
        try:
            qa = json.loads(qa_path.read_text())
            errors = qa.get("errors", 0); warnings = qa.get("warnings", 0)
            errors = errors if isinstance(errors, int) else len(errors)
            warnings = warnings if isinstance(warnings, int) else len(warnings)
            lines.append(f"Final mechanical QA: {errors} errors · {warnings} warnings")
        except (json.JSONDecodeError, AttributeError):
            pass
    lines += [
              "Producer session (the main Claude Code session) is not included — note it from `npx ccusage@latest session`."]
    (ep / "notes" / "usage.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


RUN = {"research": st_research, "script": st_script, "factcheck": st_factcheck, "voice": st_voice, "align": st_align,
       "edit": st_edit, "fix": st_fix, "deliver": st_deliver, "package": st_package, "usage": st_usage,
       "components": st_components}


def summary(ep: Path) -> None:
    def grab(p, pat):
        m = re.search(pat, p.read_text(), re.M) if p.exists() else None
        return m.group(1).strip() if m else "—"
    print("\n── summary")
    print("  cover:", grab(ep / "cover.md", r'^cover_text:\s*"([^"]*)"'))
    print("  hook: ", grab(ep / "cover.md", r"^## Hook line.*\n+(.+)"))
    r = subprocess.run([PY, "pipeline/fact_lint.py", str(ep)], cwd=ROOT, capture_output=True, text=True).stdout
    print("  " + next((x.strip() for x in r.splitlines() if "script:" in x), "script: —"))
    for f in ("fact-check.md",):
        print(f"  {f}: {verdict(ep / 'notes' / f)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--topic", default="")
    ap.add_argument("--format", type=int, choices=[30, 60, 90])
    ap.add_argument("--from", dest="frm", choices=STAGES)
    ap.add_argument("--only", choices=STAGES + ["fix", "components"])
    ap.add_argument("--accept-length", action="store_true", help="the creator accepted a voice outside the format range")
    ap.add_argument("--extra-rounds", type=int, default=0,
                    help="review rounds the creator grants past the 3-round cap (existing reviews count)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ep = (ROOT / a.episode).resolve() if not Path(a.episode).is_absolute() else Path(a.episode)
    if a.format is None:
        m = re.search(r"target_seconds:\s*(\d+)", (ep / "script.md").read_text()) if (ep / "script.md").exists() else None
        a.format = int(m.group(1)) if m else 60
    if not (ep / "script.md").exists() and not a.topic:
        sys.exit("produce: new episode needs --topic")
    # default start: research for a new topic, else the script loop
    stages = [a.only] if a.only else STAGES[STAGES.index(a.frm or ("research" if a.topic else "script")):]
    (ep / "notes").mkdir(parents=True, exist_ok=True)
    (ep / "notes" / "STOP.md").unlink(missing_ok=True)
    global DRY
    DRY = a.dry_run
    L = Line(ep, a.dry_run)
    print(f"produce {ep.name}: {' → '.join(stages)}  (cli {L.cli})")
    for st in stages:
        print(f"\n▶ {st}", flush=True)
        RUN[st](L, ep, a)
        if st == "factcheck":
            summary(ep)
    if "usage" not in stages:
        st_usage(L, ep, a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
