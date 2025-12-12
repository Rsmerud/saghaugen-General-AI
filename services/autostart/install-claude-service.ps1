# Install Claude Code as Windows Service
# Kjør som Administrator!

$serviceName = "ClaudeCodeGeneralAI"
$serviceDisplayName = "Claude Code General AI"
$serviceDescription = "General AI - CTO for Saghaugen"
$nodePath = "C:\Program Files\nodejs\node.exe"
$claudePath = "C:\Users\admin\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\cli.js"
$workingDir = "C:\ClaudeCodeProjects\GeneralAI"

# Sjekk om NSSM finnes
$nssmPath = "C:\Tools\nssm.exe"
if (-not (Test-Path $nssmPath)) {
    Write-Host "NSSM ikke funnet. Kjør fileserver install-service.ps1 først for å laste ned NSSM."
    exit 1
}

# Stopp og fjern eksisterende tjeneste hvis den finnes
& $nssmPath stop $serviceName 2>$null
& $nssmPath remove $serviceName confirm 2>$null

# Installer tjenesten
Write-Host "Installerer $serviceDisplayName..."
& $nssmPath install $serviceName $nodePath $claudePath
& $nssmPath set $serviceName DisplayName $serviceDisplayName
& $nssmPath set $serviceName Description $serviceDescription
& $nssmPath set $serviceName Start SERVICE_AUTO_START
& $nssmPath set $serviceName AppDirectory $workingDir
& $nssmPath set $serviceName AppStdout "C:\ClaudeCodeProjects\GeneralAI\services\autostart\claude.log"
& $nssmPath set $serviceName AppStderr "C:\ClaudeCodeProjects\GeneralAI\services\autostart\claude-error.log"

# Start tjenesten
Write-Host "Starter tjenesten..."
& $nssmPath start $serviceName

Write-Host ""
Write-Host "Ferdig! Tjenesten '$serviceDisplayName' er installert."
Write-Host "Status: $(Get-Service $serviceName -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Status)"
Write-Host ""
Write-Host "MERK: Claude Code som service fungerer best for bakgrunnsoppgaver."
Write-Host "For interaktiv bruk, start Claude Code manuelt i terminalen."
