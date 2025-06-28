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

lint file="":
    uv run ruff format .
    uv run ruff check . --fix
    uv run djlint . --reformat --quiet

test:
    uv run pytest


serve:
    uvicorn main:app --host 0.0.0.0 --port 5555 --reload

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

# Generate static site by crawling all FastAPI endpoints
generate_site output_dir="./dist":
    uv run python generate_site.py "{{output_dir}}"

# Run inference using aider
# AI! make this work by receiving Make it make this work by receiving a receiving the prompt from standard inn instead of in the argument slot. have it just be that it has to receive a file and if it doesn't receive a file it should just basically do the default. so don't worry if it doesn't have the first argument and then basically I need you to modify the resolve scripts so that it should receive the prompt in from standard inn. so you'll need to modify the just file and also the resolve python module here
resolve file prompt="":
    uv run python resolve.py "{{file}}" "{{prompt}}"

# List available context files
list_contexts:
    uv run python resolve.py --list-contexts