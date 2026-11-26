#!/usr/bin/env python3
"""Propaga uma troca de paleta do colors.toml para os arquivos com hex fixo.

Compara o colors.toml de uma revisao do git (padrao: HEAD) com o do disco e
troca, em uma unica passada, cada hex antigo pelo novo nos demais arquivos do
tema. Rode depois de editar o colors.toml e antes do commit:

    python3 scripts/sync_extras.py            # aplica
    python3 scripts/sync_extras.py --check    # so mostra o que mudaria
    python3 scripts/sync_extras.py --from v1  # compara com outra revisao

Ao final lista os hex que nao pertencem a paleta, para revisao manual.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = ("scripts/", ".github/", "backgrounds/", "docs/")
SKIP_FILES = {"colors.toml", "README.md", "AGENTS.md", "preview.png",
              "chromium.theme", "icons.theme", ".gitignore"}
HEX = r"[0-9a-fA-F]"


def parse(text):
    """Papel -> lista de hex (minusculo, sem #). Gradientes rendem varios."""
    roles = {}
    for key, value in re.findall(r'^(\w+)\s*=\s*"([^"]*)"', text, re.M):
        found = re.findall(rf"#({HEX}{{6}})\b|rgba?\(({HEX}{{6}})", value)
        if found:
            roles[key] = [(a or b).lower() for a, b in found]
    return roles


def mapping(old, new):
    out = {}
    for key, olds in old.items():
        for o, n in zip(olds, new.get(key, [])):
            if o != n and out.setdefault(o, n) != n:
                print(f"aviso: {o} era de mais de um papel; ficou {out[o]}, "
                      f"ignorado {n} ({key})", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--from", dest="rev", default="HEAD")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    git = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a],
                                    capture_output=True, text=True, check=True).stdout
    new = parse((ROOT / "colors.toml").read_text())
    remap = mapping(parse(git("show", f"{args.rev}:colors.toml")), new)
    palette = {h for hs in new.values() for h in hs}

    # Um hex casa com ou sem '#', e com alfa de dois digitos colado (rgba).
    pattern = re.compile(
        rf"(?<!{HEX})({'|'.join(remap) or 'x^'})(?=(?:{HEX}{{2}})?(?!{HEX}))", re.I)
    # steam.css escreve as cores como trio decimal: "36, 36, 36".
    dec = lambda h: [str(int(h[i:i + 2], 16)) for i in (0, 2, 4)]
    triples = {tuple(dec(o)): ", ".join(dec(n)) for o, n in remap.items()}
    triple = re.compile(r"(?<![\d.])(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})(?![\d.])")
    stray = {}
    for rel in git("ls-files").splitlines():
        path = ROOT / rel
        if rel in SKIP_FILES or rel.startswith(SKIP_DIRS) or not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        result, count = pattern.subn(lambda m: remap[m.group(1).lower()], text)
        result, more = triple.subn(
            lambda m: triples.get(m.groups(), m.group(0)), result)
        count += sum(m.groups() in triples for m in triple.finditer(text)) if more else 0
        if count:
            print(f"{rel}: {count} troca(s)")
            if not args.check:
                path.write_text(result)
        for h in re.findall(rf"#({HEX}{{6}})\b", result):
            if h.lower() not in palette:
                stray.setdefault(h.lower(), set()).add(rel)

    bg = new["background"][0]
    rgb = ",".join(str(int(bg[i:i + 2], 16)) for i in (0, 2, 4))
    chromium = ROOT / "chromium.theme"
    if chromium.read_text().strip() != rgb:
        print(f"chromium.theme: {rgb}")
        if not args.check:
            chromium.write_text(rgb + "\n")

    if stray:
        print("\nhex fora da paleta (revisar a mao):")
        for h, files in sorted(stray.items()):
            print(f"  #{h}  {', '.join(sorted(files))}")


if __name__ == "__main__":
    main()
