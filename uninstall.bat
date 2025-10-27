@echo off
:: ============================================================
:: SpotlightNow Uninstaller
:: NOTE: This script must be run with Administrator rights.
:: Required because:
::   - Scheduled tasks are created/removed with elevated privileges
::   - Registry policies under HKLM are deleted
::   - Application data at C:\ProgramData\SpotlightNow is removed
:: ============================================================

:: --- Self-elevate to Administrator if not already ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs -WorkingDirectory '%~dp0'"
    exit /b
)

setlocal

REM Script directory (always points to where uninstall.bat lives)
set SCRIPT_DIR=%~dp0
set TARGET_DIR=C:\ProgramData\SpotlightNow

:: remove scheduled tasks
schtasks /Delete /TN "SpotlightNow-Download" /F
schtasks /Delete /TN "SpotlightNow-UpdateLockscreen" /F

:: call uninstall function in spotlight-now.exe
echo Running SpotlightNow uninstall ...
call "%TARGET_DIR%\spotlight-now.exe" uninstall

echo Deleting files in %TARGET_DIR% ...
rd /S /Q "%TARGET_DIR%"

echo Uninstallation complete.
pause
endlocal