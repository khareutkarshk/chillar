#!/usr/bin/env python3
"""Build bounded, role-specific text briefs for headless production agents.

The brief is deliberately text-only: image assets are referenced by path and inspected only
by roles that need them. Sources remain authoritative; this is a per-run snapshot, not a new
source of truth.
"""
from __future__ import annotations

import re
from pathlib import Path


def _read(path: Path, limit: int) -> str:
    if not path.exists() or not path.is_file():
        return "[missing]"
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".mp4", ".wav"}:
        return f"[visual/media file; inspect only if your task requires it: {path}]"
    text = path.read_text(errors="replace")
    if len(text) > limit:
        return text[:limit] + f"\n[truncated at {limit} chars; open source only for the missing detail]"
    return text


def _note_for_role(path: Path, role: str, only_blockers: bool = False) -> str:
    """Keep only the hand-off material an agent owns; preserve full prior notes for the reviewer."""
    text = path.read_text(errors="replace")
    if role == "video-reviewer" or path.name == "fact-check.md":
        return text
    if role in {"scriptwriter", "script-reviewer"}:
        keep_sections = {"prior notes", "notes (most important first)", "keep"}
        sections: set[str] = set()
        out = [line for line in text.splitlines() if line.startswith(("verdict:", "round:", "scores:", "words:"))]
        active = ""
        for line in text.splitlines():
            if line.startswith("## "):
                active = line[3:].strip().lower()
                continue
            if active in keep_sections:
                out.append(line)
        return "\n".join(out) or text

    owner = {"director": "director", "editor": "editor", "component-dev": "component"}.get(role)
    if not owner:
        return text
    out = [line for line in text.splitlines() if line.startswith(("verdict:", "round:", "swipe risk:"))]
    in_notes = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_notes = line[3:].strip().lower() == "notes"
            continue
        if not in_notes or not line.lstrip().startswith("-"):
            continue
        m = re.match(r"\s*-\s*\[([^\]]+)\]\s*(blocker|polish)?", line, re.I)
        if not m:
            continue
        owners = {x.strip().split(":", 1)[0] for x in m.group(1).split("|")}
        severity = (m.group(2) or "blocker").lower()
        if owner in owners and (not only_blockers or severity == "blocker"):
            out.append(line)
    if len(out) <= 3:
        return "\n".join(out + ["No review notes routed to this role."])
    return "\n".join(out)


def build_brief(ep: Path, role: str, mode: str, task: str, paths: list[Path], *,
                note: Path | None = None, max_chars: int = 24000) -> str:
    """Return a size-bounded brief with only the files selected by the orchestrator."""
    chunks = [
        f"TASK BRIEF · role={role} · mode={mode}",
        "Use this brief as the task context. Do not browse other files or inspect images unless the task below requires it.",
        f"Task: {task}",
        "",
    ]
    remaining = max_chars - sum(map(len, chunks)) - 100  # reserve room for the size footer
    selected = ([note] if note else []) + paths
    seen: set[Path] = set()
    for path in selected:
        if path is None:
            continue
        path = path.resolve()
        if path in seen:
            continue
        seen.add(path)
        label = f"\n--- {path.relative_to(ep.parent.parent) if ep.parent.parent in path.parents else path} ---\n"
        if remaining <= len(label):
            break
        body = (_note_for_role(path, role, only_blockers=(role == "component-dev" and "blocker" in task.lower()))
                if note and path == note.resolve() else _read(path, min(remaining - len(label), 18000)))
        if len(body) > remaining - len(label):
            body = body[:remaining - len(label)] + "\n[truncated to brief budget]"
        part = label + body + "\n"
        if len(part) > remaining:
            part = part[:remaining]
        chunks.append(part)
        remaining -= len(part)
    brief = "".join(chunks)
    return brief + f"\n[brief payload: {len(brief)} chars]\n"


def edit_inputs(ep: Path, role: str, mode: str, note: Path | None = None, *,
                only_blockers: bool = False) -> list[Path]:
    """Canonical, small file sets for scene planning, revisions and visual review."""
    c, n = ep / ".cache", ep / "notes"
    if role == "director":
        if mode == "first":
            return [ep / "script.md", c / "words.txt", ep / "facts.md", ep / "cover.md",
                    Path("components/_catalog.md"), Path("brand/rules/themes.md"), Path("brand/rules/formats.md"),
                    Path("brand/shot-patterns.json")]
        return [ep / "scenes/scenes.json", c / "qa.json"]
    if role == "editor":
        if mode == "first":
            return [ep / "scenes/scenes.json", c / "words.txt", c / "qa.json",
                    Path("brand/rules/formats.md"), Path("brand/rules/sound.md")]
        return [ep / "scenes/scenes.json", c / "qa.json"]
    if role == "video-reviewer":
        return [c / "qa.json", c / "palette_report.json", c / "scenes.resolved.json",
                c / "voice_check.md", ep / "script.md", ep / "cover.md"]
    if role == "component-dev":
        names: set[str] = set()
        if note and note.exists():
            names.update(re.findall(r"\[component:([\w-]+)\]", _note_for_role(note, role, only_blockers=only_blockers)))
        return [Path("components") / name / file for name in sorted(names)
                for file in ("component.json", "component.css", "component.js")]
    if role == "scriptwriter":
        if mode == "first":
            return [ep / "script.md", ep / "facts.md", ep / "cover.md", ep / "notes/premise.md",
                    Path("brand/rules/comedy.md"), Path("brand/rules/formats.md")]
        return [ep / "script.md", ep / "facts.md", ep / "cover.md", ep / "notes/premise.md"]
    if role == "script-reviewer":
        if mode == "revision":
            return [ep / "script.md", ep / "facts.md", ep / "cover.md"]
        return [ep / "script.md", ep / "facts.md", ep / "cover.md",
                Path("brand/rules/comedy.md"), Path("brand/rules/formats.md")]
    return []


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("episode", type=Path)
    p.add_argument("role")
    p.add_argument("mode", choices=["first", "revision", "review"])
    p.add_argument("task")
    p.add_argument("--note", type=Path)
    p.add_argument("--max-chars", type=int, default=24000)
    a = p.parse_args()
    ep = a.episode.resolve()
    note = a.note.resolve() if a.note else None
    only_blockers = a.role == "component-dev" and "blocker" in a.task.lower()
    text = build_brief(ep, a.role, a.mode, a.task,
                       edit_inputs(ep, a.role, a.mode, note, only_blockers=only_blockers), note=note,
                       max_chars=a.max_chars)
    print(text, end="")
    print(f"brief_chars={len(text)}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
