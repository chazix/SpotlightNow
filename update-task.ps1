# Action: run spotlight-now.exe update-lockscreen
$Action = New-ScheduledTaskAction -Execute "C:\ProgramData\SpotlightNow\spotlight-now.exe" -Argument "update-lockscreen" -WorkingDirectory "C:\ProgramData\SpotlightNow"

# Trigger: run at system startup
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Run as SYSTEM with highest privileges
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

# Register the task
Register-ScheduledTask -TaskName "SpotlightNow-UpdateLockscreen" -Action $Action -Trigger $Trigger -Principal $Principal -Description "Update lock screen image at startup"