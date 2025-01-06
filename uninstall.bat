@echo off
setlocal EnableDelayedExpansion

:: Admin check and elevation
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo [*] Requesting admin rights...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo [*] Starting uninstallation...

:: Kill process if running
echo [*] Stopping running processes...
taskkill /F /IM "shortcuts_tray.exe" >nul 2>&1
if !ERRORLEVEL! equ 0 (
    echo [*] Process terminated, waiting for cleanup...
    timeout /t 3 /nobreak >nul
)

:: Remove Defender exclusion
echo [*] Removing Windows Defender exclusion...
powershell -Command "Remove-MpPreference -ExclusionPath '%USERPROFILE%\negative\shortcuts_tray'" 2>nul

:: Remove shortcuts
echo [*] Removing shortcuts...
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\shortcuts_tray.lnk" (
    del /F /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\shortcuts_tray.lnk"
)
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\shortcuts_tray.lnk" (
    del /F /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\shortcuts_tray.lnk"
)

:: Remove program files with retry
echo [*] Removing program files...
set "MAX_ATTEMPTS=3"
:retry_remove
if exist "%USERPROFILE%\negative\shortcuts_tray" (
    rd /S /Q "%USERPROFILE%\negative\shortcuts_tray" 2>nul
    if !ERRORLEVEL! neq 0 (
        echo [!] Failed to remove files, retrying...
        timeout /t 2 /nobreak >nul
        set /a MAX_ATTEMPTS-=1
        if !MAX_ATTEMPTS! gtr 0 goto :retry_remove
        echo [!] Could not remove some files. Please:
        echo     1. Close any programs using the files
        echo     2. Try running this uninstaller again
        echo     3. If still failing, restart computer and retry
        echo [*] Path to check: %USERPROFILE%\negative\shortcuts_tray
    )
)

:: Try to remove parent folder if empty
rd "%USERPROFILE%\negative" 2>nul

echo.
echo [*] Uninstallation complete!
if exist "%USERPROFILE%\negative\shortcuts_tray" (
    echo [!] Note: Some files may need manual removal after restart
)
pause