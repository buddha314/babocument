# Babocument Server Launcher
# Usage: .\run-server.ps1 [-Port 8000]

param([int]$Port = 8000)

Write-Host "Starting Babocument Server..." -ForegroundColor Cyan
if (-not (Test-Path "app/main.py")) {
    Write-Host "Error: Run from project root" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found" -ForegroundColor Red
    exit 1
}

& "venv\Scripts\Activate.ps1"

# Get local IP address
$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*","Wi-Fi*" | Where-Object { $_.IPAddress -notlike "169.254.*" } | Select-Object -First 1).IPAddress
if (-not $localIP) {
    $localIP = "localhost"
}

Write-Host "`nServer will be accessible at:" -ForegroundColor Green
Write-Host "  Local:   http://localhost:$Port" -ForegroundColor Cyan
Write-Host "  Network: http://${localIP}:$Port" -ForegroundColor Cyan
Write-Host "  Docs:    http://localhost:$Port/docs" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --host 0.0.0.0 --port $Port --reload
