#!/usr/bin/env python3
import shutil
import time
from pathlib import Path
import argparse
import requests

# Configuration
OWNER = "DFHack"
REPO = "dfhack"
API_BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = str(SCRIPT_DIR / ".." / "proto")

def get_api_json(url: str) -> dict | list | None:
    """Makes a GET request to the GitHub API, handles rate limiting, and returns the JSON response."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 403 and 'rate limit' in response.text.lower():
            print("GitHub API rate limit exceeded. Waiting for 10 seconds...")
            time.sleep(10)
            return get_api_json(url)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API endpoint {url}: {e}")
        return None

def download_file(download_url: str, local_path: Path):
    """Downloads a file from a URL and saves it to a local path."""
    try:
        with requests.get(download_url, stream=True, timeout=10) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"  Downloaded {local_path.name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file {download_url}: {e}")

def fetch_proto_files_from_path(base_path: str, tag: str, output_dir: Path):
    """Finds and downloads all .proto files from a given path in the repo."""
    print(f"\nChecking path: {base_path}")
    contents_url = f"{API_BASE_URL}/contents/{base_path}?ref={tag}"
    items = get_api_json(contents_url)

    if not items or not isinstance(items, list):
        print("  -> Path not found or is not a directory.")
        return

    for item in items:
        if item['type'] == 'file' and Path(item['path']).suffix == '.proto':
            local_save_path = output_dir / item['name']
            download_file(item['download_url'], local_save_path)

def main():
    """Main function to parse arguments and orchestrate the download process."""
    parser = argparse.ArgumentParser(
        description="Fetch all .proto files from a specific DFHack git tag."
    )
    parser.add_argument(
        "--tag",
        required=True,
        help="The DFHack git tag to pull .proto files from (e.g., '51.13-r1')."
    )
    tag = parser.parse_args().tag

    output_dir = Path(f"{OUTPUT_DIR}/{tag}")

    print(f"Preparing output directory: {output_dir.resolve()}")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # 1. Fetch from the core library
    fetch_proto_files_from_path("library/proto", tag, output_dir)

    # 2. Discover and fetch from all plugins
    print("\nDiscovering plugins with .proto files...")
    plugins_url = f"{API_BASE_URL}/contents/plugins?ref={tag}"
    plugins = get_api_json(plugins_url)

    if plugins and isinstance(plugins, list):
        for plugin in plugins:
            if plugin['type'] == 'dir':
                plugin_proto_path = f"{plugin['path']}/proto"
                proto_check_url = f"{API_BASE_URL}/contents/{plugin_proto_path}?ref={tag}"
                
                proto_contents = get_api_json(proto_check_url)
                if proto_contents and isinstance(proto_contents, list):
                    fetch_proto_files_from_path(plugin_proto_path, tag, output_dir)
    else:
        print(f"No plugins found for tag '{tag}'")

    print(f"\n✅ Done. All .proto files for tag '{tag}' have been downloaded to {output_dir.resolve()}")

if __name__ == "__main__":
    main()