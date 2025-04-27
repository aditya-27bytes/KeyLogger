@echo off
echo.
echo =============================================
echo =        KEYLOGGER COMPLETE STOP           =
echo =                                           =
echo = This will restart your computer to ensure =
echo = that all keylogger processes are stopped. =
echo =============================================
echo.
echo Press CTRL+C to cancel if you don't want to restart.
echo.
timeout /t 10
echo.
echo Restarting computer now...
shutdown /r /t 5 /c "Restarting to terminate keylogger processes" /f /d p:4:1 