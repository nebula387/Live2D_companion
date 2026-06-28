@echo off
title Nika Companion Launcher
color 0A

echo ==========================================
echo   Nika - English Teacher ^& Companion
echo ==========================================
echo.

:: ─── ПУТИ — УКАЖИ СВОИ ───────────────────────────────
set LM_STUDIO_PATH=C:\Program Files\LM Studio\LM Studio.exe
set VTUBE_PATH=C:\Program Files (x86)\Steam\steamapps\common\VTube Studio\VTube Studio.exe
set NIKA_SCRIPT=C:\AI\nika.py

:: ─── ЗАДЕРЖКИ (секунды) ──────────────────────────────
set LM_DELAY=15
set VTUBE_DELAY=8

:: ─── ЗАПУСК LM STUDIO ────────────────────────────────
echo [1/3] Starting LM Studio...
start "" "%LM_STUDIO_PATH%"
echo     Waiting %LM_DELAY% seconds for LM Studio to load...
timeout /t %LM_DELAY% /nobreak >nul

:: ─── ЗАПУСК VTUBE STUDIO ─────────────────────────────
echo [2/3] Starting VTube Studio...
start "" "%VTUBE_PATH%"
echo     Waiting %VTUBE_DELAY% seconds for VTube Studio to load...
timeout /t %VTUBE_DELAY% /nobreak >nul

:: ─── ЗАПУСК PYTHON СКРИПТА ───────────────────────────
echo [3/3] Starting Nika...
echo.
echo ==========================================
echo   Say NIKA to start talking!
echo   Type 'quit' to exit
echo ==========================================
echo.
python "%NIKA_SCRIPT%"

echo.
echo Nika has stopped. Press any key to exit.
pause >nul
