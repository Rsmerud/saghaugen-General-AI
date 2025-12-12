# Setup autostart for General AI services using Task Scheduler
# Kan kjøres uten admin-rettigheter for user-level tasks

$username = $env:USERNAME

# === FILSERVER TASK ===
$fileserverTaskName = "SaghaugenFileserver"
$fileserverAction = New-ScheduledTaskAction -Execute "C:\Python314\python.exe" -Argument "C:\ClaudeCodeProjects\GeneralAI\services\fileserver\fileserver.py" -WorkingDirectory "C:\ClaudeCodeProjects\GeneralAI\services\fileserver"
$fileserverTrigger = New-ScheduledTaskTrigger -AtLogOn -User $username
$fileserverSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

# Fjern gammel task hvis den finnes
Unregister-ScheduledTask -TaskName $fileserverTaskName -Confirm:$false -ErrorAction SilentlyContinue

# Opprett ny task
Register-ScheduledTask -TaskName $fileserverTaskName -Action $fileserverAction -Trigger $fileserverTrigger -Settings $fileserverSettings -Description "Saghaugen Filserver - Toveis filutveksling"
Write-Host "Fileserver task opprettet: $fileserverTaskName"

# Start filserveren nå
Start-ScheduledTask -TaskName $fileserverTaskName
Write-Host "Fileserver startet"

# === CLAUDE CODE TASK ===
$claudeTaskName = "ClaudeCodeGeneralAI"
$claudeAction = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c start `"Claude Code`" claude" -WorkingDirectory "C:\ClaudeCodeProjects\GeneralAI"
$claudeTrigger = New-ScheduledTaskTrigger -AtLogOn -User $username
$claudeSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Fjern gammel task hvis den finnes
Unregister-ScheduledTask -TaskName $claudeTaskName -Confirm:$false -ErrorAction SilentlyContinue

# Opprett ny task
Register-ScheduledTask -TaskName $claudeTaskName -Action $claudeAction -Trigger $claudeTrigger -Settings $claudeSettings -Description "Claude Code General AI - CTO for Saghaugen"
Write-Host "Claude Code task opprettet: $claudeTaskName"

Write-Host ""
Write-Host "=== AUTOSTART KONFIGURERT ==="
Write-Host "Begge tjenester vil starte automatisk ved innlogging."
Write-Host ""
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Saghaugen*" -or $_.TaskName -like "*Claude*"} | Format-Table TaskName, State
