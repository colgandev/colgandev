"""
Static site generator that crawls FastAPI endpoints and saves HTML files.

This module provides functionality to generate a static version of the FastAPI
application by starting a development server, crawling all GET routes, and
saving the HTML responses to disk.
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests


def generate_site(output_dir: str = "./dist"):
    """Generate static site by crawling all FastAPI endpoints"""
    # Add current directory to Python path to import our app
    sys.path.insert(0, os.getcwd())

    from colgandev.app import app

    # Start the server in background
    print("Starting FastAPI server...")
    server_process = subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])

    # Wait for server to start
    time.sleep(2)

    try:
        base_url = "http://127.0.0.1:8000"
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Discover all routes from FastAPI app
        routes = []
        for route in app.routes:
            if hasattr(route, "path") and hasattr(route, "methods"):
                if "GET" in route.methods:
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
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(response.text)

                print(f"  → {file_path}")

            except Exception as e:
                print(f"Error crawling {route}: {e}")

        print(f"\nStatic site generated in {output_path}")

    finally:
        # Clean up server process
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    import sys

    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./dist"
    generate_site(output_dir)
