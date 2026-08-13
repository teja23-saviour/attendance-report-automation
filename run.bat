@echo off
title Attendance Report Automation

cd /d "%~dp0"

python main.py

if errorlevel 1 (
    echo.
    echo ==============================================
    echo   Attendance Automation stopped with an error
    echo ==============================================
    echo.
    pause
)