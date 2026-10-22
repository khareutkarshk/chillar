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
import budget

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "bin" / "python")
AGENTS = ROOT / ".claude" / "agents"
STAGES = ["research", "script", "factcheck", "voice", "align", "edit", "deliver", "package", "usage"]
MAX_ROUNDS = 3
CULTURE_MIN_FRESH = 4            # Culture now rows that peaked this month or last, before the writer starts
REVISE_EFFORT = "medium"         # director revisions / fix passes (the first plan uses the frontmatter's, medium since 2026-10-21)
REVISE_MODEL = "sonnet"          # director fix/polish passes edit a few scenes from routed notes: Opus only for the first plan
OUTRO_S = 2.0                    # outro receipt after the voice (cuts on the last word, 1.9 s)
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
# "You've hit your session limit · resets 9:50pm (Asia/Kolkata)" arrives as a normal result, not an error
LIMIT_RE = re.compile(r"hit your [\w ]*limit", re.I)
LIMIT_WAIT_MAX = 6 * 3600        # a 5-hour session window resets inside this; a weekly limit doesn't, so that one stops
LIMIT_RETRIES = 2


def limit_wait(text: str) -> float | None:
    """Seconds until the reset named in a limit message (+2 min slack), or None if it names no clock time."""
    m = re.search(r"resets\s+(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*([ap]m)\s*(?:\(([\w/+-]+)\))?", text, re.I)
    if not m:
        return None
    try:
        from zoneinfo import ZoneInfo
        now = dt.datetime.now(ZoneInfo(m.group(4))) if m.group(4) else dt.datetime.now()
    except Exception:
        now = dt.datetime.now()
    at = now.replace(hour=int(m.group(1)) % 12 + (12 if m.group(3).lower() == "pm" else 0),
                     minute=int(m.group(2) or 0), second=0, microsecond=0)
    if at <= now:
        at += dt.timedelta(days=1)
    return (at - now).total_seconds() + 120


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

    def agent(self, name: str, prompt: str, stage: str, effort: str = "", *, model: str = "",
              tools_override: str | None = None, bash_allow: list[str] | None = None) -> str:
        """effort / model (an alias from MODELS) override the frontmatter's (revisions run below the first pass)."""
        meta = frontmatter(name)
        if effort:
            meta["effort"] = effort
        if model:
            meta["model"] = model
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
        b = budget.check()               # an armed batch budget (budget.py start) counts every Claude session here
        if b.get("over"):
            stop(self.ep, f"batch budget reached: ${b['spent']} of ${b['cap']} (≈ {b['pct_now']}% weekly)",
                 "The master stops every reel. Disarm with `.venv/bin/python pipeline/budget.py stop` only if the "
                 "creator raises the limit, then resume with --from <this stage>.")
        for attempt in range(LIMIT_RETRIES + 1):
            t0 = time.time()
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=ENV)
            d, calls = parse_stream(r.stdout)
            if not d:
                d = {"result": (r.stdout + r.stderr)[-2000:], "is_error": True}
            u = d.get("usage", {})
            limited = LIMIT_RE.search(str(d.get("result", "")))
            rec = {"at": dt.datetime.now().isoformat(timespec="seconds"), "stage": stage, "agent": name,
                   "prompt_chars": len(prompt),
                   "models": list(d.get("modelUsage", {})), "cost": round(d.get("total_cost_usd", 0) or 0, 4),
                   "turns": d.get("num_turns"), "secs": round(time.time() - t0),
                   "effort": meta.get("effort"),
                   "tokens": {k: u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")},
                   "cache_1h": (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0),
                   "tools": tool_summary(calls),
                   "error": "limit" if limited else
                            d.get("subtype") if d.get("is_error") or d.get("subtype", "success") != "success" else None}
            with self.log.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            if not limited:
                break
            # 2026-11-12 reel: the session limit hit mid-edit, the CLI answered "success" with the limit text, and the
            # line ran qa on a half-written plan, stopped as "qa blocks" and sat 10 h. Wait out the reset, rerun the call.
            text = str(d.get("result", "")).strip()
            wait = limit_wait(text)
            if wait is None or wait > LIMIT_WAIT_MAX or attempt == LIMIT_RETRIES:
                stop(self.ep, f"Claude usage limit hit during {name} ({stage}) — nothing from that run is trusted",
                     f"{text}\nAfter the reset, resume with --from {stage}.")
            print(f"    ⏸ {text} — waiting {wait / 60:.0f} min, then rerunning {name}", flush=True)
            time.sleep(wait)
        if d.get("is_error") and not rec["models"]:      # the agent never ran (auth, CLI crash): its output is not work
            stop(self.ep, f"{name} ({stage}) did not run: {rec['error']}", str(d.get("result", ""))[-1500:])
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
        self.last_error = rec["error"]
        return d.get("result", "")

    def scoped_agent(self, name: str, ep: Path, task: str, stage: str, mode: str,
                     *, note: Path | None = None, effort: str = "", model: str = "") -> str:
        """Run scene/review work with a bounded brief and only the tools needed for that role."""
        only_blockers = name == "component-dev" and "blocker" in task.lower()
        paths = edit_inputs(ep, name, mode, note, only_blockers=only_blockers)
        catalog = ""
        if name == "director" and mode == "first":
            # the brief cuts any file at 18k chars and the whole brief at 32k: the 27k catalog arrived truncated (and
            # themes/formats/shot-patterns after it), so every first plan re-grepped it, 5–9k chars a call, 15–34 turns.
            # Inline it whole once (≈ 7k tokens, cached) — cheaper than greps whose results ride along every later turn.
            cat_path = ROOT / "components" / "_catalog.md"
            paths = [p for p in paths if p.name != "_catalog.md"]
            catalog = (f"\n--- components/_catalog.md (complete — do not open or grep it) ---\n"
                       f"{cat_path.read_text()}\n") if cat_path.exists() else ""
        brief = build_brief(ep, name, mode, task, paths, note=note,
                            max_chars=32000 if name == "director" and mode == "first" else 24000) + catalog
        prompt = (f"{task}\n\nUse this bounded context brief as your source set; do not rediscover context "
                  f"with broad shell reads. Brief size: {len(brief)} chars.\n\n{brief}")
        tools = {
            "director": "Read,Write,Edit,Bash",
            "editor": "Read,Edit,Bash",
            "video-reviewer": "Read,Write,Bash",
            "component-dev": "Read,Write,Edit,Bash",
            "voice": "Read,Write,Edit",
            "scriptwriter": "Read,Write,Edit,Bash",
            "script-reviewer": "Read,Write,Bash",
        }.get(name)
        return self.agent(name, prompt, stage, effort, model=model, tools_override=tools,
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
    open_for = {m.group(1) for ln in have.splitlines() if ln.startswith("- [ ]") for m in COMP_TAG.finditer(ln)}
    new = []
    for x in items:
        body = re.sub(r"^\s*[-*\d.]+\s*", "", x).strip()
        names = set(COMP_TAG.findall(body))
        if names and names <= open_for:          # already open for this component — the batch run reads it there
            continue
        open_for |= names
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
    if mode == "first":
        prompt += (" Budget: the whole catalog is below — never grep or reopen it. Write scenes.json, run validate, then "
                   "`qa.py --for director` once, fix every ✗ in one batch of edits, run validate + qa once more and stop "
                   "(a third run only if that one still shows a ✗). No grep|qa loops, no output filters on qa.")
    # fix / polish passes edit a handful of scenes from routed notes — Sonnet does that at ~1/5 of Opus
    L.scoped_agent("director", ep, prompt, stage, mode, note=note, effort=effort,
                   model="" if mode == "first" else REVISE_MODEL)
    if L.dry:
        return
    backlog(ep, L.last_out.name, [x for x in L.last_out.read_text().splitlines() if COMP_TAG.search(x)])


NOTE_LINE = re.compile(r"^\s*-\s*\[([^\]]+)\]\s*(blocker|polish)?(.*)$", re.M)


def notes_for(review: Path, who: str, sev: str | None = None) -> list[str]:
    """Note lines routed to `who` (director / editor / component / voice), optionally only one severity."""
    if not review.exists():
        return []
    out = []
    for m in NOTE_LINE.finditer(review.read_text()):
        owners = {r.strip().split(":")[0] for r in m.group(1).split("|")}
        if who in owners and (sev is None or (m.group(2) or "blocker") == sev):
            out.append(m.group(0).strip())
    return out


def repair_voice(L: Line, ep: Path, review: Path, stage: str) -> None:
    """Handle reviewer-owned voice blockers once, then realign before any scene render."""
    e = ep.relative_to(ROOT)
    notes = "\n".join(notes_for(review, "voice", "blocker"))
    if not notes:
        return
    blocker_ids = set(re.findall(r"\bL\d+\b", notes))
    vc = ep / ".cache" / "voice_check.json"
    # 2026-11 batch: the repair agent re-applied the reviewer's respelling that had already failed → the same stop
    # twice. Every spelling Sunny was heard to miss is kept per line and shown with what whisper heard, never reused.
    tried_p = ep / ".cache" / "voice_failed.json"
    tried: dict[str, list[str]] = json.loads(tried_p.read_text()) if tried_p.exists() else {}
    rows = {r["line"]: r for r in json.loads(vc.read_text()).get("rows", [])} if vc.exists() else {}
    for lid in sorted(blocker_ids):
        r = rows.get(lid)
        if r and r["tts"] not in tried.setdefault(lid, []):
            tried[lid].append(r["tts"])
    evidence = "\n".join(
        f"- {lid}: heard \"{rows[lid]['heard'] if lid in rows else '?'}\" · flags {'; '.join(rows[lid]['flags']) or '—' if lid in rows else '?'}"
        f" · spellings that already failed (never reuse, not even the reviewer's suggestion if it is one of these): "
        + " | ".join(f'"{t}"' for t in tried.get(lid, [])) for lid in sorted(blocker_ids))
    if not L.dry:
        tried_p.write_text(json.dumps(tried, ensure_ascii=False, indent=1))
    L.scoped_agent("voice", ep,
                   f"Fix only these voice blockers from {e}/notes/{review.name}. Compare each line with "
                   f".cache/voice_check.md. Prefer a pronunciation respelling in voice/tts.txt or "
                   f"brand/pronunciations.tsv that preserves the approved script words exactly. Do not edit "
                   f"script.md or scenes. Each blocker line below lists what the voice-check heard and every "
                   f"spelling that already failed: a new spelling must differ from all of them (a different "
                   f"syllable split, Latin vs Devanagari, or a pronunciations.tsv row). If no safe new respelling "
                   f"fixes a genuinely unclear line, leave it unchanged and report it unresolved so the pipeline "
                   f"can stop for a creator decision.\n\n{notes}\n\nCurrent voice check + failed spellings:\n{evidence}",
                   stage, "revision", note=review)
    if L.dry:
        return
    L.sh(PY, "pipeline/tts.py", str(ep))
    clean_align(L, ep)
    L.sh(PY, "pipeline/voice_check.py", str(ep), check=False)
    if not vc.exists():
        stop(ep, "voice repair did not produce a voice-check report", "Inspect the TTS and alignment output before resuming.")
    data = json.loads(vc.read_text())
    flagged = [r for r in data.get("rows", []) if r.get("line") in blocker_ids and r.get("flags")]
    for r in flagged:
        if r["tts"] not in tried.setdefault(r["line"], []):
            tried[r["line"]].append(r["tts"])
    tried_p.write_text(json.dumps(tried, ensure_ascii=False, indent=1))
    # every word of the line heard inside its padded window (match 100 %) = Sunny says it; a leftover nasal/ASR flag
    # alone isn't worth a creator stop. A number flag still stops: a line with no Hindi words scores 100 % by default.
    remaining = [r["line"] for r in flagged
                 if r.get("match", 0) < 1.0 or any(f.startswith("number") for f in r["flags"])]
    if flagged and not remaining:
        print(f"  voice re-take: {', '.join(r['line'] for r in flagged)} still flagged, but every word is heard — continuing")
    if remaining:
        stop(ep, f"voice blockers remain after one targeted re-take: {', '.join(remaining)}",
             "Listen to these lines, then correct voice/tts.txt or mark the reviewer note resolved before resuming. "
             "Spellings already tried per line: .cache/voice_failed.json.")


def blocker_signature(review: Path) -> set[tuple[str, str]]:
    """Stable enough to catch a review round that repeats the same blockers without progress."""
    if not review.exists():
        return set()
    out = set()
    for m in NOTE_LINE.finditer(review.read_text()):
        if (m.group(2) or "blocker").lower() != "blocker":
            continue
        owners = ",".join(sorted(x.strip().split(":")[0] for x in m.group(1).split("|")))
        body = m.group(3)
        line_id = re.search(r"\bL\d+\b", body)
        timestamp = re.search(r"\bt\s*=\s*[\d.]+", body)
        anchor = line_id.group(0).lower() if line_id else (re.sub(r"\s+", "", timestamp.group(0).lower()) if timestamp else re.sub(r"\s+", " ", body.lower()).strip()[:100])
        out.add((owners, anchor))
    return out


# ------------------------------------------------------------------ stages
def st_research(L: Line, ep: Path, a) -> None:
    if not (ep / "script.md").exists():
        shutil.copytree(ROOT / "episodes" / "_template", ep, dirs_exist_ok=True)
    s = (ep / "script.md").read_text()
    s = re.sub(r"target_seconds: \d+", f"target_seconds: {a.format}", s)
    (ep / "script.md").write_text(s)
    L.sh(PY, "pipeline/source_index.py", "sync", check=False)
    L.agent("researcher", f"Research {ep.relative_to(ROOT)} — topic: {a.topic}. Format {a.format} s.", "research")
    rows = facts_rows_lint(ep)      # 2026-10-30: two URL-less "do not use" rows rode through every script round to a BLOCK
    if rows and not L.dry:
        print(f"  facts gate: {len(rows)} facts.md row problem(s) → researcher, before the writer")
        L.agent("researcher", f"Fix only these facts.md rows in {ep.relative_to(ROOT)} (source each one, or move it out of "
                "the table under `## Not usable (unverified)`), then re-run fact_lint: " + " | ".join(rows[:10]), "research")
    if L.dry:
        return
    # fresh lowest script score on both 11-batch 60 s reels: the pool held a recent reel's meme and last month's rows
    import memes
    from types import SimpleNamespace
    dropped, fresh = memes.prune_culture(SimpleNamespace(dir=ep))
    if dropped:
        print(f"  culture gate: dropped {len(dropped)} row(s) a recent reel used: {', '.join(dropped)}")
    if fresh < CULTURE_MIN_FRESH:
        print(f"  culture gate: {fresh} Culture now row(s) peaked this month or last → researcher tops it up")
        L.agent("researcher", f"Top up only `## Culture now` in {ep.relative_to(ROOT)}/facts.md: it has {fresh} row(s) "
                f"that peaked this month or last; reach {CULTURE_MIN_FRESH}+. Run `.venv/bin/python pipeline/memes.py "
                f"trending --episode {ep.relative_to(ROOT)}` (and `--kind sound`), pick rows that fit this topic's "
                "beats, keep the row format. Touch nothing else.", "research", "low")


def facts_rows_lint(ep: Path) -> list[str]:
    """fact_lint problems that belong to facts.md rows (`F3: …`), not to the script."""
    r = subprocess.run([PY, "pipeline/fact_lint.py", str(ep), "--json"], cwd=ROOT, capture_output=True, text=True)
    try:
        return [p for p in json.loads(r.stdout).get("problems", []) if re.match(r"F\d+:", p)]
    except json.JSONDecodeError:
        return []


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
    to the writer once, before an Opus review is spent finding them: 5 of 6 first reviews failed on exactly these.
    Recheck after the repair so a still-invalid draft never reaches the paid reviewer."""
    if L.dry:
        return
    def mechanical_misses() -> list[str] | None:
        r = subprocess.run([PY, "pipeline/fact_lint.py", str(ep), "--json"], cwd=ROOT, capture_output=True, text=True)
        try:
            j = json.loads(r.stdout)
        except json.JSONDecodeError:
            return None
        miss = [p for p in j.get("problems", []) if not re.match(r"F\d+:", p)]  # facts.md rows aren't the writer's
        miss += [w for w in j.get("warnings", []) if "already used in" in w or "classic meme budget" in w]  # reused / too many classics
        miss += [s for s in j.get("script", [])[1:] if re.search(r"outside|first laugh|minimum|absolute|support an|takeaway|follow_up|jargon|open_loop", s)]
        return miss

    miss = mechanical_misses()
    if miss is None:
        return
    if not miss:
        return
    print(f"  lint gate: {len(miss)} mechanical miss(es) → writer, before the review")
    L.scoped_agent("scriptwriter", ep, f"Before review: fix only these fact_lint misses in {ep.relative_to(ROOT)}/script.md, "
                   "keep every joke that isn't involved, re-run fact_lint until they're gone. Misses: " + " | ".join(miss[:10]),
                   "script", "revision", effort=REVISE_EFFORT)
    remaining = mechanical_misses()
    if remaining:
        stop(ep, "mechanical script lint still fails after one targeted repair",
             "Remaining misses: " + " | ".join(remaining[:10]) +
             "\nFix these in script.md, then resume with --from script. The script reviewer was skipped.")


def st_script(L: Line, ep: Path, a) -> None:
    e = ep.relative_to(ROOT)
    start = len(list((ep / "notes").glob("script-review-*.md"))) + 1
    fix = ""
    if start > 1 and verdict(ep / "notes" / f"script-review-{start - 1}.md") == "PASS":
        fix = length_miss(L, ep, a)              # resumed after a length stop: the writer gets the length fix, not the notes
        if not fix:
            return
    last = MAX_ROUNDS + a.extra_rounds           # rounds past the cap only when the creator grants them
    for n in range(start, last + 1):
        if n == 1:
            L.sh(PY, "pipeline/joke_log.py", check=False)         # writers' room memory: games taken, what landed / fell flat
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
        # Re-run mechanical checks after every write, including measured length fixes.
        # Otherwise a length-only rewrite can regress facts or written-length bounds before review.
        lint_gate(L, ep)
        prior = ep / "notes" / f"script-review-{n - 1}.md" if n > 1 else None
        L.scoped_agent("script-reviewer", ep, f"Review {e}/script.md, round {n}." +
                       (" This is a length-only fix: check changed lines and preserve the rest." if fix else "") +
                       (f" Verify unresolved items in {prior.relative_to(ROOT)}, then assess the current draft." if prior else ""),
                       "script", "revision" if prior else "first", note=prior,
                       effort=REVISE_EFFORT if prior else "")     # round 1 judges cold at high; 2+ checks known notes
        # the reviewer's picks among the writer's {alt: …} lines — a punch-up without another round
        L.sh(PY, "pipeline/script_picks.py", str(ep), "--review", str(ep / "notes" / f"script-review-{n}.md"), check=False)
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
        if not script_blocks(fc):       # only facts.md rows block: the fact-checker re-runs, no writer/reviewer round
            print("  fact-check BLOCK is facts.md-only → no script round")
            continue
        n = len(list((ep / "notes").glob("script-review-*.md")))
        fc_note = ep / "notes" / "fact-check.md"
        L.scoped_agent("scriptwriter", ep, f"Fix only the BLOCK rows listed in {e}/notes/fact-check.md in {e}/script.md "
                       "(change nothing else).", "factcheck", "revision", note=fc_note)
        L.scoped_agent("script-reviewer", ep, f"Review only the lines changed for {e}/notes/fact-check.md in {e}/script.md, "
                       f"round {n + 1} (PASS if they're fixed and still funny).", "factcheck", "revision", note=fc_note)
    stop(ep, "fact-check still BLOCK after one fix cycle",
         "see notes/fact-check.md · options: fix the BLOCK rows (facts.md source / script line) then --from factcheck, "
         "or accept a row the creator has verified and --from voice")


def script_blocks(fc: Path) -> bool:
    """Does any blocking row of notes/fact-check.md point at a script line (L#) or an on-screen shot?"""
    rows = [l for l in fc.read_text().splitlines() if l.startswith("|") and re.search(r"❌|⚠", l)]
    return not rows or any(re.match(r"\|\s*(L\d+|scene|shot|on-screen)", l, re.I) for l in rows)


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
    vchk = c / "voice_check.json"                  # a run resumed --from align skipped the voice stage's listen
    if not vchk.exists() or vchk.stat().st_mtime < wj.stat().st_mtime:
        L.sh(PY, "pipeline/voice_check.py", str(ep), check=False)
    dur = duration(ep / ".cache" / "voice_clean.wav")
    fmt = json.loads((ROOT / "brand" / "tokens.json").read_text())["formats"][str(a.format)]["seconds"]
    total = dur + OUTRO_S
    print(f"  voice {dur:.1f} s + outro ≈ {total:.1f} s (format {fmt[0]}–{fmt[1]} s)")
    if not fmt[0] <= total <= fmt[1] and not a.accept_length:
        stop(ep, f"voice is {dur:.1f} s (+ outro ≈ {total:.1f} s) — outside {fmt[0]}–{fmt[1]} s",
             "trim/extend the script (new review round) or accept it, then --from align")


def qa_brief(ep: Path) -> str:
    """Exact qa errors (kind, time, element, box, fix) + the safe-zone limits, inlined into a fix-pass prompt so the
    fixer starts from the failing frames instead of re-deriving them (2 of 4 reels stopped on a first fix pass)."""
    try:
        d = json.loads((ep / ".cache" / "qa.json").read_text())
        z = json.loads((ROOT / "brand" / "tokens.json").read_text())["safeZone"]
    except (OSError, ValueError, KeyError):
        return ""
    errs = [i for i in d.get("issues", []) if i.get("sev") == "error"][:25]
    if not errs:
        return ""
    lines = "\n".join(f"- [{i.get('kind')}] t={i.get('t')} {i.get('where')} -> {i.get('route')}: {i.get('msg')} | fix: {i.get('fix')}"
                      for i in errs)
    return (f"\n\nExact qa errors (fix each, then re-run validate+qa once):\n{lines}\nSafe zone: x {z['left']}-{1080 - z['right']}, "
            f"y {z['top']}-{1920 - z['bottom']}; captions band {z['captionBand']}. A text box needs x+w <= {1080 - z['right']}. "
            "Overlaps: move/shrink one element or shift its reveal frame; mascot and stamps must not cover text.")


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
        sp = ep / "scenes" / "scenes.json"
        planned = ep / ".cache" / "plan_ok"       # director + editor first passes both finished: a stop mid-plan
        if n == 1 and sp.exists() and planned.exists() and wj.exists() and planned.stat().st_mtime > wj.stat().st_mtime:
            print("  scenes.json already planned for this voice — keeping it (delete .cache/plan_ok to re-plan)")
        elif n == 1:                                  # (limit, crash) leaves a half plan, which is re-planned, not kept
            planned.unlink(missing_ok=True)
            director(L, ep, f"Plan {e}/scenes/scenes.json from script.md + .cache/words.txt; validate + qa clean.", "edit")
            ok = not getattr(L, "last_error", None)
            L.scoped_agent("editor", ep, f"Tighten {e}/scenes/scenes.json (director's first pass); validate + qa clean.", "edit", "first")
            if ok and not getattr(L, "last_error", None) and not L.dry:
                planned.touch()
        else:
            # only the roles the review routed notes to. A component runs now only for a *blocker* (the frame is
            # broken without it); component polish waits in the backlog for the batch run
            backlog(ep, prev.name, [x for x in notes_for(prev, "component", "polish") if COMP_TAG.search(x)])
            component_output = ""
            if notes_for(prev, "component", "blocker"):
                L.scoped_agent("component-dev", ep, f"Fix the [component:*] blocker notes in {e}/notes/video-review-{n - 1}.md "
                                 "(skip polish notes and any already done).", "edit", "revision", note=prev)
                component_output = L.last_out.read_text() if getattr(L, "last_out", None) and L.last_out.exists() else ""
            if notes_for(prev, "voice", "blocker"):
                repair_voice(L, ep, prev, "edit")
            if routed(prev, "director") or component_output:
                wiring = ("\n\nComponent implementation handoff (apply its episode-level param advice in scenes.json; "
                          "do not leave the same QA finding unresolved):\n" + component_output[:4000]) if component_output else ""
                director(L, ep, f"Revise {e}/scenes/scenes.json from the [director] notes in "
                         f"{e}/notes/video-review-{n - 1}.md and .cache/qa.json.{wiring}", "edit", REVISE_EFFORT)
            if routed(prev, "editor"):
                L.scoped_agent("editor", ep, f"Apply the [editor] notes in {e}/notes/video-review-{n - 1}.md to "
                               f"{e}/scenes/scenes.json (skip any already resolved).", "edit", "revision", note=prev)
        if draft(L, ep):            # qa blocked the render: one fix pass, then try again
            director(L, ep, f"qa blocked the render of {e}: fix every error in .cache/qa.json "
                     "(route [editor] timing errors too). Validate + qa clean." + qa_brief(ep), "edit", REVISE_EFFORT)
            if draft(L, ep):
                stop(ep, "qa still blocks the draft render after a fix pass", "see .cache/qa.json")
        L.scoped_agent("video-reviewer", ep, f"Review the draft of {e}, round {n} → notes/video-review-{n}.md.",
                       "edit", "review", note=prev if n > 1 else None)
        v = verdict(ep / "notes" / f"video-review-{n}.md")
        print(f"  video review {n}: {v}")
        if v == "PASS":
            polish(L, ep, ep / "notes" / f"video-review-{n}.md")
            return
        if n > 1:
            current = blocker_signature(ep / "notes" / f"video-review-{n}.md")
            previous = blocker_signature(ep / "notes" / f"video-review-{n - 1}.md")
            if current and current == previous:
                stop(ep, f"video review repeated the same {len(current)} blocker(s) with no progress in round {n}",
                     f"Review notes: notes/video-review-{n}.md. Resolve those blockers, then resume with --from edit.")
    stop(ep, f"video review: no PASS after {last} rounds",
         f"last notes: notes/video-review-{last}.md · draft: output/final.mp4 · "
         "options: fix specific notes then --from deliver, or one more round with --from edit --extra-rounds N")


def qa_clean(L: Line, ep: Path) -> bool:
    return all(L.sh(PY, "pipeline/make_reel.py", str(ep), "--only", st, check=False) == 0 for st in ("validate", "build", "qa"))


POLISH_QA = ("late-content", "late-text", "empty-paper", "narrow-frame", "small-object", "mascot-on-text", "top-heavy")   # qa warns polish fixes


def polish(L: Line, ep: Path, review: Path) -> None:
    """A PASS still carries the reviewer's polish notes (an empty frame, a chart at 60 % width, a 0.8 s blink) — they
    used to be dropped on the way to delivery. One cheap pass applies them; if qa isn't clean afterwards, the
    reviewed plan is restored, so polish can never cost the PASS."""
    e = ep.relative_to(ROOT)
    backlog(ep, review.name, [x for x in notes_for(review, "component") if COMP_TAG.search(x)])
    d, ed = notes_for(review, "director"), notes_for(review, "editor")
    try:        # blank paper on screen (late-text / empty-paper) fired on 5 of 6 reels and nobody was ever sent to fix it
        qa_warns = [i for i in json.loads((ep / ".cache" / "qa.json").read_text()).get("issues", [])
                    if i.get("sev") == "warn" and i.get("kind") in POLISH_QA and "director" in str(i.get("route", ""))]
    except (OSError, ValueError, AttributeError):
        qa_warns = []
    if not (d or ed or qa_warns) or L.dry:
        return
    sj = ep / "scenes" / "scenes.json"
    keep = sj.read_text()
    rule = ("Polish pass after a PASS, no review follows: apply these notes where they're cheap and safe, change nothing "
            "else, stay inside CLAUDE.md; skip a note you can't do cleanly and say why. Validate + qa clean.")
    print(f"  polish: {len(d)} director + {len(ed)} editor note(s) from {review.name} + {len(qa_warns)} qa warning(s)")
    if d or qa_warns:
        director(L, ep, f"{rule} The [director] notes in {e}/notes/{review.name} (+ qa.json warnings routed to "
                 f"director: {', '.join(POLISH_QA)}).", "edit", REVISE_EFFORT)
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
    review = ep / "notes" / f"video-review-{n}.md"
    if notes_for(review, "voice", "blocker"):
        repair_voice(L, ep, review, "fix")
    component_output = ""
    if routed(ep / "notes" / f"video-review-{n}.md", "component"):
        L.scoped_agent("component-dev", ep, f"Fix the [component:*] notes in {notes}. {final}",
                       "fix", "revision", note=ep / "notes" / f"video-review-{n}.md")
        component_output = L.last_out.read_text() if getattr(L, "last_out", None) and L.last_out.exists() else ""
    if routed(review, "director") or component_output:
        wiring = ("\n\nComponent implementation handoff (apply episode-level param advice in scenes.json):\n" +
                  component_output[:4000]) if component_output else ""
        director(L, ep, f"Revise {e}/scenes/scenes.json from the [director] notes in {notes} and .cache/qa.json. {final}{wiring}",
                 "fix", REVISE_EFFORT)
    if routed(review, "editor"):
        L.scoped_agent("editor", ep, f"Apply the [editor] notes in {notes} to {e}/scenes/scenes.json. {final}",
                       "fix", "revision", note=review)
    if not qa_clean(L, ep):
        director(L, ep, f"qa blocks {e}: fix every error in .cache/qa.json (route [editor] timing errors too). "
                 "Validate + qa clean." + qa_brief(ep), "fix", REVISE_EFFORT)
        if not qa_clean(L, ep):
            stop(ep, "qa still blocks after the fix pass", "see .cache/qa.json")
    print("  fix pass done, qa clean → --from deliver")


def st_deliver(L: Line, ep: Path, a) -> None:
    L.sh(PY, "pipeline/make_reel.py", str(ep), "--from", "validate", "--quality", "delivery")
    print("  → look at output/contact_sheet.png before calling it done (CLAUDE.md §8)")


def st_package(L: Line, ep: Path, a) -> None:
    post = ep / "output" / "post.md"
    inputs = [ep / n for n in ("script.md", "facts.md", "cover.md", "notes/fact-check.md")]
    if a.only != "package" and post.exists() and all(post.stat().st_mtime > p.stat().st_mtime for p in inputs if p.exists()):
        print("  post.md is newer than script/facts/cover/fact-check — kept (--only package rewrites it)")
        return
    L.agent("packager", f"Write {ep.relative_to(ROOT)}/output/post.md.", "package")


def st_usage(L: Line, ep: Path, a) -> None:
    if not L.log.exists():
        return
    report_path = ep / "notes" / "usage.md"
    previous_report = report_path.read_text() if report_path.exists() else ""
    producer_section = ""
    if (m := re.search(r"(?m)^## Producer session.*$", previous_report)):
        producer_section = previous_report[m.start():].strip()
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
             f"Updated: {dt.datetime.now():%Y-%m-%d %H:%M} local time. Agent totals exclude the interactive producer session and external services such as TTS.", "",
             "| stage | runs | turns | prompt chars | cached read tokens | cost |", "|---|---:|---:|---:|---:|---:|"]
    lines += [f"| {k} | {v['runs']} | {v['turns']} | {v['prompt_chars']:,} | {v['cache_read']:,} | ${v['cost']:.2f} |" for k, v in by.items()]
    lines += [f"| **total** | {sum(v['runs'] for v in by.values())} | {sum(v['turns'] for v in by.values())} | "
              f"{sum(v['prompt_chars'] for v in by.values()):,} | {sum(v['cache_read'] for v in by.values()):,} | **${total:.2f}** |", "",
              f"Review rounds: script {rounds['script']} · video {rounds['video']}."]
    source_log = ep / "notes" / "source-search.jsonl"
    if source_log.exists():
        try:
            searches = [json.loads(x) for x in source_log.read_text().splitlines() if x.strip()]
            sources = {}
            for item in searches:
                sources.update(item.get("sources", {}))
            excerpt_chars = sum(x.get("excerpt_chars", 0) for x in searches)
            hit_count = sum(x.get("hits", 0) for x in searches)
            matched_chars = sum(x.get("chars", 0) for x in sources.values())
            lines.append(f"Local source retrieval: {len(searches)} searches · {hit_count} excerpts · "
                         f"{excerpt_chars:,} chars returned from {matched_chars:,} chars of matched sources")
        except (json.JSONDecodeError, AttributeError, TypeError):
            lines.append("Local source retrieval: search log could not be summarized")
    script_reviews = sorted((ep / "notes").glob("script-review-*.md"), key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    video_reviews = sorted((ep / "notes").glob("video-review-*.md"), key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    if script_reviews:
        score = next((x.strip() for x in script_reviews[-1].read_text().splitlines() if x.lower().startswith("scores:")), "scores not recorded")
        lines.append(f"Latest script quality: {score}")
        ev = next((x.strip() for x in script_reviews[-1].read_text().splitlines() if x.lower().startswith("evidence:")), "")
        if ev:
            lines.append(f"Score evidence: {ev[9:].strip()}")
    if video_reviews:
        review_text = video_reviews[-1].read_text()
        risk = next((x.strip() for x in review_text.splitlines() if x.lower().startswith("swipe risk:")), "swipe risk not recorded")
        blockers = len(re.findall(r"^\s*-\s*\[[^\]]+\]\s*blocker\b", review_text, re.M | re.I))
        polish_n = len(re.findall(r"^\s*-\s*\[[^\]]+\]\s*polish\b", review_text, re.M | re.I))
        # the delivery render always follows the review; what matters is whether the reviewed plan changed after it
        plan = ep / "scenes" / "scenes.json"
        changed = plan.exists() and plan.stat().st_mtime > video_reviews[-1].stat().st_mtime
        freshness = ("" if not changed else " · polished after this PASS (qa-guarded, not re-reviewed: look at the "
                     "contact sheet)" if verdict(video_reviews[-1]) == "PASS" else " · STALE: scenes.json changed after this review")
        lines.append(f"Latest reviewer report: {risk} · blockers {blockers} · polish notes {polish_n}{freshness}")
    if ep.name[:10] and re.fullmatch(r"\d{4}-\d{2}-\d{2}", ep.name[:10]):
        try:
            post_date = dt.date.fromisoformat(ep.name[:10])
            script_text = (ep / "script.md").read_text() if (ep / "script.md").exists() else ""
            if re.search(r'^series:\s*["\']?Chillar Report', script_text, re.M):
                fact_text = (ep / "facts.md").read_text() if (ep / "facts.md").exists() else ""
                checked = [dt.date.fromisoformat(x) for x in re.findall(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|", fact_text)]
                latest = max(checked, default=None)
                if latest and (post_date - latest).days > 5:
                    lines.append(f"⚠ Recheck Chillar Report status before posting {post_date}: latest fact check is {latest} (>5 days before post date).")
        except ValueError:
            lines.append("⚠ Could not parse the scheduled posting date or fact check date; verify current claims before posting.")
    qa_path = ep / ".cache" / "qa.json"
    if qa_path.exists():
        try:
            qa = json.loads(qa_path.read_text())
            errors = qa.get("errors", 0); warnings = qa.get("warnings", 0)
            errors = errors if isinstance(errors, int) else len(errors)
            warnings = warnings if isinstance(warnings, int) else len(warnings)
            qa_time = dt.datetime.fromtimestamp(qa_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            lines.append(f"Mechanical QA: {errors} errors · {warnings} warnings (qa.json updated {qa_time})")
        except (json.JSONDecodeError, AttributeError):
            pass
    if producer_section:
        lines += ["", producer_section]
    else:
        lines += ["", "## Producer session", "", "Not included in the agent table. Record it with `npx ccusage@latest session`."]
    report_path.write_text("\n".join(lines) + "\n")
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
    ap.add_argument("--post-date", help="planned posting date (YYYY-MM-DD); required when starting a new episode")
    ap.add_argument("--from", dest="frm", choices=STAGES)
    ap.add_argument("--only", choices=STAGES + ["fix", "components"])
    ap.add_argument("--accept-length", action="store_true", help="the creator accepted a voice outside the format range")
    ap.add_argument("--extra-rounds", type=int, default=0,
                    help="review rounds the creator grants past the 3-round cap (existing reviews count)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ep = (ROOT / a.episode).resolve() if not Path(a.episode).is_absolute() else Path(a.episode)
    is_new = not (ep / "script.md").exists()
    if is_new and a.topic:
        # The folder is the durable episode identifier, so bind it to its scheduled publishing day.
        date_text = a.post_date
        if not date_text:
            match = re.match(r"^(\d{4}-\d{2}-\d{2})-", ep.name)
            date_text = match.group(1) if match else ""
        try:
            post_date = dt.date.fromisoformat(date_text)
        except ValueError:
            sys.exit("produce: new episode needs --post-date YYYY-MM-DD (the planned posting date)")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_text):
            sys.exit("produce: --post-date must use YYYY-MM-DD")
        if not re.match(r"^\d{4}-\d{2}-\d{2}-", ep.name):
            ep = ep.with_name(f"{post_date.isoformat()}-{ep.name}")
        elif ep.name[:10] != post_date.isoformat():
            sys.exit(f"produce: episode folder date {ep.name[:10]} does not match --post-date {post_date.isoformat()}")
    if a.format is None:
        m = re.search(r"target_seconds:\s*(\d+)", (ep / "script.md").read_text()) if (ep / "script.md").exists() else None
        a.format = int(m.group(1)) if m else 60
    if not (ep / "script.md").exists() and not a.topic:
        sys.exit("produce: new episode needs --topic")
    # default start: research for a new topic, else the script loop
    stages = [a.only] if a.only else STAGES[STAGES.index(a.frm or ("research" if a.topic else "script")):]
    (ep / "notes").mkdir(parents=True, exist_ok=True)
    (ep / "notes" / "STOP.md").unlink(missing_ok=True)
    toml = ep / "episode.toml"
    if a.accept_length and not a.dry_run and toml.exists() and "length_accepted" not in toml.read_text():
        # persist the creator's call so validate_scenes (and every later --from) stops blocking on the format range
        toml.write_text(toml.read_text().replace("[render]\n", "[render]\nlength_accepted = true       "
                                                 "# creator accepted a voice outside the format range\n", 1))
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
