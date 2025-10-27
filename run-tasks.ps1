# Register tasks first (download-task.ps1, update-task.ps1)

# Run download task once
Start-ScheduledTask -TaskName "SpotlightNow-Download"

# Wait until it finishes
do {
    Start-Sleep -Seconds 2
    $state = (Get-ScheduledTask -TaskName "SpotlightNow-Download").State
} while ($state -eq 'Running')

# Now run update task once
Start-ScheduledTask -TaskName "SpotlightNow-UpdateLockscreen"