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

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "bin" / "python")
AGENTS = ROOT / ".claude" / "agents"
STAGES = ["research", "script", "factcheck", "voice", "align", "edit", "deliver", "package", "usage"]
MAX_ROUNDS = 3

# frontmatter alias -> pinned model id (update here when the brand moves to a new model)
MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5"}
MIN_CLI = (2, 1, 280)            # oldest Claude Code that serves the models above
# safety caps per agent run (USD) — generous; a run that hits one is logged and flagged, not retried
BUDGET = {"researcher": 1.5, "scriptwriter": 1.5, "script-reviewer": 1.0, "fact-checker": 1.0, "voice": 0.8,
          "director": 3.0, "editor": 1.0, "video-reviewer": 1.0, "component-dev": 2.0, "packager": 0.4}
# Bash the agents may run without a prompt (headless runs can't ask). Everything else is denied.
BASH_OK = [".venv/bin/python", "python3", "npx", "ffmpeg", "ffprobe", "ls", "cat", "head", "tail", "grep", "wc",
           "sed", "jq", "mkdir", "cp", "find", "diff", "cd", "echo", "sort", "uniq", "awk"]
LEAN = ["--strict-mcp-config", "--disable-slash-commands", "--settings", '{"disableAllHooks": true}',
        "--permission-mode", "acceptEdits", "--output-format", "json", "--no-session-persistence"]


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

    def agent(self, name: str, prompt: str, stage: str) -> str:
        meta = frontmatter(name)
        model = MODELS.get(meta.get("model", "sonnet"), meta.get("model", "sonnet"))
        tools = ",".join(t.strip() for t in meta.get("tools", "Read").split(","))
        allow = [t for t in tools.split(",") if t != "Bash"] + ([f"Bash({b}:*)" for b in BASH_OK] if "Bash" in tools else [])
        cmd = [self.cli, "-p", "--agent", name, "--model", model, "--tools", tools, "--allowedTools", " ".join(allow),
               "--max-budget-usd", str(BUDGET.get(name, 1.0)), *LEAN]
        if meta.get("effort"):
            cmd += ["--effort", meta["effort"]]
        cmd.append(prompt)
        print(f"  ▸ {name} ({model}, {meta.get('effort', '-')}) — {prompt[:90]}", flush=True)
        if self.dry:
            return "verdict: PASS (dry run)"
        t0 = time.time()
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except json.JSONDecodeError:
            d = {"result": (r.stdout + r.stderr)[-2000:], "is_error": True}
        u = d.get("usage", {})
        rec = {"at": dt.datetime.now().isoformat(timespec="seconds"), "stage": stage, "agent": name,
               "models": list(d.get("modelUsage", {})), "cost": round(d.get("total_cost_usd", 0) or 0, 4),
               "turns": d.get("num_turns"), "secs": round(time.time() - t0),
               "tokens": {k: u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")},
               "error": d.get("subtype") if d.get("is_error") or d.get("subtype", "success") != "success" else None}
        with self.log.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        n = len(list(self.out.glob(f"{stage}-*.txt"))) + 1
        (self.out / f"{stage}-{n}-{name}.txt").write_text(d.get("result", ""))
        flag = f"  ⚠ {rec['error']}" if rec["error"] else ""
        if rec["models"] and not any(m.startswith(model) for m in rec["models"]):
            flag += f"  ⚠ ran on {rec['models']}, expected {model}"
        print(f"    ${rec['cost']:.2f} · {rec['turns']} turns · {rec['secs']} s{flag}", flush=True)
        if rec["error"] and "budget" in str(rec["error"]):
            print(f"    ⚠ {name} hit its ${BUDGET.get(name)} cap — check its output before trusting it", flush=True)
        return d.get("result", "")

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


def routed(review: Path, who: str) -> bool:
    return review.exists() and f"[{who}" in review.read_text()


# ------------------------------------------------------------------ stages
def st_research(L: Line, ep: Path, a) -> None:
    if not (ep / "script.md").exists():
        shutil.copytree(ROOT / "episodes" / "_template", ep, dirs_exist_ok=True)
    s = (ep / "script.md").read_text()
    s = re.sub(r"target_seconds: \d+", f"target_seconds: {a.format}", s)
    (ep / "script.md").write_text(s)
    L.agent("researcher", f"Research {ep.relative_to(ROOT)} — topic: {a.topic}. Format {a.format} s.", "research")


def st_script(L: Line, ep: Path, a) -> None:
    e = ep.relative_to(ROOT)
    start = len(list((ep / "notes").glob("script-review-*.md"))) + 1
    for n in range(start, MAX_ROUNDS + 1):
        if n == 1:
            topic = f" Topic: {a.topic}." if a.topic else ""
            L.agent("scriptwriter", f"Write {e}/script.md, {a.format} s format.{topic} Fill cover.md first if it still "
                    "has placeholders, and the script.md frontmatter (title, series, concept).", "script")
        else:
            L.agent("scriptwriter", f"Rewrite {e}/script.md from {e}/notes/script-review-{n - 1}.md.", "script")
        L.agent("script-reviewer", f"Review {e}/script.md, round {n}.", "script")
        v = verdict(ep / "notes" / f"script-review-{n}.md")
        print(f"  script review {n}: {v}")
        if v == "PASS":
            return
    stop(ep, f"script review: no PASS after {MAX_ROUNDS} rounds", f"last notes: notes/script-review-{MAX_ROUNDS}.md")


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
        L.agent("scriptwriter", f"Fix only the BLOCK rows listed in {e}/notes/fact-check.md in {e}/script.md "
                "(change nothing else).", "factcheck")
        L.agent("script-reviewer", f"Review only the lines changed for {e}/notes/fact-check.md in {e}/script.md, "
                f"round {n + 1} (PASS if they're fixed and still funny).", "factcheck")
    stop(ep, "fact-check still BLOCK after one fix cycle", "see notes/fact-check.md")


def st_voice(L: Line, ep: Path, a) -> None:
    L.agent("voice", f"Make the voiceover for {ep.relative_to(ROOT)}.", "voice")


def st_align(L: Line, ep: Path, a) -> None:
    L.sh(PY, "pipeline/make_reel.py", str(ep), "--only", "clean")
    L.sh(PY, "pipeline/make_reel.py", str(ep), "--only", "align")
    if L.dry:
        return
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(ep / ".cache" / "voice_clean.wav")], capture_output=True, text=True).stdout or 0)
    fmt = json.loads((ROOT / "brand" / "tokens.json").read_text())["formats"][str(a.format)]["seconds"]
    total = dur + 3.5
    print(f"  voice {dur:.1f} s + outro ≈ {total:.1f} s (format {fmt[0]}–{fmt[1]} s)")
    if not fmt[0] <= total <= fmt[1] and not a.accept_length:
        stop(ep, f"voice is {dur:.1f} s (+ outro ≈ {total:.1f} s) — outside {fmt[0]}–{fmt[1]} s",
             "trim/extend the script (new review round) or accept it, then --from align")


def draft(L: Line, ep: Path) -> int:
    return L.sh(PY, "pipeline/make_reel.py", str(ep), "--from", "validate", "--quality", "draft", check=False)


def st_edit(L: Line, ep: Path, a) -> None:
    e = ep.relative_to(ROOT)
    start = len(list((ep / "notes").glob("video-review-*.md"))) + 1
    for n in range(start, MAX_ROUNDS + 1):
        prev = ep / "notes" / f"video-review-{n - 1}.md"
        if n == 1:
            L.agent("director", f"Plan {e}/scenes/scenes.json from script.md + .cache/words.json; validate + qa clean.", "edit")
            L.agent("editor", f"Tighten {e}/scenes/scenes.json (director's first pass); validate + qa clean.", "edit")
        else:
            # only the roles the review actually routed notes to
            if routed(prev, "component"):
                L.agent("component-dev", f"Fix the [component:*] notes in {e}/notes/video-review-{n - 1}.md.", "edit")
            if routed(prev, "director"):
                L.agent("director", f"Revise {e}/scenes/scenes.json from the [director] notes in "
                        f"{e}/notes/video-review-{n - 1}.md and .cache/qa.json.", "edit")
            if routed(prev, "editor"):
                L.agent("editor", f"Apply the [editor] notes in {e}/notes/video-review-{n - 1}.md to "
                        f"{e}/scenes/scenes.json (skip any already resolved).", "edit")
        if draft(L, ep):            # qa blocked the render: one fix pass, then try again
            L.agent("director", f"qa blocked the render of {e}: fix every error in .cache/qa.json "
                    "(route [editor] timing errors too). Validate + qa clean.", "edit")
            if draft(L, ep):
                stop(ep, "qa still blocks the draft render after a fix pass", "see .cache/qa.json")
        L.agent("video-reviewer", f"Review the draft of {e}, round {n} → notes/video-review-{n}.md.", "edit")
        v = verdict(ep / "notes" / f"video-review-{n}.md")
        print(f"  video review {n}: {v}")
        if v == "PASS":
            return
    stop(ep, f"video review: no PASS after {MAX_ROUNDS} rounds",
         f"last notes: notes/video-review-{MAX_ROUNDS}.md · draft: output/final.mp4 · "
         "options: fix specific notes then --from deliver, or one more round with --from edit")


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
        L.agent("component-dev", f"Fix the [component:*] notes in {notes}. {final}", "fix")
    if routed(ep / "notes" / f"video-review-{n}.md", "director"):
        L.agent("director", f"Revise {e}/scenes/scenes.json from the [director] notes in {notes} and .cache/qa.json. {final}", "fix")
    if routed(ep / "notes" / f"video-review-{n}.md", "editor"):
        L.agent("editor", f"Apply the [editor] notes in {notes} to {e}/scenes/scenes.json. {final}", "fix")
    def clean() -> bool:
        return all(L.sh(PY, "pipeline/make_reel.py", str(ep), "--only", st, check=False) == 0
                   for st in ("validate", "build", "qa"))
    if not clean():
        L.agent("director", f"qa blocks {e}: fix every error in .cache/qa.json (route [editor] timing errors too). "
                "Validate + qa clean.", "fix")
        if not clean():
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
        s = by.setdefault(r["stage"], {"cost": 0.0, "runs": 0, "turns": 0})
        s["cost"] += r["cost"]; s["runs"] += 1; s["turns"] += r["turns"] or 0
    total = sum(s["cost"] for s in by.values())
    rounds = {k: len(list((ep / "notes").glob(f"{k}-review-*.md"))) for k in ("script", "video")}
    lines = [f"# Usage — {ep.name} (agent runs, from notes/usage.jsonl)", "",
             "| stage | runs | turns | cost |", "|---|---|---|---|"]
    lines += [f"| {k} | {v['runs']} | {v['turns']} | ${v['cost']:.2f} |" for k, v in by.items()]
    lines += [f"| **total** | {sum(v['runs'] for v in by.values())} | | **${total:.2f}** |", "",
              f"Review rounds: script {rounds['script']} · video {rounds['video']}.",
              "Producer session (the main Claude Code session) is not included — note it from `npx ccusage@latest session`."]
    (ep / "notes" / "usage.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


RUN = {"research": st_research, "script": st_script, "factcheck": st_factcheck, "voice": st_voice, "align": st_align,
       "edit": st_edit, "fix": st_fix, "deliver": st_deliver, "package": st_package, "usage": st_usage}


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
    ap.add_argument("--only", choices=STAGES + ["fix"])
    ap.add_argument("--accept-length", action="store_true", help="the creator accepted a voice outside the format range")
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
