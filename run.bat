@echo off
cd /d "%~dp0"

python main.py

if errorlevel 1 (
    echo.
    echo Attendance Automation stopped because an error occurred.
    pause
)