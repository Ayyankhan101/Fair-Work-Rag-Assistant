#Requires -Version 5.1
# DEF-015: PowerShell equivalent for service verification
# Usage: .\scripts\verify.ps1 [-TimeoutSeconds 60] [-CheckInterval 5]

param(
    [int]$TimeoutSeconds = 60,
    [int]$CheckInterval = 5
)

$ErrorActionPreference = "Stop"
$Elapsed = 0

Write-Host "Waiting for service to be ready (timeout: ${TimeoutSeconds}s)..."

while ($Elapsed -lt $TimeoutSeconds) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:7860" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "Service is ready after ${Elapsed}s"
            exit 0
        }
    } catch {
        # Service not ready yet
    }
    
    Start-Sleep -Seconds $CheckInterval
    $Elapsed += $CheckInterval
    Write-Host "  Still waiting... (${Elapsed}/${TimeoutSeconds}s)"
}

Write-Host "ERROR: Service did not become ready within ${TimeoutSeconds}s"
exit 1
