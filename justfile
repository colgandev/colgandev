# Master justfile for Colgan Development
# AI These are all actions you can take

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


# Run aider with a context file
context file prompt="":
    uv run python scripts/run_context.py "{{file}}" "{{prompt}}"

# List available context files
list_contexts:
    uv run python scripts/run_context.py --list-contexts

# Generate static site by crawling all FastAPI endpoints
generate_site output_dir="./dist":
    #!/usr/bin/env python3
    import os
    import sys
    import requests
    import time
    import subprocess
    from pathlib import Path
    from urllib.parse import urljoin, urlparse
    
    # Add current directory to Python path to import our app
    sys.path.insert(0, '{{invocation_directory()}}')
    
    from main import app
    
    # Start the server in background
    print("Starting FastAPI server...")
    server_process = subprocess.Popen([
        "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"
    ], cwd="{{invocation_directory()}}")
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        base_url = "http://127.0.0.1:8000"
        output_path = Path("{{output_dir}}")
        output_path.mkdir(exist_ok=True)
        
        # Discover all routes from FastAPI app
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                if 'GET' in route.methods:
                    routes.append(route.path)
        
        print(f"Found {len(routes)} routes to crawl:")
        for route in routes:
            print(f"  {route}")
        
        # Crawl each route
        for route in routes:
            try:
                url = urljoin(base_url, route)
                print(f"Crawling {url}...")
                
                response = requests.get(url)
                response.raise_for_status()
                
                # Create directory structure
                if route == "/":
                    file_path = output_path / "index.html"
                else:
                    # Convert route to file path
                    clean_route = route.strip("/")
                    if clean_route:
                        route_path = output_path / clean_route
                        route_path.mkdir(parents=True, exist_ok=True)
                        file_path = route_path / "index.html"
                    else:
                        file_path = output_path / "index.html"
                
                # Write the HTML content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"  → {file_path}")
                
            except Exception as e:
                print(f"Error crawling {route}: {e}")
        
        print(f"\nStatic site generated in {output_path}")
        
    finally:
        # Clean up server process
        server_process.terminate()
        server_process.wait()


# Serve the generated static site for testing
serve_static output_dir="./dist":
    #!/usr/bin/env python3
    import http.server
    import socketserver
    import os
    from pathlib import Path
    
    output_path = Path("{{output_dir}}")
    if not output_path.exists():
        print(f"Output directory {output_path} does not exist. Run 'just generate_site' first.")
        exit(1)
    
    os.chdir(output_path)
    
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving static site at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()

