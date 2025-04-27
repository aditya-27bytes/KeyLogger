# Run as administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))  
{  
    Write-Warning "Please run this script as Administrator!"
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "Advanced Keylogger Process Killer" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Kill all potential keylogger processes
$processes = @("pythonw", "python", "wscript", "cscript")
foreach ($proc in $processes) {
    Write-Host "Searching for $proc processes..." -ForegroundColor Yellow
    $foundProcs = Get-Process -Name $proc -ErrorAction SilentlyContinue
    
    if ($foundProcs) {
        Write-Host "Found $($foundProcs.Count) $proc processes. Terminating..." -ForegroundColor Red
        Stop-Process -Name $proc -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "No $proc processes found." -ForegroundColor Green
    }
}

# Search for processes with keylogger in the command line
Write-Host "`nSearching for processes related to keylogger..." -ForegroundColor Yellow
$keyloggerProcesses = Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -like "*keylogger*" }

if ($keyloggerProcesses) {
    Write-Host "Found $($keyloggerProcesses.Count) keylogger-related processes. Terminating..." -ForegroundColor Red
    foreach ($process in $keyloggerProcesses) {
        Write-Host "Killing PID: $($process.ProcessId) - $($process.CommandLine)" -ForegroundColor Red
        Stop-Process -Id $process.ProcessId -Force -ErrorAction SilentlyContinue
    }
} else {
    Write-Host "No keylogger-related processes found." -ForegroundColor Green
}

# Clean up temporary files
Write-Host "`nCleaning up temporary files..." -ForegroundColor Yellow
$filesToDelete = @(
    "*.jpg", "*.png", "*.wav", "*.txt", "*.log", "*.vbs", 
    "temp_*.*", "camera_capture.jpg", "screenshot.png", 
    "audio.wav", "system_info.txt", "keylogger.log", 
    "keylogger_launcher.log", "app_log.txt", "app_error.txt", 
    "temp_launcher.vbs"
)

foreach ($filePattern in $filesToDelete) {
    $files = Get-ChildItem -Path $filePattern -ErrorAction SilentlyContinue
    if ($files) {
        Write-Host "Removing $($files.Count) files matching $filePattern..." -ForegroundColor Yellow
        Remove-Item -Path $filePattern -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "`nCleanup completed!" -ForegroundColor Green
Write-Host "If you still believe the keylogger is running, please restart your computer." -ForegroundColor Cyan
Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 