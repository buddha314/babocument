Set-Location 'C:\Users\b\src\babocument\client'
$Host.UI.RawUI.WindowTitle = 'Babocument - Frontend Client'
Write-Host '=== Babocument Frontend Client ===' -ForegroundColor Cyan
Write-Host ''

# Check if node_modules exists
if (-not (Test-Path 'node_modules')) {
    Write-Host 'Installing dependencies...' -ForegroundColor Yellow
    npm install
}

Write-Host 'Client accessible at:' -ForegroundColor Green
Write-Host '  Local:   http://localhost:3000' -ForegroundColor White
Write-Host '  Network: http://192.168.1.200:3000' -ForegroundColor White
Write-Host ''
Write-Host 'For VR: Open http://192.168.1.200:3000 in Meta Quest browser' -ForegroundColor Yellow
Write-Host ''

# Start Next.js dev server
npm run dev -- --port 3000 --hostname 0.0.0.0
