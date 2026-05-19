@echo off
docker compose up --build -d
echo.
echo Dashboard started at http://localhost:8080
start http://localhost:8080
