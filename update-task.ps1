# Action: run spotlight-now.exe update-lockscreen
$Action = New-ScheduledTaskAction `
    -Execute "C:\ProgramData\SpotlightNow\spotlight-now.exe" `
    -Argument "update-lockscreen" `
    -WorkingDirectory "C:\ProgramData\SpotlightNow"

# Trigger 1: run at user logon
$Trigger1 = New-ScheduledTaskTrigger -AtLogon

# Trigger 2: start 8 hours from now, then repeat every 8 hours indefinitely
$StartTime = (Get-Date).AddHours(8)

$Trigger2 = New-ScheduledTaskTrigger -Once -At $StartTime `
    -RepetitionInterval (New-TimeSpan -Hours 8)

# Principal: run as current user with highest privileges
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

# Register the task with both triggers
Register-ScheduledTask `
    -TaskName "SpotlightNow-UpdateLockscreen" `
    -Action $Action `
    -Trigger @($Trigger1, $Trigger2) `
    -Principal $Principal `
    -Description "Update lock screen image at logon and every 8 hours"