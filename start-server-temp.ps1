Set-Location 'C:\Users\b\src\babocument\server'
$Host.UI.RawUI.WindowTitle = 'Babocument - Backend Server'
Write-Host '=== Babocument Backend Server ===' -ForegroundColor Cyan
Write-Host ''

# Activate virtual environment
if (Test-Path 'venv\Scripts\Activate.ps1') {
    & 'venv\Scripts\Activate.ps1'
    Write-Host 'Virtual environment activated' -ForegroundColor Green
} else {
    Write-Host 'ERROR: Virtual environment not found!' -ForegroundColor Red
    Write-Host 'Run: cd server; python -m venv venv; venv\Scripts\pip install -r requirements.txt' -ForegroundColor Yellow
    Read-Host 'Press Enter to exit'
    exit 1
}

Write-Host ''
Write-Host 'Server accessible at:' -ForegroundColor Green
Write-Host '  Local:   http://localhost:8000' -ForegroundColor White
Write-Host '  Network: http://192.168.1.200:8000' -ForegroundColor White
Write-Host '  Docs:    http://localhost:8000/docs' -ForegroundColor Gray
Write-Host ''

# Start uvicorn server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
