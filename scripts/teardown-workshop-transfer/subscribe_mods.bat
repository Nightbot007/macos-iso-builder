@echo off
setlocal
REM =========================================================
REM  Teardown Steam Workshop Mod Subscriber – Batch Launcher
REM  Runs subscribe_mods.ps1 in PowerShell (Windows 10/11)
REM =========================================================

echo.
echo  Teardown Workshop Mod Subscriber
echo  ---------------------------------
echo  This wrapper launches subscribe_mods.ps1
echo.
echo  For FULLY AUTOMATIC subscriptions (no clicking) run:
echo    python subscribe_mods.py --session-id ^<ID^> --steam-login-secure ^<VALUE^>
echo.
echo  See README.md for setup instructions.
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0subscribe_mods.ps1"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: PowerShell script failed with exit code %errorlevel%.
    echo Make sure PowerShell 5.1 or later is installed.
    pause
    exit /b %errorlevel%
)

pause
