@echo off
:: ============================================================
:: SpotlightNow Installer
:: NOTE: This script requires Administrator rights.
::       Admin is required because scheduled tasks must run
::       with elevated privileges and files are written to
::       C:\ProgramData\SpotlightNow.
:: ============================================================

:: --- Self-elevate to Administrator if not already ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs -WorkingDirectory '%~dp0'"
    exit /b
)

setlocal

REM Script directory (always points to where install.bat lives)
set SCRIPT_DIR=%~dp0
set TARGET_DIR=C:\ProgramData\SpotlightNow

echo Creating %TARGET_DIR% ...
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

echo Copying spotlight-now.exe and config.json ...
copy /Y "%SCRIPT_DIR%spotlight-now.exe" "%TARGET_DIR%"
copy /Y "%SCRIPT_DIR%config.json" "%TARGET_DIR%"

echo Running PowerShell setup scripts ...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%download-task.ps1"
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%update-task.ps1"

echo Installation complete.
pause
endlocal