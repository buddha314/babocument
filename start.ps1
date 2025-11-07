# Babocument Quick Start Script
# Simple launcher for local development

param(
    [int]$Port = 8000,
    [switch]$Help
)

if ($Help) {
    Write-Host "Babocument Server Launcher" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\start.ps1 [-Port 8000] [-Help]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Port      Server port (default: 8000)"
    Write-Host "  -Help      Show this help message"
    exit 0
}

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "  Starting Babocument Backend Server" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "app/main.py")) {
    Write-Host "ERROR: Must run from babocument project root" -ForegroundColor Red
    Write-Host "Current directory: $PWD" -ForegroundColor Yellow
    exit 1
}

# Check virtual environment
if (-not (Test-Path "venv/Scripts/python.exe")) {
    Write-Host "ERROR: Virtual environment not found" -ForegroundColor Red
    Write-Host "Please create it with: python -m venv venv" -ForegroundColor Yellow
    Write-Host "Then install dependencies: .\venv\Scripts\pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting server on port $Port..." -ForegroundColor Green
Write-Host "Access at: http://localhost:$Port" -ForegroundColor Cyan
Write-Host "API Docs:  http://localhost:$Port/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Activate venv and start server
& ".\venv\Scripts\Activate.ps1"
python -m uvicorn app.main:app --host 0.0.0.0 --port $Port --reload
