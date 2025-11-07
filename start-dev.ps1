# Babocument Development Launcher
# Starts server for network-accessible development
# Usage: .\start-dev.ps1 [-ServerPort 8000]

param(
    [int]$ServerPort = 8000
)

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Babocument - Development Environment Launcher" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from project root
if (-not (Test-Path "app/main.py")) {
    Write-Host "Error: Must run from project root directory" -ForegroundColor Red
    exit 1
}

# Get local IP address for network access
$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*","Wi-Fi*" | Where-Object { $_.IPAddress -notlike "169.254.*" -and $_.IPAddress -notlike "127.*" } | Select-Object -First 1).IPAddress
if (-not $localIP) {
    Write-Host "Warning: Could not detect network IP, using localhost" -ForegroundColor Yellow
    $localIP = "localhost"
}

Write-Host "Network Configuration:" -ForegroundColor Green
Write-Host "  Local IP: $localIP" -ForegroundColor Cyan
Write-Host "  Server Port: $ServerPort" -ForegroundColor Cyan
Write-Host ""

# Check Redis
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    $redisCheck = Get-Process redis-server -ErrorAction SilentlyContinue
    if ($redisCheck) {
        Write-Host "[OK] Redis is running" -ForegroundColor Green
    }
    else {
        Write-Host "[WARN] Redis not detected. Event bus may not work." -ForegroundColor Yellow
        Write-Host "       Start Redis with: redis-server" -ForegroundColor Gray
    }
}
catch {
    Write-Host "[WARN] Could not check Redis status" -ForegroundColor Yellow
}

# Check Ollama
try {
    $ollamaCheck = Test-NetConnection -ComputerName localhost -Port 11434 -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    if ($ollamaCheck.TcpTestSucceeded) {
        Write-Host "[OK] Ollama is running" -ForegroundColor Green
    }
    else {
        Write-Host "[WARN] Ollama not detected. LLM features may not work." -ForegroundColor Yellow
        Write-Host "       Start Ollama with: ollama serve" -ForegroundColor Gray
    }
}
catch {
    Write-Host "[WARN] Could not check Ollama status" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Access URLs (from any device on your network):" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:" -ForegroundColor Yellow
Write-Host "  http://localhost:$ServerPort                   (this computer)" -ForegroundColor White
Write-Host "  http://${localIP}:$ServerPort               (network)" -ForegroundColor White
Write-Host "  http://localhost:$ServerPort/docs              (API docs)" -ForegroundColor Gray
Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting server..." -ForegroundColor Green
Write-Host ""

# Function to start server in new window
function Start-Server {
    Write-Host "Starting Backend Server..." -ForegroundColor Cyan
    
    # Create server startup script file
    $serverScriptPath = Join-Path $PWD "start-server-temp.ps1"
    $serverContent = @"
Set-Location '$PWD'
`$Host.UI.RawUI.WindowTitle = 'Babocument - Backend Server'
Write-Host '=== Babocument Backend Server ===' -ForegroundColor Cyan
Write-Host ''

# Activate virtual environment
if (Test-Path 'venv\Scripts\Activate.ps1') {
    & 'venv\Scripts\Activate.ps1'
    Write-Host 'Virtual environment activated' -ForegroundColor Green
} else {
    Write-Host 'ERROR: Virtual environment not found!' -ForegroundColor Red
    Write-Host 'Run: python -m venv venv; venv\Scripts\pip install -r requirements.txt' -ForegroundColor Yellow
    Read-Host 'Press Enter to exit'
    exit 1
}

Write-Host ''
Write-Host 'Server accessible at:' -ForegroundColor Green
Write-Host '  Local:   http://localhost:$ServerPort' -ForegroundColor White
Write-Host '  Network: http://$localIP`:$ServerPort' -ForegroundColor White
Write-Host '  Docs:    http://localhost:$ServerPort/docs' -ForegroundColor Gray
Write-Host ''

# Start uvicorn server
python -m uvicorn app.main:app --host 0.0.0.0 --port $ServerPort --reload
"@
    Set-Content -Path $serverScriptPath -Value $serverContent
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", $serverScriptPath
}

# Start server
Start-Server

Write-Host ""
Write-Host "[OK] Server starting in separate window" -ForegroundColor Green
Write-Host ""
Write-Host "Quick Start:" -ForegroundColor Yellow
Write-Host "  1. Wait ~5 seconds for server to start" -ForegroundColor White
Write-Host "  2. Open http://localhost:$ServerPort/docs in your browser" -ForegroundColor White
Write-Host "  3. Test API endpoints from the interactive documentation" -ForegroundColor White
Write-Host ""
Write-Host "Network Access:" -ForegroundColor Yellow
Write-Host "  - Other computers: http://${localIP}:$ServerPort" -ForegroundColor White
Write-Host "  - Firewall: Allow port $ServerPort" -ForegroundColor Gray
Write-Host ""
Write-Host "Troubleshooting:" -ForegroundColor Yellow
Write-Host "  - Check firewall settings if network access fails" -ForegroundColor White
Write-Host "  - Ensure Redis and Ollama are running for full features" -ForegroundColor White
Write-Host "  - Close service window to stop server" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Cleanup temporary script file
$serverScriptPath = Join-Path $PWD "start-server-temp.ps1"
if (Test-Path $serverScriptPath) {
    Remove-Item $serverScriptPath -Force -ErrorAction SilentlyContinue
}
