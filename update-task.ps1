$Action = New-ScheduledTaskAction -Execute "C:\ProgramData\SpotlightNow\spotlight-now.exe" -Argument "update-lockscreen" -WorkingDirectory "C:\ProgramData\SpotlightNow"
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest
Register-ScheduledTask -TaskName "SpotlightNow-UpdateLockscreen" -Action $Action -Trigger $Trigger -Principal $Principal -Description "Update lock screen image at startup"