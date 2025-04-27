@echo off
title Keylogger Terminator - Windows 10/11 Compatible
color 0A
echo.
echo Checking and terminating keylogger processes...
echo.

echo [1/4] Looking for Python processes...
tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST
tasklist /FI "IMAGENAME eq python.exe" /FO LIST
echo.

echo [2/4] Attempting to terminate Python processes...
taskkill /F /IM pythonw.exe 2>nul
taskkill /F /IM python.exe 2>nul
echo.

echo [3/4] Looking for script host processes...
tasklist /FI "IMAGENAME eq wscript.exe" /FO LIST
taskkill /F /IM wscript.exe 2>nul
echo.

echo [4/4] Removing temporary files...
echo Removing files...

:: Remove the files one by one with error checking
if exist "camera_capture.jpg" (
    del /F /Q "camera_capture.jpg" 2>nul
    echo - Removed camera_capture.jpg
)

if exist "screenshot.png" (
    del /F /Q "screenshot.png" 2>nul
    echo - Removed screenshot.png
)

if exist "audio.wav" (
    del /F /Q "audio.wav" 2>nul
    echo - Removed audio.wav
)

if exist "system_info.txt" (
    del /F /Q "system_info.txt" 2>nul
    echo - Removed system_info.txt
)

if exist "keylogger.log" (
    del /F /Q "keylogger.log" 2>nul
    echo - Removed keylogger.log
)

if exist "temp_launcher.vbs" (
    del /F /Q "temp_launcher.vbs" 2>nul
    echo - Removed temp_launcher.vbs
)

echo.
echo ============================================================
echo Process complete! 
echo.
echo If nothing was found, the keylogger is likely already stopped.
echo For complete peace of mind, consider restarting your computer.
echo ============================================================
echo.
echo Press any key to exit...
pause > nul 