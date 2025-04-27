@echo off
echo Checking if keylogger is actually running...
echo.

echo --- Process Check ---
echo Running processes:
tasklist | findstr "python"
echo.

echo --- Checking for Python ---
where python
where pythonw
echo.

echo --- Checking Startup Location ---
echo Looking in startup folder...
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" /b
echo.

echo --- Log File Check ---
if exist keylogger.log (
    echo Keylogger log exists! Last few lines:
    type keylogger.log
) else (
    echo No keylogger log found.
)

echo.
echo Scan complete. If no python processes are shown above and no keylogger log exists,
echo the keylogger might already be stopped or is not running.
echo.
echo Press any key to exit...
pause > nul 