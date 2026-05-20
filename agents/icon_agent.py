#!/usr/bin/env python3
"""
Icon Agent - Czech Steel Dashboard
Searches, downloads, and processes SVG icons from game-icons.net.

G-12 rule: game-icons.net SVGs have a black background path (M0 0h512v512H0z)
and a white icon path. We remove the background and set icon fill to currentColor.

Usage:
    python agents/icon_agent.py search furnace
    python agents/icon_agent.py download factory blast-furnace rail
    python agents/icon_agent.py process C:\Downloads\rebar.svg armatury
    python agents/icon_agent.py catalog
    python agents/icon_agent.py list

Output:
    dashboard/assets/icons/{name}.svg   (processed, ready to embed)
    output/icon_catalog.md              (catalog with preview info)
"""

import re
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

PROJECT_ROOT  = Path(__file__).parent.parent
ICONS_DIR     = PROJECT_ROOT / "dashboard" / "assets" / "icons"
CATALOG_PATH  = PROJECT_ROOT / "output" / "icon_catalog.md"

# game-icons.net raw SVG base URL pattern
# Icons are at: https://raw.githubusercontent.com/game-icons/icons/master/delapouite/{name}.svg
# or:           https://raw.githubusercontent.com/game-icons/icons/master/lorc/{name}.svg
ICON_BASES = [
    "https://raw.githubusercontent.com/game-icons/icons/master/delapouite",
    "https://raw.githubusercontent.com/game-icons/icons/master/lorc",
    "https://raw.githubusercontent.com/game-icons/icons/master/skoll",
    "https://raw.githubusercontent.com/game-icons/icons/master/willdabeast",
]

# Curated steel-industry icon catalog (name → artist subfolder)
STEEL_ICONS = {
    # Ironmaking / raw materials
    "furnace":              "delapouite",
    "blast-furnace":        "delapouite",
    "coke":                 "delapouite",
    "coal":                 "delapouite",
    "ore":                  "delapouite",
    "mining-helmet":        "delapouite",
    "mine-wagon":           "delapouite",

    # Steelmaking
    "steel":                "delapouite",
    "factory":              "delapouite",
    "industrial-machinery": "delapouite",
    "gears":                "delapouite",
    "anvil":                "lorc",
    "smelting":             "lorc",
    "cauldron":             "lorc",

    # Rolling / products
    "rolling":              "delapouite",
    "wire-coil":            "delapouite",
    "pipes":                "delapouite",
    "train-rails":          "delapouite",
    "train":                "delapouite",
    "rail":                 "delapouite",
    "beam":                 "delapouite",

    # Energy / environment
    "electric":             "delapouite",
    "solar-power":          "delapouite",
    "wind-turbine":         "delapouite",
    "recycling":            "lorc",
    "recycle":              "delapouite",

    # Business / market
    "bar-chart":            "delapouite",
    "trending":             "delapouite",
    "profit":               "delapouite",
    "loss":                 "delapouite",
    "scales":               "delapouite",
    "money-stack":          "delapouite",

    # Location / logistics
    "city":                 "delapouite",
    "warehouse":            "delapouite",
    "cargo-ship":           "delapouite",
    "truck":                "delapouite",
}


def fetch_url(url: str) -> bytes | None:
    """Fetch URL, return bytes or None on error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read()
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return None


def process_svg(raw: bytes, accent_color: str = "#7A1F2B") -> str:
    """
    Process game-icons.net SVG per G-12 rules:
    1. Remove black background path (M0 0h512v512H0z or similar)
    2. Remove any fill="#000" or fill="#000000" on background paths
    3. Set remaining paths fill to currentColor (inherits CSS color)
    4. Add viewBox if missing, remove fixed width/height.
    Returns processed SVG string.
    """
    svg_text = raw.decode("utf-8", errors="replace")

    # Remove background path: no fill attr AND starts with M0 0h512v512H0
    # Pattern: <path d="M0 0h512v512H0z"/> or <path d="M0 0h512v512H0 0z"/>
    svg_text = re.sub(
        r'<path\s+d="M\s*0\s+0h\d+v\d+H\s*0[^"]*z"\s*/>',
        '',
        svg_text
    )
    # Also remove <rect> black backgrounds
    svg_text = re.sub(
        r'<rect[^>]*fill=["\'](?:#000000?|black)["\'][^>]*/?>',
        '',
        svg_text
    )

    # Set all remaining paths to currentColor
    # Replace fill="#fff" or fill="white" → fill="currentColor"
    svg_text = re.sub(r'fill=["\'](?:#fff(?:fff)?|white)["\']', 'fill="currentColor"', svg_text)

    # Remove fixed width/height from <svg> tag (let CSS control size)
    svg_text = re.sub(r'\s+width="\d+"', '', svg_text)
    svg_text = re.sub(r'\s+height="\d+"', '', svg_text)

    # Ensure xmlns present
    if 'xmlns=' not in svg_text:
        svg_text = svg_text.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)

    return svg_text.strip()


def try_download_icon(name: str) -> tuple[str | None, str | None]:
    """
    Try to download icon by name from known artist subfolders.
    Returns (svg_content_raw_bytes, source_url) or (None, None).
    """
    # First check curated catalog
    if name in STEEL_ICONS:
        artist = STEEL_ICONS[name]
        url = f"https://raw.githubusercontent.com/game-icons/icons/master/{artist}/{name}.svg"
        data = fetch_url(url)
        if data:
            return data, url

    # Try all artist bases
    for base in ICON_BASES:
        url = f"{base}/{name}.svg"
        data = fetch_url(url)
        if data and b"<svg" in data:
            return data, url

    return None, None


def cmd_search(keywords: list[str]):
    """Search curated catalog for keywords."""
    print(f"\nSearching for: {', '.join(keywords)}")
    print("-" * 50)
    found = []
    for icon_name in STEEL_ICONS:
        for kw in keywords:
            if kw.lower() in icon_name.lower():
                found.append((icon_name, STEEL_ICONS[icon_name]))
                break
    if found:
        print(f"Found {len(found)} icon(s) in curated catalog:\n")
        for name, artist in found:
            print(f"  {name:35s}  (artist: {artist})")
        print(f"\nTo download: python agents/icon_agent.py download {' '.join(n for n, _ in found)}")
    else:
        print("No matches in curated catalog.")
        print("Try: python agents/icon_agent.py download <exact-game-icons-name>")


def cmd_download(names: list[str]):
    """Download and process icons by name."""
    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for name in names:
        print(f"\n  [{name}] fetching...", end="", flush=True)
        raw, url = try_download_icon(name)
        if raw is None:
            print(f" NOT FOUND")
            results.append({"name": name, "status": "not_found", "url": None})
            continue

        processed = process_svg(raw)
        out_path = ICONS_DIR / f"{name}.svg"
        out_path.write_text(processed, encoding="utf-8")
        print(f" OK → dashboard/assets/icons/{name}.svg")
        print(f"         source: {url}")
        results.append({"name": name, "status": "ok", "url": url, "path": str(out_path)})

    # Update catalog
    _update_catalog(results)

    ok_count = sum(1 for r in results if r["status"] == "ok")
    print(f"\n✓ Downloaded {ok_count}/{len(names)} icon(s)")
    if ok_count > 0:
        print(f"  Location: dashboard/assets/icons/")
        print(f"  Catalog:  output/icon_catalog.md")


def cmd_catalog():
    """Show catalog of all downloaded icons."""
    if not ICONS_DIR.exists():
        print("No icons downloaded yet. Run: python agents/icon_agent.py download <name>")
        return

    icons = sorted(ICONS_DIR.glob("*.svg"))
    if not icons:
        print("Icons directory is empty.")
        return

    print(f"\n{'Icon name':35s} {'Size':>8s}  Path")
    print("-" * 70)
    for icon in icons:
        size = icon.stat().st_size
        print(f"  {icon.stem:33s} {size:>7d}B  dashboard/assets/icons/{icon.name}")
    print(f"\nTotal: {len(icons)} icon(s)")


def cmd_process(src_path_str: str, output_name: str | None = None):
    """
    Process a locally downloaded SVG file per G-12 rules and save to assets/icons/.

    Args:
        src_path_str: Path to the downloaded SVG file (any location on disk)
        output_name:  Name for the output file (without .svg). Defaults to source filename stem.

    Example:
        icon_agent.py process C:\\Downloads\\rebar.svg armatury
        → saves to dashboard/assets/icons/armatury.svg
    """
    src = Path(src_path_str)
    if not src.exists():
        print(f"ERROR: file not found: {src}")
        return
    if src.suffix.lower() != ".svg":
        print(f"ERROR: expected .svg file, got: {src.suffix}")
        return

    name = output_name or src.stem
    # Sanitize name: lowercase, spaces→hyphens, remove unsafe chars
    name = re.sub(r"[^\w\-]", "-", name.lower()).strip("-")

    raw = src.read_bytes()
    processed = process_svg(raw)

    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ICONS_DIR / f"{name}.svg"
    out_path.write_text(processed, encoding="utf-8")

    print(f"\n[process] {src.name} → dashboard/assets/icons/{name}.svg")
    print(f"  Size: {len(raw)} → {len(processed.encode())} bytes")

    # Quick sanity check
    has_bg = "M0 0h512" in processed or "M0 0h512" in processed
    has_color = "currentColor" in processed
    print(f"  Background removed: {'YES' if not has_bg else 'CHECK MANUALLY'}")
    print(f"  currentColor set:   {'YES' if has_color else 'NO — fill may be hardcoded'}")

    if not has_color:
        print("\n  HINT: No currentColor found. If icon appears black/invisible,")
        print("  manually add fill='currentColor' to the <path> elements in the SVG.")

    _update_catalog([{"name": name, "status": "ok", "url": str(src), "path": str(out_path)}])
    print(f"\n  Use in HTML: <img src='assets/icons/{name}.svg' style='width:24px'>")
    print(f"  Or inline:   fetch('assets/icons/{name}.svg').then embed as <svg>")


def cmd_list():
    """List all icons in curated catalog."""
    print(f"\nCurated steel-industry icon catalog ({len(STEEL_ICONS)} icons):\n")
    by_artist: dict[str, list[str]] = {}
    for name, artist in STEEL_ICONS.items():
        by_artist.setdefault(artist, []).append(name)

    for artist, names in sorted(by_artist.items()):
        print(f"  {artist}:")
        for n in names:
            dl = "✓" if (ICONS_DIR / f"{n}.svg").exists() else "·"
            print(f"    {dl} {n}")
        print()

    if ICONS_DIR.exists():
        downloaded = len(list(ICONS_DIR.glob("*.svg")))
        print(f"Downloaded: {downloaded}/{len(STEEL_ICONS)}")


def _update_catalog(results: list[dict]):
    """Append download results to output/icon_catalog.md."""
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Read existing catalog or create header
    if CATALOG_PATH.exists():
        existing = CATALOG_PATH.read_text(encoding="utf-8")
    else:
        existing = (
            "# Icon Catalog — Czech Steel Dashboard\n\n"
            "Icons sourced from game-icons.net (CC BY 3.0).\n"
            "Processed per G-12: background removed, fill=currentColor.\n\n"
            "| Icon | Status | Source | Local path |\n"
            "|------|--------|--------|------------|\n"
        )

    new_rows = []
    for r in results:
        status = "✓" if r["status"] == "ok" else "✗ not found"
        url_md = f"[link]({r['url']})" if r.get("url") else "—"
        path_md = f"`dashboard/assets/icons/{r['name']}.svg`" if r["status"] == "ok" else "—"
        new_rows.append(f"| {r['name']} | {status} | {url_md} | {path_md} |")

    updated = existing.rstrip() + "\n" + "\n".join(new_rows) + "\n"
    CATALOG_PATH.write_text(updated, encoding="utf-8")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0].lower()
    rest = args[1:]

    if cmd == "search":
        if not rest:
            print("Usage: icon_agent.py search <keyword> [keyword2 ...]")
        else:
            cmd_search(rest)

    elif cmd == "download":
        if not rest:
            print("Usage: icon_agent.py download <icon-name> [icon2 ...]")
            print("Tip:   icon_agent.py list   ← shows all curated names")
        else:
            cmd_download(rest)

    elif cmd == "process":
        if not rest:
            print("Usage: icon_agent.py process <path/to/file.svg> [output-name]")
            print("Example: icon_agent.py process C:\\Downloads\\rebar.svg armatury")
        else:
            src = rest[0]
            name = rest[1] if len(rest) > 1 else None
            cmd_process(src, name)

    elif cmd == "catalog":
        cmd_catalog()

    elif cmd == "list":
        cmd_list()

    else:
        print(f"Unknown command: {cmd}")
        print("Commands: search | download | catalog | list")


if __name__ == "__main__":
    main()
