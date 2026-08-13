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
    echo Please install Python 3.10 or newer.
    echo Make sure "Add Python to PATH" is enabled
    echo during Python installation.
    echo.
    pause
    exit /b 1
)

echo Python found.
python --version
echo.

echo Installing required Python packages...
echo.

python -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo ERROR: Could not update pip.
    echo.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install required packages.
    echo.
    pause
    exit /b 1
)

echo.
echo Installing Playwright Chromium browser...
echo.

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
echo.

set "APP_DIR=%~dp0"
set "RUN_FILE=%APP_DIR%run.bat"

for /f "usebackq delims=" %%D in (`powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"`) do set "DESKTOP=%%D"

if not exist "%DESKTOP%" (
    echo.
    echo WARNING: Desktop folder could not be found.
    echo.
    echo Setup is otherwise complete.
    echo You can start the application using run.bat.
    echo.
    pause
    exit /b 0
)

set "SHORTCUT=%DESKTOP%\Attendance Report Automation.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%RUN_FILE%'; $s.WorkingDirectory = '%APP_DIR%'; $s.Description = 'Attendance Report Automation'; $s.Save()"

if exist "%SHORTCUT%" (
    echo.
    echo ==============================================
    echo       SETUP COMPLETED SUCCESSFULLY
    echo ==============================================
    echo.
    echo Desktop shortcut created:
    echo.
    echo     Attendance Report Automation
    echo.
    echo You can now launch the application
    echo using the desktop shortcut.
    echo.
) else (
    echo.
    echo ==============================================
    echo   SETUP COMPLETED - SHORTCUT NOT CREATED
    echo ==============================================
    echo.
    echo You can start the application manually using:
    echo.
    echo     run.bat
    echo.
)

pause