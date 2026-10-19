"""License policy + ledger (assets/licenses.json).

Every downloaded file gets one ledger entry with a saved license snapshot.
Anything not on the allow-list is refused.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path

from .common import ASSETS, ROOT, Candidate, slug

LEDGER = ASSETS / "licenses.json"
SNAPSHOTS = ASSETS / "snapshots"

# license name -> (commercial use ok, attribution required)
ALLOWED = {
    "CC0 1.0": (True, False),
    "Pixabay Content License": (True, False),
    "Mixkit Sound Effects Free License": (True, False),
    "Mixkit Stock Music Free License": (True, False),
    "Pexels License": (True, False),
    "MIT": (True, True),            # keep the notice in the ledger
    "ISC": (True, True),
    "Apache-2.0": (True, True),
    "OFL-1.1": (True, False),
}


class LicenseRefused(Exception):
    pass


def check_policy(c: Candidate) -> None:
    if c.license_name not in ALLOWED:
        raise LicenseRefused(f"{c.key}: license '{c.license_name}' not on allow-list")
    ok, _ = ALLOWED[c.license_name]
    if not ok:
        raise LicenseRefused(f"{c.key}: license '{c.license_name}' disallows commercial use")


def load() -> list[dict]:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text() or "[]")
    return []


def save(entries: list[dict]) -> None:
    LEDGER.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n")


def save_snapshot(c: Candidate, text: str) -> str:
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    p = SNAPSHOTS / f"{c.source}-{slug(c.source_id, 40)}.txt"
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    p.write_text(f"# license snapshot {stamp}\n# {c.page_url}\n# {c.license_url}\n\n{text[:20000]}\n")
    return str(p.relative_to(ROOT))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def record(c: Candidate, file: Path, snapshot: str, **extra) -> dict:
    entries = load()
    entry = {
        "name": c.title,
        "file": str(file.relative_to(ROOT)),
        "kind": c.kind,
        "source": c.source,
        "source_id": c.source_id,
        "url": c.page_url,
        "download_url": c.download_url,
        "author": c.author,
        "license": c.license_name,
        "license_url": c.license_url,
        "attribution_needed": "y" if c.attribution_required else "n",
        "attribution_text": c.extra.get("attribution", ""),
        "date": dt.date.today().isoformat(),
        "sha256": sha256(file),
        "license_snapshot": snapshot,
        **extra,
    }
    entries = [e for e in entries if e.get("file") != entry["file"]]
    entries.append(entry)
    save(entries)
    return entry


def entry_for(file: Path) -> dict | None:
    rel = str(Path(file).resolve().relative_to(ROOT))
    return next((e for e in load() if e.get("file") == rel), None)
