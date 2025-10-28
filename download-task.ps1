# Action: run spotlight-now.exe download
$Action = New-ScheduledTaskAction -Execute "C:\ProgramData\SpotlightNow\spotlight-now.exe" -Argument "download" -WorkingDirectory "C:\ProgramData\SpotlightNow"

# Trigger: start once today, repeat every 1 hours indefinitely
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date `
    -RepetitionInterval (New-TimeSpan -Hours 1)

# Run as SYSTEM with highest privileges
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest

# Register the task
Register-ScheduledTask -TaskName "SpotlightNow-Download" -Action $Action -Trigger $Trigger -Principal $Principal -Description "Periodically download new Spotlight images"