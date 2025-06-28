# Master justfile for Colgan Development

# Use bash for the default shell
set shell := ["bash", "-c"]

# Read from the .env file
set dotenv-load

default:
    @just --list


CONFIG_FOLDERS := "alacritty bspwm dunst kitty nvim sxhkd"
HOME_FILES := "bashrc gitconfig"


# Idempotently create symlinks to install all dotfiles into ~/ and ~/.config, and scripts into ~/.local/bin/
sync_dotfiles:
    #!/bin/bash

    DOTFILES_DIR="{{invocation_directory()}}"

    cd "$HOME"

    for file in {{HOME_FILES}}; do
        ln -sfv "$DOTFILES_DIR/home/$file" ".$file"
    done

    cd "$HOME/.config/"

    for folder in {{CONFIG_FOLDERS}}; do
        ln -sfv "$DOTFILES_DIR/$folder/" .
    done

    cd "$HOME/.local/bin/"

    for script in "$DOTFILES_DIR/scripts"/*; do
        script_name=$(basename "$script")
        ln -sfv "$script" "$script_name"
    done

lint:
    uv run ruff format .
    uv run ruff check . --fix
    uv run djlint . --reformat --quiet

test:
    uv run pytest


serve:
    uvicorn main:app --host vividness.buri-frog.ts.net --port 5555

#dark_theme := "Mint-Y-Dark"
#light_theme := "Mint-Y"
#
#dark_mode_on:
#    #!/bin/bash
#    dconf write /org/cinnamon/desktop/interface/gtk-theme "'{{dark_theme}}'"
#    dconf write /org/cinnamon/desktop/wm/preferences/theme "'{{dark_theme}}'"
#    dconf write /org/cinnamon/theme/name "'{{dark_theme}}'"
#    dconf write /org/cinnamon/desktop/interface/icon-theme "'{{dark_theme}}'"
#    echo "Dark mode enabled"
#
#dark_mode_off:
#    #!/bin/bash
#    dconf write /org/cinnamon/desktop/interface/gtk-theme "'{{light_theme}}'"
#    dconf write /org/cinnamon/desktop/wm/preferences/theme "'{{light_theme}}'"
#    dconf write /org/cinnamon/theme/name "'{{light_theme}}'"
#    dconf write /org/cinnamon/desktop/interface/icon-theme "'{{light_theme}}'"
#    echo "Light mode enabled"
#

upgrade:
   #!/bin/bash

   # Update Neovim to latest version
   curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz
   sudo rm -rf /opt/nvim
   sudo tar -C /opt -xzf nvim-linux-x86_64.tar.gz
   sudo ln -sf /opt/nvim-linux-x86_64/bin/nvim /usr/local/bin/nvim


backup_folders := "inbox repos"

backup_home:
    #!/usr/bin/env bash
    set -euo pipefail

    for folder in {{backup_folders}}; do
        rsync -avzh "$HOME/$folder/" "optimism:$HOME/backups/vividness/$folder/"
    done

