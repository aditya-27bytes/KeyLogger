@echo off
echo Stopping keylogger processes...

:: Kill all pythonw processes (This will terminate the keylogger)
taskkill /F /IM pythonw.exe 2>nul
if %errorlevel% equ 0 (
  echo Keylogger stopped successfully.
) else (
  echo No keylogger process found or failed to stop.
)

:: Delete temporary files
echo Cleaning up temporary files...
if exist camera_capture.jpg del /F /Q camera_capture.jpg
if exist screenshot.png del /F /Q screenshot.png
if exist audio.wav del /F /Q audio.wav
if exist system_info.txt del /F /Q system_info.txt
if exist keylogger.log del /F /Q keylogger.log
if exist keylogger_launcher.log del /F /Q keylogger_launcher.log
if exist app_log.txt del /F /Q app_log.txt
if exist app_error.txt del /F /Q app_error.txt
if exist temp_launcher.vbs del /F /Q temp_launcher.vbs

echo Cleanup completed.
echo.
echo Press any key to exit...
pause > nul 