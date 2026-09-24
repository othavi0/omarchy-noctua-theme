# Omarchy Noctua Theme

Neutral One Dark Pro palette for Omarchy/Hyprland, built on a `#242424` base. It ships matching terminal, shell, editor, and app colors plus three original wallpapers.

![Noctua theme running on Hyprland, with editor and terminal](preview.png)

## Requirements

Omarchy 4 (Quattro) or newer.

## Install

Use the Omarchy theme installer:

```bash
omarchy-theme-install https://github.com/othavi0/omarchy-noctua-theme
```

### herdr (opt-in)

Omarchy does not theme [herdr](https://github.com/herdrdev/herdr), so its colors are not applied by the installer. To keep herdr in sync automatically, install the bundled Omarchy hook once:

```bash
mkdir -p ~/.config/omarchy/hooks/theme-set.d
cp ~/.config/omarchy/themes/noctua/herdr.hook.sh ~/.config/omarchy/hooks/theme-set.d/herdr
```

On every theme change the hook applies the theme's `herdr.toml` when it ships one, and falls back to herdr's `terminal` theme otherwise. It never overwrites a hand-edited `[theme]` block. Prefer manual setup? Follow the merge notes inside `herdr.toml`.

## Palette

Noctua keeps the One Dark Pro syntax family while moving the desktop base to `#242424`. The primary Omarchy accent is `#61afef`.

![Noctua palette: core, normal and bright colors with hex values](.github/assets/palette.svg)

## What's included

### Applied by Omarchy

`omarchy-theme-set noctua` applies these on its own.

- `colors.toml` is the source Omarchy generates from. That covers the terminals (Alacritty, Kitty, Ghostty, Foot), the Hyprland window borders, the omarchy-shell surfaces (bar, launcher, notifications, popups, lock screen), and the Neovim, VS Code, Helix and Obsidian themes.
- `shell.menu.toml` restyles the omarchy-shell menu with a darker card, a blue gradient border and a blue selected row.
- `btop.theme` colors btop.
- `chromium.theme` sets the Chromium frame color.
- `icons.theme` selects the Yaru-blue icon theme.
- `backgrounds/` holds the three wallpapers below.

### Manual extras

Omarchy does not apply these. Copy the ones you want into each app's config.

- `gtk.css` holds GTK4/libadwaita color overrides.
- `steam.css` holds color overrides for the Adwaita for Steam skin.
- `vencord.theme.css` is a Discord theme for Vencord.
- `firefox.css` holds base16 color variables for a Firefox `userChrome.css`.
- `colors.fish` sets Fish syntax and pager colors.
- `fzf.fish` sets fzf colors from Fish.
- `warp.yaml` is a Warp terminal theme.
- `bat/Noctua.tmTheme` is a bat syntax theme.
- `aether.override.css` and `aether.zed.json` are Aether and Zed overrides.
- `herdr.toml` and `herdr.hook.sh` theme herdr, as described in the herdr section above.
- `vscode.settings.snippet.jsonc` holds token refinements scoped to the One Dark Pro VS Code theme. They do nothing under the Omarchy theme that VS Code gets by default.

## Motion and shadow (opt-in)

Themes installed from git cannot ship Lua, so Omarchy drops any `*.lua` file from them. To get the Noctua window shadow and animation curves, paste this block into `~/.config/hypr/looknfeel.lua`. It stays active when you switch to another theme.

```lua
hl.config({
  decoration = {
    shadow = { enabled = true, range = 10, render_power = 3, color = "rgba(00000099)", offset = { 2, 2 } },
  },
})
hl.curve("noctua",   { type = "bezier", points = { { 0.55, 0.02 }, { 0.38, 0.98 } } })
hl.curve("midnight", { type = "bezier", points = { { 0.70, 0.01 }, { 0.30, 1.00 } } })
hl.animation({ leaf = "windows",     enabled = true,  speed = 4, bezier = "noctua" })
hl.animation({ leaf = "windowsIn",   enabled = false })
hl.animation({ leaf = "windowsOut",  enabled = false })
hl.animation({ leaf = "windowsMove", enabled = true,  speed = 3, bezier = "noctua" })
hl.animation({ leaf = "fade",        enabled = true,  speed = 4, bezier = "midnight" })
hl.animation({ leaf = "fadeIn",      enabled = true,  speed = 4, bezier = "midnight" })
hl.animation({ leaf = "fadeOut",     enabled = true,  speed = 3, bezier = "midnight" })
hl.animation({ leaf = "workspaces",  enabled = true,  speed = 3, bezier = "midnight", style = "fade" })
```

## Wallpapers

Click any thumbnail for the full-resolution file.

| | | |
| --- | --- | --- |
| [![City skyline at dusk](.github/assets/00-city-dusk.jpg)](backgrounds/00-city-dusk.jpg) | [![Close view of the moon](.github/assets/01-lunar-arc.jpg)](backgrounds/01-lunar-arc.jpg) | [![Snow-capped mountain ridge](.github/assets/02-alpine-ridge.jpg)](backgrounds/02-alpine-ridge.jpg) |
| `00-city-dusk.jpg` | `01-lunar-arc.jpg` | `02-alpine-ridge.jpg` |

