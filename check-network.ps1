# Network Check Script
# Verifies network accessibility for Babocument development

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Babocument - Network Accessibility Check" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

# Get network information
$networkAdapters = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*" 
} | Select-Object IPAddress, InterfaceAlias

Write-Host "Network Interfaces:" -ForegroundColor Yellow
foreach ($adapter in $networkAdapters) {
    Write-Host "  $($adapter.InterfaceAlias): $($adapter.IPAddress)" -ForegroundColor White
}

# Get primary IP
$localIP = ($networkAdapters | Select-Object -First 1).IPAddress

if (-not $localIP) {
    Write-Host ""
    Write-Host "❌ No network connection detected" -ForegroundColor Red
    Write-Host "   Please connect to WiFi or Ethernet" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Primary IP: $localIP" -ForegroundColor Green
Write-Host ""

# Check if services are running
Write-Host "Checking Services..." -ForegroundColor Yellow
Write-Host ""

# Check Server (Port 8000)
Write-Host "Backend Server (Port 8000):" -ForegroundColor Cyan
try {
    $serverTest = Test-NetConnection -ComputerName localhost -Port 8000 -WarningAction SilentlyContinue -InformationLevel Quiet
    if ($serverTest) {
        Write-Host "  ✓ Running and accessible" -ForegroundColor Green
        Write-Host "    Local:   http://localhost:8000" -ForegroundColor Gray
        Write-Host "    Network: http://${localIP}:8000" -ForegroundColor Gray
    } else {
        Write-Host "  ✗ Not running" -ForegroundColor Red
        Write-Host "    Start with: .\start-dev.ps1 or .\run-server.ps1" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ Not running" -ForegroundColor Red
}

Write-Host ""

# Check Client (Port 3000)
Write-Host "Frontend Client (Port 3000):" -ForegroundColor Cyan
try {
    $clientTest = Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue -InformationLevel Quiet
    if ($clientTest) {
        Write-Host "  ✓ Running and accessible" -ForegroundColor Green
        Write-Host "    Local:   http://localhost:3000" -ForegroundColor Gray
        Write-Host "    Network: http://${localIP}:3000" -ForegroundColor Gray
    } else {
        Write-Host "  ✗ Not running" -ForegroundColor Red
        Write-Host "    Start with: .\start-dev.ps1" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ Not running" -ForegroundColor Red
}

Write-Host ""

# Check Firewall Rules
Write-Host "Checking Firewall Rules..." -ForegroundColor Yellow
Write-Host ""

$firewallRules = Get-NetFirewallRule | Where-Object { 
    $_.DisplayName -like "*Babocument*" -or 
    $_.DisplayName -like "*8000*" -or 
    $_.DisplayName -like "*3000*"
}

if ($firewallRules) {
    Write-Host "Firewall Rules:" -ForegroundColor Green
    foreach ($rule in $firewallRules) {
        $status = if ($rule.Enabled) { "✓" } else { "✗" }
        Write-Host "  $status $($rule.DisplayName)" -ForegroundColor $(if ($rule.Enabled) { "Green" } else { "Yellow" })
    }
} else {
    Write-Host "⚠ No firewall rules found for Babocument" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To allow network access, run (as Administrator):" -ForegroundColor White
    Write-Host ""
    Write-Host "New-NetFirewallRule -DisplayName 'Babocument Dev' -Direction Inbound -LocalPort 8000,3000 -Protocol TCP -Action Allow" -ForegroundColor Gray
    Write-Host ""
}

Write-Host ""

# Check Dependencies
Write-Host "Checking Dependencies..." -ForegroundColor Yellow
Write-Host ""

# Redis
try {
    $redisProcess = Get-Process redis-server -ErrorAction SilentlyContinue
    if ($redisProcess) {
        Write-Host "  ✓ Redis running" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Redis not running (optional for basic features)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Redis not running" -ForegroundColor Yellow
}

# Ollama
try {
    $ollamaTest = Test-NetConnection -ComputerName localhost -Port 11434 -WarningAction SilentlyContinue -InformationLevel Quiet
    if ($ollamaTest) {
        Write-Host "  ✓ Ollama running" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Ollama not running (optional for LLM features)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Ollama not running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

if ($serverTest -and $clientTest) {
    Write-Host "✓ Both services running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access from this computer:" -ForegroundColor White
    Write-Host "  http://localhost:3000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Access from other devices:" -ForegroundColor White
    Write-Host "  http://${localIP}:3000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "VR Headset:" -ForegroundColor White
    Write-Host "  1. Connect to same WiFi network" -ForegroundColor Gray
    Write-Host "  2. Open browser on headset" -ForegroundColor Gray
    Write-Host "  3. Navigate to: http://${localIP}:3000" -ForegroundColor Cyan
} else {
    Write-Host "⚠ Services not running" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Start both services:" -ForegroundColor White
    Write-Host "  .\start-dev.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or start individually:" -ForegroundColor White
    Write-Host "  Server: .\run-server.ps1" -ForegroundColor Gray
    Write-Host "  Client: cd client; npm run dev -- --hostname 0.0.0.0" -ForegroundColor Gray
}

Write-Host ""
Write-Host "For detailed network setup guide, see:" -ForegroundColor Gray
Write-Host "  NETWORK_ACCESS.md" -ForegroundColor Cyan
Write-Host ""
