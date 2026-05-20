#!/usr/bin/env python3
"""
fix_github.py — Fixes GitHub push via fresh clone in ASCII path.
Clones Market-map, copies the 5 updated files, commits and pushes.
"""
import subprocess, shutil, sys
from pathlib import Path

SRC  = Path(r"C:\Users\po44t\OneDrive\Документы\Claude\Projects\Map of Czech\czech-steel-dashboard")
TMP  = Path(r"C:\Temp\csd-clone")
REPO = "https://github.com/pisarevski-maker/Market-map.git"

FILES_TO_COPY = [
    ("dashboard/plant-detail.html",  "dashboard/plant-detail.html"),
    ("dashboard/index.html",         "dashboard/index.html"),
    ("agents/qa_agent.py",           "agents/qa_agent.py"),
    ("agents/export_agent.py",       "agents/export_agent.py"),
    ("run_agents.bat",               "run_agents.bat"),
    ("CLAUDE.md",                    "CLAUDE.md"),
    ("Dockerfile",                   "Dockerfile"),
    ("docker-compose.yml",           "docker-compose.yml"),
    ("nginx.conf",                   "nginx.conf"),
]

def run(cmd, cwd=None):
    print(f"  > {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if r.stdout.strip(): print(r.stdout.strip())
    if r.stderr.strip(): print(r.stderr.strip())
    return r.returncode

print("\n=== Step 1: Clean temp dir ===")
if TMP.exists():
    shutil.rmtree(TMP)

print("\n=== Step 2: Clone from GitHub ===")
rc = run(["git", "clone", REPO, str(TMP)])
if rc != 0:
    print("ERROR: clone failed"); sys.exit(1)

print("\n=== Step 3: Copy updated files ===")
for src_rel, dst_rel in FILES_TO_COPY:
    src_f = SRC / src_rel
    dst_f = TMP / dst_rel
    if src_f.exists():
        dst_f.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_f, dst_f)
        print(f"  copied: {src_rel}")
    else:
        print(f"  SKIP (not found): {src_rel}")

print("\n=== Step 4: Commit ===")
run(["git", "config", "user.email", "pisarevski@gmail.com"], cwd=TMP)
run(["git", "config", "user.name",  "pisarevski-maker"],      cwd=TMP)
run(["git", "add", "-A"],                                      cwd=TMP)
run(["git", "status"],                                         cwd=TMP)
rc = run(["git", "commit", "-m",
          "fix: parallel rolling mills flow + EU net import + pure Python QA/export agents"],
         cwd=TMP)

if rc != 0:
    print("Nothing to commit or error — check git status above")
    sys.exit(0)

print("\n=== Step 5: Push ===")
rc = run(["git", "push", "origin", "master"], cwd=TMP)
if rc == 0:
    print("\nDone! GitHub Pages updates in ~1 minute.")
    print("URL: https://pisarevski-maker.github.io/Market-map/dashboard/plant-detail.html")
else:
    print("\nERROR: push failed — may need GitHub token")
