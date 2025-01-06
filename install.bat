@echo off
setlocal EnableDelayedExpansion

:: Store the script's directory and ensure it's the working directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Admin check and elevation
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo [*] Requesting admin rights...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs -WorkingDirectory '%SCRIPT_DIR%'"
    exit /b
)

echo [*] Starting installation...
echo [*] Working directory: %CD%

:: Validate source exists
if not exist "shortcuts_tray" (
    echo [!] ERROR: shortcuts_tray folder not found
    echo [*] Please place this script next to the shortcuts_tray folder
    pause
    exit /b 1
)

:: Create install directory
echo [*] Creating installation directory...
mkdir "%USERPROFILE%\negative" 2>nul
mkdir "%USERPROFILE%\negative\shortcuts_tray" 2>nul

:: Copy files
echo [*] Copying program files...
xcopy /E /I /Y "shortcuts_tray\*" "%USERPROFILE%\negative\shortcuts_tray"

:: Verify installation
if not exist "%USERPROFILE%\negative\shortcuts_tray\shortcuts_tray.exe" (
    echo [!] ERROR: Installation failed - executable not found
    pause
    exit /b 1
)

:: Add to Windows Defender exclusions
echo [*] Adding Windows Defender exclusion...
powershell -Command "Add-MpPreference -ExclusionPath '%USERPROFILE%\negative\shortcuts_tray'"

:: Create shortcuts
echo [*] Creating shortcuts...
powershell -Command "$WShell = New-Object -ComObject WScript.Shell; $Shortcut = $WShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\shortcuts_tray.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\negative\shortcuts_tray\shortcuts_tray.exe'; $Shortcut.WorkingDirectory = '%USERPROFILE%\negative\shortcuts_tray'; $Shortcut.Save()"
powershell -Command "$WShell = New-Object -ComObject WScript.Shell; $Shortcut = $WShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\shortcuts_tray.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\negative\shortcuts_tray\shortcuts_tray.exe'; $Shortcut.WorkingDirectory = '%USERPROFILE%\negative\shortcuts_tray'; $Shortcut.Save()"

echo.
echo [*] Installation completed!
echo [*] Installation path: %USERPROFILE%\negative\shortcuts_tray
echo [*] Shortcuts created in Start Menu and Startup
pause