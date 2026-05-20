#!/usr/bin/env python3
"""
Icon Update Agent - Czech Steel Dashboard
Double-click icon_update.bat to run.

Workflow:
  1. Read all SVGs from dashboard/assets/icons/new/
  2. Validate name exists in icons/slots.json
  3. Process SVG (G-12: remove background, set currentColor)
  4. Move old in-use/{name}.svg  ->  unused/
  5. Write processed SVG to     ->  in-use/
  6. Git commit + push

Folder structure:
  dashboard/assets/icons/
    raw/     <- drop downloaded SVGs here (any name, for browsing)
    new/     <- rename to slot name (e.g. eq_blast_furnace.svg), put here
    in-use/  <- active icons referenced by dashboard HTML/JS
    unused/  <- replaced icons (archived, not deleted)
"""

import re
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
ICONS_BASE   = PROJECT_ROOT / "dashboard" / "assets" / "icons"
RAW_DIR      = ICONS_BASE / "raw"
NEW_DIR      = ICONS_BASE / "new"
IN_USE_DIR   = ICONS_BASE / "in-use"
UNUSED_DIR   = ICONS_BASE / "unused"
SLOTS_FILE   = PROJECT_ROOT / "icons" / "slots.json"

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def load_slots() -> dict:
    if not SLOTS_FILE.exists():
        print(f"{RED}ERROR: slots.json not found at {SLOTS_FILE}{RESET}")
        sys.exit(1)
    data = json.loads(SLOTS_FILE.read_text(encoding="utf-8"))
    all_slots = {}
    for category, entries in data.items():
        if category.startswith("_"):
            continue
        for slot_name, slot_data in entries.items():
            if slot_name.startswith("_"):
                continue
            all_slots[slot_name] = {**slot_data, "_category": category}
    return all_slots


def process_svg(raw: bytes) -> str:
    """
    G-12: Clean up game-icons.net SVG (or any SVG with black bg).
    - Remove black background path M0 0h512v512H0z
    - Remove black <rect> backgrounds
    - Replace fill="#fff"/fill="white" with fill="currentColor"
    - Remove fixed width/height (CSS controls size)
    """
    text = raw.decode("utf-8", errors="replace")

    # Remove background path (no fill, covers entire viewBox)
    text = re.sub(r'<path\s+d="M\s*0\s+0h\d+v\d+H\s*0[^"]*z"\s*/?>', '', text)
    text = re.sub(r'<path\s+d="M0,0h\d+v\d+H0[^"]*z"\s*/?>', '', text)

    # Remove black rect backgrounds
    text = re.sub(r'<rect[^>]*fill=["\'](?:#000000?|black)["\'][^>]*/?>',  '', text)
    text = re.sub(r'<rect[^>]*(?:width|height)=["\']\d+["\'][^>]*fill=["\'](?:#000000?|black)["\'][^>]*/?>',  '', text)

    # White fill -> currentColor
    text = re.sub(r'fill=["\'](?:#fff(?:fff)?|white)["\']', 'fill="currentColor"', text)

    # Remove hardcoded size (let CSS control)
    text = re.sub(r'\s+width="\d+"', '', text)
    text = re.sub(r'\s+height="\d+"', '', text)

    # Ensure xmlns
    if 'xmlns=' not in text:
        text = text.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)

    return text.strip()


def git_commit_push(changed: list[str]) -> bool:
    """Commit changed icon files and push to origin/master."""
    try:
        # Delete index to force git to re-scan (G-16 workaround)
        index = PROJECT_ROOT / ".git" / "index"
        if index.exists():
            index.unlink()

        subprocess.run(["git", "-C", str(PROJECT_ROOT), "add", "-A"],
                       check=True, capture_output=True)

        names = ", ".join(changed[:3])
        if len(changed) > 3:
            names += f" +{len(changed)-3} more"
        msg = f"icons: update {len(changed)} slot(s) — {names}"

        subprocess.run(["git", "-C", str(PROJECT_ROOT), "commit", "-m", msg],
                       check=True, capture_output=True)

        result = subprocess.run(["git", "-C", str(PROJECT_ROOT), "push", "origin", "master"],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{YELLOW}  Push warning: {result.stderr.strip()}{RESET}")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}  Git error: {e.stderr.decode() if e.stderr else e}{RESET}")
        return False


def main():
    print()
    print(f"{BOLD}{'='*55}{RESET}")
    print(f"{BOLD}  Icon Update Agent — Czech Steel Dashboard{RESET}")
    print(f"{'='*55}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Ensure dirs exist
    for d in [RAW_DIR, NEW_DIR, IN_USE_DIR, UNUSED_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    # Load slot dictionary
    slots = load_slots()
    print(f"  Slots loaded: {len(slots)} valid slot names")

    # Find SVGs in new/
    new_files = sorted(NEW_DIR.glob("*.svg"))
    if not new_files:
        print(f"\n{YELLOW}  No SVGs found in new/ folder.{RESET}")
        print(f"  Put your SVGs there named by slot (e.g. eq_blast_furnace.svg)")
        print(f"\n  Valid slot names:")
        for name, data in slots.items():
            print(f"    {name:30s}  {data['label']}")
        print()
        input("  Press Enter to exit...")
        return

    print(f"\n  Found {len(new_files)} SVG(s) in new/\n")

    applied   = []
    skipped   = []
    warnings  = []

    for svg_path in new_files:
        slot_name = svg_path.stem
        print(f"  [{slot_name}]")

        # Validate slot name
        if slot_name not in slots:
            print(f"    {RED}UNKNOWN SLOT — skipping{RESET}")
            print(f"    Hint: rename file to a valid slot name (see list above)")
            skipped.append(slot_name)
            continue

        slot_info = slots[slot_name]
        print(f"    Slot: {slot_info['label']}")

        # Read and process SVG
        raw = svg_path.read_bytes()
        processed = process_svg(raw)

        # Sanity checks
        has_remaining_bg = re.search(r'<rect[^>]*fill=["\'](?:#000|black)["\']', processed)
        has_color = "currentColor" in processed

        if has_remaining_bg:
            warnings.append(f"{slot_name}: possible background not removed")
            print(f"    {YELLOW}WARN: possible background path remaining — check visually{RESET}")
        if not has_color:
            warnings.append(f"{slot_name}: no currentColor — may appear black or invisible")
            print(f"    {YELLOW}WARN: no currentColor found — check fill manually{RESET}")

        # Archive old in-use if exists
        existing = IN_USE_DIR / f"{slot_name}.svg"
        if existing.exists():
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive = UNUSED_DIR / f"{slot_name}_{ts}.svg"
            shutil.move(str(existing), str(archive))
            print(f"    Archived old → unused/{archive.name}")

        # Write processed SVG to in-use/
        dest = IN_USE_DIR / f"{slot_name}.svg"
        dest.write_text(processed, encoding="utf-8")
        print(f"    {GREEN}OK → in-use/{slot_name}.svg{RESET}")

        # Remove from new/
        svg_path.unlink()
        applied.append(slot_name)

    # Summary
    print()
    print(f"{'='*55}")
    print(f"  Applied:  {len(applied)}  |  Skipped: {len(skipped)}")

    if warnings:
        print(f"\n  {YELLOW}Warnings:{RESET}")
        for w in warnings:
            print(f"    - {w}")

    # Coverage report
    covered  = [s for s in slots if (IN_USE_DIR / f"{s}.svg").exists()]
    missing  = [s for s in slots if not (IN_USE_DIR / f"{s}.svg").exists()]
    pct = int(len(covered) / len(slots) * 100) if slots else 0
    print(f"\n  Coverage: {len(covered)}/{len(slots)} slots filled ({pct}%)")
    if missing:
        print(f"  Still missing ({len(missing)}):")
        for m in missing[:10]:
            print(f"    - {m:30s}  {slots[m]['label']}")
        if len(missing) > 10:
            print(f"    ... and {len(missing)-10} more")

    # Git
    if applied:
        print(f"\n  Running git commit + push...")
        ok = git_commit_push(applied)
        if ok:
            print(f"  {GREEN}Pushed to GitHub{RESET}")
        else:
            print(f"  {YELLOW}Push failed — commit is local, push manually{RESET}")
    else:
        print(f"\n  Nothing applied — no git commit.")

    print(f"{'='*55}")
    print()
    input("  Done. Press Enter to close...")


if __name__ == "__main__":
    main()
