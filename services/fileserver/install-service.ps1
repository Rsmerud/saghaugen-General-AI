# Install Saghaugen Fileserver as Windows Service
# Kjør som Administrator!

$serviceName = "SaghaugenFileserver"
$serviceDisplayName = "Saghaugen Filserver"
$serviceDescription = "Toveis filutveksling mellom General AI og Ronny"
$pythonPath = "C:\Python314\python.exe"
$scriptPath = "C:\ClaudeCodeProjects\GeneralAI\services\fileserver\fileserver.py"

# Sjekk om NSSM finnes, hvis ikke last ned
$nssmPath = "C:\Tools\nssm.exe"
if (-not (Test-Path $nssmPath)) {
    Write-Host "Laster ned NSSM (Non-Sucking Service Manager)..."
    New-Item -ItemType Directory -Path "C:\Tools" -Force | Out-Null

    $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
    $zipPath = "C:\Tools\nssm.zip"

    Invoke-WebRequest -Uri $nssmUrl -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath "C:\Tools\nssm-temp" -Force
    Copy-Item "C:\Tools\nssm-temp\nssm-2.24\win64\nssm.exe" $nssmPath
    Remove-Item $zipPath -Force
    Remove-Item "C:\Tools\nssm-temp" -Recurse -Force
    Write-Host "NSSM installert til $nssmPath"
}

# Stopp og fjern eksisterende tjeneste hvis den finnes
& $nssmPath stop $serviceName 2>$null
& $nssmPath remove $serviceName confirm 2>$null

# Installer tjenesten
Write-Host "Installerer $serviceDisplayName..."
& $nssmPath install $serviceName $pythonPath $scriptPath
& $nssmPath set $serviceName DisplayName $serviceDisplayName
& $nssmPath set $serviceName Description $serviceDescription
& $nssmPath set $serviceName Start SERVICE_AUTO_START
& $nssmPath set $serviceName AppDirectory "C:\ClaudeCodeProjects\GeneralAI\services\fileserver"
& $nssmPath set $serviceName AppStdout "C:\ClaudeCodeProjects\GeneralAI\services\fileserver\fileserver.log"
& $nssmPath set $serviceName AppStderr "C:\ClaudeCodeProjects\GeneralAI\services\fileserver\fileserver-error.log"

# Start tjenesten
Write-Host "Starter tjenesten..."
& $nssmPath start $serviceName

Write-Host ""
Write-Host "Ferdig! Tjenesten '$serviceDisplayName' er installert og startet."
Write-Host "Status: $(Get-Service $serviceName | Select-Object -ExpandProperty Status)"
