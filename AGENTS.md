# Repository Guidelines

## Project Structure & Module Organization
- Targets Omarchy 4. `colors.toml` is the source: Omarchy generates the terminal configs, `hyprland.lua` (window borders from `hyprland_active_border`), the omarchy-shell `shell.toml`, and the Neovim/VS Code/Helix/Obsidian themes from it via `/usr/share/omarchy/default/themed/*.tpl`.
- `shell.<section>.toml` replaces that whole section of the generated `shell.toml` (e.g., `shell.menu.toml` replaces `[menu]`). The body has no `[section]` header, and text keys (`text`, `selected-text`) take hex only.
- A theme installed from git never ships `*.lua`, `vscode.json`, `alacritty.toml`, `foot.ini`, `ghostty.conf` or `kitty.conf`: Omarchy drops them and regenerates from `colors.toml`. Do not add them; Hyprland tweaks go in the README as opt-in snippets for `~/.config/hypr/looknfeel.lua`.
- Other root files (`gtk.css`, `steam.css`, `firefox.css`, `warp.yaml`, ...) are manual extras Omarchy does not apply; `btop.theme`, `chromium.theme` and `icons.theme` are applied as shipped.
- `backgrounds/` contains the bundled wallpapers used by the theme. Omarchy scans this directory and treats every image in it as a selectable wallpaper — never put non-wallpaper assets here.
- `.github/assets/` holds README-only assets (palette SVG, wallpaper thumbnails).
- `scripts/` holds the palette generator and the README integrity checker.
- `preview.png` is the visual snapshot used in the README.

## Build, Test, and Development Commands
This repo is configuration-only; there is no build system or automated test runner.
- Install the theme with Omarchy: `omarchy-theme-install https://github.com/othavi0/omarchy-noctua-theme`.
- For local iteration, edit the installed copy in `~/.config/omarchy/themes/noctua/`, run `omarchy-theme-set noctua`, and open the menu with Super+Space to check `shell.menu.toml`.

## Coding Style & Naming Conventions
- Follow the existing formatting in each file type; do not reformat unrelated sections.
- Indentation: Lua snippets in the README use 2 spaces; `shell.*.toml` aligns `=` in one column like the generated `shell.toml`.
- Colors use hex (`#abb2bf`). Gradient values (`hyprland_active_border`, `border` in `shell.*.toml`) are space-separated colors plus an angle, and each color is `rgb(RRGGBB)` or `rgba(RRGGBBAA)` with no spaces inside the parentheses.
- Keep filenames descriptive and lowercase, especially for wallpapers in `backgrounds/`.

## Testing Guidelines
- Run `python3 scripts/check_readme.py` after touching the README or renaming any asset; it fails if a referenced path is missing or a theme file is undocumented.
- Regenerate the palette with `python3 scripts/gen_palette.py` after changing `colors.toml`.
- No other automated tests are defined.
- Verify changes visually in the target app and update `preview.png` when the UI changes.
- Neovim has no file here: Omarchy generates `neovim.lua` from `colors.toml` (aether.nvim), so check Neovim colors by changing `colors.toml`.
- Check what Omarchy resolves from `colors.toml` with `omarchy-theme-color --file colors.toml --all`.

## Commit & Pull Request Guidelines
- Commit history is short and direct (e.g., “update readme”, “color corrections”); keep messages concise and action-focused.
- In PRs, list the files/apps affected and include screenshots when UI output changes.
- If you add or rename assets, update the README’s “What’s included” or wallpapers table accordingly.
