#!/usr/bin/env python3
"""Search cached primary-source PDFs/HTML locally with SQLite FTS5.

  source_index.py sync
  source_index.py search "soft enquiry score unaffected" [--source rbi-cic-master-jan25.pdf]
                                    [--episode episodes/<slug>] [--limit 5]
  source_index.py status

The index lives in .cache/source-index.sqlite3 and is disposable. brand/sources/index.json and the
cached files remain the source of truth. PDF extraction uses the local `pdftotext` utility.
"""
from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "brand" / "sources"
SOURCE_MANIFEST = SOURCE_DIR / "index.json"
DB = ROOT / ".cache" / "source-index.sqlite3"
MAX_CHUNK = 1600


class TextHTML(HTMLParser):
    """Extract visible HTML text without scripts, styles, or navigation noise."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script", "style", "noscript", "svg"}:
            self.skip += 1
        elif tag.lower() in {"p", "br", "div", "li", "tr", "h1", "h2", "h3", "section"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1
        elif tag.lower() in {"p", "br", "div", "li", "tr", "h1", "h2", "h3", "section"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def connect() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB, timeout=30)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=30000")
    con.execute("CREATE TABLE IF NOT EXISTS source_meta (path TEXT PRIMARY KEY, url TEXT, sha256 TEXT, bytes INTEGER, mtime_ns INTEGER, chars INTEGER)")
    con.execute("CREATE TABLE IF NOT EXISTS source_errors (path TEXT PRIMARY KEY, sha256 TEXT, error TEXT)")
    con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(text, path UNINDEXED, url UNINDEXED, page UNINDEXED, tokenize='unicode61')")
    return con


def urls_by_file() -> dict[str, str]:
    try:
        data = json.loads(SOURCE_MANIFEST.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    out = {}
    for url, row in data.items():
        name = row.get("file") if isinstance(row, dict) else None
        if name and name not in out:
            out[name] = url
    return out


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ").replace("\u00ad", "")
    return re.sub(r"[ \t\r\f]+", " ", text)


def extract_pages(path: Path) -> list[tuple[int, str]]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        proc = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
                              capture_output=True, text=True, errors="replace", timeout=180)
        if proc.returncode:
            raise RuntimeError(proc.stderr.strip()[-500:] or "pdftotext failed")
        return [(i, clean_text(page)) for i, page in enumerate(proc.stdout.split("\f"), 1) if page.strip()]
    if suffix in {".html", ".htm"}:
        parser = TextHTML()
        parser.feed(path.read_text(errors="replace"))
        return [(1, clean_text("".join(parser.parts)))]
    if suffix in {".txt", ".text"}:
        return [(1, clean_text(path.read_text(errors="replace")))]
    return []


def split_chunks(text: str) -> list[str]:
    """Pack paragraphs into bounded chunks while keeping source wording intact."""
    paras = [re.sub(r"\s+", " ", p).strip() for p in text.splitlines() if p.strip()]
    chunks, current = [], ""
    for para in paras:
        while len(para) > MAX_CHUNK:
            cut = para.rfind(" ", 0, MAX_CHUNK)
            cut = cut if cut > MAX_CHUNK // 2 else MAX_CHUNK
            part, para = para[:cut].strip(), para[cut:].strip()
            if current:
                chunks.append(current); current = ""
            if part:
                chunks.append(part)
        if not para:
            continue
        if current and len(current) + len(para) + 1 > MAX_CHUNK:
            chunks.append(current); current = para
        else:
            current = f"{current} {para}".strip()
    if current:
        chunks.append(current)
    return chunks


def sync() -> tuple[int, int, int]:
    """Index new/changed cached files; unchanged files are neither extracted nor reindexed."""
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    con = connect()
    urls = urls_by_file()
    files = sorted(p for p in SOURCE_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".html", ".htm", ".txt", ".text"})
    present = {str(p.resolve()) for p in files}
    removed = [r[0] for r in con.execute("SELECT path FROM source_meta") if r[0] not in present]
    for old in removed:
        con.execute("DELETE FROM chunks WHERE path=?", (old,))
        con.execute("DELETE FROM source_meta WHERE path=?", (old,))
    for old in [r[0] for r in con.execute("SELECT path FROM source_errors") if r[0] not in present]:
        con.execute("DELETE FROM source_errors WHERE path=?", (old,))

    changed = 0
    for path in files:
        path_s = str(path.resolve())
        stat = path.stat()
        url = urls.get(path.name, "")
        old = con.execute("SELECT sha256,bytes,mtime_ns,url FROM source_meta WHERE path=?", (path_s,)).fetchone()
        if old and old[1] == stat.st_size and old[2] == stat.st_mtime_ns and old[3] == url:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        failed = con.execute("SELECT sha256 FROM source_errors WHERE path=?", (path_s,)).fetchone()
        if failed and failed[0] == digest:
            continue
        if failed:
            con.execute("DELETE FROM source_errors WHERE path=?", (path_s,))
        if old and old[0] == digest and old[3] == url:
            con.execute("UPDATE source_meta SET bytes=?,mtime_ns=? WHERE path=?", (stat.st_size, stat.st_mtime_ns, path_s))
            continue
        try:
            pages = extract_pages(path)
        except (OSError, subprocess.TimeoutExpired, RuntimeError, FileNotFoundError) as exc:
            print(f"source-index: skipped {path.name}: {exc}", file=sys.stderr)
            con.execute("INSERT OR REPLACE INTO source_errors(path,sha256,error) VALUES(?,?,?)",
                        (path_s, digest, str(exc)[-500:]))
            continue
        con.execute("DELETE FROM source_errors WHERE path=?", (path_s,))
        con.execute("DELETE FROM chunks WHERE path=?", (path_s,))
        total_chars = 0
        for page, body in pages:
            total_chars += len(body)
            for chunk in split_chunks(body):
                con.execute("INSERT INTO chunks(text,path,url,page) VALUES(?,?,?,?)",
                            (chunk, path_s, url, str(page)))
        con.execute("INSERT OR REPLACE INTO source_meta(path,url,sha256,bytes,mtime_ns,chars) VALUES(?,?,?,?,?,?)",
                    (path_s, url, digest, stat.st_size, stat.st_mtime_ns, total_chars))
        changed += 1
    con.commit()
    docs = con.execute("SELECT COUNT(*), COALESCE(SUM(chars),0) FROM source_meta").fetchone()
    con.close()
    return changed, docs[0], docs[1]


def fts_query(query: str, mode: str) -> str:
    terms = re.findall(r"[^\W_]+", query, flags=re.UNICODE)
    if not terms:
        return ""
    quoted = ['"' + t.replace('"', '""') + '"' for t in terms[:16]]
    return (" AND " if mode == "all" else " OR ").join(quoted)


def log_search(episode: str | None, query: str, rows: list[tuple], excerpt_chars: int, corpus_chars: int) -> None:
    if not episode:
        return
    ep = Path(episode)
    if not ep.is_absolute():
        ep = ROOT / ep
    log = ep / "notes" / "source-search.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    sources = {}
    for row in rows:
        sources[row[0]] = {"url": row[1], "chars": row[5] or 0}
    record = {"at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "query": query,
              "hits": len(rows), "excerpt_chars": excerpt_chars, "corpus_chars": corpus_chars,
              "sources": sources}
    with log.open("a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def search(query: str, limit: int, source: str | None, episode: str | None) -> int:
    changed, docs, corpus_chars = sync()
    con = connect()
    if not docs:
        print("No cached source text indexed. Cache a primary source first with facts_library.py cache.")
        con.close(); return 1
    match = fts_query(query, "all")
    if not match:
        print("Enter at least one searchable word.")
        con.close(); return 2
    where = "chunks MATCH ?"
    args: list[object] = [match]
    if source:
        where += " AND (path LIKE ? OR url LIKE ?)"
        args += [f"%{source}%", f"%{source}%"]
    sql = ("SELECT path,url,page,snippet(chunks,0,'⟦','⟧',' … ',34),bm25(chunks) "
           f"FROM chunks WHERE {where} ORDER BY bm25(chunks) LIMIT ?")
    try:
        rows = con.execute(sql, (*args, limit)).fetchall()
    except sqlite3.OperationalError:
        # Some relevant wording may be separated by stop words or OCR artifacts; broaden once.
        match = fts_query(query, "any")
        rows = con.execute(sql, (match, *args[1:], limit)).fetchall() if match else []
    indexed_chars = {r[0]: r[2] for r in con.execute("SELECT path,url,chars FROM source_meta")}
    con.close()
    if not rows:
        # An AND-only query with no hits is broadened to OR terms, including source-restricted searches.
        con = connect()
        match = fts_query(query, "any")
        rows = con.execute(sql, (match, *args[1:], limit)).fetchall() if match else []
        con.close()
    if not rows:
        print("No matching cached passage. Try fewer or alternate terms; then use the primary source directly.")
        return 1

    excerpt_chars = 0
    for i, row in enumerate(rows, 1):
        path, url, page, excerpt, _rank = row
        excerpt = re.sub(r"\s+", " ", excerpt).strip()
        excerpt_chars += len(excerpt)
        cited = f"{url} (p. {page})" if url and path.lower().endswith(".pdf") else (url or f"local source: {Path(path).name}")
        print(f"[{i}] {cited}\n{excerpt}\n")
    # Add source character counts to the in-memory rows for the optional per-episode measurement log.
    log_rows = [(r[0], r[1], r[2], r[3], r[4], indexed_chars.get(r[0], 0)) for r in rows]
    log_search(episode, query, log_rows, excerpt_chars, corpus_chars)
    print(f"source-index: {len(rows)} excerpts · {excerpt_chars:,} chars returned · {corpus_chars:,} chars indexed"
          + (f" · {changed} source(s) indexed this run" if changed else ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("sync", help="index new/changed files in brand/sources")
    q = sub.add_parser("search", help="search cached source passages")
    q.add_argument("query")
    q.add_argument("--source", help="restrict to a filename or URL fragment")
    q.add_argument("--episode", help="log retrieval volume in episodes/<slug>/notes")
    q.add_argument("--limit", type=int, default=5)
    sub.add_parser("status", help="show indexed documents and text volume")
    a = ap.parse_args()
    if a.command == "sync":
        changed, docs, chars = sync()
        print(f"source-index: {docs} cached source(s) · {chars:,} extracted chars · {changed} indexed/updated")
        return 0
    if a.command == "search":
        if not 1 <= a.limit <= 10:
            ap.error("--limit must be between 1 and 10")
        return search(a.query, a.limit, a.source, a.episode)
    changed, docs, chars = sync()
    print(f"source-index: {docs} cached source(s) · {chars:,} extracted chars · {changed} indexed/updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
