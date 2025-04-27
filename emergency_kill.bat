@echo off
color 4F
title !!! EMERGENCY PROCESS KILLER !!!
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo !!           EMERGENCY KILL SWITCH            !!
echo !!  THIS WILL FORCEFULLY TERMINATE PROCESSES  !!
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo.
echo WARNING: This will kill ALL Python and script processes
echo This might affect other legitimate programs
echo.
pause

echo.
echo Killing ALL Python and script host processes...
echo.

:: Kill with extreme prejudice
taskkill /F /IM pythonw.exe /T
taskkill /F /IM python.exe /T
taskkill /F /IM wscript.exe /T
taskkill /F /IM cscript.exe /T

:: Use more direct methods too
wmic process where name="pythonw.exe" delete
wmic process where name="python.exe" delete
wmic process where name="wscript.exe" delete
wmic process where name="cscript.exe" delete

:: Specifically target any running Python processes
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq pythonw.exe" /nh') do (
    echo Killing pythonw.exe PID: %%a
    taskkill /F /PID %%a
)

echo.
echo Cleaning up temporary files...
del /F /Q *.jpg
del /F /Q *.png
del /F /Q *.wav
del /F /Q *.txt
del /F /Q *.log
del /F /Q *.vbs

echo.
echo EMERGENCY SHUTDOWN COMPLETE!
echo If you still see suspicious activity, please restart your computer.
echo.
echo Press any key to exit...
pause > nul 