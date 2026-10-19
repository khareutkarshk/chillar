"""Verify brand fonts cover the glyphs Chillar needs. Exit 1 on a hard miss.

Writes brand/fonts/coverage.json so components know whether ₹ must fall back
from Bricolage Grotesque / JetBrains Mono to Mukta.
"""
import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "brand" / "fonts"

RUPEE = 0x20B9
CHECKS = {
    "BricolageGrotesque[opsz,wdth,wght].ttf": {"latin": range(0x41, 0x5B), "digits": range(0x30, 0x3A), "rupee": [RUPEE]},
    "Mukta-ExtraBold.ttf": {
        "latin": range(0x41, 0x5B),
        "devanagari": range(0x0905, 0x0915),
        "rupee": [RUPEE],
    },
    "JetBrainsMono[wght].ttf": {"digits": range(0x30, 0x3A), "rupee": [RUPEE]},
}
HARD = {("Mukta-ExtraBold.ttf", "devanagari"), ("Mukta-ExtraBold.ttf", "latin"),
        ("JetBrainsMono[wght].ttf", "digits"), ("BricolageGrotesque[opsz,wdth,wght].ttf", "latin"), ("BricolageGrotesque[opsz,wdth,wght].ttf", "digits")}


def main() -> int:
    report, ok = {}, True
    for fname, groups in CHECKS.items():
        path = FONTS / fname
        if not path.exists():
            print(f"    missing font: {fname}")
            ok = False
            continue
        cmap = TTFont(path).getBestCmap()
        report[fname] = {}
        for g, cps in groups.items():
            missing = [hex(c) for c in cps if c not in cmap]
            report[fname][g] = not missing
            mark = "ok" if not missing else f"MISSING {missing[:4]}"
            print(f"    {fname:26s} {g:11s} {mark}")
            if missing and (fname, g) in HARD:
                ok = False
    for f in ("BricolageGrotesque[opsz,wdth,wght].ttf", "JetBrainsMono[wght].ttf"):
        has = report.get(f, {}).get("rupee", False)
        print(f"    ₹ in {f.split('[')[0]} text renders in: {'itself' if has else 'Mukta (font stack fallback)'}")
    report["rupee_font"] = "Mukta"
    (FONTS / "coverage.json").write_text(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
