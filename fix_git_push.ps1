# fix_git_push.ps1
# Fixes git stat-cache bug on Windows+OneDrive+Cyrillic path
# Run once in PowerShell from ANY directory — script uses absolute path

$repo = "C:\Users\po44t\OneDrive\Документы\Claude\Projects\Map of Czech\czech-steel-dashboard"

Set-Location $repo

Write-Host "=== Step 1: Delete git index (stat cache) ===" -ForegroundColor Cyan
Remove-Item ".git\index" -Force
Write-Host "  index deleted"

Write-Host "=== Step 2: Rebuild index and stage all files ===" -ForegroundColor Cyan
git add -A
git status

Write-Host "=== Step 3: Commit ===" -ForegroundColor Cyan
git commit -m "feat: parallel rolling mills flow + EU net import + pure Python QA/export agents"

Write-Host "=== Step 4: Push to GitHub ===" -ForegroundColor Cyan
git push origin master

Write-Host ""
Write-Host "Done! GitHub Pages will update in ~1 minute." -ForegroundColor Green
Write-Host "URL: https://pisarevski-maker.github.io/Market-map/dashboard/index.html"
