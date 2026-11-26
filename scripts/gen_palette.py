#!/usr/bin/env python3
"""Gera .github/assets/palette.svg a partir do colors.toml."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".github" / "assets" / "palette.svg"

STROKE = "#3d444d"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"

W, PAD, GAP = 880, 28, 12

HUES = ("red", "green", "yellow", "blue", "magenta", "cyan")
CORE = ("background", "foreground", "accent", "selection_background",
        "dark_background", "muted")
# Mesma ordem ANSI que o Omarchy usa nos templates de terminal.
NORMAL = ("background", *HUES, "foreground")
BRIGHT = ("muted", *(f"bright_{h}" for h in HUES), "bright_foreground")


def load_colors():
    text = (ROOT / "colors.toml").read_text()
    values = dict(re.findall(r'^(\w+)\s*=\s*"(#[0-9a-fA-F]{6})"', text, re.M))
    missing = [k for k in CORE + NORMAL + BRIGHT if k not in values]
    if missing:
        sys.exit(f"colors.toml sem as chaves: {', '.join(missing)}")
    return values


def swatch(x, y, w, h, color, label, sub=None):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
           f'fill="{color}" stroke="{STROKE}" stroke-width="1"/>']
    ty = y + h + 18
    out.append(f'<text x="{x}" y="{ty}" font-family="{MONO}" font-size="12" '
               f'fill="{FG}">{label}</text>')
    if sub:
        out.append(f'<text x="{x}" y="{ty + 16}" font-family="{MONO}" '
                   f'font-size="11" fill="{MUTED}">{sub}</text>')
    return out


def row_label(x, y, text):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="11" '
            f'fill="{MUTED}" letter-spacing="1.2">{text}</text>')


def main():
    global BG, FG, MUTED
    c = load_colors()
    BG, FG, MUTED = c["dark_background"], c["foreground"], c["muted"]
    core = [("Background", c["background"]), ("Foreground", c["foreground"]),
            ("Accent", c["accent"]), ("Selection", c["selection_background"])]
    normal = [c[k] for k in NORMAL]
    bright = [c[k] for k in BRIGHT]

    parts, y = [], PAD

    parts.append(row_label(PAD, y + 10, "CORE"))
    y += 26
    core_w = (W - 2 * PAD - 3 * GAP) // 4
    for i, (name, hexv) in enumerate(core):
        parts += swatch(PAD + i * (core_w + GAP), y, core_w, 56, hexv, name, hexv)
    y += 56 + 58

    cell_w = (W - 2 * PAD - 7 * GAP) // 8
    for title, row in (("NORMAL", normal), ("BRIGHT", bright)):
        parts.append(row_label(PAD, y + 10, title))
        y += 26
        for i, hexv in enumerate(row):
            parts += swatch(PAD + i * (cell_w + GAP), y, cell_w, 44, hexv, hexv)
        y += 44 + 34

    h = y + PAD - 22
    svg = "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
        f'viewBox="0 0 {W} {h}" role="img" aria-label="Noctua color palette">',
        f'<rect width="{W}" height="{h}" rx="10" fill="{BG}"/>',
        *parts, "</svg>",
    ])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg)
    print(f"{OUT.relative_to(ROOT)} {W}x{h} {len(svg)} bytes")


if __name__ == "__main__":
    main()
