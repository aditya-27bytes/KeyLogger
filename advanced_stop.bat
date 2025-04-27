@echo off
echo Attempting to forcefully stop all keylogger processes...

:: Run as administrator (UAC prompt)
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:: Kill processes by name
echo Terminating all possible keylogger processes...
taskkill /F /IM pythonw.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM wscript.exe /T 2>nul
taskkill /F /IM cscript.exe /T 2>nul

:: Find and kill any Python processes running keylogger.py specifically
echo Checking for any specific keylogger processes...
for /f "tokens=1" %%i in ('wmic process where "commandline like '%%keylogger.py%%'" get processid 2^>nul ^| findstr /r "[0-9]"') do (
    echo Found keylogger process with PID: %%i
    taskkill /F /PID %%i 2>nul
)

:: Cleanup all possible temp files in the current directory
echo Removing all temporary files...
if exist "*.jpg" del /F /Q *.jpg
if exist "*.png" del /F /Q *.png
if exist "*.wav" del /F /Q *.wav
if exist "*.txt" del /F /Q *.txt
if exist "*.log" del /F /Q *.log
if exist "*.vbs" del /F /Q *.vbs
if exist "temp_*.*" del /F /Q temp_*.*

:: Kill the Python interpreter to be sure
echo Checking running Python processes...
wmic process where name="pythonw.exe" delete
wmic process where name="python.exe" delete

echo.
echo All possible keylogger processes have been terminated.
echo If you still believe the keylogger is running, please restart your computer.
echo.
echo Press any key to exit...
pause > nul 