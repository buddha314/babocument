# Babocument Server Setup Script
# This script automates the initial setup of the Babocument server

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Babocument Server Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check if we're in the server directory
if (-not (Test-Path "app/main.py")) {
    Write-Host "✗ Please run this script from the server directory" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create data directories
Write-Host ""
Write-Host "Creating data directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data/chroma" | Out-Null
Write-Host "✓ Data directories created" -ForegroundColor Green

# Create models directory if it doesn't exist
Write-Host ""
Write-Host "Checking model storage directory..." -ForegroundColor Yellow
if (-not (Test-Path "d:\models")) {
    Write-Host "Creating d:\models directory..." -ForegroundColor Yellow
    try {
        New-Item -ItemType Directory -Force -Path "d:\models" | Out-Null
        Write-Host "✓ Model storage directory created at d:\models" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Could not create d:\models. You may need to create it manually or update .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ Model storage directory exists at d:\models" -ForegroundColor Green
}

# Check if .env exists
Write-Host ""
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
} else {
    Write-Host "✗ .env file not found - using .env.example as template" -ForegroundColor Yellow
}

# Check Ollama installation
Write-Host ""
Write-Host "Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "✓ Ollama is installed" -ForegroundColor Green
    
    # Check if Ollama is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 2 2>&1
        Write-Host "✓ Ollama is running" -ForegroundColor Green
        
        # Check for models
        Write-Host ""
        Write-Host "Checking downloaded models..." -ForegroundColor Yellow
        ollama list
        
    } catch {
        Write-Host "⚠ Ollama is not running. Start it with: ollama serve" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ Ollama not found. Install from: https://ollama.com/download" -ForegroundColor Red
    Write-Host "  Or use: winget install Ollama.Ollama" -ForegroundColor Yellow
}

# Check Redis installation
Write-Host ""
Write-Host "Checking Redis..." -ForegroundColor Yellow
try {
    $dockerPs = docker ps --filter "name=babocument-redis" --format "{{.Names}}" 2>&1
    if ($dockerPs -match "babocument-redis") {
        Write-Host "✓ Redis container is running" -ForegroundColor Green
    } else {
        Write-Host "⚠ Redis container not found" -ForegroundColor Yellow
        Write-Host "  Start with: docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Docker not found or not running" -ForegroundColor Yellow
    Write-Host "  Install Docker Desktop or use Windows Redis port" -ForegroundColor Yellow
}

# Setup complete
Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure Ollama is running: " -NoNewline; Write-Host "ollama serve" -ForegroundColor White
Write-Host "2. Download models: " -NoNewline; Write-Host "ollama pull llama3.2:3b" -ForegroundColor White
Write-Host "3. Start Redis: " -NoNewline; Write-Host "docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine" -ForegroundColor White
Write-Host "4. Run the server: " -NoNewline; Write-Host "python app/main.py" -ForegroundColor White
Write-Host "5. View API docs: " -NoNewline; Write-Host "http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see SETUP.md" -ForegroundColor Cyan
Write-Host ""
