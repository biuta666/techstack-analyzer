@echo off
title TechStack Analyzer
echo ==============================================
echo   TechStack Analyzer - Technology Intelligence
echo ==============================================
echo.
pip install -r requirements.txt -q
echo [OK] Starting on http://localhost:8010
echo.
echo   API:         http://localhost:8010/scan?url=example.com
echo   Report:      http://localhost:8010/report?url=example.com
echo   Health:      http://localhost:8010/health
echo.
python api/server.py
