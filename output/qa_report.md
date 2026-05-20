# QA Report - Czech Steel Dashboard

Date: 2026-05-20 08:47
Method: Pure Python (no LLM)
Score: 36/39 checks passed (92%)

| # | Category | Check | Result | Detail |
|---|----------|-------|--------|--------|
| 1 | Files | index.html | OK | exists |
| 2 | Files | plant-detail.html | OK | exists |
| 3 | Files | czech_steel_plants.json | OK | exists |
| 4 | Files | market_context.json | OK | exists |
| 5 | Files | trinecke_zelezarny.json | OK | exists |
| 6 | Math | 2023: 5800-3400-238=2162 | OK | result=2162 |
| 7 | Math | 2022: 7100-4200-261=2639 | OK | result=2639 |
| 8 | JSON | parseable | OK | valid JSON |
| 9 | JSON | production 2020-2024 | OK | all years present |
| 10 | JSON | apparent_consumption 2020-2024 | OK | all years present |
| 11 | JSON | trinecke_zelezarny plant data | OK |  |
| 12 | JSON | nova_hut_ostrava plant data | OK |  |
| 13 | JSON | 3rd country trade data present | OK | found |
| 14 | index | market-panel class | OK |  |
| 15 | index | prod-tbody id | OK |  |
| 16 | index | trade-grid id | OK |  |
| 17 | index | cons-bars id | OK |  |
| 18 | index | MARKET JS object | OK |  |
| 19 | index | renderTradeGrid function | WARN |  |
| 20 | index | renderConsBars function | WARN |  |
| 21 | index | EU net header | OK |  |
| 22 | index | EU net formula in JS | WARN | euNet = ac - prod - imp |
| 23 | index | body height:100vh | OK |  |
| 24 | index | market-panel flex-shrink:0 | OK |  |
| 25 | plant-detail | buildFlowSVG function | OK |  |
| 26 | plant-detail | Array.isArray parallel | OK |  |
| 27 | plant-detail | parCY function | OK |  |
| 28 | plant-detail | MARKET_SHARES data | OK |  |
| 29 | plant-detail | marketShareBlock function | OK |  |
| 30 | plant-detail | BOF+EAF parallel in HTML inline | OK | nested array in PLANTS_DATA |
| 31 | plant-detail | Rolling mills parallel in HTML inline | OK | nested array found |
| 32 | plant-detail | product-mshare class | OK |  |
| 33 | plant-detail | mshare-bar-fill class | OK |  |
| 34 | Sync | TZ JSON has parallel arrays | OK | nested arrays present |
| 35 | Sync | TZ JSON BOF+EAF parallel | OK | OK |
| 36 | Sync | TZ JSON rolling mills parallel | OK | OK |
| 37 | Sync | TZ HTML inline BOF+EAF parallel | OK | OK |
| 38 | Sync | TZ HTML inline rolling mills parallel | OK | OK |
| 39 | Sync | JSON and HTML inline sources in sync | OK | both sources have parallel flow |

## Summary
- Passed: 36
- Warnings: 3
- Failed: 0
