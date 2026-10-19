"""Shared paths, env, HTTP session and politeness helpers."""
from __future__ import annotations

import os
import random
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "brand"
ASSETS = ROOT / "assets"
CACHE = ROOT / ".cache"
load_dotenv(ROOT / ".env")

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/155.0 Safari/537.36 chillar-reels/0.1 (personal asset fetcher)")

session = requests.Session()
session.headers["User-Agent"] = UA


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()


def polite_sleep() -> None:
    lo = float(env("SCRAPE_DELAY_MIN", "3"))
    hi = float(env("SCRAPE_DELAY_MAX", "5"))
    time.sleep(random.uniform(lo, hi))


def slug(s: str, n: int = 48) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n] or "item"


def text_of(html: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).strip()


@dataclass
class Candidate:
    """One downloadable asset. `verify()` must be called right before download."""
    source: str
    source_id: str
    title: str
    kind: str                      # sfx | music | image | video | icon
    page_url: str
    download_url: str
    license_name: str
    license_url: str
    attribution_required: bool
    author: str = ""
    duration: float | None = None
    ext: str = "mp3"
    extra: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return f"{self.source}:{self.source_id}"
