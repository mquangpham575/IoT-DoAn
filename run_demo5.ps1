# run_demo5.ps1
# INTENT: Automate sending 5 critical sensor readings with a 6-second delay to verify Discord alert spam prevention.

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Starting Demo 5: Discord Cooldown Alert Verification" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

for ($i = 1; $i -le 5; $i++) {
    Write-Host "[Reading $i/5] Sending CRITICAL data..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "http://20.212.105.13:8000/api/v1/sensor/readings" `
            -Method Post `
            -Headers @{ "X-API-KEY" = "IOT_SECRET_2026" } `
            -ContentType "application/json" `
            -Body '{"device_id":"esp32_01","temperature":25,"humidity":60,"gas":3500,"light":300,"noise":200}'
        
        $statusLabel = $response.data.status_label
        $comfortLevel = $response.data.comfort_level
        Write-Host " -> Server Response: status_label = $statusLabel, comfort_level = $comfortLevel" -ForegroundColor Green
    } catch {
        Write-Error " -> Failed to send request: $_"
    }

    if ($i -lt 5) {
        Write-Host " -> Sleeping 6 seconds..."
        Start-Sleep -Seconds 6
    }
}

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Demo 5 Execution Finished. Check Discord channel and SQLite DB." -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
