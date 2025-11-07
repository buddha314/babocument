# Babocument Server Setup Script# Babocument Server Setup Script

# This script automates the initial setup of the Babocument server# This script automates the initial setup of the Babocument server



Write-Host "==================================" -ForegroundColor CyanWrite-Host "==================================" -ForegroundColor Cyan

Write-Host "Babocument Server Setup" -ForegroundColor CyanWrite-Host "Babocument Server Setup" -ForegroundColor Cyan

Write-Host "==================================" -ForegroundColor CyanWrite-Host "==================================" -ForegroundColor Cyan

Write-Host ""Write-Host ""



# Check Python installation# Check Python installation

Write-Host "Checking Python installation..." -ForegroundColor YellowWrite-Host "Checking Python installation..." -ForegroundColor Yellow

try {try {

    $pythonVersion = python --version 2>&1    $pythonVersion = python --version 2>&1

    Write-Host "Success $pythonVersion" -ForegroundColor Green    Write-Host "✓ $pythonVersion" -ForegroundColor Green

}}

catch {catch {

    Write-Host "X Python not found. Please install Python 3.11+ from https://python.org" -ForegroundColor Red    Write-Host "✗ Python not found. Please install Python 3.11+ from https://python.org" -ForegroundColor Red

    exit 1    exit 1

}}



# Check if we're in the server directory# Check if we're in the server directory

if (-not (Test-Path "app/main.py")) {if (-not (Test-Path "app/main.py")) {

    Write-Host "X Please run this script from the server directory" -ForegroundColor Red    Write-Host "✗ Please run this script from the server directory" -ForegroundColor Red

    exit 1    exit 1

}}



# Create virtual environment# Create virtual environment

Write-Host ""Write-Host ""

Write-Host "Creating virtual environment..." -ForegroundColor YellowWrite-Host "Creating virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {if (Test-Path "venv") {

    Write-Host "Success Virtual environment already exists" -ForegroundColor Green    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green

}}

else {else {

    python -m venv venv    python -m venv venv

    Write-Host "Success Virtual environment created" -ForegroundColor Green    Write-Host "✓ Virtual environment created" -ForegroundColor Green

}}



# Activate virtual environment# Activate virtual environment

Write-Host ""Write-Host ""

Write-Host "Activating virtual environment..." -ForegroundColor YellowWrite-Host "Activating virtual environment..." -ForegroundColor Yellow

& ".\venv\Scripts\Activate.ps1"& ".\venv\Scripts\Activate.ps1"



# Upgrade pip# Upgrade pip

Write-Host ""Write-Host ""

Write-Host "Upgrading pip..." -ForegroundColor YellowWrite-Host "Upgrading pip..." -ForegroundColor Yellow

python -m pip install --upgrade pip --quietpython -m pip install --upgrade pip --quiet



# Install dependencies# Install dependencies

Write-Host ""Write-Host ""

Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor YellowWrite-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow

pip install -r requirements.txt --quietpip install -r requirements.txt --quiet

Write-Host "Success Dependencies installed" -ForegroundColor GreenWrite-Host "✓ Dependencies installed" -ForegroundColor Green



# Create data directories# Create data directories

Write-Host ""Write-Host ""

Write-Host "Creating data directories..." -ForegroundColor YellowWrite-Host "Creating data directories..." -ForegroundColor Yellow

New-Item -ItemType Directory -Force -Path "data/chroma" | Out-NullNew-Item -ItemType Directory -Force -Path "data/chroma" | Out-Null

Write-Host "Success Data directories created" -ForegroundColor GreenWrite-Host "✓ Data directories created" -ForegroundColor Green



# Create models directory if it doesn't exist# Create models directory if it doesn't exist

Write-Host ""Write-Host ""

Write-Host "Checking model storage directory..." -ForegroundColor YellowWrite-Host "Checking model storage directory..." -ForegroundColor Yellow

if (-not (Test-Path "d:\models")) {if (-not (Test-Path "d:\models")) {

    Write-Host "Creating d:\models directory..." -ForegroundColor Yellow    Write-Host "Creating d:\models directory..." -ForegroundColor Yellow

    try {    try {

        New-Item -ItemType Directory -Force -Path "d:\models" | Out-Null        New-Item -ItemType Directory -Force -Path "d:\models" | Out-Null

        Write-Host "Success Model storage directory created at d:\models" -ForegroundColor Green        Write-Host "✓ Model storage directory created at d:\models" -ForegroundColor Green

    }    }

    catch {    catch {

        Write-Host "Warning Could not create d:\models. You may need to create it manually or update .env" -ForegroundColor Yellow        Write-Host "⚠ Could not create d:\models. You may need to create it manually or update .env" -ForegroundColor Yellow

    }    }

}}

else {else {

    Write-Host "Success Model storage directory exists at d:\models" -ForegroundColor Green    Write-Host "✓ Model storage directory exists at d:\models" -ForegroundColor Green

}}



# Check if .env exists# Check if .env exists

Write-Host ""Write-Host ""

Write-Host "Checking configuration..." -ForegroundColor YellowWrite-Host "Checking configuration..." -ForegroundColor Yellow

if (Test-Path ".env") {if (Test-Path ".env") {

    Write-Host "Success .env file already exists" -ForegroundColor Green    Write-Host "✓ .env file already exists" -ForegroundColor Green

}}

else {else {

    Write-Host "X .env file not found - using .env.example as template" -ForegroundColor Yellow    Write-Host "✗ .env file not found - using .env.example as template" -ForegroundColor Yellow

}}



# Check Ollama installation# Check Ollama installation

Write-Host ""Write-Host ""

Write-Host "Checking Ollama installation..." -ForegroundColor YellowWrite-Host "Checking Ollama installation..." -ForegroundColor Yellow

try {try {

    $ollamaVersion = ollama --version 2>&1    $ollamaVersion = ollama --version 2>&1

    Write-Host "Success Ollama is installed" -ForegroundColor Green    Write-Host "✓ Ollama is installed" -ForegroundColor Green

        

    # Check if Ollama is running    # Check if Ollama is running

    try {    try {

        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 2 2>&1        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -Method Get -TimeoutSec 2 2>&1

        Write-Host "Success Ollama is running" -ForegroundColor Green        Write-Host "✓ Ollama is running" -ForegroundColor Green

                

        # Check for models        # Check for models

        Write-Host ""        Write-Host ""

        Write-Host "Checking downloaded models..." -ForegroundColor Yellow        Write-Host "Checking downloaded models..." -ForegroundColor Yellow

        ollama list        ollama list

    }        

    catch {    }

        Write-Host "Warning Ollama is not running. Start it with: ollama serve" -ForegroundColor Yellow    catch {

    }        Write-Host "⚠ Ollama is not running. Start it with: ollama serve" -ForegroundColor Yellow

}    }

catch {}

    Write-Host "X Ollama not found. Install from: https://ollama.com/download" -ForegroundColor Redcatch {

    Write-Host "  Or use: winget install Ollama.Ollama" -ForegroundColor Yellow    Write-Host "✗ Ollama not found. Install from: https://ollama.com/download" -ForegroundColor Red

}    Write-Host "  Or use: winget install Ollama.Ollama" -ForegroundColor Yellow

}

# Check Redis installation

Write-Host ""# Check Redis installation

Write-Host "Checking Redis..." -ForegroundColor YellowWrite-Host ""

try {Write-Host "Checking Redis..." -ForegroundColor Yellow

    $dockerPs = docker ps --filter "name=babocument-redis" --format "{{.Names}}" 2>&1try {

    if ($dockerPs -match "babocument-redis") {    $dockerPs = docker ps --filter "name=babocument-redis" --format "{{.Names}}" 2>&1

        Write-Host "Success Redis container is running" -ForegroundColor Green    if ($dockerPs -match "babocument-redis") {

    }        Write-Host "✓ Redis container is running" -ForegroundColor Green

    else {    }

        Write-Host "Warning Redis container not found" -ForegroundColor Yellow    else {

        Write-Host "  Start with: docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine" -ForegroundColor Yellow        Write-Host "⚠ Redis container not found" -ForegroundColor Yellow

    }        Write-Host "  Start with: docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine" -ForegroundColor Yellow

}    }

catch {}

    Write-Host "Warning Docker not found or not running" -ForegroundColor Yellowcatch {

    Write-Host "  Install Docker Desktop or use Windows Redis port" -ForegroundColor Yellow    Write-Host "⚠ Docker not found or not running" -ForegroundColor Yellow

}    Write-Host "  Install Docker Desktop or use Windows Redis port" -ForegroundColor Yellow

}

# Setup complete

Write-Host ""# Setup complete

Write-Host "==================================" -ForegroundColor CyanWrite-Host ""

Write-Host "Setup Complete!" -ForegroundColor GreenWrite-Host "==================================" -ForegroundColor Cyan

Write-Host "==================================" -ForegroundColor CyanWrite-Host "Setup Complete!" -ForegroundColor Green

Write-Host ""Write-Host "==================================" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor YellowWrite-Host ""

Write-Host "1. Ensure Ollama is running: ollama serve" -ForegroundColor WhiteWrite-Host "Next steps:" -ForegroundColor Yellow

Write-Host "2. Download models: ollama pull llama3.2:3b" -ForegroundColor WhiteWrite-Host "1. Ensure Ollama is running: " -NoNewline; Write-Host "ollama serve" -ForegroundColor White

Write-Host "3. Start Redis: docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine" -ForegroundColor WhiteWrite-Host "2. Download models: " -NoNewline; Write-Host "ollama pull llama3.2:3b" -ForegroundColor White

Write-Host "4. Run the server: python app/main.py" -ForegroundColor WhiteWrite-Host "3. Start Redis: " -NoNewline; Write-Host "docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine" -ForegroundColor White

Write-Host "5. View API docs: http://localhost:8000/docs" -ForegroundColor WhiteWrite-Host "4. Run the server: " -NoNewline; Write-Host "python app/main.py" -ForegroundColor White

Write-Host ""Write-Host "5. View API docs: " -NoNewline; Write-Host "http://localhost:8000/docs" -ForegroundColor White

Write-Host "For detailed instructions, see SETUP.md" -ForegroundColor CyanWrite-Host ""

Write-Host ""Write-Host "For detailed instructions, see SETUP.md" -ForegroundColor Cyan

Write-Host ""
