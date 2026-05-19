@echo off

echo Czech Steel Dashboard - Agent Runner
echo =====================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

echo Step 1 of 2 - QA Agent (pure Python, fast)
echo --------------------------------------------
python agents\qa_agent.py
if %errorlevel% neq 0 (
    echo ERROR: QA Agent failed
    pause
    exit /b 1
)

echo.
echo Step 2 of 2 - Docker build and launch
echo ---------------------------------------
docker compose up --build -d
if %errorlevel% neq 0 (
    echo ERROR: Docker failed. Is Docker Desktop running?
    pause
    exit /b 1
)

echo.
echo =====================================
echo DONE
echo QA report:  output\qa_report.md
echo Dashboard:  http://localhost:8080
echo =====================================
start http://localhost:8080
pause
