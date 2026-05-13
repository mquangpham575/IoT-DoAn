param (
    [Parameter(Position=0)]
    [ValidateSet("deploy", "stop", "status", "logs")]
    [string]$Action = "deploy"
)

# =============================================================================
# deploy_iot.ps1 - Manage IoT Health Backend on Azure VM
# =============================================================================

$RemotePath = "/opt/iot_backend"
$SSH_KEY = "C:\Project\uma_tracker\UmaCore\.ssh\umacore_key"
$IP = "20.212.105.13"
$User = "umacore"

switch ($Action) {
    "deploy" {
        Write-Host "📦 Packaging and Syncing Integrated IoT Stack to $IP..." -ForegroundColor Magenta
        # Create a temporary tarball, excluding large/unnecessary folders
        tar --exclude=./.git --exclude=./__pycache__ --exclude=./firmware --exclude=./mobile --exclude=./docs --exclude=./deploy_iot.ps1 --exclude=./iot_project.tar.gz -czf iot_project.tar.gz .

        # Create remote directory and upload
        ssh -i $SSH_KEY "$User@$IP" "sudo mkdir -p $RemotePath && sudo chown ${User}:${User} $RemotePath"
        scp -i $SSH_KEY iot_project.tar.gz "$User@$($IP):$RemotePath/"

        # Extract and start
        ssh -i $SSH_KEY "$User@$IP" "cd $RemotePath && tar -xzf iot_project.tar.gz && rm iot_project.tar.gz && docker compose up -d --build"

        Remove-Item iot_project.tar.gz
        Write-Host "✨ Deployment complete! IoT service is running." -ForegroundColor Green
    }
    
    "stop" {
        Write-Host "🛑 Stopping IoT service on $IP..." -ForegroundColor Yellow
        ssh -i $SSH_KEY "$User@$IP" "cd $RemotePath && docker compose down"
        Write-Host "✅ Service stopped." -ForegroundColor Green
    }

    "status" {
        Write-Host "🔍 Checking container status on $IP..." -ForegroundColor Cyan
        ssh -i $SSH_KEY "$User@$IP" "docker ps -f name=iot-"
    }

    "logs" {
        Write-Host "📜 Streaming live logs from $IP... (Ctrl+C to stop)" -ForegroundColor Cyan
        ssh -i $SSH_KEY "$User@$IP" "cd $RemotePath && docker compose logs -f --tail=50"
    }
}
