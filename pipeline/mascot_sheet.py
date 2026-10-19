#!/usr/bin/env python3
"""Render the Chillar character sheet and export layered SVGs.

  mascot_sheet.py            -> brand/mascot/sheet.png, chillar.svg, expressions/<expr>.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "brand" / "mascot"

SHEET = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../colors.css"><link rel="stylesheet" href="mascot.css">
<style>
 body { margin:0; width:1800px; }
 .wrap { padding: 48px 56px 56px 140px; }
 h1 { font-size: 92px; margin: 0; }
 .sub { font-size: 28px; margin: 6px 0 30px; }
 .grid { display:grid; grid-template-columns: repeat(4, 1fr); gap: 30px; }
 .cell { padding: 18px 10px 14px; display:flex; flex-direction:column; align-items:center; }
 .grid .cell svg { width: 320px; height: 352px; }
 .label { font-family: var(--font-mono); font-weight: 700; font-size: 24px; margin-top: 6px; }
 .scale { display:flex; align-items:flex-end; gap: 40px; margin-top: 34px; }
 .scale .cell { flex-direction: row; gap: 30px; align-items:flex-end; }
</style></head>
<body class="chillar-paper"><div class="wrap">
 <h1 class="t-head">Chillar — character sheet</h1>
 <div class="sub t-body t-sub">healthy ₹1 coin · haldi · deadpan · never fully smiles</div>
 <div class="grid" id="grid"></div>
 <div class="scale chillar-card" style="padding:16px 24px"><div class="cell" id="sizes"></div></div>
</div>
<script src="chillar.js"></script>
<script>
 const g = document.getElementById('grid');
 Chillar.EXPRESSIONS.forEach((e, i) => {
   const d = document.createElement('div'); d.className = 'cell chillar-card';
   d.innerHTML = Chillar.svg({ expr: e, id: 'c' + i, size: 320 }) + '<div class="label">' + e + '</div>';
   g.appendChild(d);
 });
 const s = document.getElementById('sizes');
 [220, 120, 64, 36].forEach((px, i) => { s.insertAdjacentHTML('beforeend', Chillar.svg({ expr: 'neutral-tired', id: 's' + i, size: px })); });
 s.insertAdjacentHTML('beforeend', '<div class="label">legibility: 220 / 120 / 64 / 36 px</div>');
</script></body></html>"""


def main() -> int:
    (M / "sheet.html").write_text(SHEET)
    (M / "expressions").mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1800, "height": 1000}, device_scale_factor=1)
        pg.goto((M / "sheet.html").as_uri())
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(M / "sheet.png"), full_page=True)
        exprs = pg.evaluate("Chillar.EXPRESSIONS")
        for e in exprs:
            svg = pg.evaluate(f"Chillar.svg({{expr: '{e}', id: 'chillar', size: 400}})")
            (M / "expressions" / f"{e}.svg").write_text(svg)
        master = pg.evaluate("Chillar.svg({expr: 'neutral-tired', id: 'chillar', size: 400})")
        (M / "chillar.svg").write_text(master)
        b.close()
    print(f"sheet: {M / 'sheet.png'}  ({len(exprs)} expressions exported)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
