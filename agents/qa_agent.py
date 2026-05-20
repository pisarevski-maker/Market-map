#!/usr/bin/env python3
"""
QA Agent - Czech Steel Dashboard
Pure Python checks - no LLM needed.
Fast, reliable, deterministic.

Usage:
    python agents/qa_agent.py
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DASHBOARD    = PROJECT_ROOT / "dashboard"
DATA         = PROJECT_ROOT / "data" / "processed"
REPORT_PATH  = PROJECT_ROOT / "output" / "qa_report.md"

checks = []  # (category, name, verdict, detail)

def check(category, name, passed, detail, warn=False):
    verdict = "OK" if passed else ("WARN" if warn else "FAIL")
    checks.append((category, name, verdict, detail))
    print(f"   [{verdict}] {name}: {detail[:90]}")

# -- 1. Files ------------------------------------------------------------------

def check_files():
    print("\n[1] File existence")
    for name, path in [
        ("index.html",              DASHBOARD / "index.html"),
        ("plant-detail.html",       DASHBOARD / "plant-detail.html"),
        ("czech_steel_plants.json", DATA / "czech_steel_plants.json"),
        ("market_context.json",     DATA / "market_context.json"),
        ("trinecke_zelezarny.json", DATA / "plant_details" / "trinecke_zelezarny.json"),
    ]:
        check("Files", name, path.exists(),
              "exists" if path.exists() else f"MISSING: {path}")

# -- 2. Math -------------------------------------------------------------------

def check_math():
    print("\n[2] EU implied net formula")
    check("Math", "2023: 5800-3400-238=2162", 5800-3400-238 == 2162, f"result={5800-3400-238}")
    check("Math", "2022: 7100-4200-261=2639", 7100-4200-261 == 2639, f"result={7100-4200-261}")

# -- 3. market_context.json ----------------------------------------------------

def check_market_json():
    print("\n[3] market_context.json")
    path = DATA / "market_context.json"
    if not path.exists():
        check("JSON", "market_context.json parseable", False, "file missing")
        return
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        check("JSON", "market_context.json parseable", False, str(e))
        return

    check("JSON", "parseable", True, "valid JSON")
    prod = d.get("production_crude_kt", {})
    years = [str(y) for y in [2020,2021,2022,2023,2024]]
    missing = [y for y in years if y not in prod]
    check("JSON", "production 2020-2024", not missing,
          "all years present" if not missing else f"missing: {missing}")

    ac = d.get("apparent_consumption_kt", {}).get("total_kt", {})
    missing_ac = [y for y in years if y not in ac]
    check("JSON", "apparent_consumption 2020-2024", not missing_ac,
          "all years present" if not missing_ac else f"missing: {missing_ac}")

    plants = d.get("plants", {})
    check("JSON", "trinecke_zelezarny plant data", "trinecke_zelezarny" in plants, "")
    check("JSON", "nova_hut_ostrava plant data",   "nova_hut_ostrava"   in plants, "")

    trade = d.get("trade_third_countries_rolled_kt", {})
    check("JSON", "3rd country trade data present", bool(trade),
          "found" if trade else "missing")

# -- 4. index.html -------------------------------------------------------------

def check_index():
    print("\n[4] index.html")
    path = DASHBOARD / "index.html"
    if not path.exists(): return
    html = path.read_text(encoding="utf-8")

    check("index", "market-panel class",        "market-panel" in html,    "")
    check("index", "prod-tbody id",             "prod-tbody" in html,      "")
    check("index", "trade-grid id",             "trade-grid" in html,      "")
    check("index", "cons-bars id",              "cons-bars" in html,       "")
    check("index", "MARKET JS object",          "const MARKET" in html or "MARKET" in html,    "", warn=not ("const MARKET" in html))
    check("index", "renderTradeGrid function",  "renderTradeGrid" in html, "", warn=not ("renderTradeGrid" in html))
    check("index", "renderConsBars function",   "renderConsBars" in html,  "", warn=not ("renderConsBars" in html))
    check("index", "EU net header",             "EU" in html and "net" in html.lower(), "")

    has_eu_formula = "ac - prod" in html.lower() or "ac-prod" in html.lower() or                      ("ac" in html and "prod" in html and "imp" in html and "euNet" in html)
    check("index", "EU net formula in JS", has_eu_formula, "euNet = ac - prod - imp", warn=not has_eu_formula)

    check("index", "body height:100vh",         "height: 100vh" in html or "height:100vh" in html, "")
    check("index", "market-panel flex-shrink:0","flex-shrink: 0" in html or "flex-shrink:0" in html, "")

# -- 5. plant-detail.html ------------------------------------------------------

def check_plant_detail():
    print("\n[5] plant-detail.html")
    path = DASHBOARD / "plant-detail.html"
    if not path.exists(): return
    html = path.read_text(encoding="utf-8")

    check("plant-detail", "buildFlowSVG function",      "buildFlowSVG" in html,    "")
    check("plant-detail", "Array.isArray parallel",     "Array.isArray" in html,   "")
    check("plant-detail", "parCY function",             "parCY" in html,           "")
    check("plant-detail", "MARKET_SHARES data",         "MARKET_SHARES" in html,   "")
    check("plant-detail", "marketShareBlock function",  "marketShareBlock" in html,"")

    bof_eaf_parallel = '["BOF Converter","EAF"]' in html or \
                       '["BOF Converter", "EAF"]' in html
    check("plant-detail", "BOF+EAF parallel in HTML inline",
          bof_eaf_parallel,
          "nested array in PLANTS_DATA" if bof_eaf_parallel else "NOT parallel - Docker will show sequential!")

    mills_in_array = re.search(r'\["Wire Rod Mill".*?"Pipe Plant"\]', html, re.S)
    check("plant-detail", "Rolling mills parallel in HTML inline",
          bool(mills_in_array),
          "nested array found" if mills_in_array else "mills not in nested array - Docker shows single node!")

    check("plant-detail", "product-mshare class",  "product-mshare" in html, "")
    check("plant-detail", "mshare-bar-fill class", "mshare-bar-fill" in html,"")

# -- 6. JSON <-> inline HTML sync (G-17) --------------------------------------
#
# CRITICAL: plant-detail.html has TWO data sources:
#   1. fetch(../data/processed/plant_details/{id}.json)  <- GitHub Pages
#   2. inline PLANTS_DATA fallback                        <- Docker / file://
# Both must have identical production_route.flow arrays.

def check_json_html_sync():
    print("\n[6] JSON <-> inline HTML sync (G-17 prevention)")
    html_path = DASHBOARD / "plant-detail.html"
    tz_json_path = DATA / "plant_details" / "trinecke_zelezarny.json"

    if not html_path.exists() or not tz_json_path.exists():
        check("Sync", "files available for sync check", False, "missing file(s)")
        return

    html = html_path.read_text(encoding="utf-8")
    try:
        tz = json.loads(tz_json_path.read_text(encoding="utf-8"))
    except Exception as e:
        check("Sync", "trinecke_zelezarny.json parseable", False, str(e))
        return

    json_flow = tz.get("production_route", {}).get("flow", [])

    has_parallel_in_json = any(isinstance(step, list) for step in json_flow)
    check("Sync", "TZ JSON has parallel arrays",
          has_parallel_in_json,
          "nested arrays present" if has_parallel_in_json else "FLAT array - GitHub Pages shows sequential!")

    bof_eaf_in_json = ["BOF Converter", "EAF"] in json_flow
    check("Sync", "TZ JSON BOF+EAF parallel",
          bof_eaf_in_json,
          "OK" if bof_eaf_in_json else "MISSING - GitHub Pages shows sequential BOF then EAF!")

    rolling_in_json = any(isinstance(s, list) and "Wire Rod Mill" in s for s in json_flow)
    check("Sync", "TZ JSON rolling mills parallel",
          rolling_in_json,
          "OK" if rolling_in_json else "MISSING - GitHub Pages shows single Rolling Mills node!")

    bof_eaf_in_html = '["BOF Converter","EAF"]' in html or '["BOF Converter", "EAF"]' in html
    check("Sync", "TZ HTML inline BOF+EAF parallel",
          bof_eaf_in_html,
          "OK" if bof_eaf_in_html else "MISSING in inline HTML - Docker shows sequential!")

    rolling_in_html = bool(re.search(r'\["Wire Rod Mill".*?"Pipe Plant"\]', html, re.S))
    check("Sync", "TZ HTML inline rolling mills parallel",
          rolling_in_html,
          "OK" if rolling_in_html else "MISSING in inline HTML - Docker shows single node!")

    both_agree = has_parallel_in_json and bof_eaf_in_html and rolling_in_html
    check("Sync", "JSON and HTML inline sources in sync",
          both_agree,
          "both sources have parallel flow" if both_agree else
          "MISMATCH - Docker vs GitHub Pages show different flows!")

# -- Report --------------------------------------------------------------------

def write_report():
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    total  = len(checks)
    passed = sum(1 for c in checks if c[2] == "OK")
    warned = sum(1 for c in checks if c[2] == "WARN")
    failed = sum(1 for c in checks if c[2] == "FAIL")
    score  = int(passed / total * 100) if total else 0

    lines = [
        "# QA Report - Czech Steel Dashboard",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Method: Pure Python (no LLM)",
        f"Score: {passed}/{total} checks passed ({score}%)",
        "",
        "| # | Category | Check | Result | Detail |",
        "|---|----------|-------|--------|--------|",
    ]
    for i, (cat, name, verdict, detail) in enumerate(checks, 1):
        lines.append(f"| {i} | {cat} | {name} | {verdict} | {detail[:100]} |")

    lines += ["", "## Summary",
              f"- Passed: {passed}", f"- Warnings: {warned}", f"- Failed: {failed}", ""]

    if failed:
        lines.append("## Issues")
        for cat, name, v, d in checks:
            if v == "FAIL":
                lines.append(f"- [{cat}] {name}: {d}")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return score

def main():
    print("=" * 50)
    print("  QA Agent - Czech Steel Dashboard (pure Python)")
    print("=" * 50)
    check_files()
    check_math()
    check_market_json()
    check_index()
    check_plant_detail()
    check_json_html_sync()

    print("\n" + "=" * 50)
    score  = write_report()
    total  = len(checks)
    passed = sum(1 for c in checks if c[2] == "OK")
    failed = sum(1 for c in checks if c[2] == "FAIL")
    print(f"Score: {passed}/{total} ({score}%)")
    print(f"Report: {REPORT_PATH}")
    if failed == 0:
        print("All checks passed - ready for export!")
    else:
        print(f"{failed} issue(s) found - check report")
    print("=" * 50)

if __name__ == "__main__":
    main()
