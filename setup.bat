@echo off
setlocal

title Attendance Report Automation - Setup

cd /d "%~dp0"

echo ==============================================
echo     ATTENDANCE REPORT AUTOMATION SETUP
echo ==============================================
echo.

echo Checking Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python was not found.
    echo.
    echo Please install Python 3.10 or newer and
    echo make sure "Add Python to PATH" is enabled.
    echo.
    pause
    exit /b 1
)

echo Python found.
echo.

echo Installing required packages...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Python packages.
    echo.
    pause
    exit /b 1
)

echo.
echo Installing Playwright Chromium...
python -m playwright install chromium

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install Playwright Chromium.
    echo.
    pause
    exit /b 1
)

echo.
echo Creating Desktop shortcut...

set "APP_DIR=%~dp0"
set "RUN_FILE=%APP_DIR%run.bat"

for /f "usebackq delims=" %%D in (`powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"`) do set "DESKTOP=%%D"

if not exist "%DESKTOP%" (
    echo.
    echo WARNING: Could not find Desktop folder.
    echo Setup is otherwise complete.
    echo.
    pause
    exit /b 0
)

set "SHORTCUT=%DESKTOP%\Attendance Report Automation.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%RUN_FILE%'; $s.WorkingDirectory = '%APP_DIR%'; $s.Description = 'Attendance Report Automation'; $s.Save()"

if exist "%SHORTCUT%" (
    echo.
    echo ==============================================
    echo          SETUP COMPLETED SUCCESSFULLY
    echo ==============================================
    echo.
    echo A desktop shortcut has been created:
    echo.
    echo     Attendance Report Automation
    echo.
    echo You can use that shortcut to start the
    echo application from now on.
    echo.
) else (
    echo.
    echo ==============================================
    echo SETUP COMPLETED, BUT SHORTCUT FAILED
    echo ==============================================
    echo.
    echo You can still start the application using:
    echo run.bat
    echo.
)

pause